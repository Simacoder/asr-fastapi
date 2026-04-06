"""
Business logic — assembles metrics into comparison payloads.
No HTTP concerns here; only pure data transformation.
"""
from __future__ import annotations
from .config import BASELINE, OPTIMIZED, LANGUAGE_WER, SUPPORTED_LANGUAGES
from .metrics import (
    compression_ratio,
    latency_speedup,
    throughput_factor,
    wer_delta_pct,
    simulate_benchmark,
)


def _resolve_language(language: str) -> str:
    """Case-insensitive match against supported languages."""
    return next(
        (lang for lang in SUPPORTED_LANGUAGES if lang.lower() == language.lower()),
        language,
    )


def build_comparison(language: str) -> tuple[dict, dict, dict]:
    lang = _resolve_language(language)
    wer = LANGUAGE_WER.get(lang, {"baseline": BASELINE["wer"], "optimized": OPTIMIZED["wer"]})

    baseline = {**BASELINE, "language": lang, "wer": wer["baseline"]}
    optimized = {**OPTIMIZED, "language": lang, "wer": wer["optimized"]}

    improvement = {
        "compression_ratio": compression_ratio(
            BASELINE["model_size_mb"], OPTIMIZED["model_size_mb"]
        ),
        "latency_improvement_x": latency_speedup(
            BASELINE["latency_ms"], OPTIMIZED["latency_ms"]
        ),
        "throughput_increase_x": throughput_factor(
            OPTIMIZED["throughput"], BASELINE["throughput"]
        ),
        "wer_degradation_pct": wer_delta_pct(wer["baseline"], wer["optimized"]),
        "size_reduction_mb": round(
            BASELINE["model_size_mb"] - OPTIMIZED["model_size_mb"], 2
        ),
        "param_reduction_x": round(
            BASELINE["params_millions"] / OPTIMIZED["params_millions"], 2
        ),
    }
    return baseline, optimized, improvement


def complexity_analysis() -> list[dict]:
    """
    Four mathematical results from the paper — presented as structured data
    for the /complexity endpoint.
    """
    return [
        {
            "technique": "Low-rank factorisation",
            "original_complexity": "O(p)",
            "reduced_complexity": "O(rp)",
            "formula": "W ≈ U·Vᵀ   (U ∈ ℝ^{m×r}, V ∈ ℝ^{n×r}, r ≪ min(m,n))",
            "explanation": (
                "Weight matrix W is approximated by two smaller matrices. "
                "Parameters reduced from O(mn) to O(r(m+n)). "
                "At rank r=5, achieves 16× parameter compression alone."
            ),
        },
        {
            "technique": "Knowledge distillation",
            "original_complexity": "O(n²)  [teacher self-attention]",
            "reduced_complexity": "O(n log n)  [student linear attention]",
            "formula": "L = α·L_CE + (1−α)·L_KD     L_KD = KL(σ(z_s/T) ‖ σ(z_t/T))",
            "explanation": (
                "Student learns from teacher's soft probability distributions. "
                "Temperature T controls knowledge transfer sharpness. "
                "α ∈ [0,1] balances hard (ground truth) vs soft (teacher) targets."
            ),
        },
        {
            "technique": "Post-training 8-bit quantization",
            "original_complexity": "O(p)  [FP32 = 4 bytes/param]",
            "reduced_complexity": "O(p/4)  [INT8 = 1 byte/param]",
            "formula": "x_q = round(x / Δ)    Δ = (x_max − x_min) / (2⁸ − 1)",
            "explanation": (
                "Weights cast from 32-bit float to 8-bit integer after training. "
                "4× memory reduction with bounded perturbation: "
                "‖f(x) − f_q(x)‖ ≤ ε where ε is controlled by scale Δ."
            ),
        },
        {
            "technique": "Sample complexity bound",
            "original_complexity": "O(n²)  [naive learning bound]",
            "reduced_complexity": "O(k log n)",
            "formula": "m ≥ (C / ε²) · k · log(n / δ)",
            "explanation": (
                "Minimum training samples for ε-WER guarantee with failure prob. δ. "
                "k = vocabulary size, n = max sequence length. "
                "Tighter than classical O(n²) VC bounds for structured speech models."
            ),
        },
    ]


def build_benchmark(language: str, dataset: str = "NCHLT") -> dict:
    lang = _resolve_language(language)
    return {"language": lang, "dataset": dataset, **simulate_benchmark(lang)}


def build_presentation() -> dict:
    per_language = []
    for lang in SUPPORTED_LANGUAGES:
        baseline, optimized, improvement = build_comparison(lang)
        per_language.append(
            {
                "language": lang,
                "baseline_wer": baseline["wer"],
                "optimized_wer": optimized["wer"],
                "baseline_size_mb": baseline["model_size_mb"],
                "optimized_size_mb": optimized["model_size_mb"],
                "baseline_latency_ms": baseline["latency_ms"],
                "optimized_latency_ms": optimized["latency_ms"],
                "wer_degradation_pct": improvement["wer_degradation_pct"],
            }
        )

    return {
        "paper_title": (
            "Algorithm Design and Mathematical Modeling for Efficient "
            "Automatic Speech Recognition in Low-Resource African Languages"
        ),
        "languages": SUPPORTED_LANGUAGES,
        "compression": "16×",
        "latency_improvement": "7.5×",
        "throughput": "6× real-time on commodity CPU",
        "wer_degradation": "5–6% (acceptable for edge deployment)",
        "model_size_baseline_mb": BASELINE["model_size_mb"],
        "model_size_optimized_mb": OPTIMIZED["model_size_mb"],
        "techniques": [
            "Knowledge Distillation (teacher → student)",
            "Low-Rank Factorisation (W ≈ UVᵀ)",
            "Post-training 8-bit Quantization",
        ],
        "math_models": [
            "L = α·L_CE + (1−α)·L_KD",
            "W ≈ U·Vᵀ,   r ≪ min(m,n)",
            "x_q = round(x/Δ),   Δ = (x_max−x_min)/255",
            "m ≥ (C/ε²)·k·log(n/δ)",
        ],
        "per_language": per_language,
        "conclusion": (
            "16× compression enables deployment on 2–4 GB mobile devices "
            "with only 5–6% WER degradation — previously impossible on commodity hardware."
        ),
    }