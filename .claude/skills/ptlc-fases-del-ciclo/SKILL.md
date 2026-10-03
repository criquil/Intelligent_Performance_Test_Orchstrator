---
name: ptlc-fases-del-ciclo
description: "Define las 9 fases del PTLC: requisitos a cierre"
---

# 03 — Fases del Performance Test Life Cycle (Detalle)

> Índice intermedio. **Cuándo leer:** ejecutar una fase concreta, sus entregables y el orden de actividades. Detalle en los documentos de esta skill (abajo).

## Las 9 Fases — Vista General

| # | Fase | Input principal | Output principal | Archivo detallado |
|---|------|-----------------|------------------|-------------------|
| 1 | Recopilación de Requisitos | Stakeholders, arquitectura, producción data | NFRs documentados, escenarios priorizados | `01_Recopilacion_de_Requisitos.md` |
| 2 | Planificación | NFRs, arquitectura | Test Plan aprobado | `02_Planificacion_y_Diseno.md` |
| 3 | Diseño de Pruebas | Test Plan | Workload model, casos de prueba | `02_Planificacion_y_Diseno.md` |
| 4 | Configuración del Entorno | Diseño, IaC templates | Entorno validado, monitoreo activo | `03_Entorno_Scripts_Ejecucion.md` |
| 5 | Desarrollo de Scripts | Casos de prueba, entorno | Scripts validados y parametrizados | `03_Entorno_Scripts_Ejecucion.md` |
| 6 | Ejecución | Scripts, entorno, runbook | Datos crudos, observaciones | `03_Entorno_Scripts_Ejecucion.md` |
| 7 | Análisis de Resultados | Datos de ejecución | Reporte con hallazgos y RCA | `04_Analisis_Optimizacion_Cierre.md` |
| 8 | Optimización y Re-testing | Reporte, fixes aplicados | Métricas mejoradas, validación | `04_Analisis_Optimizacion_Cierre.md` |
| 9 | Cierre | Resultados finales | Sign-off, lessons learned, archivo | `04_Analisis_Optimizacion_Cierre.md` |

---

## 📂 Contenido de la Subcarpeta

### [`01_Recopilacion_de_Requisitos.md`](01_Recopilacion_de_Requisitos.md) — NFRs, cálculo de carga, template
- Para qué: capturar requisitos de performance firmados.
- Consultar si: necesitas el template de requisitos (8 secciones) · calculas usuarios concurrentes esperados · facilitates un workshop con stakeholders

### [`02_Planificacion_y_Diseno.md`](02_Planificacion_y_Diseno.md) — Test Plan y diseño de carga
- Para qué: escribir el plan y diseñar el workload model.
- Consultar si: defines criterios de aceptación / pass-fail · elaboras la estrategia de test data · diseñas el monitoreo de la prueba

### [`03_Entorno_Scripts_Ejecucion.md`](03_Entorno_Scripts_Ejecucion.md) — entorno, scripts, ejecución, runbook
- Para qué: preparar y ejecutar la prueba de forma controlada.
- Consultar si: validas que el entorno está listo (checklist) · organizas la estructura de scripts · necesitas el runbook pre/durante/post ejecución

### [`04_Analisis_Optimizacion_Cierre.md`](04_Analisis_Optimizacion_Cierre.md) — reporte, optimización, sign-off
- Para qué: cerrar el ciclo con reporte y retrospectiva.
- Consultar si: usas el template de reporte ejecutivo (7 secciones) · iteras tune → test → validate · formalizas el sign-off y la retrospectiva

---

## 🔗 Relación con otras categorías

| Desde aquí puedo ir a... | Para... |
|--------------------------|---------|
| [ptlc-fundamentos](../ptlc-fundamentos/SKILL.md) | Entender los fundamentos antes de las fases |
| [ptlc-metricas-kpis](../ptlc-metricas-kpis/SKILL.md) | Definir qué medir (usado en Fases 1, 7) |
| [ptlc-herramientas](../ptlc-herramientas/SKILL.md) | Implementar scripts (Fase 5) |
| [ptlc-workload-modeling](../ptlc-workload-modeling/SKILL.md) | Calcular el modelo de carga (Fase 3) |
| [ptlc-monitoreo](../ptlc-monitoreo/SKILL.md) | Configurar observabilidad (Fase 4) |
| [ptlc-analisis-bottlenecks](../ptlc-analisis-bottlenecks/SKILL.md) | Técnicas de RCA detalladas (Fase 7) |