# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

This is the **Intelligent Performance Test Orchestrator v3** — an AI-agent knowledge platform for the Performance Test Life Cycle (PTLC). It is **not a traditional application**; it is a documentation knowledge base (~650 KB, 37 files) combined with agent/skill definitions that orchestrate performance testing workflows using the [gem-team](https://github.com/mubaidr/gem-team) framework.

**Primary language: Spanish** — all documentation, agent output, and navigation text must be in Spanish.

## Commands

There is no build/lint/test pipeline at the repository level.

**APM dependencies** (gem-team framework):
```
~/.apm-bin/apm-windows-x86_64/apm.exe install
```

**Gatling tests** (the only code component, under `tests/performance/gatling/`):
```bash
# Run default simulation
mvn clean test -Dgatling.simulationClass=simulations.SimpsonsBaselineSimulation

# Parameterized run
mvn clean test \
  -Dgatling.simulationClass=simulations.SimpsonsBaselineSimulation \
  -Dusers=50 -DrampUpSeconds=30 -DdurationSeconds=120 -DtargetHost=https://example.com
```
Requires Java 17+ and Maven. Reports land in `target/gatling/`.

## Architecture

### 3-Level Navigation Model

All knowledge lives under `DOCs/` and follows a strict hierarchy:
- **Level 1**: `README.md` — master index, keyword lookup, recommended reading paths
- **Level 2**: index files inside `DOCs/` category folders — scope and table of contents per category
- **Level 3**: detailed `.md` files inside subcategories — authoritative content

Always read the Level 2 index before editing any Level 3 content file.

### Knowledge Base Structure (DOCs/)

| Folder | Topic |
|--------|-------|
| `01_Introduccion_PTLC/` | Fundamentals, roles, ISO 25010 / ISTQB / TMMi standards |
| `02_Tipos_de_Pruebas/` | 22+ test types: Load, Stress, Soak, Spike, Baseline, Smoke, Capacity, Resiliency… |
| `03_Fases_del_PTLC/` | 6-phase lifecycle: Requirements → Planning → Design → Env Setup → Execution → Analysis |
| `04_Metricas_y_KPIs/` | p50/p90/p95/p99, Apdex, throughput, error rate, Little's Law formulas |
| `05_Herramientas/` | Complete guides for Locust (97 KB), Gatling (95 KB), JMeter (69 KB), k6 (73 KB) |
| `06_Workload_Modeling/` | Little's Law, VU calculation, load distributions, traffic patterns |
| `07_Entorno_y_Monitoreo/` | Prometheus, Grafana, OpenTelemetry, Jaeger, alerting |
| `08_Desarrollo_de_Scripts/` | Advanced scripting: correlation, token refresh, WebSocket, GraphQL |
| `09_Analisis_y_Bottlenecks/` | RCA: 5 Whys, Fishbone diagrams, DB query profiling |
| `10_Mejores_Practicas/` | CI/CD, shift-left, Kubernetes, microservices, AI/ML trends |

### Agent System (.github/agents/)

**Rule**: Every agent has a `<pre_execution>` section listing files it **must** `read` before producing output. Reading is mandatory, not optional.

**`gem-orchestrator` is the unified entry point (v2.0)** for all tasks — general development and performance testing. It detects performance testing intent in Phase 0 and builds a 6-wave PTLC plan delegating to `ptlc-*` agents directly.

**PTLC pipeline** (6-wave sequential DAG, orchestrated by `gem-orchestrator`):
```
gem-orchestrator (Phase 0: detects domain=performance-testing)
  → Wave 1: ptlc-intake          (requirements + tool selection)
  → Wave 2: ptlc-diagnostics     (technical diagnosis + readiness score)
  → Wave 3: ptlc-procedure-plan  (test types + workload model)
  → Wave 4: ptlc-test-plan       (formal ISTQB/IEEE-829 document)
  → Wave 5: ptlc-execution       (scripts + test run — requires user approval)
  → Wave 6: ptlc-analysis        (metrics + RCA + final report)
```

`ptlc-orchestrator` remains user-invocable as a convenience direct entry point to the PTLC pipeline.

**gem-team agents** (general dev support): `gem-planner`, `gem-researcher`, `gem-implementer`, `gem-reviewer`, `gem-debugger`, `gem-documentation-writer`, and others — all coordinated by `gem-orchestrator`.

### Skills (.github/skills/)

Eight reusable modules invocable from agents:

| Skill | Purpose |
|-------|---------|
| `performance-tool-selector` | Decision tree to pick the right tool |
| `k6-performance-workflow` | k6 test design and script generation |
| `jmeter-performance-workflow` | JMeter test design and script generation |
| `gatling-performance-workflow` | Gatling CE test design and script generation |
| `locust-performance-workflow` | Locust test design and script generation |
| `performance-test-strategy` | Test type selection, workload modeling, acceptance criteria |
| `performance-metrics-analysis` | Percentile analysis, Apdex, throughput interpretation |
| `performance-diagnostics-rca` | Root cause analysis of bottlenecks |

### Deliverables

Agents produce these artifacts in the workspace:

| Path | Content |
|------|---------|
| `docs/plan/{plan_id}/plan.yaml` | Active plan state (enables resumable workflows) |
| `docs/performance-test-plan.md` | Formal ISTQB/IEEE-829 test plan |
| `tests/performance/{tool}/` | Generated test scripts |
| `docs/performance-test-report.md` | Final analysis report with RCA and PASSED/FAILED verdict |

## File Organization Rules

- File naming pattern: `NN_Topic_Name.md` with zero-padded numeric prefix.
- New Level 3 documents go under the correct thematic subfolder in `DOCs/`.
- When adding, renaming, or moving files, update cross-references in `README.md` **and** the parent Level 2 index.
- Prefer updating existing docs over creating duplicates.

## Key Reference Files

- `DOCs/11_Arquitectura_y_Mapas/MAP.md` — visual architecture diagrams and agent-to-docs mapping
- `DOCs/11_Arquitectura_y_Mapas/AGENTS.md` — agent team guide (mirrors much of this file)
- `DOCs/12_Roadmap_y_Decisiones/ADR_001_ORCHESTRATOR_EVOLUTION.md` — v1.0 (CLI) → v2.0 (gem-orchestrator) decision record
- `DOCs/12_Roadmap_y_Decisiones/FRAMEWORK_v2_0_ROADMAP.md` — planned multi-tool parallelism and advanced RCA features
- `.gem-team.yaml` — team orchestration config (max 2 concurrent agents, Spanish output, knowledge base path)
