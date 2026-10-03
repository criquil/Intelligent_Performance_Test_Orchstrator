# 🗺️ MAP — Intelligent Performance Test Orchestrator

> Mapa único de la arquitectura v3.0: estructura del repo, pipeline de agentes, cobertura del knowledge base, entregables y tiempos.
> Convenciones y reglas de navegación del repo en [AGENTS.md](AGENTS.md). Pipeline por fases en [`../ptlc-fases-del-ciclo/`](../ptlc-fases-del-ciclo/SKILL.md).

## Índice

1. [Arquitectura general](#1-arquitectura-general)
2. [Pipeline v3.0: ptlc-orchestrator como entry point obligatorio](#2-pipeline-v30-ptlc-orchestrator-como-entry-point-obligatorio)
3. [Fases del pipeline: lecturas, procesos y salidas](#3-fases-del-pipeline-lecturas-procesos-y-salidas)
4. [Guías por agente](#4-guías-por-agente)
5. [Principios de arquitectura y decisiones críticas](#5-principios-de-arquitectura-y-decisiones-críticas)
6. [Selección de herramienta de prueba](#6-selección-de-herramienta-de-prueba)
7. [Cobertura del knowledge base por fase](#7-cobertura-del-knowledge-base-por-fase)
8. [Estructura de archivos](#8-estructura-de-archivos)
9. [Modelo de navegación: 3 niveles](#9-modelo-de-navegación-3-niveles)
10. [Entregables y artefactos por ciclo](#10-entregables-y-artefactos-por-ciclo)
11. [Tiempos estimados por fase](#11-tiempos-estimados-por-fase)

---

## 1. Arquitectura general

```mermaid
graph TB
    subgraph ROOT["📁 Raíz del Proyecto"]
        CLAUDE["📄 AGENTS.md\nGuía para agentes AI"]
    end

    subgraph SKILLS_ROOT["📂 .opencode/skills/ — Knowledge Base PTLC"]
        direction TB
        IDX["📄 README.md\nÍndice maestro · Punto de entrada"]
        D01["📂 ptlc-fundamentos"]
        D02["📂 ptlc-tipos-de-pruebas"]
        D03["📂 ptlc-fases-del-ciclo"]
        D04["📂 ptlc-metricas-kpis"]
        D05["📂 ptlc-herramientas"]
        D06["📂 ptlc-workload-modeling"]
        D07["📂 ptlc-monitoreo"]
        D08["📂 ptlc-scripting"]
        D09["📂 ptlc-analisis-bottlenecks"]
        D10["📂 ptlc-mejores-practicas"]
        D11["📂 ptlc-arquitectura-mapas"]
        D12["📂 ptlc-roadmap-decisiones"]
    end

    subgraph GITHUB["📂 .opencode/"]
        subgraph AGENTS["📂 agents/ — 1 agente"]
            PTLC_ORCH["🎯 ptlc-orchestrator\n(ENTRY POINT OBLIGATORIO v3.0)"]
        end
        subgraph SKILLS["📂 skills/ — 18 skills ptlc-*"]
            PIPE["⚙️ 6 skills pipeline PTLC\nintake · diagnostics · procedure\nplan · execution · analysis"]
            OPS["🛠️ Guías operativas por herramienta\nptlc-herramientas/ (k6 · JMeter\nGatling · Locust)"]
        end
    end

    IDX --> D01
    IDX --> D12
    CLAUDE --> SKILLS_ROOT
    PTLC_ORCH --> PIPE
    PIPE --> OPS
```

---

## 2. Pipeline v3.0: ptlc-orchestrator como entry point obligatorio

```mermaid
flowchart TD
    USER(["👤 Usuario\n'Necesito probar mi API'\nO cualquier request"])

    PTLC_ORCH["🎯 ptlc-orchestrator\nENTRY POINT OBLIGATORIO\nPhase 0: detecta dominio + clasifica\nPersiste plan en docs/plan/"]

    DOMAIN{{"¿Dominio detectado?"}}

    subgraph PTLC_FLOW["📊 Pipeline PTLC — skills ptlc-*"]
        direction TB
        F1["Wave 1 · skill ptlc-intake\nRequisitos + tool selection"]
        F2["Wave 2 · skill ptlc-diagnostics\nReadiness Score · Riesgos"]
        F3["Wave 3 · skill ptlc-procedure-plan\nTipos de prueba · Workload Model"]
        F4["Wave 4 · skill ptlc-test-plan\nDocumento ISTQB/IEEE-829"]
        F5["Wave 5 · skill ptlc-execution\n⚠️ Requiere aprobación usuario\nGenera scripts + ejecuta"]
        F6["Wave 6 · skill ptlc-analysis\nMétricas · RCA · Veredicto"]
        F1 --> F2 --> F3 --> F4 --> F5 --> F6
    end

    GEN_FLOW["🛠️ Soporte general — subagentes integrados\n`general` (multi-paso) · `explore` (exploración)"]

    OUT_PTLC(["📦 Entregables PTLC\n• docs/performance-test-plan.md\n• tests/performance/{tool}/\n• docs/performance-test-report.md"])
    OUT_GEN(["📦 Entregables generales\n• código · documentación · tests"])

    USER --> PTLC_ORCH
    PTLC_ORCH --> DOMAIN
    DOMAIN -->|performance-testing| PTLC_FLOW
    DOMAIN -->|general| GEN_FLOW
    PTLC_FLOW --> OUT_PTLC
    GEN_FLOW --> OUT_GEN

    F5 -->|approval gate: aprobado| USER
    F5 -->|approval gate: rechazado| PAUSE["🛑 Ciclo pausado\n(no se ejecuta)"]
    USER -->|confirmación explícita| F5
```

---

## 3. Fases del pipeline: lecturas, procesos y salidas

| # | Skill | Entrada | Lecturas del knowledge base | Proceso | Salida / artefacto |
|---|-------|---------|------------------------------|---------|--------------------|
| 0 | `ptlc-orchestrator` | Request del usuario | PRD (`ptlc-roadmap-decisiones`) | Detección de dominio + plan 6-wave | `docs/plan/{plan_id}/plan.yaml` |
| 1 | `ptlc-intake` | Solicitud | `ptlc-fundamentos`, `ptlc-tipos-de-pruebas`, `ptlc-herramientas` (matriz de decisión), `ptlc-workload-modeling` | Preguntas estructuradas + selección de UNA herramienta | Requisitos completos + herramienta elegida |
| 2 | `ptlc-diagnostics` | Requisitos, entorno | `ptlc-fases-del-ciclo` (readiness), `ptlc-metricas-kpis`, `ptlc-workload-modeling`, `ptlc-monitoreo`, `ptlc-mejores-practicas` | Evaluación de entorno y dependencias | Readiness score + riesgos |
| 3 | `ptlc-procedure-plan` | Requisitos + diagnóstico | `ptlc-tipos-de-pruebas`, `ptlc-workload-modeling` (Little's Law), `ptlc-metricas-kpis` | Tipos de prueba + modelo de carga | Workload model + tipos seleccionados |
| 4 | `ptlc-test-plan` | Procedure plan | `ptlc-fundamentos`, `ptlc-fases-del-ciclo` (planificación) | Redacción ISTQB/IEEE-829 | `docs/performance-test-plan.md` |
| — | **APPROVAL GATE** | Plan completo | — | `ptlc-orchestrator` presenta el plan y espera confirmación explícita | Aprobado → Wave 5 · rechazado → ciclo pausado |
| 5 | `ptlc-execution` | Test plan aprobado | `ptlc-herramientas` (guía de la herramienta), `ptlc-scripting`, `ptlc-fases-del-ciclo` | Generación on-demand de scripts + ejecución | Scripts + resultados en `tests/performance/{tool}/{plan_id}/` |
| 6 | `ptlc-analysis` | Resultados de ejecución | `ptlc-metricas-kpis`, `ptlc-analisis-bottlenecks`, `ptlc-fases-del-ciclo` (análisis y cierre), `ptlc-monitoreo` | Métricas + RCA + health scoring | `docs/performance-test-report.md` + veredicto PASSED/FAILED |

---

## 4. Guías por agente

| Agente | Guías que debe leer |
|--------|--------------------|
| `ptlc-orchestrator` | Detección de dominio (Phase 0), generación de plan 6-wave (Phase 2), approval gate (Phase 3B) |
| `ptlc-intake` | [`ptlc-herramientas/SKILL.md`](../ptlc-herramientas/SKILL.md) — protocolo, complejidad, lenguaje, tipo de prueba → selecciona UNA herramienta |
| `ptlc-diagnostics` | Checklist de readiness de [`ptlc-fases-del-ciclo/SKILL.md`](../ptlc-fases-del-ciclo/SKILL.md) |
| `ptlc-procedure-plan` | [`ptlc-tipos-de-pruebas/SKILL.md`](../ptlc-tipos-de-pruebas/SKILL.md) + [`ptlc-workload-modeling/SKILL.md`](../ptlc-workload-modeling/SKILL.md) — tipos de prueba + Little's Law |
| `ptlc-test-plan` | [`ptlc-fundamentos/SKILL.md`](../ptlc-fundamentos/SKILL.md) + template ISTQB/IEEE-829 de [`ptlc-fases-del-ciclo/`](../ptlc-fases-del-ciclo/SKILL.md) |
| `ptlc-execution` | Guía de la herramienta en [`ptlc-herramientas/`](../ptlc-herramientas/SKILL.md) (k6 / JMeter / Gatling / Locust) + [`ptlc-scripting/`](../ptlc-scripting/SKILL.md) |
| `ptlc-analysis` | [`ptlc-metricas-kpis/SKILL.md`](../ptlc-metricas-kpis/SKILL.md) — percentiles, Apdex, throughput, error rate · [`ptlc-analisis-bottlenecks/SKILL.md`](../ptlc-analisis-bottlenecks/SKILL.md) — 5 Whys, Fishbone, health scoring, ranking P1/P2/P3 |

---

## 5. Principios de arquitectura y decisiones críticas

| Principio | Implementación |
|-----------|----------------|
| Entry point único | `ptlc-orchestrator` recibe todos los requests; resuelve los no-PTLC con los subagentes integrados (`general`/`explore`) o el knowledge base |
| Una herramienta por ciclo | `ptlc-intake` selecciona UNA herramienta; nunca paralelo |
| Generación on-demand | Scripts generados en Wave 5 — no existen pre-creados |
| Aprobación explícita | `ptlc-execution` no corre sin confirmación del usuario |
| Resultados individuales | Cada ejecución es independiente; no hay comparación cross-tool |
| Estado persistido | `docs/plan/{plan_id}/plan.yaml` guarda el estado de cada ciclo |
| Knowledge Base como fuente de verdad | Cada agente lee los documentos relevantes antes de actuar |
| Outputs en español | Todos los reportes, planes y comunicaciones en español |

| Decisión | Valor | Justificación |
|----------|-------|---------------|
| Script generation | On-demand en Wave 5 | No existen scripts pre-creados; se generan para cada request |
| Output path | `tests/performance/{tool}/{plan_id}/` | Organización por herramienta y ciclo para trazabilidad |
| State persistence | `docs/plan/{plan_id}/plan.yaml` | Permite retomar ciclos interrumpidos |
| Approval gate | Requerida antes de ejecutar | `ptlc-execution` tiene impacto real sobre infraestructura |
| Idioma | Español en todos los outputs | Requisito de producto definido en [`ptlc-roadmap-decisiones/PRD.yaml`](../ptlc-roadmap-decisiones/PRD.yaml) |

---

## 6. Selección de herramienta de prueba

```mermaid
flowchart LR
    Q1{{"¿Protocolo?"}}
    
    Q1 -->|"JDBC/JMS/FTP\nbinario"| JMETER["🔴 JMeter\n.opencode/skills/ptlc-herramientas/\n05_JMeter_Guia_Completa.md"]
    Q1 -->|HTTP/gRPC| Q2{{"¿Lenguaje\ndel equipo?"}}
    Q1 -->|WebSocket\ncomplejo| Q3{{"¿Stack?"}}
    
    Q2 -->|"JavaScript/TS"| Q4{{"¿CI-first?"}}
    Q2 -->|"Java/Kotlin/Scala"| GATLING["🔵 Gatling CE\n.opencode/skills/ptlc-herramientas/\n04_Gatling_Community_Guia_Completa.md"]
    Q2 -->|"Python"| LOCUST["🟢 Locust\n.opencode/skills/ptlc-herramientas/\n03_Locust_Guia_Completa.md"]
    
    Q4 -->|"Sí, pipeline first"| K6["🟡 k6\n.opencode/skills/ptlc-herramientas/\n06_k6_Guia_Completa_Expandida.md"]
    Q4 -->|"No, GUI disponible"| JMETER
    
    Q3 -->|Python| LOCUST
    Q3 -->|JS/Java| K6
```

> Las guías se están reorganizando por tema; la tabla de decisión vigente está en [`ptlc-herramientas/SKILL.md`](../ptlc-herramientas/SKILL.md).

---

## 7. Cobertura del knowledge base por fase

```mermaid
graph LR
    subgraph AGENTS_COL["Skills del pipeline PTLC"]
        A_INT["ptlc-intake"]
        A_DIA["ptlc-diagnostics"]
        A_PRO["ptlc-procedure-plan"]
        A_TPL["ptlc-test-plan"]
        A_EXE["ptlc-execution"]
        A_ANL["ptlc-analysis"]
    end

    subgraph DOCS_COL[".opencode/skills/ — Knowledge Base"]
        D01A["ptlc-fundamentos/01_Definicion_y_Fundamentos"]
        D01B["ptlc-fundamentos/02_Roles_y_Responsabilidades"]
        D01C["ptlc-fundamentos/03_Frameworks_y_Estandares"]
        D02I["ptlc-tipos-de-pruebas (índice)"]
        D02D["ptlc-tipos-de-pruebas/*\nLoad·Stress·Soak·Spike\nBaseline·Smoke·Resiliency"]
        D03A["ptlc-fases-del-ciclo/01_Recopilacion"]
        D03B["ptlc-fases-del-ciclo/02_Planificacion"]
        D03C["ptlc-fases-del-ciclo/03_Entorno_Scripts"]
        D03D["ptlc-fases-del-ciclo/04_Analisis_Cierre"]
        D04["ptlc-metricas-kpis"]
        D05I["ptlc-herramientas (índice + comparativa)"]
        D05K["ptlc-herramientas/06_k6 Expandida"]
        D05J["ptlc-herramientas/05_JMeter"]
        D05G["ptlc-herramientas/04_Gatling CE"]
        D05L["ptlc-herramientas/03_Locust"]
        D06["ptlc-workload-modeling · Little's Law"]
        D07["ptlc-monitoreo · Prometheus · Grafana"]
        D08["ptlc-scripting avanzado"]
        D09["ptlc-analisis-bottlenecks · RCA"]
        D10["ptlc-mejores-practicas · CI/CD"]
    end

    A_INT --> D02I
    A_INT --> D03A
    A_INT --> D04
    A_INT --> D05I

    A_DIA --> D03A
    A_DIA --> D04
    A_DIA --> D06
    A_DIA --> D07
    A_DIA --> D10

    A_PRO --> D02I
    A_PRO --> D02D
    A_PRO --> D03B
    A_PRO --> D04
    A_PRO --> D06

    A_TPL --> D01A
    A_TPL --> D01B
    A_TPL --> D01C
    A_TPL --> D03A
    A_TPL --> D03B
    A_TPL --> D04

    A_EXE --> D03C
    A_EXE --> D05K
    A_EXE --> D05J
    A_EXE --> D05G
    A_EXE --> D05L
    A_EXE --> D06
    A_EXE --> D08

    A_ANL --> D03D
    A_ANL --> D04
    A_ANL --> D07
    A_ANL --> D09
```

---

## 8. Estructura de archivos

```mermaid
graph TD
    ROOT["📁 /"]

    ROOT --> CLAUDE_F["📄 AGENTS.md"]
    ROOT --> GIT_F["📄 .gitignore"]
    ROOT --> SK_ROOT_F["📂 .opencode/skills/"]
    ROOT --> GH_F["📂 .opencode/agents/"]

    SK_ROOT_F --> README_SK["📄 README.md\nÍndice maestro"]
    SK_ROOT_F --> K1["📂 ptlc-fundamentos · ptlc-tipos-de-pruebas\nptlc-fases-del-ciclo · ptlc-metricas-kpis"]
    SK_ROOT_F --> K2["📂 ptlc-herramientas · ptlc-workload-modeling\nptlc-monitoreo · ptlc-scripting"]
    SK_ROOT_F --> K3["📂 ptlc-analisis-bottlenecks · ptlc-mejores-practicas\nptlc-arquitectura-mapas · ptlc-roadmap-decisiones"]
    SK_ROOT_F --> K4["⚙️ 6 skills pipeline: ptlc-intake\nptlc-diagnostics · ptlc-procedure-plan\nptlc-test-plan · ptlc-execution · ptlc-analysis"]
    SK_ROOT_F --> K5["🛠️ Guías operativas por herramienta\nptlc-herramientas/"]

    GH_F --> AG_F["📂 agents/"]
    GH_F --> INS_F["📂 instructions/"]

    AG_F --> PTLC_AG["🎯 .opencode/agents/ptlc-orchestrator.md\n(entry point obligatorio)"]
```

---

## 9. Modelo de navegación: 3 niveles

```mermaid
graph TD
    N1["🔵 NIVEL 1\n.opencode/skills/README.md\nMaster index global\nLookup por necesidad / keyword"]

    N2A["🟡 ptlc-tipos-de-pruebas (SKILL.md)"]
    N2B["🟡 ptlc-fases-del-ciclo (SKILL.md)"]
    N2C["🟡 ptlc-herramientas (SKILL.md)"]
    N2D["🟡 ptlc-analisis-bottlenecks (SKILL.md)"]
    N2E["🟡 ... índices temáticos más"]

    N3A["🟢 Load Testing"]
    N3B["🟢 Stress Testing"]
    N3C["🟢 k6 Guía Expandida"]
    N3D["🟢 JMeter Guía"]
    N3E["🟢 RCA y Troubleshooting"]
    N3F["🟢 Workload Modeling\n(Little's Law)"]

    N1 -->|"¿Qué tipo de prueba?"| N2A
    N1 -->|"¿Cómo ejecutar el ciclo?"| N2B
    N1 -->|"¿Qué herramienta usar?"| N2C
    N1 -->|"¿Cómo analizar resultados?"| N2D
    N1 --> N2E

    N2A --> N3A
    N2A --> N3B
    N2C --> N3C
    N2C --> N3D
    N2D --> N3E
    N2B --> N3F
```

---

## 10. Entregables y artefactos por ciclo

```mermaid
flowchart LR
    subgraph RUNTIME["⚙️ En ejecución"]
        PY["docs/plan/{plan_id}/\nplan.yaml"]
    end

    subgraph DOCS_OUT["📋 Documentos"]
        TP["docs/\nperformance-test-plan.md\n(Plan formal ISTQB)"]
        TR["docs/\nperformance-test-report.md\n(Reporte ejecutivo + RCA)"]
    end

    subgraph SCRIPTS["🧪 Scripts de Prueba"]
        K6S["tests/performance/k6/\nscripts/ · data/ · results/"]
        JMS["tests/performance/jmeter/\nscripts/ · data/ · results/"]
        GTS["tests/performance/gatling/\nscripts/ · data/ · results/"]
        LCS["tests/performance/locust/\nscripts/ · data/ · results/"]
    end

    PY --> TP
    TP --> TR
    TP --> K6S
    TP --> JMS
    TP --> GTS
    TP --> LCS
```

**Scripts generados por herramienta (Wave 5, on-demand):**

```
tests/performance/{tool}/{plan_id}/
├── [k6]       script.js + run.sh
├── [JMeter]   test-plan.jmx + pom.xml + run.ps1
├── [Gatling]  Simulation.scala/Java/Kotlin + pom.xml
└── [Locust]   locustfile.py + run.sh
```

---

## 11. Tiempos estimados por fase

```
ptlc-orchestrator (Phase 0+2)   ██░░░░░░░░░░  ~2 min  (detección + plan)
ptlc-intake        (Wave 1)     ████░░░░░░░░  ~5 min  (preguntas + selección)
ptlc-diagnostics   (Wave 2)     ████░░░░░░░░  ~5 min  (readiness check)
ptlc-procedure-plan(Wave 3)     ████████░░░░  ~10 min (workload modeling)
ptlc-test-plan     (Wave 4)     ██████████░░  ~15 min (redacción del plan)
APPROVAL GATE                   ██░░░░░░░░░░  variable
ptlc-execution     (Wave 5)     ████████████  variable (gen + ejecución)
ptlc-analysis      (Wave 6)     ████████░░░░  ~10 min (análisis + reporte)
──────────────────────────────────────────────────────────
TOTAL (sin ejecución)                         ~47 min
```

---

*Actualizado: Octubre 2026 — v3.0: knowledge base migrada de `DOCs/` a `.opencode/skills/`, `ptlc-orchestrator` como entry point obligatorio. Este documento consolidó los tres mapas previos (agentes ↔ skills, funcional simplificado y funcional v1.0), ya eliminados.*
