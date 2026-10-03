# Fase 2: Planificación y Fase 3: Diseño de Pruebas

## FASE 2: PLANIFICACIÓN DE PRUEBAS

### Propósito
Transformar los requisitos recopilados en un plan accionable que defina qué, cómo, cuándo, dónde y con qué se van a ejecutar las pruebas de rendimiento.

---

### Estructura del Performance Test Plan

#### 1. Introducción y Objetivos
```markdown
## Objetivos del Plan
- Validar que el sistema cumple con los NFRs definidos en [PRS doc]
- Identificar cuellos de botella antes del release [version]
- Establecer baseline de rendimiento para future comparisons
- Proveer datos para capacity planning del próximo trimestre

## Alcance
### In-scope:
- Login y autenticación
- Flujo de compra completo
- Búsqueda de productos
- API endpoints públicos (v2)

### Out-of-scope:
- Admin panel (< 10 usuarios)
- Batch processing nocturno (testado por separado)
- Mobile app nativa (solo API backend)
```

#### 2. Estrategia de Testing

```yaml
test_strategy:
  types:
    load_test:
      objective: "Validar SLAs bajo carga esperada"
      scenarios: "All in-scope"
      duration: "2.5 hours (30min ramp + 2h steady)"
      users: 1000
      priority: 1
      
    stress_test:
      objective: "Encontrar breaking point"
      scenarios: "Login + Search + Checkout"
      approach: "Incremental +200 users/5min"
      max_users: 5000
      priority: 2
      
    endurance_test:
      objective: "Detectar memory/resource leaks"
      scenarios: "All in-scope"
      duration: "24 hours"
      users: 700
      priority: 3
      
    spike_test:
      objective: "Validar auto-scaling"
      scenarios: "Homepage + Search"
      spike: "200 → 3000 users in 30s"
      priority: 4
      
  execution_order:
    1: "Smoke test (validate scripts)"
    2: "Baseline test (minimal load)"
    3: "Load test"
    4: "Stress test"
    5: "Endurance test"
    6: "Spike test"
    7: "Re-tests (post optimization)"
```

#### 3. Entorno y Herramientas

```yaml
environment:
  target:
    servers:
      application: "4x m5.2xlarge (8 CPU, 32GB RAM)"
      database: "1x r5.4xlarge (16 CPU, 128GB RAM) + 2 read replicas"
      cache: "1x ElastiCache r6g.large (Redis 7)"
      load_balancer: "AWS ALB"
    network: "VPC peering, same region as production"
    data: "Anonymized copy of production (15M users, 80M orders)"
    
  load_generators:
    tool: "k6 v0.47"
    machines: "4x c5.2xlarge (load generation)"
    controller: "1x m5.large (orchestration)"
    
  monitoring:
    apm: "New Relic APM"
    infrastructure: "Prometheus + Grafana"
    logs: "ELK Stack"
    custom: "k6 Cloud for real-time results"
```

#### 4. Cronograma

```
Week 1: Environment setup + Script development
Week 2: Script validation + Baseline tests
Week 3: Load tests + Stress tests
Week 4: Endurance + Spike tests + Analysis
Week 5: Re-tests (after fixes) + Final report

Milestones:
- M1: Environment ready (Week 1, Day 4)
- M2: Scripts validated (Week 2, Day 3)
- M3: Initial results available (Week 3, Day 2)
- M4: Final report delivered (Week 5, Day 3)
- M5: Go/No-Go recommendation (Week 5, Day 5)
```

#### 5. Criterios de Entrada y Salida

```yaml
entry_criteria:
  - "Application deployed and stable (no known critical bugs)"
  - "Environment configured and validated"
  - "Test data loaded and verified"
  - "Scripts developed and smoke-tested"
  - "Monitoring configured and collecting data"
  - "Stakeholders notified and available"
  
exit_criteria:
  - "All planned test types executed"
  - "Results analyzed and documented"
  - "Bottlenecks identified with root cause"
  - "Recommendations provided"
  - "Go/No-Go recommendation issued"
  - "Stakeholder sign-off obtained"
  
abort_criteria:
  - "Environment instability (crashes, restarts)"
  - "Error rate > 50% during execution"
  - "Critical bug blocking test scenarios"
  - "Monitoring failure (unable to collect data)"
  - "External dependency unavailable"
```

#### 6. Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|-----------|
| Entorno no disponible a tiempo | Media | Alto | Empezar setup en paralelo con scripting |
| Datos de prueba insuficientes | Baja | Alto | Generador de datos como fallback |
| Herramienta no soporta protocolo | Baja | Alto | Evaluación técnica early |
| Equipo sin disponibilidad | Media | Medio | Backup members identificados |
| Resultados no concluyentes | Media | Medio | Múltiples ejecuciones, diferentes condiciones |
| Dependencias externas inestables | Alta | Medio | Mocks como fallback |

---

## FASE 3: DISEÑO DE PRUEBAS

### Propósito
Transformar la estrategia del plan en diseños detallados y ejecutables: escenarios específicos, workload models precisos, y especificaciones de monitoreo.

---

### 1. Diseño de Escenarios de Prueba

#### Template de escenario

```yaml
scenario_id: "SC-001"
name: "Complete Purchase Flow"
priority: "Critical"
type: "Business Transaction"

description: |
  Simulates a user completing a full purchase:
  browsing → selecting → adding to cart → checkout → payment

steps:
  1:
    name: "Open Homepage"
    method: "GET"
    url: "/homepage"
    think_time: "5-8s (normal)"
    expected_response: 200
    assertions:
      - "body contains 'Welcome'"
      - "response_time < 2000ms"
      
  2:
    name: "Search Product"
    method: "GET"
    url: "/api/search?q=${search_term}"
    think_time: "3-6s (normal)"
    expected_response: 200
    assertions:
      - "body contains 'results'"
      - "json $.results.length > 0"
      
  3:
    name: "View Product Detail"
    method: "GET"
    url: "/products/${product_id}"
    think_time: "8-15s (normal)"
    correlation: "Extract product_id from search results"
    expected_response: 200
    
  4:
    name: "Add to Cart"
    method: "POST"
    url: "/api/cart/add"
    body: '{"product_id": "${product_id}", "quantity": 1}'
    think_time: "2-4s"
    correlation: "Extract cart_id from response"
    expected_response: 201
    
  5:
    name: "View Cart"
    method: "GET"
    url: "/api/cart/${cart_id}"
    think_time: "5-10s"
    expected_response: 200
    
  6:
    name: "Enter Shipping"
    method: "POST"
    url: "/api/checkout/shipping"
    body: '{"cart_id": "${cart_id}", "address": "${address}"}'
    think_time: "15-30s (filling form)"
    expected_response: 200
    
  7:
    name: "Process Payment"
    method: "POST"
    url: "/api/checkout/payment"
    body: '{"cart_id": "${cart_id}", "payment_method": "${payment}"}'
    think_time: "5-10s"
    expected_response: 200
    assertions:
      - "json $.status == 'confirmed'"
      - "response_time < 5000ms"

data_requirements:
  - "100+ unique search terms"
  - "1000+ unique user accounts with valid credentials"
  - "Valid payment methods (test cards)"
  - "Valid shipping addresses"
  
transactions_to_measure:
  - "T01_Homepage": [step 1]
  - "T02_Search": [step 2]
  - "T03_ViewProduct": [step 3]
  - "T04_AddToCart": [step 4]
  - "T05_Checkout": [steps 5-7]
  - "T06_EndToEnd": [steps 1-7]
```

---

### 2. Workload Model Detallado

#### Distribución de escenarios

```
WORKLOAD DISTRIBUTION
═══════════════════════════════════════════════════════════

Total Target Users: 1,000 concurrent

Scenario Breakdown:
┌──────────────────────┬────────┬───────┬──────────────┐
│ Scenario             │ Weight │ Users │ Behavior     │
├──────────────────────┼────────┼───────┼──────────────┤
│ Browse Only          │  45%   │  450  │ View pages   │
│ Search & Compare     │  25%   │  250  │ Search+view  │
│ Full Purchase        │  15%   │  150  │ End-to-end   │
│ Account Management   │  10%   │  100  │ Profile/hist │
│ API Direct (mobile)  │   5%   │   50  │ API calls    │
└──────────────────────┴────────┴───────┴──────────────┘

Think Time Matrix:
┌──────────────────────┬──────────┬────────┬───────────┐
│ Action Type          │ Min (s)  │ Avg (s)│ Max (s)   │
├──────────────────────┼──────────┼────────┼───────────┤
│ Page view/read       │    3     │    8   │    20     │
│ Form filling         │   10     │   25   │    60     │
│ Decision making      │    5     │   15   │    45     │
│ Between transactions │   30     │   60   │   180     │
│ API calls (mobile)   │    1     │    3   │    8      │
└──────────────────────┴──────────┴────────┴───────────┘

Pacing:
- Browse: 1 iteration every 3-5 minutes
- Search: 1 iteration every 4-6 minutes
- Purchase: 1 iteration every 7-12 minutes
- Account: 1 iteration every 5-8 minutes
- API: 1 iteration every 2-3 minutes
```

#### Load Profile Timeline

```
LOAD PROFILE: Load Test (2.5 hours total)
═══════════════════════════════════════════

Phase 1: Ramp-up (30 minutes)
- Linear increase from 0 to 1000 users
- Rate: ~33 users/minute
- Purpose: Gradual warm-up, cache population

Phase 2: Steady State (2 hours)
- Maintain 1000 concurrent users
- Purpose: Sustained performance measurement
- Data collection window: Full 2 hours

Phase 3: Ramp-down (10 minutes)
- Linear decrease from 1000 to 0
- Purpose: Verify clean shutdown, resource release

Timeline Visualization:
Users
1000 ├────────────────────────────────────────────────────┐
     │       ╱│                                          │╲
 750 │      ╱ │                                          │ ╲
     │     ╱  │          STEADY STATE                    │  ╲
 500 │    ╱   │          (2 hours)                       │   ╲
     │   ╱    │                                          │    ╲
 250 │  ╱     │                                          │     ╲
     │ ╱      │                                          │      ╲
   0 ├╱───────┴──────────────────────────────────────────┴───────╲─
     0       30min                                    150min    160min
```

---

### 3. Diseño de Monitoreo

#### Monitoring Design Document

```yaml
monitoring_design:
  
  layer_1_user_experience:
    source: "Load testing tool (k6)"
    metrics:
      - response_time_per_transaction (all percentiles)
      - throughput_per_second
      - error_rate
      - active_virtual_users
    collection_interval: "real-time (per request)"
    dashboard: "k6 Cloud / Grafana"
    
  layer_2_application:
    source: "New Relic APM"
    metrics:
      - transaction_traces
      - error_analytics
      - thread_count
      - gc_pause_time
      - heap_usage
      - connection_pool_usage
    collection_interval: "1 second"
    alerts:
      - "Response time P95 > 3x baseline"
      - "Error rate > 5%"
      - "GC pause > 1 second"
      
  layer_3_database:
    source: "PostgreSQL pg_stat + Prometheus"
    metrics:
      - active_connections
      - query_duration_avg
      - locks_waiting
      - buffer_cache_hit_ratio
      - rows_returned_per_second
      - deadlocks
    collection_interval: "5 seconds"
    alerts:
      - "Active connections > 80% of max"
      - "Lock wait time > 5 seconds"
      
  layer_4_infrastructure:
    source: "Prometheus + node_exporter"
    metrics:
      - cpu_utilization_per_core
      - memory_used_percent
      - disk_io_utilization
      - network_bytes_in_out
      - tcp_connections
    collection_interval: "5 seconds"
    alerts:
      - "CPU > 85% for 2 minutes"
      - "Memory > 90%"
      - "Disk I/O > 80%"
      
  layer_5_cache:
    source: "Redis INFO + Prometheus"
    metrics:
      - hit_ratio
      - memory_usage
      - connected_clients
      - keys_evicted
      - commands_per_second
    collection_interval: "5 seconds"
```

---

### 4. Data Requirements Design

```yaml
test_data_design:
  
  user_accounts:
    total: 5000
    attributes:
      - username (unique)
      - password (hashed)
      - email (unique)
      - profile_complete: true
      - valid_payment_method: true
    source: "Generated with Faker, pre-loaded in DB"
    format: "CSV for parameterization"
    
  product_catalog:
    total: 10000
    attributes:
      - product_id
      - name
      - category (20 categories)
      - price (range: $1 - $5000)
      - in_stock: true
    source: "Subset of production data (anonymized)"
    
  search_terms:
    total: 500
    source: "Production search logs (top 500 terms)"
    distribution: "Zipf distribution (realistic)"
    
  addresses:
    total: 1000
    source: "Generated with Faker (valid format)"
    
  data_management:
    reset_strategy: "Database restore from snapshot between tests"
    growth_during_test: "~15,000 new orders created per load test"
    cleanup: "Automated script post-test"
```

---

### 5. Success Criteria Matrix

```
ACCEPTANCE CRITERIA MATRIX
═══════════════════════════════════════════════════════════════════

Transaction          │ P50    │ P90    │ P95    │ P99    │ Max    │ TPS
─────────────────────┼────────┼────────┼────────┼────────┼────────┼─────
T01_Homepage         │ <500ms │ <1.0s  │ <1.5s  │ <3.0s  │ <5.0s  │ ≥150
T02_Search           │ <800ms │ <1.5s  │ <2.0s  │ <4.0s  │ <8.0s  │ ≥80
T03_ViewProduct      │ <600ms │ <1.0s  │ <1.5s  │ <3.0s  │ <5.0s  │ ≥100
T04_AddToCart        │ <400ms │ <800ms │ <1.0s  │ <2.0s  │ <4.0s  │ ≥50
T05_Checkout         │ <1.0s  │ <2.0s  │ <3.0s  │ <5.0s  │ <10s   │ ≥30
T06_EndToEnd         │ <3.0s  │ <5.0s  │ <7.0s  │ <12s   │ <20s   │ ≥15
─────────────────────┼────────┴────────┴────────┴────────┴────────┴─────
Error Rate           │ < 0.5% overall, < 0.1% for checkout
Resource Util.       │ CPU < 75%, Memory < 80%, DB Conn < 85%
Throughput           │ Aggregate ≥ 500 TPS
```

---

*Documento de referencia - Performance Test Life Cycle*
*Última actualización: Junio 2026*
