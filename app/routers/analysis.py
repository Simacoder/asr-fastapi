from __future__ import annotations
from fastapi import APIRouter
from app.comparison import complexity_analysis, build_presentation
from app.models import ComplexityEntry, PresentationSummary

router = APIRouter(tags=["Analysis"])


@router.get(
    "/complexity",
    response_model=list[ComplexityEntry],
    summary="Time and space complexity analysis for all compression techniques",
)
def complexity():
    """
    Returns the mathematical complexity breakdown for:
    1. Low-rank factorisation  (W ≈ UVᵀ)
    2. Knowledge distillation  (L = αL_CE + (1-α)L_KD)
    3. 8-bit post-training quantization
    4. Sample complexity bound (O(k log n))
    """
    return complexity_analysis()


@router.get(
    "/presentation",
    response_model=PresentationSummary,
    summary="Full presentation-ready summary — all languages and metrics",
)
def presentation():
    """
    Single endpoint returning everything needed for the research presentation:
    aggregate improvements, per-language breakdowns, techniques, and formulas.
    """
    return build_presentation()