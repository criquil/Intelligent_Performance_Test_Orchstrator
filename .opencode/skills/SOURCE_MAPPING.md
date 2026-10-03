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

- `performance-tool-selector`
  - Consolida selección de herramientas para el contexto PTLC.
- `k6-performance-workflow`
  - Deriva de `k6-script-generator` y lo orienta a lifecycle, executors y thresholds.
- `jmeter-performance-workflow`
  - Deriva de `jmeter-test-plan-creator` + lineamientos de `151-java-performance-jmeter`.
- `gatling-performance-workflow`
  - Deriva de `gatling-scenario-creator` con foco en DSL e injection profiles.
- `locust-performance-workflow`
  - Deriva de `locust-test-creator` con foco en load shapes y distribución.
- `performance-test-strategy`
  - Consolida `load/stress/spike/soak/baseline` y planning.
- `performance-metrics-analysis`
  - Consolida `percentile/apdex/throughput/response-time`.
- `performance-diagnostics-rca`
  - Consolida profiling y RCA técnico de bottlenecks.

## Criterio de selección
- Se priorizaron skills alineadas a herramientas del repositorio (`k6`, `JMeter`, `Gatling`, `Locust`).
- Se agruparon skills muy granulares en skills operables y mantenibles para evitar duplicación.
- Se enlazó la documentación local en `.opencode/skills/` para mantener una única fuente de verdad.