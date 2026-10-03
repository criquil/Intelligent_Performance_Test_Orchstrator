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
| `ptlc-herramientas/SKILL.md` | Seleccionar herramienta según la matriz de decisión |
| `ptlc-herramientas/06_k6_Guia_Completa_Expandida.md` | Diseñar/generar pruebas con k6 |
| `ptlc-herramientas/05_JMeter_Guia_Completa.md` | Diseñar/generar pruebas con JMeter |
| `ptlc-herramientas/04_Gatling_Community_Guia_Completa.md` | Diseñar/generar pruebas con Gatling CE |
| `ptlc-herramientas/03_Locust_Guia_Completa.md` | Diseñar/generar pruebas con Locust |
| `ptlc-tipos-de-pruebas/` + `ptlc-workload-modeling/` | Estrategia: tipos de prueba, workload model, criterios |
| `ptlc-metricas-kpis/` | Análisis de percentiles, Apdex, throughput |
| `ptlc-analisis-bottlenecks/` | RCA técnico de bottlenecks |

## Entregables del PTLC

- `docs/plan/{plan_id}/plan.yaml` — estado del plan activo
- `docs/performance-test-plan.md` — plan de pruebas formal
- `tests/performance/{tool}/` — scripts de prueba
- `docs/performance-test-report.md` — reporte de resultados

## Commands
- No build, test, or lint pipeline is defined in this repository.
- Typical validation is link integrity and markdown consistency checks.

## Control de tokens

El presupuesto de tokens del knowledge base se mide con `scripts/measure_tokens.py` (Python 3, sin dependencias; estima tokens como `caracteres / 3.5`):

```bash
python scripts/measure_tokens.py           # reporte legible
python scripts/measure_tokens.py --strict  # falla (exit 1) si se supera algun presupuesto
python scripts/measure_tokens.py --json out.json
```

`--strict` valida los artefactos del knowledge base:

- contexto siempre activo (descripciones de skills + agentes + `CLAUDE.md` + `.claude/settings.json`) ≤ 1.500 tokens
- cuerpo de cada agente del pipeline (`ptlc-orchestrator.md`) ≤ 3.200 tokens
- índice de cada skill `ptlc-*` (`SKILL.md`) ≤ 2.000 tokens
- ningún documento de detalle > 6.000 tokens

El reporte también lista cuerpos de agentes e índices ordenados de mayor a menor, el top-20 de documentos de detalle, totales en KB y duplicados exactos y cerca-duplicados (Jaccard ≥ 0.30 sobre shingles de 8 palabras).
