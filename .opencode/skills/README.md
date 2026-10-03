# PTLC Skills Pack — Índice Maestro

> **Este archivo es el punto de entrada único del knowledge base.** Toda la documentación del Performance Test Life Cycle (PTLC) y los procedimientos de los agentes viven aquí, como skills organizadas por tema.
> **Para agentes AI:** usar este índice para navegar; leer directamente el `SKILL.md` de la skill que corresponda al tema, y de ahí los documentos detallados que ahí se enlazan.

---

## 🏗️ Arquitectura v2.0

- **Entry point obligatorio:** `ptlc-orchestrator` (agente en `.opencode/agents/ptlc-orchestrator.md`) — todo request del usuario entra por él. Orquesta las 6 fases del PTLC cargando las skills del pipeline, y deriva tareas generales (no-PTLC) al equipo `gem-*`.
- **Pipeline PTLC:** 6 skills de fase (`ptlc-intake` → `ptlc-diagnostics` → `ptlc-procedure-plan` → `ptlc-test-plan` → `ptlc-execution` → `ptlc-analysis`), con approval gate antes de ejecutar.
- **Knowledge base:** 12 skills temáticas (~650 KB, 48 documentos) que reemplazan la antigua carpeta `DOCs/`.
- **Skills operativas:** 8 skills `performance-*` y `{tool}-performance-workflow` para diseño, ejecución y análisis.

---

## 📚 Skills de Conocimiento (12)

| Skill | Tema | Detalle |
|-------|------|---------|
| [ptlc-fundamentos](ptlc-fundamentos/SKILL.md) | Definición PTLC, NFRs, glosario, roles RACI, ISO 25010 / ISTQB / TMMi / SRE | 3 documentos |
| [ptlc-tipos-de-pruebas](ptlc-tipos-de-pruebas/SKILL.md) | 22+ tipos: load, stress, soak, spike, baseline, smoke, capacity, resiliency… | 7 documentos |
| [ptlc-fases-del-ciclo](ptlc-fases-del-ciclo/SKILL.md) | Las 9 fases: requisitos → planificación → diseño → entorno → scripts → ejecución → análisis → optimización → cierre | 4 documentos |
| [ptlc-metricas-kpis](ptlc-metricas-kpis/SKILL.md) | Percentiles, Apdex, throughput, error rate, Little's Law, fórmulas pass/fail | 1 documento |
| [ptlc-herramientas](ptlc-herramientas/SKILL.md) | Guías exhaustivas k6, JMeter, Gatling, Locust + matriz de decisión | 6 documentos |
| [ptlc-workload-modeling](ptlc-workload-modeling/SKILL.md) | Little's Law, cálculo de VUs, distribuciones, patrones de tráfico | 1 documento |
| [ptlc-monitoreo](ptlc-monitoreo/SKILL.md) | Prometheus, Grafana, OpenTelemetry, Jaeger, alerting | 1 documento |
| [ptlc-scripting](ptlc-scripting/SKILL.md) | Correlación, tokens, WebSocket, GraphQL, data management | 1 documento |
| [ptlc-analisis-bottlenecks](ptlc-analisis-bottlenecks/SKILL.md) | RCA: 5 Whys, Fishbone, profiling, bottlenecks de DB/red | 1 documento |
| [ptlc-mejores-practicas](ptlc-mejores-practicas/SKILL.md) | CI/CD, shift-left, errores comunes, tendencias | 1 documento |
| [ptlc-arquitectura-mapas](ptlc-arquitectura-mapas/SKILL.md) | Mapas de arquitectura y convenciones `AGENTS.md` | 5 documentos |
| [ptlc-roadmap-decisiones](ptlc-roadmap-decisiones/SKILL.md) | ADRs, roadmap v2.0, plan de implementación, `PRD.yaml` | 4 documentos |

## 🤖 Skills del Pipeline PTLC (6)

Cada skill es el procedimiento completo de una fase (lecturas obligatorias, workflow, formato de salida y reglas). Son invocadas por `ptlc-orchestrator` en orden secuencial.

| Skill | Wave | Rol |
|-------|------|-----|
| [ptlc-intake](ptlc-intake/SKILL.md) | 1 | Recopila requisitos y selecciona herramienta |
| [ptlc-diagnostics](ptlc-diagnostics/SKILL.md) | 2 | Diagnóstico técnico y readiness score |
| [ptlc-procedure-plan](ptlc-procedure-plan/SKILL.md) | 3 | Tipos de prueba y workload model |
| [ptlc-test-plan](ptlc-test-plan/SKILL.md) | 4 | Documento formal ISTQB/IEEE-829 |
| [ptlc-execution](ptlc-execution/SKILL.md) | 5 | Generación y ejecución de scripts (**requiere aprobación**) |
| [ptlc-analysis](ptlc-analysis/SKILL.md) | 6 | Métricas, RCA y reporte final |

## 🛠️ Skills Operativas (8)

- `performance-tool-selector`: selecciona la herramienta adecuada (k6, JMeter, Gatling, Locust).
- `k6-performance-workflow`: flujo de trabajo de k6 para diseño, ejecución y análisis.
- `jmeter-performance-workflow`: flujo de trabajo de JMeter, incluyendo modo no-GUI y estructura de plan.
- `gatling-performance-workflow`: flujo de trabajo de Gatling con DSL e injection profiles.
- `locust-performance-workflow`: flujo de trabajo de Locust con user classes, load shapes y modo distribuido.
- `performance-test-strategy`: diseña estrategia de pruebas (load, stress, spike, soak, baseline).
- `performance-metrics-analysis`: analiza percentiles, Apdex, throughput y criterios pass/fail.
- `performance-diagnostics-rca`: RCA técnico con foco en bottlenecks de app, DB y red.

---

## 🔍 Lookup Rápido por Necesidad

| Necesito... | Ir a |
|-------------|------|
| Entender qué es el PTLC, roles, estándares | [ptlc-fundamentos](ptlc-fundamentos/SKILL.md) |
| Saber qué tipo de prueba usar | [ptlc-tipos-de-pruebas](ptlc-tipos-de-pruebas/SKILL.md) |
| Ejecutar las fases del ciclo | [ptlc-fases-del-ciclo](ptlc-fases-del-ciclo/SKILL.md) |
| Métricas, KPIs, fórmulas, percentiles | [ptlc-metricas-kpis](ptlc-metricas-kpis/SKILL.md) |
| Elegir o usar una herramienta | [ptlc-herramientas](ptlc-herramientas/SKILL.md) |
| Modelar carga, calcular VUs, Little's Law | [ptlc-workload-modeling](ptlc-workload-modeling/SKILL.md) |
| Monitoreo, Prometheus, Grafana, OTel | [ptlc-monitoreo](ptlc-monitoreo/SKILL.md) |
| Scripting avanzado, correlación, patrones | [ptlc-scripting](ptlc-scripting/SKILL.md) |
| Analizar resultados, RCA, troubleshooting | [ptlc-analisis-bottlenecks](ptlc-analisis-bottlenecks/SKILL.md) |
| Best practices, CI/CD, errores comunes | [ptlc-mejores-practicas](ptlc-mejores-practicas/SKILL.md) |
| Diagramas de arquitectura y convenciones | [ptlc-arquitectura-mapas](ptlc-arquitectura-mapas/SKILL.md) |
| Roadmap, ADRs, PRD del producto | [ptlc-roadmap-decisiones](ptlc-roadmap-decisiones/SKILL.md) |
| Iniciar un proyecto PTLC completo | Agente `ptlc-orchestrator` |

## 📂 Estructura de cada skill temática

```
.opencode/skills/<skill>/
├── SKILL.md        ← índice temático (frontmatter + resumen + tabla de contenido)
└── NN_Tema.md      ← documentos detallados (antes DOCs/<carpeta>/)
```

Las skills mantienen el prefijo numérico `NN_` original para preservar el orden de lectura.

## 📄 Entregables del PTLC (no son knowledge base)

- `docs/plan/{plan_id}/plan.yaml` — estado del plan activo
- `docs/performance-test-plan.md` — plan de pruebas formal
- `docs/performance-test-report.md` — reporte de resultados
- `tests/performance/{tool}/{plan_id}/` — scripts generados on-demand

## Fuentes externas consideradas

- `jeremylongshore/claude-code-plugins-plus-skills` (categoría `10-performance-testing`)
- `jabrena/cursor-rules-java` (skill `151-java-performance-jmeter`)

Ver [SOURCE_MAPPING.md](SOURCE_MAPPING.md) para el detalle de adaptación de skills externas.

*Skills adaptadas al contexto PTLC de este repositorio.*
