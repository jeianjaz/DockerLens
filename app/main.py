"""DockerLens — Observable Flask application with Prometheus metrics."""

import random
import time

from flask import Flask, g, jsonify, request
from prometheus_client import (
    Counter,
    Histogram,
    Info,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Prometheus Metrics (RED: Rate, Errors, Duration)
# ---------------------------------------------------------------------------

# RATE + ERRORS — Counter counts total requests, labeled by method/endpoint/status.
#   Rate  = rate(http_requests_total[5m])
#   Errors = rate(http_requests_total{status=~"5.."}[5m])
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

# DURATION — Histogram measures how long each request takes.
#   Buckets define the "bins" for latency: <10ms, <25ms, ... <10s.
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "Request latency in seconds",
    ["method", "endpoint"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)

# App info — static label, useful in Grafana dashboards
APP_INFO = Info("dockerlens", "DockerLens application info")
APP_INFO.info({"version": "1.0.0", "environment": "production"})


@app.before_request
def _start_timer():
    """Record request start time — runs before every request."""
    g.start_time = time.time()


@app.after_request
def _record_metrics(response):
    """Record RED metrics — runs after every request."""
    # Skip /metrics endpoint itself to avoid self-counting
    if request.path == "/metrics":
        return response

    elapsed = time.time() - g.start_time
    endpoint = request.path
    method = request.method
    status = str(response.status_code)

    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
    REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(elapsed)

    return response


@app.route("/metrics")
def metrics():
    """Prometheus scrape endpoint — returns all metrics in Prometheus format."""
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@app.route("/")
def index():
    """Landing page — returns service info."""
    return jsonify({
        "service": "DockerLens",
        "version": "1.0.0",
        "description": "Observable Containers with AI Alerting",
        "endpoints": {
            "/": "Service info",
            "/health": "Health check",
            "/metrics": "Prometheus metrics",
            "/api/items": "Sample CRUD (GET/POST)",
            "/api/slow": "Simulate slow response",
            "/api/error": "Simulate 500 error",
        }
    })


@app.route("/health")
def health():
    """Health check endpoint for Kubernetes liveness/readiness probes."""
    return jsonify({"status": "healthy", "timestamp": time.time()}), 200


@app.route("/api/items", methods=["GET"])
def get_items():
    """Return sample items — simulates a real API."""
    items = [
        {"id": 1, "name": "Container Alpha", "status": "running"},
        {"id": 2, "name": "Container Beta", "status": "running"},
        {"id": 3, "name": "Container Gamma", "status": "stopped"},
    ]
    # Simulate variable latency (10-50ms)
    time.sleep(random.uniform(0.01, 0.05))
    return jsonify({"items": items, "count": len(items)})


@app.route("/api/items", methods=["POST"])
def create_item():
    """Create an item — simulates write operation."""
    data = request.get_json(force=True, silent=True) or {}
    name = data.get("name", "unnamed")
    return jsonify({"id": random.randint(100, 999), "name": name, "status": "created"}), 201


@app.route("/api/slow")
def slow_endpoint():
    """Simulate a slow response (1-3 seconds) for latency alerting demos."""
    delay = random.uniform(1.0, 3.0)
    time.sleep(delay)
    return jsonify({"message": "slow response", "delay_seconds": round(delay, 2)})


@app.route("/api/error")
def error_endpoint():
    """Simulate a 500 error for error-rate alerting demos."""
    if random.random() < 0.8:
        return jsonify({"error": "Internal Server Error", "detail": "Simulated failure"}), 500
    return jsonify({"message": "Got lucky — no error this time"}), 200


# ---------------------------------------------------------------------------
# Entry point (dev only — production uses gunicorn)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
