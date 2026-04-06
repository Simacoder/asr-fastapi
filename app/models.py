from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field
from typing import Any


class ModelMetrics(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    language: str
    model_size_mb: float = Field(..., description="On-disk size in megabytes")
    latency_ms: float = Field(..., description="End-to-end inference latency (ms)")
    wer: float = Field(..., description="Word Error Rate  [0, 1]")
    throughput: float = Field(..., description="Real-time factor (>1 = faster than live speech)")
    time_complexity: str
    space_complexity: str
    params_millions: float = Field(..., description="Trainable parameters (millions)")
    description: str


class ImprovementSummary(BaseModel):
    compression_ratio: float
    latency_improvement_x: float
    throughput_increase_x: float
    wer_degradation_pct: float
    size_reduction_mb: float
    param_reduction_x: float


class ComparisonResponse(BaseModel):
    language: str
    baseline: ModelMetrics
    optimized: ModelMetrics
    improvement: ImprovementSummary


class ComplexityEntry(BaseModel):
    technique: str
    original_complexity: str
    reduced_complexity: str
    formula: str
    explanation: str


class BenchmarkResult(BaseModel):
    language: str
    dataset: str
    baseline_latency_ms: float
    optimized_latency_ms: float
    baseline_wer: float
    optimized_wer: float
    baseline_throughput: float
    optimized_throughput: float


class InferenceResponse(BaseModel):
    filename: str
    file_size_kb: float
    language_detected: str
    transcript: str
    model: str
    latency_ms: float
    confidence: float
    note: str


class PresentationSummary(BaseModel):
    paper_title: str
    languages: list[str]
    compression: str
    latency_improvement: str
    throughput: str
    wer_degradation: str
    model_size_baseline_mb: float
    model_size_optimized_mb: float
    techniques: list[str]
    math_models: list[str]
    per_language: list[dict[str, Any]]
    conclusion: str