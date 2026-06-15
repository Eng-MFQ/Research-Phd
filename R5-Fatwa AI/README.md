# Fatawa AI

This folder contains the current working materials for the Fatawa AI paper and dataset release.

## Current Structure

- `paper/`: canonical manuscript source and compiled PDF.
- `huggingface/fatawa-ai-hanafi-qa-298/`: Hugging Face-ready private dataset package with the 298-question Hanafi QA benchmark under the MIT License.
- `references/`: supporting reference papers used while preparing the manuscript.

Legacy `paper_source/` and `paper-symorg/` folders have been removed. The former was an old source-paper bundle and the latter was a stale SymOrg working copy with evaluation artifacts.

## Submission Target

Target venue: EUSPN 2026.

EUSPN publishes accepted papers in Elsevier Procedia Computer Science. Full papers are limited to 8 pages, including figures, tables, and references. The current manuscript in `paper/` is the canonical content draft, but it still needs conversion from the current LNCS working format to the Elsevier Procedia template before submission.

## Dataset Release

The dataset package is intentionally QA-only. It excludes model outputs, judge scores, prompts, API logs, usage/cost metadata, and intermediate evaluation artifacts.

To publish privately on Hugging Face:

```bash
cd "huggingface/fatawa-ai-hanafi-qa-298"
hf auth login
hf repos create <hf-username-or-org>/fatawa-ai-hanafi-qa-298 --repo-type dataset --private --exist-ok
hf upload <hf-username-or-org>/fatawa-ai-hanafi-qa-298 . . --repo-type dataset --commit-message "Initial private dataset release"
```

Replace `<hf-username-or-org>` with the target Hugging Face account or organization.
