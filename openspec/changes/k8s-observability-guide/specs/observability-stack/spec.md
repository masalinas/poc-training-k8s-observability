# Spec Delta: observability-stack

## Purpose

Defines declarative Kubernetes manifests and lightweight Helm configurations to run a complete observability laboratory without overloading cluster resources.

## ADDED Requirements

### Requirement: Metrics Server Manifests
The project SHALL provide manifests in `manifests/00-metrics-server/` to deploy Metrics Server with appropriate flags for lab environments (such as insecure TLS kubelet communication).

#### Scenario: Metrics Server deployment validation
- **WHEN** manifests in `manifests/00-metrics-server/` are applied to a Kubernetes cluster
- **THEN** `kubectl top nodes` and `kubectl top pods` return CPU and memory consumption metrics

### Requirement: Optimized Prometheus Stack Configuration
The project SHALL provide a trimmed Helm values file in `manifests/01-prometheus/values-lab.yaml` for `kube-prometheus-stack` configuring Prometheus, Node Exporter, kube-state-metrics, and Grafana while constraining resource consumption.

#### Scenario: Prometheus deployment with lab profile
- **WHEN** `kube-prometheus-stack` is installed using `values-lab.yaml`
- **THEN** Prometheus scrape loops execute with a 12-hour metric retention period and Alertmanager disabled to prevent node OOMKilled events

### Requirement: Lightweight Log Aggregation with Loki and Promtail
The project SHALL provide Helm values in `manifests/02-loki-promtail/values-lab.yaml` configuring Grafana Loki in single-binary mode and Promtail as a DaemonSet to ingest node container logs.

#### Scenario: Container log ingestion and querying
- **WHEN** Loki and Promtail are deployed using `values-lab.yaml`
- **THEN** Promtail streams container logs from `/var/log/pods` to Loki, and logs are queryable via LogQL selectors

### Requirement: Distributed Tracing with Jaeger All-in-One
The project SHALL provide a manifest in `manifests/03-jaeger/jaeger-all-in-one.yaml` deploying Jaeger all-in-one with in-memory storage and OTLP ingestion support.

#### Scenario: Jaeger deployment and trace collection
- **WHEN** `manifests/03-jaeger/jaeger-all-in-one.yaml` is applied
- **THEN** the Jaeger query UI is accessible on port 16686 and spans can be sent over standard OTLP ports

### Requirement: Chaos Demo Application and ServiceMonitor
The project SHALL provide manifests in `manifests/04-podinfo/` deploying `podinfo` alongside a `ServiceMonitor` resource to expose metrics and support controlled failure injection.

#### Scenario: Controlled incident generation
- **WHEN** HTTP traffic hits `podinfo` endpoints `/status/500`, `/delay`, or `/stress-cpu`
- **THEN** Prometheus records error and latency rate spikes while Promtail captures corresponding error log entries
