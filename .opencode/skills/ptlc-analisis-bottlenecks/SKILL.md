---
name: ptlc-analisis-bottlenecks
description: "Analisis de resultados y RCA de bottlenecks: 5 Whys, Fishbone, drill-down y profiling de aplicacion, base de datos y red."
---

# 09 — Análisis de Resultados y Bottlenecks

> **Rol de este archivo:** Índice intermedio. Resume las técnicas de análisis, RCA y troubleshooting, y dirige al documento con frameworks completos.  
> **Cuándo leer este archivo:** Cuando necesitas interpretar resultados, encontrar la causa raíz de un problema, o hacer profiling.  
> **Carpeta detallada:** [`.`](09_Analisis_y_Bottlenecks/)

---

## Framework de Análisis — 4 Pasos

```
1. OBSERVAR    → Identificar síntomas (response time alto, errors, saturación)
2. CORRELACIONAR → Cruzar métricas de app + infra + logs + traces
3. AISLAR      → Determinar componente/capa responsable
4. VALIDAR     → Confirmar hipótesis con evidencia (profiling, reproduce)
```

### Síntomas Comunes y Dónde Buscar

| Síntoma | Probable causa | Primer lugar a mirar |
|---------|----------------|---------------------|
| Response time crece linealmente con VUs | CPU bottleneck | CPU utilization, thread pool |
| Response time crece exponencialmente | Queue saturation | Connection pool, thread pool size |
| Errors 5xx bajo carga | Resource exhaustion | Memory, file descriptors, connections |
| Throughput se estanca (flat) | Bottleneck upstream | DB connections, external service |
| Memory crece sin parar | Memory leak | Heap dumps, object allocation |
| Latencia intermitente (spikes) | GC pauses o I/O waits | GC logs, disk I/O latency |

### Técnicas de RCA (Root Cause Analysis)

| Técnica | Cuándo usarla |
|---------|---------------|
| **5 Whys** | Problema simple con causa lineal |
| **Fishbone / Ishikawa** | Múltiples posibles causas (categorizar) |
| **Drill-Down** | Localizar en qué capa/componente está el problema |
| **Comparative Analysis** | Comparar ejecución buena vs mala |
| **Profiling** | Cuando ya sabes el componente pero no la línea de código |

---

## 📂 Contenido de la Subcarpeta

### [`01_RCA_y_Troubleshooting.md`](01_RCA_y_Troubleshooting.md)
**Contenido completo (~14 KB):**

| Sección | Qué encontrarás |
|---------|-----------------|
| Framework de Análisis Sistemático | Proceso paso a paso, decision tree |
| Técnicas de RCA | 5 Whys con ejemplos, Fishbone template, drill-down methodology |
| Troubleshooting por Síntoma | Tabla extendida: síntoma → diagnóstico → solución |
| Herramientas de Profiling | CPU profilers, memory analyzers, I/O tools, network capture |
| Patrones de Bottleneck y Soluciones | CPU-bound, memory-bound, I/O-bound, network-bound, lock contention — con soluciones concretas |

**Ir aquí si necesitas:**
- Diagnosticar por qué un test falló
- Decision tree para identificar tipo de bottleneck
- Herramientas de profiling por lenguaje/plataforma
- Soluciones concretas para cada tipo de cuello de botella
- Template para documentar un RCA formal

---

## 🔗 Relación con otras categorías

| Desde aquí puedo ir a... | Para... |
|--------------------------|---------|
| [04_Metricas](../ptlc-metricas-kpis/SKILL.md) | Entender qué significan las métricas que veo |
| [07_Monitoreo](../ptlc-monitoreo/SKILL.md) | Verificar que tengo suficiente observabilidad |
| [03_Fases](../ptlc-fases-del-ciclo/SKILL.md) | Fase 7 (Análisis) y Fase 8 (Optimización) |
| [02_Tipos](../ptlc-tipos-de-pruebas/SKILL.md) | Pruebas de isolation/configuration para confirmar RCA |
