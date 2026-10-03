---
name: ptlc-fundamentos
description: "Define el PTLC: NFRs, RACI, ISO 25010, ISTQB, TMMi"
---

# 01 — Introducción al Performance Test Life Cycle (PTLC)

> Índice intermedio. **Cuándo leer:** qué es el PTLC, quién lo ejecuta, bajo qué estándares opera. Detalle en los documentos de esta skill (abajo).

## Resumen Ejecutivo

El **Performance Test Life Cycle (PTLC)** es una metodología estructurada de 9 fases para planificar, diseñar, ejecutar y gestionar pruebas de rendimiento. Su objetivo es garantizar que los sistemas cumplan criterios de velocidad, escalabilidad y estabilidad antes de llegar a producción.

### Las 9 Fases del PTLC

```
1. Recopilación de Requisitos    →  Entender NFRs y arquitectura
2. Planificación                  →  Estrategia, alcance, herramientas
3. Diseño de Pruebas             →  Casos de prueba y modelos de carga
4. Configuración del Entorno     →  Infraestructura y monitoreo
5. Desarrollo de Scripts         →  Codificar y parametrizar
6. Ejecución                     →  Ejecutar y monitorear
7. Análisis de Resultados        →  Interpretar datos y RCA
8. Optimización y Re-testing     →  Iterar hasta cumplir SLAs
9. Cierre                        →  Reporting final y retrospectiva
```

---

## 📂 Contenido de la Subcarpeta

### [`01_Definicion_y_Fundamentos.md`](01_Definicion_y_Fundamentos.md) — qué es PTLC, NFRs, glosario
- Para qué: introducir el ciclo y sus términos a stakeholders.
- Consultar si: necesitas una definición formal para un stakeholder · dudas entre performance testing y otros tipos de QA · buscas la definición de un término técnico

### [`02_Roles_y_Responsabilidades.md`](02_Roles_y_Responsabilidades.md) — roles, RACI, career path
- Para qué: definir quién responde en cada fase.
- Consultar si: armas un equipo de performance testing · elaboras la matriz RACI o el reporting a stakeholders · defines el career path del equipo

### [`03_Frameworks_y_Estandares.md`](03_Frameworks_y_Estandares.md) — ISO 25010, ISTQB, SRE, TMMi
- Para qué: justificar prácticas con estándares internacionales.
- Consultar si: implementas SLOs/SLIs al estilo Google SRE · evalúas la madurez del proceso (TMMi) · buscas regulaciones aplicables (financiero, salud)

---

## 🔗 Relación con otras categorías

| Desde aquí puedo ir a... | Para... |
|--------------------------|---------|
| [ptlc-tipos-de-pruebas](../ptlc-tipos-de-pruebas/SKILL.md) | Entender qué tipos de pruebas existen |
| [ptlc-fases-del-ciclo](../ptlc-fases-del-ciclo/SKILL.md) | Profundizar en la ejecución de cada fase |
| [ptlc-metricas-kpis](../ptlc-metricas-kpis/SKILL.md) | Definir los KPIs que se mencionan en los NFRs |