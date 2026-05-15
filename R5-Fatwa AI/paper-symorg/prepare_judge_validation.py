"""
Prepare the 30-question human validation sample for the Fatawa AI judge study.

The human scoring workbook intentionally excludes Claude scores and model names.
Use the key CSV after annotation to merge human scores back with Claude scores.
"""

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path

import pandas as pd
from openpyxl.styles import Alignment, Font

from get_stats import parse_judgement


CATEGORIES = [
    "المعاملات والأمانات",
    "الحظر والإباحة واللباس والزينة",
    "الذكر والتزكية والأخلاق",
    "الزواج والطلاق والنفقات",
    "العبادات",
]


def question_key(row):
    return row.get("question") or row.get("user_questions") or row.get("query")


def load_clean_pairs(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    by_question = defaultdict(list)
    for index, row in enumerate(data):
        by_question[question_key(row)].append((index, row))

    pairs = []
    skipped = []
    for question, rows in by_question.items():
        llms = sorted(row.get("llm") for _, row in rows)
        if llms != ["gemini-2.5-flash", "gpt-5.1"]:
            skipped.append((question, llms))
            continue
        category = rows[0][1].get("_fatherdepartment")
        pairs.append(
            {
                "question": question,
                "category": category,
                "id": rows[0][1].get("id"),
                "rows": rows,
            }
        )
    return pairs, skipped


def sample_questions(pairs, per_category, seed):
    by_category = defaultdict(list)
    for pair in pairs:
        by_category[pair["category"]].append(pair)

    selected = []
    for offset, category in enumerate(CATEGORIES):
        candidates = sorted(
            by_category[category],
            key=lambda item: (str(item.get("id")), item["question"]),
        )
        if len(candidates) < per_category:
            raise ValueError(
                f"Category {category!r} has {len(candidates)} clean paired questions; "
                f"need {per_category}."
            )
        rng = random.Random(seed + offset)
        selected.extend(rng.sample(candidates, per_category))
    return selected


def build_outputs(selected, seed):
    human_rows = []
    key_rows = []
    question_rows = []
    response_letters = ["A", "B"]

    for q_index, pair in enumerate(selected, start=1):
        qid = f"Q{q_index:03d}"
        rows = list(pair["rows"])
        random.Random(seed * 1000 + q_index).shuffle(rows)

        first_row = rows[0][1]
        question_rows.append(
            {
                "question_sample_id": qid,
                "source_id": first_row.get("id"),
                "category": first_row.get("_fatherdepartment"),
                "son_department": first_row.get("son_department"),
                "title": first_row.get("title"),
                "question": question_key(first_row),
                "reference_answer": first_row.get("answer"),
            }
        )

        for letter, (source_index, row) in zip(response_letters, rows):
            validation_pair_id = f"{qid}_{letter}"
            human_rows.append(
                {
                    "validation_pair_id": validation_pair_id,
                    "question_sample_id": qid,
                    "category": row.get("_fatherdepartment"),
                    "son_department": row.get("son_department"),
                    "title": row.get("title"),
                    "question": question_key(row),
                    "reference_answer": row.get("answer"),
                    "model_answer": row.get("llm_answer"),
                    "human_score_-1_0_1": "",
                    "human_notes": "",
                }
            )
            key_rows.append(
                {
                    "validation_pair_id": validation_pair_id,
                    "question_sample_id": qid,
                    "source_row_index": source_index,
                    "source_id": row.get("id"),
                    "category": row.get("_fatherdepartment"),
                    "llm": row.get("llm"),
                    "claude_score": parse_judgement(row.get("llm_judgement")),
                    "raw_claude_judgement": row.get("llm_judgement"),
                    "question": question_key(row),
                }
            )

    return (
        pd.DataFrame(human_rows),
        pd.DataFrame(key_rows),
        pd.DataFrame(question_rows),
    )


def write_workbook(path, human_df, questions_df):
    instructions = pd.DataFrame(
        [
            {
                "field": "Task",
                "value": "Score each model_answer against reference_answer for the same question.",
            },
            {
                "field": "Allowed scores",
                "value": "-1 = contradictory, 0 = partially correct, 1 = identical meaning.",
            },
            {
                "field": "Blinding",
                "value": "Claude scores and model names are intentionally excluded from this workbook.",
            },
        ]
    )

    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        instructions.to_excel(writer, sheet_name="instructions", index=False)
        human_df.to_excel(writer, sheet_name="human_scoring", index=False)
        questions_df.to_excel(writer, sheet_name="selected_questions", index=False)

        workbook = writer.book
        for sheet in workbook.worksheets:
            sheet.freeze_panes = "A2"
            for row in sheet.iter_rows():
                for cell in row:
                    cell.alignment = Alignment(wrap_text=True, vertical="top")
            for cell in sheet[1]:
                cell.font = Font(bold=True)

        widths = {
            "instructions": {
                "A": 22,
                "B": 90,
            },
            "human_scoring": {
                "A": 18,
                "B": 18,
                "C": 28,
                "D": 22,
                "E": 28,
                "F": 48,
                "G": 60,
                "H": 70,
                "I": 18,
                "J": 36,
            },
            "selected_questions": {
                "A": 18,
                "B": 12,
                "C": 28,
                "D": 22,
                "E": 28,
                "F": 48,
                "G": 60,
            },
        }
        for sheet_name, columns in widths.items():
            sheet = workbook[sheet_name]
            for column, width in columns.items():
                sheet.column_dimensions[column].width = width


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data",
        default="data/results_final_llm_answers_judge_FINAL_paired_clean.json",
        help="Clean paired judge-results JSON.",
    )
    parser.add_argument(
        "--out-dir",
        default="data/judge_validation",
        help="Directory for validation outputs.",
    )
    parser.add_argument("--seed", type=int, default=20260503)
    parser.add_argument("--per-category", type=int, default=6)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    pairs, skipped = load_clean_pairs(args.data)
    selected = sample_questions(pairs, args.per_category, args.seed)
    human_df, key_df, questions_df = build_outputs(selected, args.seed)

    workbook_path = out_dir / "judge_validation_30_questions_human_scoring.xlsx"
    human_csv_path = out_dir / "judge_validation_30_questions_human_scoring.csv"
    key_csv_path = out_dir / "judge_validation_30_questions_key.csv"
    questions_csv_path = out_dir / "judge_validation_30_questions_selected.csv"
    manifest_path = out_dir / "judge_validation_manifest.json"

    write_workbook(workbook_path, human_df, questions_df)
    human_df.to_csv(human_csv_path, index=False, encoding="utf-8")
    key_df.to_csv(key_csv_path, index=False, encoding="utf-8")
    questions_df.to_csv(questions_csv_path, index=False, encoding="utf-8")

    manifest = {
        "data": args.data,
        "seed": args.seed,
        "per_category": args.per_category,
        "clean_paired_questions_available": len(pairs),
        "skipped_unpaired_questions": len(skipped),
        "selected_unique_questions": len(questions_df),
        "human_scoring_rows": len(human_df),
        "outputs": {
            "workbook": str(workbook_path),
            "human_scoring_csv": str(human_csv_path),
            "key_csv": str(key_csv_path),
            "selected_questions_csv": str(questions_csv_path),
        },
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Selected questions: {len(questions_df)}")
    print(f"Human scoring rows: {len(human_df)}")
    print(f"Wrote {workbook_path}")
    print(f"Wrote {key_csv_path}")


if __name__ == "__main__":
    main()
