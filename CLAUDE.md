# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

This is the **Intelligent Performance Test Orchestrator v3** — an AI-agent knowledge platform for the Performance Test Life Cycle (PTLC). It is **not a traditional application**; it is a documentation knowledge base (~650 KB, 48 documents) organized as skills under `.github/skills/`, combined with agent definitions that orchestrate performance testing workflows using the [gem-team](https://github.com/mubaidr/gem-team) framework.

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

### Entry Point (v3.0)

**`ptlc-orchestrator` is the mandatory entry point for every user request.** It orchestrates the 6-phase PTLC pipeline by loading one skill per phase, and derives non-PTLC general tasks to the `gem-*` team (`gem-orchestrator`).

### 3-Level Navigation Model

All knowledge lives under `.github/skills/` as skills organized by topic:
- **Level 1**: `.github/skills/README.md` — master index, keyword lookup, recommended reading paths
- **Level 2**: `SKILL.md` inside each thematic skill — scope and table of contents per topic
- **Level 3**: detailed `NN_Tema.md` files inside each skill — authoritative content

Always read the Level 2 `SKILL.md` before editing any Level 3 content file.

### Knowledge Base Structure (`.github/skills/`)

| Skill | Topic |
|-------|-------|
| `ptlc-fundamentos/` | Fundamentals, roles, ISO 25010 / ISTQB / TMMi standards |
| `ptlc-tipos-de-pruebas/` | 22+ test types: Load, Stress, Soak, Spike, Baseline, Smoke, Capacity, Resiliency… |
| `ptlc-fases-del-ciclo/` | 9-phase lifecycle: Requirements → Planning → Design → Env Setup → Execution → Analysis → Closure |
| `ptlc-metricas-kpis/` | p50/p90/p95/p99, Apdex, throughput, error rate, Little's Law formulas |
| `ptlc-herramientas/` | Complete guides for Locust (97 KB), Gatling (95 KB), JMeter (69 KB), k6 (73 KB) |
| `ptlc-workload-modeling/` | Little's Law, VU calculation, load distributions, traffic patterns |
| `ptlc-monitoreo/` | Prometheus, Grafana, OpenTelemetry, Jaeger, alerting |
| `ptlc-scripting/` | Advanced scripting: correlation, token refresh, WebSocket, GraphQL |
| `ptlc-analisis-bottlenecks/` | RCA: 5 Whys, Fishbone diagrams, DB query profiling |
| `ptlc-mejores-practicas/` | CI/CD, shift-left, Kubernetes, microservices, AI/ML trends |
| `ptlc-arquitectura-mapas/` | Architecture maps and `AGENTS.md` conventions |
| `ptlc-roadmap-decisiones/` | ADRs, v2.0 roadmap, implementation plan, `PRD.yaml` |

### Agent System (`.github/agents/`)

**Rule**: Every agent has a `<pre_execution>` section listing files it **must** `read` before producing output. Reading is mandatory, not optional.

**`ptlc-orchestrator` is the mandatory entry point (v3.0)** — it receives every user request, detects performance testing intent in Phase 0, and drives the 6-wave PTLC pipeline by loading one skill per wave:

```
ptlc-orchestrator (Phase 0: detects domain=performance-testing)
  → Wave 1: skill ptlc-intake          (requirements + tool selection)
  → Wave 2: skill ptlc-diagnostics     (technical diagnosis + readiness score)
  → Wave 3: skill ptlc-procedure-plan  (test types + workload model)
  → Wave 4: skill ptlc-test-plan       (formal ISTQB/IEEE-829 document)
  → ⚠️ Approval Gate (explicit user approval required)
  → Wave 5: skill ptlc-execution       (scripts + test run)
  → Wave 6: skill ptlc-analysis        (metrics + RCA + final report)
```

Requests that are not performance-testing related are derived to `gem-orchestrator`.

**gem-team agents** (general dev support): `gem-planner`, `gem-researcher`, `gem-implementer`, `gem-reviewer`, `gem-debugger`, `gem-documentation-writer`, and others — coordinated by `gem-orchestrator`.

### Skills (`.github/skills/`)

Twenty-six skills in total:

**Pipeline skills (6)** — one per PTLC phase, loaded by `ptlc-orchestrator`:

| Skill | Purpose |
|-------|---------|
| `ptlc-intake` | Requirements gathering and tool selection |
| `ptlc-diagnostics` | Technical diagnosis and readiness score |
| `ptlc-procedure-plan` | Test types, scenarios and workload model |
| `ptlc-test-plan` | Formal test plan document (ISTQB/IEEE-829) |
| `ptlc-execution` | Script generation and test execution (requires approval) |
| `ptlc-analysis` | Metrics, RCA and final report |

**Operational skills (8)**:

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

**Knowledge skills (12)** — the former `DOCs/` knowledge base, one skill per topic (see table above).

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
- New Level 3 documents go inside the correct thematic skill under `.github/skills/`.
- When adding, renaming, or moving files, update cross-references in `.github/skills/README.md` **and** the parent `SKILL.md`.
- Prefer updating existing docs over creating duplicates.

## Key Reference Files

- `.github/skills/README.md` — master index of the whole knowledge base
- `.github/skills/ptlc-arquitectura-mapas/MAP.md` — visual architecture diagrams and agent-to-docs mapping
- `.github/skills/ptlc-arquitectura-mapas/AGENTS.md` — agent team guide (mirrors much of this file)
- `.github/skills/ptlc-roadmap-decisiones/ADR_001_ORCHESTRATOR_EVOLUTION.md` — v1.0 (CLI) → v2.0 (gem-orchestrator) decision record
- `.github/skills/ptlc-roadmap-decisiones/FRAMEWORK_v2_0_ROADMAP.md` — planned multi-tool parallelism and advanced RCA features
- `.github/skills/ptlc-roadmap-decisiones/PRD.yaml` — product requirements (read in Phase 0)
- `.gem-team.yaml` — team orchestration config (max 2 concurrent agents, Spanish output, knowledge base path)
