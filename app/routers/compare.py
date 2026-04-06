from __future__ import annotations
from fastapi import APIRouter, HTTPException
from app.comparison import build_comparison, complexity_analysis
from app.models import ComparisonResponse
from app.config import SUPPORTED_LANGUAGES

router = APIRouter(prefix="/compare", tags=["Comparison"])


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
    response_model=ComparisonResponse,
    summary="Baseline vs optimised model — full metric comparison",
)
def compare(language: str):
    """
    Returns a side-by-side comparison of the large baseline ASR model
    and the proposed efficient model for the given language.

    Includes model size, latency, WER, throughput, complexity, and
    computed improvement ratios.
    """
    lang = _validate(language)
    baseline, optimized, improvement = build_comparison(lang)
    return ComparisonResponse(
        language=lang,
        baseline=baseline,
        optimized=optimized,
        improvement=improvement,
    )