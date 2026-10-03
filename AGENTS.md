# AGENTS.md

Guía persistente para agentes OpenCode.

## Qué es

**Intelligent Performance Test Orchestrator v3**: base de conocimiento del Performance Test Life Cycle (PTLC). El conocimiento vive como skills en `.opencode/skills/`; los agentes de `.opencode/agents/` orquestan el performance testing.

**Idioma primario: español** en documentación, output y navegación.

## Entry point

**`ptlc-orchestrator` es el entry point OBLIGATORIO de todo request** (`opencode.json` lo fija como `default_agent`). Detecta el dominio en Phase 0 y ejecuta el pipeline cargando una skill por fase; lo no-PTLC se resuelve con los subagentes integrados (`general`/`explore`) o desde el knowledge base.

- **1 · `ptlc-intake`** — requisitos + selección de herramienta
- **2 · `ptlc-diagnostics`** — diagnóstico técnico + readiness
- **3 · `ptlc-procedure-plan`** — tipos de prueba, escenarios, workload model
- **4 · `ptlc-test-plan`** — plan formal ISTQB/IEEE-829
- **Approval Gate** — requiere aprobación explícita del usuario
- **5 · `ptlc-execution`** — scripts + ejecución
- **6 · `ptlc-analysis`** — métricas + RCA + reporte final

## Reglas obligatorias

- **`<pre_execution>`**: todo agente o skill con esa sección DEBE leer con `read` lo que lista antes de producir output.
- **3 niveles**: `.opencode/skills/README.md` (índice maestro) → `SKILL.md` de la skill → `NN_Tema.md` (autoritativo). Leer el Nivel 2 antes de editar un Nivel 3.
- **Edición**: Nivel 3 usa naming `NN_Topic_Name.md`. No duplicar docs: actualizar el existente. Al mover o renombrar, actualizar referencias en `.opencode/skills/README.md` y el `SKILL.md` padre.
- **Catálogo**: el índice de skills (y herramientas en `ptlc-herramientas/`) está en `.opencode/skills/README.md`.

## Presupuesto de tokens

- **Índice antes que documento**: dudas → `SKILL.md`/índice; detalle → sección con `grep -n "^## "` + `read` por offset/limit. Nunca leer completo un doc >2.000 tokens.
- **Cheat sheets primero**: fórmulas/umbrales en `ptlc-metricas-kpis/00_Cheat_Sheet_Metricas.md`, `ptlc-workload-modeling/00_Cheat_Sheet_Workload.md` y `ptlc-herramientas/00b_Cheat_Sheet_Herramientas.md` (bajo `.opencode/skills/`); el doc completo, para API/sintaxis/ejemplos.
- **Envelope acumulado**: cada fase persiste su bloque en `docs/plan/{plan_id}/context_envelope.json`; las siguientes lo cargan y no releen lo ya sintetizado.
- **Medición continua**: `python scripts/measure_tokens.py --strict` valida: activo ≤1.400; agente ≤3.200; `SKILL.md` ≤2.000; detalle ≤6.000.

## Entregables

- `docs/plan/{plan_id}/plan.yaml` — plan activo (workflows resumibles)
- `docs/performance-test-plan.md` — plan de pruebas formal
- `tests/performance/{tool}/` — scripts generados
- `docs/performance-test-report.md` — reporte final con RCA y veredicto PASSED/FAILED

## Rutas clave

- `.opencode/skills/README.md` — índice maestro
- `.opencode/skills/ptlc-roadmap-decisiones/PRD.yaml` — requisitos de producto (Phase 0)
- `.opencode/agents/ptlc-orchestrator.md` — entry point y pipeline
- `opencode.json` — `default_agent` y config del proyecto