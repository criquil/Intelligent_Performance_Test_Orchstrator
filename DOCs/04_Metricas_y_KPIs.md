# 04 — Métricas y KPIs de Performance Testing

> **Rol de este archivo:** Índice intermedio. Resume qué métricas existen, cómo clasificarlas, y dirige al documento exhaustivo con fórmulas y cálculos.  
> **Cuándo leer este archivo:** Cuando necesitas saber qué medir, cómo definir criterios de éxito, o qué fórmulas aplicar.  
> **Carpeta detallada:** [`04_Metricas_y_KPIs/`](04_Metricas_y_KPIs/)

---

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

---

## 📂 Contenido de la Subcarpeta

### [`01_Metricas_Exhaustivas.md`](04_Metricas_y_KPIs/01_Metricas_Exhaustivas.md)
**Contenido completo (~18 KB):**

| Sección | Qué encontrarás |
|---------|-----------------|
| Taxonomía de Métricas | Clasificación completa por categoría |
| Response Time - Análisis Profundo | Desglose en componentes (DNS, TCP, TLS, TTFB, content transfer), cómo interpretar cada uno |
| Throughput - Análisis Profundo | Curvas de throughput, punto de saturación, relación con VUs |
| Error Rate - Análisis Profundo | Tipos de error, clasificación, umbrales por tipo de sistema |
| Percentiles y Distribución | p50/p90/p95/p99, por qué promedios mienten, histogramas |
| Métricas de Infraestructura Detalladas | CPU, memory, disk, network, JVM, containers, DB connections |
| Calculadora de Métricas | Fórmulas aplicadas con ejemplos numéricos reales |

**Ir aquí si necesitas:**
- Fórmulas con ejemplos numéricos paso a paso
- Entender por qué usar percentiles en vez de promedios
- Definir umbrales de alerta para cada métrica de infra
- Calcular VUs usando Little's Law con datos reales
- Construir un Apdex score para tu aplicación

---

## 🔗 Relación con otras categorías

| Desde aquí puedo ir a... | Para... |
|--------------------------|---------|
| [02_Tipos_de_Pruebas](02_Tipos_de_Pruebas_de_Rendimiento.md) | Saber qué métricas priorizar por tipo de prueba |
| [06_Workload](06_Workload_Modeling_y_Diseno_de_Escenarios.md) | Aplicar Little's Law al modelo de carga |
| [07_Monitoreo](07_Entorno_y_Monitoreo.md) | Implementar la recolección de estas métricas |
| [09_Analisis](09_Analisis_de_Resultados_y_Bottlenecks.md) | Interpretar métricas y hacer RCA |
