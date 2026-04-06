from __future__ import annotations
from fastapi import APIRouter, HTTPException
from app.comparison import build_benchmark
from app.models import BenchmarkResult
from app.config import SUPPORTED_LANGUAGES

router = APIRouter(prefix="/benchmark", tags=["Benchmark"])

DATASETS = {"NCHLT", "CommonVoice", "FLEURS"}


def _validate(language: str) -> str:
    match = next(
        (l for l in SUPPORTED_LANGUAGES if l.lower() == language.lower()), None
    )
    if not match:
        raise HTTPException(
            status_code=404,
            detail=f"Language '{language}' not supported. Choose from: {SUPPORTED_LANGUAGES}",
        )
    return match


@router.get(
    "/{language}",
    response_model=BenchmarkResult,
    summary="Simulated dataset benchmark for one language",
)
def benchmark_one(language: str, dataset: str = "NCHLT"):
    """
    Simulates a benchmarking run over the NCHLT / CommonVoice / FLEURS corpus.

    Replace `simulate_benchmark()` in `app/metrics.py` with real
    model inference calls for live numbers.
    """
    if dataset not in DATASETS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown dataset '{dataset}'. Choose from: {sorted(DATASETS)}",
        )
    lang = _validate(language)
    return build_benchmark(lang, dataset)


@router.get(
    "",
    response_model=list[BenchmarkResult],
    summary="Benchmark all three languages at once",
)
def benchmark_all(dataset: str = "NCHLT"):
    """Run the benchmark simulation for isiZulu, Setswana, and Sesotho."""
    if dataset not in DATASETS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown dataset '{dataset}'. Choose from: {sorted(DATASETS)}",
        )
    return [build_benchmark(lang, dataset) for lang in SUPPORTED_LANGUAGES]