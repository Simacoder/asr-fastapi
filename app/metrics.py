"""
Pure computation helpers — no FastAPI imports here.
All formulas trace directly to the paper's mathematical model.
"""
from __future__ import annotations
import numpy as np


# ── Core metric formulas ──────────────────────────────────────────────────────

def compression_ratio(original_mb: float, compressed_mb: float) -> float:
    """Memory reduction ratio:  original / compressed."""
    return round(original_mb / compressed_mb, 2)


def latency_speedup(baseline_ms: float, optimized_ms: float) -> float:
    """How many times faster is the optimised model?"""
    return round(baseline_ms / optimized_ms, 2)


def throughput_factor(optimized: float, baseline: float) -> float:
    return round(optimized / baseline, 2)


def wer_delta_pct(baseline: float, optimized: float) -> float:
    """Absolute WER increase as a percentage."""
    return round((optimized - baseline) * 100, 2)


# ── Benchmark simulation ──────────────────────────────────────────────────────

def simulate_benchmark(language: str, n_samples: int = 60) -> dict:
    """
    Simulates a benchmarking loop over an audio corpus.

    Replace the numpy random calls with real model inference calls
    (Whisper / wav2vec2 / MMS) to get live numbers.

    The seed is language-deterministic so results are reproducible
    across API calls during a live demo.
    """
    rng = np.random.default_rng(seed=abs(hash(language)) % (2 ** 31))

    baseline_latencies = rng.normal(loc=1200, scale=80, size=n_samples)
    optimized_latencies = rng.normal(loc=160, scale=15, size=n_samples)
    baseline_wers = rng.uniform(0.15, 0.20, size=n_samples)
    optimized_wers = rng.uniform(0.20, 0.26, size=n_samples)

    return {
        "baseline_latency_ms": round(float(baseline_latencies.mean()), 2),
        "optimized_latency_ms": round(float(optimized_latencies.mean()), 2),
        "baseline_wer": round(float(baseline_wers.mean()), 4),
        "optimized_wer": round(float(optimized_wers.mean()), 4),
        "baseline_throughput": 0.8,
        "optimized_throughput": 6.0,
    }