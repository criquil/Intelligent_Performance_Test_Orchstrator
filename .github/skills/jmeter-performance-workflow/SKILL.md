---
name: jmeter-performance-workflow
description: Usa esta skill para planificar y ejecutar pruebas con JMeter en modo no-GUI, definiendo thread groups, ramp-up, loops, extractores, correlación y reportes.
---

# JMeter Performance Workflow

## Referencias
- [.github/skills/ptlc-herramientas/05_JMeter_Guia_Completa.md](../ptlc-herramientas/05_JMeter_Guia_Completa.md)
- [.github/skills/ptlc-herramientas/SKILL.md](../ptlc-herramientas/SKILL.md)

## Flujo
1. Define test plan mínimo reproducible con objetivo claro.
2. Configura `Thread Group` con usuarios, ramp-up y loops.
3. Implementa correlación y parametrización (CSV, extractores, variables).
4. Ejecuta en modo CLI/no-GUI para resultados válidos de performance.
5. Analiza dashboard HTML y registra cuellos de botella.

## Nota de Integración
Incluye criterios inspirados en la skill `151-java-performance-jmeter` para escenarios Java, priorizando ejecución desde raíz de proyecto y parámetros explícitos de carga.
