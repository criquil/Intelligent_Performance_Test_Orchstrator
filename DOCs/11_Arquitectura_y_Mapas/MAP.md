# 🗺️ MAP — Intelligent Performance Test Orchestrator

> Mapa visual completo del proyecto: estructura, agentes, flujos y cobertura de conocimiento.

---

## 1. Arquitectura General del Proyecto

```mermaid
graph TB
    subgraph ROOT["📁 Raíz del Proyecto"]
        README["📄 README.md\nPunto de entrada · Master index"]
        AGENTS_MD["📄 AGENTS.md\nGuía para agentes AI"]
        MAP["📄 MAP.md\nEste archivo"]
        APM_YML["📄 apm.yml\nManifiesto APM"]
        GEM_CFG["📄 .gem-team.yaml\nConfig del equipo de agentes"]
    end

    subgraph DOCS["📂 DOCs/ — Knowledge Base PTLC (~650 KB)"]
        direction TB
        D01["📂 01 Introducción PTLC"]
        D02["📂 02 Tipos de Pruebas"]
        D03["📂 03 Fases del PTLC"]
        D04["📂 04 Métricas y KPIs"]
        D05["📂 05 Herramientas"]
        D06["📂 06 Workload Modeling"]
        D07["📂 07 Entorno y Monitoreo"]
        D08["📂 08 Desarrollo de Scripts"]
        D09["📂 09 Análisis y Bottlenecks"]
        D10["📂 10 Mejores Prácticas"]
    end

    subgraph GITHUB["📂 .github/"]
        subgraph AGENTS["📂 agents/ — 23 agentes totales"]
            GEM_ORCH["🏆 gem-orchestrator\n(entry point unificado v2.0)"]
            PTLC_ORCH["🎯 ptlc-orchestrator\n(conveniencia, acceso directo)"]
            PTLC_SUBS["⚙️ 6 subagentes PTLC"]
            GEM_AGENTS["🤖 15 agentes gem-team"]
        end
        subgraph SKILLS["📂 skills/ — 8 skills"]
            SK1["performance-tool-selector"]
            SK2["k6 · jmeter · gatling · locust\nworkflow skills"]
            SK3["performance-test-strategy"]
            SK4["performance-metrics-analysis"]
            SK5["performance-diagnostics-rca"]
        end
    end

    README --> DOCS
    README --> GITHUB
    AGENTS_MD --> GITHUB
    APM_YML --> GEM_AGENTS
    GEM_CFG --> GEM_ORCH
    GEM_ORCH --> PTLC_SUBS
```

---

## 2. Flujo v2.0 — gem-orchestrator como coordinador central

```mermaid
flowchart TD
    USER(["👤 Usuario\n'Necesito probar mi API'\nO cualquier tarea general"])

    GEM_ORCH["🏆 gem-orchestrator\nEntry point unificado v2.0\nPhase 0: detecta dominio + clasifica\nPersiste plan en docs/plan/"]

    DOMAIN{{"¿Dominio detectado?"}}

    subgraph PTLC_FLOW["📊 Pipeline PTLC — performance-testing"]
        direction TB
        F1["Wave 1 · ptlc-intake\nRequisitos + tool selection"]
        F2["Wave 2 · ptlc-diagnostics\nReadiness Score · Riesgos"]
        F3["Wave 3 · ptlc-procedure-plan\nTipos de prueba · Workload Model"]
        F4["Wave 4 · ptlc-test-plan\nDocumento ISTQB/IEEE-829"]
        F5["Wave 5 · ptlc-execution\n⚠️ Requiere aprobación usuario\nGenera scripts + ejecuta"]
        F6["Wave 6 · ptlc-analysis\nMétricas · RCA · Veredicto"]
        F1 --> F2 --> F3 --> F4 --> F5 --> F6
    end

    subgraph GEM_FLOW["🛠️ Pipeline General — development"]
        direction TB
        G1["gem-planner → DAG de tasks"]
        G2["gem-researcher / gem-implementer\ngem-reviewer / gem-debugger\ngem-documentation-writer..."]
        G1 --> G2
    end

    OUT_PTLC(["📦 Entregables PTLC\n• docs/performance-test-plan.md\n• tests/performance/{tool}/\n• docs/performance-test-report.md"])
    OUT_GEN(["📦 Entregables generales\n• código · documentación · tests"])

    USER --> GEM_ORCH
    GEM_ORCH --> DOMAIN
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
    
    Q1 -->|"JDBC/JMS/FTP\nbinario"| JMETER["🔴 JMeter\nDOCs/05_Herramientas/\n05_JMeter_Guia_Completa.md"]
    Q1 -->|HTTP/gRPC| Q2{{"¿Lenguaje\ndel equipo?"}}
    Q1 -->|WebSocket\ncomplejo| Q3{{"¿Stack?"}}
    
    Q2 -->|"JavaScript/TS"| Q4{{"¿CI-first?"}}
    Q2 -->|"Java/Kotlin/Scala"| GATLING["🔵 Gatling CE\nDOCs/05_Herramientas/\n04_Gatling_Community_Guia_Completa.md"]
    Q2 -->|"Python"| LOCUST["🟢 Locust\nDOCs/05_Herramientas/\n03_Locust_Guia_Completa.md"]
    
    Q4 -->|"Sí, pipeline first"| K6["🟡 k6\nDOCs/05_Herramientas/\n06_k6_Guia_Completa_Expandida.md"]
    Q4 -->|"No, GUI disponible"| JMETER
    
    Q3 -->|Python| LOCUST
    Q3 -->|JS/Java| K6
```

---

## 4. Cobertura de DOCs por Agente

```mermaid
graph LR
    subgraph AGENTS_COL["Agentes PTLC"]
        A_INT["ptlc-intake"]
        A_DIA["ptlc-diagnostics"]
        A_PRO["ptlc-procedure-plan"]
        A_TPL["ptlc-test-plan"]
        A_EXE["ptlc-execution"]
        A_ANL["ptlc-analysis"]
    end

    subgraph DOCS_COL["DOCs — Knowledge Base"]
        D01A["01/01 Definición y Fundamentos"]
        D01B["01/02 Roles y Responsabilidades"]
        D01C["01/03 Frameworks y Estándares"]
        D02I["02 Tipos de Pruebas (índice)"]
        D02D["02/* Load·Stress·Soak·Spike\nBaseline·Smoke·Resiliency"]
        D03A["03/01 Recopilación de Requisitos"]
        D03B["03/02 Planificación y Diseño"]
        D03C["03/03 Entorno Scripts Ejecución"]
        D03D["03/04 Análisis Optimización Cierre"]
        D04["04 Métricas y KPIs"]
        D05I["05 Herramientas (índice + comparativa)"]
        D05K["05/06 k6 Expandida"]
        D05J["05/05 JMeter"]
        D05G["05/04 Gatling CE"]
        D05L["05/03 Locust"]
        D06["06 Workload Modeling · Little's Law"]
        D07["07 Monitoreo · Prometheus · Grafana"]
        D08["08 Scripting Avanzado"]
        D09["09 RCA y Troubleshooting"]
        D10["10 CI/CD y Mejores Prácticas"]
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

    ROOT --> README_F["📄 README.md"]
    ROOT --> AGENTS_F["📄 AGENTS.md"]
    ROOT --> MAP_F["📄 MAP.md"]
    ROOT --> APM_F["📄 apm.yml"]
    ROOT --> GEM_F["📄 .gem-team.yaml"]
    ROOT --> GIT_F["📄 .gitignore"]
    ROOT --> DOCS_F["📂 DOCs/"]
    ROOT --> GH_F["📂 .github/"]

    DOCS_F --> D01_F["📂 01_Introduccion_PTLC/\n• 01_Definicion_y_Fundamentos.md\n• 02_Roles_y_Responsabilidades.md\n• 03_Frameworks_y_Estandares.md"]
    DOCS_F --> D02_F["📂 02_Tipos_de_Pruebas/\n• 01_Load · 02_Stress · 03_Endurance\n• 04_Baseline · 05_Smoke · 06_Config\n• 07_Resiliency"]
    DOCS_F --> D03_F["📂 03_Fases_del_PTLC/\n• 01_Recopilacion · 02_Planificacion\n• 03_Entorno · 04_Analisis"]
    DOCS_F --> D04_F["📂 04_Metricas_y_KPIs/\n• 01_Metricas_Exhaustivas.md"]
    DOCS_F --> D05_F["📂 05_Herramientas/\n• 01_k6 · 02_Comparativa · 03_Locust\n• 04_Gatling · 05_JMeter · 06_k6_Expandida"]
    DOCS_F --> D06_F["📂 06_Workload_Modeling/\n• 01_Workload_Modeling_Exhaustivo.md"]
    DOCS_F --> D07_F["📂 07_Entorno_y_Monitoreo/\n• 01_Monitoreo_y_Observabilidad.md"]
    DOCS_F --> D08_F["📂 08_Desarrollo_de_Scripts/\n• 01_Scripting_Avanzado.md"]
    DOCS_F --> D09_F["📂 09_Analisis_y_Bottlenecks/\n• 01_RCA_y_Troubleshooting.md"]
    DOCS_F --> D10_F["📂 10_Mejores_Practicas/\n• 01_CICD_y_Tendencias_Futuras.md"]

    GH_F --> AG_F["📂 agents/"]
    GH_F --> SK_F["📂 skills/"]

    AG_F --> PTLC_AG["🎯 PTLC Agents\nptlc-orchestrator.agent.md\nptlc-intake.agent.md\nptlc-diagnostics.agent.md\nptlc-procedure-plan.agent.md\nptlc-test-plan.agent.md\nptlc-execution.agent.md\nptlc-analysis.agent.md"]
    AG_F --> GEM_AG["🤖 gem-team Agents (16)\ngem-orchestrator · gem-researcher\ngem-planner · gem-implementer\ngem-reviewer · gem-debugger\ngem-critic · gem-devops\n...y 8 más"]

    SK_F --> SKILL_LIST["📦 8 Skills\nperformance-tool-selector\nk6-performance-workflow\njmeter-performance-workflow\ngatling-performance-workflow\nlocust-performance-workflow\nperformance-test-strategy\nperformance-metrics-analysis\nperformance-diagnostics-rca"]
```

---

## 6. Modelo de Navegación (3 Niveles)

```mermaid
graph TD
    N1["🔵 NIVEL 1\nREADME.md\nMaster index global\nLookup por necesidad / keyword"]

    N2A["🟡 02 Tipos de Pruebas"]
    N2B["🟡 03 Fases del PTLC"]
    N2C["🟡 05 Herramientas"]
    N2D["🟡 09 Análisis y Bottlenecks"]
    N2E["🟡 ... 6 índices más"]

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

*Actualizado: Junio 2026 — Generado automáticamente por ptlc-orchestrator*
