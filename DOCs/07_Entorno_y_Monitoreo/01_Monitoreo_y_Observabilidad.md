# Monitoreo y Observabilidad para Performance Testing

## Stack de Observabilidad Moderno

### Los Tres Pilares de la Observabilidad

```
┌─────────────────────────────────────────────────────────────┐
│                    OBSERVABILIDAD                             │
├───────────────────┬─────────────────────┬───────────────────┤
│      METRICS      │       LOGS          │      TRACES       │
│   (Qué pasó)     │  (Por qué pasó)     │  (Dónde pasó)     │
├───────────────────┼─────────────────────┼───────────────────┤
│ • CPU, Memory     │ • Application logs  │ • Request flow    │
│ • Response time   │ • Error stack traces│ • Service-to-svc  │
│ • Throughput      │ • Audit events      │ • DB queries      │
│ • Error count     │ • Debug info        │ • External calls  │
│ • Saturation      │ • Business events   │ • Timing breakdown│
├───────────────────┼─────────────────────┼───────────────────┤
│ Prometheus        │ ELK Stack           │ Jaeger            │
│ Grafana           │ Loki                │ Zipkin            │
│ Datadog           │ Splunk              │ Tempo             │
│ CloudWatch        │ Fluentd             │ OpenTelemetry     │
└───────────────────┴─────────────────────┴───────────────────┘
```

---

## Prometheus + Grafana Stack

### Arquitectura para Performance Testing

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ App Server 1 │     │ App Server 2 │     │ App Server N │
│ ┌──────────┐ │     │ ┌──────────┐ │     │ ┌──────────┐ │
│ │ Exporter │ │     │ │ Exporter │ │     │ │ Exporter │ │
│ └────┬─────┘ │     │ └────┬─────┘ │     │ └────┬─────┘ │
└──────┼───────┘     └──────┼───────┘     └──────┼───────┘
       │                    │                    │
       └────────────────────┼────────────────────┘
                            │ scrape
                   ┌────────▼────────┐
                   │   PROMETHEUS    │
                   │  (Time Series   │
                   │   Database)     │
                   └────────┬────────┘
                            │ query
                   ┌────────▼────────┐
                   │    GRAFANA      │
                   │  (Visualization │
                   │   & Alerting)   │
                   └─────────────────┘
```

### PromQL Queries Esenciales para Performance Testing

```promql
# CPU Utilization (per instance)
100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory Utilization
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

# HTTP Request Rate (from app metrics)
sum(rate(http_requests_total[1m])) by (method, status_code)

# Response Time P95 (histogram)
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, handler))

# Error Rate
sum(rate(http_requests_total{status_code=~"5.."}[5m])) 
/ sum(rate(http_requests_total[5m])) * 100

# Active Connections
sum(node_netstat_Tcp_CurrEstab)

# Disk I/O Utilization
rate(node_disk_io_time_seconds_total[5m]) * 100

# GC Pause Time (JVM)
rate(jvm_gc_pause_seconds_sum[5m])

# Database Connection Pool
hikaricp_connections_active / hikaricp_connections_max * 100

# Queue Depth (RabbitMQ)
rabbitmq_queue_messages_ready
```

### Grafana Dashboard para Performance Testing

```json
{
  "dashboard": {
    "title": "Performance Test - Live Monitoring",
    "panels": [
      {
        "title": "Active Virtual Users",
        "type": "stat",
        "targets": [{"expr": "k6_vus"}]
      },
      {
        "title": "Response Time P95",
        "type": "timeseries",
        "targets": [
          {"expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[1m])) by (le))"}
        ]
      },
      {
        "title": "Throughput (RPS)",
        "type": "timeseries",
        "targets": [
          {"expr": "sum(rate(http_requests_total[1m]))"}
        ]
      },
      {
        "title": "Error Rate (%)",
        "type": "timeseries",
        "targets": [
          {"expr": "sum(rate(http_requests_total{status=~'5..'}[1m])) / sum(rate(http_requests_total[1m])) * 100"}
        ],
        "thresholds": [{"value": 1, "color": "red"}]
      },
      {
        "title": "CPU Utilization (all servers)",
        "type": "timeseries",
        "targets": [
          {"expr": "100 - avg by(instance)(rate(node_cpu_seconds_total{mode='idle'}[1m])) * 100"}
        ]
      },
      {
        "title": "Memory Usage",
        "type": "timeseries",
        "targets": [
          {"expr": "(1 - node_memory_MemAvailable_bytes/node_memory_MemTotal_bytes) * 100"}
        ]
      },
      {
        "title": "DB Connection Pool",
        "type": "gauge",
        "targets": [
          {"expr": "hikaricp_connections_active / hikaricp_connections_max * 100"}
        ],
        "thresholds": [
          {"value": 70, "color": "yellow"},
          {"value": 85, "color": "red"}
        ]
      }
    ]
  }
}
```

---

## OpenTelemetry

### Instrumentación estándar

```
OpenTelemetry proporciona:
├── APIs & SDKs (vendor-neutral instrumentation)
├── Collector (receive, process, export telemetry)
├── Semantic Conventions (standard naming)
└── Auto-instrumentation (zero-code agents)

Architecture:
┌──────────┐    ┌──────────────────┐    ┌────────────────┐
│ App +    │───▶│  OTel Collector  │───▶│  Backends      │
│ OTel SDK │    │  (processing)    │    │  Prometheus    │
└──────────┘    └──────────────────┘    │  Jaeger        │
                                        │  Grafana Tempo │
                                        │  Datadog       │
                                        └────────────────┘
```

### Configuración del Collector

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 5s
    send_batch_size: 1000
  memory_limiter:
    limit_mib: 512

exporters:
  prometheus:
    endpoint: "0.0.0.0:8889"
  jaeger:
    endpoint: "jaeger:14250"
    tls:
      insecure: true
  loki:
    endpoint: "http://loki:3100/loki/api/v1/push"

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, memory_limiter]
      exporters: [jaeger]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]
    logs:
      receivers: [otlp]
      processors: [batch]
      exporters: [loki]
```

---

## Alerting para Performance Testing

### Reglas de alerta durante ejecución

```yaml
# prometheus-alerts.yaml
groups:
  - name: performance_test_alerts
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[2m])) 
          / sum(rate(http_requests_total[2m])) > 0.05
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Error rate exceeds 5%"
          description: "Current error rate: {{ $value | humanizePercentage }}"
          
      - alert: HighResponseTime
        expr: |
          histogram_quantile(0.95, 
            sum(rate(http_request_duration_seconds_bucket[2m])) by (le)
          ) > 5
        for: 3m
        labels:
          severity: warning
        annotations:
          summary: "P95 response time exceeds 5 seconds"
          
      - alert: HighCPU
        expr: |
          100 - avg(rate(node_cpu_seconds_total{mode="idle"}[2m])) * 100 > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "CPU utilization above 85% for 5 minutes"
          
      - alert: MemoryLeak
        expr: |
          predict_linear(
            node_memory_MemAvailable_bytes[30m], 3600
          ) < 0
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "Memory predicted to exhaust within 1 hour"
          
      - alert: DBConnectionPoolExhaustion
        expr: |
          hikaricp_connections_active / hikaricp_connections_max > 0.9
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "DB connection pool >90% utilized"
```

---

## Monitoreo de Base de Datos

### PostgreSQL Performance Monitoring

```sql
-- Active queries and their duration
SELECT pid, now() - pg_stat_activity.query_start AS duration,
       query, state, wait_event_type, wait_event
FROM pg_stat_activity
WHERE (now() - pg_stat_activity.query_start) > interval '5 seconds'
AND state != 'idle'
ORDER BY duration DESC;

-- Index usage statistics
SELECT relname, indexrelname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;  -- Low scan count = potentially unused index

-- Table bloat and dead tuples
SELECT relname, n_live_tup, n_dead_tup,
       round(n_dead_tup::numeric / NULLIF(n_live_tup, 0) * 100, 2) as dead_pct
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;

-- Connection statistics
SELECT count(*) as total,
       count(*) FILTER (WHERE state = 'active') as active,
       count(*) FILTER (WHERE state = 'idle') as idle,
       count(*) FILTER (WHERE state = 'idle in transaction') as idle_in_txn
FROM pg_stat_activity;

-- Lock monitoring
SELECT blocked_locks.pid AS blocked_pid,
       blocking_locks.pid AS blocking_pid,
       blocked_activity.query AS blocked_query,
       blocking_activity.query AS blocking_query
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;

-- Cache hit ratio (should be > 99%)
SELECT 
  sum(heap_blks_read) as heap_read,
  sum(heap_blks_hit)  as heap_hit,
  round(sum(heap_blks_hit) / 
    NULLIF(sum(heap_blks_hit) + sum(heap_blks_read), 0) * 100, 2) 
    as cache_hit_ratio
FROM pg_statio_user_tables;
```

### Key DB Metrics Dashboard

```
┌─────────────────────────────────────────────────┐
│  DATABASE PERFORMANCE DASHBOARD                  │
├────────────────────────┬────────────────────────┤
│  Active Queries: 45    │  Connections: 180/200  │
│  Avg Query Time: 12ms  │  Idle in Txn: 3       │
├────────────────────────┼────────────────────────┤
│  Cache Hit Ratio: 99.2%│  Deadlocks/min: 0     │
│  Rows Read/s: 45,000   │  Lock Waits: 2        │
├────────────────────────┴────────────────────────┤
│  [Slow Queries Log - Last 5 minutes]            │
│  1. SELECT * FROM orders WHERE... (3.2s)        │
│  2. UPDATE inventory SET... (1.8s)              │
│  3. INSERT INTO audit_log... (1.1s)             │
└─────────────────────────────────────────────────┘
```

---

## Docker Compose - Stack de Monitoreo Completo

```yaml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus:latest
    ports: ["9090:9090"]
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - ./alerts.yml:/etc/prometheus/alerts.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.retention.time=30d'

  grafana:
    image: grafana/grafana:latest
    ports: ["3000:3000"]
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - ./grafana/dashboards:/var/lib/grafana/dashboards
      - ./grafana/datasources:/etc/grafana/provisioning/datasources

  node-exporter:
    image: prom/node-exporter:latest
    ports: ["9100:9100"]
    
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    ports: ["8080:8080"]
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro

  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"  # UI
      - "14250:14250"  # gRPC
      - "4317:4317"    # OTLP gRPC

  loki:
    image: grafana/loki:latest
    ports: ["3100:3100"]

  alertmanager:
    image: prom/alertmanager:latest
    ports: ["9093:9093"]
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml
```

---

*Documento de referencia - Performance Test Life Cycle*
*Última actualización: Junio 2026*
