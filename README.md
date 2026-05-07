# DockerLens — Observable Containers with AI Alerting

Containerized Flask application with full observability stack: Prometheus metrics, Grafana dashboards, alerting, Trivy security scanning, and Kubernetes deployment on EKS.

## Project Status

| Step | Description | Status |
|------|-------------|--------|
| 1 | Flask app + Dockerfile + docker-compose | 🟢 DONE |
| 2 | Prometheus metrics instrumentation | ⬜ |
| 3 | Prometheus + Grafana stack | ⬜ |
| 4 | Grafana dashboards (RED metrics) | ⬜ |
| 5 | Alert rules (high error rate, latency) | ⬜ |
| 6 | Trivy image scanning in CI | ⬜ |
| 7 | Kubernetes manifests (Deployment, Service, HPA) | ⬜ |
| 8 | Helm chart / Kustomize | ⬜ |
| 9 | Chaos test (pod kill + recovery) | ⬜ |
| 10 | EKS deploy + README + ADRs | ⬜ |

## Quick Start

```bash
# Build and run
docker compose up --build

# Test endpoints
curl http://localhost:8080/
curl http://localhost:8080/health
curl http://localhost:8080/api/items
curl http://localhost:8080/api/slow
curl http://localhost:8080/api/error
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| Application | Flask (Python 3.12) |
| Container | Docker (multi-stage, non-root) |
| Orchestration | Kubernetes (minikube / EKS) |
| Monitoring | Prometheus + Grafana |
| Alerting | AlertManager / Grafana Alerts |
| Security | Trivy (image scanning in CI) |
| CI/CD | GitHub Actions |

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service info |
| `/health` | GET | Health check (K8s probes) |
| `/metrics` | GET | Prometheus metrics |
| `/api/items` | GET | List items |
| `/api/items` | POST | Create item |
| `/api/slow` | GET | Simulate latency (1-3s) |
| `/api/error` | GET | Simulate 500 errors |

## Author

**Jeian Jasper** · [Portfolio](https://www.jeianjasper.me) · [GitHub](https://github.com/jeianjaz) · [LinkedIn](https://www.linkedin.com/in/jeianjasper/)
