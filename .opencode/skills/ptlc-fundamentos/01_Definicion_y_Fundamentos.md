# Performance Test Life Cycle - Definición y Fundamentos

## ¿Qué es el Performance Testing?

El **Performance Testing** es una disciplina de ingeniería de software que se enfoca en determinar cómo un sistema se comporta en términos de **responsividad**, **estabilidad**, **escalabilidad** y **uso de recursos** bajo una carga de trabajo determinada. A diferencia del testing funcional que verifica *qué* hace el sistema, el performance testing verifica *cómo de bien* lo hace.

### Definición formal

> El Performance Testing es el proceso de determinar la velocidad, capacidad de respuesta y estabilidad de un sistema informático bajo una carga de trabajo particular. También puede servir para investigar, medir, validar o verificar otros atributos de calidad del sistema, como la escalabilidad, la fiabilidad y el uso de recursos.
> — ISO 25010 (System and Software Quality Models)

---

## ¿Qué es el Performance Test Life Cycle (PTLC)?

El **PTLC** es un marco metodológico estructurado que define las fases, actividades, entregables y criterios necesarios para ejecutar pruebas de rendimiento de manera sistemática, repetible y efectiva. Es al performance testing lo que el SDLC es al desarrollo de software.

### Analogía con SDLC

| SDLC | PTLC |
|------|------|
| Requirements Analysis | Performance Requirements Gathering |
| System Design | Test Design & Workload Modeling |
| Implementation | Script Development |
| Testing | Test Execution |
| Deployment | Results Analysis |
| Maintenance | Optimization & Continuous Testing |

---

## Origen e Historia

### Evolución del Performance Testing

| Era | Período | Características |
|-----|---------|----------------|
| **Pre-web** | 1980-1995 | Testing manual, mainframes, focus en batch processing |
| **Primera generación web** | 1995-2005 | Primeras herramientas (LoadRunner 1993), testing de websites |
| **SOA & Enterprise** | 2005-2012 | Testing de servicios web, arquitecturas distribuidas |
| **Cloud & DevOps** | 2012-2018 | Shift-left, CI/CD integration, herramientas open-source |
| **Cloud-native & AI** | 2018-presente | Microservicios, containers, chaos engineering, observabilidad |

### Influencias metodológicas
- **ISTQB** (International Software Testing Qualifications Board): Proporciona el marco teórico de testing.
- **IEEE 829**: Estándar para documentación de testing.
- **ISO 25010**: Modelo de calidad de software (reemplaza ISO 9126).
- **OWASP Performance Testing Guide**: Guías específicas de seguridad y rendimiento.

---

## Principios Fundamentales del PTLC

### 1. Orientación a objetivos
Cada prueba debe tener un objetivo claro y medible. Sin un objetivo definido, los resultados no tienen contexto ni valor.

```
MAL:  "Probar el rendimiento del sistema"
BIEN: "Verificar que el sistema soporta 1000 usuarios concurrentes
       con tiempo de respuesta P95 < 3 segundos y error rate < 0.5%"
```

### 2. Realismo
Las pruebas deben simular condiciones lo más cercanas posible a la realidad de producción. Esto incluye:
- Datos realistas (volumen y variedad)
- Comportamiento de usuario realista (think times, navigation patterns)
- Infraestructura similar a producción
- Integración con servicios externos (o mocks apropiados)

### 3. Reproducibilidad
Los resultados deben ser consistentes y reproducibles. Factores que afectan la reproducibilidad:
- Entorno controlado y estable
- Scripts determinísticos (con variación controlada)
- Datos de prueba reseteables
- Documentación completa de condiciones

### 4. Iteratividad
El PTLC no es lineal; es iterativo. Se ejecutan múltiples ciclos de:
```
Ejecutar → Analizar → Optimizar → Re-ejecutar → Comparar
```

### 5. Colaboración
Performance testing no es una actividad aislada. Requiere colaboración entre:
- Testers de rendimiento
- Desarrolladores
- DBAs
- Arquitectos
- DevOps/SRE
- Product Owners

### 6. Proactividad
No esperar a que los problemas lleguen a producción. El testing proactivo identifica riesgos antes de que se materialicen.

---

## Requisitos No Funcionales (NFRs)

### Definición
Los NFRs son restricciones y criterios que definen cómo debe comportarse el sistema (no qué debe hacer). Son la base de todo el PTLC.

### Categorías de NFRs relevantes

| Categoría | Descripción | Ejemplos de métricas |
|-----------|-------------|---------------------|
| **Rendimiento** | Velocidad de respuesta | Response time < 2s |
| **Capacidad** | Volumen que puede manejar | 10,000 usuarios concurrentes |
| **Escalabilidad** | Capacidad de crecer | Linear scaling up to 4x |
| **Disponibilidad** | Uptime del sistema | 99.95% availability |
| **Fiabilidad** | Consistencia bajo estrés | < 0.1% error rate under load |
| **Eficiencia** | Uso de recursos | < 70% CPU at peak load |

### SMART NFRs
Los NFRs deben ser **SMART**:
- **S**pecific: "P95 response time for login < 2 seconds"
- **M**easurable: Valor numérico verificable
- **A**chievable: Realista para la arquitectura
- **R**elevant: Alineado con objetivos de negocio
- **T**ime-bound: En qué condiciones (carga, duración)

### Ejemplo de especificación de NFRs

```yaml
performance_requirements:
  transaction_login:
    response_time:
      p50: "< 1 second"
      p95: "< 2 seconds"
      p99: "< 4 seconds"
    throughput: ">= 100 TPS"
    error_rate: "< 0.1%"
    conditions:
      concurrent_users: 500
      test_duration: "2 hours"
      
  transaction_search:
    response_time:
      p50: "< 500ms"
      p95: "< 1.5 seconds"
      p99: "< 3 seconds"
    throughput: ">= 200 TPS"
    error_rate: "< 0.5%"
    conditions:
      concurrent_users: 500
      data_volume: "10M records"
      
  infrastructure:
    cpu_utilization: "< 75% sustained"
    memory_utilization: "< 80%"
    disk_io_latency: "< 10ms average"
    network_bandwidth: "< 60% capacity"
```

---

## El PTLC en el contexto del SDLC

### Integración con metodologías ágiles

```
Sprint Planning → Sprint Execution → Sprint Review
     │                  │                  │
     ▼                  ▼                  ▼
Identify perf      Execute perf      Review perf
scenarios          tests in CI/CD    results & trends
```

### Cuándo iniciar performance testing

| Fase SDLC | Actividades de Performance |
|-----------|---------------------------|
| Requirements | Definir NFRs, identificar escenarios críticos |
| Design | Validar arquitectura, capacity planning |
| Development | Unit performance tests, benchmarks |
| Integration | API load tests, component tests |
| System Testing | Full load/stress/endurance tests |
| Pre-Production | Full-scale tests en staging |
| Production | Monitoring, synthetic testing |

### Shift-Left Performance Testing

El concepto de "shift-left" aplica especialmente a performance:

```
Costo de corregir un problema de rendimiento:
                                          
  $$$$$                              ■
  $$$$                           ■
  $$$                        ■
  $$                     ■
  $                  ■
              ■ ■ ■
  ─────────────────────────────────────────
  Design  Dev  Integration  System  Production
  
  Mientras más tarde se detecta, más caro es corregir.
```

---

## Beneficios del PTLC estructurado

### Para el negocio
- Reducción de riesgo de caídas en producción
- Mejor experiencia de usuario = mayor retención
- Capacidad de planificar crecimiento con datos objetivos
- Reducción de costos de infraestructura (right-sizing)

### Para el equipo técnico
- Proceso repetible y predecible
- Detección temprana de regresiones
- Datos objetivos para decisiones de arquitectura
- Base de conocimiento para futuros proyectos

### Para operaciones
- Confianza en la capacidad del sistema
- Datos para capacity planning
- Identificación proactiva de límites
- Mejor preparación para eventos de tráfico

---

## Relación con otras disciplinas

```
┌─────────────────────────────────────────────────────────────┐
│                    Quality Engineering                        │
├───────────────┬─────────────────┬───────────────────────────┤
│  Functional   │  Performance    │  Security Testing         │
│  Testing      │  Testing (PTLC) │                           │
├───────────────┼─────────────────┼───────────────────────────┤
│  Unit Testing │  Load Testing   │  Penetration Testing      │
│  Integration  │  Stress Testing │  Vulnerability Assessment │
│  E2E Testing  │  Soak Testing   │  DDoS Resilience          │
├───────────────┴─────────────────┴───────────────────────────┤
│                    DevOps / SRE                               │
├─────────────────────────────────────────────────────────────┤
│  CI/CD │ Monitoring │ Incident Response │ Capacity Planning  │
└─────────────────────────────────────────────────────────────┘
```

### Chaos Engineering + Performance Testing
La combinación de chaos engineering y performance testing permite:
- Verificar rendimiento bajo condiciones de fallo
- Validar mecanismos de failover
- Probar circuit breakers bajo carga
- Evaluar graceful degradation

### SRE (Site Reliability Engineering)
El PTLC alimenta directamente las prácticas SRE:
- **SLIs** (Service Level Indicators): Métricas de performance testing
- **SLOs** (Service Level Objectives): Basados en NFRs validados
- **SLAs** (Service Level Agreements): Garantizados por testing
- **Error Budgets**: Informados por resultados de pruebas

---

## Glosario de Términos Clave

| Término | Definición |
|---------|-----------|
| **NFR** | Non-Functional Requirement - Requisito que define cómo debe comportarse el sistema |
| **SLA** | Service Level Agreement - Acuerdo contractual de niveles de servicio |
| **SLO** | Service Level Objective - Objetivo interno de nivel de servicio |
| **SLI** | Service Level Indicator - Métrica que mide un SLO |
| **TPS** | Transactions Per Second - Transacciones por segundo |
| **RPS** | Requests Per Second - Requests por segundo |
| **P95/P99** | Percentil 95/99 - Valor bajo el cual cae el 95%/99% de las mediciones |
| **VUser** | Virtual User - Usuario simulado por la herramienta de testing |
| **Think Time** | Pausa entre acciones de un usuario simulado |
| **Ramp-up** | Incremento gradual de usuarios virtuales |
| **Steady State** | Período de carga constante en un test |
| **Bottleneck** | Cuello de botella - Componente que limita el rendimiento |
| **Baseline** | Línea base de rendimiento para comparación |
| **Throughput** | Cantidad de trabajo procesado por unidad de tiempo |
| **Latency** | Tiempo de espera antes de que comience la transferencia |
| **Concurrency** | Número de operaciones simultáneas |
| **Saturation** | Grado de utilización de un recurso |

---

*Documento de referencia - Performance Test Life Cycle*
*Última actualización: Junio 2026*
