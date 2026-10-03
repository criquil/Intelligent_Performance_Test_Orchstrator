# AGENTS Guide for This Repository

## Project Scope
- This repository is a documentation knowledge base for PTLC (Performance Test Life Cycle), organizado como skills bajo `.github/skills/`.
- Primary language is Spanish. Keep headings, summaries, and navigation text in Spanish.
- Main entry point: [.github/skills/README.md](../README.md) (índice maestro de skills).

## Navigation Contract (Read First)
- Use the navigation model defined in [.github/skills/README.md](../README.md):
  - **Nivel 1:** `.github/skills/README.md` — índice maestro y lookup por necesidad/keyword
  - **Nivel 2:** `SKILL.md` de cada skill temática — resumen del tema y tabla de contenido
  - **Nivel 3:** documentos detallados `NN_Tema.md` dentro de cada skill
- Before editing any content file, read the corresponding `SKILL.md` (Nivel 2) for scope and context.

## File Organization Rules
- Keep naming pattern `NN_Topic_Name.md` with zero-padded numeric prefix.
- New detailed documents (Nivel 3) must be added inside the correct thematic skill under `.github/skills/`.
- If you add, rename, or move files, update cross-references in:
  - [.github/skills/README.md](../README.md)
  - The corresponding `SKILL.md` (Nivel 2) of that skill

## Content Editing Rules
- Prefer updating existing docs over creating duplicates.
- Preserve section intent and hierarchy in each file.
- Use concise, actionable markdown and keep terminology consistent with the existing content.
- Use fenced code blocks with language identifiers when adding examples.

## Validation Checklist
- Verify modified links resolve as relative workspace paths.
- Ensure any new topic is discoverable from `.github/skills/README.md` and the parent `SKILL.md`.
- Confirm Spanish consistency in all newly added navigation and explanatory text.

## Agent Team

### Entry Point Obligatorio (v3.0)

`ptlc-orchestrator` es el **entry point obligatorio de todo request del usuario** y el orquestador del ciclo PTLC. Recibe toda solicitud, detecta el dominio y ejecuta el pipeline cargando las skills correspondientes. Las tareas generales (no-PTLC) se derivan al equipo `gem-*`.

| Agente | Archivo | Invocación | Rol |
|--------|---------|------------|-----|
| `ptlc-orchestrator` | `.github/agents/ptlc-orchestrator.agent.md` | **Primario — todo request** | Entry point obligatorio + orquestador del pipeline PTLC |
| `gem-orchestrator` | `.github/agents/gem-orchestrator.agent.md` | Derivado (tareas generales) | Orquestador del equipo gem-team para desarrollo general |

### Pipeline PTLC — Skills de fase (invocadas por ptlc-orchestrator)

| Skill | Archivo | Wave | Rol |
|-------|---------|------|-----|
| `ptlc-intake` | `.github/skills/ptlc-intake/SKILL.md` | 1 | Recopila requisitos y selecciona herramienta |
| `ptlc-diagnostics` | `.github/skills/ptlc-diagnostics/SKILL.md` | 2 | Diagnóstico técnico y readiness |
| `ptlc-procedure-plan` | `.github/skills/ptlc-procedure-plan/SKILL.md` | 3 | Plan de procedimiento y tipos de prueba |
| `ptlc-test-plan` | `.github/skills/ptlc-test-plan/SKILL.md` | 4 | Documento formal de plan de pruebas |
| `ptlc-execution` | `.github/skills/ptlc-execution/SKILL.md` | 5 | Scripts y ejecución (**requiere aprobación**) |
| `ptlc-analysis` | `.github/skills/ptlc-analysis/SKILL.md` | 6 | Análisis de resultados y reporte final |

### gem-team — Agentes de soporte general

Los agentes `gem-*` proveen capacidades generales (planificación, investigación, revisión, documentación). Se usan para tareas de desarrollo general o como apoyo del pipeline PTLC.

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
    └─ domain=general → deriva a gem-orchestrator (plan DAG con agentes gem-*)
```

### Skills operativas disponibles

| Skill | Disparador |
|-------|-----------|
| `performance-tool-selector` | Seleccionar herramienta según criterios técnicos |
| `k6-performance-workflow` | Diseñar/generar pruebas con k6 |
| `jmeter-performance-workflow` | Diseñar/generar pruebas con JMeter |
| `gatling-performance-workflow` | Diseñar/generar pruebas con Gatling CE |
| `locust-performance-workflow` | Diseñar/generar pruebas con Locust |
| `performance-test-strategy` | Estrategia: tipos de prueba, workload model, criterios |
| `performance-metrics-analysis` | Análisis de percentiles, Apdex, throughput |
| `performance-diagnostics-rca` | RCA técnico de bottlenecks |

## Entregables del PTLC

- `docs/plan/{plan_id}/plan.yaml` — estado del plan activo
- `docs/performance-test-plan.md` — plan de pruebas formal
- `tests/performance/{tool}/` — scripts de prueba
- `docs/performance-test-report.md` — reporte de resultados

## Commands
- No build, test, or lint pipeline is defined in this repository.
- Typical validation is link integrity and markdown consistency checks.
- APM binary: `~/.apm-bin/apm-windows-x86_64/apm.exe install` — reinstala dependencias APM.
