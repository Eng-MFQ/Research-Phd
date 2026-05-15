"""
Run this on Google Colab after uploading results_final_llm_answers_judge_FINAL.json.
Produces all numbers needed for the paper.

Usage:
    python get_stats.py --data /content/results_final_llm_answers_judge_FINAL.json
"""

import json
import argparse
from collections import defaultdict
from scipy.stats import chi2_contingency
import numpy as np
import re


def parse_judgement(raw):
    """Extract integer score (-1, 0, or 1) from raw judge output."""
    if raw is None:
        return None
    if isinstance(raw, int):
        return raw if raw in (-1, 0, 1) else None

    text = str(raw).strip()
    cleaned = text.replace("*", "").replace("`", "").strip()

    def coerce_score(value):
        try:
            val = int(value)
        except (TypeError, ValueError):
            return None
        return val if val in (-1, 0, 1) else None

    # Most rows are just "-1", "0", or "1", sometimes with Markdown bold.
    for line in cleaned.splitlines():
        line = line.strip()
        score = coerce_score(line.lstrip("+"))
        if score is not None:
            return score

        # Some Claude responses include a Markdown/JSON-style field:
        # "**Rating:** 0", '"Rating": -1', etc.
        match = re.search(r'(?i)\brating\b["\']?\s*[:=]\s*["\']?([+-]?1|0)\b', line)
        if match:
            return coerce_score(match.group(1).lstrip("+"))

    match = re.search(r'(?i)\brating\b["\']?\s*[:=]\s*["\']?([+-]?1|0)\b', cleaned)
    if match:
        return coerce_score(match.group(1).lstrip("+"))

    # A few responses use a heading followed by the score on the next line.
    match = re.search(r'(?is)#\s*rating\s*\n\s*([+-]?1|0)\b', cleaned)
    if match:
        return coerce_score(match.group(1).lstrip("+"))

    return None


def load_and_dedup(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    # Separate by LLM
    gpt_records = [r for r in data if r.get("llm") == "gpt-5.1"]
    gem_records = [r for r in data if r.get("llm") == "gemini-2.5-flash"]

    print(f"Raw counts  — GPT: {len(gpt_records)}, Gemini: {len(gem_records)}")

    # Deduplicate: keep first occurrence per question text
    def dedup(records):
        seen = set()
        out = []
        for r in records:
            key = r.get("question") or r.get("user_questions") or r.get("query", "")
            if key not in seen:
                seen.add(key)
                out.append(r)
        return out

    gpt_records = dedup(gpt_records)
    gem_records = dedup(gem_records)
    print(f"After dedup — GPT: {len(gpt_records)}, Gemini: {len(gem_records)}")
    return gpt_records, gem_records


def score_breakdown(records, label):
    scores = [parse_judgement(r.get("llm_judgement")) for r in records]
    scores = [s for s in scores if s is not None]
    total = len(scores)
    correct  = sum(1 for s in scores if s == 1)
    partial  = sum(1 for s in scores if s == 0)
    contra   = sum(1 for s in scores if s == -1)
    print(f"\n=== {label} (N={total}) ===")
    print(f"  +1 Identical  : {correct:3d} ({correct/total*100:.1f}%)")
    print(f"   0 Partial    : {partial:3d} ({partial/total*100:.1f}%)")
    print(f"  -1 Contradict : {contra:3d}  ({contra/total*100:.1f}%)")
    print(f"  Accuracy (only +1): {correct/total*100:.2f}%")
    return {"total": total, "correct": correct, "partial": partial,
            "contradictory": contra, "accuracy": correct/total*100}


def breakdown_by_category(records, label, cat_key="_fatherdepartment"):
    cat_stats = defaultdict(lambda: {"total": 0, "correct": 0, "partial": 0, "contra": 0})
    for r in records:
        cat = r.get(cat_key, "Unknown")
        score = parse_judgement(r.get("llm_judgement"))
        if score is None:
            continue
        cat_stats[cat]["total"] += 1
        if score == 1:
            cat_stats[cat]["correct"] += 1
        elif score == 0:
            cat_stats[cat]["partial"] += 1
        elif score == -1:
            cat_stats[cat]["contra"] += 1

    print(f"\n=== {label} — by category ===")
    print(f"{'Category':<40} {'Total':>5} {'Acc%':>6} {'+1':>4} {'0':>4} {'-1':>4}")
    print("-" * 65)
    for cat, s in sorted(cat_stats.items()):
        acc = s["correct"] / s["total"] * 100 if s["total"] else 0
        print(f"{cat:<40} {s['total']:>5} {acc:>6.1f} {s['correct']:>4} {s['partial']:>4} {s['contra']:>4}")
    return cat_stats


def mcnemar_test(gpt_records, gem_records):
    """
    Pair GPT and Gemini results by question, then run McNemar test.
    Returns the 2x2 table and p-value.
    """
    gpt_by_q = {}
    for r in gpt_records:
        q = r.get("question") or r.get("user_questions") or r.get("query", "")
        gpt_by_q[q] = parse_judgement(r.get("llm_judgement"))

    gem_by_q = {}
    for r in gem_records:
        q = r.get("question") or r.get("user_questions") or r.get("query", "")
        gem_by_q[q] = parse_judgement(r.get("llm_judgement"))

    # Pairs on shared questions
    shared = set(gpt_by_q.keys()) & set(gem_by_q.keys())
    print(f"\nPaired questions for McNemar: {len(shared)}")

    # Binary: 1 = correct (+1), 0 = not correct
    gpt_correct = {q: int(gpt_by_q[q] == 1) for q in shared if gpt_by_q[q] is not None}
    gem_correct = {q: int(gem_by_q[q] == 1) for q in shared if gem_by_q[q] is not None}
    paired_qs = set(gpt_correct.keys()) & set(gem_correct.keys())

    # 2x2 table: rows=GPT, cols=Gemini
    # [GPT+,Gem+]  [GPT+,Gem-]
    # [GPT-,Gem+]  [GPT-,Gem-]
    pp = sum(1 for q in paired_qs if gpt_correct[q]==1 and gem_correct[q]==1)
    pn = sum(1 for q in paired_qs if gpt_correct[q]==1 and gem_correct[q]==0)
    np_ = sum(1 for q in paired_qs if gpt_correct[q]==0 and gem_correct[q]==1)
    nn = sum(1 for q in paired_qs if gpt_correct[q]==0 and gem_correct[q]==0)

    table = np.array([[pp, pn], [np_, nn]])
    print(f"\nMcNemar 2x2 table (GPT rows, Gemini cols):")
    print(f"  Both correct:    {pp}")
    print(f"  GPT only:        {pn}")
    print(f"  Gemini only:     {np_}")
    print(f"  Both wrong:      {nn}")

    # McNemar statistic: (|b-c|-1)^2 / (b+c) with continuity correction
    b, c = pn, np_
    if b + c == 0:
        print("McNemar: cannot compute (no discordant pairs)")
        return table, None
    chi2 = (abs(b - c) - 1)**2 / (b + c)
    from scipy.stats import chi2 as chi2_dist
    p_value = chi2_dist.sf(chi2, df=1)
    print(f"\nMcNemar chi2 (with continuity correction) = {chi2:.4f}, p = {p_value:.4f}")
    sig = "SIGNIFICANT" if p_value < 0.05 else "NOT significant"
    print(f"Result: {sig} at alpha=0.05")
    return table, p_value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True,
                        help="Path to results_final_llm_answers_judge_FINAL.json")
    args = parser.parse_args()

    gpt, gem = load_and_dedup(args.data)

    gpt_stats = score_breakdown(gpt, "GPT-5.1")
    gem_stats = score_breakdown(gem, "Gemini-2.5-Flash")

    breakdown_by_category(gpt, "GPT-5.1")
    breakdown_by_category(gem, "Gemini-2.5-Flash")

    table, p = mcnemar_test(gpt, gem)

    print("\n" + "="*60)
    print("COPY THESE INTO THE PAPER:")
    print("="*60)
    for label, s in [("GPT-5.1", gpt_stats), ("Gemini-2.5-Flash", gem_stats)]:
        print(f"{label}: N={s['total']}, +1={s['correct']} ({s['accuracy']:.2f}%), "
              f"0={s['partial']} ({s['partial']/s['total']*100:.1f}%), "
              f"-1={s['contradictory']} ({s['contradictory']/s['total']*100:.1f}%)")
    if p is not None:
        print(f"McNemar p-value: {p:.4f} ({'significant' if p<0.05 else 'not significant'} at alpha=0.05)")


if __name__ == "__main__":
    main()
