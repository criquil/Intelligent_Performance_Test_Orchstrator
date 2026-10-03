# 🛡️ Resiliency Testing — Parte 3 de 3: Experimentos, Game Days, métricas y código

> Diseño y priorización de experimentos, Game Days, métricas y SLOs de resiliencia, scripts k6 y bash de fault injection, antipatrones y checklist.
>
> **Guía en 3 partes:** · 1 · [`Fundamentos, steady-state hypothesis y patrones de resiliencia`](01_Fundamentos_y_Patrones_de_Resiliencia.md) · 2 · [`Fault injection, herramientas y cloud-native`](02_Fault_Injection_Herramientas_y_Cloud.md) · **3 · Experimentos, Game Days, métricas y código** (este documento)
## Índice

9. [Diseño de Experimentos de Caos](#9-diseño-de-experimentos-de-caos)
10. [Game Days](#10-game-days)
11. [Métricas de Resiliencia](#11-métricas-de-resiliencia)
13. [Ejemplos Prácticos con Código](#13-ejemplos-prácticos-con-código)
15. [Antipatrones y Errores Comunes](#15-antipatrones-y-errores-comunes)
16. [Checklist de Implementación](#16-checklist-de-implementación)

> Índice completo de las 3 partes (secciones 1-16): [`01_Fundamentos_y_Patrones_de_Resiliencia.md`](01_Fundamentos_y_Patrones_de_Resiliencia.md#índice) · [Referencias](01_Fundamentos_y_Patrones_de_Resiliencia.md#referencias)

---

## 9. Diseño de Experimentos de Caos

### Template de Experimento

```markdown
## Experimento: [NOMBRE]

### Metadata
- **ID:** CHAOS-001
- **Fecha:** 2024-XX-XX
- **Equipo:** Platform Engineering
- **Aprobado por:** [nombre]
- **Blast Radius:** [Bajo/Medio/Alto]

### Contexto
- **Sistema objetivo:** [nombre del sistema]
- **Componente afectado:** [nombre del componente]
- **Entorno:** [staging/production]
- **Ventana:** [horario de menor tráfico]

### Steady-State Hypothesis
"Creemos que [el sistema] puede tolerar [falla X] 
manteniendo [métrica Y] dentro de [umbral Z] 
y recuperándose en menos de [tiempo W]."

### Métricas a Monitorear
| Métrica | Normal | Degradado Aceptable | Crítico (abort) |
|---------|--------|--------------------:|----------------:|
| Success Rate | > 99.5% | > 95% | < 90% |
| P95 Latency | < 500ms | < 2000ms | > 5000ms |
| Error Rate | < 0.5% | < 5% | > 10% |

### Método (Pasos)
1. Confirmar steady-state (10 min observación)
2. Activar fault injection: [descripción exacta]
3. Observar durante: [X minutos]
4. Remover fault injection
5. Observar recuperación durante: [Y minutos]

### Abort Conditions (Parar inmediatamente si...)
- [ ] Error rate > 10% por más de 2 minutos
- [ ] P99 > 10 segundos
- [ ] Alertas de negocio activas
- [ ] Impacto a usuarios externos detectado
- [ ] Revenue impact > $X

### Rollback Plan
1. [Paso para revertir la fault injection]
2. [Paso para forzar recovery]
3. [Contacto de escalación]

### Resultados
- **Hipótesis:** [CONFIRMADA / REFUTADA]
- **Hallazgos:**
  - ...
- **Acciones:**
  - ...
```

### Matriz de Priorización de Experimentos

```
                     IMPACTO AL NEGOCIO
                  Bajo          Alto
              ┌──────────┬──────────────┐
        Alta  │ QUICK    │ PRIORITARIO  │
PROBABILIDAD  │ WINS     │ (hacer       │
  DE FALLA    │          │  primero)    │
              ├──────────┼──────────────┤
        Baja  │ BACKLOG  │ PLANIFICAR   │
              │ (hacer   │ (hacer       │
              │  último) │  segundo)    │
              └──────────┴──────────────┘
```

### Progresión de complejidad

```
Semana 1-2: FALLAS SIMPLES
  └─ Un componente a la vez
  └─ Entorno de staging
  └─ Duración corta (< 5 min)

Semana 3-4: FALLAS COMPUESTAS
  └─ Dos componentes simultáneos
  └─ Staging con carga realista
  └─ Duración media (5-15 min)

Mes 2: ESCENARIOS REALISTAS
  └─ Basados en post-mortems reales
  └─ Pre-producción / Canary
  └─ Duración extendida (15-60 min)

Mes 3+: PRODUCCIÓN
  └─ Game days programados
  └─ Fallas multi-servicio
  └─ Duración real (30+ min)
  └─ Con equipo de respuesta activo
```

---

## 10. Game Days

### ¿Qué es un Game Day?

Un **Game Day** es un ejercicio planificado donde un equipo inyecta fallas deliberadamente en producción (o staging) para validar la resiliencia del sistema Y la capacidad de respuesta del equipo humano.

### Estructura de un Game Day

```
┌─────────────────────────────────────────────────────────────────┐
│                        GAME DAY TIMELINE                         │
├─────────┬───────────────────────────────────────────────────────┤
│ -1 week │ Planificación, comunicación, preparación              │
│ -1 day  │ Verificar runbooks, alertas, dashboards              │
│         │                                                       │
│ T+0:00  │ Kickoff: briefing al equipo                          │
│ T+0:15  │ Validar steady-state                                 │
│ T+0:30  │ INYECTAR FALLA #1                                    │
│ T+0:45  │ Observar / Equipo responde                           │
│ T+1:00  │ INYECTAR FALLA #2 (escalar)                          │
│ T+1:15  │ Observar cascada / respuesta                         │
│ T+1:30  │ REMOVER FALLAS                                       │
│ T+1:45  │ Validar recuperación completa                        │
│ T+2:00  │ Debrief inmediato (hot wash)                         │
│         │                                                       │
│ +1 day  │ Retrospectiva detallada                              │
│ +1 week │ Action items implementados                           │
└─────────┴───────────────────────────────────────────────────────┘
```

### Roles en un Game Day

| Rol | Responsabilidad |
|-----|----------------|
| **Game Master** | Diseña escenarios, inyecta fallas, controla el ejercicio |
| **Observadores** | Monitoreán métricas, documentan comportamiento del sistema |
| **Respondedores** | Equipo que responde como si fuera un incidente real |
| **Safety Officer** | Autoridad para ABORT si se excede el blast radius |
| **Narrator** | Documenta timeline de eventos en tiempo real |

### Métricas del Game Day (no solo del sistema)

**Métricas del equipo humano:**
- **MTTD (Mean Time to Detect):** ¿Cuánto tardó el equipo en notar el problema?
- **MTTI (Mean Time to Identify):** ¿Cuánto en identificar la causa?
- **MTTR (Mean Time to Resolve):** ¿Cuánto en resolver?
- **Communication Effectiveness:** ¿Se notificó a stakeholders a tiempo?
- **Runbook Accuracy:** ¿Los runbooks sirvieron o estaban desactualizados?

---

## 11. Métricas de Resiliencia

### Métricas Cuantitativas

| Métrica | Fórmula | Objetivo típico |
|---------|---------|-----------------|
| **Availability** | uptime / (uptime + downtime) × 100 | 99.95% |
| **MTBF** | Total uptime / Número de fallas | > 720h (30 días) |
| **MTTR** | Total downtime / Número de fallas | < 5 min |
| **MTTD** | Σ(tiempo de detección) / N | < 1 min |
| **Recovery Time** | Tiempo falla → steady state | < 2 min |
| **Degradation Depth** | % de pérdida funcional durante falla | < 20% |
| **Blast Radius** | % de usuarios afectados | < 5% |
| **Error Budget Consumed** | downtime / allowable_downtime × 100 | < 80%/quarter |

### Score de Resiliencia

```
Resilience Score = Σ (peso_i × score_i) / Σ peso_i

Donde cada dimensión tiene score 0-100:

┌─────────────────────────────────────────────────────────────┐
│ Dimensión            │ Peso │ Cómo se mide                  │
├──────────────────────┼──────┼───────────────────────────────┤
│ Redundancia          │  20% │ # replicas, multi-AZ, multi-R │
│ Detección            │  15% │ MTTD, cobertura de alertas    │
│ Recuperación         │  20% │ MTTR, auto-healing rate       │
│ Degradación graceful │  15% │ % funcionalidad mantenida     │
│ Aislamiento          │  15% │ Blast radius promedio         │
│ Automatización       │  15% │ % respuestas automatizadas    │
└──────────────────────┴──────┴───────────────────────────────┘

Ejemplo:
  Redundancia:   80/100 (multi-AZ, no multi-region)
  Detección:     90/100 (alertas < 30s)
  Recuperación:  70/100 (MTTR 3 min, algo manual)
  Degradación:   60/100 (algunos servicios no tienen fallback)
  Aislamiento:   85/100 (bulkheads en 85% de servicios)
  Automatización: 75/100 (auto-scaling pero rollback manual)

Score = (20×80 + 15×90 + 20×70 + 15×60 + 15×85 + 15×75) / 100
      = (1600 + 1350 + 1400 + 900 + 1275 + 1125) / 100
      = 76.5 / 100
```

### SLIs y SLOs para Resiliencia

```yaml
# Ejemplo de SLO document
slos:
  - name: "Payment Service Availability"
    sli: "proportion of successful payment requests"
    target: 99.95%
    window: "30 days rolling"
    error_budget: "21.6 minutes / month"
    
  - name: "Recovery from single-AZ failure"
    sli: "time from AZ loss detection to full traffic redistribution"
    target: "< 60 seconds in 99% of cases"
    
  - name: "Graceful degradation under cache failure"
    sli: "proportion of requests served (potentially from fallback) during Redis outage"
    target: "100% of requests get a response (even if degraded)"
    
  - name: "Blast radius containment"
    sli: "proportion of unrelated services unaffected by a single-service failure"
    target: "> 99%"
```

---

## 13. Ejemplos Prácticos con Código

### 13.1 Test de Resiliencia con k6 + Fault Injection

```javascript
// resilience-test.js - k6 test que valida resiliencia durante fault injection
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

// Métricas custom de resiliencia
const resilienceSuccessRate = new Rate('resilience_success_rate');
const degradedResponses = new Counter('degraded_responses');
const recoveryTime = new Trend('recovery_time_ms');

export const options = {
  scenarios: {
    // Carga constante durante todo el experimento
    constant_load: {
      executor: 'constant-arrival-rate',
      rate: 100,
      timeUnit: '1s',
      duration: '15m',  // 3 min baseline + 7 min chaos + 5 min recovery
      preAllocatedVUs: 50,
      maxVUs: 200,
    },
  },
  thresholds: {
    // Métricas de resiliencia
    'resilience_success_rate': ['rate>0.95'],          // 95% durante caos
    'http_req_duration{phase:chaos}': ['p(95)<3000'],  // 3s P95 durante caos
    'http_req_duration{phase:recovery}': ['p(95)<500'],// 500ms P95 en recovery
  },
};

// Fases del experimento
const PHASES = {
  BASELINE: { start: 0, end: 180 },      // 0-3 min
  CHAOS: { start: 180, end: 600 },        // 3-10 min
  RECOVERY: { start: 600, end: 900 },     // 10-15 min
};

function getCurrentPhase() {
  const elapsed = (__VU > 0) ? (Date.now() - __ENV.START_TIME) / 1000 : 0;
  if (elapsed < PHASES.BASELINE.end) return 'baseline';
  if (elapsed < PHASES.CHAOS.end) return 'chaos';
  return 'recovery';
}

export default function () {
  const phase = getCurrentPhase();
  
  const res = http.get('http://api.example.com/payments', {
    tags: { phase: phase },
    timeout: '10s',
  });
  
  // Evaluar resiliencia según la fase
  const isSuccess = res.status === 200 || res.status === 206; // 206 = degraded OK
  resilienceSuccessRate.add(isSuccess);
  
  if (res.status === 206) {
    degradedResponses.add(1);
  }
  
  // Validaciones por fase
  if (phase === 'baseline') {
    check(res, {
      'baseline: status 200': (r) => r.status === 200,
      'baseline: latency < 500ms': (r) => r.timings.duration < 500,
    });
  } else if (phase === 'chaos') {
    check(res, {
      'chaos: response received': (r) => r.status !== 0,
      'chaos: not server error 5xx': (r) => r.status < 500 || r.status === 503,
      'chaos: latency < 5000ms': (r) => r.timings.duration < 5000,
    });
  } else { // recovery
    check(res, {
      'recovery: status 200': (r) => r.status === 200,
      'recovery: latency < 500ms': (r) => r.timings.duration < 500,
    });
  }
  
  sleep(0.1);
}

// Setup: trigger fault injection at the right time
export function setup() {
  return { startTime: Date.now() };
}
```

### 13.2 Validación de Circuit Breaker

```javascript
// circuit-breaker-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Counter, Rate } from 'k6/metrics';

const circuitBreakerTrips = new Counter('circuit_breaker_trips');
const fastFailRate = new Rate('fast_fail_rate');

export const options = {
  scenarios: {
    trip_circuit_breaker: {
      executor: 'ramping-arrival-rate',
      startRate: 10,
      timeUnit: '1s',
      stages: [
        { duration: '30s', target: 10 },   // Baseline
        { duration: '30s', target: 200 },   // Overload (trip CB)
        { duration: '60s', target: 200 },   // Sustained overload
        { duration: '30s', target: 10 },    // Recovery
        { duration: '30s', target: 10 },    // Verify recovery
      ],
      preAllocatedVUs: 100,
      maxVUs: 500,
    },
  },
};

export default function () {
  const res = http.get('http://api.example.com/downstream-call');
  
  // Detectar circuit breaker abierto
  if (res.status === 503 && res.headers['X-Circuit-Breaker'] === 'OPEN') {
    circuitBreakerTrips.add(1);
    
    // Verificar fast-fail (< 50ms = no esperó al downstream)
    const isFastFail = res.timings.duration < 50;
    fastFailRate.add(isFastFail);
    
    check(res, {
      'CB open: fast fail < 50ms': (r) => r.timings.duration < 50,
      'CB open: fallback body present': (r) => r.body.includes('fallback'),
      'CB open: retry-after header': (r) => r.headers['Retry-After'] !== undefined,
    });
  } else if (res.status === 200) {
    check(res, {
      'CB closed: normal response': (r) => r.status === 200,
      'CB closed: normal latency': (r) => r.timings.duration < 1000,
    });
  }
  
  sleep(0.05);
}
```

### 13.3 Script de Fault Injection Orquestado

```bash
#!/bin/bash
# orchestrate-chaos.sh - Orquestador de experimentos de resiliencia

set -euo pipefail

EXPERIMENT_NAME="${1:-pod-kill}"
NAMESPACE="${2:-staging}"
DURATION="${3:-300}"  # 5 min default
STEADY_STATE_WAIT=120
RECOVERY_WAIT=180

echo "═══════════════════════════════════════════════════"
echo "  CHAOS EXPERIMENT: ${EXPERIMENT_NAME}"
echo "  Namespace: ${NAMESPACE}"
echo "  Duration: ${DURATION}s"
echo "═══════════════════════════════════════════════════"

# 1. Verificar steady state
echo "[$(date +%T)] Phase 1: Verifying steady state..."
if ! ./scripts/verify-steady-state.sh "${NAMESPACE}"; then
  echo "❌ System not in steady state. Aborting."
  exit 1
fi
echo "✅ Steady state confirmed."
sleep ${STEADY_STATE_WAIT}

# 2. Snapshot de métricas pre-chaos
echo "[$(date +%T)] Phase 2: Capturing pre-chaos metrics..."
PRE_METRICS=$(curl -s "http://prometheus:9090/api/v1/query?query=\
  {__name__=~'http_requests_total|http_errors_total|http_duration_seconds'}")
echo "${PRE_METRICS}" > /tmp/pre-chaos-metrics.json

# 3. Inyectar falla
echo "[$(date +%T)] Phase 3: Injecting chaos - ${EXPERIMENT_NAME}..."
kubectl apply -f "chaos-experiments/${EXPERIMENT_NAME}.yaml" -n "${NAMESPACE}"

# 4. Monitorear durante el caos
echo "[$(date +%T)] Phase 4: Monitoring during chaos (${DURATION}s)..."
END_TIME=$(($(date +%s) + DURATION))
ABORT=false

while [ $(date +%s) -lt ${END_TIME} ] && [ "${ABORT}" = "false" ]; do
  # Verificar abort conditions
  ERROR_RATE=$(curl -s "http://prometheus:9090/api/v1/query?query=\
    sum(rate(http_errors_total[1m]))/sum(rate(http_requests_total[1m]))" \
    | jq -r '.data.result[0].value[1]')
  
  if (( $(echo "${ERROR_RATE} > 0.10" | bc -l) )); then
    echo "⚠️  ABORT: Error rate ${ERROR_RATE} exceeds 10% threshold!"
    ABORT=true
  fi
  
  sleep 10
done

# 5. Remover falla
echo "[$(date +%T)] Phase 5: Removing chaos..."
kubectl delete -f "chaos-experiments/${EXPERIMENT_NAME}.yaml" -n "${NAMESPACE}" --ignore-not-found

# 6. Esperar y verificar recuperación
echo "[$(date +%T)] Phase 6: Waiting for recovery (${RECOVERY_WAIT}s)..."
sleep ${RECOVERY_WAIT}

echo "[$(date +%T)] Phase 7: Verifying recovery..."
if ./scripts/verify-steady-state.sh "${NAMESPACE}"; then
  echo "✅ System recovered to steady state."
  RESULT="PASSED"
else
  echo "❌ System did NOT recover to steady state!"
  RESULT="FAILED"
fi

# 7. Generar reporte
echo "[$(date +%T)] Phase 8: Generating report..."
cat << EOF > "reports/${EXPERIMENT_NAME}-$(date +%Y%m%d-%H%M).json"
{
  "experiment": "${EXPERIMENT_NAME}",
  "namespace": "${NAMESPACE}",
  "duration_seconds": ${DURATION},
  "result": "${RESULT}",
  "aborted": ${ABORT},
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

echo "═══════════════════════════════════════════════════"
echo "  RESULT: ${RESULT}"
echo "═══════════════════════════════════════════════════"

[ "${RESULT}" = "PASSED" ] && exit 0 || exit 1
```

---

## 15. Antipatrones y Errores Comunes

### ❌ Antipatrón 1: "Big Bang Chaos"
```
MALO: Inyectar 5 fallas simultáneas en producción sin experiencia previa
BUENO: Empezar con 1 falla simple en staging, escalar gradualmente
```

### ❌ Antipatrón 2: "Chaos sin Observabilidad"
```
MALO: Inyectar fallas sin dashboards ni alertas configuradas
BUENO: Primero observabilidad completa, LUEGO chaos
```

### ❌ Antipatrón 3: "Fire and Forget"
```
MALO: Ejecutar experimento y no analizar resultados
BUENO: Cada experimento → análisis → action items → validación
```

### ❌ Antipatrón 4: "Solo infraestructura"
```
MALO: Solo matar pods/instancias
BUENO: También probar fallas de aplicación (timeouts, datos corruptos, slow responses)
```

### ❌ Antipatrón 5: "Chaos Cowboy"
```
MALO: Un ingeniero ejecuta chaos sin avisar a nadie
BUENO: Comunicación previa, safety officer, abort conditions claras
```

### ❌ Antipatrón 6: "Retry Storm"
```
MALO: Todos los clientes reintentando simultáneamente sin backoff
BUENO: Exponential backoff + jitter + circuit breaker
```

### ❌ Antipatrón 7: "Timeout Chain Violation"
```
MALO: 
  API Gateway timeout: 5s
  Service A timeout: 10s  ← MAYOR que el gateway!
  Service B timeout: 15s  ← Aún mayor!
  
BUENO:
  API Gateway timeout: 10s
  Service A timeout: 5s
  Service B timeout: 2s
```

### ❌ Antipatrón 8: "Health Check Lie"
```
MALO: /health retorna 200 aunque el servicio no puede procesar requests
BUENO: /health verifica dependencias reales (DB, cache, downstream)
```

---

## 16. Checklist de Implementación

### Pre-requisitos (antes de hacer Resiliency Testing)

- [ ] **Observabilidad completa:** Logs, métricas, traces configurados
- [ ] **Alertas calibradas:** Alertas que detectan degradación (no solo caídas)
- [ ] **Runbooks actualizados:** Procedimientos documentados para cada escenario
- [ ] **Baseline establecido:** Métricas de estado estable documentadas
- [ ] **Equipo capacitado:** El equipo entiende chaos engineering
- [ ] **Stakeholders informados:** Management aprueba el enfoque

### Implementación Progresiva

```
□ MES 1: Foundations
  □ Definir steady-state hypothesis para servicios críticos
  □ Configurar Toxiproxy para tests de integración
  □ Agregar circuit breakers a todas las dependencias externas
  □ Implementar health checks profundos (liveness + readiness)
  □ Primer experimento manual en staging

□ MES 2: Automation
  □ Crear suite de chaos experiments automatizados
  □ Integrar resiliency tests en pipeline CI/CD (staging)
  □ Configurar LitmusChaos / Chaos Mesh en cluster staging
  □ Primer Game Day con equipo reducido
  □ Documentar resultados y crear action items

□ MES 3: Expansion
  □ Expandir a todos los servicios críticos
  □ Primer experimento en pre-producción
  □ Introducir fallas de dependencia (no solo infra)
  □ Automatizar reportes de resiliencia score
  □ Game Day con equipo completo

□ MES 4+: Production
  □ Chaos experiments regulares en producción (ventanas seguras)
  □ Continuous chaos (Chaos Monkey-style)
  □ Multi-failure scenarios
  □ Cross-team Game Days
  □ Resiliencia como parte del Definition of Done
```

### KPIs de Éxito del Programa

| KPI | Target | Cómo medir |
|-----|--------|------------|
| Experimentos ejecutados/mes | > 10 | Automation platform |
| % servicios con chaos coverage | > 80% | Inventario vs. experiments |
| MTTR improvement | -50% YoY | Incident metrics |
| Incidentes prevenidos | > 3/quarter | Post-mortem attribution |
| Game Days ejecutados | 1/month | Calendar |
| Resilience Score promedio | > 80/100 | Score card |
