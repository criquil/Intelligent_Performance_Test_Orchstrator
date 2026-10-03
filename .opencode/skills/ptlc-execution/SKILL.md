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

**Cargar `docs/plan/{plan_id}/context_envelope.json` si existe; no releer documentos ya sintetizados en él.**

**Leer exactamente lo listado; solo 2 documentos COMPLETOS. Sección = `grep -n "^## " <archivo>` + `read` offset/limit. Regla de herramienta: si `task_definition.selected_tool` (o `tool_selected`) falta, PREGUNTA; NUNCA leas las 4 guías, solo la seleccionada y sus secciones requeridas.**

### Documentos completos
- `.opencode/skills/ptlc-herramientas/SKILL.md` — comparativa canónica de herramientas
- `.opencode/skills/ptlc-scripting/SKILL.md` — panorama de patrones de scripting

### Lecturas por sección (comunes)
- `.opencode/skills/ptlc-fases-del-ciclo/03_Entorno_Scripts_Ejecucion.md` §FASE 4 (3) — configuración del entorno
- `.opencode/skills/ptlc-fases-del-ciclo/03_Entorno_Scripts_Ejecucion.md` §FASE 6 (441) → Pre-execution (450), Execution (461), Post-execution (487) — ejecución, limit 98
- `.opencode/skills/ptlc-workload-modeling/01_Workload_Modeling_Exhaustivo.md` §Patrones de Tráfico (224) — perfiles de carga
- `.opencode/skills/ptlc-scripting/01_Scripting_Avanzado.md` §Data Management Strategies (325) — feeders y datos
- `.opencode/skills/ptlc-scripting/01_Scripting_Avanzado.md` §Error Handling Best Practices (392) — manejo de errores
- `.opencode/skills/ptlc-herramientas/00_Comunes_Guia_Herramientas.md` §3.1 Prácticas (267) — mejores prácticas
- `.opencode/skills/ptlc-herramientas/00_Comunes_Guia_Herramientas.md` §3.2 Antipatrones (282) — antipatrones
- `.opencode/skills/ptlc-herramientas/00_Comunes_Guia_Herramientas.md` §1.7 Quality gate (151) — check_thresholds.py

### Lecturas por sección (solo `tool_selected`, solo lo requerido)
Guías en `.opencode/skills/ptlc-herramientas/`:
- k6 `06_k6_Guia_Completa_Expandida.md` §5 Executors (392), §6 Scenarios (575), §9 Thresholds (931), §4 Lifecycle (227), §11 Datos/Parametrización (1163)
- JMeter `05_JMeter_Guia_Completa.md` §5 Thread Groups (310), §9 Extractors/Correlation (595), §10 Assertions (688), §17 CLI (1191)
- Gatling `04_Gatling_Community_Guia_Completa.md` §12 Injection Profiles (1303), §15 Assertions (1689), §11 Feeders (1203)
- Locust `03_Locust_Guia_Completa.md` §5 User Classes (462), §9 Custom Load Shapes (1032), §8 Wait Times/Pacing (943)

Aplicar patrones de carga de `ptlc-workload-modeling/`, scripting de `ptlc-scripting/` y sintaxis de la guía de la herramienta.

**Presupuesto de lectura:** ninguna lectura >2.000 tokens; cargar secciones, no archivos completos; reutilizar `context_envelope.json`. Para fórmulas/umbrales/sintaxis usa `ptlc-workload-modeling/00_Cheat_Sheet_Workload.md` y `ptlc-herramientas/00b_Cheat_Sheet_Herramientas.md` antes que el doc completo.

</pre_execution>

<workflow>

## Flujo de Trabajo

1. **Leer plan completo:** `procedure_plan` (tipos, escenarios, VUs, criterios), `requirements` (endpoints, protocolo, datos, stack), `selected_tool`, `test_plan` (criterios definitivos).
2. **Crear estructura** en `tests/performance/`: `{tool}/scripts/`, `{tool}/data/`, `{tool}/config/`, `{tool}/results/`, `README.md`.
3. **Generar scripts por tipo de prueba:**
   - k6: `executor` correcto (`ramping-vus`, `constant-arrival-rate`), `scenarios`, `thresholds`, `SharedArray`, `setup/default/teardown`.
   - JMeter: JMX con Thread Group (ramp-up, users, duration), CSV Data Set, Response/Duration Assertion, extractors, Backend Listener.
   - Gatling: DSL, `inject` (`rampUsers`, `constantUsersPerSec`, `stressPeakUsers`), `assertions`, `feeder`.
   - Locust: `HttpUser` con `tasks`/`wait_time`, `LoadTestShape`, `--headless`, `events`.
4. **Ejecutar** (si `execute = true`): smoke primero (2-3 min); si pasa, pruebas en orden; si falla, detener y reportar. Capturar stdout/stderr, CSV/JSON/HTML, tiempos.
5. **Empaquetar resultados** en `tests/performance/{tool}/results/` + resumen.

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
