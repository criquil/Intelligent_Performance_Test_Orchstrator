---
applyTo: "**"
---

# PTLC Knowledge Base — Instrucciones Globales

Este repositorio es la base de conocimiento autoritativa del **Performance Test Life Cycle (PTLC)**.

## Regla fundamental para todos los agentes

**ANTES de responder cualquier pregunta relacionada con performance testing, pruebas de rendimiento, herramientas (k6, JMeter, Gatling, Locust), métricas, workload modeling, scripting, monitoreo, RCA o análisis de resultados:**

→ Leer los archivos relevantes de `DOCs/` usando la herramienta `read`. No inventar ni asumir: la respuesta está en los documentos.

## Estructura del Knowledge Base

```
DOCs/
├── 01_Introduccion_PTLC/           ← fundamentos, roles RACI, estándares ISO/ISTQB
├── 02_Tipos_de_Pruebas/            ← 22+ tipos: load, stress, soak, spike, baseline...
├── 03_Fases_del_PTLC/              ← ciclo completo: requisitos → planificación → ejecución → análisis
├── 04_Metricas_y_KPIs/             ← p95, p99, Apdex, throughput, error rate, fórmulas
├── 05_Herramientas/                ← guías exhaustivas: k6 (73KB), JMeter (69KB), Gatling (95KB), Locust (97KB)
├── 06_Workload_Modeling/           ← Little's Law, cálculo de VUs, distribuciones, templates
├── 07_Entorno_y_Monitoreo/         ← Prometheus, Grafana, OpenTelemetry, alerting
├── 08_Desarrollo_de_Scripts/       ← correlación, patrones avanzados, data management
├── 09_Analisis_y_Bottlenecks/      ← RCA: 5 Whys, Fishbone, profiling, DB bottlenecks
└── 10_Mejores_Practicas/           ← CI/CD, shift-left, microservicios, K8s, tendencias
```

## Punto de entrada

Para navegar el knowledge base siempre empezar por `README.md` — contiene el lookup rápido por necesidad y por keyword.

## Idioma

Todas las respuestas, documentos generados y comunicación con el usuario en **español**.
