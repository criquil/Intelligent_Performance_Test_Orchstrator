# Workload Modeling - Guía Exhaustiva

## Fundamentos Teóricos

### ¿Qué hace un buen Workload Model?

Un workload model efectivo es aquel que **reproduce fielmente el comportamiento real de los usuarios** en el sistema. La calidad del modelo determina directamente la validez de los resultados.

```
REALIDAD (Producción)          →   MODELO (Test)
══════════════════════              ══════════════
Múltiples tipos de usuarios        Múltiples escenarios
Comportamiento variable            Think times con distribución
Patrones temporales                Ramp-up/steady/ramp-down
Datos diversos                     Parametrización
Navegación no-lineal               Flujos con variabilidad
Abandono de sesiones               Drop-off rates
Dispositivos variados              Diferentes configuraciones
```

---

## Recolección de Datos para el Modelo

### Fuentes de datos

#### 1. Web Analytics (Google Analytics, Adobe, etc.)
```
Datos extraíbles:
- Sessions por hora/día (traffic patterns)
- Average session duration
- Pages per session
- Bounce rate
- Top landing pages
- User flow (navigation paths)
- Device breakdown (desktop/mobile/tablet)
- Geographic distribution
- New vs returning users

Ejemplo de extracción:
┌────────────────────────────────────────────────────┐
│ Peak Hour Analysis (10:00 - 11:00 AM)              │
├────────────────────────────────────────────────────┤
│ Sessions: 5,200                                    │
│ Avg Duration: 4.5 minutes                          │
│ Pages/Session: 6.2                                 │
│ Concurrent Users (estimated): 5200 × 4.5/60 = 390 │
│ Requests/Session: 6.2 × 3 (assets) = 18.6         │
│ RPS: 390 × 18.6 / 270s = 26.8 RPS per user batch  │
└────────────────────────────────────────────────────┘
```

#### 2. Server Access Logs
```bash
# Analyze peak hour traffic
awk '$4 ~ /10:00|10:30|11:00/' access.log | wc -l

# Requests per second distribution
awk '{print $4}' access.log | cut -d: -f2-4 | uniq -c | sort -rn | head

# Top endpoints by frequency
awk '{print $7}' access.log | sort | uniq -c | sort -rn | head -20

# Response time distribution
awk '{print $NF}' access.log | sort -n | awk '
  BEGIN {count=0; sum=0}
  {a[count++]=$1; sum+=$1}
  END {
    print "Count:", count
    print "Average:", sum/count, "ms"
    print "P50:", a[int(count*0.50)]
    print "P90:", a[int(count*0.90)]
    print "P95:", a[int(count*0.95)]
    print "P99:", a[int(count*0.99)]
  }'

# User session analysis
awk '{print $1}' access.log | sort | uniq -c | sort -rn | awk '
  {sessions++; total_requests+=$1}
  END {print "Avg requests/session:", total_requests/sessions}'
```

#### 3. APM Data
```
Datos extraíbles de APM:
- Transaction breakdown por tipo
- Response time baselines
- Error rates por endpoint
- Dependency call patterns
- Database query patterns
- External service call frequency

Ejemplo (New Relic/Dynatrace):
Transaction             │ Calls/min │ Avg RT  │ % of total
────────────────────────┼───────────┼─────────┼───────────
GET /api/products       │   2,400   │  120ms  │   35%
GET /api/search         │   1,200   │  350ms  │   18%
POST /api/cart          │     600   │   80ms  │    9%
GET /api/user/profile   │     500   │   60ms  │    7%
POST /api/orders        │     200   │  450ms  │    3%
(otros 40 endpoints)    │   1,900   │  various│   28%
```

#### 4. Business Intelligence
```
Datos del negocio:
- Ventas por hora/día
- Conversion funnel rates
- Cart abandonment rate
- Seasonal patterns
- Planned marketing events
- Growth projections

Ejemplo de conversion funnel:
Homepage visits:     100%  (10,000/hour)
Product views:        60%  (6,000/hour)
Add to cart:          15%  (1,500/hour)
Start checkout:        8%  (800/hour)
Complete purchase:     4%  (400/hour)

→ Esto define la distribución de scenarios
```

---

## Modelado Matemático

### Cálculos fundamentales

#### Concurrent Users

```
Método 1: Desde sessions
───────────────────────
Concurrent_Users = (Active_Sessions × Avg_Session_Duration) / Observation_Period

Ejemplo:
- 5,000 sessions en 1 hora
- Avg session = 5 minutos
Concurrent = (5000 × 5min) / 60min = 417 users

Método 2: Desde throughput (Little's Law)
────────────────────────────────────────
Concurrent_Users = Throughput × Avg_Response_Time

Ejemplo:
- Throughput = 200 RPS
- Avg Response = 0.3s
Concurrent = 200 × 0.3 = 60 active requests

Método 3: Desde requests por usuario
────────────────────────────────────
VUsers_Needed = Target_RPS × (Think_Time + Response_Time) / Requests_Per_Iteration

Ejemplo:
- Target: 500 RPS
- Think time: 5s
- Response time: 0.5s
- Requests per iteration: 3
VUsers = 500 × (5 + 0.5) / 3 = 917 VUsers
```

#### Pacing Calculation

```
Pacing = How often a VUser starts a new iteration

Approach 1: Throughput-driven
─────────────────────────────
Target: 100 business transactions per hour per user type
Pacing = 3600s / 100 = 36 seconds between iterations

Approach 2: Response-time-aware
───────────────────────────────
Desired_Iteration_Time = 60 seconds
Actual_Script_Duration = 25 seconds (think time + response time)
Pacing_Delay = 60 - 25 = 35 seconds wait after iteration

Approach 3: Dynamic (throughput controller)
──────────────────────────────────────────
Target_TPS = 50
If more VUs available → reduce individual pacing
If fewer VUs → increase pacing
(Tools like k6's constant-arrival-rate handle this automatically)
```

#### Think Time Distribution

```
Real user think times follow a LOG-NORMAL distribution:
(NOT normal/Gaussian!)

Why log-normal?
- Think time is always positive (can't be negative)
- Most users are relatively fast
- Some users are much slower (long tail)
- Multiplicative factors (reading speed × page length × interruptions)

Parameters:
- μ (mu): location parameter
- σ (sigma): scale parameter

Median = e^μ
Mean = e^(μ + σ²/2)

Example: Target median=8s, mean=10s
σ² = 2 × (ln(mean) - ln(median)) = 2 × (ln(10) - ln(8)) = 0.446
σ = 0.668
μ = ln(median) = ln(8) = 2.079

Implementation (k6):
function logNormalThinkTime(median, sigma) {
  const mu = Math.log(median);
  // Box-Muller transform for normal random
  const u1 = Math.random();
  const u2 = Math.random();
  const z = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
  return Math.exp(mu + sigma * z);
}
```

---

## Patrones de Tráfico

### Patrones temporales típicos

#### E-commerce (B2C)
```
Users
 ┤                        ╱╲
 ┤                       ╱  ╲
 ┤              ╱╲      ╱    ╲
 ┤             ╱  ╲    ╱      ╲
 ┤            ╱    ╲  ╱        ╲
 ┤     ╱╲   ╱      ╲╱          ╲
 ┤    ╱  ╲ ╱                     ╲
 ┤───╱    ╲╱                      ╲───
 └──────────────────────────────────────→
   6am  9am  12pm  3pm  6pm  9pm  12am
   
Peaks: 10-11am (morning browse), 8-9pm (evening shopping)
Valley: 2-5am
Weekend: Similar pattern, slightly later peaks
```

#### Enterprise SaaS (B2B)
```
Users
 ┤              ┌──────────────┐
 ┤             ╱│              │╲
 ┤            ╱ │  Workday     │ ╲
 ┤           ╱  │  plateau     │  ╲
 ┤          ╱   │              │   ╲
 ┤         ╱    │              │    ╲
 ┤────────╱     │              │     ╲────
 └──────────────────────────────────────────→
   6am  8am  9am              5pm  6pm  8pm
   
Peaks: 9am (login storm), 2pm (post-lunch)
Valleys: Nights, weekends
Monday morning: Highest spike of the week
```

#### Global Application (24/7)
```
Users
 ┤──────────────────────────────────────
 ┤   US peak    EU peak    APAC peak
 ┤   ╱╲         ╱╲         ╱╲
 ┤──╱──╲───────╱──╲───────╱──╲────────
 ┤ ╱    ╲     ╱    ╲     ╱    ╲
 ┤╱      ╲   ╱      ╲   ╱      ╲
 └──────────────────────────────────────→
   0h   4h   8h   12h  16h  20h  24h UTC
   
No real valley - overlapping time zones
Peak: Multiple regional peaks
Consideration: Load from multiple regions simultaneously
```

---

## Template Completo de Workload Model

```yaml
# WORKLOAD MODEL SPECIFICATION
# Project: E-Commerce Platform
# Version: 2.1
# Date: 2026-06-10

metadata:
  application: "ShopFast E-Commerce"
  environment: "Performance Test (AWS)"
  baseline_source: "Production analytics, May 2026"
  growth_factor: 1.5  # 50% growth projection

target_load:
  concurrent_users: 1000
  peak_rps: 800
  peak_tps: 120  # Business transactions per second
  
user_distribution:
  browsers:
    desktop: 55%
    mobile: 35%
    tablet: 10%
  new_vs_returning:
    new: 30%
    returning: 70%

scenarios:
  - id: "SC-01"
    name: "Anonymous Browsing"
    weight: 40%
    vusers: 400
    description: "Users browsing without login"
    steps:
      - { action: "GET /", think_time: "lognormal(5,0.5)" }
      - { action: "GET /category/{cat_id}", think_time: "lognormal(8,0.6)" }
      - { action: "GET /product/{prod_id}", think_time: "lognormal(12,0.7)" }
      - { action: "GET /product/{prod_id}", think_time: "lognormal(10,0.6)" }
    pacing: "random(180,300)"  # 3-5 minutes per iteration
    data:
      cat_id: "random from categories.csv (20 categories)"
      prod_id: "random from products.csv (10000 products)"
    drop_off_rate: 30%  # 30% leave after step 2
    
  - id: "SC-02"
    name: "Search and Compare"
    weight: 25%
    vusers: 250
    description: "Users searching and comparing products"
    steps:
      - { action: "GET /", think_time: "lognormal(3,0.4)" }
      - { action: "GET /search?q={term}", think_time: "lognormal(6,0.5)" }
      - { action: "GET /search?q={term}&filter={filter}", think_time: "lognormal(5,0.5)" }
      - { action: "GET /product/{prod_id}", think_time: "lognormal(10,0.6)" }
      - { action: "GET /compare?ids={id1},{id2}", think_time: "lognormal(15,0.7)" }
    pacing: "random(240,360)"  # 4-6 minutes
    data:
      term: "zipf distribution from search_terms.csv (500 terms)"
      filter: "random from ['price_asc','rating_desc','newest']"
    
  - id: "SC-03"
    name: "Full Purchase Flow"
    weight: 15%
    vusers: 150
    description: "Complete end-to-end purchase"
    steps:
      - { action: "POST /login", think_time: "lognormal(2,0.3)" }
      - { action: "GET /search?q={term}", think_time: "lognormal(5,0.5)" }
      - { action: "GET /product/{prod_id}", think_time: "lognormal(10,0.6)" }
      - { action: "POST /cart/add", think_time: "lognormal(3,0.4)" }
      - { action: "GET /cart", think_time: "lognormal(8,0.6)" }
      - { action: "POST /checkout/shipping", think_time: "lognormal(25,0.8)" }
      - { action: "POST /checkout/payment", think_time: "lognormal(10,0.6)" }
    pacing: "random(420,720)"  # 7-12 minutes
    drop_off_rates:
      after_cart: 25%
      after_shipping: 10%
    data:
      credentials: "unique from users.csv (5000 users)"
      payment: "test credit cards from payments.csv"
      
  - id: "SC-04"
    name: "Account Management"
    weight: 10%
    vusers: 100
    steps:
      - { action: "POST /login", think_time: "lognormal(2,0.3)" }
      - { action: "GET /profile", think_time: "lognormal(8,0.5)" }
      - { action: "GET /orders", think_time: "lognormal(10,0.6)" }
      - { action: "GET /orders/{order_id}", think_time: "lognormal(12,0.6)" }
      - { action: "PUT /profile/settings", think_time: "lognormal(20,0.7)" }
    pacing: "random(300,480)"  # 5-8 minutes
    
  - id: "SC-05"
    name: "API Mobile Clients"
    weight: 10%
    vusers: 100
    description: "Direct API calls from mobile app"
    steps:
      - { action: "POST /api/v2/auth", think_time: "constant(1)" }
      - { action: "GET /api/v2/feed", think_time: "lognormal(3,0.4)" }
      - { action: "GET /api/v2/notifications", think_time: "lognormal(5,0.5)" }
      - { action: "POST /api/v2/cart/sync", think_time: "lognormal(2,0.3)" }
    pacing: "random(120,180)"  # 2-3 minutes
    note: "Higher frequency, shorter think times (mobile behavior)"

load_profile:
  type: "load_test"
  phases:
    - { name: "ramp_up", duration: "30m", start: 0, end: 1000, pattern: "linear" }
    - { name: "steady_state", duration: "120m", users: 1000, pattern: "constant" }
    - { name: "ramp_down", duration: "10m", start: 1000, end: 0, pattern: "linear" }
  total_duration: "160 minutes"

data_requirements:
  users: { count: 5000, attributes: ["unique email", "valid password", "profile"] }
  products: { count: 10000, attributes: ["id", "name", "category", "in_stock"] }
  search_terms: { count: 500, distribution: "zipf (power law)" }
  addresses: { count: 1000, attributes: ["valid format by country"] }
  payment_methods: { count: 100, attributes: ["test cards, various types"] }

validation:
  expected_rps: "~800 RPS at steady state"
  expected_tps: "~120 business TPS"
  formula: |
    RPS = Σ(vusers_per_scenario × requests_per_iteration / iteration_time)
    SC-01: 400 × 4 / 240s = 6.7 RPS per user × 400 = 2,667? 
    Adjusted with think time: 400 × 4 / (4×8 + 240) = ~5.9 → 400 × 0.015 = 5.9
    (Note: Validate with pilot test)
```

---

## Validación y Calibración

### Proceso de calibración

```
1. Pilot Test (5-10 VUsers, 5 minutes)
   └─ Verify: Scripts work, data flows, assertions pass

2. Throughput Validation (50 VUsers, 10 minutes)
   └─ Verify: Actual TPS matches calculated TPS
   └─ Adjust: Think times if throughput too high/low

3. Resource Validation (100 VUsers, 15 minutes)
   └─ Verify: Load generators not saturated
   └─ Verify: Monitoring capturing data

4. Scale Test (500 VUsers, 30 minutes)
   └─ Verify: Linear scaling from 100 to 500
   └─ Adjust: Any parameters based on behavior

5. Full Calibration (1000 VUsers, 60 minutes)
   └─ Verify: All metrics match expectations
   └─ Document: Final calibrated model
```

---

*Documento de referencia - Performance Test Life Cycle*
*Última actualización: Junio 2026*
