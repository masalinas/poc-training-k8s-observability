# Proposal: Kubernetes Observability Training Guide and Lab Stack

## Why

Students in Kubernetes training courses often struggle to understand observability because production stacks (such as full ELK/EFK or heavy enterprise observability platforms) consume excessive CPU/RAM and cause Out-Of-Memory (OOMKilled) failures in resource-constrained lab clusters. Furthermore, beginners lack a structured path from native CLI debugging (`kubectl top`, Stern) to declarative metrics scraping (Prometheus, ServiceMonitors), log aggregation (Loki, Promtail), and distributed tracing (Jaeger).

This change delivers a publication-grade, hands-on training guide and accompanying optimized manifests modeled after the high-standard pedagogical design of the PostgreSQL StatefulSet chapter (`k8s-postgresql-statefulset.pdf`), enabling students to diagnose realistic incidents with a low-footprint LGTM + Jaeger stack.

## What Changes

- **Observability Training Guide (`docs/k8s-observabilidad.md`)**: A complete 9-section master guide covering native diagnostics, `kube-prometheus-stack`, `Grafana Loki + Promtail`, `Jaeger all-in-one`, unified Grafana correlation (Explore split-screen), a controlled chaos experiment with `podinfo`, and production trade-offs.
- **Publication & PDF Tooling (`scripts/generate_html_pdf.py`)**: Script that compiles the guide into an editorial HTML document (`docs/k8s-observabilidad.html`) with customized typography (Inter, JetBrains Mono), callouts, diagrams, and renders `k8s-observabilidad.pdf` via headless Chrome with hierarchical sidebar bookmarks via `pypdf`.
- **Lab Manifests & Helm Profiles (`manifests/`)**:
  - `manifests/00-metrics-server/`: Deployment of Metrics Server for native `kubectl top` and HPA support.
  - `manifests/01-prometheus/values-lab.yaml`: Scaled-down `kube-prometheus-stack` values (short retention, reduced resources, disabled Alertmanager).
  - `manifests/02-loki-promtail/values-lab.yaml`: Low-footprint Loki and Promtail DaemonSet configuration for node log scraping.
  - `manifests/03-jaeger/jaeger-all-in-one.yaml`: In-memory Jaeger all-in-one deployment for tracing.
  - `manifests/04-podinfo/`: Deployment, Service, and ServiceMonitor for `podinfo` with endpoints to trigger chaos and load (`/status/500`, `/delay`, `/stress-cpu`).

## Capabilities

### New Capabilities

- `observability-guide`: Structured technical documentation and PDF generation tooling detailing the 3 pillars of observability in Kubernetes, pedagogical progression, and troubleshooting.
- `observability-stack`: Declarative lab configurations and optimized Helm values for deploying a lightweight observability stack (Metrics Server, Prometheus, Loki, Promtail, Jaeger) and a chaos target application in Kubernetes.

### Modified Capabilities

None.

## Impact

- **Documentation**: New master Markdown guide and compiled PDF asset in the repository.
- **Manifests**: Ready-to-apply Kubernetes manifests and Helm value overrides for training labs.
- **Dependencies**: Requires Python 3, `pypdf`, and Google Chrome / Chromium for compiling the final PDF artifact.
