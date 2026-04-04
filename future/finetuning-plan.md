# Fine-Tuning Plan

Design doc for fine-tuning a small model on the Agent Factory wiki to create a specialized agent-building assistant.

## Goal

Create a model that can answer agent-building questions accurately, grounded in the 85+ wiki articles, without needing to load the full wiki into context every time.

## Approach

### Base model selection

| Candidate | Parameters | Reasoning |
|-----------|-----------|-----------|
| Llama 3 8B | 8B | Good quality/size ratio, LoRA-friendly |
| Phi-3 mini | 3.8B | Very fast inference, good for deployment |
| Mistral 7B | 7B | Strong at instruction following |
| Qwen2 7B | 7B | Competitive performance, multilingual |

**Recommendation:** Start with Llama 3 8B via QLoRA (4-bit quantization + LoRA adapters). Fits on a single A100 or even a consumer GPU (24GB VRAM).

### Training data

From `future/synthetic-data.md` pipeline:
- ~500 Q&A pairs from wiki articles
- ~200 classification examples from good/bad examples
- ~100 summarization pairs from articles and grading reports
- **Total: ~800 training examples**

Split: 80% train (640), 10% validation (80), 10% test (80)

### Training configuration

```python
training_args = {
    "model": "meta-llama/Llama-3-8B",
    "adapter": "qlora",
    "quantization": "4bit",
    "lora_r": 16,
    "lora_alpha": 32,
    "lora_dropout": 0.05,
    "learning_rate": 2e-4,
    "epochs": 3,
    "batch_size": 4,
    "gradient_accumulation_steps": 4,
    "max_seq_length": 4096,
    "warmup_ratio": 0.1,
}
```

### Evaluation

| Metric | Method | Target |
|--------|--------|--------|
| Factual accuracy | Human evaluation on test set | > 85% correct |
| Source grounding | % of answers that correctly cite wiki source | > 90% |
| Hallucination rate | % of answers containing claims not in wiki | < 5% |
| Response quality | LLM-as-judge scoring (1-5) | > 4.0 average |
| AGENT_SPEC alignment | Answers consistent with spec anchors | > 95% |

### Infrastructure

| Component | Option | Cost estimate |
|-----------|--------|--------------|
| Training | RunPod A100 (80GB) | ~$2/hr x 2hr = ~$4 |
| Training | Google Colab Pro (A100) | ~$10/month |
| Serving | Ollama (local) | Free |
| Serving | Together.ai API | ~$0.20/M tokens |
| Serving | vLLM self-hosted | ~$0.50/hr |

### Pipeline

```
synthetic-data.md pipeline
        ↓
training_data.jsonl (800 examples)
        ↓
QLoRA fine-tuning (Llama 3 8B, ~2 GPU hours)
        ↓
Evaluation on test set
        ↓
If metrics pass → export adapter
        ↓
Merge adapter → quantized model (GGUF for Ollama)
        ↓
Deploy: Ollama locally or API endpoint
```

## Risks

- **800 examples may be insufficient** -- consider augmenting with paraphrased variants
- **Wiki updates invalidate the model** -- need retraining pipeline on wiki changes
- **Hallucination on edge cases** -- RAG fallback for questions outside training distribution
- **Evaluation quality** -- LLM-as-judge may have systematic biases

## Alternatives to fine-tuning

| Approach | Pros | Cons |
|----------|------|------|
| RAG only | No training needed, always current | Slower, needs embedding + retrieval |
| Prompt caching | Simple, uses frontier model | Cost scales with usage |
| Context stuffing | No infra | Limited to context window size |
| Fine-tuning | Fast inference, specialized | Training cost, staleness risk |

**Recommendation:** Start with RAG for immediate value, fine-tune when the wiki is stable and training data pipeline is validated.

## Status

Not yet implemented. Depends on `future/synthetic-data.md` pipeline being built first.
