# Smoke, Peak, Capacity y Breakpoint Testing

## 1. Smoke Testing (Performance)

### Definición
El **Smoke Test** de performance es una prueba rápida y ligera que valida que los scripts de prueba funcionan correctamente y que el sistema es capaz de responder bajo carga mínima. Es el "sanity check" antes de invertir tiempo en tests de carga completos.

### Analogía
> Como "encender el auto y verificar que arranca" antes de hacer un viaje largo.

### Propósito
1. **Validar scripts**: Assertions pasan, correlaciones funcionan, data fluye
2. **Validar entorno**: Sistema accesible, servicios corriendo, DB respondiendo
3. **Validar monitoreo**: Métricas se capturan correctamente
4. **Gate check**: Si el smoke falla, NO ejecutar load test (ahorra tiempo)

### Diseño

```yaml
smoke_test:
  vusers: 1-3
  duration: "2-5 minutos"
  scenarios: "Todos (1 iteración mínima de cada uno)"
  
  success_criteria:
    - "0% error rate"
    - "All assertions pass"
    - "All transactions complete"
    - "Monitoring captures data"
    - "Response times within 10x of expected baseline"
    
  failure_actions:
    - "DO NOT proceed to load testing"
    - "Debug and fix script/environment issues"
    - "Re-run smoke until clean"
    
  execution:
    frequency: "Before EVERY load test execution"
    duration_total: "< 10 minutes including setup"
```

### Ejemplo (k6)

```javascript
// smoke-test.js
import { options as loadOptions } from './load-test.js';

export const options = {
  vus: 1,
  duration: '3m',
  thresholds: {
    http_req_failed: ['rate==0'],          // ZERO errors
    http_req_duration: ['p(99)<10000'],     // Very generous threshold
    checks: ['rate==1'],                    // ALL checks must pass
  },
};

// Uses same scenarios as load test, just with 1 VU
export { default } from './load-test.js';
```

### ¿Cuándo falla un Smoke Test?
| Causa | Síntoma | Acción |
|-------|---------|--------|
| App no desplegada | Connection refused | Deploy/restart |
| DB sin datos | Empty responses | Load test data |
| Script mal correlacionado | 4xx errors | Fix extraction |
| Token expirado en data | 401 Unauthorized | Refresh credentials |
| Endpoint cambiado | 404 Not Found | Update script URLs |
| Certificado SSL expirado | TLS error | Renovar cert |
| Firewall bloqueando | Timeout | Abrir puertos |

---

## 2. Peak Testing

### Definición
El **Peak Testing** simula el **pico máximo esperado de tráfico real** que el sistema debe manejar, basado en datos históricos o proyecciones de negocio.

### Diferencia con Load Testing y Stress Testing

```
                Load Test        Peak Test         Stress Test
                ─────────        ─────────         ───────────
Carga:          Promedio/Normal  Máximo esperado   Más allá del máximo
Objetivo:       Validar SLAs    Validar para pico  Encontrar límites
Resultado:      Cumple/No       Sobrevive pico     Punto de quiebre
Frecuencia:     Cada sprint     Pre-eventos        Menos frecuente
Ejemplo:        800 users       2500 users         5000+ users
                (normal day)    (Black Friday)     (beyond capacity)
```

### ¿Cuándo usar Peak Testing?

| Escenario de negocio | Peak esperado | Cuándo testear |
|---------------------|---------------|----------------|
| Black Friday / Cyber Monday | 5-10x tráfico normal | 1-2 meses antes |
| Lanzamiento de producto | 3-5x primer día | Pre-launch |
| Campaña de marketing masiva | 2-4x durante campaña | 1 semana antes |
| Venta de entradas (evento) | 50-100x en primeros minutos | 2 semanas antes |
| Final de mes (facturación) | 2-3x para batch + online | Monthly |
| Inicio de clases (educación) | 5x primera semana | Agosto |
| Tax deadline (gobierno) | 10x última semana | Pre-deadline |

### Diseño del Peak Test

```yaml
peak_test:
  context: "Black Friday 2026"
  
  data_sources:
    - "Black Friday 2025 production logs"
    - "Marketing team: 40% more email recipients this year"
    - "Growth rate: 25% YoY"
    
  calculated_peak:
    last_year_peak: 1800 concurrent users
    growth_factor: 1.25
    campaign_factor: 1.40
    safety_margin: 1.20
    target: "1800 × 1.25 × 1.40 × 1.20 = 3,780 concurrent users"
    rounded_target: 4000 concurrent users
    
  load_profile:
    # Simula el patrón real de Black Friday
    phases:
      - { name: "pre-event", duration: "30m", users: 500 }     # Madrugada
      - { name: "ramp-to-peak", duration: "15m", users: 4000 } # Apertura 6AM
      - { name: "peak-sustained", duration: "4h", users: 4000 } # Peak sostenido
      - { name: "gradual-decline", duration: "2h", users: 2000 } # Tarde
      - { name: "second-peak", duration: "30m", users: 3500 }  # Evening surge
      - { name: "wind-down", duration: "1h", users: 500 }      # Noche
      
  acceptance_criteria:
    - "All SLAs met during peak (4000 users)"
    - "No auto-scaling failures"
    - "Zero data loss"
    - "Error rate < 1% during peak"
    - "Response time P95 < 5s during peak"
    - "Recovery to normal within 15 minutes post-peak"
```

---

## 3. Capacity Testing

### Definición
El **Capacity Testing** determina **cuántos usuarios, transacciones o datos** puede manejar el sistema antes de que se incumplan los SLAs. Responde: "¿Cuál es nuestra capacidad máxima real?"

### Diferencia con Stress Testing

```
Capacity Testing:                  Stress Testing:
─────────────────                  ────────────────
"¿Cuántos users soportamos        "¿Qué pasa cuando lo rompemos?"
 manteniendo los SLAs?"            
                                   
Incrementa hasta SLA breach        Incrementa hasta crash
Se detiene en el límite SLA        Continúa más allá
Resultado: número de capacidad     Resultado: modo de fallo
                                   
Output: "Soportamos 1,800 users"   Output: "Crashea a 3,100 users"
```

### Proceso de Capacity Testing

```
MÉTODO: Incremental hasta SLA breach

Step 1: Start at 50% of expected capacity
Step 2: Increment by 10% every 10-15 minutes
Step 3: At each level, verify ALL SLAs
Step 4: When FIRST SLA is breached → that's your capacity

Users:  500  600  700  800  900  1000 1100 1200 1300 1400
        ─────────────────────────────────────────────────
P95:    1.0s 1.1s 1.2s 1.4s 1.6s 1.9s 2.2s 2.6s 3.1s 3.8s
SLA:    ──────────────────────────────── < 3.0s ──────────
Status: ✅   ✅   ✅   ✅   ✅   ✅   ✅   ✅   ❌   ❌
                                                  ↑
                                         CAPACITY = 1,200 users
                                         (last level where ALL SLAs met)
```

### Capacity Planning Formula

```
CAPACITY PLANNING:
═════════════════

Current capacity: 1,200 users
Current peak usage: 800 users
Headroom: (1200 - 800) / 1200 = 33%

Growth rate: 10% monthly
Time to capacity: 
  Month 1: 880 users (27% headroom)
  Month 2: 968 users (19% headroom)
  Month 3: 1065 users (11% headroom)  ← WARNING: <15%
  Month 4: 1171 users (2% headroom)   ← CRITICAL: need scaling!

RECOMMENDATION:
"Current infrastructure supports 1,200 concurrent users.
 At 10% monthly growth, scaling needed within 3 months.
 Recommend capacity upgrade by Month 2 to maintain 20% headroom."
```

### Output del Capacity Test

```
CAPACITY TEST RESULTS
═════════════════════

System: E-Commerce Platform v3.2
Date: 2026-06-10
Environment: 4x m5.2xlarge + 1x r5.4xlarge DB

CAPACITY THRESHOLDS:
┌──────────────────────────────────────────────────────────┐
│ SLA Constraint           │ Breached At  │ Bottleneck     │
├──────────────────────────┼──────────────┼────────────────┤
│ Response Time P95 < 3s   │ 1,300 users  │ DB Connection  │
│ Error Rate < 1%          │ 1,500 users  │ Thread Pool    │
│ CPU < 80%                │ 1,100 users  │ App Server CPU │
│ Throughput ≥ 500 TPS     │ 1,400 users  │ DB Locks       │
└──────────────────────────┴──────────────┴────────────────┘

EFFECTIVE CAPACITY: 1,100 users
(Determined by FIRST constraint breached: CPU)

HEADROOM ANALYSIS:
- Current peak: 700 users → 36% headroom ✅
- Projected peak (6 months): 1,050 users → 5% headroom ⚠️

SCALING RECOMMENDATIONS:
1. Short-term: Optimize CPU-heavy code paths
2. Medium-term: Add 2 more app servers (→ capacity ~1,800)
3. Long-term: Database read replicas (→ capacity ~2,500)
```

---

## 4. Breakpoint Testing

### Definición
El **Breakpoint Testing** es una variante del stress testing cuyo objetivo específico es encontrar el **punto exacto** donde el sistema deja de funcionar aceptablemente. A diferencia del capacity testing (que busca el límite SLA), el breakpoint testing busca el límite ABSOLUTO.

### Escala de límites

```
     Baseline    Load      Capacity   Breakpoint    Crash
        │          │          │          │            │
        ▼          ▼          ▼          ▼            ▼
────────○──────────○──────────○──────────○────────────○────
       5 VU      1000 VU   1200 VU   2500 VU     3100 VU
        │          │          │          │            │
     Perfect    SLAs Met   SLA Limit  Degraded    System
                                      but works    Dead
```

### Tipos de Breakpoints

| Tipo | Definición | Indicador |
|------|-----------|-----------|
| **SLA Breakpoint** | Primer SLA incumplido | = Capacity limit |
| **Functional Breakpoint** | Primera funcionalidad que falla | Errores funcionales |
| **Resource Breakpoint** | Primer recurso que satura (100%) | CPU/Memory/Pool exhaustion |
| **Recovery Breakpoint** | Punto desde el cual no hay auto-recovery | Requires restart |
| **Data Integrity Breakpoint** | Punto donde se corrompen/pierden datos | Missing transactions |

### Proceso

```yaml
breakpoint_test:
  method: "Binary search for exact breakpoint"
  
  steps:
    1: "Start at known-good load (capacity limit)"
    2: "Double the load"
    3: "If system survives → increase more"
    4: "If system fails → reduce halfway"
    5: "Repeat binary search until ±5% precision"
    
  example:
    - { users: 1200, status: "OK (known capacity)" }
    - { users: 2400, status: "FAILED" }
    - { users: 1800, status: "OK but degraded" }
    - { users: 2100, status: "FAILED" }
    - { users: 1950, status: "OK barely" }
    - { users: 2025, status: "FAILED" }
    # Breakpoint: ~2,000 users (±50)
    
  documentation:
    - "Exact breakpoint value"
    - "Which component fails first"
    - "Mode of failure"
    - "Recovery possibility (auto vs manual)"
    - "Time to failure at breakpoint load"
```

---

## 5. Concurrency Testing

### Definición
El **Concurrency Testing** evalúa el comportamiento del sistema cuando múltiples usuarios realizan **exactamente la misma operación al mismo tiempo**, enfocándose en problemas de concurrencia como race conditions, deadlocks y data corruption.

### Diferencia con Load Testing

```
Load Testing:                    Concurrency Testing:
─────────────                    ─────────────────────
Múltiples usuarios haciendo      Múltiples usuarios haciendo
DIFERENTES cosas                 la MISMA cosa al MISMO tiempo

Simula uso normal diverso        Simula peor caso de contención
Distribuido en el tiempo         Sincronizado en el instante
Busca bottlenecks generales      Busca race conditions específicas
```

### Escenarios críticos

```yaml
concurrency_scenarios:
  
  simultaneous_purchase:
    description: "100 users intentan comprar el ÚLTIMO item en stock"
    expected_behavior:
      - "Solo 1 compra exitosa"
      - "99 reciben 'Out of stock' (NO overselling)"
      - "Zero inventario negativo"
      - "Zero transacciones duplicadas"
    implementation: "Rendezvous/barrier para sincronizar"
    
  simultaneous_registration:
    description: "50 users registran con el MISMO email"
    expected_behavior:
      - "Solo 1 registro exitoso"
      - "49 reciben error de duplicado"
      - "Zero registros duplicados en DB"
    checks: "Unique constraint holds under concurrency"
    
  simultaneous_balance_update:
    description: "10 transacciones simultáneas en la misma cuenta"
    expected_behavior:
      - "Balance final = balance_inicial + sum(todas las transacciones)"
      - "Zero lost updates"
      - "Zero double-spending"
    checks: "ACID properties maintained"
    
  simultaneous_file_write:
    description: "Multiple processes writing to shared resource"
    expected_behavior:
      - "No data corruption"
      - "All writes eventually persisted"
      - "No file locking deadlocks"
```

### Implementación: Rendezvous Point

```javascript
// k6: No tiene rendezvous nativo, pero se puede simular con timing
// Para verdadero rendezvous, usar JMeter's Synchronizing Timer

// JMeter approach:
// Synchronizing Timer: "Wait for 100 users before releasing ALL"
// → Todos los 100 users hacen el request en el mismo instante

// k6 workaround: Usar arrival-rate executor con burst
export const options = {
  scenarios: {
    burst: {
      executor: 'shared-iterations',
      vus: 100,
      iterations: 100,    // Each VU does exactly 1 iteration
      maxDuration: '10s', // All must complete quickly
    },
  },
};

// All VUs start nearly simultaneously
export default function() {
  // All 100 VUs hit this endpoint at ~the same time
  const res = http.post(`${BASE_URL}/api/purchase`, JSON.stringify({
    product_id: 'LAST-ITEM-001',  // Same item for all!
    quantity: 1,
  }));
  
  check(res, {
    'got 200 or 409': (r) => r.status === 200 || r.status === 409,
  });
}
```

---

## 6. Reliability Testing

### Definición
El **Reliability Testing** valida que el sistema mantiene un **nivel consistente de rendimiento y disponibilidad** a lo largo del tiempo y bajo diferentes condiciones. Combina aspectos de endurance, failover y recovery testing.

### Componentes

```
RELIABILITY = Availability × Consistency × Recoverability

Availability:  ¿El sistema está UP cuando se necesita?
Consistency:   ¿El rendimiento es predecible y estable?
Recoverability: ¿Se recupera correctamente después de fallos?
```

### Métricas de Reliability

| Métrica | Fórmula | Target típico |
|---------|---------|---------------|
| **Uptime %** | (Total time - Downtime) / Total time × 100 | 99.95% |
| **MTBF** | Total uptime / Number of failures | > 720 hours |
| **MTTR** | Total repair time / Number of failures | < 5 minutes |
| **Error budget** | Allowed downtime per period | ~22 min/month (99.95%) |

### Diseño del Reliability Test

```yaml
reliability_test:
  duration: "72 hours"
  load: "Normal production load (70% capacity)"
  
  validations:
    - "Zero unplanned downtime during 72 hours"
    - "Response time consistent (CV < 10%)"
    - "Error rate < 0.01% continuously"
    - "No memory growth trend"
    - "No performance degradation trend"
    - "Survives planned failover"
    - "Recovers from injected fault within 2 minutes"
    
  injected_faults:
    at_24h: "Kill 1 app instance → verify failover"
    at_36h: "Network partition for 30s → verify recovery"
    at_48h: "DB failover to replica → verify continuity"
    at_60h: "Memory pressure event → verify GC recovery"
```

---

*Documento de referencia - Performance Test Life Cycle*
*Última actualización: Junio 2026*
