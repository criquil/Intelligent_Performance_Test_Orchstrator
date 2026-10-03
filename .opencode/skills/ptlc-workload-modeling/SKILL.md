---
name: ptlc-workload-modeling
description: "Modela carga: Little's Law, VUs, patrones de trafico"
---

# 06 — Workload Modeling y Diseño de Escenarios

> Índice intermedio. **Cuándo leer:** calcular VUs, diseñar patrones de carga o distribuciones. Detalle en los documentos de esta skill (abajo).

## ¿Qué es el Workload Modeling?

El modelado de carga transforma datos reales de producción (o estimaciones de negocio) en un modelo ejecutable que simula patrones de uso realistas. Es el **puente entre los requisitos** (Fase 1) y **los scripts** (Fase 5).

### Fórmula Central: Little's Law

```
L = λ × W

Donde:
  L = Número de usuarios concurrentes (VUs)
  λ = Tasa de llegada (requests/segundo o transacciones/segundo)
  W = Tiempo promedio de respuesta (en segundos)

Ejemplo:
  Si necesito 100 TPS y el response time es 2s → VU = 100 × 2 = 200 VUs
```

### Elementos del Modelo de Carga

| Elemento | Descripción | Ejemplo |
|----------|-------------|---------|
| Transaction Mix | % de cada operación | 60% browse, 25% search, 10% cart, 5% checkout |
| Think Time | Pausa entre acciones del usuario | 3-8 segundos (distribución normal) |
| Pacing | Tiempo total por iteración | 30s fijo (garantiza ritmo constante) |
| Ramp-up | Tiempo para alcanzar carga completa | 5 min para 500 VUs = 100 VU/min |
| Steady State | Duración a carga máxima | Mínimo 30 min (idealmente 1h+) |
| Ramp-down | Tiempo de descenso | 2-5 minutos |

> **Nota de uso:** usar el cheat sheet para fórmulas; el documento para el detalle.

---

## 📂 Contenido de la Subcarpeta

### [`00_Cheat_Sheet_Workload.md`](00_Cheat_Sheet_Workload.md) — fórmulas y patrones operativos (≤600 tokens)
- Para qué: obtener de un golpe Little's Law, VUs para throughput objetivo, ramp-up y patrones de carga.
- Consultar si: solo necesitas la fórmula o el patrón; el detalle vive en el documento.

### [`01_Workload_Modeling_Exhaustivo.md`](01_Workload_Modeling_Exhaustivo.md) — fórmulas, patrones y template YAML
- Para qué: construir y validar un modelo de carga realista.
- Consultar si: convierte datos de producción/APM en VUs concurrentes · eliges distribución de think times o patrón (diurnal, seasonal) · usas el template YAML del workload model

---

## 🔗 Relación con otras categorías

| Desde aquí puedo ir a... | Para... |
|--------------------------|---------|
| [ptlc-fases-del-ciclo](../ptlc-fases-del-ciclo/SKILL.md) | Fase 3 (Diseño) donde se crea el workload model |
| [ptlc-metricas-kpis](../ptlc-metricas-kpis/SKILL.md) | Little's Law y fórmulas de throughput |
| [ptlc-herramientas](../ptlc-herramientas/SKILL.md) | Implementar el modelo en k6/JMeter/Gatling/Locust |
| [ptlc-tipos-de-pruebas](../ptlc-tipos-de-pruebas/SKILL.md) | Baseline para validar el modelo |