---
pretty_name: Fatawa AI Hanafi QA Benchmark
language:
- ar
task_categories:
- question-answering
size_categories:
- n<1K
tags:
- islamic-jurisprudence
- fiqh
- hanafi
- arabic
configs:
- config_name: default
  data_files:
  - split: test
    path: data/fatawa_ai_hanafi_qa_298.csv
---

# Fatawa AI Hanafi QA Benchmark

This dataset contains 298 Arabic question-answer pairs for evaluating question answering in Hanafi Islamic jurisprudence.

The public release contains only the benchmark question-answer data. It does not include model-generated answers, LLM judge scores, judge prompts, API logs, or intermediate evaluation artifacts.

## Data

The dataset is provided in both CSV and JSONL formats:

- `data/fatawa_ai_hanafi_qa_298.csv`
- `data/fatawa_ai_hanafi_qa_298.jsonl`

Both files contain the same 298 examples.

## Columns

- `benchmark_id`: Sequential benchmark row identifier.
- `source_id`: Identifier from the cleaned source collection.
- `category_ar`: Top-level Arabic category.
- `category_en`: English category label used in the paper.
- `subcategory_ar`: Arabic subcategory.
- `title_ar`: Arabic title for the fatwa question.
- `question_ar`: Arabic user question.
- `reference_answer_ar`: Arabic reference answer.

## Provenance

The benchmark was sampled from an approximately 10,000-item cleaned Hanafi fatwa source pool. The source pool was organized into a data taxonomy using an LLM- and embedding-assisted classification pipeline, then validated and corrected where necessary by a domain expert and review team. Five top-level categories were selected because each appeared at least 500 times in the source pool. A provisional sample of 300 question-answer pairs was created, with 60 examples per category; two items were excluded because of incomplete or duplicated model-output pairings in the evaluation pipeline, leaving the final 298-question benchmark.

## Intended Use

This benchmark is intended for research on retrieval, abstention, and reliability of AI systems for Islamic jurisprudence question answering. It should not be used as a standalone source of religious guidance for end users.

## License

The dataset license must be set by the dataset owners before public release.
