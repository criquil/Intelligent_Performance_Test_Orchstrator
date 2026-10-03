# Cheat Sheet — Workload Modeling

**Little's Law** `L = λ × W` (L=VUs/requests concurrentes, λ=throughput, W=response time)
- Ej1: λ=100 RPS, W=0.5s → L=50.
- Ej2: λ=200 RPS, W=0.3s → L=60.
Concurrent_Users = (Sessions × Avg_Session_Duration) / Period (5000×5min/60min = 417).
Detalle: [01_Workload_Modeling_Exhaustivo.md](01_Workload_Modeling_Exhaustivo.md#concurrent-users)

**VUs para throughput objetivo**
`VUsers = Target_RPS × (Think_Time + Response_Time) / Requests_Per_Iteration`
Ej: 500 RPS, think 5s, resp 0.5s, 3 req/iter → 500×(5.5)/3 = 917 VUs.
Detalle: [01_Workload_Modeling_Exhaustivo.md](01_Workload_Modeling_Exhaustivo.md#cálculos-fundamentales)

**Ramp-up y fases**
Ramp-up 100 VU/min (5 min→500); template 30 min→1000. Steady ≥30 min (ideal 1 h+); ramp-down 2-5 min.
Detalle: [01_Workload_Modeling_Exhaustivo.md](01_Workload_Modeling_Exhaustivo.md#template-completo-de-workload-model)

**Patrones de carga**
| Patrón | Cuándo usar |
|---|---|
| Constante | validar SLA/capacidad en steady state |
| Rampa | alcanzar carga gradual; evita pico inicial irreal |
| Escalón (step) | hallar knee point/límite por tramos |
| Pico (spike) | validar auto-scaling y recuperación ante subida súbita |
| Ola (wave) | spikes repetidos (p. ej. Black Friday) |
Detalle: [01_Load_Testing.md](../ptlc-tipos-de-pruebas/01_Load_Testing.md#patrones-de-carga-para-load-testing) · [03_Endurance_Spike_Volume_Scalability.md](../ptlc-tipos-de-pruebas/03_Endurance_Spike_Volume_Scalability.md#escenarios-reales-de-spikes)

**VUs ↔ usuarios concurrentes**
VU = usuario virtual (incluye think time). Requests concurrentes = L = λ×W. VUs_activos ≈ L.
Detalle: [01_Workload_Modeling_Exhaustivo.md](01_Workload_Modeling_Exhaustivo.md#cálculos-fundamentales)
