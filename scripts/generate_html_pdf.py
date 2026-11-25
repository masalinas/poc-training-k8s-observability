#!/usr/bin/env python3
# =============================================================================
# scripts/generate_html_pdf.py
# Genera el documento HTML profesional y compila k8s-observabilidad.pdf
# con marcadores interactivos (Document Outlines) en el panel lateral.
# =============================================================================
import os
import subprocess
import shutil

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(WORKSPACE_DIR, "docs")
HTML_PATH = os.path.join(DOCS_DIR, "k8s-observabilidad.html")
PDF_PATH = os.path.join(WORKSPACE_DIR, "k8s-observabilidad.pdf")

HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Guía Práctica de Observabilidad en Kubernetes con LGTM y Jaeger</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

    @page {
      size: A4 portrait;
      margin: 18mm 14mm 18mm 14mm;
      @bottom-right {
        content: "Página " counter(page);
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #64748b;
      }
      @bottom-left {
        content: "Curso Kubernetes - Módulo: Observabilidad y Diagnóstico con Stack LGTM y Jaeger";
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #64748b;
      }
    }

    * {
      box-sizing: border-box;
    }

    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 10pt;
      line-height: 1.55;
      color: #1e293b;
      background-color: #ffffff;
      margin: 0;
      padding: 0;
    }

    /* Portada */
    .cover {
      page-break-after: always;
      display: flex;
      flex-direction: column;
      justify-content: center;
      min-height: 90vh;
      padding: 40px 20px;
    }

    .badge-k8s {
      display: inline-block;
      align-self: flex-start;
      background-color: #e0f2fe;
      color: #0369a1;
      font-weight: 700;
      font-size: 9pt;
      padding: 6px 14px;
      border-radius: 9999px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 24px;
    }

    .cover h1 {
      font-size: 27pt;
      font-weight: 800;
      line-height: 1.15;
      color: #0f172a;
      margin: 0 0 16px 0;
    }

    .cover h1 span {
      color: #326ce5; /* K8s Blue */
    }

    .cover .subtitle {
      font-size: 13.5pt;
      font-weight: 400;
      color: #475569;
      margin-bottom: 40px;
      line-height: 1.45;
    }

    .cover-meta {
      border-top: 2px solid #e2e8f0;
      padding-top: 24px;
      margin-top: 40px;
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
    }

    .meta-item {
      font-size: 9.5pt;
    }

    .meta-label {
      color: #64748b;
      font-weight: 500;
      text-transform: uppercase;
      font-size: 8pt;
      letter-spacing: 0.05em;
    }

    .meta-val {
      color: #0f172a;
      font-weight: 600;
      margin-top: 2px;
    }

    /* Títulos */
    h2 {
      font-size: 15pt;
      font-weight: 700;
      color: #0f172a;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 6px;
      margin-top: 28px;
      margin-bottom: 14px;
      page-break-after: avoid;
    }

    .section-banner {
      background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
      color: #ffffff;
      padding: 16px 20px;
      border-radius: 8px;
      margin-top: 30px;
      margin-bottom: 20px;
      page-break-after: avoid;
    }

    .section-banner h2 {
      color: #ffffff;
      border: none;
      padding: 0;
      margin: 0;
      font-size: 15.5pt;
    }

    .section-banner p {
      color: #93c5fd;
      margin: 4px 0 0 0;
      font-size: 9pt;
    }

    h3 {
      font-size: 12pt;
      font-weight: 600;
      color: #1e3a8a;
      margin-top: 20px;
      margin-bottom: 8px;
      page-break-after: avoid;
    }

    h4 {
      font-size: 10.5pt;
      font-weight: 600;
      color: #334155;
      margin-top: 14px;
      margin-bottom: 6px;
      page-break-after: avoid;
    }

    p {
      margin-top: 0;
      margin-bottom: 10px;
    }

    ul, ol {
      margin-top: 0;
      margin-bottom: 12px;
      padding-left: 22px;
    }

    li {
      margin-bottom: 4px;
    }

    /* Bloques de Código y Diagramas */
    pre {
      background-color: #0f172a;
      color: #f8fafc;
      font-family: 'JetBrains Mono', monospace;
      font-size: 8pt;
      line-height: 1.45;
      padding: 12px 14px;
      border-radius: 6px;
      border-left: 4px solid #38bdf8;
      margin: 10px 0 14px 0;
      page-break-inside: avoid;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
      white-space: pre-wrap !important;
      word-wrap: break-word !important;
      word-break: break-all !important;
      overflow-wrap: anywhere !important;
      overflow: visible !important;
    }

    pre.ascii-diagram {
      background-color: #090d16;
      border-left: 4px solid #818cf8;
      font-size: 7.5pt;
      line-height: 1.25;
      letter-spacing: -0.02em;
    }

    code {
      font-family: 'JetBrains Mono', monospace;
      font-size: 8.5pt;
      background-color: #f1f5f9;
      color: #0f172a;
      padding: 2px 5px;
      border-radius: 4px;
      border: 1px solid #e2e8f0;
      word-break: break-all;
      overflow-wrap: anywhere;
    }

    pre code {
      background-color: transparent;
      color: inherit;
      padding: 0;
      border: none;
      font-size: inherit;
      white-space: pre-wrap !important;
      word-break: break-all !important;
      overflow-wrap: anywhere !important;
    }

    /* Cajas de Alerta */
    .alert {
      padding: 12px 14px;
      border-radius: 6px;
      margin: 14px 0;
      font-size: 9pt;
      page-break-inside: avoid;
      border-left: 4px solid;
    }

    .alert-warning {
      background-color: #fffbeb;
      border-color: #f59e0b;
      color: #92400e;
    }

    .alert-important {
      background-color: #fef2f2;
      border-color: #ef4444;
      color: #991b1b;
    }

    .alert-note {
      background-color: #f0f9ff;
      border-color: #0284c7;
      color: #075985;
    }

    .alert-tip {
      background-color: #f0fdf4;
      border-color: #22c55e;
      color: #166534;
    }

    .alert-title {
      font-weight: 700;
      margin-bottom: 4px;
      text-transform: uppercase;
      font-size: 8pt;
      letter-spacing: 0.05em;
    }

    /* Tablas */
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 14px 0;
      font-size: 8.8pt;
      page-break-inside: avoid;
    }

    th, td {
      border: 1px solid #cbd5e1;
      padding: 8px 10px;
      text-align: left;
    }

    th {
      background-color: #f8fafc;
      font-weight: 600;
      color: #0f172a;
    }

    tr:nth-child(even) td {
      background-color: #f1f5f9;
    }

    .toc {
      background-color: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 30px;
      page-break-after: always;
    }

    .toc h2 {
      margin-top: 0;
      border-bottom: 2px solid #cbd5e1;
      padding-bottom: 8px;
      font-size: 14pt;
    }

    .toc ul {
      list-style-type: none;
      padding-left: 0;
      margin-bottom: 0;
    }

    .toc > ul > li {
      font-weight: 600;
      margin-top: 10px;
    }

    .toc ul ul {
      padding-left: 20px;
      margin-top: 4px;
    }

    .toc ul ul li {
      font-weight: 400;
      font-size: 9pt;
      margin-top: 3px;
    }

    .toc a {
      color: #1e3a8a;
      text-decoration: none;
    }

    .toc a:hover {
      text-decoration: underline;
    }

    .page-break {
      page-break-after: always;
    }
  </style>
</head>
<body>

  <!-- PORTADA -->
  <div class="cover">
    <div class="badge-k8s">Curso Especializado de Kubernetes &bull; Módulo Práctico</div>
    <h1>Guía Práctica de <span>Observabilidad</span> en Kubernetes</h1>
    <div class="subtitle">
      Métricas con Prometheus, Logs Centralizados con Loki, Trazabilidad Distribuida con Jaeger y Diagnóstico de Incidentes en Tiempo Real
    </div>

    <div class="cover-meta">
      <div class="meta-item">
        <div class="meta-label">Autor & Equipo Docente</div>
        <div class="meta-val">Arquitectura Cloud Native & Kubernetes</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Entregable Oficial</div>
        <div class="meta-val"><code>k8s-observabilidad.pdf</code></div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Stack Tecnológico</div>
        <div class="meta-val">Prometheus &bull; Loki &bull; Promtail &bull; Grafana &bull; Jaeger</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">Perfil de Recursos</div>
        <div class="meta-val">Optimizado para Clústeres de Laboratorio (< 1 GB RAM)</div>
      </div>
    </div>
  </div>

  <!-- TABLA DE CONTENIDOS -->
  <div class="toc" id="toc">
    <h2>Tabla de Contenidos</h2>
    <ul>
      <li><a href="#sec1">1. Fundamentos y Modelo Mental de la Observabilidad en Kubernetes</a>
        <ul>
          <li><a href="#sec1-1">1.1 Más allá del Monitoreo Pasivo: El Triángulo de Observabilidad</a></li>
          <li><a href="#sec1-2">1.2 El Dilema de la Carga Efímera: Por Qué kubectl logs No Escala</a></li>
          <li><a href="#sec1-3">1.3 Arquitectura del Stack de Laboratorio vs. Gran Empresa</a></li>
          <li><a href="#sec1-4">1.4 Matriz Comparativa de Recursos en Entornos de Formación</a></li>
        </ul>
      </li>
      <li><a href="#sec2">2. Diagnóstico Nativo: Metrics Server y Herramientas CLI</a>
        <ul>
          <li><a href="#sec2-1">2.1 Despliegue y Validación de Metrics Server</a></li>
          <li><a href="#sec2-2">2.2 La Métrica Puntual: kubectl top nodes y kubectl top pods</a></li>
          <li><a href="#sec2-3">2.3 Escalado Automático Basado en Métricas: Horizontal Pod Autoscaler (HPA)</a></li>
          <li><a href="#sec2-4">2.4 La Terminal al Límite: Inspección con Stern y k9s</a></li>
        </ul>
      </li>
      <li><a href="#sec3">3. El Pilar de las Métricas: kube-prometheus-stack Optimizado</a>
        <ul>
          <li><a href="#sec3-1">3.1 Anatomía del Prometheus Operator y Componentes Clave</a></li>
          <li><a href="#sec3-2">3.2 Adaptación Quirúrgica de values-lab.yaml: Evitando OOMKilled</a></li>
          <li><a href="#sec3-3">3.3 El Modelo de Ingesta por Extracción (Scrape / Pull)</a></li>
          <li><a href="#sec3-4">3.4 Despliegue del Stack con Helm</a></li>
        </ul>
      </li>
      <li><a href="#sec4">4. Scraping Declarativo: ServiceMonitors y PromQL en la Práctica</a>
        <ul>
          <li><a href="#sec4-1">4.1 La Abstracción del ServiceMonitor: Selectores y Puertos</a></li>
          <li><a href="#sec4-2">4.2 Anatomía de una Métrica Prometheus y Formato OpenMetrics</a></li>
          <li><a href="#sec4-3">4.3 Consultas Esenciales en PromQL (rate, histogram_quantile, agregaciones)</a></li>
        </ul>
      </li>
      <li><a href="#sec5">5. El Pilar de los Logs: Grafana Loki y Promtail en Modo Ligero</a>
        <ul>
          <li><a href="#sec5-1">5.1 Por Qué Descartar Elasticsearch / Kibana en Laboratorios</a></li>
          <li><a href="#sec5-2">5.2 Filosofía de Indexación de Loki: Menos Metadatos, Menor Consumo</a></li>
          <li><a href="#sec5-3">5.3 Despliegue de Promtail como DaemonSet sobre /var/log/pods</a></li>
          <li><a href="#sec5-4">5.4 Consultas con LogQL: Filtros de Flujo, Parsing JSON y Métricas Derivadas</a></li>
        </ul>
      </li>
      <li><a href="#sec6">6. El Tercer Pilar: Trazabilidad Distribuida con Jaeger All-in-One</a>
        <ul>
          <li><a href="#sec6-1">6.1 Anatomía de una Traza: Traces, Spans, Context Propagation y Trace ID</a></li>
          <li><a href="#sec6-2">6.2 Despliegue de Jaeger All-in-One en Memoria</a></li>
          <li><a href="#sec6-3">6.3 Recepción de Trazas OTLP y Consulta en la Interfaz Web</a></li>
        </ul>
      </li>
      <li><a href="#sec7">7. El Centro de Mando: Correlación Multi-Pilar en Grafana</a>
        <ul>
          <li><a href="#sec7-1">7.1 Configuración de Data Sources Unificados (Prometheus, Loki, Jaeger)</a></li>
          <li><a href="#sec7-2">7.2 El Poder de la Vista Explore en Pantalla Dividida</a></li>
          <li><a href="#sec7-3">7.3 Del Trace ID al Log Exacto: Cerrando el Círculo de la Observabilidad</a></li>
        </ul>
      </li>
      <li><a href="#sec8">8. El Experimento del Caos: Diagnóstico de un Incidente Real con Podinfo</a>
        <ul>
          <li><a href="#sec8-1">8.1 Despliegue de la Aplicación de Prueba podinfo y su ServiceMonitor</a></li>
          <li><a href="#sec8-2">8.2 Inyección de Fallos Controlados: Errores 500, Latencia y Pico de CPU</a></li>
          <li><a href="#sec8-3">8.3 Resolución del Incidente en 4 Pasos Guiados</a></li>
        </ul>
      </li>
      <li><a href="#sec9">9. La Brecha hacia la Producción y Resolución de Problemas (Troubleshooting)</a>
        <ul>
          <li><a href="#sec9-1">9.1 Almacenamiento Persistente en Producción: S3/MinIO y Thanos/Cortex</a></li>
          <li><a href="#sec9-2">9.2 Error 1: Pods en Pending o CrashLoopBackOff por Falta de Recursos</a></li>
          <li><a href="#sec9-3">9.3 Error 2: ServiceMonitor No Recoge Métricas</a></li>
          <li><a href="#sec9-4">9.4 Error 3: Promtail Sin Permisos RBAC para /var/log/pods</a></li>
        </ul>
      </li>
    </ul>
  </div>

  <!-- SECCIÓN 1 -->
  <div class="section-banner" id="sec1">
    <h2>1. Fundamentos y Modelo Mental de la Observabilidad en Kubernetes</h2>
    <p>Diferencias clave entre monitoreo y observabilidad, el triángulo de datos y optimización de recursos</p>
  </div>

  <h3 id="sec1-1">1.1 Más allá del Monitoreo Pasivo: El Triángulo de Observabilidad</h3>
  <p>
    Tradicionalmente, en la administración de servidores físicos o máquinas virtuales monolíticas, el concepto de <strong>monitoreo</strong> consistía en comprobar periódicamente si un servicio estaba "vivo" mediante checks de ping, sondas TCP o consultas básicas de CPU y memoria. Si el umbral superaba el 80%, se disparaba una alarma por correo o SMS.
  </p>
  <p>
    En arquitecturas distribuidas sobre <strong>Kubernetes</strong>, este enfoque resulta totalmente insuficiente. Un clúster moderno aloja cientos de contenedores efímeros que nacen, se escalan y mueren de forma continua en milisegundos. Cuando un usuario experimenta lentitud o errores en una aplicación compuesta por múltiples microservicios, saber que "la CPU del nodo está al 45%" no responde a las preguntas críticas del negocio.
  </p>
  <p>
    La <strong>observabilidad</strong> no es una herramienta, sino una propiedad de nuestro sistema: <strong>la capacidad de deducir el estado interno de nuestras aplicaciones analizando únicamente sus salidas externas</strong>.
  </p>

  <table>
    <thead>
      <tr>
        <th>Pilar</th>
        <th>Naturaleza del Dato</th>
        <th>Pregunta que Resuelve</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Métricas</strong></td>
        <td>Series temporales numéricas agregadas (Prometheus)</td>
        <td>"¿Está ocurriendo un problema ahora? ¿Cuál es la tasa de error y tráfico?"</td>
      </tr>
      <tr>
        <td><strong>Logs</strong></td>
        <td>Eventos textuales con marca de tiempo y contexto (Loki)</td>
        <td>"¿Por qué falló exactamente? ¿Cuál es el stack trace de la app?"</td>
      </tr>
      <tr>
        <td><strong>Trazas</strong></td>
        <td>Flujo de petición end-to-end a través de servicios (Jaeger)</td>
        <td>"¿Dónde se consume el tiempo en la llamada distribuida?"</td>
      </tr>
    </tbody>
  </table>

  <h3 id="sec1-2">1.2 El Dilema de la Carga Efímera: Por Qué <code>kubectl logs</code> No Escala</h3>
  <p>
    Cuando un alumno se inicia en Kubernetes, su primera herramienta de depuración es la CLI de Kubernetes: <code>kubectl logs -f mi-pod-xyz</code>. Sin embargo, confiar exclusivamente en este mecanismo en entornos reales adolece de graves limitaciones:
  </p>
  <ul>
    <li><strong>Volatilidad Extrema:</strong> Cuando un contenedor sufre un fallo irrecuperable (ej. <code>OOMKilled</code>), los logs del contenedor previo solo son accesibles temporalmente vía <code>--previous</code>. Si el Pod vuelve a reiniciarse o es reemplazado por un Deployment, los logs se pierden irreversiblemente en el disco local del nodo trabajador.</li>
    <li><strong>Falta de Agregación:</strong> Si un microservicio cuenta con 10 réplicas distribuidas en 3 nodos, una petición HTTP errónea impactará solo en una réplica. Con <code>kubectl logs</code> el operador se ve obligado a abrir 10 terminales distintas o adivinar cuál fue el Pod afectado.</li>
    <li><strong>Sobrecarga de la API Server:</strong> Cada invocación abre un socket HTTPS persistente hacia el <code>kube-apiserver</code>, degradando severamente el rendimiento del Control Plane.</li>
  </ul>

  <div class="alert alert-warning">
    <div class="alert-title">Advertencia Crítica</div>
    En Kubernetes, los Pods deben considerarse efímeros e intercambiables. La única manera de garantizar la capacidad de auditoría y resolución de incidencias es desacoplar el almacenamiento de eventos de la vida del contenedor mediante un sistema centralizado de ingesta.
  </div>

  <h3 id="sec1-3">1.3 Arquitectura del Stack de Laboratorio vs. Gran Empresa</h3>
  <p>
    En la industria es común encontrar arquitecturas basadas en el stack <strong>ELK/EFK</strong> (Elasticsearch, Logstash/Fluentd, Kibana). Aunque potente, para un clúster de laboratorio o formación representa un grave obstáculo: requiere más de 4 GB de RAM solo para la JVM de Elasticsearch, saturando los nodos. La combinación idónea y moderna es el <strong>Stack LGTM ligero</strong> (Prometheus + Loki + Grafana) complementado con <strong>Jaeger All-in-One</strong>.
  </p>

  <pre class="ascii-diagram">
+-----------------------------------------------------------------------------------------+
|                  ARQUITECTURA DEL LABORATORIO: FLUJO DE DATOS Y COMPONENTES             |
+-----------------------------------------------------------------------------------------+

  [ NODO KUBERNETES / WORKER ]
  |
  |  +---------------------------+       +---------------------------+
  |  | Pod Aplicación (Podinfo)  |       | Kubelet / Contenedores    |
  |  | - Expone /metrics (TCP)   |       | - Vuelca logs a stdout    |
  |  | - Emite trazas OTLP       |       | - /var/log/pods/*.log     |
  |  +---------------------------+       +---------------------------+
  |               |                                    |
  |      (Scrape cada 15s)                             | (Lectura directa)
  |               v                                    v
  |  +---------------------------+       +---------------------------+
  |  | Prometheus Operator       |       | Promtail (DaemonSet)      |
  |  | (kube-prometheus-stack)   |       | (Filtra y etiqueta)       |
  |  +---------------------------+       +---------------------------+
  |               |                                    |
  +---------------+------------------------------------+----------------------------------+
                  | (Series temporales)                | (Push de Streams)
                  v                                    v
  +--------------------------------+   +--------------------------------+   +-------------+
  | Prometheus TSDB (Local Memory) |   | Grafana Loki (Single Binary)   |   | Jaeger UI   |
  +--------------------------------+   +--------------------------------+   +-------------+
                  \                                   /                            |
                   \                                 /                             |
                    v                               v                              v
  +---------------------------------------------------------------------------------------+
  | GRAFANA DASHBOARD & EXPLORE (Punto Único de Correlación: Métricas + Logs + Trazas)    |
  +---------------------------------------------------------------------------------------+
  </pre>

  <h3 id="sec1-4">1.4 Matriz Comparativa de Recursos en Entornos de Formación</h3>
  <table>
    <thead>
      <tr>
        <th>Componente</th>
        <th>Stack Enterprise Clásico</th>
        <th>Stack Ligero CNCF (Este Curso)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Métricas</strong></td>
        <td>Prometheus Clásico (10d rotación) &bull; RAM: ~1.5 GB</td>
        <td>Prometheus Operator (12h retención) &bull; RAM: ~300 MB</td>
      </tr>
      <tr>
        <td><strong>Logs</strong></td>
        <td>Elasticsearch + Logstash &bull; RAM: ~3.0 - 4.5 GB</td>
        <td>Grafana Loki + Promtail &bull; RAM: ~200 MB</td>
      </tr>
      <tr>
        <td><strong>Trazabilidad</strong></td>
        <td>Jaeger + Cassandra / ES &bull; RAM: ~2.0 GB</td>
        <td>Jaeger All-in-One (In-Memory) &bull; RAM: ~100 MB</td>
      </tr>
      <tr>
        <td><strong>Visualización</strong></td>
        <td>Kibana + Grafana duplicados &bull; RAM: ~1.2 GB</td>
        <td>Grafana Unificado (Explore view) &bull; RAM: ~150 MB</td>
      </tr>
      <tr>
        <td><strong>TOTAL CLÚSTER</strong></td>
        <td><strong>~7.7 - 9.2 GB RAM (Peligro de OOMKilled)</strong></td>
        <td><strong>~0.75 - 1.0 GB RAM (Óptimo para Labs)</strong></td>
      </tr>
    </tbody>
  </table>

  <!-- SECCIÓN 2 -->
  <div class="section-banner" id="sec2">
    <h2>2. Diagnóstico Nativo: Metrics Server y Herramientas CLI</h2>
    <p>Consumo puntual de recursos con kubectl top, bucle de control del HPA e inspección con Stern y k9s</p>
  </div>

  <h3 id="sec2-1">2.1 Despliegue y Validación de Metrics Server</h3>
  <p>
    El componente central del diagnóstico básico en Kubernetes es el <strong><code>Metrics Server</code></strong>. No almacena series temporales a largo plazo; es un agregador en memoria que consulta cada 15-60 segundos el endpoint <code>/stats/summary</code> del kubelet en cada nodo y expone los datos a través de la API estándar <code>metrics.k8s.io</code>.
  </p>
  <pre><code>kubectl apply -f manifests/00-metrics-server/metrics-server.yaml
kubectl get deployment metrics-server -n kube-system
kubectl get apiservice v1beta1.metrics.k8s.io</code></pre>

  <div class="alert alert-note">
    <div class="alert-title">Nota Técnica: Certificados Kubelet</div>
    En clústeres locales o kubeadm sin certificados firmados por una CA pública para los kubelets, <code>metrics-server</code> requiere el argumento <code>--kubelet-insecure-tls</code> para evitar errores de validación x509 al consultar los puertos 10250 de los nodos.
  </div>

  <h3 id="sec2-2">2.2 La Métrica Puntual: <code>kubectl top nodes</code> y <code>kubectl top pods</code></h3>
  <p>
    Una vez recolectadas las primeras muestras, se desbloquean los comandos de diagnóstico nativo en terminal:
  </p>
  <pre><code># Inspección de nodos
kubectl top nodes

# Inspección de pods ordenados por memoria consumida
kubectl top pods -A --sort-by=memory</code></pre>

  <h3 id="sec2-3">2.3 Escalado Automático Basado en Métricas: Horizontal Pod Autoscaler (HPA)</h3>
  <p>
    La presencia de <code>Metrics Server</code> es el requisito indispensable para que el controlador HPA pueda escalar pods dinámicamente según la carga observada:
  </p>
  <pre class="ascii-diagram">
+-----------------------------------------------------------------------------------------+
|                  BUCLE DE CONTROL DEL HORIZONTAL POD AUTOSCALER (HPA)                   |
+-----------------------------------------------------------------------------------------+

    [ Kubelet Node ] -----> [ Metrics Server ] <---- (Consulta cada 15s)                  
                                     |                                                    
                                     v                                                    
                           [ metrics.k8s.io API ]                                         
                                     |                                                    
                                     v                                                    
                     [ HPA Controller (Kube-Controller-Manager) ]                         
                                     |                                                    
                         ¿CPU actual > CPU objetivo?                                      
                               /            \                                             
                           (SÍ)              (NO)                                         
                            /                  \                                          
                           v                    v                                         
                 Escala Réplicas (Up)       Mantiene o Reduce (Down)                      
  </pre>

  <h3 id="sec2-4">2.4 La Terminal al Límite: Inspección con Stern y k9s</h3>
  <p>
    Para superar las limitaciones de <code>kubectl logs</code> en múltiples réplicas, utilizamos herramientas avanzadas de CLI:
  </p>
  <ul>
    <li><strong>Stern:</strong> Agrega logs de múltiples pods mediante regex y colorea la salida según la réplica:
      <pre><code>stern "podinfo-.*" --tail 20 --color always</code></pre>
    </li>
    <li><strong>k9s:</strong> Interfaz interactiva de terminal con navegación veloz, dashboards de CPU y lectura de eventos en tiempo real.</li>
  </ul>

  <!-- SECCIÓN 3 -->
  <div class="section-banner" id="sec3">
    <h2>3. El Pilar de las Métricas: kube-prometheus-stack Optimizado</h2>
    <p>Operador de Prometheus, ajuste quirúrgico de valores para laboratorios y scraping dinámico</p>
  </div>

  <h3 id="sec3-1">3.1 Anatomía del Prometheus Operator y Componentes Clave</h3>
  <p>
    El chart de Helm <code>kube-prometheus-stack</code> implementa el patrón operador para gestionar Prometheus declarativamente mediante Custom Resource Definitions (CRDs):
  </p>
  <ul>
    <li><strong>Prometheus Operator:</strong> Observa los recursos (<code>ServiceMonitor</code>, <code>PodMonitor</code>) y genera la configuración dinámica.</li>
    <li><strong>Prometheus TSDB:</strong> Servidor central de almacenamiento de series temporales y ejecución de PromQL.</li>
    <li><strong>Node Exporter:</strong> DaemonSet recolector de métricas de bajo nivel del sistema operativo del nodo (CPU, RAM, disco, red).</li>
    <li><strong>Kube-State-Metrics (KSM):</strong> Expone métricas sobre el estado de los objetos de Kubernetes (réplicas deseadas, pods en Pending, etc.).</li>
    <li><strong>Grafana:</strong> Motor de cuadros de mando web con paneles prediseñados para clústeres Kubernetes.</li>
  </ul>

  <h3 id="sec3-2">3.2 Adaptación Quirúrgica de <code>values-lab.yaml</code>: Evitando OOMKilled</h3>
  <p>
    En <code>manifests/01-prometheus/values-lab.yaml</code> desactivamos Alertmanager, limitamos la retención a 12 horas y configuramos el parámetro crítico <code>serviceMonitorSelectorNilUsesHelmValues: false</code> para permitir capturar cualquier ServiceMonitor del clúster sin exigir etiquetas de release específicas.
  </p>

  <div class="alert alert-important">
    <div class="alert-title">Importante: Selector de ServiceMonitors</div>
    Por defecto, Prometheus Operator solo monitoriza aquellos ServiceMonitors que incluyan la etiqueta <code>release: prometheus</code>. Al configurar <code>serviceMonitorSelectorNilUsesHelmValues: false</code>, Prometheus capturará cualquier ServiceMonitor desplegado por los alumnos en cualquier namespace.
  </div>

  <h3 id="sec3-3">3.3 El Modelo de Ingesta por Extracción (Scrape / Pull)</h3>
  <p>
    Prometheus utiliza un modelo <strong>Pull</strong>: cada 15 segundos realiza peticiones HTTP GET contra el endpoint <code>/metrics</code> expuesto por los contenedores, registrando los datos en su base de datos TSDB local.
  </p>

  <h3 id="sec3-4">3.4 Despliegue del Stack con Helm</h3>
  <pre><code>kubectl create namespace observability
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace observability \
  --values manifests/01-prometheus/values-lab.yaml</code></pre>

  <!-- SECCIÓN 4 -->
  <div class="section-banner" id="sec4">
    <h2>4. Scraping Declarativo: ServiceMonitors y PromQL en la Práctica</h2>
    <p>Conexión declarativa de servicios, formato OpenMetrics y consultas fundamentales en PromQL</p>
  </div>

  <h3 id="sec4-1">4.1 La Abstracción del <code>ServiceMonitor</code>: Selectores y Puertos</h3>
  <p>
    Un <code>ServiceMonitor</code> asocia declarativamente el servidor de Prometheus con los Pods de una aplicación a través de las etiquetas del Service de Kubernetes:
  </p>
  <pre class="ascii-diagram">
+-----------------------------------------------------------------------------------------+
|                  CÓMO EL SERVICEMONITOR VINCULA PROMETHEUS CON EL POD                   |
+-----------------------------------------------------------------------------------------+

  [ ServiceMonitor ]
  - selector: matchLabels: app.kubernetes.io/name: podinfo
  - endpoints: - port: http, path: /metrics
          |
          | (1. Busca servicios que coincidan con las etiquetas)
          v
  [ Kubernetes Service (ClusterIP) ]
  - labels: app.kubernetes.io/name: podinfo
  - port: 9898 (name: http) ----> targetPort: 9898
          |
          | (2. Encuentra los Endpoints activos)
          v
  [ Pods de la Aplicación: podinfo-xxx ]
  - IP del Pod: 10.244.1.45:9898/metrics <------- (3. Prometheus realiza el scrape HTTP GET)
  </pre>

  <h3 id="sec4-2">4.2 Anatomía de una Métrica Prometheus y Formato OpenMetrics</h3>
  <p>
    Las métricas en formato texto plano contienen nombre, tipo (Counter, Gauge, Histogram), etiquetas de dimensionalidad y valor numérico:
  </p>
  <pre><code># TYPE http_requests_total counter
http_requests_total{handler="/status/500",method="GET",status="500"} 42</code></pre>

  <h3 id="sec4-3">4.3 Consultas Esenciales en PromQL (rate, histogram_quantile, agregaciones)</h3>
  <ul>
    <li><strong>Tasa de Peticiones por Segundo (RPS):</strong>
      <pre><code>rate(http_requests_total{namespace="default"}[5m])</code></pre>
    </li>
    <li><strong>Suma de Errores HTTP 5xx Agregada por Handler:</strong>
      <pre><code>sum(rate(http_requests_total{status=~"5.."}[2m])) by (app, handler)</code></pre>
    </li>
    <li><strong>Porcentaje Relativo de Errores:</strong>
      <pre><code>(sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))) * 100</code></pre>
    </li>
    <li><strong>Latencia Percentil 99 (P99) sobre Histogramas:</strong>
      <pre><code>histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))</code></pre>
    </li>
  </ul>

  <!-- SECCIÓN 5 -->
  <div class="section-banner" id="sec5">
    <h2>5. El Pilar de los Logs: Grafana Loki y Promtail en Modo Ligero</h2>
    <p>Indexación de metadatos, recolección de logs con DaemonSet y consultas avanzadas con LogQL</p>
  </div>

  <h3 id="sec5-1">5.1 Por Qué Descartar Elasticsearch / Kibana en Laboratorios</h3>
  <p>
    Elasticsearch requiere una máquina virtual Java pesada y crea índices invertidos de texto completo para cada palabra. En entornos de laboratorio, esto satura el disco con IOPS excesivas y provoca caídas constantes por falta de memoria.
  </p>

  <h3 id="sec5-2">5.2 Filosofía de Indexación de Loki: Menos Metadatos, Menor Consumo</h3>
  <p>
    <strong>Grafana Loki no indexa el texto del log</strong>; únicamente indexa los metadatos de Kubernetes (namespace, pod, container). Los mensajes se almacenan comprimidos en bloques. La búsqueda ejecuta un <code>grep</code> distribuido ultra-rápido en memoria, reduciendo el consumo de RAM hasta un 90%.
  </p>

  <h3 id="sec5-3">5.3 Despliegue de Promtail como DaemonSet sobre <code>/var/log/pods</code></h3>
  <p>
    Promtail corre en cada nodo físico, montando <code>/var/log/pods</code> en modo solo lectura para enviar los logs estructurados directamente a Loki:
  </p>
  <pre><code>helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

helm install loki grafana/loki-stack \
  --namespace observability \
  --values manifests/02-loki-promtail/values-lab.yaml</code></pre>

  <h3 id="sec5-4">5.4 Consultas con LogQL: Filtros de Flujo, Parsing JSON y Métricas Derivadas</h3>
  <ul>
    <li>Filtro por flujo y texto:
      <pre><code>{namespace="default", app="podinfo"} |= "error" != "debug"</code></pre>
    </li>
    <li>Parseo automático de JSON y filtro numérico:
      <pre><code>{namespace="default", app="podinfo"} | json | status >= 500</code></pre>
    </li>
    <li>Conversión de eventos de log en métricas en tiempo real:
      <pre><code>sum(rate({namespace="default", app="podinfo"} |= "error" [1m])) by (pod)</code></pre>
    </li>
  </ul>

  <!-- SECCIÓN 6 -->
  <div class="section-banner" id="sec6">
    <h2>6. El Tercer Pilar: Trazabilidad Distribuida con Jaeger All-in-One</h2>
    <p>Context Propagation, arquitectura de spans y despliegue ligero en memoria</p>
  </div>

  <h3 id="sec6-1">6.1 Anatomía de una Traza: Traces, Spans, Context Propagation y Trace ID</h3>
  <p>
    En arquitecturas de microservicios, el rastreo distribuido permite entender la latencia exacta de cada servicio participante en una transacción:
  </p>
  <pre class="ascii-diagram">
+-----------------------------------------------------------------------------------------+
|                  ANATOMÍA DE UNA TRAZA DISTRIBUIDA (TRACE & SPANS)                      |
+-----------------------------------------------------------------------------------------+

  Trace ID: 7c4b6e8a0f... (Duración Total: 280ms)
  
  [ Span 1: API Gateway (GET /order/102) ] -------------------------------------> [280ms]
      |
      +---> [ Span 2: Auth Service (Validate JWT) ] ------> [45ms]
      |
      +---> [ Span 3: Order Service (Process Order) ] --------------------------> [210ms]
                |
                +---> [ Span 4: Postgres DB (SELECT * FROM orders) ] -> [80ms]
                |
                +---> [ Span 5: Payment Service (Charge Card) ] ------> [115ms]
  </pre>

  <h3 id="sec6-2">6.2 Despliegue de Jaeger All-in-One en Memoria</h3>
  <p>
    Empaquetado en un único ejecutable en memoria (<100MB RAM) con recolector OTLP y UI web:
  </p>
  <pre><code>kubectl apply -f manifests/03-jaeger/jaeger-all-in-one.yaml
kubectl get pods -n observability -l "app.kubernetes.io/name=jaeger"</code></pre>

  <h3 id="sec6-3">6.3 Recepción de Trazas OTLP y Consulta en la Interfaz Web</h3>
  <p>
    Acceso a la interfaz gráfica en el puerto 16686:
  </p>
  <pre><code>kubectl port-forward svc/jaeger-query 16686:16686 -n observability</code></pre>

  <!-- SECCIÓN 7 -->
  <div class="section-banner" id="sec7">
    <h2>7. El Centro de Mando: Correlación Multi-Pilar en Grafana</h2>
    <p>Data Sources unificados, vista Explore split-screen y salto directo de logs a trazas</p>
  </div>

  <h3 id="sec7-1">7.1 Configuración de Data Sources Unificados (Prometheus, Loki, Jaeger)</h3>
  <p>
    Grafana actúa como panel de control central conectando con Prometheus (puerto 9090), Loki (puerto 3100) y Jaeger (puerto 16686).
  </p>

  <h3 id="sec7-2">7.2 El Poder de la Vista Explore en Pantalla Dividida</h3>
  <p>
    La pantalla dividida (*Split Screen*) permite correlacionar el instante temporal de una anomalía en las métricas con las líneas de log emitidas en esa misma ventana de segundos:
  </p>
  <pre class="ascii-diagram">
+-----------------------------------------------------------------------------------------+
|                  VISTA DE CORRELACIÓN EN GRAFANA (EXPLORE SPLIT SCREEN)                 |
+-----------------------------------------------------------------------------------------+
|  PANEL IZQUIERDO: MÉTRICAS (PROMETHEUS)    |  PANEL DERECHO: LOGS (LOKI)                |
|  Query: sum(rate(http_requests_total       |  Query: {namespace="default",              |
|         {status="500"}[1m]))               |         app="podinfo"} |= "error"          |
|                                            |                                            |
|   RPS Error                                |  [2026-11-25 18:45:01] ERROR: database     |
|   5 |           /\                         |  connection timeout on /status/500         |
|   4 |          /  \                        |  [2026-11-25 18:45:02] ERROR: connection   |
|   3 |         /    \                       |  refused host 10.244.1.80:5432             |
|   0 +--------+------+--------+             |  [2026-11-25 18:45:03] ERROR: execution    |
|       18:40  18:45   18:50                 |  failed trace_id=4bf92f3577b34da6          |
+--------------------------------------------+--------------------------------------------+
  </pre>

  <h3 id="sec7-3">7.3 Del Trace ID al Log Exacto: Cerrando el Círculo de la Observabilidad</h3>
  <p>
    Configurando un <em>Derived Field</em> en Grafana, los identificadores <code>trace_id</code> presentes en los logs se convierten en enlaces directos que abren la traza en Jaeger con un solo clic.
  </p>

  <!-- SECCIÓN 8 -->
  <div class="section-banner" id="sec8">
    <h2>8. El Experimento del Caos: Diagnóstico de un Incidente Real con Podinfo</h2>
    <p>Inyección controlada de errores HTTP 500, latencia inducida y resolución paso a paso</p>
  </div>

  <h3 id="sec8-1">8.1 Despliegue de la Aplicación de Prueba <code>podinfo</code> y su <code>ServiceMonitor</code></h3>
  <pre><code>kubectl apply -f manifests/04-podinfo/podinfo.yaml
kubectl get pods -l app.kubernetes.io/name=podinfo</code></pre>

  <h3 id="sec8-2">8.2 Inyección de Fallos Controlados: Errores 500, Latencia y Pico de CPU</h3>
  <pre><code># 1. Inyección de bucle de errores HTTP 500
kubectl run curl-attacker --rm -i --tty --image=curlimages/curl -- sh -c '
  while true; do
    curl -s "http://podinfo.default.svc:9898/status/500" > /dev/null
    sleep 0.1
  done
'

# 2. Inyección de pico de CPU por 30 segundos
kubectl run cpu-stresser --rm -i --tty --image=curlimages/curl -- sh -c '
  curl -s "http://podinfo.default.svc:9898/stress-cpu?duration=30s"
'</code></pre>

  <h3 id="sec8-3">8.3 Resolución del Incidente en 4 Pasos Guiados</h3>
  <ol>
    <li><strong>Detección en Métricas:</strong> Identificar el salto en <code>sum(rate(http_requests_total{status="500"}[1m]))</code> en Grafana.</li>
    <li><strong>Aislamiento en Loki:</strong> Filtrar logs con <code>{app="podinfo"} |= "status=500"</code> para confirmar la ruta de fallo.</li>
    <li><strong>Impacto en Recursos:</strong> Comprobar con <code>kubectl top pods</code> la saturación de CPU de la réplica afectada.</li>
    <li><strong>Restauración:</strong> Cancelar la carga y verificar la normalización de las métricas.</li>
  </ol>

  <!-- SECCIÓN 9 -->
  <div class="section-banner" id="sec9">
    <h2>9. La Brecha hacia la Producción y Resolución de Problemas (Troubleshooting)</h2>
    <p>Arquitectura de producción a largo plazo y catálogo de errores comunes en laboratorios</p>
  </div>

  <h3 id="sec9-1">9.1 Almacenamiento Persistente en Producción: S3/MinIO y Thanos/Cortex</h3>
  <table>
    <thead>
      <tr>
        <th>Dimensión</th>
        <th>Entorno de Formación / Lab</th>
        <th>Entorno de Producción</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Logs (Loki)</strong></td>
        <td>Local (emptyDir / disco) &bull; Retención: 24h</td>
        <td>Buckets de objetos S3 / GCS &bull; Retención: 30 a 90 días</td>
      </tr>
      <tr>
        <td><strong>Métricas (Prometheus)</strong></td>
        <td>TSDB local &bull; Retención: 12h</td>
        <td>Thanos / Cortex &bull; Retención: 1 a 2 años</td>
      </tr>
      <tr>
        <td><strong>Trazas (Jaeger)</strong></td>
        <td>In-Memory &bull; Volátil al reiniciar</td>
        <td>Grafana Tempo o Jaeger persistente sobre Cassandra / ES</td>
      </tr>
      <tr>
        <td><strong>Alta Disponibilidad</strong></td>
        <td>1 réplica única</td>
        <td>Arquitectura distribuida multirréplica desacoplada</td>
      </tr>
    </tbody>
  </table>

  <h3 id="sec9-2">9.2 Error 1: Pods en <code>Pending</code> o <code>CrashLoopBackOff</code> por Falta de Recursos</h3>
  <p>
    Si los pods quedan en <code>Pending</code> con evento <code>Insufficient memory</code>, reducir los <code>requests.memory</code> en <code>values-lab.yaml</code> para ajustarse a la capacidad real del nodo.
  </p>

  <h3 id="sec9-3">9.3 Error 2: <code>ServiceMonitor</code> No Recoge Métricas</h3>
  <p>
    Verificar que <code>serviceMonitorSelectorNilUsesHelmValues: false</code> esté activo en Prometheus, o etiquetar manualmente el ServiceMonitor:
  </p>
  <pre><code>kubectl label servicemonitor podinfo release=prometheus</code></pre>

  <h3 id="sec9-4">9.4 Error 3: Promtail Sin Permisos RBAC para <code>/var/log/pods</code></h3>
  <p>
    Si Promtail registra errores de permiso denegado sobre el hostPath, verificar que su ClusterRoleBinding esté activo y que no existan políticas de Pod Security Standards bloqueando el acceso a ficheros del nodo.
  </p>

</body>
</html>
"""

OUTLINE_STRUCTURE = [
    {
        "title": "Portada",
        "page": 0
    },
    {
        "title": "Tabla de Contenidos",
        "id": "toc"
    },
    {
        "title": "1. Fundamentos y Modelo Mental de la Observabilidad en Kubernetes",
        "id": "sec1",
        "children": [
            {"title": "1.1 Más allá del Monitoreo Pasivo: El Triángulo de Observabilidad", "id": "sec1-1"},
            {"title": "1.2 El Dilema de la Carga Efímera: Por Qué kubectl logs No Escala", "id": "sec1-2"},
            {"title": "1.3 Arquitectura del Stack de Laboratorio vs. Gran Empresa", "id": "sec1-3"},
            {"title": "1.4 Matriz Comparativa de Recursos en Entornos de Formación", "id": "sec1-4"}
        ]
    },
    {
        "title": "2. Diagnóstico Nativo: Metrics Server y Herramientas CLI",
        "id": "sec2",
        "children": [
            {"title": "2.1 Despliegue y Validación de Metrics Server", "id": "sec2-1"},
            {"title": "2.2 La Métrica Puntual: kubectl top nodes y kubectl top pods", "id": "sec2-2"},
            {"title": "2.3 Escalado Automático Basado en Métricas: Horizontal Pod Autoscaler (HPA)", "id": "sec2-3"},
            {"title": "2.4 La Terminal al Límite: Inspección con Stern y k9s", "id": "sec2-4"}
        ]
    },
    {
        "title": "3. El Pilar de las Métricas: kube-prometheus-stack Optimizado",
        "id": "sec3",
        "children": [
            {"title": "3.1 Anatomía del Prometheus Operator y Componentes Clave", "id": "sec3-1"},
            {"title": "3.2 Adaptación Quirúrgica de values-lab.yaml: Evitando OOMKilled", "id": "sec3-2"},
            {"title": "3.3 El Modelo de Ingesta por Extracción (Scrape / Pull)", "id": "sec3-3"},
            {"title": "3.4 Despliegue del Stack con Helm", "id": "sec3-4"}
        ]
    },
    {
        "title": "4. Scraping Declarativo: ServiceMonitors y PromQL en la Práctica",
        "id": "sec4",
        "children": [
            {"title": "4.1 La Abstracción del ServiceMonitor: Selectores y Puertos", "id": "sec4-1"},
            {"title": "4.2 Anatomía de una Métrica Prometheus y Formato OpenMetrics", "id": "sec4-2"},
            {"title": "4.3 Consultas Esenciales en PromQL (rate, histogram_quantile, agregaciones)", "id": "sec4-3"}
        ]
    },
    {
        "title": "5. El Pilar de los Logs: Grafana Loki y Promtail en Modo Ligero",
        "id": "sec5",
        "children": [
            {"title": "5.1 Por Qué Descartar Elasticsearch / Kibana en Laboratorios", "id": "sec5-1"},
            {"title": "5.2 Filosofía de Indexación de Loki: Menos Metadatos, Menor Consumo", "id": "sec5-2"},
            {"title": "5.3 Despliegue de Promtail como DaemonSet sobre /var/log/pods", "id": "sec5-3"},
            {"title": "5.4 Consultas con LogQL: Filtros de Flujo, Parsing JSON y Métricas Derivadas", "id": "sec5-4"}
        ]
    },
    {
        "title": "6. El Tercer Pilar: Trazabilidad Distribuida con Jaeger All-in-One",
        "id": "sec6",
        "children": [
            {"title": "6.1 Anatomía de una Traza: Traces, Spans, Context Propagation y Trace ID", "id": "sec6-1"},
            {"title": "6.2 Despliegue de Jaeger All-in-One en Memoria", "id": "sec6-2"},
            {"title": "6.3 Recepción de Trazas OTLP y Consulta en la Interfaz Web", "id": "sec6-3"}
        ]
    },
    {
        "title": "7. El Centro de Mando: Correlación Multi-Pilar en Grafana",
        "id": "sec7",
        "children": [
            {"title": "7.1 Configuración de Data Sources Unificados (Prometheus, Loki, Jaeger)", "id": "sec7-1"},
            {"title": "7.2 El Poder de la Vista Explore en Pantalla Dividida", "id": "sec7-2"},
            {"title": "7.3 Del Trace ID al Log Exacto: Cerrando el Círculo de la Observabilidad", "id": "sec7-3"}
        ]
    },
    {
        "title": "8. El Experimento del Caos: Diagnóstico de un Incidente Real con Podinfo",
        "id": "sec8",
        "children": [
            {"title": "8.1 Despliegue de la Aplicación de Prueba podinfo y su ServiceMonitor", "id": "sec8-1"},
            {"title": "8.2 Inyección de Fallos Controlados: Errores 500, Latencia y Pico de CPU", "id": "sec8-2"},
            {"title": "8.3 Resolución del Incidente en 4 Pasos Guiados", "id": "sec8-3"}
        ]
    },
    {
        "title": "9. La Brecha hacia la Producción y Resolución de Problemas (Troubleshooting)",
        "id": "sec9",
        "children": [
            {"title": "9.1 Almacenamiento Persistente en Producción: S3/MinIO y Thanos/Cortex", "id": "sec9-1"},
            {"title": "9.2 Error 1: Pods en Pending o CrashLoopBackOff por Falta de Recursos", "id": "sec9-2"},
            {"title": "9.3 Error 2: ServiceMonitor No Recoge Métricas", "id": "sec9-3"},
            {"title": "9.4 Error 3: Promtail Sin Permisos RBAC para /var/log/pods", "id": "sec9-4"}
        ]
    }
]


def add_pdf_bookmarks(pdf_path):
    """Inyecta el árbol de marcadores (Document Outlines) en el PDF usando pypdf."""
    try:
        import pypdf
    except ImportError:
        print("Aviso: 'pypdf' no está disponible. Omitiendo inyección de marcadores del panel lateral.")
        return

    print("Inyectando marcadores jerárquicos (Document Outlines) en el panel lateral del PDF...")
    reader = pypdf.PdfReader(pdf_path)
    writer = pypdf.PdfWriter()
    writer.append(reader)

    def get_page(target_id):
        for key in (target_id, "/" + target_id):
            if key in reader.named_destinations:
                return reader.get_destination_page_number(reader.named_destinations[key])
        return None

    def add_items(items, parent=None):
        for item in items:
            p_num = item.get("page")
            if p_num is None and "id" in item:
                p_num = get_page(item["id"])
            if p_num is not None:
                node = writer.add_outline_item(item["title"], p_num, parent=parent)
                if "children" in item:
                    add_items(item["children"], parent=node)

    add_items(OUTLINE_STRUCTURE)

    temp_path = pdf_path + ".tmp"
    with open(temp_path, "wb") as f:
        writer.write(f)
    os.replace(temp_path, pdf_path)


def main():
    os.makedirs(DOCS_DIR, exist_ok=True)
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"HTML generado en: {HTML_PATH}")

    chrome_candidates = [
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    ]
    chrome_bin = None
    for cand in chrome_candidates:
        if os.path.exists(cand):
            chrome_bin = cand
            break
        found = shutil.which(cand)
        if found:
            chrome_bin = found
            break

    if not chrome_bin:
        chrome_bin = "google-chrome"
    cmd = [
        chrome_bin,
        "--headless",
        "--no-sandbox",
        "--disable-gpu",
        "--allow-file-access-from-files",
        "--enable-local-file-accesses",
        "--user-data-dir=/tmp/chrome-user-data-obs",
        "--no-pdf-header-footer",
        f"--print-to-pdf={PDF_PATH}",
        f"file://{HTML_PATH}"
    ]
    print(f"Compilando PDF con Chrome headless a: {PDF_PATH}...")
    if os.path.exists(PDF_PATH):
        os.remove(PDF_PATH)
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0 and os.path.exists(PDF_PATH):
        add_pdf_bookmarks(PDF_PATH)
        size_kb = os.path.getsize(PDF_PATH) / 1024
        print(f"¡Éxito! Archivo PDF generado con marcadores del panel lateral: {PDF_PATH} ({size_kb:.1f} KB)")
    else:
        print("Error generando PDF:")
        print(res.stderr)
        exit(1)

if __name__ == "__main__":
    main()
