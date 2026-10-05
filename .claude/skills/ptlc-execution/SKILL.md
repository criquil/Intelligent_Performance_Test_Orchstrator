---
name: ptlc-execution
description: "Ejecuta scripts k6, JMeter, Gatling, Locust"
---

# PTLC-EXECUTION — Definición y Ejecución de Pruebas

<role>

## Rol

Performance test engineer: generas scripts de calidad para la herramienta seleccionada (scenarios, thresholds, feeders) y ejecutas según el plan. Cada guía de herramienta trae un mapa de secciones al inicio: carga solo lo necesario (`grep -n "^## "` o `read` por offset).

</role>

<pre_execution>

## ⚠️ LECTURA OBLIGATORIA ANTES DE OPERAR

**Cargar `tests/performance/{selected_tool}/{plan_id}/context_envelope.json` si existe; no releer documentos ya sintetizados en él.**

**Leer exactamente lo listado; solo 2 documentos COMPLETOS. Sección = `grep -n "^## " <archivo>` + `read` offset/limit. Regla de herramienta: si `task_definition.selected_tool` (o `tool_selected`) falta, PREGUNTA; NUNCA leas las 4 guías, solo la seleccionada y sus secciones requeridas.**

### Documentos completos
- `.claude/skills/ptlc-herramientas/SKILL.md` — comparativa canónica de herramientas
- `.claude/skills/ptlc-scripting/SKILL.md` — panorama de patrones de scripting

### Lecturas por sección (comunes)
- `.claude/skills/ptlc-fases-del-ciclo/03_Entorno_Scripts_Ejecucion.md` §FASE 4 (3) — configuración del entorno
- `.claude/skills/ptlc-fases-del-ciclo/03_Entorno_Scripts_Ejecucion.md` §FASE 6 (441) → Pre-execution (450), Execution (461), Post-execution (487) — ejecución, limit 98
- `.claude/skills/ptlc-workload-modeling/01_Workload_Modeling_Exhaustivo.md` §Patrones de Tráfico (224) — perfiles de carga
- `.claude/skills/ptlc-scripting/01_Scripting_Avanzado.md` §Data Management Strategies (325) — feeders y datos
- `.claude/skills/ptlc-scripting/01_Scripting_Avanzado.md` §Error Handling Best Practices (392) — manejo de errores

### Lecturas por sección (solo `tool_selected`, solo lo requerido)
**Nota:** La skill `ptlc-herramientas` ahora solo contiene el cheat sheet. Consulta documentación oficial de cada herramienta para sintaxis específica:
- k6 → [Documentación oficial k6](https://grafana.com/k6/)
- JMeter → [Apache JMeter Documentation](https://jmeter.apache.org/documentation/)
- Gatling → [Gatling Docs](https://gatling.io/docs/)
- Locust → [Locust Docs](https://locust.readthedocs.io/)

Usa `.claude/skills/ptlc-herramientas/00b_Cheat_Sheet_Herramientas.md` para matriz de decisión y secciones comunes (CI/CD, troubleshooting).

**Presupuesto de lectura:** ninguna lectura >2.000 tokens; cargar secciones, no archivos completos; reutilizar `context_envelope.json`. Para fórmulas/umbrales/sintaxis usa `ptlc-workload-modeling/00_Cheat_Sheet_Workload.md` y `ptlc-herramientas/00b_Cheat_Sheet_Herramientas.md` antes que el doc completo.

</pre_execution>

<workflow>

## Flujo de Trabajo

1. **Leer plan completo:** `procedure_plan` (tipos, escenarios, VUs, criterios), `requirements` (endpoints, protocolo, datos, stack), `selected_tool`, `test_plan` (criterios definitivos).
2. **Crear estructura** solo para la herramienta seleccionada (`selected_tool`) en `tests/performance/{selected_tool}/{plan_id}/`: `{selected_tool}/scripts/`, `{selected_tool}/data/`, `{selected_tool}/config/`, `{selected_tool}/results/`, `README.md`.
3. **Generar scripts por tipo de prueba:**
   - k6: `executor` correcto (`ramping-vus`, `constant-arrival-rate`), `scenarios`, `thresholds`, `SharedArray`, `setup/default/teardown`.
   - JMeter: JMX con Thread Group (ramp-up, users, duration), CSV Data Set, Response/Duration Assertion, extractors, Backend Listener.
   - Gatling: DSL, `inject` (`rampUsers`, `constantUsersPerSec`, `stressPeakUsers`), `assertions`, `feeder`.
   - Locust: `HttpUser` con `tasks`/`wait_time`, `LoadTestShape`, `--headless`, `events`.
4. **Ejecutar** (si `execute = true`): smoke primero (2-3 min); si pasa, pruebas en orden; si falla, detener y reportar. Capturar stdout/stderr, CSV/JSON/HTML, tiempos.
5. **Empaquetar resultados** en `tests/performance/{selected_tool}/{plan_id}/results/` + resumen.

</workflow>

<output_format>

## Formato de Salida

Retornar SOLO JSON válido:

```json
{
  "status": "completed | failed | smoke_failed | skipped_execution",
  "plan_id": "string", "task_id": "string", "tool": "k6 | JMeter | Gatling | Locust",
  "scripts_generated": [{"test_type": "string", "file_path": "string", "description": "string"}],
  "execution_results": [{
    "test_type": "string", "status": "pass | fail | skipped", "duration_minutes": 0,
    "metrics": {"p95_ms": 0, "p99_ms": 0, "avg_ms": 0, "error_rate_pct": 0, "throughput_tps": 0, "peak_vus": 0},
    "thresholds_passed": true, "result_file": "string", "notes": "string"
  }],
  "overall_pass": true, "failed_thresholds": ["string"], "recommendations": ["string"], "confidence": 0.0
}
```

**Persistir el bloque `execution` del envelope y actualizar `meta.last_updated`.**

</output_format>

<rules>

## Reglas

- Requiere aprobación explícita del usuario (Approval Gate); sin `execute: true` aprobado, generar scripts y retornar `skipped_execution`.
- SIEMPRE smoke test primero; si falla, no continuar con pruebas mayores.
- Scripts reproducibles: sin valores hardcoded de ambiente, usar variables/config files.
- Thresholds DEBEN coincidir con los criterios de aceptación del test plan.
- Documentar cada script con comentarios explicando la configuración.
- JMeter: modo no-GUI (`-n -t test.jmx`). k6: incluir `--out json`.
- Citar el DOC de referencia de la herramienta en el README generado.

</rules>
