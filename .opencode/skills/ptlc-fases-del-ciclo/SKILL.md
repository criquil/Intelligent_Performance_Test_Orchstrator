---
name: ptlc-fases-del-ciclo
description: "Las 9 fases del Performance Test Life Cycle: requisitos, planificacion, diseno, entorno, scripts, ejecucion, analisis, optimizacion y cierre con reporting."
---

# 03 — Fases del Performance Test Life Cycle (Detalle)

> **Rol de este archivo:** Índice intermedio. Resume las 9 fases del PTLC y dirige a la documentación operativa detallada.  
> **Cuándo leer este archivo:** Cuando necesitas ejecutar una fase específica del ciclo, saber qué entregables produce, o entender el orden de las actividades.  
> **Carpeta detallada:** [`.`](03_Fases_del_PTLC/)

---

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

### [`01_Recopilacion_de_Requisitos.md`](01_Recopilacion_de_Requisitos.md)
**Fase cubierta:** Fase 1 — Recopilación y Análisis de Requisitos  
**Secciones:** Propósito · Fuentes de requisitos (producción, negocio, técnicas) · Proceso de recopilación (workshops, entrevistas) · Análisis de carga esperada (cálculos de concurrencia) · Identificación de escenarios críticos · Template de documentación de requisitos (Executive Summary, SUT, Performance Requirements, Load Profile, Scenarios, Constraints, Risks, Approval) · Errores comunes

**Ir aquí si necesitas:**
- Template para documentar requisitos de performance
- Fórmulas para calcular usuarios concurrentes esperados
- Guía para facilitar workshops con stakeholders
- Priorizar escenarios de prueba

---

### [`02_Planificacion_y_Diseno.md`](02_Planificacion_y_Diseno.md)
**Fases cubiertas:** Fase 2 (Planificación) + Fase 3 (Diseño)  
**Secciones:** Objetivos del plan · Alcance (in/out scope) · Cronograma · Diseño de pruebas · Workload model definition · Criterios de aceptación · Monitoring design · Test data strategy

**Ir aquí si necesitas:**
- Escribir un Performance Test Plan
- Diseñar el workload model
- Definir criterios de pass/fail para cada escenario
- Planificar test data

---

### [`03_Entorno_Scripts_Ejecucion.md`](03_Entorno_Scripts_Ejecucion.md)
**Fases cubiertas:** Fase 4 (Entorno) + Fase 5 (Scripts) + Fase 6 (Ejecución)  
**Secciones:** IaC (Infrastructure as Code) · Validación del entorno · Framework de scripts (estructura, parametrización) · Ejecución controlada · Pre/Post execution checklists · Runbook de ejecución

**Ir aquí si necesitas:**
- Checklist para validar que el entorno está listo
- Estructura recomendada para organizar scripts
- Runbook paso a paso para ejecutar una prueba
- Saber qué hacer antes, durante y después de una ejecución

---

### [`04_Analisis_Optimizacion_Cierre.md`](04_Analisis_Optimizacion_Cierre.md)
**Fases cubiertas:** Fase 7 (Análisis) + Fase 8 (Optimización) + Fase 9 (Cierre)  
**Secciones:** Template de reporte ejecutivo (7 secciones) · Optimización iterativa · Re-testing strategy · Sign-off process · Retrospectiva (what went well, improve, action items, metrics) · Archivo de evidencias

**Ir aquí si necesitas:**
- Template completo para reporte ejecutivo
- Proceso de optimización iterativa (tune → test → validate)
- Criterios para dar sign-off formal
- Guía para retrospectiva de performance testing

---

## 🔗 Relación con otras categorías

| Desde aquí puedo ir a... | Para... |
|--------------------------|---------|
| [01_Introduccion](../ptlc-fundamentos/SKILL.md) | Entender los fundamentos antes de las fases |
| [04_Metricas](../ptlc-metricas-kpis/SKILL.md) | Definir qué medir (usado en Fases 1, 7) |
| [05_Herramientas](../ptlc-herramientas/SKILL.md) | Implementar scripts (Fase 5) |
| [06_Workload](../ptlc-workload-modeling/SKILL.md) | Calcular el modelo de carga (Fase 3) |
| [07_Monitoreo](../ptlc-monitoreo/SKILL.md) | Configurar observabilidad (Fase 4) |
| [09_Analisis](../ptlc-analisis-bottlenecks/SKILL.md) | Técnicas de RCA detalladas (Fase 7) |
