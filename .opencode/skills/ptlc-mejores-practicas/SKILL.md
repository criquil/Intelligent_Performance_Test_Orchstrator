---
name: ptlc-mejores-practicas
description: "Mejores practicas y errores comunes de performance testing: CI/CD, shift-left, microservicios, Kubernetes y tendencias."
---

# 10 — Mejores Prácticas y Errores Comunes

> **Rol de este archivo:** Índice intermedio. Resume best practices, integración CI/CD, errores a evitar, y tendencias futuras.  
> **Cuándo leer este archivo:** Cuando necesitas mejorar tu proceso, integrarlo con CI/CD, evitar errores, o explorar nuevas tendencias.  
> **Carpeta detallada:** [`.`](10_Mejores_Practicas/)

---

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

### [`01_CICD_y_Tendencias_Futuras.md`](01_CICD_y_Tendencias_Futuras.md)
**Contenido completo (~15 KB):**

| Sección | Qué encontrarás |
|---------|-----------------|
| Performance Testing en CI/CD | Pipeline design, gates, smoke vs full, rollback triggers |
| Performance Budgets | Cómo definir, asignar y enforcement por equipo |
| Microservicios | Estrategias para testing distribuido, service mesh, contract testing |
| Cloud-Native Performance Testing | K8s, serverless, auto-scaling validation, ephemeral envs |
| Tendencias Futuras (2025-2027) | AI/ML para análisis, AIOps, chaos engineering mainstream, observability-driven testing |
| Checklist Final | Performance Testing Excellence checklist completo |

**Ir aquí si necesitas:**
- Diseñar un pipeline de CI/CD con performance gates
- Implementar performance budgets por equipo/feature
- Estrategia de performance testing para microservicios
- Entender hacia dónde va la industria
- Checklist para validar tu proceso completo

---

## 🔗 Relación con otras categorías

| Desde aquí puedo ir a... | Para... |
|--------------------------|---------|
| [03_Fases](../ptlc-fases-del-ciclo/SKILL.md) | Integrar estas prácticas en cada fase |
| [05_Herramientas](../ptlc-herramientas/SKILL.md) | CI/CD específico de cada herramienta |
| [07_Monitoreo](../ptlc-monitoreo/SKILL.md) | Stack de observabilidad para CI/CD |
| [02_Tipos](../ptlc-tipos-de-pruebas/SKILL.md) | Smoke testing en CI/CD, resiliency automático |
