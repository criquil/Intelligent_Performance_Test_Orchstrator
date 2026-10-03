# Configuration, Failover, Recovery, Regression y otros tipos de pruebas

## 7. Configuration Testing (Performance)

### Definición
El **Configuration Testing** evalúa el impacto de **cambios en la configuración del sistema** sobre el rendimiento. Permite encontrar la configuración óptima sin cambiar código.

### ¿Qué se configura?

```
CAPAS DE CONFIGURACIÓN:
═══════════════════════

Application Layer:
├── Thread pool size (min/max threads)
├── Connection pool size
├── Cache size y TTL
├── Session timeout
├── Request timeout
├── Async thread count
├── Batch sizes
└── Rate limiting thresholds

JVM/Runtime:
├── Heap size (-Xms, -Xmx)
├── GC algorithm (G1, ZGC, Shenandoah)
├── GC parameters (pause targets, regions)
├── Thread stack size
├── Direct memory
└── JIT compilation thresholds

Database:
├── shared_buffers / buffer_pool_size
├── work_mem / sort_buffer_size
├── max_connections
├── effective_cache_size
├── checkpoint_segments
├── wal_buffers
└── query_cache_size

Web Server:
├── Worker processes/threads
├── Keep-alive timeout
├── Max connections per worker
├── Buffer sizes
├── Gzip compression level
└── Upload size limits

OS Level:
├── File descriptor limits
├── TCP buffer sizes
├── Swappiness
├── I/O scheduler
├── Network queue sizes
└── Kernel semaphores
```

### Metodología: A/B Configuration Testing

```yaml
configuration_ab_test:
  approach: "Change ONE variable at a time, measure impact"
  
  test_matrix:
    baseline:
      db_pool: 100
      thread_pool: 200
      heap: "4GB"
      gc: "G1GC"
      result: "P95 = 2.1s, TPS = 450"
      
    variant_a:
      change: "db_pool: 100 → 200"
      result: "P95 = 1.6s, TPS = 520"
      impact: "-24% response time, +16% throughput ✅"
      
    variant_b:
      change: "db_pool: 100 → 300"
      result: "P95 = 1.5s, TPS = 530"
      impact: "Only marginal improvement over 200 ⚠️"
      conclusion: "200 is optimal (diminishing returns)"
      
    variant_c:
      change: "heap: 4GB → 8GB"
      result: "P95 = 2.0s, TPS = 460"
      impact: "Minimal improvement, longer GC pauses"
      conclusion: "4GB sufficient, 8GB not worth it"
      
    variant_d:
      change: "gc: G1GC → ZGC"
      result: "P95 = 1.9s, P99 = 2.2s (was 4.5s)"
      impact: "P99 dramatically improved (lower pause)"
      conclusion: "ZGC reduces tail latency significantly ✅"

  optimal_config:
    db_pool: 200
    thread_pool: 200
    heap: "4GB"
    gc: "ZGC"
    expected: "P95 = 1.4s, TPS = 540"
```

### Reglas de Configuration Testing

```
1. SOLO UN CAMBIO A LA VEZ
   (Para aislar el impacto de cada variable)
   
2. MISMA CARGA EN TODAS LAS VARIANTES
   (Para comparación válida)
   
3. MÚLTIPLES EJECUCIONES POR VARIANTE
   (Mínimo 3 para confianza estadística)
   
4. DOCUMENTAR TODO
   (Configuración exacta + resultados + conclusión)
   
5. BUSCAR DIMINISHING RETURNS
   (Más no siempre es mejor: 200 → 300 pool puede no justificarse)
   
6. CONSIDERAR TRADE-OFFS
   (Más heap = mejor throughput pero peor GC pause)
```

---

## 8. Failover Testing

### Definición
El **Failover Testing** evalúa el rendimiento del sistema **durante y después de un evento de failover** (cuando un componente falla y otro toma su lugar).

### Escenarios de failover

```yaml
failover_scenarios:

  app_server_failure:
    setup: "4 app servers behind load balancer"
    action: "Kill 1 server during load test"
    measure:
      - "Time for LB to detect failure"
      - "Requests lost during detection window"
      - "Impact on response time (remaining 3 servers)"
      - "Recovery when killed server returns"
    acceptance:
      detection_time: "< 10 seconds"
      lost_requests: "< 0.1%"
      response_time_impact: "< 33% increase (capacity reduced 25%)"
      
  database_failover:
    setup: "Primary DB + Hot Standby (synchronous replication)"
    action: "Kill primary DB"
    measure:
      - "Time for automatic failover"
      - "Transactions lost during failover"
      - "Response time during promotion"
      - "Connection re-establishment time"
    acceptance:
      failover_time: "< 30 seconds"
      data_loss: "ZERO (synchronous replication)"
      total_impact_duration: "< 60 seconds"
      
  cache_failure:
    setup: "Redis cluster with 3 nodes"
    action: "Kill 1 Redis node"
    measure:
      - "Cache miss rate increase"
      - "DB load increase"
      - "Response time impact"
      - "Auto-recovery time"
    acceptance:
      cache_miss_spike: "< 50% for < 30 seconds"
      response_time_increase: "< 100% during recovery"
      
  availability_zone_failure:
    setup: "Multi-AZ deployment"
    action: "Simulate AZ outage"
    measure:
      - "Cross-AZ failover time"
      - "Capacity reduction impact"
      - "Data consistency"
    acceptance:
      failover_time: "< 60 seconds"
      service_continuity: "No user-facing outage"
```

### Timeline de un failover bien manejado

```
FAILOVER TIMELINE (Good):
═════════════════════════

T+0s:     Component fails
T+5s:     Health check detects failure
T+10s:    Load balancer marks as unhealthy
T+10s:    Traffic rerouted to healthy instances
T+15s:    Alert fires to on-call team
T+30s:    System stabilized at reduced capacity
T+2min:   Auto-scaling adds replacement instance
T+5min:   Full capacity restored

User impact: ~5 seconds of elevated error rate
Data loss: ZERO
Manual intervention needed: NONE

──────────────────────────────────────────────────

FAILOVER TIMELINE (Bad):
═════════════════════════

T+0s:     Component fails
T+30s:    Health check timeout (too long!)
T+60s:    LB still sending traffic to dead node
T+60s:    Connection queue fills up
T+90s:    Cascading failures begin
T+120s:   50% error rate
T+180s:   Alert fires (too late!)
T+300s:   Manual intervention begins
T+600s:   System partially recovered

User impact: 5+ minutes of major outage
Data loss: Unknown (possible)
Manual intervention: REQUIRED
```

---

## 9. Recovery Testing

### Definición
El **Recovery Testing** mide la capacidad del sistema de **volver a operación normal** después de un fallo, sobrecarga o evento disruptivo. Se enfoca en el "después" del problema.

### Tipos de recovery

```
RECOVERY TYPES:
═══════════════

1. AUTO-RECOVERY (sin intervención humana)
   ├── Restart automático de proceso
   ├── Auto-scaling después de stress
   ├── Cache rebuild automático
   └── Connection pool refresh

2. GRACEFUL RECOVERY (con asistencia mínima)
   ├── Rollback de deployment
   ├── Database failover con script
   ├── Cache invalidation manual
   └── Config change + restart

3. MANUAL RECOVERY (intervención completa)
   ├── Restore from backup
   ├── Data reconstruction
   ├── Infrastructure re-provisioning
   └── Full system restart
```

### Métricas de Recovery

| Métrica | Definición | Target |
|---------|-----------|--------|
| **RTO** (Recovery Time Objective) | Tiempo máximo tolerable de downtime | Depende del SLA |
| **RPO** (Recovery Point Objective) | Máxima pérdida de datos tolerable | Depende del negocio |
| **Time to Detection** | Tiempo para detectar el problema | < 1 minuto |
| **Time to Mitigation** | Tiempo para reducir impacto | < 5 minutos |
| **Time to Recovery** | Tiempo para volver a normal 100% | < 15 minutos |
| **Recovery Completeness** | % de funcionalidad restaurada | 100% |

### Test de Recovery post-stress

```yaml
recovery_test:
  phase_1_establish_normal:
    duration: "15 minutes"
    load: "Normal (1000 users)"
    verify: "All SLAs met, baseline metrics"
    
  phase_2_apply_stress:
    duration: "10 minutes"
    load: "Beyond capacity (3000 users)"
    expect: "System degrades or partially fails"
    
  phase_3_remove_load:
    action: "Drop ALL traffic instantly"
    verify: "System begins recovery"
    
  phase_4_measure_recovery:
    measure:
      - "Time until error rate = 0%"
      - "Time until response time returns to baseline (±10%)"
      - "Time until CPU returns to baseline"
      - "Time until all connections released"
      - "Time until queues drain"
      - "GC behavior post-stress"
    
  phase_5_validate_post_recovery:
    action: "Re-apply normal load"
    duration: "15 minutes"
    verify:
      - "Performance equals pre-stress baseline"
      - "No lingering degradation"
      - "No data loss or corruption"
      - "All services healthy"
      
  classification:
    excellent: "Full recovery in < 1 minute"
    good: "Full recovery in 1-5 minutes"
    acceptable: "Full recovery in 5-15 minutes"
    poor: "Recovery requires > 15 minutes"
    critical: "Manual intervention required"
```

---

## 10. Regression Testing (Performance)

### Definición
El **Performance Regression Testing** detecta **degradaciones de rendimiento** introducidas entre versiones del software, comparando automáticamente contra una baseline establecida.

### Cuándo ejecutar

```
TRIGGERS PARA REGRESSION TEST:
═════════════════════════════

✅ Cada merge a main/master
✅ Cada release candidate
✅ Después de refactoring significativo
✅ Después de upgrade de dependencias
✅ Después de cambio de ORM/framework
✅ Después de migración de datos
✅ Antes de release a producción
```

### Implementación en CI/CD

```javascript
// k6: regression-test.js
// Ejecuta los mismos escenarios que load test pero más corto
// Se compara automáticamente contra baseline almacenada

export const options = {
  scenarios: {
    quick_regression: {
      executor: 'constant-vus',
      vus: 50,
      duration: '10m',
    },
  },
  thresholds: {
    // Thresholds relativos a baseline (loaded from file)
    'http_req_duration{name:Login}': [`p(95)<${BASELINE.login_p95 * 1.15}`],
    'http_req_duration{name:Search}': [`p(95)<${BASELINE.search_p95 * 1.15}`],
    'http_req_duration{name:Checkout}': [`p(95)<${BASELINE.checkout_p95 * 1.15}`],
    // Allow 15% degradation before failing
  },
};
```

### Reporte de regresión

```
PERFORMANCE REGRESSION REPORT
═════════════════════════════
Comparison: v3.2.2 vs v3.2.1 (baseline)

Transaction    │ Baseline (P95) │ Current (P95) │ Change  │ Status
───────────────┼────────────────┼───────────────┼─────────┼────────
Login          │     1.2s       │     1.3s      │  +8%    │ ✅ OK
Search         │     1.8s       │     2.9s      │  +61%   │ ❌ REGRESSION
Checkout       │     3.0s       │     3.2s      │  +7%    │ ✅ OK
Browse         │     0.8s       │     0.85s     │  +6%    │ ✅ OK

REGRESSION DETECTED in Search (+61%)
Git blame: Commit abc123 "Added full-text search logging"
Author: developer@company.com
Impact: Synchronous log write in search hot path

RECOMMENDATION: Make logging async or remove from search path
ACTION: Block release until fixed
```

---

## 11. Network Performance Testing

### Definición
Evalúa el impacto de **condiciones de red** en el rendimiento de la aplicación: latencia, pérdida de paquetes, ancho de banda limitado.

### Escenarios

```yaml
network_testing:
  
  latency_impact:
    conditions:
      - { latency: "0ms", description: "Same datacenter" }
      - { latency: "20ms", description: "Same region" }
      - { latency: "100ms", description: "Cross-continent" }
      - { latency: "300ms", description: "Satellite/remote" }
    measure: "Response time increase per added latency"
    
  bandwidth_limitation:
    conditions:
      - { bandwidth: "100 Mbps", description: "Fiber" }
      - { bandwidth: "10 Mbps", description: "Corporate" }
      - { bandwidth: "4G", description: "Mobile 4G" }
      - { bandwidth: "3G", description: "Mobile 3G" }
    measure: "Page load time, API response size impact"
    
  packet_loss:
    conditions:
      - { loss: "0%", description: "Normal" }
      - { loss: "1%", description: "Mild congestion" }
      - { loss: "5%", description: "Poor connection" }
      - { loss: "10%", description: "Very poor" }
    measure: "Retransmission impact, timeout frequency"
    
  tools:
    - "tc (Linux traffic control)"
    - "NetEm (network emulator)"
    - "Charles Proxy"
    - "Comcast (Go tool for network simulation)"
```

---

## 12. API Performance Testing

### Definición
Testing específico de **endpoints API** (REST, GraphQL, gRPC) enfocado en rendimiento a nivel de servicio sin considerar UI.

### Métricas específicas de API

| Métrica | Descripción | Target típico |
|---------|-------------|---------------|
| TTFB | Time to first byte | < 200ms |
| Response size | Payload size | < 1MB |
| Rate limit behavior | Requests antes de throttle | Per plan |
| Pagination performance | Tiempo por página | Constante |
| Batch endpoint | Time vs items count | Linear or better |
| Concurrent connections | Per-client limit | As documented |

### Test patterns para APIs

```yaml
api_performance_patterns:
  
  pagination_test:
    description: "¿La paginación es eficiente?"
    test:
      - "GET /api/items?page=1&limit=20 → measure time"
      - "GET /api/items?page=100&limit=20 → measure time"
      - "GET /api/items?page=10000&limit=20 → measure time"
    expected: "Time should be roughly constant (good indexing)"
    common_issue: "OFFSET pagination degrades at high page numbers"
    
  n_plus_1_detection:
    description: "¿Hay N+1 queries ocultas?"
    test:
      - "GET /api/orders?include=items → measure with 10 orders"
      - "GET /api/orders?include=items → measure with 100 orders"
      - "GET /api/orders?include=items → measure with 1000 orders"
    expected: "Time grows sub-linearly (batch loading)"
    red_flag: "Linear time growth = N+1 pattern"
    
  payload_size_test:
    description: "¿Responses grandes impactan?"
    test:
      - "Compare: with compression vs without"
      - "Compare: full object vs summary"
      - "Compare: embedded vs linked resources"
    optimization: "Use fields/sparse fieldsets to reduce payload"
```

---

## 13. Frontend/Browser Performance Testing

### Definición
Mide el rendimiento **percibido por el usuario** en el navegador, incluyendo rendering, interactividad y estabilidad visual.

### Core Web Vitals (Google)

```
CORE WEB VITALS:
════════════════

LCP (Largest Contentful Paint):
- ¿Cuándo se renderiza el contenido principal?
- Good: < 2.5s | Needs work: 2.5-4s | Poor: > 4s

FID (First Input Delay) → INP (Interaction to Next Paint):
- ¿Cuánto tarda el browser en responder a interacción?
- Good: < 200ms | Needs work: 200-500ms | Poor: > 500ms

CLS (Cumulative Layout Shift):
- ¿Cuánto se mueve el contenido después de cargar?
- Good: < 0.1 | Needs work: 0.1-0.25 | Poor: > 0.25

ADDITIONAL:
TTFB (Time to First Byte): < 800ms
FCP (First Contentful Paint): < 1.8s
TBT (Total Blocking Time): < 200ms
TTI (Time to Interactive): < 3.8s
```

### Herramientas para Browser Performance

```
Synthetic Testing:
├── Lighthouse (Google) - Auditoría automática
├── WebPageTest - Multi-location testing
├── k6 browser - Load testing con browser real
└── Playwright/Puppeteer - Scripted browser tests

Real User Monitoring (RUM):
├── Google Analytics (Web Vitals)
├── New Relic Browser
├── Datadog RUM
└── SpeedCurve
```

---

## 14. Isolation Testing

### Definición
El **Isolation Testing** consiste en **aislar un componente específico** para confirmar que un problema de rendimiento detectado es reproducible y está localizado en ese componente.

### Cuándo usar

```
Situación: Load test muestra degradación, pero no está claro qué componente causa el problema.

Proceso de isolation:
1. Identificar sospechoso (ej: "parece ser la base de datos")
2. Aislar: Test SOLO contra la DB (sin app, sin network complexity)
3. Reproducir: ¿Se reproduce el problema en aislamiento?
   - SÍ → Confirmado: DB es el bottleneck
   - NO → El problema es en la interacción entre componentes
4. Repetir con otro sospechoso si NO se confirmó
```

### Técnicas de aislamiento

| Técnica | Descripción |
|---------|-------------|
| Mock dependencias | Reemplazar servicios con mocks rápidos |
| Test directo a DB | Queries directas sin app layer |
| Test de red aislado | Medir latencia/bandwidth sin app |
| Component benchmark | Benchmark de función/módulo aislado |
| A/B environment | Comparar con/sin componente sospechoso |

---

## 15. Saturation Testing

### Definición
El **Saturation Testing** determina el punto en el cual un recurso específico alcanza **100% de utilización**, y evalúa el impacto en el rendimiento general del sistema.

### Recursos a saturar

```
POR CADA RECURSO:
═════════════════

1. CPU Saturation Test
   - Incrementar carga hasta CPU = 100%
   - Medir: ¿Qué pasa con response time? ¿Errores?
   - ¿Se degrada gradualmente o colapsó súbitamente?

2. Memory Saturation Test
   - Cargar hasta memoria = 100%
   - ¿GC storms? ¿OOM kill? ¿Swap?
   - ¿Cuánto antes del 100% empieza la degradación?

3. Connection Pool Saturation
   - Consumir todas las connections
   - ¿Qué pasa con nuevas requests? ¿Queue? ¿Timeout?
   - ¿Recovery time cuando se liberan connections?

4. Disk I/O Saturation
   - Generar carga I/O hasta saturación
   - ¿Impact en read performance? ¿Write latency?
   - ¿Queue depth behavior?

5. Network Bandwidth Saturation
   - Saturar el enlace de red
   - ¿Packet loss? ¿Retransmissions?
   - ¿TCP window adjustment?

6. Thread Pool Saturation
   - Consumir todos los threads disponibles
   - ¿Requests queued? ¿Rejected?
   - ¿Timeout behavior?
```

### Resultado típico de saturation analysis

```
SATURATION ANALYSIS RESULTS:
════════════════════════════

Resource         │ Saturates At │ Impact when saturated    │ Recovery
─────────────────┼──────────────┼──────────────────────────┼──────────
DB Conn Pool     │   800 users  │ Timeouts, 503 errors     │ 30 seconds
CPU (App)        │  1100 users  │ Linear RT degradation    │ Immediate
Thread Pool      │  1300 users  │ Request rejection (503)  │ Immediate
Memory           │  2000 users  │ GC storms → OOM kill     │ Restart req
Disk I/O         │  N/A         │ Never reached            │ N/A
Network          │  N/A         │ Never reached            │ N/A

FIRST TO SATURATE: DB Connection Pool (800 users)
→ This is the system's WEAKEST LINK
→ Priority fix: Increase pool OR optimize connection hold time
```

---

## Mapa Completo de Tipos de Pruebas

```
MAPA COMPLETO: TODOS LOS TIPOS DE PERFORMANCE TESTING
══════════════════════════════════════════════════════════

                    VALIDATION          LIMITS           DURATION
                    ──────────          ──────           ────────
Smoke ─────────── Script validation    1-3 VUs          2-5 min
Baseline ─────── Reference point       1-10 VUs         15-30 min
Load ──────────── SLA compliance       Expected load    2-4 hours
Peak ──────────── Max expected traffic Peak projected   4-8 hours
Stress ────────── Breaking point       Beyond capacity  30-60 min
Spike ─────────── Sudden load change   Bursts           30-60 min
Endurance/Soak ── Time degradation     Normal load      8-72 hours
Volume ────────── Data handling        Normal + big data 1-4 hours
Scalability ───── Scaling efficiency   Variable         2-6 hours
Capacity ──────── Max within SLA       Incremental      2-4 hours
Breakpoint ────── Exact failure point  Extreme          1-2 hours
Concurrency ───── Race conditions      Synchronized     15-30 min
Configuration ─── Tuning impact        Constant         Multiple runs
Failover ──────── HA validation        Normal + failure 1-2 hours
Recovery ──────── Post-failure state   Stress → 0       1-2 hours
Regression ────── Version comparison   Standard         10-30 min
Reliability ───── Long-term stability  Normal + faults  24-72 hours
Network ───────── Condition impact     Normal + degraded 1-2 hours
API ───────────── Service performance  Variable         1-2 hours
Browser/Frontend─ User perception      Variable         30-60 min
Isolation ─────── Component confirm    Targeted         15-30 min
Saturation ────── Resource limits      Extreme targeted 1-2 hours
```

---

*Documento de referencia - Performance Test Life Cycle*
*Última actualización: Junio 2026*
