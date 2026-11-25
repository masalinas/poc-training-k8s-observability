# Guía Práctica de Observabilidad en Kubernetes
## Métricas, Logs Centralizados, Trazabilidad Distribuida y Diagnóstico de Incidentes con el Stack LGTM y Jaeger

**Autor:** Equipo Docente de Kubernetes y Arquitectura Cloud Native  
**Documento Oficial del Curso:** Módulo Práctico - Observabilidad y Diagnóstico de Sistemas Distribuidos  
**Entregable:** `k8s-observabilidad.pdf`

---

## Tabla de Contenidos

1. [Fundamentos y Modelo Mental de la Observabilidad en Kubernetes](#1-fundamentos-y-modelo-mental-de-la-observabilidad-en-kubernetes)
   - [1.1 Más allá del Monitoreo Pasivo: El Triángulo de Observabilidad](#11-más-allá-del-monitoreo-pasivo-el-triángulo-de-observabilidad)
   - [1.2 El Dilema de la Carga Efímera: Por Qué `kubectl logs` No Escala](#12-el-dilema-de-la-carga-efímera-por-qué-kubectl-logs-no-escala)
   - [1.3 Arquitectura del Stack de Laboratorio vs. Gran Empresa](#13-arquitectura-del-stack-de-laboratorio-vs-gran-empresa)
   - [1.4 Matriz Comparativa de Recursos en Entornos de Formación](#14-matriz-comparativa-de-recursos-en-entornos-de-formación)
2. [Diagnóstico Nativo: Metrics Server y Herramientas CLI](#2-diagnóstico-nativo-metrics-server-y-herramientas-cli)
   - [2.1 Despliegue y Validación de Metrics Server](#21-despliegue-y-validación-de-metrics-server)
   - [2.2 La Métrica Puntual: `kubectl top nodes` y `kubectl top pods`](#22-la-métrica-puntual-kubectl-top-nodes-y-kubectl-top-pods)
   - [2.3 Escalado Automático Basado en Métricas: Horizontal Pod Autoscaler (HPA)](#23-escalado-automático-basado-en-métricas-horizontal-pod-autoscaler-hpa)
   - [2.4 La Terminal al Límite: Inspección con Stern y k9s](#24-la-terminal-al-límite-inspección-con-stern-y-k9s)
3. [El Pilar de las Métricas: `kube-prometheus-stack` Optimizado](#3-el-pilar-de-las-métricas-kube-prometheus-stack-optimizado)
   - [3.1 Anatomía del Prometheus Operator y Componentes Clave](#31-anatomía-del-prometheus-operator-y-componentes-clave)
   - [3.2 Adaptación Quirúrgica de `values-lab.yaml`: Evitando OOMKilled](#32-adaptación-quirúrgica-de-values-labyaml-evitando-oomkilled)
   - [3.3 El Modelo de Ingesta por Extracción (Scrape / Pull)](#33-el-modelo-de-ingesta-por-extracción-scrape--pull)
   - [3.4 Despliegue del Stack con Helm](#34-despliegue-del-stack-con-helm)
4. [Scraping Declarativo: ServiceMonitors y PromQL en la Práctica](#4-scraping-declarativo-servicemonitors-y-promql-en-la-práctica)
   - [4.1 La Abstracción del `ServiceMonitor`: Selectores y Puertos](#41-la-abstracción-del-servicemonitor-selectores-y-puertos)
   - [4.2 Anatomía de una Métrica Prometheus y Formato OpenMetrics](#42-anatomía-de-una-métrica-prometheus-y-formato-openmetrics)
   - [4.3 Consultas Esenciales en PromQL (`rate`, `histogram_quantile`, agregaciones)](#43-consultas-esenciales-en-promql-rate-histogram_quantile-agregaciones)
5. [El Pilar de los Logs: Grafana Loki y Promtail en Modo Ligero](#5-el-pilar-de-los-logs-grafana-loki-y-promtail-en-modo-ligero)
   - [5.1 Por Qué Descartar Elasticsearch / Kibana en Laboratorios](#51-por-qué-descartar-elasticsearch--kibana-en-laboratorios)
   - [5.2 Filosofía de Indexación de Loki: Menos Metadatos, Menor Consumo](#52-filosofía-de-indexación-de-loki-menos-metadatos-menor-consumo)
   - [5.3 Despliegue de Promtail como DaemonSet sobre `/var/log/pods`](#53-despliegue-de-promtail-como-daemonset-sobre-varlogpods)
   - [5.4 Consultas con LogQL: Filtros de Flujo, Parsing JSON y Métricas Derivadas](#54-consultas-con-logql-filtros-de-flujo-parsing-json-y-métricas-derivadas)
6. [El Tercer Pilar: Trazabilidad Distribuida con Jaeger All-in-One](#6-el-tercer-pilar-trazabilidad-distribuida-con-jaeger-all-in-one)
   - [6.1 Anatomía de una Traza: Traces, Spans, Context Propagation y Trace ID](#61-anatomía-de-una-traza-traces-spans-context-propagation-y-trace-id)
   - [6.2 Despliegue de Jaeger All-in-One en Memoria](#62-despliegue-de-jaeger-all-in-one-en-memoria)
   - [6.3 Recepción de Trazas OTLP y Consulta en la Interfaz Web](#63-recepción-de-trazas-otlp-y-consulta-en-la-interfaz-web)
7. [El Centro de Mando: Correlación Multi-Pilar en Grafana](#7-el-centro-de-mando-correlación-multi-pilar-en-grafana)
   - [7.1 Configuración de Data Sources Unificados (Prometheus, Loki, Jaeger)](#71-configuración-de-data-sources-unificados-prometheus-loki-jaeger)
   - [7.2 El Poder de la Vista *Explore* en Pantalla Dividida](#72-el-poder-de-la-vista-explore-en-pantalla-dividida)
   - [7.3 Del Trace ID al Log Exacto: Cerrando el Círculo de la Observabilidad](#73-del-trace-id-al-log-exacto-cerrando-el-círculo-de-la-observabilidad)
8. [El Experimento del Caos: Diagnóstico de un Incidente Real con Podinfo](#8-el-experimento-del-caos-diagnóstico-de-un-incidente-real-con-podinfo)
   - [8.1 Despliegue de la Aplicación de Prueba `podinfo` y su `ServiceMonitor`](#81-despliegue-de-la-aplicación-de-prueba-podinfo-y-su-servicemonitor)
   - [8.2 Inyección de Fallos Controlados: Errores 500, Latencia y Pico de CPU](#82-inyección-de-fallos-controlados-errores-500-latencia-y-pico-de-cpu)
   - [8.3 Resolución del Incidente en 4 Pasos Guiados](#83-resolución-del-incidente-en-4-pasos-guiados)
9. [La Brecha hacia la Producción y Resolución de Problemas (Troubleshooting)](#9-la-brecha-hacia-la-producción-y-resolución-de-problemas-troubleshooting)
   - [9.1 Almacenamiento Persistente en Producción: S3/MinIO y Thanos/Cortex](#91-almacenamiento-persistente-en-producción-s3minio-y-thanoscortex)
   - [9.2 Error 1: Pods en `Pending` o `CrashLoopBackOff` por Falta de Recursos](#92-error-1-pods-en-pending-o-crashloopbackoff-por-falta-de-recursos)
   - [9.3 Error 2: `ServiceMonitor` No Recoge Métricas (Selector de Release Faltante)](#93-error-2-servicemonitor-no-recoge-métricas-selector-de-release-faltante)
   - [9.4 Error 3: Promtail Sin Permisos RBAC para `/var/log/pods`](#94-error-3-promtail-sin-permisos-rbac-para-varlogpods)

---

## 1. Fundamentos y Modelo Mental de la Observabilidad en Kubernetes

### 1.1 Más allá del Monitoreo Pasivo: El Triángulo de Observabilidad

Tradicionalmente, en la administración de servidores físicos o máquinas virtuales monolíticas, el concepto de **monitoreo** consistía en comprobar periódicamente si un servicio estaba "vivo" mediante checks de ping, sondas TCP o consultas básicas de CPU y memoria. Si el umbral superaba el 80%, se disparaba una alarma por correo o SMS.

En arquitecturas distribuidas sobre **Kubernetes**, este enfoque resulta totalmente insuficiente. Un clúster moderno aloja cientos de contenedores efímeros que nacen, se escalan y mueren de forma continua en milisegundos. Cuando un usuario experimenta lentitud o errores en una aplicación compuesta por múltiples microservicios, saber que "la CPU del nodo está al 45%" no responde a las preguntas críticas del negocio:
* ¿Qué microservicio específico está introduciendo latencia en la transacción?
* ¿Por qué falló una petición concreta si los demás Pods responden correctamente?
* ¿Qué excepción arrojó la aplicación justo antes de que el contenedor fuera destruido por Kubernetes?

La **observabilidad** no es una herramienta, sino una propiedad de nuestro sistema: **la capacidad de deducir el estado interno de nuestras aplicaciones analizando únicamente sus salidas externas**. Esta disciplina se apoya en los tres pilares clásicos:

```
+-----------------------------------------------------------------------------------------+
|                       LOS TRES PILARES DE LA OBSERVABILIDAD EN K8S                      |
+-----------------------------------------------------------------------------------------+
|  Pilar       | Naturaleza del Dato             | Pregunta que Resuelve                 |
+--------------+---------------------------------+---------------------------------------+
|  Métricas    | Series temporales numéricas     | "¿Está ocurriendo un problema ahora?  |
|              | agregadas (Prometheus)          | ¿Cuál es la tasa de error y tráfico?" |
+--------------+---------------------------------+---------------------------------------+
|  Logs        | Eventos textuales con marca de  | "¿Por qué falló exactamente?          |
|              | tiempo y contexto (Loki)        | ¿Cuál es el stack trace de la app?"   |
+--------------+---------------------------------+---------------------------------------+
|  Trazas      | Flujo de petición end-to-end    | "¿Dónde se consume el tiempo en la    |
|              | a través de servicios (Jaeger)  | llamada distribuida?"                 |
+--------------+---------------------------------+---------------------------------------+
```

---

### 1.2 El Dilema de la Carga Efímera: Por Qué `kubectl logs` No Escala

Cuando un estudiante se inicia en Kubernetes, su primera herramienta de depuración es la CLI de Kubernetes:
```bash
kubectl logs -f mi-pod-xyz -n default
```
Sin embargo, confiar exclusivamente en `kubectl logs` en entornos reales adolece de graves limitaciones intrínsecas al diseño de Kubernetes:
1. **Volatilidad Extrema:** Cuando un contenedor sufre un fallo irrecuperable (por ejemplo, `OOMKilled` o un fallo de segmentación), Kubernetes reinicia el Pod según su política de reinicio (`RestartPolicy`). Los logs del contenedor previo solo son accesibles temporalmente mediante el flag `--previous`. Si el Pod vuelve a reiniciarse o es reemplazado por un Deployment, los logs se pierden irreversiblemente en el disco local del nodo trabajador.
2. **Falta de Agregación:** Si un microservicio cuenta con 10 réplicas distribuidas en 3 nodos, una petición HTTP errónea impactará solo en una réplica. Con `kubectl logs` el operador se ve obligado a abrir 10 terminales distintas o adivinar cuál fue el Pod afectado.
3. **Sobrecarga de la API Server:** Cada invocación de `kubectl logs` abre un socket HTTPS persistente hacia el `kube-apiserver`, que a su vez se conecta al daemon `kubelet` del nodo y lee el fichero `/var/log/pods/...`. Cientos de consultas concurrentes degradan severamente el rendimiento del Control Plane.

> [!WARNING]
> En Kubernetes, los Pods deben considerarse efímeros e intercambiables. La única manera de garantizar la capacidad de auditoría y resolución de incidencias es desacoplar el almacenamiento de eventos de la vida del contenedor mediante un sistema centralizado de ingesta.

---

### 1.3 Arquitectura del Stack de Laboratorio vs. Gran Empresa

En la industria es común encontrar arquitecturas basadas en el stack **ELK/EFK** (Elasticsearch, Logstash/Fluentd, Kibana). Aunque Elasticsearch es un motor de búsqueda por texto completo extremadamente potente, para un clúster de laboratorio o formación representa un grave obstáculo:
* Un único nodo de Elasticsearch requiere un mínimo absoluto de 2 a 4 GB de memoria RAM solo para inicializar su máquina virtual Java (JVM).
* Los índices de texto completo (*inverted indexes*) consumen ingentes cantidades de almacenamiento en disco y operaciones de entrada/salida (IOPS).
* En clústeres tipo `kind`, `minikube` o servidores con recursos moderados (8-16 GB RAM), desplegar Elasticsearch conduce inexorablemente al colapso de los nodos por eventos `NodeNotReady` o `OOMKilled`.

La alternativa moderna y eficiente promovida por la **CNCF (Cloud Native Computing Foundation)** es el **Stack LGTM ligero** (Prometheus + Loki + Grafana) complementado con **Jaeger All-in-One**:

```
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
```

---

### 1.4 Matriz Comparativa de Recursos en Entornos de Formación

La siguiente matriz evidencia por qué el stack seleccionado es el idóneo para cursos y laboratorios:

```
+-----------------------------------------------------------------------------------------+
|               MATRIZ DE RECURSOS: STACK PESADO (ELK) VS STACK LAB (LGTM)                |
+-----------------------------------------------------------------------------------------+
|  Componente       | Stack Enterprise Clásico     | Stack Ligero CNCF (Este Curso)       |
+-------------------+------------------------------+--------------------------------------+
|  Métricas         | Prometheus Clásico (10d rot) | Prometheus Operator (12h retención)  |
|                   | RAM: ~1.5 GB                 | RAM: ~300 MB                         |
+-------------------+------------------------------+--------------------------------------+
|  Logs             | Elasticsearch + Logstash     | Grafana Loki + Promtail              |
|                   | RAM: ~3.0 - 4.5 GB           | RAM: ~200 MB                         |
+-------------------+------------------------------+--------------------------------------+
|  Trazabilidad     | Jaeger + Cassandra / ES      | Jaeger All-in-One (In-Memory)        |
|                   | RAM: ~2.0 GB                 | RAM: ~100 MB                         |
+-------------------+------------------------------+--------------------------------------+
|  Visualización    | Kibana + Grafana duplicados  | Grafana Unificado (Explore view)     |
|                   | RAM: ~1.2 GB                 | RAM: ~150 MB                         |
+-------------------+------------------------------+--------------------------------------+
|  TOTAL CLÚSTER    | ~7.7 - 9.2 GB RAM (Peligro)  | ~0.75 - 1.0 GB RAM (Óptimo Lab)      |
+-------------------+------------------------------+--------------------------------------+
```

---

## 2. Diagnóstico Nativo: Metrics Server y Herramientas CLI

### 2.1 Despliegue y Validación de Metrics Server

Antes de instalar operadores complejos, es imperativo que los alumnos comprendan qué herramientas ofrece Kubernetes de manera nativa. El componente central del diagnóstico básico es el **`Metrics Server`**.

`Metrics Server` no es un motor de métricas a largo plazo (no almacena series temporales ni dispone de base de datos en disco); es un agregador en memoria que consulta cada 15-60 segundos el endpoint `/stats/summary` del kubelet en cada nodo del clúster y expone los datos a través de la API estándar `metrics.k8s.io`.

Para desplegarlo en nuestro laboratorio (ubicado en `manifests/00-metrics-server/metrics-server.yaml`):

```bash
kubectl apply -f manifests/00-metrics-server/metrics-server.yaml
```

Verificamos que el Deployment esté operativo y la API registrada:
```bash
kubectl get deployment metrics-server -n kube-system
kubectl get apiservice v1beta1.metrics.k8s.io
```

> [!NOTE]
> En clústeres locales o kubeadm sin certificados firmados por una entidad pública para los kubelets, `metrics-server` requiere el argumento `--kubelet-insecure-tls` para evitar errores de validación x509 al consultar los puertos 10250 de los nodos.

---

### 2.2 La Métrica Puntual: `kubectl top nodes` y `kubectl top pods`

Una vez que `metrics-server` recolecta su primera ventana de muestras (aproximadamente 60 segundos tras el arranque), se desbloquean los comandos nativos de inspección de recursos:

1. **Inspección de Nodos:**
   ```bash
   kubectl top nodes
   ```
   *Salida típica:*
   ```text
   NAME             CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
   k8s-control-01   142m         7%     1412Mi          36%
   k8s-worker-01    98m          4%     980Mi           25%
   ```

2. **Inspección de Cargas de Trabajo (Pods):**
   ```bash
   kubectl top pods -A --sort-by=memory
   ```
   Permite identificar de inmediato qué contenedor está consumiendo la mayor parte de la memoria del clúster antes de que alcance su límite (`limit`) y sufra un reinicio forzado.

---

### 2.3 Escalado Automático Basado en Métricas: Horizontal Pod Autoscaler (HPA)

Además del comando `top`, la existencia de `Metrics Server` es el requisito sine qua non para que el **Horizontal Pod Autoscaler (HPA)** de Kubernetes pueda tomar decisiones de escalado automático.

```
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
```

Si definimos un HPA sobre un Deployment de prueba:
```bash
kubectl autoscale deployment podinfo --cpu-percent=70 --min=2 --max=6
```
El controlador de Kubernetes calculará la fórmula:
$$\text{Réplicas deseables} = \lceil \text{Réplicas actuales} \times \frac{\text{Métrica actual}}{\text{Métrica objetivo}} \rceil$$

---

### 2.4 La Terminal al Límite: Inspección con Stern y k9s

Cuando múltiples Pods de un mismo microservicio fallan en paralelo, la instrucción tradicional `kubectl logs` resulta ineficiente. Para mitigar esta fricción en terminal, existen dos herramientas comunitarias indispensables:

1. **Stern:** Permite realizar un tailing simultáneo de logs combinando Pods y contenedores mediante expresiones regulares, asignando un color distinto a cada réplica:
   ```bash
   stern "podinfo-.*" --tail 20 --color always
   ```
2. **k9s:** Una interfaz de usuario basada en terminal (TUI) que permite navegar entre Namespaces, Pods, Services y logs en tiempo real mediante atajos de teclado (`l` para logs, `s` para shell, `d` para describe), mostrando barras gráficas de CPU y memoria obtenidas de Metrics Server.

> [!TIP]
> En la sesión práctica, haz que los alumnos intenten descubrir qué réplica exacta falló usando únicamente `kubectl logs` y luego usando `stern`. La diferencia de productividad ilustra claramente por qué la centralización es obligatoria.

---

## 3. El Pilar de las Métricas: `kube-prometheus-stack` Optimizado

### 3.1 Anatomía del Prometheus Operator y Componentes Clave

El chart de Helm **`kube-prometheus-stack`** (mantenido por la comunidad Prometheus Community) despliega una arquitectura completa de monitorización basada en el patrón de operadores de Kubernetes:

```
+-----------------------------------------------------------------------------------------+
|                    COMPONENTES DE KUBE-PROMETHEUS-STACK EN EL CLÚSTER                   |
+-----------------------------------------------------------------------------------------+

  +-------------------------------------------------------------------------------------+
  | PROMETHEUS OPERATOR                                                                 |
  | Observa los Custom Resources (ServiceMonitor, PodMonitor, PrometheusRule)           |
  | y genera dinámicamente la configuración activa para el Pod de Prometheus.           |
  +-------------------------------------------------------------------------------------+
        |                                       |                               |
        v                                       v                               v
  +------------------+                 +------------------+            +------------------+
  | PROMETHEUS TSDB  |                 | NODE EXPORTER    |            | KUBE-STATE-METR. |
  | Servidor central |                 | DaemonSet en     |            | Traduce estado   |
  | de scraping y    |                 | cada nodo físico |            | de k8s (Pods,    |
  | consultas PromQL |                 | (CPU, RAM, red)  |            | Deployments)     |
  +------------------+                 +------------------+            +------------------+
        |
        v
  +-------------------------------------------------------------------------------------+
  | GRAFANA                                                                             |
  | Motor de visualización web con dashboards oficiales preconfigurados para k8s.       |
  +-------------------------------------------------------------------------------------+
```

---

### 3.2 Adaptación Quirúrgica de `values-lab.yaml`: Evitando OOMKilled

El chart oficial con sus valores por defecto está pensado para clústeres de producción empresariales: habilita Alertmanager con alta disponibilidad, activa múltiples reglas de alerta redundantes y solicita más de 2 GB de memoria RAM.

Para nuestro laboratorio de formación, hemos diseñado el perfil quirúrgico `manifests/01-prometheus/values-lab.yaml`. Analicemos sus decisiones críticas:

```yaml
# Desactivación de Alertmanager para liberar memoria (~150MB ahorrados)
alertmanager:
  enabled: false

# Configuración del servidor Prometheus
prometheus:
  prometheusSpec:
    # Retención corta (12 horas): evita acumular gigabytes en disco
    retention: 12h
    scrapeInterval: "15s"
    replicas: 1
    
    # CRÍTICO: Permitir al Operator capturar ServiceMonitors sin requerir
    # que lleven la etiqueta release=prometheus
    serviceMonitorSelectorNilUsesHelmValues: false
    podMonitorSelectorNilUsesHelmValues: false
    serviceMonitorSelector: {}
    
    # Almacenamiento efímero en memoria/disco local del nodo
    storageSpec:
      emptyDir: {}
    resources:
      requests:
        cpu: 100m
        memory: 256Mi
      limits:
        cpu: 500m
        memory: 512Mi
```

> [!IMPORTANT]
> El parámetro `serviceMonitorSelectorNilUsesHelmValues: false` es el error más recurrente en los laboratorios de Kubernetes. Por defecto, Prometheus Operator solo monitoriza aquellos `ServiceMonitor` que incluyan la etiqueta `release: <nombre-de-la-release-helm>`. Al establecerlo en `false`, Prometheus monitorizará cualquier `ServiceMonitor` desplegado en el clúster independientemente de sus etiquetas de release.

---

### 3.3 El Modelo de Ingesta por Extracción (Scrape / Pull)

A diferencia de otros sistemas de monitoreo basados en agentes que empujan datos continuamente (modelo Push), **Prometheus opera por extracción periódica (Pull)**:
1. El servidor de Prometheus consulta a la API de Kubernetes para descubrir qué Pods y Servicios existen en el clúster.
2. Cada 15 segundos (intervalo de scrape), Prometheus establece una conexión HTTP GET hacia el puerto del contenedor (habitualmente `/metrics`).
3. El contenedor responde con un documento en texto plano estructurado según el estándar OpenMetrics.
4. Prometheus almacena los datos en su base de datos de series temporales (TSDB) añadiendo automáticamente las etiquetas del clúster (`namespace`, `pod`, `instance`).

---

### 3.4 Despliegue del Stack con Helm

Instalamos el repositorio oficial y desplegamos el chart con nuestro perfil ligero en el namespace dedicado `observability`:

```bash
# 1. Crear namespace de observabilidad
kubectl create namespace observability

# 2. Agregar el repositorio Helm de Prometheus Community
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# 3. Desplegar con nuestros valores optimizados
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace observability \
  --values manifests/01-prometheus/values-lab.yaml
```

Verificamos que todos los Pods alcancen el estado `Running` (el proceso toma entre 60 y 90 segundos):
```bash
kubectl get pods -n observability -l "release=prometheus"
```

Accedemos a la interfaz gráfica de Grafana exponiendo su puerto o mediante el NodePort 30080 configurado en los values:
```bash
# Opción port-forwarding (localhost:3000)
kubectl port-forward svc/prometheus-grafana 3000:80 -n observability
# Credenciales configuradas: admin / admin
```

---

## 4. Scraping Declarativo: ServiceMonitors y PromQL en la Práctica

### 4.1 La Abstracción del `ServiceMonitor`: Selectores y Puertos

En lugar de editar manualmente un fichero de configuración monolítico (`prometheus.yml`) cada vez que se despliega una nueva aplicación, en Kubernetes utilizamos el recurso personalizado **`ServiceMonitor`**.

Un `ServiceMonitor` actúa como un contrato declarativo entre el equipo de desarrollo de la aplicación y el equipo de infraestructura:

```
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
```

Examinemos el manifiesto `manifests/04-podinfo/podinfo.yaml`:
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: podinfo
  namespace: default
  labels:
    app.kubernetes.io/name: podinfo
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: podinfo
  endpoints:
  - port: http
    path: /metrics
    interval: 15s
```

---

### 4.2 Anatomía de una Métrica Prometheus y Formato OpenMetrics

Si consultamos directamente el endpoint `/metrics` de cualquier Pod de nuestra aplicación:
```bash
kubectl exec -it deploy/podinfo -- curl -s http://localhost:9898/metrics | grep http_requests_total
```
Obtendremos líneas con la siguiente estructura:
```text
# HELP http_requests_total Total number of HTTP requests made.
# TYPE http_requests_total counter
http_requests_total{handler="/status/500",method="GET",status="500"} 42
```
Los cuatro elementos constitutivos son:
1. **Nombre de la Métrica (`http_requests_total`):** Indica qué fenómeno se mide.
2. **Tipo de Métrica:**
   * **Counter:** Valor acumulativo monotónico que solo se incrementa o se reinicia a 0 en caso de reinicio de la aplicación (ej. número total de peticiones o bytes enviados).
   * **Gauge:** Valor instantáneo que puede subir o bajar arbitrariamente (ej. uso de memoria en bytes o número de conexiones activas).
   * **Histogram:** Muestreo de observaciones (habitualmente duraciones o tamaños de respuesta) ordenadas en cubos acumulativos (*buckets*).
3. **Etiquetas (*Labels*):** Pares clave-valor entre llaves (`status="500"`) que aportan dimensionalidad.
4. **Valor numérico:** Siempre de tipo coma flotante de 64 bits.

---

### 4.3 Consultas Esenciales en PromQL (`rate`, `histogram_quantile`, agregaciones)

Prometheus incluye **PromQL (Prometheus Query Language)**, un lenguaje funcional diseñado específicamente para operar sobre vectores de series temporales.

A continuación, las 4 consultas esenciales que todo administrador de Kubernetes debe dominar:

1. **Tasa de Peticiones por Segundo (RPS):**
   Dado que los counters crecen continuamente, nunca se grafica el valor absoluto del counter. Se utiliza la función `rate()` sobre una ventana de tiempo (ej. 5 minutos):
   ```promql
   rate(http_requests_total{namespace="default"}[5m])
   ```
2. **Tasa de Errores HTTP 5xx Agregada:**
   Suma las peticiones por segundo filtrando por códigos de estado que comiencen por 5:
   ```promql
   sum(rate(http_requests_total{status=~"5.."}[2m])) by (app, handler)
   ```
3. **Porcentaje de Error (Error Budget / Tasa Relativa):**
   ```promql
   (sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))) * 100
   ```
4. **Latencia Percentil 99 (P99) mediante Histogramas:**
   Calcula el tiempo de respuesta del 99% de las peticiones para detectar la latencia de cola (*tail latency*):
   ```promql
   histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
   ```

---

## 5. El Pilar de los Logs: Grafana Loki y Promtail en Modo Ligero

### 5.1 Por Qué Descartar Elasticsearch / Kibana en Laboratorios

Como se analizó en la sección 1, los clústeres de laboratorio sufren enormemente bajo la carga de Elasticsearch. La indexación completa de texto genera:
* **Frecuentes OOMKilled:** El proceso `java` de Elasticsearch consume toda la memoria disponible del nodo, forzando a Linux a invocar el OOM-Killer.
* **Corrupción de Índices:** Al apagar o reiniciar los nodos de laboratorio bruscamente, los índices de Lucene pueden corromperse.
* **Complejidad de Mantenimiento:** Exige configurar mapeos de esquemas, shards y réplicas.

---

### 5.2 Filosofía de Indexación de Loki: Menos Metadatos, Menor Consumo

**Grafana Loki** invierte completamente el paradigma de Elasticsearch inspirándose en la arquitectura de Prometheus:
* **Loki no indexa el cuerpo textual de los logs.**
* Loki únicamente indexa las **etiquetas de metadatos de Kubernetes** (`namespace`, `pod`, `container`, `app`).
* Los mensajes de log se agrupan en flujos continuos comprimidos con gzip (*streams*) y se almacenan directamente en bloques en el sistema de ficheros o almacenamiento de objetos.
* Cuando el usuario ejecuta una búsqueda de texto, Loki primero filtra los flujos a través del índice de etiquetas y luego ejecuta un `grep` multihilo ultra-rápido en memoria sobre los bloques descomprimidos.

El resultado es un sistema que consume hasta un **90% menos de memoria RAM** y un **75% menos de almacenamiento**.

---

### 5.3 Despliegue de Promtail como DaemonSet sobre `/var/log/pods`

Para recolectar los logs de los contenedores y enviarlos a Loki, desplegamos **Promtail** como un `DaemonSet` (un Pod por cada nodo de Kubernetes).

El contenedor del Pod escribe en su salida estándar (`stdout`/`stderr`). El runtime de contenedores de Kubernetes (containerd o CRI-O) captura esta salida y la guarda en el sistema de ficheros del nodo bajo la ruta estructurada:
`/var/log/pods/<namespace>_<pod-name>_<pod-uid>/<container-name>/<retry>.log`

Promtail monta este directorio en modo solo lectura, lee los nuevos ficheros mediante inotify, extrae los metadatos del nombre de la ruta y los envía a Loki vía HTTP POST:

```
+-----------------------------------------------------------------------------------------+
|                  MECANISMO DE RECOLECCIÓN DE LOGS CON PROMTAIL                          |
+-----------------------------------------------------------------------------------------+

  [ Pod: podinfo-69f8c... ] ---> escribe en stdout: '{"level":"error","msg":"fail"}'
             |
             v
  [ Kubelet / Containerd ] ----> vuelca a disco en el nodo:
                                 /var/log/pods/default_podinfo-.../podinfo/0.log
                                             |
                                             v (Montaje HostPath)
  [ Promtail DaemonSet Pod ] <---------------+
  - Lee la línea del log
  - Asigna etiquetas: {namespace="default", pod="podinfo-...", container="podinfod"}
  - Envía paquete HTTP POST a Loki: http://loki.observability.svc:3100/loki/api/v1/push
```

Desplegamos Loki y Promtail utilizando el archivo `manifests/02-loki-promtail/values-lab.yaml`:

```bash
# 1. Agregar el repositorio de Grafana
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# 2. Desplegar Loki y Promtail en modo monolithic
helm install loki grafana/loki-stack \
  --namespace observability \
  --values manifests/02-loki-promtail/values-lab.yaml
```

Verificamos la correcta ejecución del DaemonSet:
```bash
kubectl get daemonset promtail -n observability
kubectl get pods -n observability -l "app=promtail"
```

---

### 5.4 Consultas con LogQL: Filtros de Flujo, Parsing JSON y Métricas Derivadas

El lenguaje de consultas de Loki es **LogQL**. Su sintaxis es intencionadamente análoga a PromQL, dividiéndose en dos partes: el **Selector de Flujo** y los **Filtros de Tubería (*Pipeline Filters*)**.

1. **Selección Básica de Flujo:**
   ```logql
   {namespace="default", app="podinfo"}
   ```
2. **Filtro de Texto (Inspección tipo grep):**
   ```logql
   {namespace="default", app="podinfo"} |= "error" != "debug"
   ```
3. **Parseo Automático de JSON y Filtrado de Campos:**
   Si la aplicación genera logs estructurados en JSON:
   ```logql
   {namespace="default", app="podinfo"} | json | status >= 500
   ```
4. **Transformación de Logs en Métricas:**
   Podemos calcular la tasa de líneas de log de error por segundo en tiempo real:
   ```logql
   sum(rate({namespace="default", app="podinfo"} |= "error" [1m])) by (pod)
   ```

---

## 6. El Tercer Pilar: Trazabilidad Distribuida con Jaeger All-in-One

### 6.1 Anatomía de una Traza: Traces, Spans, Context Propagation y Trace ID

Las métricas alertan sobre un problema y los logs detallan qué ocurrió en una línea específica de código. Sin embargo, en una arquitectura de microservicios donde una petición entrante atraviesa un API Gateway, un servicio de autenticación, un servicio de catálogo y una base de datos, ninguno de los dos pilares anteriores responde a: **¿cuánto tiempo tardó cada servicio individual en responder a esa petición específica?**

Aquí entra en juego el **rastreo distribuido (*Distributed Tracing*)**:
* **Trace (Traza):** Representa el viaje completo de una petición a través de toda la malla de microservicios. Se identifica unívocamente mediante un **Trace ID** de 64 o 128 bits.
* **Span:** Representa una unidad individual de trabajo dentro de la traza (ej. una llamada HTTP saliente, una consulta SQL o una operación en memoria). Cuenta con un nombre, marca de tiempo de inicio, duración y etiquetas de contexto.
* **Context Propagation:** La técnica mediante la cual el cliente inyecta cabeceras HTTP estándar (estándar W3C `traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01`) que el servicio receptor lee y retransmite a sus llamadas subsiguientes.

```
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
```

---

### 6.2 Despliegue de Jaeger All-in-One en Memoria

Para evitar el despliegue de almacenes de datos complejos en nuestro laboratorio, utilizamos la imagen oficial `jaegertracing/all-in-one`. Este contenedor empaqueta el recolector de trazas, el motor de almacenamiento volátil en memoria y la interfaz de usuario web en un único ejecutable que consume menos de 100 MB de RAM.

Desplegamos el manifiesto `manifests/03-jaeger/jaeger-all-in-one.yaml`:

```bash
kubectl apply -f manifests/03-jaeger/jaeger-all-in-one.yaml
```

Verificamos el estado del Pod y del Servicio:
```bash
kubectl get pods -n observability -l "app.kubernetes.io/name=jaeger"
kubectl get svc -n observability -l "app.kubernetes.io/name=jaeger"
```

El servicio expone:
* Puerto `16686` (HTTP): Interfaz web de usuario (UI de Jaeger).
* Puerto `4317` (gRPC) / `4318` (HTTP): Endpoints nativos del estándar OpenTelemetry (OTLP) para la recepción directa de trazas.

Acceso a la interfaz web mediante port-forward:
```bash
kubectl port-forward svc/jaeger-query 16686:16686 -n observability
```

---

### 6.3 Recepción de Trazas OTLP y Consulta en la Interfaz Web

Cualquier aplicación moderna instrumentada con la librería de OpenTelemetry puede enviar sus datos a Jaeger simplemente configurando la variable de entorno:
```bash
OTEL_EXPORTER_OTLP_ENDPOINT="http://jaeger-collector.observability.svc:4318"
```
En la interfaz de Jaeger podremos:
1. Filtrar por nombre de servicio (`podinfo`).
2. Localizar las trazas con mayor duración o aquellas que hayan registrado la etiqueta `error=true`.
3. Hacer clic en una traza individual para ver el desglose en cascada (*waterfall view*) de cada microservicio participante.

---

## 7. El Centro de Mando: Correlación Multi-Pilar en Grafana

### 7.1 Configuración de Data Sources Unificados (Prometheus, Loki, Jaeger)

La verdadera potencia del stack radica en unificar los tres pilares bajo una única interfaz de control. Gracias a nuestro archivo `values-lab.yaml`, Grafana tiene preconfigurados los tres orígenes de datos:

1. **Prometheus:** `http://prometheus-k8s.observability.svc:9090` (Métricas).
2. **Loki:** `http://loki.observability.svc:3100` (Logs).
3. **Jaeger:** `http://jaeger-query.observability.svc:16686` (Trazas).

Para comprobarlos en la UI de Grafana:
* Navega al menú lateral &rarr; **Connections** &rarr; **Data Sources**.
* Comprueba que los tres Data Sources presenten el estado verde (*Data source is working*).

---

### 7.2 El Poder de la Vista *Explore* en Pantalla Dividida

La funcionalidad más destacada para la depuración en directo es la vista **Explore** con pantalla dividida (*Split Screen*):

```
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
```

Al hacer clic en el botón **Split** en la esquina superior derecha:
* En el panel izquierdo introducimos la métrica de Prometheus. Observamos el instante temporal exacto en el que ocurrió la anomalía (ej. 18:45).
* En el panel derecho seleccionamos Loki como origen de datos. Los rangos de tiempo de ambos paneles se sincronizan automáticamente.
* Al hacer zoom sobre el pico de la gráfica métrica, el panel de logs se actualiza inmediatamente mostrando las líneas emitidas en esa misma ventana de segundos.

---

### 7.3 Del Trace ID al Log Exacto: Cerrando el Círculo de la Observabilidad

Cuando la aplicación está configurada para volcar el `trace_id` en sus mensajes de log estructurados, Grafana permite crear un enlace derivado (*Derived Field*):
1. El operador observa el log de error en Grafana Loki.
2. La cadena `trace_id=4bf92f3577b34da6` se detecta mediante una expresión regular y se resalta automáticamente como un hipervínculo azul.
3. Al pulsar sobre el enlace, Grafana abre directamente la traza de Jaeger correspondiente en el panel contiguo, mostrando qué función o servicio externo tardó más de la cuenta.

---

## 8. El Experimento del Caos: Diagnóstico de un Incidente Real con Podinfo

### 8.1 Despliegue de la Aplicación de Prueba `podinfo` y su `ServiceMonitor`

Para poner en práctica los conocimientos adquiridos, utilizaremos el microservicio `podinfo` (ubicado en `manifests/04-podinfo/podinfo.yaml`):

```bash
kubectl apply -f manifests/04-podinfo/podinfo.yaml
```

Verificamos que los 2 Pods estén en estado `Ready`:
```bash
kubectl get pods -l app.kubernetes.io/name=podinfo
kubectl get servicemonitor podinfo
```

En la interfaz de Prometheus (`Status` &rarr; `Targets`), comprobamos que el endpoint `serviceMonitor/default/podinfo/0` aparezca en estado **UP (1/1)**.

---

### 8.2 Inyección de Fallos Controlados: Errores 500, Latencia y Pico de CPU

Para simular una degradación severa en el servicio, utilizaremos un Pod efímero con `curl` o un bucle bash desde un terminal:

1. **Inyección de Errores HTTP 500:**
   ```bash
   kubectl run curl-attacker --rm -i --tty --image=curlimages/curl -- sh -c '
     while true; do
       curl -s "http://podinfo.default.svc:9898/status/500" > /dev/null
       sleep 0.1
     done
   '
   ```
2. **Inyección de Carga Masiva de CPU:**
   En otra terminal, solicitamos a Podinfo que estrese la CPU durante 30 segundos:
   ```bash
   kubectl run cpu-stresser --rm -i --tty --image=curlimages/curl -- sh -c '
     curl -s "http://podinfo.default.svc:9898/stress-cpu?duration=30s"
   '
   ```

---

### 8.3 Resolución del Incidente en 4 Pasos Guiados

El alumno debe seguir el protocolo estándar de respuesta a incidentes en 4 pasos:

* **Paso 1 (Detección en Métricas):**
  En Grafana, consulta la tasa de fallos de la aplicación en PromQL:
  ```promql
  sum(rate(http_requests_total{status="500"}[1m])) by (pod)
  ```
  *Observación:* Se identifica que las dos réplicas de `podinfo` están sirviendo más de 10 peticiones fallidas por segundo.
* **Paso 2 (Aislamiento Temporal en Loki):**
  Pasa a la vista dividida (*Split*) y consulta los logs del Pod afectado en ese rango de tiempo:
  ```logql
  {app="podinfo"} |= "status=500"
  ```
  *Observación:* Se leen mensajes que indican un fallo inducido en el handler `/status/500`.
* **Paso 3 (Impacto en Recursos del Nodo):**
  Ejecuta la consulta nativa en la terminal:
  ```bash
  kubectl top pods -l app.kubernetes.io/name=podinfo
  ```
  *Observación:* Se aprecia que el Pod que recibió la llamada `/stress-cpu` alcanzó el límite de 100m de CPU asignado en su manifiesto.
* **Paso 4 (Verificación de Restauración):**
  Finaliza el proceso del Pod `curl-attacker` (Ctrl+C). Verifica en la gráfica de Prometheus cómo la curva desciende a cero y la aplicación recupera la normalidad operativa.

---

## 9. La Brecha hacia la Producción y Resolución de Problemas (Troubleshooting)

### 9.1 Almacenamiento Persistente en Producción: S3/MinIO y Thanos/Cortex

El stack desplegado en este taller utiliza almacenamiento local o en memoria, ideal para aprender sin incurrir en costes ni requerir infraestructura compleja. Sin embargo, en un entorno de producción empresarial deben tenerse en cuenta las siguientes transformaciones arquitectónicas:

```
+-----------------------------------------------------------------------------------------+
|                 COMPARATIVA: LABORATORIO VS ARQUITECTURA DE PRODUCCIÓN                  |
+-----------------------------------------------------------------------------------------+
|  Dimensión        | Entorno de Formación / Lab   | Entorno de Producción                |
+-------------------+------------------------------+--------------------------------------+
|  Almacenamiento   | Local (emptyDir / disco)     | Buckets de objetos S3 / GCS / Azure  |
|  de Logs (Loki)   | Retención: 24 horas          | Retención: 30 a 90 días              |
+-------------------+------------------------------+--------------------------------------+
|  Métricas a Largo | TSDB local de Prometheus     | Thanos / Cortex / VictoriaMetrics    |
|  Plazo (PromQL)   | Retención: 12 horas          | Retención: 1 a 2 años                |
+-------------------+------------------------------+--------------------------------------+
|  Almacén de       | Jaeger All-in-One en memoria | Grafana Tempo o Jaeger con Backend   |
|  Trazas           | Se pierden al reiniciar      | Cassandra / Elasticsearch persistente|
+-------------------+------------------------------+--------------------------------------+
|  Alta             | Réplica única (1 pod)        | Despliegue distribuido con micro-    |
|  Disponibilidad   | (Sin redundancia)            | servicios desacoplados (ingester...) |
+-------------------+------------------------------+--------------------------------------+
```

---

### 9.2 Error 1: Pods en `Pending` o `CrashLoopBackOff` por Falta de Recursos

* **Síntoma:** Al desplegar el stack, los Pods de Prometheus o Grafana quedan estancados en `Pending`.
* **Causa Raíz:** Los nodos del clúster no disponen de suficiente memoria RAM libre para satisfacer los `requests` declarados en los manifiestos.
* **Diagnóstico:**
  ```bash
  kubectl describe pod <nombre-del-pod> -n observability
  ```
  Buscar eventos del tipo: `0/1 nodes are available: 1 Insufficient memory`.
* **Solución:** Disminuir los valores de `requests.memory` en `values-lab.yaml` o añadir más memoria a la máquina virtual/nodo del clúster.

---

### 9.3 Error 2: `ServiceMonitor` No Recoge Métricas (Selector de Release Faltante)

* **Síntoma:** Se aplica el `ServiceMonitor`, pero el target no aparece en la interfaz de Prometheus (`Status` &rarr; `Targets`).
* **Causa Raíz:** Prometheus Operator ignora por defecto cualquier recurso que no tenga la etiqueta correspondiente a la release de Helm (ej. `release: prometheus`).
* **Solución:**
  Asegurarse de que en `values-lab.yaml` esté configurado:
  ```yaml
  prometheus:
    prometheusSpec:
      serviceMonitorSelectorNilUsesHelmValues: false
  ```
  O alternativamente, etiquetar el ServiceMonitor con el nombre de la release:
  ```bash
  kubectl label servicemonitor podinfo release=prometheus
  ```

---

### 9.4 Error 3: Promtail Sin Permisos RBAC para `/var/log/pods`

* **Síntoma:** Promtail inicia correctamente pero no envía logs a Loki; en sus logs se observan errores `permission denied`.
* **Causa Raíz:** En distribuciones de Kubernetes con SELinux estricto o políticas de Pod Security Standards (PSS) restringidas, el montaje del volumen `hostPath` sobre `/var/log/pods` queda bloqueado.
* **Solución:**
  Verificar que el `ClusterRole` y `ClusterRoleBinding` de Promtail cuenten con permisos sobre los recursos de pods y namespaces, y habilitar la opción `privileged: true` o el contexto de seguridad adecuado en el `values-lab.yaml` de Promtail.
