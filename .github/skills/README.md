# PTLC Skills Pack

Este paquete agrega skills reutilizables para agentes en este repositorio.

## Skills Incluidas

- `performance-tool-selector`: Selecciona la herramienta adecuada (k6, JMeter, Gatling, Locust).
- `k6-performance-workflow`: Flujo de trabajo de k6 para diseño, ejecución y análisis.
- `jmeter-performance-workflow`: Flujo de trabajo de JMeter, incluyendo modo no-GUI y estructura de plan.
- `gatling-performance-workflow`: Flujo de trabajo de Gatling con DSL e injection profiles.
- `locust-performance-workflow`: Flujo de trabajo de Locust con user classes, load shapes y modo distribuido.
- `performance-test-strategy`: Diseña estrategia de pruebas (load, stress, spike, soak, baseline).
- `performance-metrics-analysis`: Analiza percentiles, Apdex, throughput y criterios pass/fail.
- `performance-diagnostics-rca`: Realiza RCA técnico con foco en bottlenecks de app, DB y red.

## Fuentes Consideradas

- `jeremylongshore/claude-code-plugins-plus-skills` (categoría `10-performance-testing`)
- `jabrena/cursor-rules-java` (skill `151-java-performance-jmeter`)

Estas skills fueron adaptadas al contexto PTLC de este repositorio y enlazan la documentación local en `DOCs/`.