# Guía de convenciones del repositorio

## Project Scope
- This repository is a documentation knowledge base for PTLC (Performance Test Life Cycle), organizado como skills bajo `.claude/skills/`.
- Primary language is Spanish. Keep headings, summaries, and navigation text in Spanish.
- Main entry point: [.claude/skills/README.md](../README.md) (índice maestro de skills).

## Navigation Contract (Read First)
- Use the navigation model defined in [.claude/skills/README.md](../README.md):
  - **Nivel 1:** `.claude/skills/README.md` — índice maestro y lookup por necesidad/keyword
  - **Nivel 2:** `SKILL.md` de cada skill temática — resumen del tema y tabla de contenido
  - **Nivel 3:** documentos detallados `NN_Tema.md` dentro de cada skill
- Before editing any content file, read the corresponding `SKILL.md` (Nivel 2) for scope and context.

## File Organization Rules
- Keep naming pattern `NN_Topic_Name.md` with zero-padded numeric prefix.
- New detailed documents (Nivel 3) must be added inside the correct thematic skill under `.claude/skills/`.
- If you add, rename, or move files, update cross-references in:
  - [.claude/skills/README.md](../README.md)
  - The corresponding `SKILL.md` (Nivel 2) of that skill

## Content Editing Rules
- Prefer updating existing docs over creating duplicates.
- Preserve section intent and hierarchy in each file.
- Use concise, actionable markdown and keep terminology consistent with the existing content.
- Use fenced code blocks with language identifiers when adding examples.

## Validation Checklist
- Verify modified links resolve as relative workspace paths.
- Ensure any new topic is discoverable from `.claude/skills/README.md` and the parent `SKILL.md`.
- Confirm Spanish consistency in all newly added navigation and explanatory text.

## Agent Team

### Entry Point Obligatorio (v3.0)

`ptlc-orchestrator` es el **entry point obligatorio de todo request del usuario** y el orquestador del ciclo PTLC. Recibe toda solicitud, detecta el dominio y ejecuta el pipeline cargando las skills correspondientes. Las tareas generales (no-PTLC) se resuelven con los subagentes integrados de Claude Code (`general-purpose`/`Explore`).

| Agente | Archivo | Invocación | Rol |
|--------|---------|------------|-----|
| `ptlc-orchestrator` | `CLAUDE.md` + `.claude/agents/ptlc-orchestrator.md` | **Entry point — todo request** | Orquestador del pipeline PTLC (memoria + subagente) |

### Pipeline PTLC — Skills de fase (invocadas por ptlc-orchestrator)

| Skill | Archivo | Wave | Rol |
|-------|---------|------|-----|
| `ptlc-intake` | `.claude/skills/ptlc-intake/SKILL.md` | 1 | Recopila requisitos y selecciona herramienta |
| `ptlc-diagnostics` | `.claude/skills/ptlc-diagnostics/SKILL.md` | 2 | Diagnóstico técnico y readiness |
| `ptlc-procedure-plan` | `.claude/skills/ptlc-procedure-plan/SKILL.md` | 3 | Plan de procedimiento y tipos de prueba |
| `ptlc-test-plan` | `.claude/skills/ptlc-test-plan/SKILL.md` | 4 | Documento formal de plan de pruebas |
| `ptlc-execution` | `.claude/skills/ptlc-execution/SKILL.md` | 5 | Scripts y ejecución (**requiere aprobación**) |
| `ptlc-analysis` | `.claude/skills/ptlc-analysis/SKILL.md` | 6 | Análisis de resultados y reporte final |

### Subagentes integrados — Soporte general

Para tareas generales (no-PTLC) o apoyo transversal se usan los subagentes integrados de Claude Code: `general-purpose` (trabajo multi-paso) y `Explore` (exploración del repo). Cuando no hace falta delegar, el propio `ptlc-orchestrator` o el knowledge base resuelven la consulta.

### Flujo v3.0 — ptlc-orchestrator como entry point

```
Usuario (cualquier request)
    ↓
ptlc-orchestrator (Phase 0: detecta dominio + clasifica complejidad)
    │
    ├─ domain=performance-testing → pipeline PTLC 6-wave (skills ptlc-*)
    │       Wave 1: ptlc-intake          (requisitos + tool selection)
    │       Wave 2: ptlc-diagnostics     (diagnóstico técnico)
    │       Wave 3: ptlc-procedure-plan  (tipos de prueba + workload model)
    │       Wave 4: ptlc-test-plan       (documento formal ISTQB/IEEE-829)
    │       ⚠️ Approval Gate — aprobación explícita del usuario
    │       Wave 5: ptlc-execution       (scripts + ejecución)
    │       Wave 6: ptlc-analysis        (resultados + RCA + reporte)
    │
    └─ domain=general → subagentes integrados (`general-purpose`/`Explore`) o knowledge base
```

### Guías operativas por herramienta

El diseño, scripting y ejecución de cada herramienta se cubren en `.claude/skills/ptlc-herramientas/`:

| Guía | Disparador |
|------|-----------|
| `ptlc-herramientas/SKILL.md` + `00b_Cheat_Sheet_Herramientas.md` | Seleccionar herramienta según la matriz de decisión (única referencia central) |
| Documentación oficial de cada herramienta | Diseñar/generar pruebas con k6, JMeter, Gatling CE, Locust (consultar docs oficiales) |
| `ptlc-tipos-de-pruebas/` + `ptlc-workload-modeling/` | Estrategia: tipos de prueba, workload model, criterios |
| `ptlc-metricas-kpis/` | Análisis de percentiles, Apdex, throughput |
| `ptlc-analisis-bottlenecks/` | RCA técnico de bottlenecks |

## Entregables del PTLC

- `tests/performance/{selected_tool}/{plan_id}/plan.yaml` — estado del plan activo
- `tests/performance/{selected_tool}/{plan_id}/performance-test-plan.md` — plan de pruebas formal
- `tests/performance/{tool}/` — scripts de prueba
- `tests/performance/{selected_tool}/{plan_id}/performance-test-report.md` — reporte de resultados

## Commands
- No build, test, or lint pipeline is defined in this repository.
- Typical validation is link integrity and markdown consistency checks.

## Control de contexto

No hay medidor automático de tokens. El ahorro de contexto se gobierna con disciplina de lectura:

- índice antes que documento: dudas → `SKILL.md`; detalle → `grep -n "^## "` + `read` por `offset/limit`
- detalle grande → mapa de secciones + lectura acotada por sección/línea en `<pre_execution>`
- fórmulas y umbrales → las 3 cheat sheets antes que el documento completo
- `context_envelope.json` para no releer lo ya sintetizado por otra fase
