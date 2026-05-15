"""Compute linear-weighted Cohen's kappa for the judge validation sample."""

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

try:
    import krippendorff
except ImportError:  # pragma: no cover - optional dependency
    krippendorff = None


LABELS = [-1, 0, 1]
SCORE_COLUMN = "human_score_-1_0_1"


def read_human_scores(path):
    path = Path(path)
    if path.suffix.lower() in {".xlsx", ".xlsm", ".xls"}:
        return pd.read_excel(path, sheet_name="human_scoring")
    return pd.read_csv(path)


def parse_score(value):
    if pd.isna(value):
        return None
    text = str(value).strip().replace("+", "")
    try:
        score = int(text)
    except ValueError:
        return None
    return score if score in LABELS else None


def linear_weighted_kappa(human_scores, judge_scores):
    label_to_index = {label: index for index, label in enumerate(LABELS)}
    matrix = np.zeros((len(LABELS), len(LABELS)), dtype=float)

    for human, judge in zip(human_scores, judge_scores):
        matrix[label_to_index[human], label_to_index[judge]] += 1

    n = matrix.sum()
    if n == 0:
        raise ValueError("No scored rows available.")

    row_marginals = matrix.sum(axis=1)
    col_marginals = matrix.sum(axis=0)
    expected = np.outer(row_marginals, col_marginals) / n

    weights = np.zeros_like(matrix)
    max_distance = len(LABELS) - 1
    for i in range(len(LABELS)):
        for j in range(len(LABELS)):
            weights[i, j] = abs(i - j) / max_distance

    observed_disagreement = (weights * matrix).sum()
    expected_disagreement = (weights * expected).sum()
    if expected_disagreement == 0:
        return 1.0, matrix
    return 1 - observed_disagreement / expected_disagreement, matrix


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--human",
        default="data/judge_validation/judge_validation_30_questions_human_scoring.xlsx",
        help="Filled human scoring workbook or CSV.",
    )
    parser.add_argument(
        "--key",
        default="data/judge_validation/judge_validation_30_questions_key.csv",
        help="Validation key CSV containing judge scores.",
    )
    parser.add_argument(
        "--judge-score-column",
        default="claude_score",
        help="Column in --key containing the automated judge score.",
    )
    parser.add_argument(
        "--judge-name",
        default="Claude",
        help="Automated judge name for printed output and report file names.",
    )
    parser.add_argument(
        "--out-dir",
        default="data/judge_validation",
        help="Directory for kappa report outputs.",
    )
    args = parser.parse_args()

    human = read_human_scores(args.human)
    key = pd.read_csv(args.key)

    if SCORE_COLUMN not in human.columns:
        raise ValueError(f"Missing required column: {SCORE_COLUMN}")

    human = human.copy()
    human["human_score"] = human[SCORE_COLUMN].apply(parse_score)
    missing = human["human_score"].isna().sum()
    if missing:
        raise ValueError(f"{missing} rows do not have a valid human score in {SCORE_COLUMN}.")

    if args.judge_score_column not in key.columns:
        raise ValueError(f"Missing judge score column in key file: {args.judge_score_column}")

    key_columns = ["validation_pair_id", args.judge_score_column]
    if "llm" in key.columns:
        key_columns.append("llm")

    merged = human.merge(
        key[key_columns],
        on="validation_pair_id",
        how="left",
        validate="one_to_one",
    )
    if merged[args.judge_score_column].isna().any():
        raise ValueError("Some validation rows do not have matching judge scores in the key file.")

    merged["judge_score"] = merged[args.judge_score_column].astype(int)
    kappa, matrix = linear_weighted_kappa(
        merged["human_score"].astype(int).tolist(),
        merged["judge_score"].tolist(),
    )

    exact_agreement = (merged["human_score"].astype(int) == merged["judge_score"]).mean()
    reliability_data = np.vstack(
        [
            merged["human_score"].astype(int).to_numpy(),
            merged["judge_score"].astype(int).to_numpy(),
        ]
    )
    krippendorff_alpha = {}
    if krippendorff is not None:
        for level in ("nominal", "ordinal", "interval"):
            krippendorff_alpha[level] = float(
                krippendorff.alpha(
                    reliability_data=reliability_data,
                    level_of_measurement=level,
                )
            )

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    judge_slug = args.judge_name.lower().replace(" ", "_")
    confusion_path = out_dir / f"judge_validation_{judge_slug}_confusion_matrix.csv"
    report_path = out_dir / f"judge_validation_{judge_slug}_kappa_report.json"

    confusion = pd.DataFrame(
        matrix.astype(int),
        index=[f"human_{label}" for label in LABELS],
        columns=[f"{judge_slug}_{label}" for label in LABELS],
    )
    confusion.to_csv(confusion_path, encoding="utf-8")

    report = {
        "n": int(len(merged)),
        "judge_name": args.judge_name,
        "judge_score_column": args.judge_score_column,
        "linear_weighted_cohens_kappa": float(kappa),
        "exact_agreement": float(exact_agreement),
        "human_score_counts": {
            str(k): int(v) for k, v in merged["human_score"].value_counts().sort_index().items()
        },
        "judge_score_counts": {
            str(k): int(v) for k, v in merged["judge_score"].value_counts().sort_index().items()
        },
        "krippendorff_alpha": krippendorff_alpha,
        "confusion_matrix_csv": str(confusion_path),
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"N={report['n']}")
    print(f"{args.judge_name} linear-weighted Cohen's kappa={kappa:.4f}")
    print(f"Exact agreement={exact_agreement:.4f}")
    if krippendorff_alpha:
        print(f"Krippendorff's alpha (ordinal)={krippendorff_alpha['ordinal']:.4f}")
    print(f"Wrote {report_path}")
    print(f"Wrote {confusion_path}")


if __name__ == "__main__":
    main()
