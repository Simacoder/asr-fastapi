"""
Full test suite — run with:  uv run pytest tests/ -v
"""
import pytest
from fastapi.testclient import TestClient
#from main import app
from app.main import app
client = TestClient(app)

LANGUAGES = ["isiZulu", "Setswana", "Sesotho"]


# ── Health ─────────────────────────────────────────────────────────────────────

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "running"
    assert "supported_languages" in data
    assert len(data["supported_languages"]) == 3


def test_languages():
    r = client.get("/languages")
    assert r.status_code == 200
    assert set(r.json()) == {"isiZulu", "Setswana", "Sesotho"}


# ── Compare ────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("lang", LANGUAGES)
def test_compare_all_languages(lang):
    r = client.get(f"/compare/{lang}")
    assert r.status_code == 200
    data = r.json()
    assert data["language"] == lang
    assert data["baseline"]["model_size_mb"] == 85.0
    assert data["optimized"]["model_size_mb"] == 5.0
    assert data["improvement"]["compression_ratio"] == 17.0
    assert data["improvement"]["latency_improvement_x"] == 7.5


def test_compare_case_insensitive():
    r = client.get("/compare/isizulu")
    assert r.status_code == 200
    assert r.json()["language"] == "isiZulu"


def test_compare_unknown_language():
    r = client.get("/compare/Swahili")
    assert r.status_code == 404
    assert "not supported" in r.json()["detail"]


def test_compare_wer_ordering():
    """Optimised WER should always be higher than baseline (it's the cost)."""
    for lang in LANGUAGES:
        data = client.get(f"/compare/{lang}").json()
        assert data["optimized"]["wer"] > data["baseline"]["wer"]


def test_compare_throughput_improvement():
    """Optimised throughput must exceed baseline."""
    for lang in LANGUAGES:
        data = client.get(f"/compare/{lang}").json()
        assert data["optimized"]["throughput"] > data["baseline"]["throughput"]


# ── Complexity ─────────────────────────────────────────────────────────────────

def test_complexity_returns_four_entries():
    r = client.get("/complexity")
    assert r.status_code == 200
    entries = r.json()
    assert len(entries) == 4


def test_complexity_contains_expected_techniques():
    entries = client.get("/complexity").json()
    techniques = {e["technique"] for e in entries}
    assert "Low-rank factorisation" in techniques
    assert "Knowledge distillation" in techniques
    assert "Post-training 8-bit quantization" in techniques
    assert "Sample complexity bound" in techniques


def test_complexity_has_formulas():
    for entry in client.get("/complexity").json():
        assert len(entry["formula"]) > 5
        assert len(entry["explanation"]) > 20


# ── Benchmark ──────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("lang", LANGUAGES)
def test_benchmark_single(lang):
    r = client.get(f"/benchmark/{lang}")
    assert r.status_code == 200
    data = r.json()
    assert data["language"] == lang
    assert data["dataset"] == "NCHLT"
    assert data["optimized_latency_ms"] < data["baseline_latency_ms"]
    assert data["optimized_wer"] > data["baseline_wer"]


def test_benchmark_all():
    r = client.get("/benchmark")
    assert r.status_code == 200
    results = r.json()
    assert len(results) == 3
    langs = {result["language"] for result in results}
    assert langs == {"isiZulu", "Setswana", "Sesotho"}


def test_benchmark_dataset_param():
    r = client.get("/benchmark/isiZulu?dataset=FLEURS")
    assert r.status_code == 200
    assert r.json()["dataset"] == "FLEURS"


def test_benchmark_invalid_dataset():
    r = client.get("/benchmark/isiZulu?dataset=invalid")
    assert r.status_code == 400


def test_benchmark_deterministic():
    """Same language should return same numbers every call (seeded RNG)."""
    r1 = client.get("/benchmark/isiZulu").json()
    r2 = client.get("/benchmark/isiZulu").json()
    assert r1["baseline_latency_ms"] == r2["baseline_latency_ms"]


# ── Presentation ───────────────────────────────────────────────────────────────

def test_presentation_shape():
    r = client.get("/presentation")
    assert r.status_code == 200
    data = r.json()
    assert data["compression"] == "16×"
    assert data["latency_improvement"] == "7.5×"
    assert len(data["per_language"]) == 3
    assert len(data["techniques"]) == 3
    assert len(data["math_models"]) == 4


def test_presentation_per_language_keys():
    per_lang = client.get("/presentation").json()["per_language"]
    required_keys = {
        "language", "baseline_wer", "optimized_wer",
        "baseline_size_mb", "optimized_size_mb",
        "baseline_latency_ms", "optimized_latency_ms",
        "wer_degradation_pct",
    }
    for entry in per_lang:
        assert required_keys.issubset(entry.keys())


# ── Inference ──────────────────────────────────────────────────────────────────

def test_infer_stub():
    fake_audio = b"RIFF" + b"\x00" * 44   # minimal WAV-like bytes
    r = client.post(
        "/infer",
        files={"audio": ("test.wav", fake_audio, "audio/wav")},
    )
    assert r.status_code == 200
    data = r.json()
    assert "transcript" in data
    assert data["latency_ms"] > 0
    assert 0 < data["confidence"] < 1
    assert "Simulated" in data["note"]