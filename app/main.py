"""DockerLens — Observable Flask application with Prometheus metrics."""

import random
import time

from flask import Flask, jsonify, request

app = Flask(__name__)

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
