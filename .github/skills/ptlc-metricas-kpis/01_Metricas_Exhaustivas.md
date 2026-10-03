# Métricas de Rendimiento - Guía Exhaustiva

## Taxonomía de Métricas

### Clasificación por perspectiva

```
┌─────────────────────────────────────────────────────────────────┐
│                    MÉTRICAS DE PERFORMANCE                        │
├───────────────────┬─────────────────────┬───────────────────────┤
│  USER-FACING      │  SYSTEM-LEVEL       │  BUSINESS-LEVEL       │
│  (Experiencia)    │  (Infraestructura)  │  (Impacto)            │
├───────────────────┼─────────────────────┼───────────────────────┤
│ Response Time     │ CPU Utilization     │ Revenue per Second    │
│ Throughput        │ Memory Usage        │ Orders per Minute     │
│ Error Rate        │ Disk I/O            │ Cart Abandonment Rate │
│ Availability      │ Network I/O         │ Session Duration      │
│ Page Load Time    │ Thread Count        │ Conversion Rate       │
│ TTFB              │ Connection Pools    │ User Satisfaction     │
│ Apdex             │ GC Metrics          │ Cost per Transaction  │
└───────────────────┴─────────────────────┴───────────────────────┘
```

---

## Response Time - Análisis Profundo

### Componentes del Response Time

```
Total Response Time (End-to-End)
═════════════════════════════════
= DNS Resolution Time
+ TCP Connection Time (handshake)
+ TLS Handshake Time
+ Time to First Byte (TTFB)
  ├── Queue Time (waiting in server queue)
  ├── Processing Time (application logic)
  │   ├── Authentication/Authorization
  │   ├── Business Logic Execution
  │   ├── Database Query Time
  │   ├── Cache Lookup Time
  │   ├── External Service Call Time
  │   └── Serialization/Rendering
  └── Transfer Time (sending response)
+ Content Download Time
```

### Desglose típico (healthy system)

```
Component             │ Time    │ % of Total │ Notes
──────────────────────┼─────────┼────────────┼──────────────
DNS Resolution        │   5ms   │    2.5%    │ Cached after first
TCP Handshake         │  15ms   │    7.5%    │ Keep-alive reduces
TLS Handshake         │  30ms   │   15.0%    │ Session resumption helps
Queue Time            │   5ms   │    2.5%    │ Should be minimal
App Processing        │  80ms   │   40.0%    │ Main optimization target
  ├─ DB Queries       │  40ms   │   20.0%    │ Often the bottleneck
  ├─ Business Logic   │  25ms   │   12.5%    │ Code efficiency
  └─ Serialization    │  15ms   │    7.5%    │ JSON/XML rendering
Transfer Time         │  65ms   │   32.5%    │ Depends on payload size
──────────────────────┼─────────┼────────────┼──────────────
TOTAL                 │ 200ms   │  100.0%    │
```

### Estadística de Response Times

#### ¿Por qué NO usar solo el promedio?

```
Ejemplo: 10 requests con estos tiempos (ms):
100, 120, 110, 130, 105, 115, 125, 108, 112, 5000

Average: 592.5ms ← ENGAÑOSO (1 outlier distorsiona todo)
Median (P50): 115ms ← Más representativo
P90: 130ms
P95: 2565ms
P99: 5000ms
StdDev: 1472ms ← Muy alta variabilidad

CONCLUSIÓN: El promedio sugiere un problema moderado,
pero la realidad es que 9 de 10 users tienen excelente
experiencia (115ms) y solo 1 sufre (5000ms).
```

#### Histograma de response times

```
Distribución típica (log-normal):

Freq
 ███
 ████
 ██████
 ████████
 ██████████
 ████████████
 ██████████████
 ███████████████
 ████████████████                          ██
 ██████████████████                    ████████
 ████████████████████            ████████████████
─┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──→ ms
 0  100 200 300 500 750 1000    2000    5000

La mayoría de requests son rápidas,
con una "cola larga" (long tail) de requests lentas.
```

### Time to First Byte (TTFB)

```
TTFB = Tiempo desde que se envía la request 
       hasta que se recibe el PRIMER byte de la response

Importancia:
- Refleja puramente el tiempo de servidor (sin transferencia)
- Elimina el efecto del tamaño del payload
- Mejor indicador de rendimiento backend

Benchmarks típicos:
- Excelente: < 100ms
- Bueno: < 200ms
- Aceptable: < 500ms
- Lento: 500ms - 1s
- Inaceptable: > 1s
```

---

## Throughput - Análisis Profundo

### Tipos de throughput

| Métrica | Unidad | Qué mide |
|---------|--------|----------|
| **RPS** (Requests/sec) | req/s | Todas las HTTP requests |
| **TPS** (Transactions/sec) | txn/s | Transacciones de negocio completadas |
| **Pages/sec** | pages/s | Páginas completas servidas |
| **Bytes/sec** | bytes/s | Volumen de datos transferidos |
| **Records/sec** | rec/s | Para batch processing |

### Relación entre Throughput, Users y Response Time

#### Little's Law
```
L = λ × W

Donde:
L = Número promedio de requests concurrentes en el sistema
λ = Throughput (requests por segundo)
W = Tiempo promedio de procesamiento (response time)

Ejemplo:
Si λ = 100 RPS y W = 0.5s
Entonces L = 100 × 0.5 = 50 requests concurrentes en el sistema

Implicación: Si response time sube (W↑), para mantener
            el mismo throughput (λ), se necesitan más resources (L↑)
```

#### Throughput Curve

```
TPS
 ├─── Zona A ───├── Zona B ──├── Zona C ──┤
     (linear)      (plateau)     (decline)
800 ┤                 ────────────
    │               ╱             ╲
600 ┤             ╱                 ╲
    │           ╱                     ╲
400 ┤         ╱                         ╲
    │       ╱
200 ┤     ╱
    │   ╱
  0 ┤─╱
    └──────────────────────────────────────→ Concurrent Users
    0    200    400    600    800   1000

Zona A: Throughput crece linealmente con usuarios
        (sistema tiene capacidad disponible)
        
Zona B: Throughput se estabiliza (plateau/saturation)
        (algún recurso está al máximo)
        
Zona C: Throughput DECRECE con más usuarios
        (overhead de contención supera capacidad)
```

### Throughput bajo carga

```
THROUGHPUT ANALYSIS TABLE

Load Level │ Expected TPS │ Actual TPS │ Efficiency │ Notes
───────────┼──────────────┼────────────┼────────────┼──────────
100 users  │     100      │     98     │    98%     │ ✅ Linear
200 users  │     200      │    195     │    98%     │ ✅ Linear
400 users  │     400      │    380     │    95%     │ ✅ Near-linear
600 users  │     600      │    540     │    90%     │ ⚠️ Starting to saturate
800 users  │     800      │    650     │    81%     │ ⚠️ Contention visible
1000 users │    1000      │    680     │    68%     │ ❌ Saturated
1200 users │    1200      │    620     │    52%     │ ❌ Declining!

Knee point: ~500 users (donde eficiencia empieza a caer)
Max useful throughput: ~680 TPS (at 1000 users)
Optimal operating point: 400-600 users (95-90% efficiency)
```

---

## Error Rate - Análisis Profundo

### Clasificación de errores

```
TIPOS DE ERRORES EN PERFORMANCE TESTING
════════════════════════════════════════

1. HTTP Client Errors (4xx)
   ├── 400 Bad Request      → Script issue o data problem
   ├── 401 Unauthorized     → Token expired, auth issue
   ├── 403 Forbidden        → Permission issue
   ├── 404 Not Found        → Data mismatch
   ├── 408 Request Timeout  → Client-side timeout
   └── 429 Too Many Requests → Rate limiting active

2. HTTP Server Errors (5xx)
   ├── 500 Internal Error   → Application crash/exception
   ├── 502 Bad Gateway      → Upstream server failure
   ├── 503 Service Unavail  → Server overloaded
   └── 504 Gateway Timeout  → Backend timeout

3. Connection Errors
   ├── Connection Refused   → Server not accepting connections
   ├── Connection Reset     → Server dropped connection
   ├── Connection Timeout   → Unable to establish connection
   └── DNS Resolution Fail  → DNS issue

4. Application Errors (200 but wrong)
   ├── Empty response body  → App returned nothing
   ├── Error in response    → {"error": "something broke"}
   └── Wrong content        → Got login page instead of data
```

### Error Rate Patterns

```
Pattern 1: Sudden Error Spike
Error %
 50 ┤                    ┌───┐
    │                    │   │
 25 │                    │   │
    │                    │   │
  0 ┤────────────────────┘   └───────
    → Causa: Un componente crasheó y se reinició

Pattern 2: Gradual Error Growth
Error %
 20 ┤                              ╱
 15 ┤                          ╱──┘
 10 ┤                    ╱────┘
  5 ┤              ╱────┘
  0 ┤─────────────┘
    → Causa: Resource exhaustion gradual (pool, memory)

Pattern 3: Constant Low-Level Errors
Error %
  3 ┤───────────────────────────────
    │
  0 ┤
    → Causa: Puede ser normal (timeouts ocasionales)
              o un bug funcional constante

Pattern 4: Load-Correlated Errors
Error %
 10 ┤     ┌─────────────────┐
    │    /│                 │\
  5 ┤   / │                 │ \
    │  /  │                 │  \
  0 ┤─┘   │ (during load)  │   └──
    → Causa: Capacity-related (solo bajo carga)
```

---

## Percentiles y Distribución

### Interpretación de percentiles

```
PERCENTILE INTERPRETATION GUIDE
════════════════════════════════

P50 (Median): "The typical user experience"
  - Half of users are faster, half are slower
  - Good for understanding "normal" performance

P90: "90% of users are this fast or faster"
  - 1 in 10 users experience worse
  - Common SLA target for web applications

P95: "95% of users are this fast or faster"
  - 1 in 20 users experience worse
  - Common SLA target for critical transactions

P99: "99% of users are this fast or faster"
  - 1 in 100 users experience worse
  - Important for high-traffic systems
  - At 1M requests/day: 10,000 users affected!

P99.9: "999 out of 1000 are this fast"
  - Critical for financial/healthcare systems
  - At 1M requests/day: 1,000 users still affected

RULE OF THUMB:
If P99/P50 ratio > 10x → High variability, investigate outliers
If P99/P50 ratio < 3x  → Very consistent performance
```

### Apdex Score

```
APPLICATION PERFORMANCE INDEX (Apdex)
═════════════════════════════════════

Formula: Apdex = (Satisfied + Tolerating/2) / Total

Where:
- Satisfied:  response_time ≤ T (threshold)
- Tolerating: T < response_time ≤ 4T
- Frustrated: response_time > 4T

Example with T = 2 seconds, 1000 requests:
- 800 requests < 2s (Satisfied)
- 150 requests between 2-8s (Tolerating)
- 50 requests > 8s (Frustrated)

Apdex = (800 + 150/2) / 1000 = (800 + 75) / 1000 = 0.875

INTERPRETATION:
1.00:       Perfect (all satisfied)
0.94-1.00:  Excellent
0.85-0.93:  Good
0.70-0.84:  Fair
0.50-0.69:  Poor
< 0.50:     Unacceptable
```

---

## Métricas de Infraestructura Detalladas

### CPU Metrics

```
CPU UTILIZATION BREAKDOWN
═════════════════════════

%user:   Time spent in user-space code (application)
%system: Time spent in kernel-space (OS operations)
%iowait: Time waiting for I/O completion
%idle:   Time doing nothing

Healthy breakdown:
%user=60%, %system=8%, %iowait=2%, %idle=30%

Problematic patterns:
- High %user:   CPU-bound application (optimize code)
- High %system: Too many syscalls, context switches
- High %iowait: Waiting for disk (optimize I/O or add SSD)
- High %steal:  VM contention (noisy neighbor in cloud)

Per-core analysis matters:
- 4 cores at 50% avg might mean 1 core at 100% + 3 at 33%
- Single-threaded bottleneck won't show in average CPU!
```

### Memory Metrics

```
MEMORY ANALYSIS
═══════════════

Total Memory = Used + Free + Buffers + Cache

Application Memory:
├── Heap (Java: Old Gen + Young Gen)
│   ├── Used Heap: Active objects
│   └── Free Heap: Available for allocation
├── Non-Heap (Metaspace, Code Cache)
├── Thread Stacks
└── Native Memory (JNI, Direct Buffers)

Key Indicators:
┌────────────────────────┬───────────────┬──────────────────────┐
│ Metric                 │ Healthy       │ Problematic          │
├────────────────────────┼───────────────┼──────────────────────┤
│ Heap Usage             │ Sawtooth ≤80% │ Continuously growing │
│ GC Frequency           │ Predictable   │ Increasing over time │
│ GC Pause Duration      │ < 200ms       │ > 1 second           │
│ GC Time % of total     │ < 5%          │ > 10%                │
│ Old Gen after GC       │ Stable        │ Growing (leak!)      │
│ Swap Usage             │ 0 bytes       │ Any swap = bad       │
└────────────────────────┴───────────────┴──────────────────────┘
```

### Network Metrics

```
NETWORK PERFORMANCE METRICS
════════════════════════════

Bandwidth Utilization:
- Measure: bytes in/out per second
- Threshold: < 60% of available bandwidth
- Alert: > 80% sustained

TCP Connections:
- ESTABLISHED: Active connections
- TIME_WAIT: Connections closing (should drain)
- CLOSE_WAIT: App not closing connections (leak!)
- SYN_RECEIVED: Pending connections (queue)

Key Ratios:
- Retransmission rate: < 1% normal, > 3% problematic
- Packet loss: < 0.1% acceptable
- Out-of-order packets: < 0.5% acceptable

Connection Pool Health:
┌──────────────────┬───────────────┬──────────────────┐
│ Metric           │ Healthy       │ Investigate      │
├──────────────────┼───────────────┼──────────────────┤
│ Pool utilization │ < 70%         │ > 85%            │
│ Wait time        │ < 10ms        │ > 100ms          │
│ Timeout errors   │ 0             │ Any              │
│ Active/Idle ratio│ Balanced      │ All active       │
└──────────────────┴───────────────┴──────────────────┘
```

---

## Calculadora de Métricas

### Fórmulas esenciales

```
═══════════════════════════════════════════════════════════

Throughput:
  TPS = Total_Successful_Transactions / Test_Duration_Seconds
  RPS = Total_Requests / Test_Duration_Seconds

Error Rate:
  Error_Rate = (Failed_Requests / Total_Requests) × 100

Concurrent Users (Little's Law):
  Concurrent_Users = Throughput × Avg_Response_Time

Network Bandwidth Required:
  BW = Avg_Response_Size × RPS × 8 (bits/byte)
  Example: 50KB × 500 RPS × 8 = 200 Mbps

Pacing Calculation:
  Pacing = Target_Iteration_Time - (Total_Think_Time + Total_Response_Time)

Users Needed for Target TPS:
  Users = Target_TPS × (Avg_Think_Time + Avg_Response_Time)
  Example: 100 TPS × (5s + 0.5s) = 550 concurrent users

Test Data Volume:
  Unique_Records_Needed = Users × Iterations_per_User × Records_per_Iteration
  Example: 1000 × 20 × 3 = 60,000 unique records

═══════════════════════════════════════════════════════════
```

---

*Documento de referencia - Performance Test Life Cycle*
*Última actualización: Junio 2026*
