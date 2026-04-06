"""
Central configuration — all numeric constants come from the paper.
Change values here; the rest of the app picks them up automatically.
"""

SUPPORTED_LANGUAGES: list[str] = ["isiZulu", "Setswana", "Sesotho"]

# ── Baseline: large uncompressed transformer ──────────────────────────────────
BASELINE: dict = {
    "model_size_mb": 85.0,
    "latency_ms": 1200.0,
    "wer": 0.18,
    "throughput": 0.8,
    "time_complexity": "O(n²)",
    "space_complexity": "O(p)",
    "params_millions": 20.0,
    "description": (
        "Full-size Transformer ASR — exceeds 2–4 GB mobile RAM limit "
        "when loaded; real-time factor < 1 (cannot keep up with live speech)."
    ),
}

# ── Proposed: distillation + low-rank + 8-bit quant ──────────────────────────
OPTIMIZED: dict = {
    "model_size_mb": 5.0,
    "latency_ms": 160.0,
    "wer": 0.23,
    "throughput": 6.0,
    "time_complexity": "O(n log n)",
    "space_complexity": "O(rp)",
    "params_millions": 1.25,
    "description": (
        "Knowledge Distillation + Low-Rank Factorisation (W≈UVᵀ, r=5) "
        "+ Post-training 8-bit Quantization. Deployable on commodity CPUs."
    ),
}

# ── Per-language WER (from paper Table 2) ────────────────────────────────────
LANGUAGE_WER: dict[str, dict[str, float]] = {
    "isiZulu":  {"baseline": 0.18, "optimized": 0.23},
    "Setswana": {"baseline": 0.16, "optimized": 0.21},
    "Sesotho":  {"baseline": 0.17, "optimized": 0.22},
}