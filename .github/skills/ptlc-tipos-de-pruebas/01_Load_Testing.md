# Load Testing - Guía Completa

## Definición

El **Load Testing** es un tipo de prueba de rendimiento que simula la carga esperada (normal y pico) sobre un sistema para verificar que cumple con los requisitos de rendimiento bajo condiciones realistas de uso.

---

## Objetivos del Load Testing

### Objetivos primarios
1. **Validar SLAs** bajo carga esperada
2. **Identificar cuellos de botella** que aparecen con carga normal/pico
3. **Verificar capacity planning** (¿la infraestructura es suficiente?)
4. **Establecer baselines** de rendimiento para futuras comparaciones
5. **Detectar regresiones** entre releases

### Objetivos secundarios
- Validar configuraciones de auto-scaling
- Verificar comportamiento de load balancers
- Confirmar que el monitoreo detecta degradaciones
- Validar timeout configurations

---

## Diseño de un Load Test

### Componentes esenciales

```yaml
load_test_design:
  objective: "Verificar que el sistema soporta carga pico de 1000 usuarios"
  
  load_profile:
    ramp_up:
      duration: "30 minutes"
      start_users: 0
      end_users: 1000
      pattern: "linear"
      
    steady_state:
      duration: "2 hours"
      users: 1000
      
    ramp_down:
      duration: "15 minutes"
      start_users: 1000
      end_users: 0
      
  scenarios:
    - name: "Browse Products"
      weight: 50%
      transactions:
        - "Open Homepage"
        - "View Category"
        - "View Product Detail"
        - "View Product Reviews"
      think_time: "8-12 seconds (normal dist)"
      
    - name: "Search & Compare"
      weight: 25%
      transactions:
        - "Search by Keyword"
        - "Filter Results"
        - "Compare Products"
      think_time: "6-10 seconds (normal dist)"
      
    - name: "Purchase Flow"
      weight: 15%
      transactions:
        - "Add to Cart"
        - "View Cart"
        - "Enter Shipping"
        - "Enter Payment"
        - "Confirm Order"
      think_time: "10-20 seconds (normal dist)"
      
    - name: "Account Management"
      weight: 10%
      transactions:
        - "Login"
        - "View Profile"
        - "View Order History"
        - "Update Settings"
      think_time: "5-8 seconds (normal dist)"
      
  acceptance_criteria:
    response_time:
      homepage: "P95 < 2s"
      search: "P95 < 3s"
      checkout: "P95 < 5s"
      api_calls: "P95 < 1s"
    throughput:
      minimum: "500 TPS"
    error_rate:
      maximum: "0.5%"
    resource_utilization:
      cpu: "< 75%"
      memory: "< 80%"
```

---

### Patrones de Carga para Load Testing

#### Patrón 1: Constant Load
```
Users
1000 ┤          ┌──────────────────────────┐
     │         /│                          │\
     │        / │      Steady State        │ \
     │       /  │      (2 hours)           │  \
     │      /   │                          │   \
   0 ┤─────/────┴──────────────────────────┴────\──
     └──────────────────────────────────────────────→ Time
        Ramp-up                              Ramp-down
```

#### Patrón 2: Step Load
```
Users
1000 ┤                              ┌──────┐
 800 ┤                    ┌─────────┘      │
 600 ┤          ┌─────────┘                │
 400 ┤┌─────────┘                          │
 200 ┤┘                                    │
   0 ┤                                     └──
     └──────────────────────────────────────────→ Time
     Incrementos de 200 users cada 15 min
```

#### Patrón 3: Peak-Valley
```
Users
1200 ┤     ╱╲        ╱╲
1000 ┤    ╱  ╲      ╱  ╲      (simula picos del día)
 800 ┤   ╱    ╲    ╱    ╲
 600 ┤──╱      ╲──╱      ╲──
 400 ┤╱                      ╲
   0 ┤                        └
     └──────────────────────────────────────────→ Time
```

---

## Proceso de Ejecución

### Pre-ejecución checklist
```
□ Scripts validados con smoke test (1-2 usuarios)
□ Datos de prueba cargados y verificados
□ Entorno aislado y estable
□ Monitoreo configurado y activo
□ Baseline registrada (sin carga)
□ Equipo notificado del inicio
□ Criterios de parada definidos (abort criteria)
□ Capacidad de load generators verificada
```

### Durante la ejecución
1. **Iniciar monitoreo** antes de empezar la carga
2. **Ramp-up gradual** - verificar que el sistema responde normalmente
3. **Monitorear en tiempo real:**
   - Response times por transacción
   - Throughput (TPS)
   - Error rate
   - Resource utilization (todos los servidores)
4. **Documentar eventos** relevantes (errores, alerts, anomalías)
5. **NO realizar cambios** en la aplicación o infraestructura durante el test
6. **Mantener steady state** el tiempo planificado
7. **Ramp-down controlado**
8. **Continuar monitoreo** post-test (recovery)

### Criterios de aborto
| Condición | Umbral de aborto | Acción |
|-----------|------------------|--------|
| Error rate | > 10% sostenido 5 min | Abort, investigate |
| Response time | > 30s P95 sostenido | Abort, investigate |
| Server down | Cualquier componente caído | Abort, investigate |
| Data corruption | Detectada | Abort immediately |
| Monitoring failure | Datos no se capturan | Abort, fix monitoring |

---

## Análisis de Resultados de Load Test

### Métricas clave a evaluar

#### 1. Response Time Distribution
```
Transacción: "Complete Purchase"
┌────────────────────────────────────┐
│  P50:  800ms   ✅ (SLA: < 2s)      │
│  P90:  1.5s    ✅ (SLA: < 3s)      │
│  P95:  2.2s    ✅ (SLA: < 5s)      │
│  P99:  4.8s    ✅ (SLA: < 5s)      │
│  Max:  12.3s   ⚠️ (outlier)        │
│  Avg:  950ms                        │
└────────────────────────────────────┘
```

#### 2. Throughput over Time
```
TPS
600 ┤     ┌─────────────────────────────┐
    │    /│          Steady: ~550 TPS   │\
500 ┤   / │                             │ \
    │  /  │                             │  \
400 ┤ /   │                             │   \
    │/    │                             │    \
300 ┤     │                             │
    └─────┴─────────────────────────────┴──────→ Time
      Target: ≥ 500 TPS → ✅ PASS
```

#### 3. Error Rate Trend
```
Error %
2.0 ┤
    │
1.5 ┤
    │        SLA Limit: 0.5%
1.0 ┤─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
    │
0.5 ┤
    │  ──────────────────────────────── (Actual: 0.3%)
0.0 ┤
    └──────────────────────────────────────→ Time
      ✅ PASS - Dentro del SLA
```

#### 4. Resource Correlation
```
Correlacionar Users vs CPU vs Response Time:

Users: ▁▂▃▄▅▆▇█████████████████████████▇▆▅▄▃▂▁
CPU %: ▁▂▃▄▅▅▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▅▅▄▃▂▁
Resp:  ▁▁▁▂▂▂▂▂▂▂▂▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▂▂▂▁▁▁

→ CPU se estabiliza en ~65% (OK)
→ Response time estable durante steady state (OK)
→ Sin degradación progresiva (OK)
```

---

## Variantes de Load Testing

### Capacity Testing
Determinar cuántos usuarios puede soportar antes de incumplir SLAs.
```
Incrementar usuarios gradualmente hasta que:
- Response time > SLA threshold
- Error rate > SLA threshold
- Resources > safe threshold

Resultado: "El sistema soporta hasta 1,200 usuarios concurrentes
           manteniendo todos los SLAs. A 1,300+ usuarios, P95
           response time excede 5 segundos."
```

### Regression Load Testing
Comparar rendimiento entre versiones:
```
Version 3.1:  P95 = 1.8s @ 1000 users
Version 3.2:  P95 = 2.3s @ 1000 users  ← 28% degradación!

Action: Investigate changes in 3.2 that caused regression
```

### Soak-lite (Extended Load)
Load test extendido (4-8 horas) para detectar tendencias:
- Memory growth
- Connection leaks
- Log file growth
- Cache behavior over time

---

## Ejemplo Completo: Reporte de Load Test

```markdown
# Load Test Report - Sprint 42

## Summary
- **Date:** 2026-06-10
- **Duration:** 2.5 hours (30min ramp + 2h steady)
- **Peak Users:** 1,000 concurrent
- **Result:** ✅ PASS (all SLAs met)

## Key Results
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| P95 Response Time | < 3s | 2.1s | ✅ |
| Throughput | ≥ 500 TPS | 548 TPS | ✅ |
| Error Rate | < 0.5% | 0.2% | ✅ |
| CPU Utilization | < 75% | 68% | ✅ |
| Memory | < 80% | 72% | ✅ |

## Observations
1. Response time stable throughout steady state
2. No memory growth detected
3. Database connection pool peaked at 85% (monitor)
4. One slow query detected (3.2s avg) - not on critical path

## Recommendations
1. Consider increasing DB connection pool by 20%
2. Optimize slow query on /api/reports endpoint
3. Plan capacity review at 1,500 users for next quarter
```

---

## Errores Comunes en Load Testing

| Error | Impacto | Prevención |
|-------|---------|------------|
| Ramp-up muy rápido | Pico inicial irreal | Ramp-up de 15-30+ minutos |
| Sin steady state suficiente | No detecta tendencias | Mínimo 1-2 horas |
| Solo un escenario | No refleja uso real | Múltiples workflows con distribución |
| Cache caliente vs frío | Resultados optimistas | Primer test con cache frío |
| Ignorar ramp-down | No verificar recovery | Incluir y monitorear descenso |
| Load generators saturados | Resultados inválidos | Monitorear CPU de generators |

---

*Documento de referencia - Performance Test Life Cycle*
*Última actualización: Junio 2026*
