---
name: ptlc-analisis-bottlenecks
description: "Analiza bottlenecks: RCA, 5 Whys, Fishbone"
---

# 09 — Análisis de Resultados y Bottlenecks

> Índice intermedio. **Cuándo leer:** interpretar resultados, hallar causa raíz o hacer profiling. Detalle en los documentos de esta skill (abajo).

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

### [`01_RCA_y_Troubleshooting.md`](01_RCA_y_Troubleshooting.md) — RCA, troubleshooting, profiling
- Para qué: pasar de síntoma a causa raíz con evidencia.
- Consultar si: usas el decision tree o el template de RCA formal · buscas la solución concreta por tipo de bottleneck (CPU, memoria, I/O, locks) · eliges herramienta de profiling por lenguaje/plataforma

---

## 🔗 Relación con otras categorías

| Desde aquí puedo ir a... | Para... |
|--------------------------|---------|
| [ptlc-metricas-kpis](../ptlc-metricas-kpis/SKILL.md) | Entender qué significan las métricas que veo |
| [ptlc-monitoreo](../ptlc-monitoreo/SKILL.md) | Verificar que tengo suficiente observabilidad |
| [ptlc-fases-del-ciclo](../ptlc-fases-del-ciclo/SKILL.md) | Fase 7 (Análisis) y Fase 8 (Optimización) |
| [ptlc-tipos-de-pruebas](../ptlc-tipos-de-pruebas/SKILL.md) | Pruebas de isolation/configuration para confirmar RCA |