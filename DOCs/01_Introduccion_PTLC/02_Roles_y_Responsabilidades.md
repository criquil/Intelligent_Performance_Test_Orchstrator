# Roles y Responsabilidades en el PTLC

## Visión General

El éxito del Performance Testing depende no solo de las herramientas y técnicas, sino fundamentalmente de las personas y sus roles. Un equipo de performance testing efectivo requiere una combinación de habilidades técnicas, de análisis y de comunicación.

---

## Estructura del Equipo de Performance

### Modelo de equipo típico

```
┌─────────────────────────────────────────────────────┐
│              STAKEHOLDERS / SPONSORS                  │
│     (Product Owner, CTO, Engineering Manager)        │
└──────────────────────────┬──────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────┐
│           PERFORMANCE TEST LEAD / MANAGER            │
│        (Planificación, coordinación, reporting)       │
└──────┬───────────────┬───────────────────┬──────────┘
       │               │                   │
┌──────▼──────┐ ┌──────▼──────┐ ┌─────────▼─────────┐
│  Perf Test  │ │  Perf Test  │ │    Perf Test      │
│  Engineer   │ │  Engineer   │ │    Analyst        │
│  (Scripting)│ │  (Infra)    │ │    (Analysis)     │
└─────────────┘ └─────────────┘ └───────────────────┘
       │               │                   │
┌──────▼───────────────▼───────────────────▼──────────┐
│              SUPPORT TEAMS                            │
│  Developers │ DBAs │ DevOps/SRE │ Network │ Security │
└─────────────────────────────────────────────────────┘
```

---

## Roles Detallados

### 1. Performance Test Lead / Manager

#### Responsabilidades principales
- Definir la estrategia general de performance testing
- Crear y mantener el plan de pruebas
- Coordinar recursos y cronograma
- Comunicar resultados a stakeholders
- Gestionar riesgos del proceso
- Tomar decisiones sobre priorización de escenarios
- Garantizar la calidad del proceso y entregables
- Mentoring del equipo

#### Habilidades requeridas
| Habilidad | Nivel | Importancia |
|-----------|-------|-------------|
| Gestión de proyectos | Avanzado | Crítica |
| Conocimiento técnico de performance | Avanzado | Crítica |
| Comunicación y presentación | Avanzado | Crítica |
| Análisis de requisitos | Avanzado | Alta |
| Gestión de stakeholders | Avanzado | Alta |
| Conocimiento de herramientas | Intermedio | Media |
| Scripting/programación | Intermedio | Media |

#### Entregables clave
- Performance Test Strategy
- Performance Test Plan
- Reportes ejecutivos de resultados
- Risk assessment
- Go/No-Go recommendations

#### Interacciones

```
Stakeholders ←→ Perf Test Lead ←→ Equipo técnico
     ↑                                    ↓
     └── Reportes, recomendaciones ←──── Datos, análisis
```

---

### 2. Performance Test Engineer (Scripting & Execution)

#### Responsabilidades principales
- Diseñar y desarrollar scripts de performance
- Configurar escenarios de prueba
- Ejecutar pruebas según el plan
- Parametrizar y correlacionar scripts
- Depurar problemas de scripts
- Mantener y evolucionar el framework de scripts
- Monitorear ejecuciones en tiempo real
- Documentar procedimientos de ejecución

#### Habilidades requeridas
| Habilidad | Nivel | Importancia |
|-----------|-------|-------------|
| Programación (Java, JavaScript, Python, etc.) | Avanzado | Crítica |
| Herramientas de performance (JMeter, k6, etc.) | Avanzado | Crítica |
| Protocolos (HTTP, WebSocket, gRPC, etc.) | Avanzado | Crítica |
| Debugging y troubleshooting | Avanzado | Alta |
| Scripting y automatización | Avanzado | Alta |
| Conocimiento de APIs REST/SOAP | Avanzado | Alta |
| Control de versiones (Git) | Intermedio | Alta |
| CI/CD pipelines | Intermedio | Media |
| Linux/Windows administration | Intermedio | Media |

#### Entregables clave
- Scripts de performance validados
- Documentación de scripts
- Procedimientos de ejecución
- Logs de ejecución
- Datos raw de resultados

---

### 3. Performance Test Engineer (Infrastructure)

#### Responsabilidades principales
- Configurar y mantener el entorno de pruebas
- Provisionar load generators
- Configurar herramientas de monitoreo
- Gestionar datos de prueba
- Asegurar estabilidad del entorno
- Troubleshooting de problemas de infraestructura
- Automatizar provisión y teardown de entornos

#### Habilidades requeridas
| Habilidad | Nivel | Importancia |
|-----------|-------|-------------|
| Administración de sistemas (Linux/Windows) | Avanzado | Crítica |
| Cloud platforms (AWS, Azure, GCP) | Avanzado | Crítica |
| Networking (TCP/IP, DNS, Load Balancers) | Avanzado | Alta |
| Containers (Docker, Kubernetes) | Avanzado | Alta |
| Infrastructure as Code (Terraform, Ansible) | Avanzado | Alta |
| Monitoring tools (Prometheus, Grafana) | Avanzado | Alta |
| Database administration | Intermedio | Media |
| Scripting (Bash, PowerShell) | Intermedio | Media |

#### Entregables clave
- Entorno de pruebas configurado y validado
- Environment readiness report
- Documentación de configuración
- Scripts de automatización de entorno
- Monitoring dashboards

---

### 4. Performance Analyst

#### Responsabilidades principales
- Analizar resultados de pruebas en profundidad
- Identificar cuellos de botella y causas raíz
- Generar reportes técnicos y ejecutivos
- Proporcionar recomendaciones de optimización
- Realizar análisis de tendencias entre ejecuciones
- Correlacionar datos de múltiples fuentes
- Validar que las optimizaciones mejoran el rendimiento

#### Habilidades requeridas
| Habilidad | Nivel | Importancia |
|-----------|-------|-------------|
| Análisis de datos | Avanzado | Crítica |
| Conocimiento de arquitecturas de software | Avanzado | Crítica |
| APM tools (New Relic, Dynatrace, etc.) | Avanzado | Crítica |
| Estadística aplicada | Avanzado | Alta |
| Comunicación técnica | Avanzado | Alta |
| Database analysis (query plans, indexes) | Avanzado | Alta |
| Profiling tools | Intermedio | Alta |
| Visualización de datos | Intermedio | Media |

#### Entregables clave
- Reportes de análisis detallados
- Identificación de bottlenecks con evidencia
- Root cause analysis documents
- Recomendaciones priorizadas
- Trend analysis reports

---

### 5. Roles de Soporte

#### Desarrolladores

| Responsabilidad | Contexto |
|----------------|----------|
| Proveer información sobre la aplicación | Arquitectura, endpoints, flujos |
| Implementar correcciones de performance | Code optimization, query tuning |
| Instrumentar código para APM | Custom metrics, tracing |
| Revisar resultados con el equipo de perf | Interpretar findings |
| Proporcionar builds estables para testing | Sin bugs funcionales que invaliden tests |

#### DBA (Database Administrator)

| Responsabilidad | Contexto |
|----------------|----------|
| Configurar base de datos del entorno de test | Schema, configuración, datos |
| Analizar slow queries identificadas | EXPLAIN plans, index suggestions |
| Optimizar queries problemáticas | Rewrite queries, add indexes |
| Monitorear métricas de DB durante tests | Locks, connections, cache hits |
| Asesorar sobre data model para performance | Denormalization, partitioning |

#### DevOps / SRE

| Responsabilidad | Contexto |
|----------------|----------|
| Provisionar infraestructura | Servidores, redes, load balancers |
| Configurar monitoreo y alertas | Prometheus, Grafana, alerting rules |
| Mantener pipelines CI/CD | Integrar perf tests en pipeline |
| Capacity planning | Usar resultados para planificar scaling |
| Incident response | Informar con datos de perf testing |

#### Arquitecto de Software

| Responsabilidad | Contexto |
|----------------|----------|
| Definir NFRs junto con negocio | Requisitos realistas y alcanzables |
| Validar diseño arquitectónico | Anti-patterns, scalability concerns |
| Recomendar cambios estructurales | Caching, async, partitioning |
| Evaluar trade-offs | Performance vs cost vs complexity |
| Aprobar soluciones de optimización | Architectural review |

---

## Modelos de Organización

### Modelo 1: Equipo Centralizado (CoE)

```
┌─────────────────────────────────────┐
│   Performance Testing Center of     │
│         Excellence (CoE)            │
├─────────────────────────────────────┤
│  • Equipo dedicado                  │
│  • Sirve a múltiples proyectos      │
│  • Estándares y procesos unificados │
│  • Tools & frameworks compartidos   │
└──────────┬──────────┬───────────────┘
           │          │
     ┌─────▼─────┐ ┌──▼──────────┐
     │ Project A │ │ Project B   │
     └───────────┘ └─────────────┘
```

**Pros:** Expertise concentrado, consistencia, reutilización.
**Contras:** Posible cuello de botella, menos contexto de negocio.

### Modelo 2: Equipo Embebido

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Team Alpha  │  │  Team Beta   │  │  Team Gamma  │
├──────────────┤  ├──────────────┤  ├──────────────┤
│ Devs         │  │ Devs         │  │ Devs         │
│ QA           │  │ QA           │  │ QA           │
│ Perf Eng ★   │  │ Perf Eng ★   │  │ Perf Eng ★   │
│ DevOps       │  │ DevOps       │  │ DevOps       │
└──────────────┘  └──────────────┘  └──────────────┘
```

**Pros:** Mayor contexto, respuesta rápida, ownership.
**Contras:** Posible inconsistencia, duplicación de esfuerzo.

### Modelo 3: Híbrido (Recomendado)

```
┌─────────────────────────────────────┐
│      CoE (Governance & Tools)       │ ← Estándares, frameworks, mentoring
└──────────┬──────────┬───────────────┘
           │          │
     ┌─────▼─────┐ ┌──▼──────────┐
     │ Team Alpha │ │ Team Beta   │ ← Perf engineers embebidos
     │ + Perf Eng │ │ + Perf Eng  │    que siguen guías del CoE
     └───────────┘ └─────────────┘
```

**Pros:** Balance entre expertise y contexto, escalable.
**Contras:** Requiere buena coordinación.

---

## Matriz RACI para el PTLC

| Actividad | Perf Lead | Perf Eng | Analyst | Dev | DBA | DevOps | PO |
|-----------|-----------|----------|---------|-----|-----|--------|-----|
| Definir NFRs | A | C | C | C | C | C | R |
| Crear Test Plan | R/A | C | C | I | I | C | I |
| Setup Entorno | A | C | I | I | C | R | I |
| Develop Scripts | A | R | I | C | I | I | I |
| Ejecutar Tests | A | R | I | I | I | C | I |
| Monitoreo | I | C | C | I | C | R | I |
| Análisis | A | C | R | C | C | I | I |
| Optimización | A | I | C | R | R | C | I |
| Reporting | R/A | C | R | I | I | I | I |
| Go/No-Go | R | I | C | C | C | C | A |

**R** = Responsible, **A** = Accountable, **C** = Consulted, **I** = Informed

---

## Career Path en Performance Engineering

```
Junior Perf Tester → Perf Test Engineer → Senior Perf Engineer →
  Principal Perf Engineer / Perf Architect → Engineering Manager / Director

Alternativas:
  → SRE / Reliability Engineer
  → Performance Consultant
  → Solutions Architect
  → DevOps Engineer
  → Technical Program Manager
```

### Certificaciones relevantes
| Certificación | Organización | Enfoque |
|--------------|-------------|---------|
| ISTQB Performance Testing | ISTQB | Fundamentos teóricos |
| LoadRunner Certified Professional | OpenText | LoadRunner específico |
| AWS Performance Efficiency | AWS | Cloud performance |
| Google Cloud Professional | Google | Cloud architecture |
| Certified Kubernetes Admin | CNCF | Container orchestration |

---

## Comunicación y Reporting

### Audiencias y contenido

| Audiencia | Qué necesitan | Formato |
|-----------|---------------|---------|
| C-Level / VP | Go/No-Go, risk summary | 1-page executive summary |
| Engineering Manager | Issues, timeline, resources | Dashboard + meeting |
| Development Team | Specific bottlenecks, code areas | Technical report + tickets |
| DBA | Query issues, indexes | SQL analysis report |
| DevOps/SRE | Infra metrics, scaling needs | Grafana dashboards |

### Cadencia de comunicación
```
Diario:    Status update (si hay ejecuciones activas)
Semanal:   Progress report, blockers, risks
Por test:  Resultado y análisis de cada ejecución
Sprint:    Trend analysis, regression report
Release:   Go/No-Go recommendation
Trimestral: Capacity planning update
```

---

*Documento de referencia - Performance Test Life Cycle*
*Última actualización: Junio 2026*
