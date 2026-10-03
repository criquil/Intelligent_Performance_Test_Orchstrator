---
name: ptlc-monitoreo
description: "Configura Prometheus, Grafana, OpenTelemetry, Jaeger"
---

# 07 — Entorno de Pruebas y Monitoreo

> Índice intermedio. **Cuándo leer:** configurar observabilidad, elegir stack o saber qué instrumentar. Detalle en los documentos de esta skill (abajo).

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

### [`01_Monitoreo_y_Observabilidad.md`](01_Monitoreo_y_Observabilidad.md) — stack moderno, PromQL, OTel, alerting
- Para qué: levantar y configurar la observabilidad de una ejecución.
- Consultar si: copias el Docker Compose de Prometheus + Grafana + Loki + Node Exporter · escribes queries PromQL o reglas de alerting · monitoreas bases de datos (PostgreSQL, MySQL, MongoDB)

---

## 🔗 Relación con otras categorías

| Desde aquí puedo ir a... | Para... |
|--------------------------|---------|
| [ptlc-fases-del-ciclo](../ptlc-fases-del-ciclo/SKILL.md) | Fase 4 (Configuración del Entorno) |
| [ptlc-metricas-kpis](../ptlc-metricas-kpis/SKILL.md) | Qué métricas recolectar |
| [ptlc-analisis-bottlenecks](../ptlc-analisis-bottlenecks/SKILL.md) | Cómo interpretar lo que el monitoreo muestra |
| [ptlc-herramientas](../ptlc-herramientas/SKILL.md) | Output/export de herramientas hacia Prometheus/Grafana |