# Cheat Sheet — Métricas y KPIs

**Percentiles** — ordenar asc; valor en posición ⌈p/100×n⌉ (ej. `a[int(n×0.95)]`).
P50=mediana · P90=1/10 peor · P95=1/20 peor · P99=1/100 peor.
Regla: P99/P50 >10× → alta variabilidad; <3× → estable.
Detalle: [01_Metricas_Exhaustivas.md](01_Metricas_Exhaustivas.md#percentiles-y-distribución)

**Apdex** — `Apdex = (Satisfied + Tolerating/2) / Total`
Satisfied rt≤T · Tolerating T<rt≤4T · Frustrated rt>4T.
Ej: T=2s, 1000 req (800/150/50) → (800+75)/1000 = 0.875.
≥0.94 Excelente · 0.85-0.93 Bueno · 0.70-0.84 Aceptable · <0.50 Inaceptable.
Detalle: [01_Metricas_Exhaustivas.md](01_Metricas_Exhaustivas.md#apdex-score)

**Throughput · Error rate · Saturación**
`TPS = Transacciones_exitosas / Duración_s` · `RPS = Requests_total / Duración_s`
`Error_Rate = (Failed / Total) × 100`
Little's Law servidor: `L = λ × W` (L=requests concurrentes, λ=RPS, W=s).
Ej: λ=100 RPS, W=0.5s → L=50. Si W↑, para igual λ se necesitan más recursos.
Curva: A lineal → B plateau (saturado) → C decrece.
Detalle: [01_Metricas_Exhaustivas.md](01_Metricas_Exhaustivas.md#calculadora-de-métricas)

**Criterios Pass/Fail** (umbral según SLO)
| Métrica | Criterio | Umbral | Resultado |
|---|---|---|---|
| p95 | response time | ≤ X ms | PENDING |
| p99 | response time | ≤ Y ms | PENDING |
| Error rate | % fallidas | ≤ Z% | PENDING |
| Throughput | ≥ N TPS | ≥ N | PENDING |
| Apdex | score | ≥ 0.85 | PENDING |
| CPU | steady-state | ≤ 80% | PENDING |
Detalle: [01_Metricas_Exhaustivas.md](01_Metricas_Exhaustivas.md#fórmulas-esenciales)
