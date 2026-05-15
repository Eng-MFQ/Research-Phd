"""Summarize the completed Grok full-evaluation judge scores."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from scipy.stats import chi2 as chi2_dist


LABELS = [-1, 0, 1]


def score_counts(frame: pd.DataFrame) -> dict:
    scores = frame["grok_score"].astype(int)
    counts = scores.value_counts().reindex(LABELS, fill_value=0)
    total = int(len(frame))
    return {
        "n": total,
        "-1": int(counts[-1]),
        "0": int(counts[0]),
        "+1": int(counts[1]),
        "accuracy": float(counts[1] / total * 100),
        "partial_rate": float(counts[0] / total * 100),
        "contradictory_rate": float(counts[-1] / total * 100),
    }


def mcnemar(frame: pd.DataFrame) -> dict:
    pivot = frame.pivot(index="question_id", columns="llm", values="grok_score").dropna()
    gpt = (pivot["gpt-5.1"].astype(int) == 1).astype(int)
    gemini = (pivot["gemini-2.5-flash"].astype(int) == 1).astype(int)

    both_correct = int(((gpt == 1) & (gemini == 1)).sum())
    gpt_only = int(((gpt == 1) & (gemini == 0)).sum())
    gemini_only = int(((gpt == 0) & (gemini == 1)).sum())
    both_wrong = int(((gpt == 0) & (gemini == 0)).sum())

    if gpt_only + gemini_only == 0:
        chi2 = 0.0
        p_value = None
    else:
        chi2 = (abs(gpt_only - gemini_only) - 1) ** 2 / (gpt_only + gemini_only)
        p_value = float(chi2_dist.sf(chi2, df=1))

    return {
        "paired_questions": int(len(pivot)),
        "both_correct": both_correct,
        "gpt_only": gpt_only,
        "gemini_only": gemini_only,
        "both_wrong": both_wrong,
        "chi2_continuity_corrected": float(chi2),
        "p_value": p_value,
    }


def usage_summary(frame: pd.DataFrame) -> dict:
    usage = []
    for raw in frame["grok_usage_json"].dropna():
        if not str(raw).strip():
            continue
        try:
            usage.append(json.loads(raw))
        except json.JSONDecodeError:
            continue

    return {
        "usage_rows": len(usage),
        "total_cost": float(sum(item.get("cost") or 0 for item in usage)),
        "total_prompt_tokens": int(sum(item.get("prompt_tokens") or 0 for item in usage)),
        "total_completion_tokens": int(sum(item.get("completion_tokens") or 0 for item in usage)),
        "total_reasoning_tokens": int(
            sum(
                (item.get("completion_tokens_details") or {}).get("reasoning_tokens") or 0
                for item in usage
            )
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scores",
        default="data/grok_full_evaluation/grok_judge_scores_medium.csv",
    )
    parser.add_argument(
        "--out-dir",
        default="data/grok_full_evaluation",
    )
    args = parser.parse_args()

    scores_path = Path(args.scores)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    frame = pd.read_csv(scores_path)
    if "status" in frame.columns:
        errors = frame[frame["status"].astype(str).str.lower() != "ok"]
        if not errors.empty:
            raise ValueError(f"Cannot summarize with non-ok rows present: {len(errors)}")
    if frame["judge_row_id"].nunique() != len(frame):
        raise ValueError("Duplicate judge_row_id values present.")

    overall = {
        llm: score_counts(group)
        for llm, group in frame.groupby("llm")
    }

    category_rows = []
    for (category, llm), group in frame.groupby(["category", "llm"]):
        stats = score_counts(group)
        category_rows.append(
            {
                "category": category,
                "llm": llm,
                **stats,
            }
        )
    category_frame = pd.DataFrame(category_rows).sort_values(["category", "llm"])

    report = {
        "scores": str(scores_path),
        "rows": int(len(frame)),
        "unique_questions": int(frame["question_id"].nunique()),
        "overall": overall,
        "mcnemar": mcnemar(frame),
        "usage": usage_summary(frame),
    }

    report_path = out_dir / "grok_full_evaluation_report.json"
    category_path = out_dir / "grok_full_evaluation_by_category.csv"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    category_frame.to_csv(category_path, index=False, encoding="utf-8")

    print(f"Rows: {report['rows']}")
    print(f"Unique questions: {report['unique_questions']}")
    for llm, stats in overall.items():
        print(
            f"{llm}: N={stats['n']}, +1={stats['+1']} ({stats['accuracy']:.2f}%), "
            f"0={stats['0']} ({stats['partial_rate']:.1f}%), "
            f"-1={stats['-1']} ({stats['contradictory_rate']:.1f}%)"
        )
    mc = report["mcnemar"]
    print(
        "McNemar: "
        f"paired={mc['paired_questions']}, "
        f"GPT-only={mc['gpt_only']}, Gemini-only={mc['gemini_only']}, "
        f"chi2={mc['chi2_continuity_corrected']:.4f}, p={mc['p_value']:.4f}"
    )
    print(f"Wrote {report_path}")
    print(f"Wrote {category_path}")


if __name__ == "__main__":
    main()
