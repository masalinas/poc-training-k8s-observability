# Design: Kubernetes Observability Training Guide and Lab Architecture

## Context

See `proposal.md` for background and motivation. The goal is to provide an end-to-end observability course guide and reproducible lab manifests modeled after `poc-training-k8s-cluster-postgresql`. The lab must run on resource-constrained single-node or small multi-node Kubernetes clusters (kubeadm, k3s, kind, minikube) without triggering out-of-memory errors (`OOMKilled`).

## Goals / Non-Goals

**Goals:**
- Provide a publication-quality Markdown guide (`docs/k8s-observabilidad.md`) with 9 pedagogically structured chapters.
- Supply lightweight, ready-to-use Helm values and Kubernetes manifests in `manifests/` for Metrics Server, Prometheus, Loki, Promtail, Jaeger, and Podinfo.
- Automate styled HTML and PDF generation (`docs/k8s-observabilidad.html` and `k8s-observabilidad.pdf`) with interactive PDF sidebar outlines.
- Provide a hands-on chaos experiment connecting metrics anomalies to log lines and trace spans.

**Non-Goals:**
- Deploying production-scale multi-tenant storage backends (e.g. AWS S3, Google Cloud Storage, Thanos querier, Cortex, or Cassandra/Elasticsearch for Jaeger).
- Full enterprise alert routing with PagerDuty / Slack (Alertmanager is explicitly disabled in the lab values to conserve RAM).
- Writing a custom tracing instrumentation SDK from scratch; standard OTLP and Podinfo built-in endpoints will be used.

## Decisions

### Decision 1: Metrics Stack via `kube-prometheus-stack` with Lab Profile
- **Choice**: Use the official CNCF `kube-prometheus-stack` Helm chart with an aggressively tuned `values-lab.yaml`.
- **Rationale**: It deploys Prometheus Operator, Node Exporter, and kube-state-metrics in a single command, exposing standard Custom Resource Definitions (CRDs) like `ServiceMonitor`.
- **Lab Adjustments**:
  - Retention reduced to `12h` (default is 10d+).
  - Storage: `emptyDir` or small local PVC.
  - Alertmanager disabled (`alertmanager.enabled: false`).
  - Prometheus replica count set to 1 with memory request `256Mi` and limit `512Mi`.
- **Alternatives Considered**:
  - *Standalone Prometheus manifest*: Harder to demonstrate Kubernetes-native declarative scraping (`ServiceMonitor`).
  - *Full default Helm values*: Consumes >2GB RAM, crashing student nodes.

### Decision 2: Log Shipping with Promtail as a DaemonSet
- **Choice**: Deploy Grafana Loki (single-binary monolithic mode) and Promtail as a DaemonSet.
- **Rationale**: Promtail directly tails `/var/log/pods` with minimal CPU/RAM overhead, automatically parsing container metadata (namespace, pod name, container name) as Loki stream labels.
- **Alternatives Considered**:
  - *Elasticsearch/Logstash (ELK)*: Discarded due to heavy JVM memory requirements causing frequent OOMKills in lab environments.
  - *Grafana Alloy*: Promtail remains simpler, more ubiquitous in existing tutorials, and easier for beginners to grasp without OTel configuration DSL.

### Decision 3: Distributed Tracing with Jaeger All-in-One
- **Choice**: Deploy Jaeger All-in-One (`jaegertracing/all-in-one`) in memory.
- **Rationale**: Provides the complete UI, collector, and in-memory storage engine in a single lightweight pod (<100Mi RAM), supporting OTLP HTTP/gRPC ingestion out-of-the-box.
- **Alternatives Considered**:
  - *Grafana Tempo*: Requires object storage or local bucket simulation and extra datasource plumbing in Grafana.
  - *Production Jaeger with Elasticsearch/Cassandra*: Overkill for a lab.

### Decision 4: Target Application using `podinfo`
- **Choice**: Use Stefan Prodan's `stefanprodan/podinfo`.
- **Rationale**: Highly popular, lightweight Go microservice with built-in Prometheus `/metrics`, customizable error endpoints (`/status/500`), delay injection (`/delay/1`), and CPU load simulation (`/stress-cpu`).
- **Alternatives Considered**:
  - *Custom Python/Node app*: Adds maintenance overhead without improving pedagogical clarity.

### Decision 5: Editorial Document Compilation Pipeline
- **Choice**: Follow the `poc-training-k8s-cluster-postgresql` toolchain:
  1. Master Markdown document `docs/k8s-observabilidad.md`.
  2. Python generator `scripts/generate_html_pdf.py` writing styled HTML with embedded CSS (`@page` A4, typography, syntax highlighting, callouts, and ASCII diagram styling).
  3. Headless Chrome (`--headless --print-to-pdf`) execution.
  4. Post-processing with `pypdf` to inject interactive lateral bookmarks corresponding to document headers.
- **Alternatives Considered**:
  - *Pandoc / LaTeX*: Requires massive TeX Live installations on host machines.
  - *Marp / Weasyprint*: Chrome headless delivers superior CSS3/Paged Media fidelity matching modern web design.

## Risks / Trade-offs

- **[Risk] Host browser missing for PDF compilation** &rarr; *Mitigation*: Script searches multiple standard Chrome/Chromium paths and prints clear instructions if the binary is missing.
- **[Risk] CRD installation timeout on slow nodes** &rarr; *Mitigation*: Document steps to apply CRDs separately or use `--timeout 10m` in Helm.
- **[Risk] Node Exporter port conflicts in minikube/kind** &rarr; *Mitigation*: Configure hostNetwork and standard port 9100 with fallback options in the troubleshooting chapter.
