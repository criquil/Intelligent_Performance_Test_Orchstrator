# 06 — Workload Modeling y Diseño de Escenarios

> **Rol de este archivo:** Índice intermedio. Resume los conceptos de modelado de carga y dirige a la documentación con fórmulas y templates.  
> **Cuándo leer este archivo:** Cuando necesitas calcular usuarios virtuales, diseñar patrones de carga, o entender distribuciones estadísticas.  
> **Carpeta detallada:** [`06_Workload_Modeling/`](06_Workload_Modeling/)

---

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

---

## 📂 Contenido de la Subcarpeta

### [`01_Workload_Modeling_Exhaustivo.md`](06_Workload_Modeling/01_Workload_Modeling_Exhaustivo.md)
**Contenido completo (~15 KB):**

| Sección | Qué encontrarás |
|---------|-----------------|
| Fundamentos Teóricos | Little's Law, Queuing Theory, distribuciones (Poisson, Normal, Uniform) |
| Recolección de Datos | APM analysis, access logs, Google Analytics, business forecasts |
| Modelado Matemático | Fórmulas paso a paso con ejemplos numéricos |
| Patrones de Tráfico | Diurnal, weekly, seasonal, event-driven + cómo modelar cada uno |
| Template Completo de Workload Model | YAML template listo para copiar y adaptar |
| Validación y Calibración | Cómo verificar que el modelo refleja la realidad |

**Ir aquí si necesitas:**
- Calcular VUs concurrentes a partir de datos de producción
- Template YAML para documentar tu modelo de carga
- Entender qué distribución usar para think times
- Convertir datos de Google Analytics en un workload model
- Validar que tu test simula carga realista

---

## 🔗 Relación con otras categorías

| Desde aquí puedo ir a... | Para... |
|--------------------------|---------|
| [03_Fases](03_Fases_del_PTLC_Detalle.md) | Fase 3 (Diseño) donde se crea el workload model |
| [04_Metricas](04_Metricas_y_KPIs.md) | Little's Law y fórmulas de throughput |
| [05_Herramientas](05_Herramientas_de_Performance_Testing.md) | Implementar el modelo en k6/JMeter/Gatling/Locust |
| [02_Tipos](02_Tipos_de_Pruebas_de_Rendimiento.md) | Baseline para validar el modelo |
