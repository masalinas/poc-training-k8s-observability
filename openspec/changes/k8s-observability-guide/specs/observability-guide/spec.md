# Spec Delta: observability-guide

## Purpose

Provides a comprehensive, publication-ready Kubernetes Observability guide and automated PDF generation tooling for training courses and workshops.

## ADDED Requirements

### Requirement: Master Observability Guide Structure
The project SHALL provide a comprehensive Markdown training guide in `docs/k8s-observabilidad.md` structured across 9 pedagogical chapters covering native CLI diagnostics, metrics, logs, distributed traces, unified Grafana correlation, chaos experimentation, and troubleshooting.

#### Scenario: Verify presence and chapter structure of guide
- **WHEN** the guide `docs/k8s-observabilidad.md` is inspected
- **THEN** it contains 9 numbered sections covering Metrics Server, Prometheus, Loki/Promtail, Jaeger all-in-one, Grafana Explore, Podinfo chaos testing, and troubleshooting

### Requirement: Publication Quality Styling and HTML Generation
The project SHALL provide a generation script in `scripts/generate_html_pdf.py` that formats the Markdown guide into a styled HTML document with typography, callouts, tables, and ASCII diagrams.

#### Scenario: Successful HTML document compilation
- **WHEN** the script `scripts/generate_html_pdf.py` is executed
- **THEN** it outputs `docs/k8s-observabilidad.html` with responsive styles, print stylesheets for A4, and semantic styling for diagrams and callouts

### Requirement: Automated PDF Compilation with Sidebar Bookmarks
The project SHALL compile the HTML document into a production-grade PDF (`k8s-observabilidad.pdf`) using headless Chrome and inject hierarchical outline bookmarks using `pypdf`.

#### Scenario: Successful PDF artifact generation
- **WHEN** `generate_html_pdf.py` completes execution
- **THEN** `k8s-observabilidad.pdf` is created at the repository root and contains an interactive PDF bookmark tree mirroring the document table of contents
