# Tasks

## 1. Lab Manifests and Infrastructure Configurations

- [x] 1.1 Create `manifests/00-metrics-server/` with Metrics Server deployment and verify manifests validate with dry-run
- [x] 1.2 Create `manifests/01-prometheus/values-lab.yaml` with trimmed `kube-prometheus-stack` configuration (12h retention, memory limits, disabled Alertmanager)
- [x] 1.3 Create `manifests/02-loki-promtail/values-lab.yaml` with lightweight Loki and Promtail DaemonSet configuration
- [x] 1.4 Create `manifests/03-jaeger/jaeger-all-in-one.yaml` for in-memory Jaeger deployment with OTLP ports
- [x] 1.5 Create `manifests/04-podinfo/` with deployment, service, and `ServiceMonitor` for the chaos demo application

## 2. Master Observability Guide Authoring

- [x] 2.1 Author Sections 1-3 in `docs/k8s-observabilidad.md` (Fundamentos, Diagnóstico CLI nativo, `kube-prometheus-stack` optimizado)
- [x] 2.2 Author Sections 4-6 in `docs/k8s-observabilidad.md` (ServiceMonitors y PromQL, Loki y Promtail, Jaeger all-in-one)
- [x] 2.3 Author Sections 7-9 in `docs/k8s-observabilidad.md` (Correlación en Grafana Explore, Experimento de Caos con Podinfo, Producción y Troubleshooting)

## 3. Publication Toolchain and PDF Generation

- [x] 3.1 Create `scripts/generate_html_pdf.py` with embedded HTML template, corporate styles, Inter/JetBrains Mono typography, callouts, and Chrome headless compilation logic
- [x] 3.2 Add hierarchical bookmark injection using `pypdf` matching the guide's table of contents
- [x] 3.3 Execute `scripts/generate_html_pdf.py` and verify `docs/k8s-observabilidad.html` and `k8s-observabilidad.pdf` are generated with valid lateral navigation bookmarks

## Workflow follow-up

- Review generated PDF layout and verify rendering of ASCII diagrams and callout boxes.
- Run `/opsx-apply` to execute implementation tasks.
