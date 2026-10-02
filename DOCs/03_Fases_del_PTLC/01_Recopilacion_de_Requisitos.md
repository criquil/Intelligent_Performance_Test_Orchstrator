# Fase 1: Recopilación de Requisitos de Performance

## Propósito de esta fase

La recopilación de requisitos es la **fase más crítica** del PTLC. Un error aquí se propaga a todas las fases siguientes. Si los requisitos son incorrectos, vagos o incompletos, todo el esfuerzo de performance testing será inútil o peor, generará falsa confianza.

---

## Fuentes de Requisitos

### 1. Requisitos de Negocio
| Fuente | Información |
|--------|-------------|
| Product Owner | Expectativas de usuario, growth plans |
| Marketing | Campañas planificadas, proyecciones de tráfico |
| Ventas | SLAs contractuales con clientes |
| Legal | Requisitos regulatorios de uptime/respuesta |
| Finanzas | Impacto económico de downtime |

### 2. Datos de Producción
| Fuente | Información |
|--------|-------------|
| Analytics (Google Analytics, etc.) | Usuarios, sessions, page views |
| APM (New Relic, Dynatrace) | Response times actuales, throughput |
| Server logs | Request patterns, peak hours |
| Database metrics | Query volumes, data growth |
| CDN stats | Traffic patterns, geographic distribution |

### 3. Requisitos Técnicos
| Fuente | Información |
|--------|-------------|
| Arquitecto | Limitaciones de diseño, capacity constraints |
| DevOps/SRE | Infrastructure limits, scaling policies |
| DBA | Database constraints, replication lag limits |
| Security | Rate limiting, authentication load |
| Network team | Bandwidth limits, latency requirements |

---

## Proceso de Recopilación

### Paso 1: Identificar Stakeholders

```
Mapa de stakeholders para performance:

                    ALTO INTERÉS
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    Arquitecto      Product Owner    VP Engineering
         │               │               │
    ALTA ─┼───────────────┼───────────────┼── BAJA
 INFLUENCIA│               │               │ INFLUENCIA
         │               │               │
    DevOps/SRE       QA Lead         End Users
         │               │               │
         └───────────────┼───────────────┘
                         │
                    BAJO INTERÉS
```

### Paso 2: Workshops de Requisitos

#### Agenda típica del workshop
1. **Contexto de negocio** (15 min)
   - ¿Qué hace la aplicación?
   - ¿Quiénes son los usuarios?
   - ¿Cuáles son los flujos críticos?

2. **Datos actuales** (20 min)
   - Tráfico actual (daily/weekly/monthly)
   - Picos conocidos
   - Problemas de rendimiento históricos

3. **Expectativas futuras** (20 min)
   - Crecimiento esperado
   - Eventos planificados
   - Nuevas funcionalidades

4. **Definición de SLAs** (30 min)
   - Response time por transacción
   - Throughput mínimo
   - Error rate máximo
   - Disponibilidad requerida

5. **Priorización** (15 min)
   - ¿Qué escenarios son más críticos?
   - ¿Qué riesgos son más altos?

### Paso 3: Documentar Requisitos

#### Template de requisito de performance

```yaml
requirement_id: "PERF-001"
title: "Login Transaction Performance"
priority: "High"
category: "Response Time"

description: |
  El proceso de login debe completarse dentro de los tiempos 
  especificados para garantizar una experiencia de usuario 
  aceptable durante horario pico.

conditions:
  concurrent_users: 500
  data_volume: "5M registered users"
  test_duration: "2 hours minimum"
  environment: "Production-equivalent"

acceptance_criteria:
  response_time:
    p50: "<= 800ms"
    p90: "<= 1.5s"
    p95: "<= 2.0s"
    p99: "<= 4.0s"
  throughput: ">= 100 successful logins per second"
  error_rate: "<= 0.1%"
  
rationale: |
  Based on industry standards (Google: 53% of mobile users 
  abandon sites taking > 3s to load) and current production 
  P95 of 1.2s with 300 concurrent users.

dependencies:
  - "Authentication service available"
  - "Database with 5M+ user records"
  - "Redis session cache configured"
  
measurement_method: |
  Measured from HTTP request sent to complete response received.
  Includes server processing but excludes client rendering.
  
source: "Workshop with PO and Architecture team, 2026-06-01"
approved_by: "CTO, Product Owner"
```

---

## Análisis de Carga Esperada

### Cálculo de usuarios concurrentes

#### Método 1: Desde analytics
```
Datos de Google Analytics (mes anterior):
- Monthly Active Users (MAU): 500,000
- Daily Active Users (DAU): 50,000
- Peak hourly users: 8,000
- Average session duration: 5 minutes
- Peak hour: 10:00 - 11:00 AM

Concurrent users (peak) = Peak hourly × (avg_session / 60)
                        = 8,000 × (5/60)
                        = 667 concurrent users

Con factor de seguridad (1.5x para crecimiento):
Target concurrent users = 667 × 1.5 = 1,000 users
```

#### Método 2: Desde logs de servidor
```
Server logs analysis (peak hour):
- Total requests/hour: 360,000
- Requests/second (avg): 100
- Requests/second (peak): 250
- Unique sessions in peak hour: 5,000
- Avg requests per session: 72

Concurrent sessions = (5,000 × 5min) / 60min = 417 sessions
Concurrent users (active) ≈ 417 × 0.3 = 125 users doing actions

NOTA: "Concurrent" puede significar cosas diferentes:
- Concurrent sessions: todos los que tienen sesión abierta
- Concurrent users: los que están activamente interactuando
- Concurrent requests: requests simultáneas en un instante
```

#### Método 3: Desde requisitos de negocio
```
Business requirements:
- "The system must support 10,000 daily users"
- Peak-to-average ratio (from industry): 3:1
- Peak users/hour: 10,000 / 8 active hours × 3 = 3,750/hour
- Average session: 8 minutes
- Concurrent: 3,750 × (8/60) = 500 users
```

### Cálculo de throughput esperado

```
Throughput = Concurrent_Users × Requests_Per_User_Per_Second

Si:
- Concurrent users: 500
- Average think time: 5 seconds
- Requests per page: 3 (main + 2 API calls)

Requests per user per second = 3 / 5 = 0.6 RPS per user
Total throughput = 500 × 0.6 = 300 RPS

Para transacciones de negocio:
- Each user completes 1 business transaction every 2 minutes
- TPS = 500 / 120 = 4.17 business TPS
```

---

## Identificación de Escenarios Críticos

### Criterios de priorización

| Criterio | Peso | Descripción |
|----------|------|-------------|
| Impacto en revenue | 30% | ¿Afecta directamente ingresos? |
| Frecuencia de uso | 25% | ¿Qué tan usado es el flujo? |
| Complejidad técnica | 20% | ¿Involucra múltiples componentes? |
| Riesgo de fallo | 15% | ¿Historial de problemas? |
| Visibilidad | 10% | ¿Impacto reputacional si falla? |

### Ejemplo de priorización

| Escenario | Revenue | Frecuencia | Complejidad | Riesgo | Visibilidad | Score |
|-----------|---------|-----------|-------------|--------|-------------|-------|
| Checkout | 10 | 6 | 9 | 8 | 10 | 8.35 |
| Search | 7 | 10 | 7 | 5 | 8 | 7.55 |
| Login | 5 | 10 | 5 | 6 | 9 | 6.85 |
| Browse | 4 | 10 | 3 | 3 | 5 | 5.15 |
| Profile | 2 | 4 | 3 | 2 | 3 | 2.85 |

### Escenarios que SIEMPRE deben incluirse
1. **Login / Authentication** - Puerta de entrada al sistema
2. **Core business transaction** - Lo que genera valor/revenue
3. **Search / Query** - Generalmente el más resource-intensive
4. **High-concurrency endpoints** - APIs llamadas frecuentemente
5. **Background processes** - Batch jobs que compiten por recursos

---

## Documentación Final de Requisitos

### Performance Requirements Specification (PRS)

```markdown
# Performance Requirements Specification
# Project: [Nombre del Proyecto]
# Version: 1.0
# Date: YYYY-MM-DD

## 1. Executive Summary
Brief description of performance testing scope and objectives.

## 2. System Under Test
- Application name, version
- Architecture overview (diagram)
- Technology stack
- Key integrations

## 3. Performance Requirements

### 3.1 Response Time Requirements
[Table of transactions with P50, P90, P95, P99 targets]

### 3.2 Throughput Requirements
[Minimum TPS/RPS for each scenario]

### 3.3 Resource Utilization Limits
[CPU, Memory, Disk, Network thresholds]

### 3.4 Scalability Requirements
[Growth expectations, scaling targets]

### 3.5 Availability Requirements
[Uptime %, recovery time objectives]

## 4. Load Profile
### 4.1 Expected Users
[Current and projected user counts]

### 4.2 Peak Patterns
[When and how peaks occur]

### 4.3 Growth Projections
[6-month, 12-month, 24-month]

## 5. Test Scenarios (Prioritized)
[Ordered list with rationale]

## 6. Constraints and Assumptions
[Environment, data, timeline limitations]

## 7. Risks
[What could invalidate our testing]

## 8. Approval
[Sign-off from stakeholders]
```

---

## Errores Comunes en esta Fase

| Error | Consecuencia | Prevención |
|-------|-------------|------------|
| No involucrar a negocio | NFRs sin contexto de valor | Workshop con PO/stakeholders |
| Requisitos vagos ("debe ser rápido") | Imposible validar pass/fail | Exigir números específicos |
| Ignorar growth projections | Obsoleto al llegar a prod | Incluir factor de crecimiento |
| Copy-paste de otro proyecto | No aplica a esta realidad | Analizar datos específicos |
| Solo considerar happy path | No cubre error scenarios | Incluir edge cases |
| No documentar assumptions | Discusiones futuras | Escribir todo explícitamente |

---

*Documento de referencia - Performance Test Life Cycle*
*Última actualización: Junio 2026*
