"""
African Language ASR Compression Comparison API
================================================
FastAPI Cloud entry point.

FastAPI Cloud's CLI auto-discovers the `app` variable in `main.py`.
All routes are registered via routers; this file stays minimal.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import SUPPORTED_LANGUAGES
from app.routers import compare, benchmark, analysis, inference

app = FastAPI(
    title="African Language ASR — Model Compression API",
    description=(
        "Comparison service for: *Algorithm Design and Mathematical Modeling "
        "for Efficient ASR in Low-Resource African Languages*. "
        "Baseline (85 MB, O(n²)) vs Proposed (5 MB, O(n log n)) — "
        "isiZulu · Setswana · Sesotho."
    ),
    version="1.0.0",
    contact={"name": "Simanga Mchunu"},
    license_info={"name": "MIT"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(compare.router)
app.include_router(benchmark.router)
app.include_router(analysis.router)
app.include_router(inference.router)


# ── Root ───────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {
        "status": "running",
        "service": "African Language ASR Comparison API",
        "version": "1.0.0",
        "docs": "/docs",
        "supported_languages": SUPPORTED_LANGUAGES,
        "endpoints": [
            "GET  /compare/{language}",
            "GET  /complexity",
            "GET  /benchmark/{language}",
            "GET  /benchmark",
            "GET  /presentation",
            "POST /infer",
        ],
    }


@app.get("/languages", tags=["Health"])
def languages() -> list[str]:
    """Return the three supported South African languages."""
    return SUPPORTED_LANGUAGES