---
name: ptlc-tipos-de-pruebas
description: "Define tipos: load, stress, soak, spike, resiliency"
---

# 02 — Tipos de Pruebas de Rendimiento

> Índice intermedio. **Cuándo leer:** qué tipo de prueba ejecutar según tu objetivo. Detalle en los documentos de esta skill (abajo).

## Mapa Completo: 22+ Tipos de Pruebas

```
VALIDACIÓN DE CAPACIDAD          ESTABILIDAD A LARGO PLAZO       LÍMITES Y EXTREMOS
├── Load Testing                 ├── Endurance/Soak Testing      ├── Stress Testing
├── Baseline Testing             ├── Reliability Testing         ├── Spike Testing
├── Smoke Testing                └── Regression Testing          ├── Peak Testing
└── Capacity Testing                                             ├── Breakpoint Testing
                                                                  └── Saturation Testing

RESILIENCIA Y RECUPERACIÓN       CONFIGURACIÓN Y RED             ESPECÍFICOS POR CAPA
├── Resiliency/Chaos Testing     ├── Configuration Testing       ├── API Performance Testing
├── Failover Testing             ├── Network Testing             ├── Browser/Frontend Testing
├── Recovery Testing             └── Scalability Testing         ├── Volume Testing (DB)
└── Concurrency Testing                                          └── Isolation Testing
```

---

## ¿Qué tipo de prueba necesito?

| Situación | Tipo recomendado | Archivo |
|-----------|------------------|---------|
| Validar que el sistema aguanta la carga diaria | Load Testing | `01_Load_Testing.md` |
| Establecer una línea base medible y repetible | Baseline Testing | `04_Baseline_Testing.md` |
| Verificar que un deploy no rompió nada rápidamente | Smoke Testing | `05_Smoke_Peak_Capacity_Breakpoint.md` |
| Saber cuántos usuarios soporta antes de colapsar | Stress / Breakpoint | `02_Stress_Testing.md` / `05_...` |
| Evaluar estabilidad durante 8-72 horas | Endurance / Soak | `03_Endurance_Spike_Volume_Scalability.md` |
| Simular un pico repentino (flash sale, evento TV) | Spike Testing | `03_Endurance_Spike_Volume_Scalability.md` |
| Verificar escalado horizontal/vertical funciona | Scalability Testing | `03_Endurance_Spike_Volume_Scalability.md` |
| Validar comportamiento con alta carga en DB | Volume Testing | `03_Endurance_Spike_Volume_Scalability.md` |
| Probar que el sistema se recupera de fallos | Failover / Recovery | `06_Configuration_Failover_...md` |
| Inyectar fallos deliberadamente (Chaos Engineering) | Resiliency Testing | `07_Resiliency_Testing/` (3 docs) |
| Verificar APIs individualmente bajo carga | API Performance | `06_Configuration_Failover_...md` |
| Medir Core Web Vitals y tiempos del browser | Browser/Frontend | `06_Configuration_Failover_...md` |
| Probar diferentes configuraciones de infra | Configuration Testing | `06_Configuration_Failover_...md` |
| Asegurar que un fix no degradó performance | Regression Testing | `06_Configuration_Failover_...md` |

---

## 📂 Contenido de la Subcarpeta

### [`01_Load_Testing.md`](01_Load_Testing.md) — carga sostenida en VUs constantes
- Para qué: validar que el SUT sostiene la carga objetivo.
- Consultar si: dimensionas VUs, ramp-up y steady-state · necesitas el reporte de ejemplo o las variantes (step, constant, wave)

### [`02_Stress_Testing.md`](02_Stress_Testing.md) — llevar el SUT más allá del límite
- Para qué: encontrar el punto de quiebre y los límites seguros.
- Consultar si: necesitas distinguir load vs stress · eliges tipo de stress (gradual, sudden, resource-bound) · quieres el script k6 de ejemplo

### [`03_Endurance_Spike_Volume_Scalability.md`](03_Endurance_Spike_Volume_Scalability.md) — endurance, spike, volume, scalability
- Para qué: cuatro tipos de carga agrupados en un solo doc.
- Consultar si: pruebas larga duración (8-72 h) o picos súbitos · validas volumen de datos o escalado horizontal · aplicas Amdahl's Law para proyectar escalabilidad

### [`04_Baseline_Testing.md`](04_Baseline_Testing.md) — línea base medible y repetible
- Para qué: fijar el punto de comparación de todas las pruebas.
- Consultar si: ejecutas el baseline inicial del ciclo · necesitas el template del documento baseline

**⚡ Destacado:** una sola ejecución NO es suficiente. Se necesitan múltiples iteraciones hasta lograr estabilidad estadística (Coeficiente de Variación < 10%).

### [`05_Smoke_Peak_Capacity_Breakpoint.md`](05_Smoke_Peak_Capacity_Breakpoint.md) — smoke, peak, capacity, breakpoint, concurrency, reliability
- Para qué: límites de capacidad y pruebas rápidas por deploy.
- Consultar si: mides cuántos usuarios soporta el sistema · defines criterios pass/fail por tipo de prueba

### [`06_Configuration_Failover_Recovery_Regression_y_Otros.md`](06_Configuration_Failover_Recovery_Regression_y_Otros.md) — configuración, failover, recovery, regression y 6 más
- Para qué: tipos por infraestructura, red y capa concreta.
- Consultar si: pruebas configuration, network, isolation o saturation · mides API, browser/frontend o recovery · quieres el mapa completo de los 22 tipos con clasificación cruzada

### [`07_Resiliency_Testing/`](07_Resiliency_Testing/) — chaos engineering y resiliencia (3 documentos)

Guía partida en 3 partes. Elige solo la que necesitas:

| Documento | Para qué |
|-----------|----------|
| [`01_Fundamentos_y_Patrones_de_Resiliencia.md`](07_Resiliency_Testing/01_Fundamentos_y_Patrones_de_Resiliencia.md) | Qué es resiliencia, diferencias con stress/failover/recovery, principios de chaos engineering, steady-state hypothesis y los 7 patrones (Circuit Breaker, Bulkhead, Retry, Timeout, Graceful Degradation, Rate Limiting, Fallback) · índice completo de la guía |
| [`02_Fault_Injection_Herramientas_y_Cloud.md`](07_Resiliency_Testing/02_Fault_Injection_Herramientas_y_Cloud.md) | Qué fallas inyectar (red, compute, aplicación, dependencias, infraestructura) · herramientas (LitmusChaos, Chaos Mesh, AWS FIS, Toxiproxy, Chaos Toolkit) · automatización en CI/CD · patrones de resiliencia en Kubernetes, Istio y multi-región |
| [`03_Experimentos_Metricas_y_Operacion.md`](07_Resiliency_Testing/03_Experimentos_Metricas_y_Operacion.md) | Template de experimento, priorización y progresión de complejidad · Game Days · métricas, Resilience Score y SLOs · scripts k6 y bash de fault injection · antipatrones · checklist de implementación |

---

## 🔗 Relación con otras categorías

| Desde aquí puedo ir a... | Para... |
|--------------------------|---------|
| [ptlc-metricas-kpis](../ptlc-metricas-kpis/SKILL.md) | Definir qué medir en cada tipo de prueba |
| [ptlc-herramientas](../ptlc-herramientas/SKILL.md) | Implementar la prueba con una tool específica |
| [ptlc-workload-modeling](../ptlc-workload-modeling/SKILL.md) | Calcular la carga para load/stress/spike |
| [ptlc-fases-del-ciclo](../ptlc-fases-del-ciclo/SKILL.md) | Entender en qué fase del ciclo se ejecuta cada tipo |