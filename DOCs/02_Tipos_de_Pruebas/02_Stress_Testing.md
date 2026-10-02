# Stress Testing - Guía Completa

## Definición

El **Stress Testing** es un tipo de prueba de rendimiento que somete al sistema a cargas que **exceden su capacidad normal de operación** para determinar su comportamiento bajo condiciones extremas, identificar su punto de quiebre y evaluar su capacidad de recuperación.

---

## Objetivos del Stress Testing

### Objetivos primarios
1. **Identificar el punto de quiebre** (breaking point) del sistema
2. **Evaluar el comportamiento ante fallos** (graceful degradation vs crash)
3. **Verificar la capacidad de recuperación** post-estrés
4. **Determinar la capacidad máxima** absoluta del sistema
5. **Validar mecanismos de protección** (circuit breakers, rate limiting, auto-scaling)

### Objetivos secundarios
- Identificar el primer componente que falla (weakest link)
- Validar alertas y monitoreo bajo estrés extremo
- Verificar que no hay corrupción de datos bajo estrés
- Evaluar la experiencia del usuario durante degradación
- Probar planes de disaster recovery

---

## Diferencia entre Load Testing y Stress Testing

| Aspecto | Load Testing | Stress Testing |
|---------|-------------|----------------|
| **Carga** | Normal/esperada | Más allá de lo esperado |
| **Objetivo** | Validar SLAs | Encontrar límites |
| **Resultado esperado** | Sistema funciona bien | Sistema eventualmente falla |
| **Duración** | Extendida (horas) | Más corta (hasta el quiebre) |
| **Pregunta que responde** | "¿Cumplimos los SLAs?" | "¿Dónde se rompe?" |
| **Carga relativa** | 100% de capacidad planificada | 150-300%+ de capacidad |

---

## Tipos de Stress Testing

### 1. Incremental Stress Test
Incrementar la carga gradualmente hasta el punto de fallo.

```
Users
5000 ┤                                        ╱ CRASH
4000 ┤                                    ╱──┘
3000 ┤                              ╱────┘
2000 ┤                        ╱────┘
1000 ┤  Normal capacity ╱────┘
     │           ╱─────┘
   0 ┤──────────┘
     └───────────────────────────────────────────→ Time
     
     Incremento: +200 users cada 5 minutos
     hasta encontrar el punto de fallo
```

### 2. Sudden Stress Test
Aplicar carga extrema de golpe (sin ramp-up).

```
Users
5000 ┤  ┌──────────────────────┐
     │  │                      │
     │  │   Extreme load       │
     │  │   (immediate)        │
     │  │                      │
   0 ┤──┘                      └──
     └───────────────────────────────→ Time
     
     Propósito: Ver si el sistema sobrevive
     un impacto súbito sin preparación
```

### 3. Sustained Stress Test
Mantener carga por encima de la capacidad durante un período.

```
Users
3000 ┤      ┌───────────────────────────┐
     │     /│   Sobre-capacidad         │\
2000 ┤    / │   sostenida               │ \
     │   /  │   (30-60 min)             │  \
1000 ┤──/   │   Normal capacity ────────│───\──
     │ /    │                           │    \
   0 ┤/     └───────────────────────────┘     \
     └────────────────────────────────────────────→ Time
     
     Propósito: ¿Se estabiliza o se degrada
     progresivamente?
```

### 4. Stress with Resource Constraints
Reducir recursos disponibles mientras se mantiene carga normal.

```
Scenarios:
- Kill 1 of 4 application servers → ¿Cómo rebalancea?
- Reduce memory by 50% → ¿GC storms?
- Limit network bandwidth → ¿Timeouts?
- Simulate disk full → ¿Graceful handling?
```

---

## Diseño de un Stress Test

### Template de diseño

```yaml
stress_test_design:
  objective: "Determinar punto de quiebre y comportamiento de fallo"
  
  approach: "incremental"
  
  baseline:
    users: 1000  # Capacidad normal verificada
    
  stress_profile:
    start_users: 1000
    increment: 200
    increment_interval: "5 minutes"
    max_users: 5000  # Límite de safety
    
  monitoring_focus:
    - "Response time P95 vs threshold"
    - "Error rate trend"
    - "CPU/Memory saturation"
    - "Connection pool exhaustion"
    - "Queue depth growth"
    
  abort_criteria:
    - "Error rate > 50% during 3 minutes"
    - "Complete system unresponsive for 2 minutes"
    - "Data corruption detected"
    - "Infrastructure failure (disk full, OOM kill)"
    
  recovery_validation:
    - "After stress removed, system returns to baseline within 10 min"
    - "No data loss or corruption"
    - "All services responsive"
    - "No zombie processes or stuck threads"
    
  expected_findings:
    - "Breaking point (max users before SLA breach)"
    - "First component to fail"
    - "Failure mode (graceful vs catastrophic)"
    - "Recovery time"
    - "Data integrity post-stress"
```

---

## Métricas Específicas del Stress Testing

### Métricas de breaking point

| Métrica | Descripción | Cómo identificar |
|---------|-------------|------------------|
| **Breaking Point** | Carga donde SLAs se incumplen | Response time > SLA threshold |
| **Saturation Point** | Carga donde throughput no crece más | Throughput plateau |
| **Crash Point** | Carga donde el sistema deja de responder | 100% error rate |
| **Recovery Time** | Tiempo para volver a normal post-estrés | Monitoring post-test |

### Patrones de degradación

#### Graceful Degradation (deseable)
```
Response Time vs Load:

RT(s)
 10 ┤                                    ╱
  8 ┤                                 ╱─┘
  6 ┤                             ╱──┘
  4 ┤                        ╱───┘
  2 ┤────────────────────╱──┘
  0 ┤
    └────────────────────────────────────→ Users
    0    500   1000  1500  2000  2500

→ Degradación gradual, predecible
→ Sistema sigue respondiendo (más lento)
→ Sin errores catastróficos
```

#### Catastrophic Failure (indeseable)
```
Response Time vs Load:

RT(s)
 ∞  ┤                              │ TIMEOUT
 30 ┤                              │
 20 ┤                              │
 10 ┤                              │
  2 ┤──────────────────────────────┘
  0 ┤
    └────────────────────────────────────→ Users
    0    500   1000  1500  2000  2500

→ Todo funciona bien... hasta que no funciona
→ Cliff effect: pasa de OK a muerto instantáneamente
→ Sin warning previo
```

#### Thrashing Pattern
```
Response Time vs Load:

RT(s)
 15 ┤          ╱╲   ╱╲
 12 ┤         ╱  ╲ ╱  ╲  ╱╲
  9 ┤        ╱    ╳    ╲╱  ╲
  6 ┤    ╱╲ ╱                ╲
  3 ┤───╱  ╳
  0 ┤
    └────────────────────────────────────→ Users
    0    500   1000  1500  2000  2500

→ Sistema inestable, oscilando
→ Típico de GC storms o connection pool contention
→ Servicio intermitente
```

---

## Análisis de Resultados de Stress Test

### Reporte de Breaking Point

```
STRESS TEST RESULTS SUMMARY
════════════════════════════

Normal Capacity (verified):     1,000 users
                                550 TPS, P95 = 1.8s

Breaking Point (SLA breach):   1,800 users
                                P95 exceeded 3s threshold
                                
Saturation Point:               2,200 users
                                Throughput capped at 890 TPS
                                
Crash Point:                    3,100 users
                                Error rate > 80%
                                Multiple servers unresponsive

First Component to Fail:        Database Connection Pool
                                Exhausted at 1,600 users
                                
Failure Mode:                   Semi-graceful
                                Degradation gradual 1000-2200
                                Rapid collapse 2200-3100
                                
Recovery Time:                  8 minutes after load removed
                                Full recovery, no data loss
                                
Safety Margin:                  80% (1,800/1,000 = 1.8x)
```

### Mapa de calor de recursos

```
Load Level:    1000u  1200u  1500u  1800u  2200u  3000u
─────────────────────────────────────────────────────────
CPU App:       ■■░░░  ■■■░░  ■■■■░  ■■■■■  ■■■■■  ■■■■■
CPU DB:        ■■░░░  ■■░░░  ■■■░░  ■■■■░  ■■■■■  ■■■■■
Memory App:    ■■░░░  ■■░░░  ■■■░░  ■■■░░  ■■■■░  ■■■■■
Memory DB:     ■■■░░  ■■■░░  ■■■░░  ■■■■░  ■■■■░  ■■■■■
Disk I/O:      ■░░░░  ■░░░░  ■■░░░  ■■░░░  ■■■░░  ■■■■░
Network:       ■░░░░  ■░░░░  ■░░░░  ■■░░░  ■■░░░  ■■■░░
DB Conns:      ■■░░░  ■■■░░  ■■■■░  ■■■■■  ■■■■■  ■■■■■ ← FIRST TO SATURATE
Thread Pool:   ■■░░░  ■■░░░  ■■■░░  ■■■■░  ■■■■■  ■■■■■

░ = Available   ■ = In use   ■■■■■ = Saturated
```

---

## Patrones de Recuperación

### Recovery Test Post-Stress
```
Test sequence:
1. Ramp-up to normal load (1000 users) → verify baseline
2. Stress to 3000 users → observe failure
3. Remove ALL load → start recovery timer
4. Wait for recovery indicators:
   - All services responding
   - Error rate = 0%
   - Response time back to baseline
   - Resource utilization back to normal
   - No stuck transactions
5. Re-apply normal load → verify system works normally post-stress

Recovery Classification:
- < 1 min:  Excellent (elastic)
- 1-5 min:  Good
- 5-15 min: Acceptable
- 15+ min:  Poor (may need manual intervention)
- No auto-recovery: Critical (requires restart)
```

---

## Validaciones Específicas del Stress Testing

### Data Integrity Check
```sql
-- Ejecutar ANTES del stress test
SELECT COUNT(*) as pre_count FROM orders;
SELECT SUM(amount) as pre_total FROM orders;

-- Ejecutar DESPUÉS del stress test
SELECT COUNT(*) as post_count FROM orders;
SELECT SUM(amount) as post_total FROM orders;

-- Verificar consistencia
-- ¿Hay transacciones parciales?
-- ¿Hay duplicados?
-- ¿Hay registros corruptos?
SELECT * FROM orders 
WHERE status = 'IN_PROGRESS' 
AND created_at < NOW() - INTERVAL '1 hour';
```

### Circuit Breaker Validation
```
Verificar que bajo estrés:
□ Circuit breaker se activa (OPEN state)
□ Requests no se envían a servicio saturado
□ Fallback response se sirve correctamente
□ Circuit breaker se recupera (HALF-OPEN → CLOSED)
□ No hay cascading failures
```

### Auto-scaling Validation
```
Verificar que bajo estrés:
□ Auto-scaling detecta la sobrecarga
□ Nuevas instancias se provisionen en tiempo razonable
□ Load balancer incorpora nuevas instancias
□ Carga se distribuye a nuevas instancias
□ Response time mejora con nuevas instancias
□ Scale-down funciona correctamente post-estrés
```

---

## Ejemplo de Stress Test Script (k6)

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const responseTime = new Trend('response_time');

export const options = {
  stages: [
    // Ramp-up to normal load
    { duration: '10m', target: 1000 },
    // Hold at normal (baseline)
    { duration: '10m', target: 1000 },
    // Stress: ramp beyond capacity
    { duration: '5m', target: 2000 },
    { duration: '5m', target: 3000 },
    { duration: '5m', target: 4000 },
    { duration: '5m', target: 5000 },
    // Hold at max stress
    { duration: '10m', target: 5000 },
    // Recovery: remove all load
    { duration: '5m', target: 0 },
  ],
  thresholds: {
    // Note: These will likely FAIL in a stress test
    // That's expected - we're testing limits
    'http_req_duration': ['p(95)<5000'],
    'errors': ['rate<0.5'],
  },
};

export default function () {
  const res = http.get('https://api.example.com/products');
  
  const success = check(res, {
    'status is 200': (r) => r.status === 200,
    'response time OK': (r) => r.timings.duration < 5000,
  });
  
  errorRate.add(!success);
  responseTime.add(res.timings.duration);
  
  sleep(Math.random() * 3 + 1); // 1-4 second think time
}
```

---

## Recomendaciones de Seguridad

### Precauciones al ejecutar Stress Tests
1. **NUNCA en producción** - Siempre en entorno aislado
2. **Avisar al equipo** - Puede afectar servicios compartidos
3. **Tener rollback plan** - Si algo sale muy mal
4. **Monitorear infraestructura compartida** - Red, DNS, etc.
5. **Definir abort criteria claros** - Saber cuándo parar
6. **Backup de datos** - Antes del test
7. **Verificar integridad post-test** - Datos y configuración

---

*Documento de referencia - Performance Test Life Cycle*
*Última actualización: Junio 2026*
