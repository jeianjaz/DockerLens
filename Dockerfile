# ---------- Build stage ----------
FROM python:3.12-slim AS builder

WORKDIR /build
COPY app/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------- Production stage ----------
FROM python:3.12-slim

LABEL maintainer="Jeian Jasper <obelidor.jeianjasper@gmail.com>"
LABEL description="DockerLens — Observable Flask app with Prometheus metrics"

# Security: run as non-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY app/ .

# Switch to non-root user
USER appuser

EXPOSE 8080

# Health check for Docker and Kubernetes
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

# Production: gunicorn with 2 workers
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--access-logfile", "-", "main:app"]
