# ADR-001: Prometheus over Datadog for Metrics Collection

## Status
Accepted

## Date
2026-05-12

## Context

DockerLens needs a metrics collection system to monitor container health, request rates, error rates, and latency. The two main options considered were:

1. **Prometheus** — Open-source, pull-based metrics collector
2. **Datadog** — Commercial SaaS observability platform

## Decision

We chose **Prometheus** with Grafana for visualization.

## Rationale

| Factor | Prometheus | Datadog |
|--------|-----------|---------|
| **Cost** | Free / open-source | $15-23/host/month |
| **Data ownership** | Self-hosted, full control | Vendor-hosted, vendor lock-in |
| **Kubernetes native** | De facto standard, built-in service discovery | Requires agent DaemonSet |
| **Learning value** | Industry-standard skill for DevOps/SRE roles | Proprietary platform knowledge |
| **PromQL** | Powerful, transferable query language | Proprietary query syntax |
| **Community** | CNCF graduated project, massive ecosystem | Closed source |
| **Setup complexity** | More initial config | Easier initial setup (SaaS) |

### Key reasons:

1. **Cost** — Zero cost for a learning project vs. potential $100+/month for Datadog
2. **Resume impact** — Prometheus + Grafana appear in 80%+ of DevOps job descriptions
3. **Transferable skills** — PromQL, alerting rules, and Grafana dashboards apply across companies
4. **Kubernetes alignment** — Prometheus is the CNCF standard for K8s monitoring
5. **Full-stack understanding** — Self-hosting forces understanding of scraping, storage, and alerting internals

## Consequences

### Positive
- No recurring costs
- Deep understanding of metrics pipeline
- Industry-standard tooling on resume
- Portable across any infrastructure

### Negative
- More configuration than a SaaS solution
- No built-in APM (application performance monitoring) traces
- Must self-manage storage retention and scaling

## Alternatives Considered

- **Datadog** — Rejected due to cost and vendor lock-in for a learning project
- **New Relic** — Similar SaaS concerns as Datadog
- **Victoria Metrics** — Prometheus-compatible but less ecosystem support; overkill for this scale
