# Baseline Testing - Guía Exhaustiva

## Definición

El **Baseline Testing** es el proceso de establecer una **línea base de rendimiento** del sistema bajo condiciones controladas y con carga mínima o predefinida. Esta línea base se convierte en el punto de referencia contra el cual se comparan TODOS los resultados futuros.

---

## ¿Por qué es Crítico?

Sin una baseline:
- No puedes saber si el sistema mejoró o empeoró
- No tienes contexto para interpretar resultados
- No puedes detectar regresiones
- No puedes cuantificar el impacto de optimizaciones
- No puedes responder "¿es esto normal?"

```
SIN BASELINE:                    CON BASELINE:
"El P95 es 2.3 segundos"        "El P95 es 2.3s vs 1.8s baseline"
→ ¿Es bueno? ¿Es malo?         → 28% degradación identificada
   No se sabe.                     Acción requerida.
```

---

## ¿Cuándo Ejecutar un Baseline Test?

### Momentos clave para establecer/actualizar baseline:

| Momento | Razón |
|---------|-------|
| **Antes del primer load test** | Punto de referencia inicial |
| **Después de cada release** | Detectar regresiones |
| **Después de cambios de infraestructura** | Nuevo hardware/config |
| **Después de optimizaciones** | Documentar mejora como nueva baseline |
| **Después de cambios de datos** | Volumen de DB cambiado |
| **Inicio de cada sprint/ciclo** | Referencia para el sprint |
| **Cambio de entorno de test** | Nueva calibración necesaria |

### Triggers para re-baseline:
```
¿Necesitas nueva baseline?

Cambió la versión de la app?          → SÍ
Cambió la infraestructura?            → SÍ  
Cambió el volumen de datos?           → SÍ
Cambió la configuración (pools, GC)?  → SÍ
Solo se agregó funcionalidad menor?   → PROBABLEMENTE
Solo cambió UI sin backend?           → NO (backend baseline válida)
```

---

## ¿Cómo Ejecutar un Baseline Test?

### Condiciones de ejecución

```yaml
baseline_test:
  conditions:
    load: "Minimal - 1 to 10 VUsers"
    purpose: "Measure system capability without load pressure"
    duration: "15-30 minutes (after warm-up)"
    environment: "Same as load test environment"
    data: "Same dataset as planned for load tests"
    state: "Clean start (caches cold OR warmed, document which)"
    monitoring: "All layers active"
    
  what_to_measure:
    - "Response time per transaction (all percentiles)"
    - "Throughput at minimal load"
    - "Resource utilization at idle/minimal"
    - "Database query times (without contention)"
    - "External service response times"
    - "GC behavior at low load"
    - "Connection pool behavior"
    
  what_NOT_to_do:
    - "Don't apply any load pressure"
    - "Don't run concurrent users competing for resources"
    - "Don't include ramp-up data in measurements"
    - "Don't measure during background batch jobs"
```

### Proceso paso a paso

```
PASO 1: WARM-UP (5-10 minutos)
══════════════════════════════
- Ejecutar con 1-2 VUsers
- Propósito: Llenar caches, compilar JIT, establecer connections
- Datos de warm-up se DESCARTAN

PASO 2: MEDICIÓN (15-30 minutos)
═══════════════════════════════
- Ejecutar con carga mínima controlada (1-5 VUsers)
- Cada transacción ejecutada múltiples veces
- Capturar TODOS los percentiles
- Monitorear recursos del sistema

PASO 3: VALIDACIÓN (repetir 2-3 veces)
══════════════════════════════════════
- REPETIR el paso 2 al menos 3 veces
- Comparar resultados entre ejecuciones
- Si varianza > 10%: investigar inestabilidad
- Tomar el PROMEDIO de las ejecuciones estables

PASO 4: DOCUMENTACIÓN
═════════════════════
- Registrar todos los valores como "BASELINE OFICIAL"
- Documentar condiciones exactas (fecha, versión, env, datos)
- Guardar en repositorio con control de versiones
```

---

## La Importancia de ITERAR para una Baseline Exacta

### ¿Por qué una sola ejecución NO es suficiente?

```
Ejecución 1: P95 = 1.2s
Ejecución 2: P95 = 1.8s    ← ¿Cuál es la baseline real?
Ejecución 3: P95 = 1.3s

Si tomas solo la primera: Baseline optimista (1.2s)
Si tomas solo la segunda: Baseline pesimista (1.8s)
Si tomas el promedio de 3: Baseline realista (1.43s)
Si investigas la 2da y la descartas (anomalía): Baseline = 1.25s
```

### Factores que causan variabilidad:

| Factor | Impacto | Mitigación |
|--------|---------|-----------|
| JIT Compilation | Primeras requests más lentas | Warm-up period |
| Cache cold/warm | Diferencia significativa en DB | Documentar estado |
| GC events | Picos aleatorios | Múltiples mediciones |
| Background processes | Competencia por CPU | Aislar entorno |
| Network jitter | Variación en latencia | Promediar múltiples runs |
| Disk cache | Primera lectura vs cache | Múltiples iteraciones |
| OS scheduling | Context switches | Medición prolongada |

### Protocolo de iteración para baseline exacta

```
ITERACIÓN 1: Run inicial
  → Resultado: P95 = 1.5s
  → ¿Warm-up incluido? Verificar

ITERACIÓN 2: Repetir (condiciones idénticas)
  → Resultado: P95 = 1.4s
  → Δ con iter 1: -7% → Aceptable (< 10%)

ITERACIÓN 3: Repetir una vez más
  → Resultado: P95 = 1.45s
  → Δ con promedio anterior: -0.3% → Muy estable

BASELINE FINAL: Promedio(1.5, 1.4, 1.45) = 1.45s
Confianza: ALTA (varianza < 5%)

────────────────────────────────────────────────

ESCENARIO PROBLEMÁTICO:

ITERACIÓN 1: P95 = 1.5s
ITERACIÓN 2: P95 = 2.8s   ← ANOMALÍA
ITERACIÓN 3: P95 = 1.6s
ITERACIÓN 4: P95 = 1.5s

Acción: Descartar iteración 2 (investigar causa)
  → Causa encontrada: GC full durante medición
  → Documentar: "Excluida por GC event atípico"
  
BASELINE FINAL: Promedio(1.5, 1.6, 1.5) = 1.53s
Nota: "P99 puede incluir GC spikes de hasta 2.8s"
```

### Criterios de estabilidad

```
BASELINE ESTABLE cuando:
✅ Coeficiente de variación (CV) < 10%
   CV = (StdDev / Mean) × 100

✅ Mínimo 3 ejecuciones consistentes
✅ Sin outliers no explicados
✅ Mismo patrón en todas las transacciones
✅ Recursos del sistema estables durante mediciones

BASELINE INESTABLE cuando:
❌ CV > 15% entre ejecuciones
❌ Tendencia ascendente o descendente
❌ Picos inexplicados
❌ Una transacción varía mientras otras no

Si inestable → NO usar como baseline
            → Investigar causa de inestabilidad
            → Resolver antes de continuar
```

---

## Baseline Document Template

```yaml
# PERFORMANCE BASELINE RECORD
# ============================

metadata:
  date: "2026-06-10"
  version: "3.2.1"
  environment: "perf-test-aws (4x m5.2xlarge)"
  database: "PostgreSQL 15.4, 50M orders, 5M users"
  tester: "Performance Team"
  iterations: 3
  confidence: "HIGH (CV < 5%)"

conditions:
  vusers: 5
  duration_per_run: "20 minutes (excl. 5min warm-up)"
  cache_state: "warm (after 5min warm-up)"
  background_jobs: "disabled"
  time_of_execution: "14:00-15:30 (no interference)"

results:
  transactions:
    T01_Homepage:
      p50: "180ms"
      p90: "250ms"
      p95: "310ms"
      p99: "520ms"
      avg: "195ms"
      
    T02_Search:
      p50: "320ms"
      p90: "480ms"
      p95: "560ms"
      p99: "890ms"
      avg: "350ms"
      
    T03_AddToCart:
      p50: "85ms"
      p90: "130ms"
      p95: "165ms"
      p99: "280ms"
      avg: "95ms"
      
    T05_Checkout:
      p50: "450ms"
      p90: "680ms"
      p95: "820ms"
      p99: "1.2s"
      avg: "490ms"
      
  infrastructure:
    cpu_at_baseline: "8-12%"
    memory_at_baseline: "45%"
    db_connections_at_baseline: "12/200"
    disk_io_at_baseline: "< 5%"

comparison_thresholds:
  warning: "20% degradation vs baseline"
  critical: "50% degradation vs baseline"
  
notes:
  - "Iteration 2 excluded from average (GC full event)"
  - "Search P99 includes full-text index warm-up"
  - "Baseline valid until next major data load or version change"
  
next_baseline_scheduled: "After v3.3.0 release"
```

---

## Uso de la Baseline en el PTLC

### Comparación durante Load Tests
```
LOAD TEST RESULTS vs BASELINE

Transaction    │ Baseline (P95) │ Load Test (P95) │ Ratio  │ Status
───────────────┼────────────────┼─────────────────┼────────┼────────
T01_Homepage   │     310ms      │      890ms      │  2.9x  │ ⚠️ 
T02_Search     │     560ms      │     1.4s        │  2.5x  │ ⚠️
T03_AddToCart  │     165ms      │      380ms      │  2.3x  │ ✅ Normal
T05_Checkout   │     820ms      │     3.9s        │  4.8x  │ ❌ Issue!

INTERPRETATION:
- 2-3x baseline under full load = NORMAL (expected degradation)
- 3-5x baseline = WARNING (investigate if exceeds SLA)
- >5x baseline = CRITICAL (definite bottleneck)

T05_Checkout at 4.8x indicates disproportionate degradation
→ Something specific to checkout doesn't scale well
→ Investigate DB queries in checkout path
```

### Regression Detection
```
Version 3.2.1 Baseline: Homepage P95 = 310ms
Version 3.2.2 Baseline: Homepage P95 = 480ms

REGRESSION DETECTED: +55% degradation in baseline!
(Under minimal load = code issue, not capacity issue)

Action: Investigate code changes between 3.2.1 and 3.2.2
Finding: New middleware added logging to every request
Fix: Make logging async
Post-fix baseline: Homepage P95 = 320ms (back to normal)
```

---

*Documento de referencia - Performance Test Life Cycle*
*Última actualización: Junio 2026*
