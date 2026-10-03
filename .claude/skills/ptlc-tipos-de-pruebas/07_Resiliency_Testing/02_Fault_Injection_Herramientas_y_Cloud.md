# 🛡️ Resiliency Testing — Parte 2 de 3: Fault injection, herramientas y cloud-native

> Qué fallas inyectar, con qué herramienta, cómo automatizarlas en CI/CD y dónde inyectarlas en Kubernetes, Istio y multi-región.
>
> **Guía en 3 partes:** · 1 · [`Fundamentos, steady-state hypothesis y patrones de resiliencia`](01_Fundamentos_y_Patrones_de_Resiliencia.md) · **2 · Fault injection, herramientas y cloud-native** (este documento) · 3 · [`Experimentos, Game Days, métricas y código`](03_Experimentos_Metricas_y_Operacion.md)
## Índice

7. [Tipos de Fault Injection](#7-tipos-de-fault-injection)
8. [Herramientas de Resiliency Testing](#8-herramientas-de-resiliency-testing)
12. [Integración con CI/CD](#12-integración-con-cicd)
14. [Resiliency en Arquitecturas Cloud-Native](#14-resiliency-en-arquitecturas-cloud-native)

> Índice completo de las 3 partes (secciones 1-16): [`01_Fundamentos_y_Patrones_de_Resiliencia.md`](01_Fundamentos_y_Patrones_de_Resiliencia.md#índice) · [Referencias](01_Fundamentos_y_Patrones_de_Resiliencia.md#referencias)

---

## 7. Tipos de Fault Injection

### 7.1 Fallas de Red

| Tipo de Falla | Descripción | Herramienta |
|---------------|-------------|-------------|
| Latencia | Agregar delay a paquetes | tc netem, Gremlin |
| Packet Loss | Descartar % de paquetes | tc netem, iptables |
| DNS Failure | Resolver a IP incorrecta | iptables, CoreDNS |
| Partition | Aislar nodo/servicio de la red | iptables, Chaos Mesh |
| Bandwidth Limit | Reducir ancho de banda | tc, wondershaper |
| Connection Reset | Resetear conexiones TCP | iptables RST |
| SSL/TLS Error | Certificados inválidos | mitmproxy |

**Ejemplo con tc (Traffic Control):**
```bash
# Agregar 200ms de latencia con 50ms de jitter
tc qdisc add dev eth0 root netem delay 200ms 50ms

# Simular 5% de packet loss
tc qdisc add dev eth0 root netem loss 5%

# Simular packet corruption
tc qdisc add dev eth0 root netem corrupt 2%

# Combinar: latencia + loss
tc qdisc add dev eth0 root netem delay 100ms loss 3%

# Remover reglas
tc qdisc del dev eth0 root
```

### 7.2 Fallas de Compute

| Tipo de Falla | Descripción | Cómo simular |
|---------------|-------------|--------------|
| CPU Stress | Saturar CPU al 100% | stress-ng, cpu burn |
| Memory Exhaustion | Consumir toda la RAM | stress-ng --vm |
| Disk Full | Llenar el disco | fallocate, dd |
| Process Kill | Matar proceso | kill -9, Chaos Monkey |
| OOM Kill | Forzar Out of Memory | cgroups limits |
| I/O Saturation | Saturar disco I/O | fio, stress-ng |
| Fork Bomb | Agotar PIDs | ulimit + fork |

**Ejemplo con stress-ng:**
```bash
# CPU stress: 4 workers al 90% por 60 segundos
stress-ng --cpu 4 --cpu-load 90 --timeout 60s

# Memory: consumir 2GB
stress-ng --vm 2 --vm-bytes 1G --timeout 60s

# I/O: saturar disco
stress-ng --io 4 --hdd 2 --timeout 60s

# Combinado
stress-ng --cpu 2 --cpu-load 80 --vm 1 --vm-bytes 512M --io 2 --timeout 120s
```

### 7.3 Fallas de Aplicación

| Tipo de Falla | Descripción | Método |
|---------------|-------------|--------|
| Exception Injection | Lanzar excepciones en código | Feature flags, AOP |
| Response Delay | Agregar delay a responses | Service mesh (Istio) |
| Error Response | Retornar HTTP 500/503 | Proxy, mock |
| Corrupt Data | Retornar datos malformados | Proxy interceptor |
| Memory Leak | Simular leak gradual | Código controlado |
| Thread Deadlock | Bloquear threads | Código controlado |
| Connection Pool Exhaust | Agotar conexiones | Never-close connections |

### 7.4 Fallas de Dependencias

| Tipo de Falla | Descripción | Impacto esperado |
|---------------|-------------|------------------|
| Database Down | Base de datos inaccesible | Fallback a cache/queue |
| Cache Miss | Redis/Memcached caído | Ir directo a DB (mayor latencia) |
| Queue Full | Message broker saturado | Backpressure, retry |
| Third-party API Down | Servicio externo no responde | Datos cacheados/default |
| Certificate Expiry | TLS cert expirado | Connection refused |
| Auth Service Down | No se pueden validar tokens | Graceful deny o cache |

### 7.5 Fallas de Infraestructura

| Tipo de Falla | Descripción | Escala |
|---------------|-------------|--------|
| Instance Termination | Matar una VM/container | Nodo individual |
| AZ Failure | Perder zona de disponibilidad | Regional |
| Region Failure | Perder región completa | Multi-region |
| Load Balancer Failure | LB no enruta tráfico | Ingress |
| DNS Outage | Resolución DNS falla | Global |
| Storage Failure | EBS/disk no disponible | Persistencia |

---

## 8. Herramientas de Resiliency Testing

### 8.1 Comparativa de Herramientas

| Herramienta | Tipo | Entorno | Complejidad | Costo |
|-------------|------|---------|-------------|-------|
| Chaos Monkey | OSS | AWS | Baja | Gratis |
| Gremlin | Comercial | Multi-cloud | Media | $$$$ |
| LitmusChaos | OSS (CNCF) | Kubernetes | Media | Gratis |
| Chaos Mesh | OSS (CNCF) | Kubernetes | Media | Gratis |
| AWS FIS | Managed | AWS | Baja | $ (por experimento) |
| Azure Chaos Studio | Managed | Azure | Baja | $ |
| Chaos Toolkit | OSS | Agnóstico | Alta | Gratis |
| Pumba | OSS | Docker | Baja | Gratis |
| PowerfulSeal | OSS | Kubernetes | Media | Gratis |
| Toxiproxy | OSS | Cualquiera | Baja | Gratis |
| Simmy | OSS (.NET) | Aplicación | Baja | Gratis |

### 8.2 LitmusChaos (Kubernetes)

```yaml
# Ejemplo: ChaosEngine para matar pods
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: payment-service-chaos
  namespace: production
spec:
  appinfo:
    appns: 'production'
    applabel: 'app=payment-service'
    appkind: 'deployment'
  engineState: 'active'
  chaosServiceAccount: litmus-admin
  experiments:
    - name: pod-delete
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: '60'        # Duración del caos (segundos)
            - name: CHAOS_INTERVAL
              value: '10'        # Intervalo entre deletes
            - name: FORCE
              value: 'true'      # Force delete (kill -9)
            - name: PODS_AFFECTED_PERC
              value: '50'        # % de pods afectados
        probe:
          - name: "check-payment-endpoint"
            type: "httpProbe"
            httpProbe/inputs:
              url: "http://payment-service:8080/health"
              method:
                get:
                  criteria: "=="
                  responseCode: "200"
            mode: "Continuous"
            runProperties:
              probeTimeout: 5
              interval: 5
              retry: 3
```

### 8.3 Chaos Mesh (Kubernetes)

```yaml
# Ejemplo: Network chaos - agregar latencia
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: network-delay-payment
  namespace: chaos-testing
spec:
  action: delay
  mode: all
  selector:
    namespaces:
      - production
    labelSelectors:
      app: payment-service
  delay:
    latency: "500ms"
    correlation: "50"
    jitter: "100ms"
  duration: "5m"
  scheduler:
    cron: "@every 2h"  # Ejecutar cada 2 horas
```

### 8.4 AWS Fault Injection Simulator

```json
{
  "description": "Kill 30% of ECS tasks in payment service",
  "targets": {
    "payment-tasks": {
      "resourceType": "aws:ecs:task",
      "selectionMode": "PERCENT(30)",
      "resourceTags": {
        "service": "payment"
      }
    }
  },
  "actions": {
    "stop-tasks": {
      "actionId": "aws:ecs:stop-task",
      "parameters": {},
      "targets": {
        "Tasks": "payment-tasks"
      },
      "startAfter": ["wait-for-steady-state"]
    },
    "wait-for-steady-state": {
      "actionId": "aws:fis:wait",
      "parameters": {
        "duration": "PT2M"
      }
    }
  },
  "stopConditions": [
    {
      "source": "aws:cloudwatch:alarm",
      "value": "arn:aws:cloudwatch:us-east-1:123456789:alarm:PaymentErrorRate"
    }
  ],
  "roleArn": "arn:aws:iam::123456789:role/FISRole"
}
```

### 8.5 Toxiproxy (Proxy de fallas)

```bash
# Crear proxy para PostgreSQL
toxiproxy-cli create postgres_primary \
  --listen 0.0.0.0:5432 \
  --upstream postgres-primary:5432

# Agregar latencia
toxiproxy-cli toxic add postgres_primary \
  --type latency \
  --attribute latency=500 \
  --attribute jitter=100

# Simular timeout (slow_close)
toxiproxy-cli toxic add postgres_primary \
  --type slow_close \
  --attribute delay=3000

# Simular connection reset
toxiproxy-cli toxic add postgres_primary \
  --type reset_peer \
  --attribute timeout=2000

# Bandwidth limit (1KB/s - extremadamente lento)
toxiproxy-cli toxic add postgres_primary \
  --type bandwidth \
  --attribute rate=1
```

### 8.6 Chaos Toolkit (Framework agnóstico)

```json
{
  "title": "Payment Service Resilience Experiment",
  "description": "Verificar que el servicio de pagos sobrevive la caída de Redis",
  "tags": ["payment", "redis", "resilience"],
  "steady-state-hypothesis": {
    "title": "Payment service responde normalmente",
    "probes": [
      {
        "type": "probe",
        "name": "payment-health-check",
        "tolerance": 200,
        "provider": {
          "type": "http",
          "url": "http://payment-service:8080/health",
          "timeout": 3
        }
      },
      {
        "type": "probe",
        "name": "payment-success-rate",
        "tolerance": {
          "type": "range",
          "range": [95.0, 100.0]
        },
        "provider": {
          "type": "python",
          "module": "chaosprometheus.probes",
          "func": "query_instant",
          "arguments": {
            "query": "sum(rate(payment_success_total[5m])) / sum(rate(payment_total[5m])) * 100"
          }
        }
      }
    ]
  },
  "method": [
    {
      "type": "action",
      "name": "kill-redis-primary",
      "provider": {
        "type": "python",
        "module": "chaosaws.ecs.actions",
        "func": "stop_task",
        "arguments": {
          "cluster": "production",
          "task": "redis-primary",
          "reason": "Chaos experiment: Redis resilience test"
        }
      },
      "pauses": {
        "after": 60
      }
    }
  ],
  "rollbacks": [
    {
      "type": "action",
      "name": "restart-redis",
      "provider": {
        "type": "python",
        "module": "chaosaws.ecs.actions",
        "func": "start_task",
        "arguments": {
          "cluster": "production",
          "task_definition": "redis-primary:latest"
        }
      }
    }
  ]
}
```

---

## 12. Integración con CI/CD

### Pipeline de Resiliency Testing

```yaml
# .github/workflows/resilience-tests.yml
name: Resilience Tests

on:
  schedule:
    - cron: '0 2 * * 1-5'  # Lun-Vie a las 2 AM
  workflow_dispatch:
    inputs:
      experiment:
        description: 'Experiment to run'
        required: true
        type: choice
        options:
          - pod-kill
          - network-latency
          - resource-exhaustion
          - dependency-failure

jobs:
  resilience-test:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup kubectl
        uses: azure/setup-kubectl@v3
        
      - name: Connect to cluster
        run: |
          aws eks update-kubeconfig --name staging-cluster
          
      - name: Verify steady state
        run: |
          ./scripts/verify-steady-state.sh
          
      - name: Run chaos experiment
        run: |
          kubectl apply -f chaos-experiments/${{ inputs.experiment }}.yaml
          
      - name: Wait for experiment duration
        run: sleep 300  # 5 minutes
        
      - name: Verify system resilience
        run: |
          ./scripts/verify-resilience-criteria.sh
          
      - name: Cleanup chaos
        if: always()
        run: |
          kubectl delete chaosengine --all -n chaos-testing
          
      - name: Collect results
        run: |
          ./scripts/collect-experiment-results.sh > results.json
          
      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: resilience-results-${{ github.run_id }}
          path: results.json
          
      - name: Notify on failure
        if: failure()
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "⚠️ Resilience test FAILED: ${{ inputs.experiment }}"
            }
```

### Shift-Left Resilience

```
┌──────────────────────────────────────────────────────────────────┐
│                    SHIFT-LEFT RESILIENCE                          │
├──────────┬──────────────┬────────────────┬──────────────────────┤
│   DEV    │     CI       │    STAGING     │     PRODUCTION       │
├──────────┼──────────────┼────────────────┼──────────────────────┤
│ Unit     │ Integration  │ Chaos          │ Game Days            │
│ tests    │ tests con    │ experiments    │ Continuous           │
│ con      │ Toxiproxy    │ automatizados  │ chaos                │
│ Simmy/   │              │ (LitmusChaos)  │ (Chaos Monkey)       │
│ fault    │ Contract     │                │                      │
│ stubs    │ tests con    │ Full fault     │ Regional             │
│          │ timeouts     │ injection      │ failover             │
│ Timeout  │              │ suite          │ drills               │
│ tests    │ Circuit      │                │                      │
│          │ breaker      │ Game Day       │ Automated            │
│ Retry    │ validation   │ (equipo)       │ blast radius         │
│ logic    │              │                │ monitoring           │
│ tests    │              │                │                      │
└──────────┴──────────────┴────────────────┴──────────────────────┘
```

---

## 14. Resiliency en Arquitecturas Cloud-Native

### Kubernetes Resilience Patterns

```yaml
# Deployment con todas las buenas prácticas de resiliencia
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service
spec:
  replicas: 3
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0  # Zero-downtime deploys
  template:
    spec:
      # Anti-affinity: no 2 pods en el mismo nodo
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app: payment-service
                topologyKey: kubernetes.io/hostname
      
      # Topology spread: distribuir entre AZs
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels:
              app: payment-service
      
      containers:
        - name: payment
          image: payment-service:v2.1.0
          resources:
            requests:
              cpu: "500m"
              memory: "512Mi"
            limits:
              cpu: "1000m"
              memory: "1Gi"
          
          # Probes para self-healing
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 10
            failureThreshold: 3    # 3 fallas → restart
          
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
            failureThreshold: 2    # 2 fallas → remove from LB
          
          startupProbe:
            httpGet:
              path: /healthz
              port: 8080
            failureThreshold: 30   # 30 × 2s = 60s para arrancar
            periodSeconds: 2

---
# PodDisruptionBudget: mínimo 2 pods siempre activos
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: payment-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: payment-service

---
# HorizontalPodAutoscaler: auto-scale bajo presión
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: payment-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: payment-service
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: "1000"
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 30   # Escalar rápido
      policies:
        - type: Percent
          value: 100
          periodSeconds: 30
    scaleDown:
      stabilizationWindowSeconds: 300  # Des-escalar lento (5 min)
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
```

### Service Mesh Resilience (Istio)

```yaml
# VirtualService con retry, timeout y circuit breaker
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: payment-service
spec:
  hosts:
    - payment-service
  http:
    - route:
        - destination:
            host: payment-service
      timeout: 5s
      retries:
        attempts: 3
        perTryTimeout: 2s
        retryOn: "5xx,reset,connect-failure,retriable-4xx"

---
# DestinationRule con circuit breaker y connection pool
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: payment-service
spec:
  host: payment-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
        connectTimeout: 30ms
      http:
        h2UpgradePolicy: DEFAULT
        http1MaxPendingRequests: 100
        http2MaxRequests: 1000
        maxRequestsPerConnection: 10
        maxRetries: 3
    outlierDetection:  # Circuit breaker
      consecutive5xxErrors: 5
      interval: 10s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
      minHealthPercent: 50
```

### Multi-Region Resilience

```
┌────────────────────────────────────────────────────────────────┐
│                    MULTI-REGION ARCHITECTURE                    │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│                    ┌──────────────┐                            │
│                    │  Global DNS  │                            │
│                    │ (Route 53)   │                            │
│                    └──────┬───────┘                            │
│                           │                                    │
│              ┌────────────┼────────────┐                      │
│              │            │            │                       │
│     ┌────────▼───┐  ┌────▼────┐  ┌───▼────────┐             │
│     │ US-EAST-1  │  │ EU-WEST │  │ AP-SOUTH   │             │
│     │ (Primary)  │  │ (Active)│  │ (Active)   │             │
│     ├────────────┤  ├─────────┤  ├────────────┤             │
│     │ App (3 AZ) │  │App(3 AZ)│  │ App (3 AZ) │             │
│     │ DB Primary │  │DB Replica│  │ DB Replica │             │
│     │ Cache      │  │ Cache   │  │ Cache      │             │
│     └────────────┘  └─────────┘  └────────────┘             │
│                                                                │
│  FALLA REGIÓN US-EAST-1:                                      │
│  1. Health check falla (30s)                                  │
│  2. DNS failover a EU-WEST (60s TTL)                         │
│  3. EU-WEST promueve DB replica a primary                    │
│  4. Tráfico US redistribuido a EU-WEST + AP-SOUTH            │
│  5. RTO total: < 3 minutos                                   │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

**Qué validar en Resiliency Testing multi-region:**
- DNS failover timing (< 60s)
- Database promotion timing
- Data consistency post-failover (RPO)
- Client retry behavior durante failover
- Cache warming en región de destino
- Capacidad de la región receptora para absorber tráfico adicional
