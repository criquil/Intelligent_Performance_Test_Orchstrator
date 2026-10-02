# PTLC Knowledge Base — Instrucciones Globales para Agentes

Este repositorio es la **base de conocimiento autoritativa** del Performance Test Life Cycle (PTLC).

## Directiva principal

**Todo agente que opere en este repositorio DEBE leer los archivos de `DOCs/` antes de producir cualquier output.** No inventar criterios, patrones ni ejemplos que contradigan la documentación provista.

## Índice de documentos (37 archivos, ~650 KB)

| Carpeta | Contenido | Archivos clave |
|---------|-----------|----------------|
| `DOCs/01_Introduccion_PTLC/` | Fundamentos, roles, estándares | `01_Definicion_y_Fundamentos.md`, `02_Roles_y_Responsabilidades.md`, `03_Frameworks_y_Estandares.md` |
| `DOCs/02_Tipos_de_Pruebas/` | 22+ tipos de prueba | `01` Load · `02` Stress · `03` Endurance/Spike · `04` Baseline · `05` Smoke/Capacity · `06` Config/Failover · `07` Resiliency |
| `DOCs/03_Fases_del_PTLC/` | Ciclo completo | `01` Requisitos · `02` Planificación · `03` Entorno/Ejecución · `04` Análisis/Cierre |
| `DOCs/04_Metricas_y_KPIs/` | Métricas y fórmulas | `01_Metricas_Exhaustivas.md` — p50/p90/p95/p99, Apdex, throughput, error rate |
| `DOCs/05_Herramientas/` | Guías por herramienta | `03` Locust (97KB) · `04` Gatling (95KB) · `05` JMeter (69KB) · `06` k6 expandida (73KB) |
| `DOCs/06_Workload_Modeling/` | Modelo de carga | `01_Workload_Modeling_Exhaustivo.md` — Little's Law, VU calc, distribuciones |
| `DOCs/07_Entorno_y_Monitoreo/` | Observabilidad | `01_Monitoreo_y_Observabilidad.md` — Prometheus, Grafana, OTel, alerting |
| `DOCs/08_Desarrollo_de_Scripts/` | Scripting avanzado | `01_Scripting_Avanzado.md` — correlación, tokens, WebSocket, GraphQL |
| `DOCs/09_Analisis_y_Bottlenecks/` | RCA y troubleshooting | `01_RCA_y_Troubleshooting.md` — 5 Whys, Fishbone, profiling, DB queries |
| `DOCs/10_Mejores_Practicas/` | CI/CD y tendencias | `01_CICD_y_Tendencias_Futuras.md` — shift-left, K8s, microservicios |

## Regla de lectura obligatoria

Cada agente tiene una sección `<pre_execution>` que lista los archivos **que DEBE leer con la herramienta `read` antes de ejecutar su tarea**. Esta lectura no es opcional.

## Entry Point v2.0

- `gem-orchestrator` — **entry point unificado** para todos los requests (general y PTLC)
  - Detecta automáticamente intención de performance testing en Phase 0
  - Orquesta el pipeline PTLC completo delegando a los agentes `ptlc-*`
- `ptlc-orchestrator` — entry point directo de conveniencia para acceso rápido al pipeline PTLC

## Pipeline PTLC (orquestado por gem-orchestrator)

`ptlc-intake` → `ptlc-diagnostics` → `ptlc-procedure-plan` → `ptlc-test-plan` → `ptlc-execution` → `ptlc-analysis`

**Nota:** Los scripts de prueba se generan **on-demand** en `tests/performance/{tool}/{plan_id}/` al ejecutar `ptlc-execution`. No existen scripts pre-creados. Cada proyecto elige UNA herramienta (k6, JMeter, Gatling o Locust).

## Idioma

Español en todas las respuestas, documentos y comunicación.
