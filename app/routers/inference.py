from __future__ import annotations
import numpy as np
from fastapi import APIRouter, UploadFile, File
from app.models import InferenceResponse

router = APIRouter(tags=["Inference"])

_SIMULATED_OUTPUTS: dict[str, str] = {
    "isizulu":  "Ngiyabonga kakhulu ngosizo lwakho",
    "setswana": "Ke a leboga thata ka thuso ya gago",
    "sesotho":  "Ke a leboha haholo ka thuso ya hau",
}


@router.post(
    "/infer",
    response_model=InferenceResponse,
    summary="Upload audio → ASR transcription (simulated)",
)
async def infer(audio: UploadFile = File(...)):
    """
    Upload a `.wav` or `.mp3` file and receive an ASR transcription.

    **This endpoint is currently simulated.**
    To connect a real model, replace the stub in `app/routers/inference.py`
    with a call to Whisper, wav2vec2, or MMS.

    The response reflects the optimised 5 MB model's expected behaviour:
    ~160 ms latency, confidence 0.88–0.95.
    """
    data = await audio.read()
    file_size_kb = round(len(data) / 1024, 2)

    # ── Replace this block with a real ASR model call ──────────────────────
    rng = np.random.default_rng(seed=42)
    language_guess = "isizulu"
    transcript = _SIMULATED_OUTPUTS.get(language_guess, "Speech recognised successfully.")
    latency = round(float(rng.normal(160, 15)), 2)
    confidence = round(float(rng.uniform(0.88, 0.95)), 3)
    # ── End stub ───────────────────────────────────────────────────────────

    return InferenceResponse(
        filename=audio.filename or "unknown",
        file_size_kb=file_size_kb,
        language_detected="isiZulu (simulated)",
        transcript=transcript,
        model="Optimised ASR — 5 MB / 8-bit quantised / 1.25M params",
        latency_ms=latency,
        confidence=confidence,
        note=(
            "Simulated response. Connect a real ASR model in "
            "app/routers/inference.py:infer() for live transcription."
        ),
    )