# African Language ASR — Compression Comparison API

> **Research presentation API for:**  
> *Algorithm Design and Mathematical Modeling for Efficient Automatic Speech Recognition in Low-Resource African Languages*

FastAPI Cloud–ready service comparing a large baseline ASR model against a proposed
efficient model (Knowledge Distillation + Low-Rank Factorisation + 8-bit Quantization)
across **isiZulu**, **Setswana**, and **Sesotho**.

---

## Results at a glance

| Metric | Baseline | Optimised |
|---|---|---|
| Model size | 85 MB | **5 MB** |
| Latency | 1 200 ms | **160 ms** |
| Throughput | 0.8× RT | **6× RT** |
| WER (isiZulu) | 18 % | 23 % (+5 %) |
| Time complexity | O(n²) | **O(n log n)** |
| Space complexity | O(p) | **O(rp)** |

---

## Project structure

```
asr-fastapi/
├── main.py                  ← FastAPI Cloud entry point
├── app/
│   ├── config.py            ← All paper constants (single source of truth)
│   ├── models.py            ← Pydantic schemas
│   ├── metrics.py           ← Pure computation helpers
│   ├── comparison.py        ← Business logic layer
│   └── routers/
│       ├── compare.py       ← GET /compare/{language}
│       ├── benchmark.py     ← GET /benchmark[/{language}]
│       ├── analysis.py      ← GET /complexity  GET /presentation
│       └── inference.py     ← POST /infer
├── tests/
│   └── test_api.py          ← 22 tests (pytest + httpx)
├── pyproject.toml
├── .env.example
└── .gitignore
```

---

## Local development

```bash
uv sync
uv run fastapi dev main.py
# open http://localhost:8000/docs
```

## Run tests

```bash
uv run pytest tests/ -v
```

## Deploy to FastAPI Cloud

```bash
uv run fastapi login
uv run fastapi deploy
```

Live at: **https://asr-fastapi.fastapicloud.dev**

---

## API endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/languages` | Supported languages |
| GET | `/compare/{language}` | Full model comparison |
| GET | `/complexity` | Time/space complexity analysis |
| GET | `/benchmark/{language}` | Dataset benchmark |
| GET | `/benchmark` | Benchmark all 3 languages |
| GET | `/presentation` | Full presentation summary |
| POST | `/infer` | Upload audio → ASR (simulated) |

`?dataset=` accepts: `NCHLT` · `CommonVoice` · `FLEURS`

---

## Mathematical foundation

| Technique | Formula | Gain |
|---|---|---|
| Low-rank factorisation | W ≈ U·Vᵀ | O(p) → O(rp) |
| Knowledge distillation | L = α·L_CE + (1−α)·L_KD | O(n²) → O(n log n) |
| 8-bit quantization | x_q = round(x/Δ) | 4× memory |
| Sample complexity | m ≥ (C/ε²)·k·log(n/δ) | O(n²) → O(k log n) |