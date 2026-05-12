# ADR-002: Helm over Kustomize for Kubernetes Packaging

## Status
Accepted

## Date
2026-05-12

## Context

DockerLens needs a way to manage Kubernetes manifests across environments (local minikube, staging, production EKS). The two main approaches are:

1. **Helm** — Template-based package manager with charts
2. **Kustomize** — Patch-based overlay system built into kubectl

## Decision

We chose **Helm 3** for Kubernetes packaging.

## Rationale

| Factor | Helm | Kustomize |
|--------|------|-----------|
| **Templating** | Full Go template engine | No templates, only patches/overlays |
| **Release management** | Built-in install/upgrade/rollback tracking | No concept of "releases" |
| **Ecosystem** | Thousands of community charts (Prometheus, Grafana, etc.) | Limited to your own manifests |
| **Conditional resources** | `{{- if .Values.autoscaling.enabled }}` | Requires separate overlay directories |
| **Industry adoption** | ~70% of K8s users (CNCF survey 2023) | ~40% (often used alongside Helm) |
| **Learning curve** | Steeper (Go templates) | Gentler (just YAML patches) |
| **Single command deploy** | `helm install myapp ./chart` | `kubectl apply -k overlays/prod` |

### Key reasons:

1. **Industry standard** — Helm is the most common K8s package manager in job postings
2. **Release lifecycle** — `helm upgrade`, `helm rollback`, `helm history` provide deployment management
3. **Parameterization** — `values.yaml` makes it trivial to configure per-environment without duplication
4. **Resume signal** — Shows experience with the dominant K8s ecosystem tool
5. **Future extensibility** — Can add chart dependencies (e.g., Prometheus sub-chart) easily

## Consequences

### Positive
- Single `values.yaml` controls all environments
- Built-in rollback on failed deployments
- Can publish chart to a registry for team reuse
- Conditional logic (e.g., enable/disable HPA)

### Negative
- Go template syntax can be hard to debug
- Rendered YAML is not easily diffable in PR reviews
- Helm adds an abstraction layer over raw K8s manifests

## Alternatives Considered

- **Kustomize** — Simpler but lacks release management; better for teams that prefer "plain YAML + patches"
- **Raw kubectl apply** — No parameterization; only suitable for single-environment use (we still keep `k8s/` folder as reference)
- **Jsonnet / cdk8s** — Too complex for this project scope; more suited for large platform teams
