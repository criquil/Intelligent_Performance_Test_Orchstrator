# Root Cause Analysis y Técnicas de Troubleshooting

## Framework de Análisis Sistemático

### Proceso de RCA para Performance

```
┌──────────────────────────────────────────────────────────────┐
│                ROOT CAUSE ANALYSIS PROCESS                     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. OBSERVE: ¿Qué síntoma se observa?                       │
│     ↓                                                        │
│  2. MEASURE: ¿Qué datos lo confirman?                       │
│     ↓                                                        │
│  3. HYPOTHESIZE: ¿Qué podría causarlo?                      │
│     ↓                                                        │
│  4. TEST: ¿Cómo validar/invalidar la hipótesis?             │
│     ↓                                                        │
│  5. IDENTIFY: ¿Cuál es la causa raíz?                       │
│     ↓                                                        │
│  6. RESOLVE: ¿Cuál es la solución?                          │
│     ↓                                                        │
│  7. VERIFY: ¿Se resolvió el problema?                       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Técnicas de RCA

### 1. Los 5 Porqués (5 Whys)

```
EJEMPLO COMPLETO: "La API de checkout tiene timeout"

¿Por qué hay timeout en checkout?
→ Porque la query de validación de inventario tarda > 30 segundos

¿Por qué la query tarda > 30 segundos?
→ Porque hace un full table scan en la tabla 'inventory' (50M rows)

¿Por qué hace full table scan?
→ Porque no existe índice en (product_id, warehouse_id)

¿Por qué no existe el índice?
→ Porque la migración #342 que lo creaba falló silenciosamente

¿Por qué falló silenciosamente?
→ Porque el pipeline no valida que las migraciones se aplicaron exitosamente

ROOT CAUSE: Falta de validación de migraciones en CI/CD
FIX INMEDIATO: Crear el índice manualmente
FIX ESTRUCTURAL: Agregar step de validación de schema en pipeline
```

### 2. Fishbone Diagram (Ishikawa)

```
                    PROBLEMA: Response time > 5s en /api/search
                    ─────────────────────────────────────────────
                              │
    ┌─────────────────────────┼─────────────────────────────┐
    │                         │                             │
    │   APPLICATION           │         DATABASE            │
    │   ├─ N+1 queries        │         ├─ Missing index    │
    │   ├─ No caching         │         ├─ Lock contention  │
    │   ├─ Sync processing    │         ├─ Large result sets│
    │   └─ Memory pressure    │         └─ Connection pool  │
    │                         │                             │
    ├─────────────────────────┼─────────────────────────────┤
    │                         │                             │
    │   INFRASTRUCTURE        │         CONFIGURATION       │
    │   ├─ CPU saturation     │         ├─ Thread pool size │
    │   ├─ Network latency    │         ├─ Timeout values   │
    │   ├─ Disk I/O           │         ├─ JVM heap size    │
    │   └─ Load balancer      │         └─ Cache TTL        │
    │                         │                             │
    └─────────────────────────┼─────────────────────────────┘
                              │
                    ──────────▼──────────
```

### 3. Drill-Down Analysis

```
Nivel 1: ¿Qué transacción es lenta?
→ T05_Checkout (P95 = 4.2s, SLA = 3s)

Nivel 2: ¿Qué request dentro del checkout?
→ POST /api/checkout/payment (contribuye 3.5s de 4.2s)

Nivel 3: ¿Qué componente dentro del payment request?
→ Database call to validate_inventory() = 2.8s
→ External call to payment_gateway = 0.5s
→ Application logic = 0.2s

Nivel 4: ¿Qué pasa en validate_inventory()?
→ SQL: SELECT stock FROM inventory WHERE product_id IN (...)
→ Execution plan: Seq Scan on inventory (cost=0..945123)
→ Rows examined: 50,000,000 (full table scan!)

Nivel 5: ¿Por qué full table scan?
→ No index on inventory(product_id)
→ Table has 50M rows without proper indexing

ROOT CAUSE FOUND: Missing index on inventory.product_id
```

### 4. Comparative Analysis

```
COMPARISON: Good Run vs Bad Run

Metric              │  Good (Jun 5)  │  Bad (Jun 10)  │  Delta
────────────────────┼────────────────┼────────────────┼──────────
App Version         │  3.2.1         │  3.2.2         │  Changed!
Users               │  1000          │  1000          │  Same
P95 Response        │  1.8s          │  4.2s          │  +133%
Throughput          │  550 TPS       │  380 TPS       │  -31%
Error Rate          │  0.2%          │  2.1%          │  +950%
CPU Avg             │  65%           │  82%           │  +26%
DB Query Avg        │  45ms          │  280ms         │  +522%
DB Connections      │  120/200       │  195/200       │  +63%

CONCLUSION: Version 3.2.2 introduced a DB performance regression
INVESTIGATION: Check git diff between 3.2.1 and 3.2.2 for DB changes
FINDING: New ORM query in checkout doesn't use prepared statements
```

### 5. Elimination Method

```
Hypothesis Testing Matrix:

Hypothesis                    │ Test                     │ Result
──────────────────────────────┼──────────────────────────┼──────────
H1: Network latency           │ Ping/traceroute          │ ❌ Normal
H2: DB slow queries           │ Enable slow_query_log    │ ✅ FOUND!
H3: App code regression       │ Profile with APM         │ ✅ Related
H4: Memory pressure (GC)      │ GC logs analysis         │ ❌ Normal
H5: Thread pool exhaustion    │ Thread dump              │ ❌ Available
H6: External service latency  │ Mock external, re-test   │ ❌ Not factor
H7: Data volume increased     │ Check table sizes        │ ❌ Same

CONFIRMED: H2 (slow queries) caused by H3 (code regression)
Specifically: New code path doesn't use existing index
```

---

## Troubleshooting por Síntoma

### Síntoma: Response Time Incrementa con Usuarios

```
DECISION TREE:
                    Response time increases with load
                              │
              ┌───────────────┼───────────────┐
              │               │               │
         CPU > 80%?      DB Wait?       Thread Pool Full?
              │               │               │
         ┌────┤          ┌────┤          ┌────┤
         │    │          │    │          │    │
        YES  NO         YES  NO         YES  NO
         │    │          │    │          │    │
    App code  │     Slow   │       Pool   │
    ineffi-   │     queries │       too    │
    ciency    │     or locks│       small  │
              │             │              │
         Network?     External      Memory/GC?
              │        service?          │
         Check     latency?        Check heap
         bandwidth                  and GC logs
```

### Síntoma: Error Rate Increases Under Load

```
Error Type Analysis:

HTTP 503 (Service Unavailable)
├─ Queue full → Increase queue size or add capacity
├─ Circuit breaker open → Investigate downstream failure
└─ Graceful shedding → Expected behavior at overload

HTTP 500 (Internal Server Error)
├─ NullPointerException → Race condition under concurrency
├─ OutOfMemoryError → Heap too small or memory leak
├─ StackOverflowError → Infinite recursion triggered by timing
└─ Timeout (downstream) → Cascading failure

HTTP 429 (Too Many Requests)
├─ Rate limiter working correctly → Adjust test expectations
└─ Rate limit too aggressive → Discuss with team

Connection Errors
├─ Connection refused → Max connections reached
├─ Connection timeout → Server overwhelmed
└─ Connection reset → Server crashed/restarted
```

### Síntoma: Memory Grows Continuously

```
MEMORY LEAK INVESTIGATION:

Step 1: Confirm the leak
- Monitor heap usage over 2+ hours under constant load
- If old-gen baseline grows after each GC cycle → LEAK CONFIRMED

Step 2: Identify retention
- Take heap dumps at T+1h, T+2h, T+4h
- Compare: What objects increased?
- Tools: Eclipse MAT, VisualVM, JProfiler

Step 3: Common leak sources
┌─────────────────────────────────────────────────────────────┐
│ Source              │ Pattern           │ Fix                 │
├─────────────────────┼───────────────────┼─────────────────────┤
│ Static collections  │ Map/List grows    │ Use weak refs/TTL   │
│ Event listeners     │ Not unregistered  │ Cleanup on close    │
│ DB connections      │ Not returned      │ try-finally/pool    │
│ Thread locals       │ Not cleaned       │ Remove after use    │
│ Caches unbounded    │ No eviction       │ Add max size/TTL    │
│ Classloader leak    │ Hot deploy issue  │ Fix classloading    │
│ Closeable not closed│ Streams/readers   │ try-with-resources  │
└─────────────────────┴───────────────────┴─────────────────────┘

Step 4: Validate fix
- Deploy fix
- Run endurance test (8+ hours)
- Verify: Heap baseline stable after GC cycles
```

---

## Herramientas de Profiling

### JVM Profiling

```bash
# Thread dump (immediate snapshot)
jstack <PID> > thread_dump_$(date +%s).txt

# Multiple thread dumps (to detect deadlocks/contention)
for i in 1 2 3 4 5; do
  jstack <PID> > thread_dump_${i}.txt
  sleep 5
done

# Heap dump
jmap -dump:live,format=b,file=heap_$(date +%s).hprof <PID>

# GC logging (JVM flags)
-Xlog:gc*:file=gc.log:time,uptime,level,tags:filecount=5,filesize=10m

# Flight Recorder (continuous profiling)
-XX:StartFlightRecording=duration=60s,filename=recording.jfr

# Async Profiler (low overhead CPU profiling)
./profiler.sh -d 30 -f flamegraph.html <PID>
```

### Database Query Analysis

```sql
-- PostgreSQL: Find slow queries
SELECT query, calls, total_time/calls as avg_time, rows
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 20;

-- PostgreSQL: Explain analyze
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT o.*, u.name 
FROM orders o 
JOIN users u ON o.user_id = u.id 
WHERE o.status = 'pending' 
  AND o.created_at > now() - interval '7 days';

-- Result interpretation:
-- Seq Scan → Needs index
-- Nested Loop with many rows → Consider hash/merge join
-- Sort with high cost → Consider index for ORDER BY
-- Buffers shared read (high) → Data not in cache, needs more RAM
```

---

## Patrones de Bottleneck y Soluciones

### Quick Reference

```
┌──────────────────────────────────────────────────────────────────┐
│  BOTTLENECK PATTERN → SOLUTION MAPPING                           │
├──────────────────────┬───────────────────────────────────────────┤
│ CPU bound            │ Code optimization, horizontal scaling     │
│ Memory bound         │ Fix leaks, tune GC, increase heap        │
│ I/O bound (disk)     │ SSD, reduce writes, async I/O            │
│ I/O bound (network)  │ Connection pooling, compression, CDN     │
│ Lock contention      │ Reduce lock scope, optimistic locking    │
│ Pool exhaustion      │ Increase pool size, reduce hold time     │
│ Garbage collection   │ Tune GC, reduce allocation rate          │
│ Serialization        │ Async processing, event-driven arch      │
│ Data volume          │ Indexing, partitioning, archiving        │
│ External dependency  │ Circuit breaker, timeout, cache, async   │
└──────────────────────┴───────────────────────────────────────────┘
```

---

*Documento de referencia - Performance Test Life Cycle*
*Última actualización: Junio 2026*
