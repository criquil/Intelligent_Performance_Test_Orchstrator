---
name: ptlc-mejores-practicas
description: "Aplica practicas: CI/CD, shift-left, Kubernetes"
---

# 10 — Mejores Prácticas y Errores Comunes

> Índice intermedio. **Cuándo leer:** mejorar el proceso, integrarlo con CI/CD o evitar errores. Detalle en los documentos de esta skill (abajo).

## Top 10 Mejores Prácticas

| # | Práctica | Impacto |
|---|----------|---------|
| 1 | **Shift-Left:** Incluir performance desde el diseño | Detectar issues 10x más barato que en producción |
| 2 | **Automatizar en CI/CD:** Performance gates en pipeline | Prevenir regresiones automáticamente |
| 3 | **Baseline iterada:** Mínimo 3 ejecuciones, CV < 10% | Datos confiables para comparar |
| 4 | **Entorno representativo:** Mínimo 1:1 o explicar diferencia | Resultados extrapolables a producción |
| 5 | **Monitoreo end-to-end:** App + Infra + DB + Network | No hay puntos ciegos en el análisis |
| 6 | **Test data realista:** Volumen y variedad de producción | Evitar falsos positivos/negativos |
| 7 | **Thresholds como SLOs:** Criterios pass/fail automáticos | No depender de interpretación manual |
| 8 | **Documentar todo:** Plan, resultados, decisiones, RCA | Reproducibilidad y audit trail |
| 9 | **Performance budget:** Presupuesto por feature/endpoint | Accountability por equipo |
| 10 | **Retrospectiva:** Cerrar cada ciclo con lessons learned | Mejora continua del proceso |

## Top 10 Errores Comunes

| # | Error | Consecuencia |
|---|-------|--------------|
| 1 | No definir NFRs claros | No hay criterio de éxito medible |
| 2 | Ejecutar solo en modo GUI (JMeter) | Resultados contaminados por la UI |
| 3 | Think time = 0 | Carga irreal, saturación artificial |
| 4 | No correlacionar valores dinámicos | Scripts fallan al primer cambio |
| 5 | Ignorar ramp-up (carga instantánea) | Connection storms, cold-start masking |
| 6 | Test data insuficiente (1 user, 1 product) | Cache hit 100%, no refleja realidad |
| 7 | Entorno no representativo sin documentar | Resultados no extrapolables |
| 8 | No monitorear el load generator | No detectar saturación del generador |
| 9 | Una sola ejecución como baseline | CV alto, datos no confiables |
| 10 | Reportar solo promedios (no percentiles) | Ocultar problemas del tail latency |

---

## 📂 Contenido de la Subcarpeta

### [`01_CICD_y_Tendencias_Futuras.md`](01_CICD_y_Tendencias_Futuras.md) — CI/CD, budgets, cloud-native, tendencias
- Para qué: industrializar el performance testing y anticiparse a la industria.
- Consultar si: diseñas un pipeline con performance gates y rollback triggers · defines performance budgets por equipo o feature · validas tu proceso con el checklist de excellence

---

## 🔗 Relación con otras categorías

| Desde aquí puedo ir a... | Para... |
|--------------------------|---------|
| [ptlc-fases-del-ciclo](../ptlc-fases-del-ciclo/SKILL.md) | Integrar estas prácticas en cada fase |
| [ptlc-herramientas](../ptlc-herramientas/SKILL.md) | CI/CD específico de cada herramienta |
| [ptlc-monitoreo](../ptlc-monitoreo/SKILL.md) | Stack de observabilidad para CI/CD |
| [ptlc-tipos-de-pruebas](../ptlc-tipos-de-pruebas/SKILL.md) | Smoke testing en CI/CD, resiliency automático |