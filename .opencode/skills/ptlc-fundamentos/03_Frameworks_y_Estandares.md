# Frameworks y Estándares de la Industria

## Estándares Internacionales

### ISO/IEC 25010 - Modelo de Calidad del Producto de Software

El estándar ISO 25010 define las características de calidad del software, siendo la **eficiencia de rendimiento** una de las 8 características principales.

#### Características de Eficiencia de Rendimiento

```
Eficiencia de Rendimiento (Performance Efficiency)
├── Comportamiento temporal (Time Behaviour)
│   └── Tiempos de respuesta y procesamiento
├── Utilización de recursos (Resource Utilization)
│   └── Cantidad y tipo de recursos utilizados
└── Capacidad (Capacity)
    └── Grado en que los límites máximos cumplen requisitos
```

#### Sub-características detalladas

| Sub-característica | Definición ISO | Métricas asociadas |
|-------------------|---------------|-------------------|
| **Time Behaviour** | Grado en que los tiempos de respuesta/procesamiento y throughput cumplen los requisitos | Response time, Throughput, Latency |
| **Resource Utilization** | Grado en que las cantidades y tipos de recursos usados cumplen requisitos | CPU%, Memory%, Disk I/O, Network |
| **Capacity** | Grado en que los límites máximos de un parámetro del producto cumplen requisitos | Max users, Max TPS, Max data volume |

---

### ISO/IEC 25023 - Medición de la Calidad del Sistema y Software

Proporciona medidas específicas para las características de ISO 25010:

#### Medidas de Time Behaviour
| ID | Medida | Fórmula |
|----|--------|---------|
| PTb-1-G | Mean response time | Σ(response_times) / n |
| PTb-2-G | Response time adequacy | Requests_within_SLA / Total_requests |
| PTb-3-G | Mean turnaround time | Σ(turnaround_times) / n |
| PTb-4-G | Throughput | Completed_tasks / Time_period |

#### Medidas de Resource Utilization
| ID | Medida | Fórmula |
|----|--------|---------|
| PRu-1-G | Mean processor utilization | Σ(CPU_usage) / measurements |
| PRu-2-G | Mean memory utilization | Σ(memory_usage) / measurements |
| PRu-3-G | Mean I/O device utilization | Σ(IO_usage) / measurements |
| PRu-4-S | Bandwidth utilization | Used_bandwidth / Available_bandwidth |

#### Medidas de Capacity
| ID | Medida | Fórmula |
|----|--------|---------|
| PCa-1-G | Transaction processing capacity | Max_TPS_within_SLA |
| PCa-2-S | User access capacity | Max_concurrent_users_within_SLA |
| PCa-3-S | Database size growth adequacy | Current_size / Max_size × 100 |

---

### IEEE 829 - Documentación de Testing

Aunque no es específico de performance testing, IEEE 829 proporciona el marco para documentación de pruebas que se aplica al PTLC:

| Documento | Aplicación en PTLC |
|-----------|-------------------|
| Test Plan | Performance Test Plan |
| Test Design Specification | Workload Model, Scenario Design |
| Test Case Specification | Performance Test Cases con datos |
| Test Procedure | Procedimiento de ejecución |
| Test Log | Execution logs y monitoring data |
| Test Incident Report | Performance defect reports |
| Test Summary Report | Performance Analysis Report |

---

### ISTQB - Performance Testing Foundation

El syllabus de ISTQB para Performance Testing define:

#### Proceso de Performance Testing (según ISTQB)
1. **Acordar requisitos de performance** con stakeholders
2. **Diseñar la prueba de performance** (escenarios, workload, environment)
3. **Implementar el diseño** (scripts, datos, entorno)
4. **Ejecutar la prueba** y monitorear
5. **Analizar resultados** y reportar
6. **Hacer seguimiento** de issues y re-test

#### Principios ISTQB aplicados a Performance Testing
- Testing muestra la presencia de defectos, no su ausencia
- Testing exhaustivo es imposible (priorizar escenarios)
- Testing temprano ahorra tiempo y dinero
- Los defectos se agrupan (Pareto: 80/20 rule)
- La paradoja del pesticida (rotar y evolucionar tests)
- Testing es dependiente del contexto
- La ausencia de errores es una falacia

---

## Frameworks de la Industria

### Microsoft Performance Testing Guidance

Microsoft proporciona un framework ampliamente adoptado:

#### Actividades del Performance Testing (Microsoft)
```
1. Identify Test Environment
2. Identify Performance Acceptance Criteria
3. Plan and Design Tests
4. Configure Test Environment
5. Implement Test Design
6. Execute Tests
7. Analyze Results, Report, Retest
```

#### Performance Testing Patterns (Microsoft)
| Pattern | Descripción |
|---------|-------------|
| **Baseline** | Establecer rendimiento inicial sin optimizaciones |
| **Benchmark** | Comparar contra estándares conocidos |
| **Load** | Verificar bajo carga esperada |
| **Stress** | Encontrar puntos de ruptura |
| **Capacity** | Determinar capacidad máxima |
| **Smoke** | Validación rápida de funcionalidad bajo carga mínima |

---

### Google SRE Framework

Google's Site Reliability Engineering aplica principios al performance testing:

#### The Four Golden Signals
| Signal | Definición | Relación con Perf Testing |
|--------|-----------|--------------------------|
| **Latency** | Tiempo para servir una request | Response time metric |
| **Traffic** | Demanda en el sistema | Throughput metric |
| **Errors** | Tasa de requests que fallan | Error rate metric |
| **Saturation** | Cuán "lleno" está el sistema | Resource utilization |

#### USE Method (Brendan Gregg)
Para cada recurso (CPU, Memory, Disk, Network):
- **U**tilization: Porcentaje de tiempo que el recurso está ocupado
- **S**aturation: Grado de trabajo extra que no puede ser servido
- **E**rrors: Número de eventos de error

```
Para cada recurso del sistema:
┌─────────────────────────────────────┐
│  Utilization → ¿Está ocupado?       │
│  Saturation  → ¿Hay cola?           │
│  Errors      → ¿Hay errores?        │
└─────────────────────────────────────┘
```

#### RED Method (Tom Wilkie)
Para cada servicio:
- **R**ate: Requests por segundo
- **E**rrors: Requests que fallan
- **D**uration: Distribución de latencias

---

### OWASP Performance Testing Guide

OWASP proporciona guías específicas para performance testing en contexto de seguridad:

#### Performance Testing Cheat Sheet
| Aspecto | Recomendación |
|---------|--------------|
| Authentication | Test login storms, token refresh under load |
| Session Management | Test session creation/destruction at scale |
| Input Validation | Test with varied/malformed input at volume |
| Error Handling | Verify error responses don't leak info under load |
| Rate Limiting | Validate rate limiting works correctly |
| Cryptography | Measure crypto overhead at scale |

---

### TMMi (Test Maturity Model integration)

Niveles de madurez aplicados a performance testing:

| Nivel | Nombre | Performance Testing characteristics |
|-------|--------|-------------------------------------|
| 1 | Initial | Ad-hoc, no process, reactive |
| 2 | Managed | Basic planning, some standards |
| 3 | Defined | Documented process, PTLC formal |
| 4 | Measured | Metrics-driven, predictable results |
| 5 | Optimization | Continuous improvement, proactive |

---

## Frameworks de Ejecución

### Continuous Performance Testing Framework

```
┌─────────────────────────────────────────────────────────────┐
│                 CONTINUOUS PERFORMANCE TESTING                │
├─────────────┬─────────────┬─────────────┬──────────────────┤
│   COMMIT    │    BUILD    │   DEPLOY    │   PRODUCTION     │
├─────────────┼─────────────┼─────────────┼──────────────────┤
│ Unit perf   │ Component   │ Integration │ Synthetic        │
│ benchmarks  │ load tests  │ load tests  │ monitoring       │
│             │             │             │                  │
│ Micro-      │ API perf    │ Full load   │ Real user        │
│ benchmarks  │ tests       │ tests       │ monitoring       │
│             │             │             │                  │
│ Static      │ Regression  │ Stress/Soak │ Chaos            │
│ analysis    │ detection   │ tests       │ experiments      │
├─────────────┼─────────────┼─────────────┼──────────────────┤
│ < 5 min     │ < 30 min    │ < 4 hours   │ Continuous       │
│ Every commit│ Every build │ Per release │ Always-on        │
└─────────────┴─────────────┴─────────────┴──────────────────┘
```

### Performance Testing Pyramid

```
                    ╱╲
                   ╱  ╲         Full System Tests
                  ╱ E2E╲        (Expensive, slow, realistic)
                 ╱──────╲
                ╱        ╲      Integration/API Tests
               ╱  API/Int ╲     (Moderate cost, focused)
              ╱────────────╲
             ╱              ╲   Component/Unit Benchmarks
            ╱  Unit/Micro    ╲  (Cheap, fast, narrow scope)
           ╱──────────────────╲
```

**Principio:** Más tests baratos y rápidos en la base, menos tests costosos en la cima.

---

## Métricas de Madurez del Performance Testing

### Assessment de Madurez

| Dimensión | Nivel 1 (Inicial) | Nivel 3 (Definido) | Nivel 5 (Optimizado) |
|-----------|-------------------|--------------------|-----------------------|
| **Proceso** | Ad-hoc, reactivo | Documentado, consistente | Automatizado, predictivo |
| **Herramientas** | Manuales, básicas | Estandarizadas | Integradas en CI/CD |
| **Skills** | Generalistas | Especialistas dedicados | T-shaped, cross-functional |
| **Entorno** | Compartido, inestable | Dedicado | On-demand, cloud-native |
| **Reporting** | Manual, irregular | Estandarizado | Automático, dashboards |
| **Integración** | Aislado | Con dev team | Totalmente integrado |
| **Datos** | Inventados | Subset producción | Mirror de producción |
| **Cobertura** | Solo pre-release | Sprint-level | Every commit |

---

## Compliance y Regulaciones

### Industrias con requisitos específicos de rendimiento

| Industria | Regulación/Estándar | Requisito de Performance |
|-----------|--------------------|--------------------------| 
| **Banca/Finanzas** | PCI DSS, SOX | Tiempos de transacción, disponibilidad |
| **Healthcare** | HIPAA, HL7 | Acceso a records, respuesta en emergencias |
| **Telecomunicaciones** | FCC, ITU | Latencia, calidad de servicio |
| **E-commerce** | Varies | SLA contractuales con merchants |
| **Gobierno** | Section 508, WCAG | Accesibilidad incluye performance |
| **Aviación** | DO-178C | Real-time response requirements |

### Documentación para Compliance
```
Evidencia requerida típicamente:
├── Test Plan aprobado
├── Environment specification
├── Test execution logs (inmutables)
├── Results analysis con timestamps
├── Sign-off de stakeholders
├── Audit trail de cambios
└── Retención por período regulatorio (3-7 años típico)
```

---

## Referencias y Recursos Adicionales

### Libros fundamentales
| Título | Autor | Enfoque |
|--------|-------|---------|
| *The Art of Application Performance Testing* | Ian Molyneaux | Metodología general |
| *Performance Testing with JMeter* | Bayo Erinle | JMeter práctico |
| *Systems Performance* | Brendan Gregg | Análisis profundo de sistemas |
| *Site Reliability Engineering* | Google | SRE y performance |
| *Web Performance in Action* | Jeremy Wagner | Web performance |
| *Every Computer Performance Book* | Bob Wescott | Fundamentos |

### Comunidades y recursos online
- **PerfBytes** - Podcast de performance testing
- **Performance Testing Community** - LinkedIn group
- **BlazeMeter University** - Cursos gratuitos
- **k6 Learn** - Tutoriales de k6
- **WOPR (Workshop on Performance and Reliability)** - Conferencia

---

*Documento de referencia - Performance Test Life Cycle*
*Última actualización: Junio 2026*
