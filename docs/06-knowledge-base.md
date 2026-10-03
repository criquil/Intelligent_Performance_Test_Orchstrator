# 06 — Knowledge base: 12 skills temáticas

Índice maestro: `../.claude/skills/README.md`. Catálogo en [05-skills](05-skills.md) · uso por fase en [04-pipeline-ptlc](04-pipeline-ptlc.md). Base: `../.claude/skills/`.

## Las 12 skills (cuándo consultar cada una)

- **ptlc-fundamentos** (`01_Definicion_y_Fundamentos.md`, `02_Roles_y_Responsabilidades.md`, `03_Frameworks_y_Estandares.md`) — qué es el PTLC, glosario, RACI, ISO 25010/ISTQB. Consultar al redactar el plan formal (F4).
- **ptlc-tipos-de-pruebas** (`01_Load_Testing.md`, `02_Stress_Testing.md`, `03_Endurance_Spike_Volume_Scalability.md`, `04_Baseline_Testing.md`, `05_Smoke_Peak_Capacity_Breakpoint.md`, `06_Configuration_Failover_Recovery_Regression_y_Otros.md`, `07_Resiliency_Testing/` ×3) — qué tipo usar. Consultar en F1 (tipos candidatos) y F3 (selección máx 5).
- **ptlc-fases-del-ciclo** (`01_Recopilacion_de_Requisitos.md`, `02_Planificacion_y_Diseno.md`, `03_Entorno_Scripts_Ejecucion.md`, `04_Analisis_Optimizacion_Cierre.md`) — las 9 fases del ciclo. Readiness (F2), estructura del plan (F4), entorno/ejecución (F5), reporting y cierre (F6).
- **ptlc-metricas-kpis** (cheat + `01_Metricas_Exhaustivas.md`) — percentiles, Apdex, throughput, error rate. Consultar en F2-F4 (NFRs) y F6 (cálculo y veredicto).
- **ptlc-herramientas** (ver guías abajo) — elegir herramienta (F1) y sintaxis de scripting/ejecución (F5).
- **ptlc-workload-modeling** (cheat + `01_Workload_Modeling_Exhaustivo.md`) — Little's Law, VUs, patrones. Consultar en F2 (estimación) y F3 (modelo nominal/pico/stress).
- **ptlc-monitoreo** (`01_Monitoreo_y_Observabilidad.md`) — Prometheus, Grafana, OTel, Jaeger, alerting. Consultar en F2 (gaps de observabilidad) y F6 (correlación con infra).
- **ptlc-scripting** (`01_Scripting_Avanzado.md`) — correlación, tokens, data management, WebSocket/GraphQL, error handling. Consultar en F5.
- **ptlc-analisis-bottlenecks** (`01_RCA_y_Troubleshooting.md`) — 5 Whys, Fishbone, patrones de bottleneck DB/red/app. Consultar en F6.
- **ptlc-mejores-practicas** (`01_CICD_y_Tendencias_Futuras.md`) — CI/CD, shift-left, checklist excellence, errores comunes. Consultar en F2 (readiness) y F5 (quality gates).
- **ptlc-arquitectura-mapas** (`MAP.md`, `CONVENTIONS.md`) - mapa de arquitectura/pipeline y convenciones del repo. Consultar al navegar el proyecto.
- **ptlc-roadmap-decisiones** (`PRD.yaml`, `CONTEXT_ENVELOPE.md`) — requisitos de producto y contrato del contexto acumulado. Consultar siempre (Phase 0 + envelope).

## Guías de herramientas

Todo el diseño/scripting/ejecución por herramienta vive en `ptlc-herramientas/` (cada guía abre con mapa de secciones):

| Guía | Contenido |
|------|-----------|
| [00_Comunes_Guia_Herramientas.md](../.claude/skills/ptlc-herramientas/00_Comunes_Guia_Herramientas.md) | Canónica común: CI/CD, troubleshooting, prácticas/antipatrones, proyecto de referencia |
| [06_k6_Guia_Completa_Expandida.md](../.claude/skills/ptlc-herramientas/06_k6_Guia_Completa_Expandida.md) | k6: executors, scenarios, thresholds, lifecycle, datos, xk6 |
| [05_JMeter_Guia_Completa.md](../.claude/skills/ptlc-herramientas/05_JMeter_Guia_Completa.md) | JMeter: thread groups, extractors/correlación, assertions, CLI non-GUI |
| [04_Gatling_Community_Guia_Completa.md](../.claude/skills/ptlc-herramientas/04_Gatling_Community_Guia_Completa.md) | Gatling CE: DSL, injection profiles, feeders, assertions |
| [03_Locust_Guia_Completa.md](../.claude/skills/ptlc-herramientas/03_Locust_Guia_Completa.md) | Locust: user classes, custom shapes, wait times, distribuido |
| [02_JMeter_Gatling_Locust.md](../.claude/skills/ptlc-herramientas/02_JMeter_Gatling_Locust.md) | Comparativa: mismo test en 3 herramientas + decision matrix |

Mapa de secciones por guía (verificado con `grep -n "^## "`): k6 22 secciones · JMeter 23 · Gatling 22 · Locust 20. Regla F5: leer SOLO la guía de la herramienta seleccionada.

## Los 3 cheat sheets (fórmulas primero)

| Cheat | Qué contiene | Cuándo usarlo en vez del doc completo |
|-------|--------------|----------------------------------------|
| [00_Cheat_Sheet_Metricas.md](../.claude/skills/ptlc-metricas-kpis/00_Cheat_Sheet_Metricas.md) | Percentiles, Apdex `(S+T×0.5)/N`, throughput, error rate, plantilla pass/fail | Solo necesitas la fórmula o el umbral (F2-F4, F6) |
| [00_Cheat_Sheet_Workload.md](../.claude/skills/ptlc-workload-modeling/00_Cheat_Sheet_Workload.md) | Little's Law `VU = TPS × RT`, ramp-up, patrones de carga | Solo necesitas VUs o el patrón (F2-F3, F5) |
| [00b_Cheat_Sheet_Herramientas.md](../.claude/skills/ptlc-herramientas/00b_Cheat_Sheet_Herramientas.md) | Matriz de decisión + mapa tarea→sección+línea por guía | Eliges herramienta o buscas executors/thresholds/correlación (F1, F5) |

## Convención de lectura por sección

Cada skill de fase declara lecturas obligatorias en `<pre_execution>`: máx 2 documentos COMPLETOS; el resto por sección:

```bash
grep -n "^## " <archivo>   # localizar la sección (línea)
# leer solo el fragmento con read offset=<línea> limit=<hasta la siguiente sección>
```

Nunca leer completo un doc >2.000 tokens. Antes de leer, consultar `context_envelope.json` por si la conclusión ya está sintetizada.
