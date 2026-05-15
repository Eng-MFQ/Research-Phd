"""Run Grok as the automated judge on the cleaned full evaluation set.

The script is resumable: successful rows already present in --out are skipped,
and the output CSV is checkpointed after every completed API call.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd
from openai import OpenAI

from run_grok_judge_validation import call_grok


DEFAULT_DATA = "data/results_final_llm_answers_judge_FINAL_paired_clean.json"
DEFAULT_OUT = "data/grok_full_evaluation/grok_judge_scores_medium.csv"


def slug(value: str) -> str:
    return (
        str(value)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace(".", "_")
        .replace("-", "_")
    )


def fallback_question_id(record: dict) -> str:
    material = "\n".join(
        [
            str(record.get("question", "")),
            str(record.get("answer", "")),
            str(record.get("llm", "")),
        ]
    )
    return hashlib.sha1(material.encode("utf-8")).hexdigest()[:12]


def normalize_record(record: dict, source_index: int) -> dict:
    question_id = str(record.get("id") or fallback_question_id(record))
    llm = str(record.get("llm", "unknown"))
    return {
        "judge_row_id": f"{question_id}__{slug(llm)}",
        "source_index": source_index,
        "question_id": question_id,
        "category": record.get("_fatherdepartment", ""),
        "son_department": record.get("son_department", ""),
        "title": record.get("title", ""),
        "question": record.get("question", ""),
        "reference_answer": record.get("answer", ""),
        "model_answer": record.get("llm_answer", ""),
        "llm": llm,
        "original_claude_judgement": record.get("llm_judgement", ""),
        "original_judge_model": record.get("llm_as_judge_modle", ""),
    }


def load_records(path: Path, model_filter: str | None) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    records = [normalize_record(record, index) for index, record in enumerate(data)]
    if model_filter:
        allowed = {item.strip() for item in model_filter.split(",") if item.strip()}
        records = [record for record in records if record["llm"] in allowed]
    duplicate_ids = pd.Series([record["judge_row_id"] for record in records]).duplicated()
    if duplicate_ids.any():
        dupes = [records[index]["judge_row_id"] for index, is_dup in enumerate(duplicate_ids) if is_dup]
        raise ValueError(f"Duplicate judge_row_id values in input: {dupes[:10]}")
    return records


def read_existing(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    existing = pd.read_csv(path)
    if "judge_row_id" not in existing.columns:
        raise ValueError(f"Existing output is missing judge_row_id: {path}")
    return existing.drop_duplicates(subset=["judge_row_id"], keep="last")


def save_checkpoint(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame(rows)
    if "judge_row_id" in frame.columns:
        frame = frame.drop_duplicates(subset=["judge_row_id"], keep="last")
    tmp = path.with_suffix(path.suffix + ".tmp")
    frame.to_csv(tmp, index=False, encoding="utf-8")
    tmp.replace(path)


def seed_from_validation(
    existing_rows: list[dict],
    rows_by_key: dict[tuple[str, str], dict],
    validation_pairs_path: Path,
    validation_key_path: Path,
    validation_scores_path: Path,
    args: argparse.Namespace,
) -> list[dict]:
    if not (validation_pairs_path.exists() and validation_key_path.exists() and validation_scores_path.exists()):
        return existing_rows

    existing_ids = {str(row.get("judge_row_id")) for row in existing_rows}
    pairs = pd.read_csv(validation_pairs_path)
    key = pd.read_csv(validation_key_path)
    scores = pd.read_csv(validation_scores_path)
    seeded = pairs.merge(key[["validation_pair_id", "source_id", "llm"]], on="validation_pair_id")
    seeded = seeded.merge(scores, on="validation_pair_id")

    new_rows = list(existing_rows)
    added = 0
    for row in seeded.to_dict(orient="records"):
        lookup_key = (str(row["source_id"]), str(row["llm"]))
        full_row = rows_by_key.get(lookup_key)
        if not full_row:
            continue
        judge_row_id = full_row["judge_row_id"]
        if judge_row_id in existing_ids:
            continue
        new_rows.append(
            {
                **full_row,
                "status": "ok",
                "grok_model": row.get("grok_model", args.model),
                "provider_base_url": row.get("provider_base_url", args.base_url),
                "reasoning_effort": row.get("reasoning_effort", args.reasoning_effort),
                "structured_output": row.get("structured_output", not args.no_structured_output),
                "grok_score": int(row["grok_score"]),
                "raw_grok_judgement": row.get("raw_grok_judgement", ""),
                "grok_usage_json": row.get("grok_usage_json", ""),
                "error_type": "",
                "error_message": "",
                "attempted_at_utc": datetime.now(UTC).isoformat(),
                "source": "validation_seed",
            }
        )
        existing_ids.add(judge_row_id)
        added += 1

    if added:
        print(f"Seeded {added} already-scored validation rows into the full output.")
    return new_rows


def make_client(
    api_key: str,
    base_url: str,
    enable_response_cache: bool,
    response_cache_ttl: int,
) -> OpenAI:
    headers = {
        "HTTP-Referer": "https://github.com/Eng-MFQ/Research-Phd",
        "X-Title": "Fatawa AI Full Judge Evaluation",
    }
    if enable_response_cache:
        headers["X-OpenRouter-Cache"] = "true"
        headers["X-OpenRouter-Cache-TTL"] = str(response_cache_ttl)

    return OpenAI(
        api_key=api_key,
        base_url=base_url,
        default_headers=headers,
    )


def judge_one(record: dict, args: argparse.Namespace, api_key: str) -> dict:
    started = datetime.now(UTC).isoformat()
    row = dict(record)
    row["_reasoning_effort"] = None if args.reasoning_effort == "omit" else args.reasoning_effort
    row["_structured_output"] = not args.no_structured_output
    row["_require_parameters"] = not args.no_require_parameters

    try:
        client = make_client(
            api_key,
            args.base_url,
            args.response_cache,
            args.response_cache_ttl,
        )
        raw, score, usage = call_grok(client, args.model, row, args.max_retries)
        return {
            **record,
            "status": "ok",
            "grok_model": args.model,
            "provider_base_url": args.base_url,
            "reasoning_effort": args.reasoning_effort,
            "structured_output": not args.no_structured_output,
            "grok_score": score,
            "raw_grok_judgement": raw,
            "grok_usage_json": json.dumps(usage, ensure_ascii=False) if usage is not None else "",
            "error_type": "",
            "error_message": "",
            "attempted_at_utc": started,
            "source": "api",
        }
    except Exception as exc:  # noqa: BLE001 - preserve provider/runtime failure for resume.
        return {
            **record,
            "status": "error",
            "grok_model": args.model,
            "provider_base_url": args.base_url,
            "reasoning_effort": args.reasoning_effort,
            "structured_output": not args.no_structured_output,
            "grok_score": "",
            "raw_grok_judgement": "",
            "grok_usage_json": "",
            "error_type": exc.__class__.__name__,
            "error_message": str(exc),
            "attempted_at_utc": started,
            "source": "api",
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default=DEFAULT_DATA)
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--model", default="x-ai/grok-4.3")
    parser.add_argument("--base-url", default="https://openrouter.ai/api/v1")
    parser.add_argument("--api-key-env", default="OPENROUTER_API_KEY")
    parser.add_argument(
        "--reasoning-effort",
        default="medium",
        choices=["omit", "none", "minimal", "low", "medium", "high", "xhigh"],
    )
    parser.add_argument("--concurrency", type=int, default=3)
    parser.add_argument("--max-retries", type=int, default=4)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--model-filter", default=None, help="Comma-separated LLM names to judge.")
    parser.add_argument("--force", action="store_true", help="Ignore successful rows already present in --out.")
    parser.add_argument("--stop-on-error", action="store_true")
    parser.add_argument("--no-structured-output", action="store_true")
    parser.add_argument("--no-require-parameters", action="store_true")
    parser.add_argument("--no-seed-validation", action="store_true")
    parser.add_argument(
        "--response-cache",
        action="store_true",
        help="Enable OpenRouter response caching for exact repeated requests.",
    )
    parser.add_argument(
        "--response-cache-ttl",
        type=int,
        default=86400,
        help="OpenRouter response-cache TTL in seconds for exact repeated requests.",
    )
    parser.add_argument(
        "--validation-pairs",
        default="data/judge_validation/judge_validation_30_questions_human_scoring.csv",
    )
    parser.add_argument(
        "--validation-key",
        default="data/judge_validation/judge_validation_30_questions_key.csv",
    )
    parser.add_argument(
        "--validation-scores",
        default="data/judge_validation/grok_judge_validation_scores_medium.csv",
    )
    args = parser.parse_args()

    api_key = (
        os.getenv(args.api_key_env)
        or os.getenv("OPENROUTER_API_KEY")
        or os.getenv("XAI_API_KEY")
        or os.getenv("GROK_API_KEY")
    )
    if not api_key:
        raise SystemExit(f"Set {args.api_key_env} or OPENROUTER_API_KEY before running.")

    data_path = Path(args.data)
    out_path = Path(args.out)
    records = load_records(data_path, args.model_filter)
    rows_by_key = {(record["question_id"], record["llm"]): record for record in records}

    existing_frame = pd.DataFrame() if args.force else read_existing(out_path)
    existing_rows = existing_frame.to_dict(orient="records") if not existing_frame.empty else []
    if existing_rows:
        existing_rows = [
            row
            for row in existing_rows
            if str(row.get("status", "ok")).lower() == "ok"
        ]
    if not args.no_seed_validation and not args.force:
        existing_rows = seed_from_validation(
            existing_rows,
            rows_by_key,
            Path(args.validation_pairs),
            Path(args.validation_key),
            Path(args.validation_scores),
            args,
        )
        save_checkpoint(out_path, existing_rows)

    done_ids = {
        str(row.get("judge_row_id"))
        for row in existing_rows
        if str(row.get("status", "ok")).lower() == "ok"
    }
    pending = [record for record in records if record["judge_row_id"] not in done_ids]
    if args.limit is not None:
        pending = pending[: args.limit]

    print(f"Input rows: {len(records)}")
    print(f"Already complete: {len(done_ids)}")
    print(f"Pending this run: {len(pending)}")
    print(f"Output: {out_path}")

    all_rows = list(existing_rows)
    if not pending:
        save_checkpoint(out_path, all_rows)
        print("Nothing to do.")
        return

    start_time = time.monotonic()
    completed = 0
    failures = 0
    with ThreadPoolExecutor(max_workers=max(1, args.concurrency)) as executor:
        futures = {
            executor.submit(judge_one, record, args, api_key): record["judge_row_id"]
            for record in pending
        }
        for future in as_completed(futures):
            result = future.result()
            completed += 1
            if result["status"] != "ok":
                failures += 1
            all_rows.append(result)
            save_checkpoint(out_path, all_rows)

            elapsed = max(time.monotonic() - start_time, 1)
            rate = completed / elapsed
            remaining = len(pending) - completed
            eta_min = remaining / rate / 60 if rate else 0
            print(
                f"[{completed}/{len(pending)}] {result['status']} "
                f"{result['judge_row_id']} score={result.get('grok_score', '')} "
                f"failures={failures} eta={eta_min:.1f}m"
            )
            if args.stop_on_error and result["status"] != "ok":
                raise RuntimeError(f"Stopping after failed row {result['judge_row_id']}")

    final_frame = read_existing(out_path)
    ok_count = int((final_frame["status"].astype(str).str.lower() == "ok").sum())
    error_count = int((final_frame["status"].astype(str).str.lower() == "error").sum())
    print(f"Wrote {out_path}")
    print(f"Successful rows: {ok_count}")
    print(f"Error rows: {error_count}")


if __name__ == "__main__":
    main()
