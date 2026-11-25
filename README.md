# PoC Training: Observabilidad en Kubernetes con Stack LGTM y Jaeger

<div align="center">

![Kubernetes](https://img.shields.io/badge/Kubernetes-v1.31-326CE5?logo=kubernetes&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-v2.54-E6522C?logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-v11.1-F46800?logo=grafana&logoColor=white)
![Loki](https://img.shields.io/badge/Grafana_Loki-v3.0-F46800?logo=grafana&logoColor=white)
![Jaeger](https://img.shields.io/badge/Jaeger-v1.57-60D0E4?logo=jaeger&logoColor=white)
![License](https://img.shields.io/badge/Curso-Módulo_Observabilidad-blue)
![Deliverable](https://img.shields.io/badge/PDF-k8s--observabilidad.pdf-red?logo=adobeacrobatreader)

**Laboratorio Práctico y Guía Oficial:** Despliegue quirúrgicamente optimizado del **Stack LGTM ligero** (Prometheus + Loki + Promtail + Grafana) y **Jaeger All-in-One**, scraping declarativo mediante `ServiceMonitors`, diagnóstico nativo con `Metrics Server`, correlación multi-pilar en pantalla dividida (*Explore Split-Screen*) y resolución guiada de un incidente de caos con `podinfo`.

</div>

---

## 🎯 Objetivo Pedagógico

El propósito fundamental de este repositorio es **desmitificar la observabilidad moderna en Kubernetes sin colapsar los recursos del clúster de laboratorio**.

En la mayoría de cursos y entornos empresariales se recurre a stacks pesados como **ELK/EFK** (Elasticsearch, Logstash/Fluentd, Kibana). Aunque Elasticsearch es un motor de búsqueda excelente, requiere más de 4 GB de RAM solo para su máquina virtual Java, provocando frecuentes bloqueos por falta de memoria (`OOMKilled`) en nodos de formación. Por otro lado, confiar únicamente en `kubectl logs` y `kubectl top` produce una visión efímera y aislada que no escala en arquitecturas de microservicios.

A través de este proyecto aprenderás:
1. **Diagnóstico Nativo y Efímero:** Despliegue de `Metrics Server`, comandos `kubectl top nodes/pods`, escalado horizontal con HPA y agregación de logs en terminal mediante `stern` y `k9s`.
2. **El Pilar de las Métricas (`kube-prometheus-stack`):** Cómo tunear quirúrgicamente los `values.yaml` de Helm (retención a 12h, Alertmanager desactivado y selectores abiertos) para operar el Prometheus Operator con menos de 300 MB de RAM.
3. **Scraping Declarativo (`ServiceMonitors`):** Cómo desvincular la configuración manual de Prometheus usando CRDs nativos de Kubernetes y dominar consultas esenciales en PromQL (`rate()`, percentiles P99 y agregaciones).
4. **El Pilar de los Logs (`Grafana Loki + Promtail`):** Por qué Loki indexa únicamente metadatos de Kubernetes en lugar del texto completo, ahorrando hasta un 90% de RAM frente a Elasticsearch, y cómo consultar streams con LogQL.
5. **El Tercer Pilar: Trazabilidad Distribuida (`Jaeger All-in-One`):** Despliegue en memoria (<100 MB RAM) con soporte nativo para OpenTelemetry (OTLP), propagación de contexto (*Trace ID*) y análisis de cascadas de latencia (*spans*).
6. **El Centro de Mando en Grafana:** Integración de los 3 Data Sources y aprovechamiento de la vista *Explore* en pantalla dividida (métrica arriba, logs abajo) con saltos directos de Log a Traza.
7. **El Experimento del Caos (Incidente Real):** Inyección controlada de errores HTTP 500 y saturación de CPU en la aplicación `podinfo`, diagnosticando y resolviendo la causa raíz en 4 pasos estructurados.

---

## ⚖️ Comparativa Conceptual: Monitoreo Tradicional vs ELK vs Stack LGTM Ligero

| Dimensión | Monitoreo Clásico (Nagios/Zabbix) | Stack Pesado (ELK / EFK) | Stack Ligero CNCF (Este Repositorio) |
| :--- | :--- | :--- | :--- |
| **Métricas** | Checks de estado binario (UP/DOWN) | Métricas dispersas o Metricbeat | **Prometheus Operator** (Series temporales PromQL) |
| **Indexación de Logs** | Sin centralización (archivos `/var/log`) | **Texto completo invertido** (Lucene/Java) | **Solo etiquetas de K8s** (Loki + LogQL) |
| **Consumo de Memoria** | Muy bajo (~50 MB) | **Crítico (~6 a 9 GB RAM)** &rarr; Riesgo `OOMKilled` | **Óptimo (~750 MB - 1 GB RAM total clúster)** |
| **Trazas Distribuidas** | Inexistente | Plugins complejos de APM | **Jaeger All-in-One** (En memoria, OTLP nativo) |
| **Integración en K8s** | Manual por agente en VM | Adaptaciones de DaemonSets pesados | **CRDs Nativos** (`ServiceMonitor`, `PodMonitor`) |
| **Visualización** | Paneles estáticos anticuados | Kibana + Grafana duplicados | **Grafana Unificado** (Explore Split-Screen) |

---

## 🏗️ Diagrama de Arquitectura y Topología

```
+--------------------------------------------------------------------------------------------------+
|               ARQUITECTURA COMPLETA: OBSERVABILIDAD EN K8S (STACK LGTM + JAEGER)                 |
+--------------------------------------------------------------------------------------------------+

  [ CAPA 0: DIAGNÓSTICO BASE / TERMINAL ]
  +----------------------------------------------------+----------------------------------------+
  |  Metrics Server (kubectl top nodes/pods, HPA)      |  Stern / k9s (Logs agregados en CLI)   |
  +----------------------------------------------------+----------------------------------------+
                                                  |
                                                  v
  [ CAPA 1: INGESTA Y ALMACENAMIENTO LIGERO (Lab Profile) ]
  +------------------------------+  +-------------------------------+  +------------------------+
  |  kube-prometheus-stack       |  |  Grafana Loki + Promtail      |  |  Jaeger All-in-One     |
  |  - Prometheus (Scrape/TSDB)  |  |  - Promtail (DaemonSet)       |  |  - En memoria (RAM)    |
  |  - Node Exporter & KSM       |  |  - Loki (Indexa metadata K8s) |  |  - UI nativa / OTLP    |
  |  - ServiceMonitor / PromQL   |  |  - LogQL                      |  |  - Trazas distribuidas |
  +------------------------------+  +-------------------------------+  +------------------------+
                 \                                |                                /
                  \                               |                               /
                   v                              v                              v
  [ CAPA 2: CENTRO DE MANDO UNIFICADO ]
  +---------------------------------------------------------------------------------------------+
  |  Grafana (Explore Split-Screen):                                                            |
  |  - Panel 1: Métricas PromQL (Tasas de error HTTP / Latencia P99 / Saturación de CPU)         |
  |  - Panel 2: Logs LogQL (Líneas de error exactas de Podinfo con metadatos de Pod/Container)  |
  |  - Panel 3: Trazas Jaeger / OTLP (Visualización en cascada de Spans y Trace ID)              |
  +---------------------------------------------------------------------------------------------+
                                                  ^
                                                  | (Métricas /metrics, Logs stdout, Trazas OTLP)
  [ CAPA 3: WORKLOAD DE LABORATORIO & EXPERIMENTO DE CAOS ]
  +---------------------------------------------------------------------------------------------+
  |  Podinfo (Deployment 2 réplicas + ClusterIP Service + ServiceMonitor)                       |
  |  - Endpoints de inyección: /status/500, /delay/2, /stress-cpu                               |
  +---------------------------------------------------------------------------------------------+
```

---

## 📁 Estructura del Repositorio

```text
poc-training-k8s-observability/
├── manifests/
│   ├── 00-metrics-server/
│   │   └── metrics-server.yaml       # Deployment de Metrics Server con flags para laboratorios
│   ├── 01-prometheus/
│   │   └── values-lab.yaml           # kube-prometheus-stack (retención 12h, Alertmanager desactivado)
│   ├── 02-loki-promtail/
│   │   └── values-lab.yaml           # Loki monolithic ligero + Promtail DaemonSet (/var/log/pods)
│   ├── 03-jaeger/
│   │   └── jaeger-all-in-one.yaml    # Jaeger all-in-one en memoria (UI web + colectores OTLP)
│   └── 04-podinfo/
│       └── podinfo.yaml              # Deployment (2 réplicas), Service y ServiceMonitor para caos
├── docs/
│   ├── k8s-observabilidad.md         # Guía didáctica completa hiper-detallada (9 capítulos)
│   └── k8s-observabilidad.html       # Documento editorial maquetado para lectura y exportación A4
├── scripts/
│   └── generate_html_pdf.py          # Script de compilación a PDF con marcadores jerárquicos (pypdf)
├── openspec/                         # Especificaciones y tareas del cambio en OpenSpec
├── k8s-observabilidad.pdf            # Entregable oficial en PDF profesional (13 páginas)
└── README.md                         # Documento de presentación del repositorio
```

---

## 🚀 Despliegue Rápido del Laboratorio

### 1. Desplegar Metrics Server para Diagnóstico CLI
```bash
kubectl apply -f manifests/00-metrics-server/metrics-server.yaml
# Esperar unos 60 segundos para la primera ventana de métricas:
kubectl top nodes
kubectl top pods -A
```

### 2. Desplegar el Stack de Métricas (`kube-prometheus-stack`)
```bash
kubectl create namespace observability

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace observability \
  --values manifests/01-prometheus/values-lab.yaml
```

Supervisar que los componentes alcancen el estado `Running`:
```bash
kubectl get pods -n observability -l "release=prometheus"
```

### 3. Desplegar el Stack de Logs (`Loki + Promtail`)
```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

helm install loki grafana/loki-stack \
  --namespace observability \
  --values manifests/02-loki-promtail/values-lab.yaml
```

Verificar que el DaemonSet Promtail corra en todos los nodos:
```bash
kubectl get daemonset promtail -n observability
```

### 4. Desplegar Trazabilidad Distribuida (`Jaeger All-in-One`)
```bash
kubectl apply -f manifests/03-jaeger/jaeger-all-in-one.yaml
kubectl get pods -n observability -l "app.kubernetes.io/name=jaeger"
```

### 5. Desplegar la Aplicación de Prueba (`Podinfo`) y su `ServiceMonitor`
```bash
kubectl apply -f manifests/04-podinfo/podinfo.yaml
kubectl get pods -l app.kubernetes.io/name=podinfo
kubectl get servicemonitor podinfo
```

### 6. Acceder al Centro de Mando (Grafana)
Grafana se encuentra configurado con el usuario y contraseña `admin` / `admin`:
```bash
# Vía port-forward local (localhost:3000):
kubectl port-forward svc/prometheus-grafana 3000:80 -n observability

# O mediante el NodePort 30080 configurado en los values:
# http://<IP-NODO>:30080
```
Comprueba en **Connections** &rarr; **Data Sources** que **Prometheus**, **Loki** y **Jaeger** estén conectados y en verde.

---

## 💥 Laboratorio de Caos: Diagnóstico de un Incidente Real

En este escenario provocamos una caída deliberada de servicio y seguimos el protocolo de respuesta a incidentes en 4 pasos:

### Paso 1: Inyección de Tráfico con Errores HTTP 500 y Estrés de CPU
Lanza un pod atacante con un bucle continuo hacia el endpoint `/status/500`:
```bash
kubectl run curl-attacker --rm -i --tty --image=curlimages/curl -- sh -c '
  while true; do
    curl -s "http://podinfo.default.svc:9898/status/500" > /dev/null
    sleep 0.1
  done
'
```

En otra terminal, solicita a Podinfo que estrese su CPU durante 30 segundos:
```bash
kubectl run cpu-stresser --rm -i --tty --image=curlimages/curl -- sh -c '
  curl -s "http://podinfo.default.svc:9898/stress-cpu?duration=30s"
'
```

### Paso 2: Detección en Métricas (PromQL)
En la pestaña **Explore** de Grafana, selecciona el Data Source **Prometheus** y ejecuta:
```promql
sum(rate(http_requests_total{status="500"}[1m])) by (pod)
```
Observa el pico repentino de más de 10 peticiones fallidas por segundo distribuidas entre las dos réplicas de Podinfo.

### Paso 3: Correlación Temporal y Aislamiento en Logs (LogQL)
Pulsa el botón **Split** en la esquina superior derecha de Grafana para abrir la pantalla dividida. Selecciona **Loki** en el panel derecho y ejecuta:
```logql
{app="podinfo"} |= "status=500"
```
Comprueba cómo los logs de ambas réplicas coinciden exactamente con la ventana temporal del pico métrico, mostrando la traza del error en el handler.

### Paso 4: Comprobación de Saturación de Recursos y Restauración
Verifica en la terminal el impacto sobre el contenedor mediante `kubectl top`:
```bash
kubectl top pods -l app.kubernetes.io/name=podinfo
```
Cancela el proceso del pod atacante (`curl-attacker` con `Ctrl+C`). Observa cómo la tasa de errores cae a 0 en Grafana y el clúster regresa a la normalidad operativa.

---

## 📄 Compilación de la Guía PDF

El entregable oficial [`k8s-observabilidad.pdf`](file:///home/miguel/git/poc-training-k8s-observability/k8s-observabilidad.pdf) está precompilado en la raíz del repositorio. Para regenerarlo tras cualquier modificación:

```bash
python3 scripts/generate_html_pdf.py
```

* **Dependencias:** Python 3, `pypdf`, y Google Chrome o Chromium.
* **Características Editoriales:**
  - Maquetación A4 con tipografías *Inter* y *JetBrains Mono*.
  - Reglas `@page` con pie de página y contador dinámico (`Página X`).
  - Diagramas ASCII encuadrados y coloreados con bloques de código adaptativos.
  - Cajas de aviso con código de color (*Note*, *Warning*, *Important*, *Tip*).
  - Árbol de marcadores jerárquicos (*PDF Outlines*) integrado en el panel lateral para los 9 capítulos y 32 subsecciones.
