---
name: k6-performance-workflow
description: Usa esta skill para diseñar, generar y revisar pruebas de rendimiento con k6, incluyendo lifecycle, executors, scenarios, thresholds y análisis de resultados.
---

# k6 Performance Workflow

## Referencias
- [.github/skills/ptlc-herramientas/06_k6_Guia_Completa_Expandida.md](../ptlc-herramientas/06_k6_Guia_Completa_Expandida.md)
- [.github/skills/ptlc-metricas-kpis/SKILL.md](../ptlc-metricas-kpis/SKILL.md)

## Flujo
1. Define objetivo y criterio pass/fail con `thresholds`.
2. Selecciona `executor` adecuado (vus o arrival-rate) según workload esperado.
3. Diseña `scenarios` y datos de prueba con foco en realismo y repetibilidad.
4. Ejecuta prueba y revisa p95/p99, tasa de error y throughput.
5. Resume hallazgos y acciones de mejora priorizadas.
