# 🗺️ MAP — Intelligent Performance Test Orchestrator

> Mapa único de la arquitectura v3.0: estructura del repo, pipeline de agentes, cobertura del knowledge base, entregables y tiempos.
> Convenciones y reglas de navegación del repo en [CONVENTIONS.md](CONVENTIONS.md). Pipeline por fases en [`../ptlc-fases-del-ciclo/`](../ptlc-fases-del-ciclo/SKILL.md).

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
        CLAUDE["📄 CLAUDE.md\nMemoria del proyecto"]
    end

    subgraph SKILLS_ROOT["📂 .claude/skills/ — Knowledge Base PTLC"]
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

    subgraph GITHUB["📂 .claude/"]
        subgraph AGENTS_SUB["📂 agents/ — 1 subagente"]
            PTLC_ORCH["🎯 ptlc-orchestrator\n(ENTRY POINT OBLIGATORIO v3.0)"]
        end
        subgraph SKILLS["📂 skills/ — 18 skills ptlc-*"]
            PIPE["⚙️ 6 skills pipeline PTLC\nintake · diagnostics · procedure\nplan · execution · analysis"]
            OPS["🛠️ Referencia central + cheat sheet\nptlc-herramientas/ (solo índice)"]
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

    PTLC_ORCH["🎯 ptlc-orchestrator\nENTRY POINT OBLIGATORIO\nPhase 0: detecta dominio + clasifica\nPersiste plan en tests/performance/{selected_tool}/{plan_id}/"]

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

    GEN_FLOW["🛠️ Soporte general — subagentes integrados\n`general-purpose` (multi-paso) · `Explore` (exploración)"]

    OUT_PTLC(["📦 Entregables PTLC\n• tests/performance/{selected_tool}/{plan_id}/performance-test-plan.md\n• tests/performance/{tool}/\n• tests/performance/{selected_tool}/{plan_id}/performance-test-report.md"])
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
| 0 | `ptlc-orchestrator` | Request del usuario | PRD (`ptlc-roadmap-decisiones`) | Detección de dominio + plan 6-wave | `tests/performance/{selected_tool}/{plan_id}/plan.yaml` |
| 1 | `ptlc-intake` | Solicitud | `ptlc-fundamentos`, `ptlc-tipos-de-pruebas`, `ptlc-herramientas` (cheat sheet), `ptlc-workload-modeling` | Preguntas estructuradas + selección de UNA herramienta | Requisitos completos + herramienta elegida |
| 2 | `ptlc-diagnostics` | Requisitos, entorno | `ptlc-fases-del-ciclo` (readiness), `ptlc-metricas-kpis`, `ptlc-workload-modeling`, `ptlc-monitoreo`, `ptlc-mejores-practicas` | Evaluación de entorno y dependencias | Readiness score + riesgos |
| 3 | `ptlc-procedure-plan` | Requisitos + diagnóstico | `ptlc-tipos-de-pruebas`, `ptlc-workload-modeling` (Little's Law), `ptlc-metricas-kpis` | Tipos de prueba + modelo de carga | Workload model + tipos seleccionados |
| 4 | `ptlc-test-plan` | Procedure plan | `ptlc-fundamentos`, `ptlc-fases-del-ciclo` (planificación) | Redacción ISTQB/IEEE-829 | `tests/performance/{selected_tool}/{plan_id}/performance-test-plan.md` |
| — | **APPROVAL GATE** | Plan completo | — | `ptlc-orchestrator` presenta el plan y espera confirmación explícita | Aprobado → Wave 5 · rechazado → ciclo pausado |
| 5 | `ptlc-execution` | Test plan aprobado | `ptlc-herramientas` (cheat sheet), `ptlc-scripting`, `ptlc-fases-del-ciclo` | Generación on-demand de scripts + ejecución | Scripts + resultados en `tests/performance/{selected_tool}/{plan_id}/` |
| 6 | `ptlc-analysis` | Resultados de ejecución | `ptlc-metricas-kpis`, `ptlc-analisis-bottlenecks`, `ptlc-fases-del-ciclo` (análisis y cierre), `ptlc-monitoreo` | Métricas + RCA + health scoring | `tests/performance/{selected_tool}/{plan_id}/performance-test-report.md` + veredicto PASSED/FAILED |

---

## 4. Guías por agente

| Agente | Guías que debe leer |
|--------|--------------------|
| `ptlc-orchestrator` | Detección de dominio (Phase 0), generación de plan 6-wave (Phase 2), approval gate (Phase 3B) |
| `ptlc-intake` | [`ptlc-herramientas/SKILL.md`](../ptlc-herramientas/SKILL.md) — matriz de decisión rápida vía cheat sheet |
| `ptlc-diagnostics` | Checklist de readiness de [`ptlc-fases-del-ciclo/SKILL.md`](../ptlc-fases-del-ciclo/SKILL.md) |
| `ptlc-procedure-plan` | [`ptlc-tipos-de-pruebas/SKILL.md`](../ptlc-tipos-de-pruebas/SKILL.md) + [`ptlc-workload-modeling/SKILL.md`](../ptlc-workload-modeling/SKILL.md) — tipos de prueba + Little's Law |
| `ptlc-test-plan` | [`ptlc-fundamentos/SKILL.md`](../ptlc-fundamentos/SKILL.md) + template ISTQB/IEEE-829 de [`ptlc-fases-del-ciclo/`](../ptlc-fases-del-ciclo/SKILL.md) |
| `ptlc-execution` | Cheat sheet en [`ptlc-herramientas/00b_Cheat_Sheet_Herramientas.md`](../ptlc-herramientas/00b_Cheat_Sheet_Herramientas.md) + [`ptlc-scripting/`](../ptlc-scripting/SKILL.md) |
| `ptlc-analysis` | [`ptlc-metricas-kpis/SKILL.md`](../ptlc-metricas-kpis/SKILL.md) — percentiles, Apdex, throughput, error rate · [`ptlc-analisis-bottlenecks/SKILL.md`](../ptlc-analisis-bottlenecks/SKILL.md) — 5 Whys, Fishbone, health scoring, ranking P1/P2/P3 |

---

## 5. Principios de arquitectura y decisiones críticas

| Principio | Implementación |
|-----------|----------------|
| Entry point único | `ptlc-orchestrator` recibe todos los requests; resuelve los no-PTLC con los subagentes integrados (`general-purpose`/`Explore`) o el knowledge base |
| Una herramienta por ciclo | `ptlc-intake` selecciona UNA herramienta; nunca paralelo |
| Generación on-demand | Scripts generados en Wave 5 — no existen pre-creados |
| Aprobación explícita | `ptlc-execution` no corre sin confirmación del usuario |
| Resultados individuales | Cada ejecución es independiente; no hay comparación cross-tool |
| Estado persistido | `tests/performance/{selected_tool}/{plan_id}/plan.yaml` guarda el estado de cada ciclo |
| Knowledge Base como fuente de verdad | Cada agente lee los documentos relevantes antes de actuar |
| Outputs en español | Todos los reportes, planes y comunicaciones en español |

| Decisión | Valor | Justificación |
|----------|-------|---------------|
| Script generation | On-demand en Wave 5 | No existen scripts pre-creados; se generan para cada request |
| Output path | `tests/performance/{selected_tool}/{plan_id}/` | Organización por herramienta y ciclo para trazabilidad |
| State persistence | `tests/performance/{selected_tool}/{plan_id}/plan.yaml` | Permite retomar ciclos interrumpidos |
| Approval gate | Requerida antes de ejecutar | `ptlc-execution` tiene impacto real sobre infraestructura |
| Idioma | Español en todos los outputs | Requisito de producto definido en [`ptlc-roadmap-decisiones/PRD.yaml`](../ptlc-roadmap-decisiones/PRD.yaml) |

---

## 6. Selección de herramienta de prueba

```mermaid
flowchart LR
    Q1{{"¿Protocolo?"}}
    
    Q1 -->|"JDBC/JMS/FTP\nbinario"| JMETER["🔴 JMeter\nDocumentación oficial"]
    Q1 -->|HTTP/gRPC| Q2{{"¿Lenguaje\ndel equipo?"}}
    Q1 -->|WebSocket\ncomplejo| Q3{{"¿Stack?"}}
    
    Q2 -->|"JavaScript/TS"| Q4{{"¿CI-first?"}}
    Q2 -->|"Java/Kotlin/Scala"| GATLING["🔵 Gatling CE\nDocumentación oficial"]
    Q2 -->|"Python"| LOCUST["🟢 Locust\nDocumentación oficial"]
    
    Q4 -->|"Sí, pipeline first"| K6["🟡 k6\nDocumentación oficial"]
    Q4 -->|"No, GUI disponible"| JMETER
    
    Q3 -->|Python| LOCUST
    Q3 -->|JS/Java| K6
```

> **Nota v3.0:** La skill `ptlc-herramientas` ahora solo contiene el cheat sheet central ([`00b_Cheat_Sheet_Herramientas.md`](../ptlc-herramientas/00b_Cheat_Sheet_Herramientas.md)). Toda información detallada sobre k6, JMeter, Gatling y Locust está en la documentación oficial de cada herramienta. Usa el cheat sheet para decisión rápida y navegación a secciones comunes (CI/CD, troubleshooting).

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

    subgraph DOCS_COL[".claude/skills/ — Knowledge Base"]
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
        D05I["ptlc-herramientas (índice + cheat sheet)"]
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
    A_EXE --> D05I
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

    ROOT --> CLAUDE_F["📄 CLAUDE.md"]
    ROOT --> GIT_F["📄 .gitignore"]
    ROOT --> SK_ROOT_F["📂 .claude/skills/"]
    ROOT --> GH_F["📂 .claude/agents/"]

    SK_ROOT_F --> README_SK["📄 README.md\nÍndice maestro"]
    SK_ROOT_F --> K1["📂 ptlc-fundamentos · ptlc-tipos-de-pruebas\nptlc-fases-del-ciclo · ptlc-metricas-kpis"]
    SK_ROOT_F --> K2["📂 ptlc-herramientas (solo cheat sheet)\nptlc-workload-modeling\nptlc-monitoreo · ptlc-scripting"]
    SK_ROOT_F --> K3["📂 ptlc-analisis-bottlenecks · ptlc-mejores-practicas\nptlc-arquitectura-mapas · ptlc-roadmap-decisiones"]
    SK_ROOT_F --> K4["⚙️ 6 skills pipeline: ptlc-intake\nptlc-diagnostics · ptlc-procedure-plan\nptlc-test-plan · ptlc-execution · ptlc-analysis"]

    GH_F --> AG_F["📂 agents/"]
    GH_F --> INS_F["📂 instructions/"]

    AG_F --> PTLC_AG["🎯 .claude/agents/ptlc-orchestrator.md\n(entry point obligatorio)"]
```

---

## 9. Modelo de navegación: 3 niveles

```mermaid
graph TD
    N1["🔵 NIVEL 1\n.claude/skills/README.md\nMaster index global\nLookup por necesidad / keyword"]

    N2A["🟡 ptlc-tipos-de-pruebas (SKILL.md)"]
    N2B["🟡 ptlc-fases-del-ciclo (SKILL.md)"]
    N2C["🟡 ptlc-herramientas (SKILL.md)"]
    N2D["🟡 ptlc-analisis-bottlenecks (SKILL.md)"]
    N2E["🟡 ... índices temáticos más"]

    N3A["🟢 Load Testing"]
    N3B["🟢 Stress Testing"]
    N3C["🟢 k6 Cheat Sheet"]
    N3D["🟢 JMeter Cheat Sheet"]
    N3E["🟢 Gatling Cheat Sheet"]
    N3F["🟢 Locust Cheat Sheet"]

    N1 --> N2A
    N1 --> N2B
    N1 --> N2C
    N1 --> N2D
    N1 --> N2E

    N2C --> N3C
    N2C --> N3D
    N2C --> N3E
    N2C --> N3F

    style N1 fill:#e1f5ff
    style N2A fill:#fff4e1
    style N2B fill:#fff4e1
    style N2C fill:#fff4e1
    style N2D fill:#fff4e1
    style N2E fill:#fff4e1
    style N3A fill:#e8f5e9
    style N3B fill:#e8f5e9
    style N3C fill:#e8f5e9
    style N3D fill:#e8f5e9
    style N3E fill:#e8f5e9
    style N3F fill:#e8f5e9
```

---

## 10. Entregables y artefactos por ciclo

| Fase | Entregable principal | Formato | Ubicación |
|------|---------------------|---------|-----------|
| F1 (Intake) | `requirements.json` + herramienta seleccionada | JSON | `tests/performance/{selected_tool}/{plan_id}/` |
| F2 (Diagnostics) | Readiness score + riesgos identificados | JSON | `tests/performance/{selected_tool}/{plan_id}/` |
| F3 (Procedure Plan) | Workload model + tipos de prueba | YAML | `tests/performance/{selected_tool}/{plan_id}/` |
| F4 (Test Plan) | Documento formal ISTQB/IEEE-829 | Markdown | `tests/performance/{selected_tool}/{plan_id}/performance-test-plan.md` |
| **Gate** | Aprobación explícita del usuario | Confirmación | Interfaz UI |
| F5 (Execution) | Scripts generados + resultados | Scripts + JSON | `tests/performance/{selected_tool}/{plan_id}/` |
| F6 (Analysis) | Reporte final con veredicto | Markdown | `tests/performance/{selected_tool}/{plan_id}/performance-test-report.md` |

---

## 11. Tiempos estimados por fase

| Fase | Tiempo estimado | Depende de |
|------|-----------------|------------|
| F0 (Detection) | ~2 min | Complejidad del request |
| F1 (Intake) | 5-15 min | Cantidad de preguntas |
| F2 (Diagnostics) | 3-8 min | Complejidad del entorno |
| F3 (Procedure Plan) | 5-10 min | Workload model complexity |
| F4 (Test Plan) | 8-15 min | Longitud del documento formal |
| **Gate** | Variable | Respuesta usuario |
| F5 (Execution) | 10-30 min | Scripts generados + infraestructura |
| F6 (Analysis) | 5-12 min | Cantidad de métricas/RCA |

**Total ciclo completo:** ~45-90 minutos promedio

---

*Documento generado automáticamente por análisis del repositorio PTLC MAP*  
*Última actualización: 2026-10-05*
