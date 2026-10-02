# 02 — Tipos de Pruebas de Rendimiento

> **Rol de este archivo:** Índice intermedio. Clasifica todos los tipos de pruebas de performance y dirige al archivo específico de cada grupo.  
> **Cuándo leer este archivo:** Cuando necesitas saber qué tipo de prueba ejecutar según tu objetivo o situación.  
> **Carpeta detallada:** [`02_Tipos_de_Pruebas/`](02_Tipos_de_Pruebas/)

---

## Mapa Completo: 22+ Tipos de Pruebas

```
VALIDACIÓN DE CAPACIDAD          ESTABILIDAD A LARGO PLAZO       LÍMITES Y EXTREMOS
├── Load Testing                 ├── Endurance/Soak Testing      ├── Stress Testing
├── Baseline Testing             ├── Reliability Testing         ├── Spike Testing
├── Smoke Testing                └── Regression Testing          ├── Peak Testing
└── Capacity Testing                                             ├── Breakpoint Testing
                                                                 └── Saturation Testing

RESILIENCIA Y RECUPERACIÓN       CONFIGURACIÓN Y RED             ESPECÍFICOS POR CAPA
├── Resiliency/Chaos Testing     ├── Configuration Testing       ├── API Performance Testing
├── Failover Testing             ├── Network Testing             ├── Browser/Frontend Testing
├── Recovery Testing             └── Scalability Testing         ├── Volume Testing (DB)
└── Concurrency Testing                                          └── Isolation Testing
```

---

## ¿Qué tipo de prueba necesito?

| Situación | Tipo recomendado | Archivo |
|-----------|------------------|---------|
| Validar que el sistema aguanta la carga diaria | Load Testing | `01_Load_Testing.md` |
| Establecer una línea base medible y repetible | Baseline Testing | `04_Baseline_Testing.md` |
| Verificar que un deploy no rompió nada rápidamente | Smoke Testing | `05_Smoke_Peak_Capacity_Breakpoint.md` |
| Saber cuántos usuarios soporta antes de colapsar | Stress / Breakpoint | `02_Stress_Testing.md` / `05_...` |
| Evaluar estabilidad durante 8-72 horas | Endurance / Soak | `03_Endurance_Spike_Volume_Scalability.md` |
| Simular un pico repentino (flash sale, evento TV) | Spike Testing | `03_Endurance_Spike_Volume_Scalability.md` |
| Verificar escalado horizontal/vertical funciona | Scalability Testing | `03_Endurance_Spike_Volume_Scalability.md` |
| Validar comportamiento con alta carga en DB | Volume Testing | `03_Endurance_Spike_Volume_Scalability.md` |
| Probar que el sistema se recupera de fallos | Failover / Recovery | `06_Configuration_Failover_...md` |
| Inyectar fallos deliberadamente (Chaos Engineering) | Resiliency Testing | `07_Resiliency_Testing.md` |
| Verificar APIs individualmente bajo carga | API Performance | `06_Configuration_Failover_...md` |
| Medir Core Web Vitals y tiempos del browser | Browser/Frontend | `06_Configuration_Failover_...md` |
| Probar diferentes configuraciones de infra | Configuration Testing | `06_Configuration_Failover_...md` |
| Asegurar que un fix no degradó performance | Regression Testing | `06_Configuration_Failover_...md` |

---

## 📂 Contenido de la Subcarpeta

### [`01_Load_Testing.md`](02_Tipos_de_Pruebas/01_Load_Testing.md)
**Tipo cubierto:** Load Testing  
**Secciones:** Definición · Objetivos · Diseño completo (VUs, ramp-up, steady-state, ramp-down) · Proceso de ejecución · Análisis de resultados · Variantes (step-load, constant, wave) · Ejemplo de reporte · Errores comunes

---

### [`02_Stress_Testing.md`](02_Tipos_de_Pruebas/02_Stress_Testing.md)
**Tipo cubierto:** Stress Testing  
**Secciones:** Definición · Objetivos · Diferencia con Load Testing · Tipos de stress (gradual, sudden, resource-bound) · Diseño · Métricas específicas · Análisis · Patrones de recuperación · Script k6 ejemplo · Seguridad

---

### [`03_Endurance_Spike_Volume_Scalability.md`](02_Tipos_de_Pruebas/03_Endurance_Spike_Volume_Scalability.md)
**Tipos cubiertos:** Endurance/Soak · Spike · Volume · Scalability  
**Secciones:** Cada tipo con definición, cuándo usar, diseño, métricas, ejemplo y antipatrones · Amdahl's Law para scalability · Resumen comparativo

---

### [`04_Baseline_Testing.md`](02_Tipos_de_Pruebas/04_Baseline_Testing.md)
**Tipo cubierto:** Baseline Testing  
**Secciones:** Definición · Por qué es crítico · Cuándo ejecutar · Cómo ejecutar · **La importancia de ITERAR** (mínimo 3 ejecuciones, CV < 10%) · Template del documento baseline · Uso de la baseline en el PTLC

**⚡ Destacado:** Este documento enfatiza que una sola ejecución NO es suficiente. Se necesitan múltiples iteraciones hasta lograr estabilidad estadística (Coeficiente de Variación < 10%).

---

### [`05_Smoke_Peak_Capacity_Breakpoint.md`](02_Tipos_de_Pruebas/05_Smoke_Peak_Capacity_Breakpoint.md)
**Tipos cubiertos:** Smoke · Peak · Capacity · Breakpoint · Concurrency · Reliability  
**Secciones:** Cada tipo con definición, objetivo, cuándo usar, diseño, métricas clave, script ejemplo, criterios pass/fail

---

### [`06_Configuration_Failover_Recovery_Regression_y_Otros.md`](02_Tipos_de_Pruebas/06_Configuration_Failover_Recovery_Regression_y_Otros.md)
**Tipos cubiertos:** Configuration · Failover · Recovery · Regression · Network · API · Browser/Frontend · Isolation · Saturation  
**Secciones:** Cada tipo documentado + Mapa completo de los 22 tipos con clasificación cruzada

---

### [`07_Resiliency_Testing.md`](02_Tipos_de_Pruebas/07_Resiliency_Testing.md)
**Tipo cubierto:** Resiliency / Chaos Engineering (~62 KB de contenido exhaustivo)  
**Secciones:** Definición y fundamentos · Diferencia con otros tipos · Principios clave · Steady-State Hypothesis · Chaos Engineering como disciplina · Patrones de resiliencia (Circuit Breaker, Bulkhead, Retry, Graceful Degradation) · Tipos de fault injection · Herramientas (LitmusChaos, Chaos Mesh, AWS FIS, Toxiproxy, Gremlin) · Diseño de experimentos · Game Days · Métricas de resiliencia · CI/CD integration · Ejemplos con código · Cloud-Native patterns · Antipatrones · Checklist

---

## 🔗 Relación con otras categorías

| Desde aquí puedo ir a... | Para... |
|--------------------------|---------|
| [04_Metricas](04_Metricas_y_KPIs.md) | Definir qué medir en cada tipo de prueba |
| [05_Herramientas](05_Herramientas_de_Performance_Testing.md) | Implementar la prueba con una tool específica |
| [06_Workload_Modeling](06_Workload_Modeling_y_Diseno_de_Escenarios.md) | Calcular la carga para load/stress/spike |
| [03_Fases](03_Fases_del_PTLC_Detalle.md) | Entender en qué fase del ciclo se ejecuta cada tipo |
