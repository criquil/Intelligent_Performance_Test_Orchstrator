# CLAUDE.md

Memoria del proyecto para Claude Code. Guía persistente del repositorio.

## Qué es

**Intelligent Performance Test Orchestrator v3**: base de conocimiento del Performance Test Life Cycle (PTLC). El conocimiento vive como skills en `.claude/skills/`; el subagente de `.claude/agents/` orquesta el performance testing.

**Idioma primario: español** en documentación, output y navegación.

## Entry point obligatorio

`ptlc-orchestrator` es el entry point obligatorio de todo request. Claude Code no tiene un agente primario por defecto, así que la orquestación vive aquí (memoria siempre activa) y en el subagente `.claude/agents/ptlc-orchestrator.md`:

- En la **sesión principal** actúas como `ptlc-orchestrator`: detectas el dominio en Phase 0 y, si es PTLC, ejecutas el pipeline cargando una skill por fase. Para orquestación no interactiva puedes delegar en el subagente.
- **Gates interactivos** (clarificación y aprobación de ejecución) los gestiona SIEMPRE la sesión principal: los subagentes de Claude Code no pueden preguntar al usuario. El subagente devuelve `needs_more_info`/`requires_approval` y la sesión principal pregunta.
- Dominio **no-PTLC**: se resuelve con los subagentes integrados de Claude Code (`general-purpose` para trabajo multi-paso, `Explore` para exploración) o desde el knowledge base.

Pipeline:

- **1 · `ptlc-intake`** — requisitos + selección de herramienta
- **2 · `ptlc-diagnostics`** — diagnóstico técnico + readiness
- **3 · `ptlc-procedure-plan`** — tipos de prueba, escenarios, workload model
- **4 · `ptlc-test-plan`** — plan formal ISTQB/IEEE-829
- **Approval Gate** — requiere aprobación explícita del usuario
- **5 · `ptlc-execution`** — scripts + ejecución
- **6 · `ptlc-analysis`** — métricas + RCA + reporte final

## Reglas obligatorias

- **`<pre_execution>`**: toda skill con esa sección DEBE leer con `read` lo que lista antes de producir output.
- **3 niveles**: `.claude/skills/README.md` (índice maestro) → `SKILL.md` de la skill → `NN_Tema.md` (autoritativo). Leer el Nivel 2 antes de editar un Nivel 3.
- **Edición**: Nivel 3 usa naming `NN_Topic_Name.md`. No duplicar docs: actualizar el existente. Al mover o renombrar, actualizar referencias en `.claude/skills/README.md` y el `SKILL.md` padre.
- **Catálogo**: el índice de skills (y herramientas en `ptlc-herramientas/`) está en `.claude/skills/README.md`.

## Eficiencia de lectura

- **Índice antes que documento**: dudas → `SKILL.md`/índice; detalle → `grep -n "^## "` + `read` por offset/limit. Nunca leer completo un doc >2.000 tokens.
- **Cheat sheets primero**: fórmulas/umbrales en `ptlc-metricas-kpis/00_Cheat_Sheet_Metricas.md`, `ptlc-workload-modeling/00_Cheat_Sheet_Workload.md` y `ptlc-herramientas/00b_Cheat_Sheet_Herramientas.md`; el doc completo, para API/sintaxis/ejemplos.
- **Envelope acumulado**: cada fase persiste su bloque en `tests/performance/{selected_tool}/{plan_id}/context_envelope.json`; las siguientes lo cargan y no releen lo ya sintetizado.

## Entregables

- `tests/performance/{selected_tool}/{plan_id}/plan.yaml` — plan activo (workflows resumibles)
- `tests/performance/{selected_tool}/{plan_id}/performance-test-plan.md` — plan de pruebas formal
- `tests/performance/{tool}/` — scripts generados
- `tests/performance/{selected_tool}/{plan_id}/performance-test-report.md` — reporte final con RCA y veredicto PASSED/FAILED

## Rutas clave

- `.claude/skills/README.md` — índice maestro
- `.claude/skills/ptlc-roadmap-decisiones/PRD.yaml` — requisitos de producto (Phase 0)
- `.claude/agents/ptlc-orchestrator.md` — subagente orquestador
- `.claude/settings.json` — permisos y configuración del harness
