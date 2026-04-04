# Synthetic Data Generation

Design doc for generating synthetic training data from the compiled wiki.

## Goal

Generate high-quality Q&A pairs, classification datasets, and summarization targets from the 85+ wiki articles. Use these to fine-tune a small, specialized model that can answer agent-building questions grounded in our knowledge base.

## Data types

### 1. Q&A pairs

Extract from each wiki article:
- **Factual Q&A** -- "What is a circuit breaker in agent design?" → answer from wiki
- **Comparative Q&A** -- "How does LangGraph differ from CrewAI?" → synthesize from framework-comparison.md
- **How-to Q&A** -- "How do I implement HITL gates?" → extract from course modules + concepts

**Target volume:** ~500 Q&A pairs from 85 articles (~6 per article)

### 2. Classification datasets

From the 22 examples (14 good, 8 bad):
- **Quality classification** -- given agent code/config, classify as good/bad with reasoning
- **Anti-pattern detection** -- given a code snippet, identify which anti-pattern(s) apply
- **Dimension scoring** -- given agent artifacts, predict AGENT_SPEC dimension scores

**Target volume:** ~200 classification examples

### 3. Summarization targets

- **Article summaries** -- first paragraph as target, full article as input
- **Course module summaries** -- key takeaways from each module
- **Grading report summaries** -- structured data → natural language summary

**Target volume:** ~100 summarization pairs

## Pipeline

```
wiki/ articles → extract_qa.py → qa_pairs.jsonl
                → extract_classifications.py → classifications.jsonl
                → extract_summaries.py → summaries.jsonl
                                         ↓
                              merge + deduplicate
                                         ↓
                              training_data.jsonl (~800 examples)
                                         ↓
                              fine-tune (see finetuning-plan.md)
```

## Quality controls

- Each Q&A pair must cite the source wiki article
- Answers must be factually grounded (no hallucinated claims)
- Classification examples must include both positive and negative cases
- Deduplication by semantic similarity (cosine > 0.9 = duplicate)

## Output format

JSONL with fields: `{"input": "...", "output": "...", "source": "wiki/path.md", "type": "qa|classification|summary"}`

## Status

Not yet implemented. This is a design doc for future work.
