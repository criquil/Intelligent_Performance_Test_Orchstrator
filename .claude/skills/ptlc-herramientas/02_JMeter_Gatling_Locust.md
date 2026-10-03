# JMeter y Otras Herramientas - Guía de Referencia

## Apache JMeter

### Arquitectura de JMeter

```
┌─────────────────────────────────────────────────────────────┐
│                     JMeter Test Plan                          │
├─────────────────────────────────────────────────────────────┤
│  Thread Group (Users)                                        │
│  ├── Config Elements (CSV, HTTP defaults, cookies)           │
│  ├── Pre-Processors (JSR223, parameters)                    │
│  ├── Samplers (HTTP, JDBC, JMS, TCP...)                     │
│  ├── Post-Processors (Extractors, assertions)               │
│  ├── Assertions (Response, Duration, JSON)                   │
│  ├── Timers (Think time, Synchronizing)                      │
│  └── Listeners (Results, Graphs, Reports)                    │
└─────────────────────────────────────────────────────────────┘
```

### Estructura del Test Plan

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2">
  <TestPlan guiclass="TestPlanGui" testname="E-Commerce Load Test">
    
    <!-- Thread Group: Main Load -->
    <ThreadGroup guiclass="ThreadGroupGui" testname="Purchase Flow">
      <intProp name="ThreadGroup.num_threads">100</intProp>
      <intProp name="ThreadGroup.ramp_time">300</intProp>
      <longProp name="ThreadGroup.duration">3600</longProp>
      
      <!-- HTTP Defaults -->
      <ConfigTestElement testname="HTTP Request Defaults">
        <stringProp name="HTTPSampler.domain">api.example.com</stringProp>
        <stringProp name="HTTPSampler.port">443</stringProp>
        <stringProp name="HTTPSampler.protocol">https</stringProp>
      </ConfigTestElement>
      
      <!-- CSV Data -->
      <CSVDataSet testname="User Data">
        <stringProp name="filename">data/users.csv</stringProp>
        <stringProp name="variableNames">username,password,email</stringProp>
        <stringProp name="delimiter">,</stringProp>
        <boolProp name="recycle">true</boolProp>
      </CSVDataSet>
      
      <!-- Transaction: Login -->
      <TransactionController testname="TC_Login">
        <HTTPSamplerProxy testname="POST /login">
          <stringProp name="HTTPSampler.method">POST</stringProp>
          <stringProp name="HTTPSampler.path">/api/login</stringProp>
          <stringProp name="HTTPSampler.postBodyRaw">
            {"username": "${username}", "password": "${password}"}
          </stringProp>
        </HTTPSamplerProxy>
        
        <!-- JSON Extractor for token -->
        <JSONPostProcessor testname="Extract Token">
          <stringProp name="JSONPostProcessor.jsonPathExprs">$.token</stringProp>
          <stringProp name="JSONPostProcessor.referenceNames">auth_token</stringProp>
        </JSONPostProcessor>
      </TransactionController>
      
      <!-- Think Time -->
      <GaussianRandomTimer testname="Think Time">
        <stringProp name="ConstantTimer.delay">5000</stringProp>
        <stringProp name="GaussianRandomTimer.range">2000</stringProp>
      </GaussianRandomTimer>
      
    </ThreadGroup>
  </TestPlan>
</jmeterTestPlan>
```

### Ejecución en modo CLI (Non-GUI)

```bash
# Basic execution
jmeter -n -t test-plan.jmx -l results.jtl -e -o report/

# With properties
jmeter -n -t test-plan.jmx \
  -Jthreads=500 \
  -Jrampup=300 \
  -Jduration=7200 \
  -Jhost=api.staging.com \
  -l results/$(date +%Y%m%d_%H%M%S).jtl \
  -e -o report/

# Distributed testing
jmeter -n -t test-plan.jmx \
  -R server1,server2,server3 \
  -l results.jtl
```

### Plugins esenciales de JMeter

| Plugin | Uso |
|--------|-----|
| Custom Thread Groups | Stepping, Ultimate, Arrivals Thread Groups |
| Throughput Shaping Timer | Control preciso de TPS |
| Response Times Over Time | Gráfico temporal de RT |
| Active Threads Over Time | Visualización de VUs |
| Transactions per Second | Gráfico de TPS |
| PerfMon | Monitoreo de servidores |
| Parallel Controller | Requests paralelas |
| JSON Path Extractor | Correlación JSON |
| Dummy Sampler | Para debugging |

---

## Gatling

### Estructura de un test Gatling (Scala DSL)

```scala
package simulations

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import scala.concurrent.duration._

class ECommerceSimulation extends Simulation {

  // HTTP Configuration
  val httpProtocol = http
    .baseUrl("https://api.example.com")
    .acceptHeader("application/json")
    .contentTypeHeader("application/json")
    .userAgentHeader("Gatling/Performance-Test")

  // Feeder (data parameterization)
  val userFeeder = csv("data/users.csv").random
  val searchFeeder = csv("data/search_terms.csv").random

  // Scenarios
  val loginScenario = scenario("Login Flow")
    .feed(userFeeder)
    .exec(
      http("POST Login")
        .post("/api/login")
        .body(StringBody("""{"username":"${username}","password":"${password}"}"""))
        .check(
          status.is(200),
          jsonPath("$.token").saveAs("authToken"),
          responseTimeInMillis.lte(2000)
        )
    )
    .pause(3, 8)  // Think time: 3-8 seconds

  val searchScenario = scenario("Search Flow")
    .feed(searchFeeder)
    .exec(
      http("GET Search")
        .get("/api/search")
        .queryParam("q", "${searchTerm}")
        .header("Authorization", "Bearer ${authToken}")
        .check(
          status.is(200),
          jsonPath("$.results").exists,
          responseTimeInMillis.lte(3000)
        )
    )
    .pause(5, 15)

  val purchaseScenario = scenario("Purchase Flow")
    .exec(loginScenario)
    .exec(searchScenario)
    .exec(
      http("POST Add to Cart")
        .post("/api/cart/add")
        .header("Authorization", "Bearer ${authToken}")
        .body(StringBody("""{"product_id": "PRD-001", "quantity": 1}"""))
        .check(status.is(201), jsonPath("$.cart_id").saveAs("cartId"))
    )
    .pause(2, 5)
    .exec(
      http("POST Checkout")
        .post("/api/checkout")
        .header("Authorization", "Bearer ${authToken}")
        .body(StringBody("""{"cart_id":"${cartId}","payment":"card_test"}"""))
        .check(status.is(200), responseTimeInMillis.lte(5000))
    )

  // Load Profile
  setUp(
    loginScenario.inject(
      rampUsers(200).during(5.minutes),
      constantUsersPerSec(10).during(30.minutes)
    ),
    searchScenario.inject(
      nothingFor(2.minutes),
      rampUsers(300).during(5.minutes),
      constantUsersPerSec(15).during(30.minutes)
    ),
    purchaseScenario.inject(
      nothingFor(5.minutes),
      rampUsers(100).during(5.minutes),
      constantUsersPerSec(5).during(30.minutes)
    )
  ).protocols(httpProtocol)
    .assertions(
      global.responseTime.percentile3.lt(3000),  // P95 < 3s
      global.successfulRequests.percent.gt(99),   // > 99% success
      forAll.responseTime.max.lt(10000)           // Max < 10s
    )
}
```

### Ejecución de Gatling

```bash
# Run simulation
./bin/gatling.sh --simulation simulations.ECommerceSimulation

# With parameters
./bin/gatling.sh \
  --simulation simulations.ECommerceSimulation \
  --run-description "Sprint 42 Load Test" \
  --results-folder /results/sprint42

# Maven execution
mvn gatling:test -Dgatling.simulationClass=simulations.ECommerceSimulation
```

---

## Locust (Python)

### Script ejemplo

```python
from locust import HttpUser, task, between, tag
from locust import events
import json
import random

class ECommerceUser(HttpUser):
    wait_time = between(3, 10)  # Think time: 3-10 seconds
    
    def on_start(self):
        """Login when user starts"""
        response = self.client.post("/api/login", json={
            "username": f"user_{self.environment.runner.user_count}@test.com",
            "password": "test123"
        })
        if response.status_code == 200:
            self.token = response.json()["token"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            self.token = None
            self.headers = {}
    
    @task(5)  # Weight: 5 (most common)
    @tag('browse')
    def browse_products(self):
        """Browse product catalog"""
        self.client.get("/api/products", headers=self.headers,
                       name="/api/products")
        
    @task(3)  # Weight: 3
    @tag('search')
    def search_products(self):
        """Search for products"""
        term = random.choice(["laptop", "phone", "tablet", "camera"])
        self.client.get(f"/api/search?q={term}", headers=self.headers,
                       name="/api/search?q=[term]")
    
    @task(1)  # Weight: 1 (least common)
    @tag('purchase')
    def purchase_flow(self):
        """Complete purchase flow"""
        # Add to cart
        cart_res = self.client.post("/api/cart/add", 
            json={"product_id": random.randint(1, 1000), "quantity": 1},
            headers=self.headers, name="/api/cart/add")
        
        if cart_res.status_code == 201:
            cart_id = cart_res.json()["cart_id"]
            
            # Checkout
            self.client.post("/api/checkout",
                json={"cart_id": cart_id, "payment": "test_card"},
                headers=self.headers, name="/api/checkout")
```

### Ejecución de Locust

```bash
# Web UI mode
locust -f locustfile.py --host=https://api.example.com

# Headless mode (CLI)
locust -f locustfile.py \
  --host=https://api.example.com \
  --headless \
  --users 500 \
  --spawn-rate 10 \
  --run-time 30m

# Distributed mode
# Master:
locust -f locustfile.py --master
# Workers:
locust -f locustfile.py --worker --master-host=192.168.1.100
```

---

## Comparativa de Sintaxis

### Mismo test en 4 herramientas

#### Escenario: Login + Get Profile

**k6 (JavaScript):**
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export default function() {
  const loginRes = http.post('https://api.example.com/login',
    JSON.stringify({ username: 'user1', password: 'pass' }),
    { headers: { 'Content-Type': 'application/json' } }
  );
  check(loginRes, { 'login ok': (r) => r.status === 200 });
  const token = loginRes.json('token');
  
  sleep(3);
  
  const profileRes = http.get('https://api.example.com/profile', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  check(profileRes, { 'profile ok': (r) => r.status === 200 });
  
  sleep(5);
}
```

**Gatling (Scala):**
```scala
scenario("Login and Profile")
  .exec(http("Login").post("/login")
    .body(StringBody("""{"username":"user1","password":"pass"}"""))
    .check(status.is(200), jsonPath("$.token").saveAs("token")))
  .pause(3)
  .exec(http("Get Profile").get("/profile")
    .header("Authorization", "Bearer ${token}")
    .check(status.is(200)))
  .pause(5)
```

**Locust (Python):**
```python
@task
def login_and_profile(self):
    res = self.client.post("/login", json={"username": "user1", "password": "pass"})
    token = res.json()["token"]
    time.sleep(3)
    self.client.get("/profile", headers={"Authorization": f"Bearer {token}"})
    time.sleep(5)
```

**JMeter (XML/GUI):**
```
Thread Group
├── HTTP Request (POST /login)
│   └── JSON Extractor ($.token → ${token})
├── Gaussian Random Timer (3000ms ± 1000ms)
├── HTTP Request (GET /profile)
│   └── Header Manager (Authorization: Bearer ${token})
└── Gaussian Random Timer (5000ms ± 2000ms)
```

---

## Selección de Herramienta - Decision Matrix

```
SCORING MATRIX (1-5 scale)
═══════════════════════════════════════════════════════════════════

Criteria (Weight)     │ k6  │ JMeter │ Gatling │ Locust │ LoadRunner
──────────────────────┼─────┼────────┼─────────┼────────┼──────────
Ease of Use (15%)     │  4  │   3    │    3    │   5    │    3
Protocol Support (20%)│  3  │   5    │    3    │   3    │    5
CI/CD Integration(15%)│  5  │   3    │    4    │   4    │    3
Scalability (15%)     │  5  │   3    │    5    │   4    │    5
Reporting (10%)       │  4  │   3    │    5    │   3    │    5
Cost (10%)            │  5  │   5    │    4    │   5    │    1
Community (10%)       │  4  │   5    │    3    │   4    │    3
Enterprise Support(5%)│  3  │   3    │    4    │   2    │    5
──────────────────────┼─────┼────────┼─────────┼────────┼──────────
WEIGHTED SCORE        │ 4.1 │  3.7   │   3.8   │  3.8   │   3.7

Best for: Developer   │ Multi│ High    │ Python │ Enterprise
teams, CI/CD,         │proto │ perf    │ teams  │ legacy
modern APIs           │      │ web/API │        │ protocols
```

---

*Documento de referencia - Performance Test Life Cycle*
*Última actualización: Junio 2026*
