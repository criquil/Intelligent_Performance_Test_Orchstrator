# Source Mapping: External to Local Skills

## Repositorios fuente
- `jeremylongshore/claude-code-plugins-plus-skills`
- `jabrena/cursor-rules-java`

## Skills externas identificadas como relevantes

### Herramientas
- `k6-script-generator`
- `jmeter-test-plan-creator`
- `gatling-scenario-creator`
- `locust-test-creator`

### Estrategia de pruebas
- `load-test-scenario-planner`
- `stress-test-config`
- `spike-test-setup`
- `soak-test-planner`
- `benchmark-suite-creator`
- `performance-baseline-creator`

### Análisis y técnicas
- `bottleneck-identifier`
- `response-time-analyzer`
- `percentile-analyzer`
- `throughput-calculator`
- `apdex-score-calculator`
- `database-query-profiler`
- `connection-pool-analyzer`
- `network-latency-tester`
- `cpu-profiler-config`
- `memory-profiler-setup`
- `thread-dump-analyzer`
- `gc-log-analyzer`
- `heap-dump-analyzer`
- `flame-graph-generator`

### Java + JMeter
- `151-java-performance-jmeter`

## Adaptación local aplicada

Las skills externas listadas arriba se consolidaron directamente en las skills de conocimiento `ptlc-*`, sin skills intermedias:

- Guías por herramienta + matriz de decisión → `.claude/skills/ptlc-herramientas/`
- `load/stress/spike/soak/baseline` y planning → `.claude/skills/ptlc-tipos-de-pruebas/` y `ptlc-workload-modeling/`
- `percentile/apdex/throughput/response-time` → `.claude/skills/ptlc-metricas-kpis/`
- Profiling y RCA de bottlenecks → `.claude/skills/ptlc-analisis-bottlenecks/`

## Criterio de selección
- Se priorizaron skills alineadas a herramientas del repositorio (`k6`, `JMeter`, `Gatling`, `Locust`).
- Se agruparon skills muy granulares en skills operables y mantenibles para evitar duplicación.
- Se enlazó la documentación local en `.claude/skills/` para mantener una única fuente de verdad.