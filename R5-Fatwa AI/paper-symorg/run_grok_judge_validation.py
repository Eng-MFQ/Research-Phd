"""Run Grok as an automated judge on the 60 human-validation answer pairs.

Defaults target Grok 4.3 through OpenRouter.
"""

import argparse
import json
import os
import random
import re
import time
from pathlib import Path

import pandas as pd
from openai import OpenAI


SYSTEM_PROMPT = """
You are an expert evaluator for Hanafi fiqh question answering.

Your only task is to score whether the candidate answer matches the reference
answer for the same question.

Treat the reference answer as authoritative for this evaluation. Do not use your
own outside fiqh knowledge to overrule it.

Use exactly this ordinal scale:
- 1: Identical meaning / correct. The model answer reaches the same Hanafi ruling
  as the reference answer, including the same legal outcome and essential conditions.
  Extra explanation is acceptable if it does not change the ruling.
- 0: Partially correct. The model answer shares part of the correct ruling but has a
  meaningful flaw: it misses an important condition, adds an unsupported condition,
  overgeneralizes, gives unnecessary mixed-school reasoning, or changes practical
  guidance in a way that could mislead but is not the direct opposite.
- -1: Contradictory / wrong. The model answer conflicts with the reference answer in
  the main legal outcome, e.g. permissible vs impermissible, obligatory vs not
  obligatory, valid vs invalid, or otherwise opposite practical guidance.

Ignore wording, length, style, and citation differences unless they change the ruling.
Return only the JSON object requested by the schema.
""".strip()


RATING_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "fiqh_judge_rating",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "rating": {
                    "type": "integer",
                    "enum": [-1, 0, 1],
                    "description": "The evaluation score on the -1, 0, 1 scale.",
                }
            },
            "required": ["rating"],
            "additionalProperties": False,
        },
    },
}


def parse_rating(text):
    if text is None:
        return None
    text = str(text).strip()
    try:
        obj = json.loads(text)
        rating = obj.get("rating")
        if rating in (-1, 0, 1):
            return int(rating)
    except json.JSONDecodeError:
        pass

    cleaned = text.replace("*", "").replace("`", "")
    match = re.search(r'(?i)\brating\b["\']?\s*[:=]\s*["\']?([+-]?1|0)\b', cleaned)
    if match:
        return int(match.group(1).replace("+", ""))

    match = re.search(r"(?m)^\s*([+-]?1|0)\s*$", cleaned)
    if match:
        return int(match.group(1).replace("+", ""))

    return None


def build_user_prompt(row):
    return f"""
Question:
{row["question"]}

Reference answer:
{row["reference_answer"]}

Model answer:
{row["model_answer"]}
""".strip()


def call_grok(client, model, row, max_retries):
    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            extra_body = {}
            if row.get("_reasoning_effort"):
                extra_body["reasoning"] = {
                    "effort": row["_reasoning_effort"],
                    "exclude": True,
                }
            if row.get("_require_parameters"):
                extra_body["provider"] = {"require_parameters": True}

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": build_user_prompt(row)},
                ],
                temperature=0,
                max_tokens=64,
                response_format=RATING_SCHEMA if row.get("_structured_output") else {"type": "json_object"},
                extra_body=extra_body or None,
            )
            raw = response.choices[0].message.content
            score = parse_rating(raw)
            if score is None:
                raise ValueError(f"Could not parse Grok rating from: {raw!r}")
            usage = getattr(response, "usage", None)
            return raw, score, usage.model_dump() if usage is not None else None
        except Exception as exc:  # noqa: BLE001 - report provider errors verbatim.
            last_error = exc
            if getattr(exc, "status_code", None) in {402, 403}:
                break
            if attempt == max_retries:
                break
            sleep_s = min(60, (2**attempt) + random.uniform(0, 1.5))
            print(f"Retry {attempt}/{max_retries} after error: {exc}. Sleeping {sleep_s:.1f}s")
            time.sleep(sleep_s)
    raise last_error


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pairs",
        default="data/judge_validation/judge_validation_30_questions_human_scoring.csv",
        help="CSV containing validation_pair_id, question, reference_answer, and model_answer.",
    )
    parser.add_argument(
        "--out",
        default="data/judge_validation/grok_judge_validation_scores.csv",
        help="Output CSV for Grok scores.",
    )
    parser.add_argument("--model", default="x-ai/grok-4.3")
    parser.add_argument("--base-url", default="https://openrouter.ai/api/v1")
    parser.add_argument(
        "--api-key-env",
        default="OPENROUTER_API_KEY",
        help="Environment variable containing the OpenRouter API key.",
    )
    parser.add_argument(
        "--reasoning-effort",
        default="low",
        choices=["omit", "none", "minimal", "low", "medium", "high", "xhigh"],
        help=(
            "OpenRouter reasoning effort. Grok 4.3 is always a reasoning model; "
            "use omit to let the provider choose its default."
        ),
    )
    parser.add_argument(
        "--no-structured-output",
        action="store_true",
        help="Use JSON object mode instead of strict JSON schema.",
    )
    parser.add_argument(
        "--no-require-parameters",
        action="store_true",
        help="Do not ask OpenRouter to require support for structured-output parameters.",
    )
    parser.add_argument("--max-retries", type=int, default=4)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--force", action="store_true", help="Re-judge rows already present in --out.")
    args = parser.parse_args()

    api_key = os.getenv(args.api_key_env) or os.getenv("OPENROUTER_API_KEY") or os.getenv("XAI_API_KEY") or os.getenv("GROK_API_KEY")
    if not api_key:
        raise SystemExit(
            f"Set {args.api_key_env} or OPENROUTER_API_KEY before running Grok judging."
        )

    pairs = pd.read_csv(args.pairs)
    required = {"validation_pair_id", "question", "reference_answer", "model_answer"}
    missing = sorted(required - set(pairs.columns))
    if missing:
        raise ValueError(f"Missing required columns in --pairs: {missing}")

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    existing = pd.DataFrame()
    done_ids = set()
    if out_path.exists() and not args.force:
        existing = pd.read_csv(out_path)
        if "validation_pair_id" in existing.columns:
            done_ids = set(existing["validation_pair_id"].astype(str))

    rows = pairs.to_dict(orient="records")
    if args.limit is not None:
        rows = rows[: args.limit]

    client = OpenAI(
        api_key=api_key,
        base_url=args.base_url,
        default_headers={
            "HTTP-Referer": "https://github.com/Eng-MFQ/Research-Phd",
            "X-Title": "Fatawa AI Judge Validation",
        },
    )
    new_rows = []
    reasoning_effort = None if args.reasoning_effort == "omit" else args.reasoning_effort

    for index, row in enumerate(rows, start=1):
        pair_id = str(row["validation_pair_id"])
        if pair_id in done_ids:
            print(f"[{index}/{len(rows)}] skip {pair_id}")
            continue

        print(f"[{index}/{len(rows)}] judging {pair_id}")
        row["_reasoning_effort"] = reasoning_effort
        row["_structured_output"] = not args.no_structured_output
        row["_require_parameters"] = not args.no_require_parameters
        raw, score, usage = call_grok(client, args.model, row, args.max_retries)
        new_rows.append(
            {
                "validation_pair_id": pair_id,
                "grok_model": args.model,
                "provider_base_url": args.base_url,
                "reasoning_effort": args.reasoning_effort,
                "structured_output": not args.no_structured_output,
                "grok_score": score,
                "raw_grok_judgement": raw,
                "grok_usage_json": json.dumps(usage, ensure_ascii=False) if usage is not None else "",
            }
        )

        combined = pd.concat([existing, pd.DataFrame(new_rows)], ignore_index=True)
        combined.to_csv(out_path, index=False, encoding="utf-8")

    print(f"Wrote {out_path}")
    print(f"New rows: {len(new_rows)}")
    print(f"Total rows in output: {len(pd.read_csv(out_path)) if out_path.exists() else 0}")


if __name__ == "__main__":
    main()
