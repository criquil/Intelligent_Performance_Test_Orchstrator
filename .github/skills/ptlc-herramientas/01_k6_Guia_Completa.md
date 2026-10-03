# k6 - Guía Completa de Referencia

## Introducción a k6

### ¿Qué es k6?
k6 es una herramienta moderna de performance testing open-source, desarrollada por Grafana Labs. Está diseñada para ser developer-friendly, con scripting en JavaScript y un motor de ejecución en Go que la hace extremadamente eficiente.

### Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                        k6 Engine (Go)                         │
├─────────────────┬───────────────────────┬───────────────────┤
│   JavaScript    │   HTTP/2 Client       │   Metrics Engine  │
│   Runtime       │   gRPC Client         │   (time series)   │
│   (goja)        │   WebSocket Client    │                   │
├─────────────────┼───────────────────────┼───────────────────┤
│   VU Scheduler  │   Checks/Thresholds   │   Output Plugins  │
│   (executors)   │   (assertions)        │   (cloud, json,   │
│                 │                       │    prometheus...)  │
└─────────────────┴───────────────────────┴───────────────────┘
```

### Ventajas clave
- **JavaScript (ES6)**: Lenguaje familiar para la mayoría de developers
- **Go engine**: Eficiente en uso de recursos (no usa threads por VU)
- **CLI-first**: Ideal para CI/CD y automatización
- **Extensible**: xk6 modules para funcionalidad adicional
- **Grafana integration**: Visualización nativa de resultados
- **Open source**: AGPL-3.0 license

---

## Instalación y Setup

### Instalación

```bash
# Windows (Chocolatey)
choco install k6

# Windows (winget)
winget install k6

# macOS
brew install k6

# Linux (Debian/Ubuntu)
sudo gpg -k
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg \
  --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | \
  sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update && sudo apt-get install k6

# Docker
docker run --rm -i grafana/k6 run - < script.js
```

---

## Conceptos Fundamentales

### Virtual Users (VUs) y Iterations

```javascript
// Cada VU ejecuta la función default() en un loop
// Una "iteration" = una ejecución completa de default()

export default function() {
  // Esta función se ejecuta N veces por cada VU
  // VU 1: iteration 1, 2, 3, 4, ...
  // VU 2: iteration 1, 2, 3, 4, ...
  // ...
  http.get('https://api.example.com');
  sleep(1);
}
```

### Executors (Tipos de carga)

| Executor | Uso | Descripción |
|----------|-----|-------------|
| `shared-iterations` | Smoke test | N iteraciones divididas entre VUs |
| `per-vu-iterations` | Fixed work | Cada VU hace N iteraciones |
| `constant-vus` | Steady state | N VUs constantes por duración |
| `ramping-vus` | Load/Stress | VUs que suben/bajan según stages |
| `constant-arrival-rate` | Throughput target | Mantener TPS constante |
| `ramping-arrival-rate` | Variable throughput | TPS que cambia en el tiempo |
| `externally-controlled` | Manual | Control externo via API |

### Ejemplo de cada executor

```javascript
// ramping-vus: Para load/stress tests
export const options = {
  stages: [
    { duration: '5m', target: 100 },   // Ramp up
    { duration: '30m', target: 100 },   // Steady
    { duration: '5m', target: 0 },      // Ramp down
  ],
};

// constant-arrival-rate: Para throughput target
export const options = {
  scenarios: {
    constant_load: {
      executor: 'constant-arrival-rate',
      rate: 100,              // 100 iterations per timeUnit
      timeUnit: '1s',         // = 100 RPS
      duration: '30m',
      preAllocatedVUs: 50,    // VUs pre-allocated
      maxVUs: 200,            // Max VUs if needed
    },
  },
};

// ramping-arrival-rate: Para spike tests
export const options = {
  scenarios: {
    spike: {
      executor: 'ramping-arrival-rate',
      startRate: 10,
      timeUnit: '1s',
      stages: [
        { duration: '2m', target: 10 },    // Normal
        { duration: '10s', target: 500 },   // Spike!
        { duration: '3m', target: 500 },    // Hold spike
        { duration: '10s', target: 10 },    // Recover
        { duration: '2m', target: 10 },     // Verify recovery
      ],
      preAllocatedVUs: 100,
      maxVUs: 600,
    },
  },
};
```

---

## Scripting Avanzado

### HTTP Requests

```javascript
import http from 'k6/http';

// GET with headers
const res = http.get('https://api.example.com/data', {
  headers: {
    'Authorization': 'Bearer ' + token,
    'Accept': 'application/json',
  },
  tags: { name: 'GetData' },  // Para agrupar en métricas
  timeout: '30s',
});

// POST with JSON body
const payload = JSON.stringify({
  username: 'user@example.com',
  password: 'password123',
});

const res = http.post('https://api.example.com/login', payload, {
  headers: { 'Content-Type': 'application/json' },
  tags: { name: 'Login' },
});

// Batch requests (parallel)
const responses = http.batch([
  ['GET', 'https://api.example.com/users', null, { tags: { name: 'GetUsers' } }],
  ['GET', 'https://api.example.com/products', null, { tags: { name: 'GetProducts' } }],
  ['GET', 'https://api.example.com/config', null, { tags: { name: 'GetConfig' } }],
]);
```

### Checks (Assertions)

```javascript
import { check } from 'k6';

const res = http.get('https://api.example.com/products');

// Multiple checks
const success = check(res, {
  'status is 200': (r) => r.status === 200,
  'response time < 500ms': (r) => r.timings.duration < 500,
  'body is not empty': (r) => r.body.length > 0,
  'contains products array': (r) => {
    const body = r.json();
    return Array.isArray(body.products) && body.products.length > 0;
  },
  'content-type is JSON': (r) => 
    r.headers['Content-Type'].includes('application/json'),
});

// Use check result for flow control
if (!success) {
  console.error(`Failed checks for ${res.url}: status=${res.status}`);
}
```

### Groups (Transaction markers)

```javascript
import { group } from 'k6';

export default function() {
  group('User Login Flow', () => {
    // All requests here are grouped as "User Login Flow"
    const loginPage = http.get('/login');
    sleep(2);
    const loginSubmit = http.post('/login', { user: 'test', pass: 'test' });
  });
  
  group('Browse Products', () => {
    const catalog = http.get('/products');
    sleep(3);
    const product = http.get('/products/123');
  });
  
  group('Checkout', () => {
    const cart = http.post('/cart/add', { product_id: '123' });
    sleep(2);
    const checkout = http.post('/checkout', { payment: 'card' });
  });
}
```

### Thresholds (SLA validation)

```javascript
export const options = {
  thresholds: {
    // Global thresholds
    http_req_duration: ['p(95)<2000'],      // 95% of requests < 2s
    http_req_failed: ['rate<0.01'],          // Error rate < 1%
    
    // Per-endpoint thresholds
    'http_req_duration{name:Login}': ['p(95)<1500'],
    'http_req_duration{name:Search}': ['p(95)<3000'],
    'http_req_duration{name:Checkout}': ['p(95)<5000'],
    
    // Custom metrics thresholds
    'purchase_success_rate': ['rate>0.95'],   // 95% success
    'checkout_duration': ['p(95)<10000'],     // Checkout < 10s
    
    // Group duration
    'group_duration{group:::User Login Flow}': ['p(95)<3000'],
  },
};
```

### Custom Metrics

```javascript
import { Counter, Gauge, Rate, Trend } from 'k6/metrics';

// Counter: Cumulative value
const orderCount = new Counter('orders_created');
orderCount.add(1);

// Rate: Percentage (true/false)
const loginSuccess = new Rate('login_success_rate');
loginSuccess.add(true);   // success
loginSuccess.add(false);  // failure

// Trend: Distribution (for percentiles)
const waitingTime = new Trend('waiting_time');
waitingTime.add(res.timings.waiting);

// Gauge: Current value (last value wins)
const activeConnections = new Gauge('active_connections');
activeConnections.add(42);
```

### Data Parameterization

```javascript
import { SharedArray } from 'k6/data';
import papaparse from 'https://jslib.k6.io/papaparse/5.1.1/index.js';

// Load CSV data (shared between VUs - memory efficient)
const users = new SharedArray('users', function() {
  return papaparse.parse(open('./data/users.csv'), { header: true }).data;
});

// Load JSON data
const products = new SharedArray('products', function() {
  return JSON.parse(open('./data/products.json'));
});

export default function() {
  // Each VU gets different data
  const user = users[__VU % users.length];
  const product = products[Math.floor(Math.random() * products.length)];
  
  // Use in requests
  const res = http.post('/login', JSON.stringify({
    username: user.email,
    password: user.password,
  }), { headers: { 'Content-Type': 'application/json' } });
}
```

### Correlation (Dynamic values)

```javascript
export default function() {
  // Step 1: Get CSRF token
  const loginPage = http.get('/login');
  const csrfToken = loginPage.html().find('input[name=_token]').attr('value');
  
  // Step 2: Login with token
  const loginRes = http.post('/login', {
    username: 'user@test.com',
    password: 'password',
    _token: csrfToken,  // Correlated value
  });
  
  // Step 3: Extract session/auth token from response
  const authToken = loginRes.json('data.token');
  
  // Step 4: Use auth token in subsequent requests
  const headers = { 'Authorization': `Bearer ${authToken}` };
  const profile = http.get('/api/profile', { headers });
}
```

---

## Scenarios Múltiples

```javascript
export const options = {
  scenarios: {
    // Scenario 1: Browsing (constant load)
    browsing: {
      executor: 'constant-vus',
      vus: 450,
      duration: '2h30m',
      exec: 'browseScenario',
      startTime: '0s',
    },
    
    // Scenario 2: Searching (ramping)
    searching: {
      executor: 'ramping-vus',
      stages: [
        { duration: '30m', target: 250 },
        { duration: '2h', target: 250 },
        { duration: '10m', target: 0 },
      ],
      exec: 'searchScenario',
      startTime: '0s',
    },
    
    // Scenario 3: Purchasing (arrival rate)
    purchasing: {
      executor: 'constant-arrival-rate',
      rate: 30,
      timeUnit: '1s',
      duration: '2h',
      preAllocatedVUs: 50,
      maxVUs: 200,
      exec: 'purchaseScenario',
      startTime: '30m',  // Start after ramp-up
    },
  },
};

// Each scenario maps to an exported function
export function browseScenario() { /* ... */ }
export function searchScenario() { /* ... */ }
export function purchaseScenario() { /* ... */ }
```

---

## Output y Reporting

### Output options

```bash
# Console output (default)
k6 run script.js

# JSON output
k6 run --out json=results.json script.js

# CSV output
k6 run --out csv=results.csv script.js

# InfluxDB (for Grafana dashboards)
k6 run --out influxdb=http://localhost:8086/k6 script.js

# Prometheus Remote Write
k6 run --out experimental-prometheus-rw script.js

# Multiple outputs
k6 run --out json=results.json --out influxdb=http://localhost:8086/k6 script.js

# k6 Cloud
k6 cloud run script.js
```

### CLI useful flags

```bash
# Basic execution
k6 run script.js

# Override VUs and duration
k6 run --vus 100 --duration 5m script.js

# Set environment variables
k6 run -e BASE_URL=https://staging.api.com -e API_KEY=xxx script.js

# Tags for filtering results
k6 run --tag testid=sprint42-load-1 script.js

# Summary export
k6 run --summary-export=summary.json script.js

# Quiet mode (less console output)
k6 run --quiet script.js

# Show only specific summary metrics
k6 run --summary-trend-stats="avg,min,med,max,p(90),p(95),p(99)" script.js
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Performance Tests
on:
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  performance-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install k6
        run: |
          curl https://github.com/grafana/k6/releases/download/v0.47.0/k6-v0.47.0-linux-amd64.tar.gz -L | tar xvz
          sudo mv k6-v0.47.0-linux-amd64/k6 /usr/local/bin/
          
      - name: Run smoke test
        run: k6 run --vus 5 --duration 30s tests/smoke.js
        
      - name: Run load test
        run: k6 run tests/load-test.js
        env:
          BASE_URL: ${{ secrets.STAGING_URL }}
          
      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: k6-results
          path: results/
```

---

## Extensiones (xk6)

### Extensiones populares

| Extensión | Uso |
|-----------|-----|
| xk6-browser | Real browser testing (Chromium) |
| xk6-sql | Database load testing |
| xk6-kafka | Kafka producer/consumer testing |
| xk6-output-prometheus-remote | Prometheus metrics output |
| xk6-dashboard | Real-time HTML dashboard |
| xk6-faker | Fake data generation |

### Browser testing (k6 browser)

```javascript
import { browser } from 'k6/browser';
import { check } from 'k6';

export const options = {
  scenarios: {
    browser: {
      executor: 'constant-vus',
      vus: 10,
      duration: '5m',
      options: { browser: { type: 'chromium' } },
    },
  },
};

export default async function() {
  const page = await browser.newPage();
  
  try {
    await page.goto('https://example.com/login');
    await page.locator('input[name="username"]').type('user@test.com');
    await page.locator('input[name="password"]').type('password');
    await page.locator('button[type="submit"]').click();
    
    const welcome = await page.locator('h1').textContent();
    check(welcome, {
      'logged in successfully': (text) => text.includes('Welcome'),
    });
  } finally {
    await page.close();
  }
}
```

---

*Documento de referencia - Performance Test Life Cycle*
*Última actualización: Junio 2026*
