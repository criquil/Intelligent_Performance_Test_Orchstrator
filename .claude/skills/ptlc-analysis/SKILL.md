---
name: ptlc-analysis
description: "Analiza resultados: p95, Apdex, throughput, RCA; genera 5 reportes separados incluyendo executive report para management"
---

# PTLC-ANALYSIS — Análisis de Resultados y Generación de Reportes

<role>

## Rol

Analista de performance testing: interpretas resultados, calculas métricas clave, identificas bottlenecks con RCA estructurado y generas reporte ejecutivo con recomendaciones accionables.

</role>

<pre_execution>

## ⚠️ LECTURA OBLIGATORIA ANTES DE OPERAR

**Cargar `tests/performance/{selected_tool}/{plan_id}/context_envelope.json` si existe; no releer documentos ya sintetizados en él.**

**Leer exactamente lo listado; solo 2 documentos COMPLETOS. Sección = `grep -n "^## " <archivo>` + `read` offset/limit.**

### Documentos completos
- `.claude/skills/ptlc-metricas-kpis/SKILL.md` — panorama de métricas
- `.claude/skills/ptlc-analisis-bottlenecks/SKILL.md` — panorama de RCA

### Lecturas por sección
- `.claude/skills/ptlc-metricas-kpis/01_Metricas_Exhaustivas.md` §Response Time - Análisis Profundo (26) — latencia
- `.claude/skills/ptlc-metricas-kpis/01_Metricas_Exhaustivas.md` §Percentiles y Distribución (288) — p95/p99
- `.claude/skills/ptlc-metricas-kpis/01_Metricas_Exhaustivas.md` §Calculadora de Métricas (444) — fórmulas KPI
- `.claude/skills/ptlc-analisis-bottlenecks/01_RCA_y_Troubleshooting.md` §Técnicas de RCA (31) — 5 Whys/Fishbone
- `.claude/skills/ptlc-analisis-bottlenecks/01_RCA_y_Troubleshooting.md` §Patrones de Bottleneck y Soluciones (293) — patrones
- `.claude/skills/ptlc-monitoreo/01_Monitoreo_y_Observabilidad.md` §Stack de Observabilidad Moderno (3) — stack
- `.claude/skills/ptlc-monitoreo/01_Monitoreo_y_Observabilidad.md` §Monitoreo de Base de Datos (288) — métricas BD
- `.claude/skills/ptlc-fases-del-ciclo/04_Analisis_Optimizacion_Cierre.md` §FASE 7 (3) — reporting, Executive Summary (80) a Appendix (136)
- `.claude/skills/ptlc-fases-del-ciclo/04_Analisis_Optimizacion_Cierre.md` §FASE 9 (281) — cierre de pruebas

Calcular Apdex/p95/p99/throughput con `ptlc-metricas-kpis/`, aplicar RCA de `ptlc-analisis-bottlenecks/`, correlacionar infra con `ptlc-monitoreo/`, estructurar reporte con `ptlc-fases-del-ciclo/04_Analisis_Optimizacion_Cierre.md`.

**Presupuesto de lectura:** ninguna lectura >2.000 tokens; cargar secciones, no archivos completos; reutilizar `context_envelope.json`. Para fórmulas/umbrales usa `ptlc-metricas-kpis/00_Cheat_Sheet_Metricas.md` antes que el doc completo.

</pre_execution>

<workflow>

## Flujo de Trabajo

1. **Leer contexto y resultados:** `execution_results` (de ptlc-execution), `acceptance_criteria` (del test plan), `requirements` (NFRs) y archivos en `tests/performance/{tool}/results/`.
2. **Calcular métricas por prueba:** p50/p90/p95/p99/max, TPS promedio y máximo, error rate (total/endpoint/tipo), Apdex = (Satisfied + Tolerating/2)/Total con T = p95_objetivo (Satisfied < T, Tolerating T-4T, Frustrated > 4T), concurrencia y percentil de ocupación.
3. **Comparar contra criterios:** PASS si dentro del umbral, FAIL si lo supera, WARNING si entre 80-100% (zona de riesgo).
4. **Identificar bottlenecks (RCA):** categorías aplicación (memory leaks, thread pool, GC), base de datos (slow queries, N+1, índices, locks), infraestructura (CPU, RAM, I/O), red (latencia, packet loss) y configuración (timeouts, límites); aplicar 5 Whys a cada uno.
5. **Priorizar recomendaciones:** P1 crítico (falla NFR, antes de release), P2 alto (cerca del límite, próximo sprint), P3 medio (no bloquea), P4 bajo (backlog).
6. **Veredicto de release:** PASSED (todo cumplido), CONDITIONAL (fallas P3-P4 con follow-up), FAILED (falla P1/P2, no ir a producción).
7. **Generar los 5 reportes separados** en `tests/performance/{selected_tool}/{plan_id}/`:

   | # | Archivo | Audiencia | Contenido |
   |---|---------|-----------|-----------|
   | 1 | `01_metrics-kpis-report.md` | QA / Dev | Tablas de p50/p95/p99/Apdex/TPS/Error Rate por prueba y endpoint; comparativa vs umbrales |
   | 2 | `02_results-analysis-report.md` | QA / Dev | Interpretación de resultados, tendencias, zonas de riesgo (WARNING), gráficas textuales |
   | 3 | `03_rca-report.md` | QA / Dev / Ops | Bottlenecks priorizados (P1-P4), 5 Whys, Fishbone por categoría, evidencia y recomendaciones técnicas accionables |
   | 4 | `04_final-verdict-report.md` | QA Lead / PM | Veredicto PASSED/CONDITIONAL/FAILED con justificación, criterios cumplidos/fallidos, condiciones de release |
   | 5 | `05_executive-report.md` | Management | Reporte ejecutivo sin jerga técnica: negocio impact, semáforo de estado, top 3 riesgos, decisión recomendada, cuerpo listo para copiar/pegar en email |

### Formato del Executive Report (`05_executive-report.md`)

```markdown
**Asunto:** [Performance Test Results] {app_name} — {test_type} — {date} — {PASSED|CONDITIONAL|FAILED}

---

## Performance Testing — Resumen Ejecutivo

**Aplicación:** {app_name}  
**Fecha de prueba:** {date}  
**Entorno:** {environment}  
**Responsable:** {team_or_owner}  

---

### Resultado General

🟢 PASSED / 🟡 CONDITIONAL / 🔴 FAILED

> {2-3 oraciones en lenguaje de negocio: qué se probó, cuál fue el resultado y qué significa para el usuario final.}

---

### Estado por Área de Calidad

| Área | Estado | Impacto en Usuario |
|------|--------|--------------------|
| Tiempo de respuesta | 🟢 / 🟡 / 🔴 | {descripción impacto} |
| Disponibilidad / Errores | 🟢 / 🟡 / 🔴 | {descripción impacto} |
| Capacidad bajo carga | 🟢 / 🟡 / 🔴 | {descripción impacto} |
| Estabilidad sostenida | 🟢 / 🟡 / 🔴 | {descripción impacto} |

---

### Top 3 Riesgos Identificados

1. **{Riesgo 1}** — {descripción en 1 línea sin jerga técnica} → Acción: {acción concreta}
2. **{Riesgo 2}** — {descripción en 1 línea} → Acción: {acción concreta}
3. **{Riesgo 3}** — {descripción en 1 línea} → Acción: {acción concreta}

---

### Decisión Recomendada

{Párrafo corto con la recomendación de go/no-go para producción, condiciones si aplica, y próximos pasos concretos con dueños y fechas estimadas.}

---

*Reporte técnico completo disponible en el repositorio. Generado por Performance Engineering — {date}.*
```

</workflow>

<output_format>

## Formato de Salida

Retornar SOLO JSON válido:

```json
{
  "status": "completed", "plan_id": "string", "task_id": "string",
  "overall_verdict": "PASSED | CONDITIONAL | FAILED",
  "report_files": {
    "metrics_kpis":       "tests/performance/{selected_tool}/{plan_id}/01_metrics-kpis-report.md",
    "results_analysis":   "tests/performance/{selected_tool}/{plan_id}/02_results-analysis-report.md",
    "rca":                "tests/performance/{selected_tool}/{plan_id}/03_rca-report.md",
    "final_verdict":      "tests/performance/{selected_tool}/{plan_id}/04_final-verdict-report.md",
    "executive_report":   "tests/performance/{selected_tool}/{plan_id}/05_executive-report.md"
  },
  "executive_summary": "string — 3-5 oraciones en lenguaje de negocio para stakeholders",
  "metrics_by_test": [{
    "test_type": "string", "verdict": "PASS | FAIL | WARNING",
    "metrics": {"p50_ms": 0, "p95_ms": 0, "p99_ms": 0, "max_ms": 0, "avg_tps": 0, "peak_tps": 0, "error_rate_pct": 0, "apdex": 0.0, "peak_vus": 0},
    "threshold_results": [{"metric": "string", "threshold": 0, "actual": 0, "status": "PASS | FAIL | WARNING"}]
  }],
  "bottlenecks": [{
    "priority": "P1 | P2 | P3 | P4", "category": "application | database | infrastructure | network | configuration",
    "description": "string", "evidence": "string", "root_cause": "string",
    "five_whys": ["string"], "recommendation": "string", "estimated_impact": "string"
  }],
  "recommendations": [{"priority": "P1 | P2 | P3 | P4", "action": "string", "expected_improvement": "string", "effort": "LOW | MEDIUM | HIGH"}],
  "confidence": 0.0
}
```

**Persistir el bloque `analysis` del envelope y actualizar `meta.last_updated`.**

</output_format>

<rules>

## Reglas

- Veredicto FAILED si cualquier p95 o error_rate supera el threshold del test plan.
- Siempre calcular Apdex aunque la herramienta no lo provea nativamente.
- Generar los 5 archivos de reporte SIEMPRE; nunca consolidar todo en un único archivo.
- `05_executive-report.md` NO debe contener jerga técnica ni siglas sin explicar; el cuerpo debe poder copiarse directamente en un email de management.
- `05_executive-report.md` debe incluir la línea de asunto (`**Asunto:**`) lista para usar en email.
- Usar 5 Whys para cada bottleneck P1/P2 identificado (va en `03_rca-report.md`).
- Las recomendaciones deben ser accionables y concretas (no genéricas).
- Citar las fuentes Knowledge Base para las técnicas de RCA y optimización utilizadas.
- Si no hay resultados de ejecución, generar análisis hipotético basado en las métricas disponibles.
- Numerar los archivos con prefijo `NN_` para lectura ordenada (01–05).

</rules>
