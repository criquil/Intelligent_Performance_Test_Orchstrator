---
name: ptlc-monitoreo
description: "Entorno y observabilidad para performance testing: Prometheus, Grafana, OpenTelemetry, Jaeger y alerting."
---

# 07 — Entorno de Pruebas y Monitoreo

> **Rol de este archivo:** Índice intermedio. Resume la infraestructura de monitoreo necesaria y dirige al documento exhaustivo.  
> **Cuándo leer este archivo:** Cuando necesitas configurar observabilidad, elegir stack de monitoreo, o entender qué instrumentar.  
> **Carpeta detallada:** [`.`](07_Entorno_y_Monitoreo/)

---

## Stack de Observabilidad para Performance Testing

```
┌─────────────────────────────────────────────────────┐
│                  VISUALIZACIÓN                        │
│         Grafana (dashboards, alertas)                │
├─────────────────────────────────────────────────────┤
│                 ALMACENAMIENTO                        │
│   Prometheus (métricas) │ Loki (logs) │ Tempo (traces)│
├─────────────────────────────────────────────────────┤
│                  RECOLECCIÓN                          │
│            OpenTelemetry Collector                    │
├─────────────────────────────────────────────────────┤
│                 INSTRUMENTACIÓN                       │
│  App metrics │ Node Exporter │ cAdvisor │ DB stats   │
└─────────────────────────────────────────────────────┘
```

### Los 3 Pilares de la Observabilidad

| Pilar | Herramienta | Pregunta que responde |
|-------|-------------|----------------------|
| **Métricas** | Prometheus + Grafana | ¿Cuánto? ¿Qué tan rápido? ¿Qué tan saturado? |
| **Logs** | Loki / ELK | ¿Qué pasó exactamente? ¿Qué errores ocurrieron? |
| **Traces** | Jaeger / Tempo | ¿Dónde se consume el tiempo? ¿Qué servicio es lento? |

---

## 📂 Contenido de la Subcarpeta

### [`01_Monitoreo_y_Observabilidad.md`](01_Monitoreo_y_Observabilidad.md)
**Contenido completo (~14.5 KB):**

| Sección | Qué encontrarás |
|---------|-----------------|
| Stack de Observabilidad Moderno | Arquitectura completa, componentes, flujo de datos |
| Prometheus + Grafana Stack | Instalación, configuración, scraping, service discovery |
| PromQL | Queries esenciales para performance testing (rate, histogram_quantile, etc.) |
| OpenTelemetry | SDK setup, auto-instrumentation, propagation, collector config |
| Alerting para Performance Testing | Reglas de alerta, routing, escalation, ejemplo Alertmanager |
| Monitoreo de Base de Datos | Queries lentas, connections, locks, buffer hit ratio |
| Docker Compose Stack Completo | Config listo para copiar: Prometheus + Grafana + Loki + Node Exporter |

**Ir aquí si necesitas:**
- Docker Compose para levantar un stack de monitoreo completo
- Queries PromQL para dashboards de performance
- Configurar OpenTelemetry para tracing distribuido
- Reglas de alerting durante una ejecución de performance test
- Monitorear bases de datos (PostgreSQL, MySQL, MongoDB)

---

## 🔗 Relación con otras categorías

| Desde aquí puedo ir a... | Para... |
|--------------------------|---------|
| [03_Fases](../ptlc-fases-del-ciclo/SKILL.md) | Fase 4 (Configuración del Entorno) |
| [04_Metricas](../ptlc-metricas-kpis/SKILL.md) | Qué métricas recolectar |
| [09_Analisis](../ptlc-analisis-bottlenecks/SKILL.md) | Cómo interpretar lo que el monitoreo muestra |
| [05_Herramientas](../ptlc-herramientas/SKILL.md) | Output/export de herramientas hacia Prometheus/Grafana |
