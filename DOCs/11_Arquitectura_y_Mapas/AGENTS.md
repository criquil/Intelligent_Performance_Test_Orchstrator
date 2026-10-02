# AGENTS Guide for This Repository

## Project Scope
- This repository is a documentation knowledge base for PTLC (Performance Test Life Cycle).
- Primary language is Spanish. Keep headings, summaries, and navigation text in Spanish.
- Main entry point: [README.md](README.md).

## Navigation Contract (Read First)
- Use the 3-level navigation model defined in [README.md](README.md):
  - Nivel 1: [README.md](README.md)
  - Nivel 2: index files in [DOCs](DOCs)
  - Nivel 3: detailed files inside subfolders under [DOCs](DOCs)
- Before editing any content file, read the corresponding Nivel 2 index for scope and context.

## File Organization Rules
- Keep naming pattern `NN_Topic_Name.md` with zero-padded numeric prefix.
- New detailed documents (Nivel 3) must be added under the correct thematic subfolder in [DOCs](DOCs).
- If you add, rename, or move files, update cross-references in:
  - [README.md](README.md)
  - The corresponding Nivel 2 index in [DOCs](DOCs)

## Content Editing Rules
- Prefer updating existing docs over creating duplicates.
- Preserve section intent and hierarchy in each file.
- Use concise, actionable markdown and keep terminology consistent with the existing content.
- Use fenced code blocks with language identifiers when adding examples.

## Validation Checklist
- Verify modified links resolve as relative workspace paths.
- Ensure any new topic is discoverable from [README.md](README.md) and the parent Nivel 2 index.
- Confirm Spanish consistency in all newly added navigation and explanatory text.

## Agent Team

### Entry Point Unificado (v2.0)

`gem-orchestrator` es el **orquestador central** para todos los tasks. Detecta automáticamente la intención de performance testing y construye el plan PTLC de 6 fases delegando a los agentes `ptlc-*`.

| Agente | Archivo | Invocación | Rol |
|--------|---------|------------|-----|
| `gem-orchestrator` | `.github/agents/gem-orchestrator.agent.md` | **Primario** (user-invocable) | Orquestador central: tasks generales + PTLC |
| `ptlc-orchestrator` | `.github/agents/ptlc-orchestrator.agent.md` | Directo (conveniencia) | Entry point PTLC dedicado (acceso directo) |

### Pipeline PTLC — Subagentes especializados

| Agente | Archivo | Wave | Rol |
|--------|---------|------|-----|
| `ptlc-intake` | `.github/agents/ptlc-intake.agent.md` | 1 | Recopila requisitos y selecciona herramienta |
| `ptlc-diagnostics` | `.github/agents/ptlc-diagnostics.agent.md` | 2 | Diagnóstico técnico y readiness |
| `ptlc-procedure-plan` | `.github/agents/ptlc-procedure-plan.agent.md` | 3 | Plan de procedimiento y tipos de prueba |
| `ptlc-test-plan` | `.github/agents/ptlc-test-plan.agent.md` | 4 | Documento formal de plan de pruebas |
| `ptlc-execution` | `.github/agents/ptlc-execution.agent.md` | 5 | Scripts y ejecución (**requiere aprobación**) |
| `ptlc-analysis` | `.github/agents/ptlc-analysis.agent.md` | 6 | Análisis de resultados y reporte final |

### gem-team — Agentes de soporte general

Los agentes `gem-*` proveen capacidades generales (planificación, investigación, revisión, documentación) y son orquestados por `gem-orchestrator` para tasks de desarrollo general o como apoyo en el pipeline PTLC.

### Flujo v2.0 — gem-orchestrator como coordinador central

```
Usuario (cualquier tarea)
    ↓
gem-orchestrator (Phase 0: detecta dominio + clasifica complejidad)
    │
    ├─ Si domain=performance-testing → construye plan PTLC 6-wave
    │       ↓
    │  Wave 1: ptlc-intake       (requisitos + tool selection)
    │       ↓
    │  Wave 2: ptlc-diagnostics  (diagnóstico técnico)
    │       ↓
    │  Wave 3: ptlc-procedure-plan (tipos de prueba + workload model)
    │       ↓
    │  Wave 4: ptlc-test-plan    (documento formal ISTQB/IEEE-829)
    │       ↓
    │  Wave 5: ptlc-execution    (scripts + ejecución — requiere aprobación usuario)
    │       ↓
    │  Wave 6: ptlc-analysis     (resultados + RCA + reporte)
    │
    └─ Si domain=general → plan DAG con gem-* agents
```

**Acceso directo (conveniencia):** Para ir directamente al pipeline PTLC sin pasar por gem-orchestrator, invocar `ptlc-orchestrator` directamente.

### Skills Disponibles (invocables desde agentes)

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