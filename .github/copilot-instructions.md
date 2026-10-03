# PTLC Knowledge Base — Instrucciones Globales para Agentes

Este repositorio es la **base de conocimiento autoritativa** del Performance Test Life Cycle (PTLC), organizada como skills bajo `.github/skills/`.

## Directiva principal

**Todo agente que opere en este repositorio DEBE leer los archivos de la skill correspondiente en `.github/skills/` antes de producir cualquier output.** No inventar criterios, patrones ni ejemplos que contradigan la documentación provista.

## Índice de skills (48 documentos, ~650 KB)

| Skill | Contenido | Archivos clave |
|-------|-----------|----------------|
| `.github/skills/ptlc-fundamentos/` | Fundamentos, roles, estándares | `01_Definicion_y_Fundamentos.md`, `02_Roles_y_Responsabilidades.md`, `03_Frameworks_y_Estandares.md` |
| `.github/skills/ptlc-tipos-de-pruebas/` | 22+ tipos de prueba | `01` Load · `02` Stress · `03` Endurance/Spike · `04` Baseline · `05` Smoke/Capacity · `06` Config/Failover · `07` Resiliency |
| `.github/skills/ptlc-fases-del-ciclo/` | Ciclo completo | `01` Requisitos · `02` Planificación · `03` Entorno/Ejecución · `04` Análisis/Cierre |
| `.github/skills/ptlc-metricas-kpis/` | Métricas y fórmulas | `01_Metricas_Exhaustivas.md` — p50/p90/p95/p99, Apdex, throughput, error rate |
| `.github/skills/ptlc-herramientas/` | Guías por herramienta | `03` Locust (97KB) · `04` Gatling (95KB) · `05` JMeter (69KB) · `06` k6 expandida (73KB) |
| `.github/skills/ptlc-workload-modeling/` | Modelo de carga | `01_Workload_Modeling_Exhaustivo.md` — Little's Law, VU calc, distribuciones |
| `.github/skills/ptlc-monitoreo/` | Observabilidad | `01_Monitoreo_y_Observabilidad.md` — Prometheus, Grafana, OTel, alerting |
| `.github/skills/ptlc-scripting/` | Scripting avanzado | `01_Scripting_Avanzado.md` — correlación, tokens, WebSocket, GraphQL |
| `.github/skills/ptlc-analisis-bottlenecks/` | RCA y troubleshooting | `01_RCA_y_Troubleshooting.md` — 5 Whys, Fishbone, profiling, DB queries |
| `.github/skills/ptlc-mejores-practicas/` | CI/CD y tendencias | `01_CICD_y_Tendencias_Futuras.md` — shift-left, K8s, microservicios |
| `.github/skills/ptlc-arquitectura-mapas/` | Mapas y convenciones | `AGENTS.md`, `MAP.md`, mapas funcionales |
| `.github/skills/ptlc-roadmap-decisiones/` | Roadmap y decisiones | `PRD.yaml`, `ADR_001_ORCHESTRATOR_EVOLUTION.md` |

Punto de entrada completo: `.github/skills/README.md`.

## Regla de lectura obligatoria

Cada agente y skill de fase tiene una sección `<pre_execution>` que lista los archivos **que DEBE leer con la herramienta `read` antes de ejecutar su tarea**. Esta lectura no es opcional.

## Entry Point v3.0

- `ptlc-orchestrator` — **entry point obligatorio** para todo request del usuario
  - Detecta automáticamente intención de performance testing en Phase 0
  - Orquesta el pipeline PTLC completo cargando las skills `ptlc-*` (una por wave)
  - Deriva tareas generales (no-PTLC) a `gem-orchestrator` y el equipo `gem-*`

## Pipeline PTLC (orquestado por ptlc-orchestrator)

`ptlc-intake` → `ptlc-diagnostics` → `ptlc-procedure-plan` → `ptlc-test-plan` → ⚠️ Approval Gate → `ptlc-execution` → `ptlc-analysis`

**Nota:** Los scripts de prueba se generan **on-demand** en `tests/performance/{tool}/{plan_id}/` al ejecutar la skill `ptlc-execution`. No existen scripts pre-creados. Cada proyecto elige UNA herramienta (k6, JMeter, Gatling o Locust).

## Idioma

Español en todas las respuestas, documentos y comunicación.
