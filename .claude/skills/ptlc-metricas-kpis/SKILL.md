---
name: ptlc-metricas-kpis
description: "Define KPI: p95/p99, Apdex, throughput, error rate"
---

# 04 — Métricas y KPIs de Performance Testing

> Índice intermedio. **Cuándo leer:** qué medir, cómo definir criterios de éxito y qué fórmulas aplicar. Detalle en los documentos de esta skill (abajo).

## Taxonomía de Métricas

### Métricas de Experiencia de Usuario (UX)
| Métrica | Qué mide | Fórmula / Referencia |
|---------|-----------|---------------------|
| Response Time | Tiempo total de respuesta | DNS + Connect + TLS + TTFB + Transfer |
| TTFB (Time to First Byte) | Latencia del servidor | Timestamp primer byte - timestamp request |
| Throughput | Transacciones por segundo | Requests exitosos / Duración |
| Error Rate | % de respuestas fallidas | Errors / Total Requests × 100 |
| Apdex | Satisfacción del usuario (0-1) | (Satisfied + Tolerating×0.5) / Total |
| Percentiles (p50, p95, p99) | Distribución de tiempos | Ordenar valores, tomar posición N% |

### Métricas de Infraestructura
| Métrica | Qué mide | Umbral típico de alerta |
|---------|-----------|------------------------|
| CPU Utilization | Uso de procesador | > 80% sostenido |
| Memory Usage | Consumo de RAM | > 85% o crecimiento constante (leak) |
| Disk I/O | Operaciones de disco | Latencia > 10ms, queue depth > 2 |
| Network I/O | Ancho de banda y paquetes | > 70% saturación, packet loss > 0.1% |
| Connection Pool | Conexiones activas vs máximo | > 80% del pool utilizado |
| Thread Count | Hilos activos | Crecimiento sin liberación = leak |
| GC (Garbage Collection) | Pausas de GC | Full GC > 1s, frequency > 1/min |

### Fórmulas Clave
| Fórmula | Uso |
|---------|-----|
| **Little's Law:** `L = λ × W` | Calcular VUs necesarios: VU = TPS × ResponseTime |
| **Apdex:** `(S + T×0.5) / N` | Medir satisfacción (T = Tolerating threshold) |
| **Concurrent Users:** `VU = TPS × AvgResponseTime` | Dimensionar carga |
| **CV (Coef. Variación):** `σ / μ × 100` | Validar estabilidad de baseline (< 10%) |
| **Throughput saturation:** `TPS_max = f(resources)` | Identificar cuello de botella |

> **Nota de uso:** usar el cheat sheet para fórmulas; el documento para el detalle.

---

## 📂 Contenido de la Subcarpeta

### [`00_Cheat_Sheet_Metricas.md`](00_Cheat_Sheet_Metricas.md) — fórmulas y umbrales operativos (≤600 tokens)
- Para qué: obtener de un golpe percentiles, Apdex, throughput, error rate y la plantilla pass/fail.
- Consultar si: solo necesitas la fórmula o el umbral; el detalle vive en el documento.

### [`01_Metricas_Exhaustivas.md`](01_Metricas_Exhaustivas.md) — análisis profundo y calculadora
- Para qué: aplicar las fórmulas con números reales.
- Consultar si: entiendes por qué usar percentiles en vez de promedios · construyes un Apdex score o defines umbrales de alerta de infra

---

## 🔗 Relación con otras categorías

| Desde aquí puedo ir a... | Para... |
|--------------------------|---------|
| [ptlc-tipos-de-pruebas](../ptlc-tipos-de-pruebas/SKILL.md) | Saber qué métricas priorizar por tipo de prueba |
| [ptlc-workload-modeling](../ptlc-workload-modeling/SKILL.md) | Aplicar Little's Law al modelo de carga |
| [ptlc-monitoreo](../ptlc-monitoreo/SKILL.md) | Implementar la recolección de estas métricas |
| [ptlc-analisis-bottlenecks](../ptlc-analisis-bottlenecks/SKILL.md) | Interpretar métricas y hacer RCA |