# CONTEXT_ENVELOPE — Contexto acumulado del ciclo PTLC

> Artefacto único por `plan_id` que acumula las conclusiones sintetizadas de cada fase del pipeline, para que las siguientes **no vuelvan a leer** los mismos documentos. Ruta: `tests/performance/{selected_tool}/{plan_id}/context_envelope.json`.

## Regla de escritura

- Cada fase escribe **solo su bloque** y actualiza `meta.last_updated`.
- Nunca borra ni reescribe bloques de otras fases.
- Antes de leer un documento del knowledge base, consultar si su conclusión ya está sintetizada aquí.

```json
{
  "meta": {
    "plan_id": "YYYYMMDD-nombre-sistema",
    "objective": "string",
    "domain": "performance-testing",
    "created": "ISO-8601",
    "last_updated": "ISO-8601"
  },
  "intake": {
    "system_description": "string",
    "requirements": ["string"],
    "nfrs": { "p95_ms": 0, "p99_ms": 0, "max_error_rate_pct": 0, "target_tps": 0 },
    "constraints": ["string"],
    "tool_selected": "k6 | JMeter | Gatling | Locust",
    "protocol": "HTTP | gRPC | WebSocket | JDBC | mixed"
  },
  "diagnostics": {
    "readiness_score": 0,
    "gaps": ["string"],
    "risks": [{ "severity": "HIGH | MEDIUM | LOW", "description": "string", "mitigation": "string" }],
    "environment": { "prod_parity": "full | partial | none", "monitoring_stack": ["string"], "observability": "string" }
  },
  "procedure": {
    "test_types": ["load", "stress", "soak"],
    "workload_model": {
      "nominal_vus": 0, "peak_vus": 0, "stress_vus": 0,
      "ramp_up": "string", "duration_minutes": 0,
      "distributions": [{ "scenario": "string", "weight_pct": 0 }]
    },
    "acceptance_criteria": { "p95_ms": 0, "p99_ms": 0, "max_error_rate_pct": 0, "min_throughput_tps": 0, "apdex": 0 }
  },
  "test_plan": {
    "path": "tests/performance/{selected_tool}/{plan_id}/performance-test-plan.md",
    "scope": "string",
    "entry_criteria": ["string"],
    "exit_criteria": ["string"],
    "approved": false
  },
  "execution": {
    "tool": "k6 | JMeter | Gatling | Locust",
    "script_paths": ["string"],
    "run_id": "string",
    "raw_results_path": "string",
    "smoke_result": "pass | fail | skipped",
    "summary_metrics": { "p95_ms": 0, "error_rate_pct": 0, "throughput_tps": 0 }
  },
  "analysis": {
    "verdict": "PASSED | CONDITIONAL | FAILED",
    "metrics": { "p50_ms": 0, "p95_ms": 0, "p99_ms": 0, "throughput_tps": 0, "error_rate_pct": 0, "apdex": 0 },
    "bottlenecks": [{ "priority": "P1 | P2 | P3 | P4", "category": "string", "description": "string", "root_cause": "string" }],
    "recommendations": [{ "priority": "P1 | P2 | P3 | P4", "action": "string", "effort": "LOW | MEDIUM | HIGH" }]
  }
}
```

## Bloques: quién escribe y quién lee

| Bloque | Escribe (fase) | Lee (fases) |
|--------|----------------|-------------|
| `meta` | cada fase actualiza `last_updated`; `ptlc-orchestrator` lo crea en Phase 2 | todas + orquestador |
| `intake` | `ptlc-intake` | diagnostics, procedure, test-plan, execution, analysis |
| `diagnostics` | `ptlc-diagnostics` | procedure, test-plan, execution |
| `procedure` | `ptlc-procedure-plan` | test-plan, execution, analysis |
| `test_plan` | `ptlc-test-plan` | execution, analysis |
| `execution` | `ptlc-execution` | analysis |
| `analysis` | `ptlc-analysis` | orquestador (cierre) |

## Cheat sheets (fórmulas y umbrales: leer antes que el documento completo)

- Métricas y umbrales → `.claude/skills/ptlc-metricas-kpis/00_Cheat_Sheet_Metricas.md`
- Workload y VUs → `.claude/skills/ptlc-workload-modeling/00_Cheat_Sheet_Workload.md`
- Herramientas → `.claude/skills/ptlc-herramientas/00b_Cheat_Sheet_Herramientas.md`

## Envelope vs. plan.yaml

- `plan.yaml` = **estado** de las fases (wave, status, depends_on). Lo gestiona `ptlc-orchestrator`.
- `context_envelope.json` = **conclusiones sintetizadas** de las fases. Lo escriben las skills.
