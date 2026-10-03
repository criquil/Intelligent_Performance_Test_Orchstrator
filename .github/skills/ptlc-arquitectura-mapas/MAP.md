# 🗺️ MAP — Intelligent Performance Test Orchestrator

> Mapa visual completo del proyecto: estructura, agentes, flujos y cobertura de conocimiento.

---

## 1. Arquitectura General del Proyecto

```mermaid
graph TB
    subgraph ROOT["📁 Raíz del Proyecto"]
        CLAUDE["📄 CLAUDE.md\nGuía para agentes AI"]
        APM_YML["📄 apm.yml\nManifiesto APM"]
        GEM_CFG["📄 .gem-team.yaml\nConfig del equipo de agentes"]
    end

    subgraph SKILLS_ROOT["📂 .github/skills/ — Knowledge Base PTLC (~650 KB)"]
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

    subgraph GITHUB["📂 .github/"]
        subgraph AGENTS["📂 agents/ — 17 agentes"]
            PTLC_ORCH["🎯 ptlc-orchestrator\n(ENTRY POINT OBLIGATORIO v3.0)"]
            GEM_ORCH["🏆 gem-orchestrator\n(tareas generales, derivado)"]
            GEM_AGENTS["🤖 15 agentes gem-team"]
        end
        subgraph SKILLS["📂 skills/ — 26 skills"]
            PIPE["⚙️ 6 skills pipeline PTLC\nintake · diagnostics · procedure\nplan · execution · analysis"]
            OPS["🛠️ 8 skills operativas\nperformance-* · {tool}-workflow"]
        end
    end

    IDX --> D01
    IDX --> D12
    CLAUDE --> SKILLS_ROOT
    GEM_CFG --> PTLC_ORCH
    PTLC_ORCH --> PIPE
    PTLC_ORCH -->|general| GEM_ORCH
    GEM_ORCH --> GEM_AGENTS
    PIPE --> OPS
```

---

## 2. Flujo v3.0 — ptlc-orchestrator como entry point obligatorio

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

    subgraph GEM_FLOW["🛠️ Pipeline General — gem-orchestrator"]
        direction TB
        G1["gem-planner → DAG de tasks"]
        G2["gem-researcher / gem-implementer\ngem-reviewer / gem-debugger\ngem-documentation-writer..."]
        G1 --> G2
    end

    OUT_PTLC(["📦 Entregables PTLC\n• docs/performance-test-plan.md\n• tests/performance/{tool}/\n• docs/performance-test-report.md"])
    OUT_GEN(["📦 Entregables generales\n• código · documentación · tests"])

    USER --> PTLC_ORCH
    PTLC_ORCH --> DOMAIN
    DOMAIN -->|performance-testing| PTLC_FLOW
    DOMAIN -->|general| GEM_FLOW
    PTLC_FLOW --> OUT_PTLC
    GEM_FLOW --> OUT_GEN

    F5 -->|approval gate| USER
    USER -->|confirmación| F5
```

---

## 3. Selección de Herramienta de Prueba

```mermaid
flowchart LR
    Q1{{"¿Protocolo?"}}
    
    Q1 -->|"JDBC/JMS/FTP\nbinario"| JMETER["🔴 JMeter\n.github/skills/ptlc-herramientas/\n05_JMeter_Guia_Completa.md"]
    Q1 -->|HTTP/gRPC| Q2{{"¿Lenguaje\ndel equipo?"}}
    Q1 -->|WebSocket\ncomplejo| Q3{{"¿Stack?"}}
    
    Q2 -->|"JavaScript/TS"| Q4{{"¿CI-first?"}}
    Q2 -->|"Java/Kotlin/Scala"| GATLING["🔵 Gatling CE\n.github/skills/ptlc-herramientas/\n04_Gatling_Community_Guia_Completa.md"]
    Q2 -->|"Python"| LOCUST["🟢 Locust\n.github/skills/ptlc-herramientas/\n03_Locust_Guia_Completa.md"]
    
    Q4 -->|"Sí, pipeline first"| K6["🟡 k6\n.github/skills/ptlc-herramientas/\n06_k6_Guia_Completa_Expandida.md"]
    Q4 -->|"No, GUI disponible"| JMETER
    
    Q3 -->|Python| LOCUST
    Q3 -->|JS/Java| K6
```

---

## 4. Cobertura de Knowledge Base por Fase (skills)

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

    subgraph DOCS_COL[".github/skills/ — Knowledge Base"]
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

## 5. Estructura de Archivos Completa

```mermaid
graph TD
    ROOT["📁 /"]

    ROOT --> CLAUDE_F["📄 CLAUDE.md"]
    ROOT --> APM_F["📄 apm.yml"]
    ROOT --> GEM_F["📄 .gem-team.yaml"]
    ROOT --> GIT_F["📄 .gitignore"]
    ROOT --> SK_ROOT_F["📂 .github/skills/"]
    ROOT --> GH_F["📂 .github/"]
    ROOT --> TESTS_F["📂 tests/"]

    SK_ROOT_F --> README_SK["📄 README.md\nÍndice maestro"]
    SK_ROOT_F --> K1["📂 ptlc-fundamentos · ptlc-tipos-de-pruebas\nptlc-fases-del-ciclo · ptlc-metricas-kpis"]
    SK_ROOT_F --> K2["📂 ptlc-herramientas · ptlc-workload-modeling\nptlc-monitoreo · ptlc-scripting"]
    SK_ROOT_F --> K3["📂 ptlc-analisis-bottlenecks · ptlc-mejores-practicas\nptlc-arquitectura-mapas · ptlc-roadmap-decisiones"]
    SK_ROOT_F --> K4["⚙️ 6 skills pipeline: ptlc-intake\nptlc-diagnostics · ptlc-procedure-plan\nptlc-test-plan · ptlc-execution · ptlc-analysis"]
    SK_ROOT_F --> K5["🛠️ 8 skills operativas\nperformance-* · {tool}-workflow"]

    GH_F --> AG_F["📂 agents/"]
    GH_F --> INS_F["📂 instructions/"]

    AG_F --> PTLC_AG["🎯 ptlc-orchestrator.agent.md\n(entry point obligatorio)"]
    AG_F --> GEM_AG["🤖 gem-team Agents (16)\ngem-orchestrator · gem-researcher\ngem-planner · gem-implementer\ngem-reviewer · gem-debugger\ngem-critic · gem-devops\n...y 9 más"]
```

---

## 6. Modelo de Navegación (3 Niveles)

```mermaid
graph TD
    N1["🔵 NIVEL 1\n.github/skills/README.md\nMaster index global\nLookup por necesidad / keyword"]

    N2A["🟡 ptlc-tipos-de-pruebas (SKILL.md)"]
    N2B["🟡 ptlc-fases-del-ciclo (SKILL.md)"]
    N2C["🟡 ptlc-herramientas (SKILL.md)"]
    N2D["🟡 ptlc-analisis-bottlenecks (SKILL.md)"]
    N2E["🟡 ... 8 índices más"]

    N3A["🟢 Load Testing"]
    N3B["🟢 Stress Testing"]
    N3C["🟢 k6 Guía Expandida\n(73 KB)"]
    N3D["🟢 JMeter Guía\n(69 KB)"]
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

## 7. Entregables Generados por el Proceso PTLC

```mermaid
flowchart LR
    subgraph RUNTIME["⚙️ En ejecución"]
        PY["docs/plan/{plan_id}/\nplan.yaml\ncontext_envelope.json"]
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

---

*Actualizado: Octubre 2026 — v3.0: knowledge base migrada de `DOCs/` a `.github/skills/`, `ptlc-orchestrator` como entry point obligatorio*
