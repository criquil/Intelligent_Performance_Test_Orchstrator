---
applyTo: "**"
---

# PTLC Knowledge Base — Instrucciones Globales

Este repositorio es la base de conocimiento autoritativa del **Performance Test Life Cycle (PTLC)**, organizada como skills bajo `.github/skills/`.

## Regla fundamental para todos los agentes

**ANTES de responder cualquier pregunta relacionada con performance testing, pruebas de rendimiento, herramientas (k6, JMeter, Gatling, Locust), métricas, workload modeling, scripting, monitoreo, RCA o análisis de resultados:**

→ Cargar la skill temática correspondiente en `.github/skills/` y leer sus documentos con la herramienta `read`. No inventar ni asumir: la respuesta está en los documentos.

## Estructura del Knowledge Base

```
.github/skills/
├── README.md                  ← Índice maestro (Nivel 1) — empezar siempre por aquí
├── ptlc-fundamentos/          ← fundamentos, roles RACI, estándares ISO/ISTQB
├── ptlc-tipos-de-pruebas/     ← 22+ tipos: load, stress, soak, spike, baseline...
├── ptlc-fases-del-ciclo/      ← ciclo completo: requisitos → planificación → ejecución → análisis
├── ptlc-metricas-kpis/        ← p95, p99, Apdex, throughput, error rate, fórmulas
├── ptlc-herramientas/         ← guías exhaustivas: k6 (73KB), JMeter (69KB), Gatling (95KB), Locust (97KB)
├── ptlc-workload-modeling/    ← Little's Law, cálculo de VUs, distribuciones, templates
├── ptlc-monitoreo/            ← Prometheus, Grafana, OpenTelemetry, alerting
├── ptlc-scripting/            ← correlación, patrones avanzados, data management
├── ptlc-analisis-bottlenecks/ ← RCA: 5 Whys, Fishbone, profiling, DB bottlenecks
├── ptlc-mejores-practicas/    ← CI/CD, shift-left, microservicios, K8s, tendencias
├── ptlc-arquitectura-mapas/   ← mapas de arquitectura y convenciones AGENTS.md
├── ptlc-roadmap-decisiones/   ← ADRs, roadmap, plan de implementación, PRD.yaml
├── ptlc-{intake,...}/         ← skills del pipeline PTLC (6 fases)
└── performance-*/ {tool}-*    ← skills operativas de testing
```

Cada skill temática contiene un `SKILL.md` (Nivel 2: índice del tema) y los documentos detallados `NN_Tema.md` (Nivel 3).

## Punto de entrada

Para navegar el knowledge base siempre empezar por `.github/skills/README.md` — contiene el lookup rápido por necesidad y por keyword.

## Entry Point de requests

Todo request del usuario entra por el agente `ptlc-orchestrator`, que orquesta el pipeline PTLC (o deriva tareas generales a `gem-orchestrator`).

## Idioma

Todas las respuestas, documentos generados y comunicación con el usuario en **español**.
