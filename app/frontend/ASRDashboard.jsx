import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
} from "recharts";

// Reusable Card component
function Card({ children, style }) {
  return (
    <div
      style={{
        border: "1px solid #e0e0e0",
        borderRadius: 12,
        padding: 20,
        boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
        backgroundColor: "#fff",
        ...style,
      }}
    >
      {children}
    </div>
  );
}

// Card content wrapper
function CardContent({ children }) {
  return <div>{children}</div>;
}

export default function ASRDashboard() {
  const [metrics, setMetrics] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchMetrics = async () => {
    try {
      const res = await axios.get(
        "https://asr-fastapi-38dd5c03.fastapicloud.dev/benchmark"
      );
      const data = res.data.map((item) => ({
        language: item.language,
        baseline_latency: item.baseline_latency_ms,
        optimized_latency: item.optimized_latency_ms,
        baseline_wer: item.baseline_wer * 100,
        optimized_wer: item.optimized_wer * 100,
        baseline_throughput: item.baseline_throughput,
        optimized_throughput: item.optimized_throughput,
      }));
      setMetrics(data);
      setLoading(false);
    } catch (err) {
      console.error("Error fetching metrics:", err);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 5000);
    return () => clearInterval(interval);
  }, []);

  if (loading)
    return (
      <div style={{ padding: 24 }}>
        <p>Loading metrics...</p>
      </div>
    );

  return (
    <div style={{ padding: 32, fontFamily: "'Segoe UI', Tahoma, sans-serif", backgroundColor: "#f8f9fa" }}>
      <h1 style={{ fontSize: "2.2rem", marginBottom: 24, color: "#333" }}>
        ASR Model Compression — Research Dashboard
      </h1>

      <div style={{ display: "flex", gap: 16, marginBottom: 32, flexWrap: "wrap" }}>
        <Card style={{ flex: "1 1 250px", backgroundColor: "#e3f2fd" }}>
          <CardContent>
            <h3>Compression</h3>
            <p style={{ fontSize: "1.5rem", fontWeight: "bold" }}>16x</p>
            <p>85 MB → 5 MB</p>
          </CardContent>
        </Card>
        <Card style={{ flex: "1 1 250px", backgroundColor: "#fce4ec" }}>
          <CardContent>
            <h3>Latency Improvement</h3>
            <p style={{ fontSize: "1.5rem", fontWeight: "bold" }}>7.5x</p>
            <p>1200 → 160 ms</p>
          </CardContent>
        </Card>
        <Card style={{ flex: "1 1 250px", backgroundColor: "#e8f5e9" }}>
          <CardContent>
            <h3>Throughput</h3>
            <p style={{ fontSize: "1.5rem", fontWeight: "bold" }}>6x</p>
            <p>0.8 → 6.0 RT factor</p>
          </CardContent>
        </Card>
      </div>

      {/* Latency Chart */}
      <Card style={{ marginBottom: 32 }}>
        <CardContent>
          <h2>Latency per Language (ms)</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={metrics}>
              <XAxis dataKey="language" />
              <YAxis />
              <Tooltip formatter={(value) => value.toFixed(2)} />
              <Legend />
              <Line dataKey="baseline_latency" name="Baseline" stroke="#1976d2" />
              <Line dataKey="optimized_latency" name="Optimized" stroke="#43a047" />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* WER Chart */}
      <Card style={{ marginBottom: 32 }}>
        <CardContent>
          <h2>WER per Language (%)</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={metrics}>
              <XAxis dataKey="language" />
              <YAxis />
              <Tooltip formatter={(value) => value.toFixed(2)} />
              <Legend />
              <Bar dataKey="baseline_wer" name="Baseline" fill="#1976d2" />
              <Bar dataKey="optimized_wer" name="Optimized" fill="#43a047" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Throughput Chart */}
      <Card style={{ marginBottom: 32 }}>
        <CardContent>
          <h2>Throughput per Language (RT factor)</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={metrics}>
              <XAxis dataKey="language" />
              <YAxis />
              <Tooltip formatter={(value) => value.toFixed(2)} />
              <Legend />
              <Line dataKey="baseline_throughput" name="Baseline" stroke="#1976d2" />
              <Line dataKey="optimized_throughput" name="Optimized" stroke="#43a047" />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Mathematical foundations */}
      <Card style={{ marginBottom: 32 }}>
        <CardContent>
          <h2>Mathematical Foundations</h2>
          <p>{"Low-rank factorization: W ~= U*V^T (r << min(m,n))"}</p>
          <p>{"Knowledge Distillation Loss: L = alpha*L_CE + (1-alpha)*L_KD"}</p>
          <p>{"8-bit Post-training Quantization: x_q = round(x / Delta), 4x memory reduction"}</p>
          <p>{"Sample Complexity Bound: m >= (C/epsilon^2) * k * log(n/delta)"}</p>
        </CardContent>
      </Card>

      {/* Live API endpoints */}
      <Card>
        <CardContent>
          <h2>Live API Endpoints</h2>
          <ul>
            <li>
              <a href="/compare/isiZulu">GET /compare/isiZulu</a>
            </li>
            <li>
              <a href="/complexity">GET /complexity</a>
            </li>
            <li>
              <a href="/benchmark">GET /benchmark</a>
            </li>
            <li>
              <a href="/presentation">GET /presentation</a>
            </li>
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}