# Mapa de Agentes y Skills - Arquitectura de Ejecución v2.0

## 🤖 Diagrama: gem-orchestrator + Agentes PTLC + Skills + DOCs

```mermaid
graph TB
    subgraph "INPUT"
        U["👤 Usuario\nSolicitud de performance testing"]
    end

    subgraph "LAYER 1: ORCHESTRATION"
        GEM["🏆 gem-orchestrator\n(Entry point unificado v2.0)\nPhase 0: detecta dominio\nPhase 2: crea plan 6-wave"]
    end

    subgraph "LAYER 2: INTAKE & TOOL SELECTION"
        INTAKE["📋 ptlc-intake\nRecopila requisitos\nFormula preguntas estructuradas"]
        SKILL1["💡 SKILL: performance-tool-selector\nEvalúa: protocolo, complejidad,\nlenguaje equipo, tipo prueba\n→ Selecciona UNA herramienta"]
        DOC1["📚 DOCs 01, 02, 05, 06\nFundamentos · Tipos de prueba\nHerramientas · Workload modeling"]
    end

    subgraph "LAYER 3: DIAGNOSIS & PLANNING"
        DIAG["🔍 ptlc-diagnostics\nReadiness score · Riesgos"]
        PROC["📐 ptlc-procedure-plan\nTipos de prueba · Little's Law\nWorkload model"]
        TPLAN["📑 ptlc-test-plan\nDocumento ISTQB/IEEE-829"]
        SKILL2["💡 SKILL: performance-test-strategy\nSelección de tipos + workload"]
        DOC2["📚 DOCs 03, 06\nFases PTLC · Workload modeling"]
    end

    subgraph "LAYER 4: EXECUTION — on-demand"
        EXEC["⚡ ptlc-execution\n⚠️ Requiere aprobación usuario\nGenera scripts on-demand\npara herramienta seleccionada"]
        SKILL3["💡 SKILL: {herramienta}-performance-workflow\nk6 / jmeter / gatling / locust"]
        DOC3["📚 DOCs 05, 08\nGuía herramienta seleccionada\nScripting avanzado"]
        OUT_EXEC["📦 tests/performance/{tool}/{plan_id}/\nScripts + runner generados\nResultados de ejecución"]
    end

    subgraph "LAYER 5: ANALYSIS & RCA"
        ANAL["📊 ptlc-analysis\nMétricas · RCA · Veredicto"]
        SKILL4["💡 SKILL: performance-metrics-analysis\nPercentiles · Apdex · Throughput"]
        SKILL5["💡 SKILL: performance-diagnostics-rca\n5 Whys · Fishbone · Health scoring\nBottleneck ranking P1/P2/P3"]
        DOC4["📚 DOCs 04, 09\nMétricas exhaustivas\nRCA y troubleshooting"]
    end

    subgraph "OUTPUT"
        PLAN["📄 docs/performance-test-plan.md"]
        REPORT["📊 docs/performance-test-report.md"]
        STATE["💾 docs/plan/{plan_id}/plan.yaml"]
    end

    U --> GEM
    GEM --> INTAKE
    INTAKE --> SKILL1
    SKILL1 --> DOC1

    SKILL1 --> DIAG
    DIAG --> PROC
    PROC --> SKILL2
    SKILL2 --> DOC2
    PROC --> TPLAN
    TPLAN --> PLAN

    TPLAN --> EXEC
    EXEC --> SKILL3
    SKILL3 --> DOC3
    EXEC --> OUT_EXEC

    OUT_EXEC --> ANAL
    ANAL --> SKILL4
    ANAL --> SKILL5
    SKILL4 --> DOC4
    SKILL5 --> DOC4
    ANAL --> REPORT

    GEM --> STATE

    style U fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    style GEM fill:#c8e6c9,stroke:#1b5e20,stroke-width:3px
    style EXEC fill:#ffccbc,stroke:#bf360c,stroke-width:2px
    style SKILL1 fill:#c8e6c9,stroke:#1b5e20,stroke-width:2px
    style SKILL2 fill:#c8e6c9,stroke:#1b5e20,stroke-width:2px
    style SKILL3 fill:#c8e6c9,stroke:#1b5e20,stroke-width:2px
    style SKILL4 fill:#c8e6c9,stroke:#1b5e20,stroke-width:2px
    style SKILL5 fill:#c8e6c9,stroke:#1b5e20,stroke-width:2px
    style REPORT fill:#81c784,stroke:#1b5e20,stroke-width:3px
```

---

## 📊 Matriz de Agentes vs Fases PTLC

| Agente | Wave | Entradas | Salidas |
|--------|------|----------|---------|
| `ptlc-intake` | 1 | Request del usuario, DOCs 01/02/05/06 | Requisitos estructurados, herramienta seleccionada |
| `ptlc-diagnostics` | 2 | Requisitos, entorno | Readiness score, riesgos identificados |
| `ptlc-procedure-plan` | 3 | Requisitos, diagnóstico, DOCs 06 | Tipos de prueba, workload model (Little's Law) |
| `ptlc-test-plan` | 4 | Procedure plan, DOCs 03 | `docs/performance-test-plan.md` (ISTQB/IEEE-829) |
| `ptlc-execution` | 5 | Test plan, **aprobación usuario** | Scripts on-demand en `tests/performance/{tool}/{plan_id}/`, resultados |
| `ptlc-analysis` | 6 | Resultados de ejecución, DOCs 04/09 | `docs/performance-test-report.md`, RCA, veredicto |

---

## 📚 DOCs Integration Points

| DOC | Documento | Agentes que lo usan |
|-----|-----------|---------------------|
| 01 | `Definicion_y_Fundamentos.md` | ptlc-intake |
| 02 | `Tipos de Pruebas` | ptlc-intake, ptlc-procedure-plan |
| 03 | `Fases_del_PTLC` | ptlc-test-plan |
| 04 | `Metricas_Exhaustivas.md` | ptlc-analysis |
| 05 | `Herramientas` (k6/JMeter/Gatling/Locust) | ptlc-intake, ptlc-execution |
| 06 | `Workload_Modeling_Exhaustivo.md` | ptlc-procedure-plan |
| 08 | `Scripting_Avanzado.md` | ptlc-execution |
| 09 | `RCA_y_Troubleshooting.md` | ptlc-analysis |
| 10 | `CICD_y_Tendencias_Futuras.md` | ptlc-analysis (roadmap) |

---

## 🔗 Flujo de Control: gem-orchestrator → Agentes → Skills → DOCs

```
USUARIO
    ↓
gem-orchestrator (Phase 0: detecta dominio performance-testing)
    ↓
gem-orchestrator (Phase 2: genera plan 6-wave PTLC)
    ↓ persiste → docs/plan/{plan_id}/plan.yaml

    WAVE 1 → ptlc-intake
        ├─ Lee DOCs 01, 02, 05, 06
        ├─ Formula preguntas al usuario
        ├─ Invoca SKILL: performance-tool-selector
        └─ → Herramienta seleccionada (UNA: k6/JMeter/Gatling/Locust)

    WAVE 2 → ptlc-diagnostics
        ├─ Evalúa entorno y dependencias
        └─ → Readiness score + riesgos

    WAVE 3 → ptlc-procedure-plan
        ├─ Lee DOCs 06 (Workload Modeling)
        ├─ Aplica Little's Law
        └─ → Tipos de prueba + modelo de carga

    WAVE 4 → ptlc-test-plan
        ├─ Lee DOCs 03 (Fases PTLC)
        └─ → docs/performance-test-plan.md

    ⚠️ APPROVAL GATE (gem-orchestrator pide confirmación explícita)

    WAVE 5 → ptlc-execution (solo con aprobación)
        ├─ Lee DOCs 05 (guía herramienta), 08 (scripting)
        ├─ Invoca SKILL: {herramienta}-performance-workflow
        ├─ Genera scripts on-demand en tests/performance/{tool}/{plan_id}/
        └─ → Resultados de ejecución

    WAVE 6 → ptlc-analysis
        ├─ Lee DOCs 04 (métricas), 09 (RCA)
        ├─ Invoca SKILL: performance-metrics-analysis
        ├─ Invoca SKILL: performance-diagnostics-rca
        └─ → docs/performance-test-report.md + veredicto
```

---

## 🎯 Skills por Agente

### gem-orchestrator
- Domain detection (Phase 0)
- Plan generation (Phase 2) — PTLC 6-wave template
- Approval gate (Phase 3B)

### ptlc-intake
- `performance-tool-selector` — evalúa protocolo, complejidad, lenguaje, tipo prueba → selecciona UNA herramienta

### ptlc-procedure-plan
- `performance-test-strategy` — selección de tipos de prueba + Little's Law workload model

### ptlc-execution
- `{herramienta}-performance-workflow` (k6 / jmeter / gatling / locust) — generación de scripts y ejecución

### ptlc-analysis
- `performance-metrics-analysis` — percentiles, Apdex, throughput, error rate
- `performance-diagnostics-rca` — 5 Whys, Fishbone, health scoring, bottleneck ranking P1/P2/P3

---

## ✅ Principios de Arquitectura v2.0

| Principio | Implementación |
|-----------|----------------|
| Entry point único | `gem-orchestrator` recibe todos los requests |
| Una herramienta por ciclo | `ptlc-intake` selecciona UNA herramienta; nunca paralelo |
| Generación on-demand | Scripts generados en Wave 5 — no existen pre-creados |
| Aprobación explícita | `ptlc-execution` no corre sin confirmación del usuario |
| Resultados individuales | Cada ejecución es independiente; no hay comparación cross-tool |
| Estado persistido | `docs/plan/{plan_id}/plan.yaml` guarda el estado de cada ciclo |
| DOCs como fuente de verdad | Cada agente lee los DOCs relevantes antes de actuar |
| Outputs en español | Todos los reportes, planes y comunicaciones en español |
