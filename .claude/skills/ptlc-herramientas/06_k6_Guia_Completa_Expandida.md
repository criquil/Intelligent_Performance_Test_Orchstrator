# ⚡ k6 (Grafana) - Guía Completa de Referencia

## Mapa de secciones

Tabla generada con `grep -n "^## "`. Para leer solo una sección concreta usa `read` con ese offset (o `grep` sobre el título) en lugar de cargar el archivo entero.

| Línea | Sección |
|--------|---------|
| 3 | Mapa de secciones |
| 33 | 1. Introducción y Filosofía |
| 102 | 2. Arquitectura Interna (Go Engine) |
| 179 | 3. Instalación y Configuración |
| 227 | 4. Lifecycle de un Script k6 |
| 392 | 5. Executors en Profundidad |
| 575 | 6. Scenarios (Multi-Scenario Testing) |
| 708 | 7. HTTP API Completa |
| 863 | 8. Checks y Validaciones |
| 931 | 9. Thresholds (Criterios Pass/Fail) |
| 1047 | 10. Métricas Built-in y Custom |
| 1163 | 11. Datos de Prueba y Parametrización |
| 1275 | 12. Grupos y Tags |
| 1430 | 13. Módulos y Organización de Código |
| 1548 | 14. Protocolos Adicionales (gRPC, WebSocket, Browser) |
| 1718 | 15. Environment Variables y Options |
| 1799 | 16. Extensions (xk6) |
| 1868 | 17. Output y Exportación de Resultados |
| 1982 | 19. Integración con Grafana Cloud |
| 2026 | 20. Patrones Avanzados |
| 2173 | 21. Testing de Performance en Microservicios |
| 2254 | Referencias |
---

## 1. Introducción y Filosofía

### ¿Qué es k6?

**k6** es una herramienta moderna de load testing open-source desarrollada por **Grafana Labs**. Está escrita en **Go** con un runtime de JavaScript (goja), lo que le da rendimiento excepcional con scripting familiar.

### Ventajas clave

- **JavaScript (ES6)**: lenguaje familiar para la mayoría de developers
- **Go engine**: eficiente en uso de recursos (no usa threads por VU)
- **CLI-first**: ideal para CI/CD y automatización
- **Extensible**: xk6 modules para funcionalidad adicional
- **Grafana integration**: visualización nativa de resultados
- **Open source**: AGPL-3.0 license

### Filosofía de diseño

| Principio | Implementación |
|-----------|---------------|
| **Developer-first** | JavaScript ES6, CLI-native, code-as-config |
| **Goal-oriented** | Thresholds como SLOs, pass/fail automático |
| **High performance** | Go engine, no usa 1 thread por VU |
| **Extensible** | xk6 para Go extensions, JS modules |
| **Cloud-native** | Grafana Cloud k6, Prometheus, InfluxDB |
| **Scriptable** | ES6 modules, imports, SharedArray |

### k6 en el ecosistema Grafana

```
┌─────────────────────────────────────────────────────────────────┐
│                    GRAFANA OBSERVABILITY STACK                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────┐  ┌──────────┐  ┌─────────┐  ┌───────────────┐    │
│  │   k6    │  │ Grafana  │  │  Loki   │  │  Prometheus   │    │
│  │ (Load)  │─►│(Dashbrd) │◄─│ (Logs)  │  │  (Metrics)    │    │
│  └─────────┘  └──────────┘  └─────────┘  └───────────────┘    │
│       │                                          ▲               │
│       │         ┌──────────┐                     │               │
│       └────────►│  Tempo   │─────────────────────┘               │
│                 │ (Traces) │                                      │
│                 └──────────┘                                      │
│                                                                   │
│  k6 genera métricas → Prometheus/Grafana Cloud                   │
│  k6 correlaciona con traces → Tempo                              │
│  k6 dashboards preconfigurados en Grafana                        │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Rendimiento comparativo

```
Throughput por instancia (8 cores, 16 GB RAM):

k6:      50,000 - 300,000 requests/second ⭐
Gatling: 20,000 - 100,000 requests/second
Locust:   5,000 -  15,000 requests/second
JMeter:   2,000 -  10,000 requests/second

Memory per VU:
k6:      ~1-3 KB per VU
Gatling: ~5-10 KB per VU (actor)
Locust:  ~4-8 KB per VU (greenlet)
JMeter:  ~500 KB - 1 MB per VU (thread)
```

---

## 2. Arquitectura Interna (Go Engine)

### Stack tecnológico

```
┌─────────────────────────────────────────────────────────────────┐
│                    k6 ARCHITECTURE                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │              JAVASCRIPT RUNTIME (goja)                    │     │
│  │  • ES6+ syntax (no Node.js, no V8)                      │     │
│  │  • Import/export modules                                 │     │
│  │  • No async/await nativo (todo es sync por diseño)       │     │
│  └────────────────────────────┬────────────────────────────┘     │
│                               │                                   │
│  ┌────────────────────────────▼────────────────────────────┐     │
│  │              EXECUTION ENGINE (Go)                        │     │
│  │                                                          │     │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │     │
│  │  │  Executor    │  │  VU Scheduler│  │  Metrics     │  │     │
│  │  │  Controller  │  │  (goroutines)│  │  Aggregator  │  │     │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │     │
│  │                                                          │     │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │     │
│  │  │  HTTP/2      │  │  gRPC        │  │  WebSocket   │  │     │
│  │  │  Client      │  │  Client      │  │  Client      │  │     │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │     │
│  │                                                          │     │
│  └──────────────────────────────────────────────────────────┘     │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │              OUTPUT PLUGINS                                │    │
│  │  stdout │ JSON │ CSV │ InfluxDB │ Prometheus │ Cloud      │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Vista de componentes

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

### Modelo de ejecución

```
IMPORTANTE: k6 NO es Node.js

┌─────────────────────────────────────────────────────────┐
│                                                          │
│  • Cada VU = 1 goroutine ejecutando el script JS        │
│  • Las llamadas HTTP son SÍNCRONAS (blocking por VU)    │
│  • Pero las goroutines se multiplexan en pocos threads  │
│  • NO hay event loop, NO hay callbacks, NO hay promises │
│  • El código se lee de arriba a abajo (simple)          │
│                                                          │
│  Beneficio: código simple + alto rendimiento            │
│  Limitación: no puedes hacer requests en paralelo       │
│              dentro de un solo VU (usa http.batch)       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Instalación y Configuración

### Instalación multiplataforma

```bash
# ─── Windows ───
choco install k6
# o con winget:
winget install k6
winget install grafana.k6

# ─── macOS ───
brew install k6

# ─── Linux (Debian/Ubuntu) ───
sudo gpg -k
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg \
  --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" \
  | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update && sudo apt-get install k6

# ─── Docker ───
docker run --rm -i grafana/k6 run - <script.js
docker run --rm -v $(pwd):/scripts grafana/k6 run /scripts/test.js

# ─── Verificar instalación ───
k6 version
```

### Primer test

```bash
# Ejecutar test básico
k6 run script.js

# Con parámetros CLI
k6 run --vus 10 --duration 30s script.js

# Con output JSON
k6 run --out json=results.json script.js

# Con múltiples outputs
k6 run --out json=results.json --out influxdb=http://localhost:8086/k6 script.js
```

---

## 4. Lifecycle de un Script k6

### Virtual Users (VUs) e Iteraciones

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

### Fases de ejecución

```javascript
// ═══════════════════════════════════════════════════════════════
// INIT CODE (ejecuta UNA vez al inicio, fuera de funciones)
// ═══════════════════════════════════════════════════════════════
// - Cargar archivos, definir opciones, importar módulos
// - NO puede hacer HTTP requests
// - Se ejecuta UNA vez por VU (para inicializar)

import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { SharedArray } from 'k6/data';
import { htmlReport } from "https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js";

// Datos compartidos (cargados UNA vez, compartidos entre VUs - read only)
const users = new SharedArray('users', function () {
  return JSON.parse(open('./data/users.json'));
});

export const options = {
  stages: [
    { duration: '2m', target: 50 },
    { duration: '5m', target: 50 },
    { duration: '1m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

// ═══════════════════════════════════════════════════════════════
// SETUP (ejecuta UNA vez antes de todos los VUs)
// ═══════════════════════════════════════════════════════════════
// - Puede hacer HTTP requests
// - Retorna data que se pasa a default() y teardown()
// - Ideal para: obtener tokens, crear test data, health check

export function setup() {
  const loginRes = http.post('https://api.example.com/auth/login', JSON.stringify({
    email: 'admin@test.com',
    password: 'admin123',
  }), { headers: { 'Content-Type': 'application/json' } });
  
  const token = loginRes.json('access_token');
  
  // Health check
  const healthRes = http.get('https://api.example.com/health');
  if (healthRes.status !== 200) {
    throw new Error('System not healthy, aborting test');
  }
  
  return { token: token, startTime: Date.now() };
}

// ═══════════════════════════════════════════════════════════════
// DEFAULT FUNCTION (ejecuta en CADA iteración de CADA VU)
// ═══════════════════════════════════════════════════════════════
// - Esta es la función principal del test
// - Recibe data de setup() como argumento
// - Se ejecuta en loop según el executor configurado

export default function (data) {
  const params = {
    headers: {
      'Authorization': `Bearer ${data.token}`,
      'Content-Type': 'application/json',
    },
  };
  
  // Seleccionar usuario para este VU
  const user = users[__VU % users.length];
  
  group('Browse Products', function () {
    const res = http.get('https://api.example.com/api/products', params);
    check(res, {
      'status is 200': (r) => r.status === 200,
      'response time < 500ms': (r) => r.timings.duration < 500,
      'has products': (r) => r.json('items').length > 0,
    });
  });
  
  sleep(Math.random() * 3 + 1); // Think time: 1-4 seconds
}

// ═══════════════════════════════════════════════════════════════
// TEARDOWN (ejecuta UNA vez después de todos los VUs)
// ═══════════════════════════════════════════════════════════════
// - Cleanup, reportes finales, notificaciones
// - Recibe data de setup()

export function teardown(data) {
  const duration = (Date.now() - data.startTime) / 1000;
  console.log(`Test completed in ${duration} seconds`);
  
  // Cleanup test data
  http.del('https://api.example.com/admin/test-data', null, {
    headers: { 'Authorization': `Bearer ${data.token}` },
  });
}

// ═══════════════════════════════════════════════════════════════
// HANDLERSUMMARY (ejecuta al final, genera reportes custom)
// ═══════════════════════════════════════════════════════════════

export function handleSummary(data) {
  return {
    'stdout': textSummary(data, { indent: ' ', enableColors: true }),
    'reports/summary.json': JSON.stringify(data, null, 2),
    'reports/report.html': htmlReport(data),
  };
}
```

### Diagrama de lifecycle

```
┌──────────────────────────────────────────────────────────────┐
│                    k6 EXECUTION LIFECYCLE                      │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  1. INIT (per VU)                                            │
│     └─ Imports, SharedArray, options                          │
│                                                               │
│  2. SETUP (once)                                             │
│     └─ Health checks, auth, prepare data                     │
│     └─ Returns: setupData                                    │
│                                                               │
│  3. VU CODE (per VU, per iteration)    ←─── LOOP ───┐       │
│     └─ default(setupData)                            │       │
│     └─ HTTP requests, checks, sleep                  │       │
│     └─ Repeat according to executor ────────────────┘       │
│                                                               │
│  4. TEARDOWN (once)                                          │
│     └─ teardown(setupData)                                   │
│     └─ Cleanup, notifications                                │
│                                                               │
│  5. HANDLE SUMMARY (once)                                    │
│     └─ handleSummary(metrics)                                │
│     └─ Generate reports                                      │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## 5. Executors en Profundidad

### Los 6 executors de k6

```javascript
export const options = {
  scenarios: {
    
    // ═══ 1. shared-iterations ═══
    // Total de N iteraciones compartidas entre M VUs
    // El test termina cuando se completan TODAS las iteraciones
    // Útil: "ejecutar exactamente 1000 requests lo más rápido posible"
    shared_load: {
      executor: 'shared-iterations',
      vus: 50,
      iterations: 1000,
      maxDuration: '5m',
    },
    
    // ═══ 2. per-vu-iterations ═══
    // Cada VU ejecuta exactamente N iteraciones
    // Útil: "cada usuario hace exactamente 10 compras"
    per_vu_load: {
      executor: 'per-vu-iterations',
      vus: 20,
      iterations: 10,      // 20 VUs × 10 iterations = 200 total
      maxDuration: '5m',
    },
    
    // ═══ 3. constant-vus ═══
    // N VUs ejecutando continuamente durante un tiempo
    // Útil: "mantener 50 usuarios concurrentes por 10 minutos"
    constant_load: {
      executor: 'constant-vus',
      vus: 50,
      duration: '10m',
    },
    
    // ═══ 4. ramping-vus ═══
    // VUs que suben y bajan en stages
    // Útil: "ramp-up → hold → ramp-down clásico"
    ramping_load: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 50 },   // Ramp to 50
        { duration: '5m', target: 50 },   // Hold at 50
        { duration: '2m', target: 100 },  // Ramp to 100
        { duration: '5m', target: 100 },  // Hold at 100
        { duration: '2m', target: 0 },    // Ramp down
      ],
      gracefulRampDown: '30s',
    },
    
    // ═══ 5. constant-arrival-rate ═══ (OPEN MODEL)
    // Tasa fija de ITERACIONES por segundo (independiente de VUs)
    // Si un VU está ocupado, k6 asigna otro
    // Útil: "enviar exactamente 100 requests/segundo"
    constant_rate: {
      executor: 'constant-arrival-rate',
      rate: 100,              // 100 iteraciones por timeUnit
      timeUnit: '1s',         // = 100 RPS
      duration: '10m',
      preAllocatedVUs: 50,    // VUs iniciales
      maxVUs: 200,            // Máximo de VUs si necesita más
    },
    
    // ═══ 6. ramping-arrival-rate ═══ (OPEN MODEL + ramp)
    // Tasa variable de iteraciones/segundo
    // Útil: "rampear de 10 a 100 RPS en 5 minutos"
    ramping_rate: {
      executor: 'ramping-arrival-rate',
      startRate: 10,
      timeUnit: '1s',
      stages: [
        { duration: '2m', target: 50 },   // Ramp to 50 RPS
        { duration: '5m', target: 50 },   // Hold 50 RPS
        { duration: '2m', target: 100 },  // Ramp to 100 RPS
        { duration: '5m', target: 100 },  // Hold 100 RPS
        { duration: '1m', target: 0 },    // Ramp down
      ],
      preAllocatedVUs: 50,
      maxVUs: 300,
    },
  },
};
```

### ¿Cuándo usar cada executor?

```
┌──────────────────────────────────────────────────────────────────┐
│ EXECUTOR              │ MODELO │ CASO DE USO                      │
├───────────────────────┼────────┼──────────────────────────────────┤
│ shared-iterations     │ Closed │ Smoke test: "ejecutar 100 req"   │
│ per-vu-iterations     │ Closed │ "Cada user hace 5 transacciones" │
│ constant-vus          │ Closed │ Baseline: "50 users por 10 min"  │
│ ramping-vus           │ Closed │ Load test clásico con ramp       │
│ constant-arrival-rate │ Open   │ "Enviar 200 RPS exactos"         │
│ ramping-arrival-rate  │ Open   │ Stress: "rampear hasta 500 RPS"  │
└───────────────────────┴────────┴──────────────────────────────────┘

REGLA:
- closed model (VUs) → controlas CONCURRENCIA
- open model (arrival-rate) → controlas THROUGHPUT
```

### Resumen de executors

| Executor | Uso | Descripción |
|----------|-----|-------------|
| `shared-iterations` | Smoke test | N iteraciones divididas entre VUs |
| `per-vu-iterations` | Fixed work | Cada VU hace N iteraciones |
| `constant-vus` | Steady state | N VUs constantes por duración |
| `ramping-vus` | Load/Stress | VUs que suben/bajan según stages |
| `constant-arrival-rate` | Throughput target | Mantener TPS constante |
| `ramping-arrival-rate` | Variable throughput | TPS que cambia en el tiempo |
| `externally-controlled` | Manual | Control externo via API |

### Shortcuts de options (sin scenarios)

```javascript
// ramping-vus: Para load/stress tests
export const options = {
  stages: [
    { duration: '5m', target: 100 },   // Ramp up
    { duration: '30m', target: 100 },  // Steady
    { duration: '5m', target: 0 },     // Ramp down
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
        { duration: '10s', target: 500 },  // Spike!
        { duration: '3m', target: 500 },   // Hold spike
        { duration: '10s', target: 10 },   // Recover
        { duration: '2m', target: 10 },    // Verify recovery
      ],
      preAllocatedVUs: 100,
      maxVUs: 600,
    },
  },
};
```

### externally-controlled (control manual vía API)

```javascript
// Las configuraciones se empujan desde fuera durante la ejecución
export const options = {
  scenarios: {
    manual: {
      executor: 'externally-controlled',
      vus: 10,
      duration: '10m',
    },
  },
};
```

---

## 6. Scenarios (Multi-Scenario Testing)

### Múltiples scenarios simultáneos

Ejemplo de tres perfiles de tráfico coexistiendo, cada uno arrancando en un momento distinto (`startTime` escalonado):

```javascript
export const options = {
  scenarios: {
    // Scenario 1: Usuarios que navegan (70% del tráfico)
    browsers: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 70 },
        { duration: '10m', target: 70 },
        { duration: '1m', target: 0 },
      ],
      exec: 'browseProducts',  // ← función a ejecutar
      tags: { scenario: 'browse' },
    },
    
    // Scenario 2: Usuarios que buscan (20%)
    searchers: {
      executor: 'constant-arrival-rate',
      rate: 20,
      timeUnit: '1s',
      duration: '12m',
      preAllocatedVUs: 10,
      maxVUs: 50,
      exec: 'searchProducts',  // ← otra función
      startTime: '30s',        // Empieza 30s después
      tags: { scenario: 'search' },
    },
    
    // Scenario 3: Compradores (10%)
    buyers: {
      executor: 'per-vu-iterations',
      vus: 10,
      iterations: 5,
      exec: 'purchaseFlow',    // ← otra función
      startTime: '2m',         // Empieza a los 2 minutos
      tags: { scenario: 'purchase' },
    },
  },
  
  thresholds: {
    // Thresholds globales
    http_req_duration: ['p(95)<2000'],
    
    // Thresholds por scenario (usando tags)
    'http_req_duration{scenario:browse}': ['p(95)<1000'],
    'http_req_duration{scenario:search}': ['p(95)<1500'],
    'http_req_duration{scenario:purchase}': ['p(95)<3000'],
  },
};

// Funciones exportadas para cada scenario
export function browseProducts() {
  http.get('https://api.example.com/products');
  sleep(Math.random() * 5 + 2);
}

export function searchProducts() {
  const terms = ['laptop', 'phone', 'headphones', 'camera'];
  const term = terms[Math.floor(Math.random() * terms.length)];
  http.get(`https://api.example.com/search?q=${term}`);
  sleep(Math.random() * 3 + 1);
}

export function purchaseFlow() {
  // Flujo completo de compra
  const cartRes = http.post('https://api.example.com/cart/add', 
    JSON.stringify({ product_id: Math.floor(Math.random() * 100) + 1 }),
    { headers: { 'Content-Type': 'application/json' } }
  );
  sleep(2);
  
  if (cartRes.status === 201) {
    http.post('https://api.example.com/checkout');
  }
  sleep(3);
}
```

Variante con carga larga por escenario (ramp de 30m, purchasers con `arrival-rate` arrancando tras el ramp):

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

## 7. HTTP API Completa

### Todos los métodos HTTP

```javascript
import http from 'k6/http';

export default function () {
  const baseUrl = 'https://api.example.com';
  const params = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer token123',
    },
    timeout: '30s',
    tags: { endpoint: 'users' },
  };
  
  // GET
  const getRes = http.get(`${baseUrl}/api/users`, params);
  
  // POST
  const postRes = http.post(`${baseUrl}/api/users`,
    JSON.stringify({ name: 'Test', email: 'test@test.com' }),
    params
  );
  
  // PUT
  const putRes = http.put(`${baseUrl}/api/users/1`,
    JSON.stringify({ name: 'Updated' }),
    params
  );
  
  // PATCH
  const patchRes = http.patch(`${baseUrl}/api/users/1`,
    JSON.stringify({ status: 'active' }),
    params
  );
  
  // DELETE
  const delRes = http.del(`${baseUrl}/api/users/1`, null, params);
  
  // OPTIONS
  const optRes = http.options(`${baseUrl}/api/users`);
  
  // HEAD
  const headRes = http.head(`${baseUrl}/api/users`);
}
```

### Batch requests (paralelo)

```javascript
import http from 'k6/http';

export default function () {
  // Ejecutar múltiples requests EN PARALELO
  const responses = http.batch([
    ['GET', 'https://api.example.com/api/products', null, { tags: { type: 'products' } }],
    ['GET', 'https://api.example.com/api/categories', null, { tags: { type: 'categories' } }],
    ['GET', 'https://api.example.com/api/promotions', null, { tags: { type: 'promotions' } }],
  ]);
  
  // O con objeto (más legible):
  const namedResponses = http.batch({
    products: { method: 'GET', url: 'https://api.example.com/api/products' },
    categories: { method: 'GET', url: 'https://api.example.com/api/categories' },
    user: { method: 'GET', url: 'https://api.example.com/api/user/profile',
            params: { headers: { 'Authorization': 'Bearer token' } } },
  });
  
  // Acceder a respuestas individuales
  console.log(namedResponses.products.status);
  console.log(namedResponses.categories.json('items').length);
}
```

### Response object completo

```javascript
import http from 'k6/http';
import { check } from 'k6';

export default function () {
  const res = http.get('https://api.example.com/api/data');
  
  // ─── Propiedades del response ───
  res.status;              // HTTP status code (number)
  res.status_text;         // "OK", "Not Found", etc.
  res.body;                // Response body (string)
  res.headers;             // Response headers (object)
  res.cookies;             // Response cookies
  res.error;               // Error message (if any)
  res.error_code;          // k6 error code (if any)
  res.url;                 // Final URL (after redirects)
  res.proto;               // Protocol ("HTTP/2.0", "HTTP/1.1")
  
  // ─── Timings (milisegundos) ───
  res.timings.duration;    // Total request time
  res.timings.blocked;     // Time waiting for free TCP connection
  res.timings.connecting;  // TCP connection time
  res.timings.tls_handshaking; // TLS handshake time
  res.timings.sending;     // Time sending request
  res.timings.waiting;     // TTFB (Time to First Byte)
  res.timings.receiving;   // Time receiving response
  
  // ─── Métodos del response ───
  res.json();              // Parse body como JSON
  res.json('path.to.key');  // JSONPath extraction
  res.html();              // Parse como HTML (Selection API)
  res.submitForm();        // Submit form encontrado en HTML
  
  // ─── HTML Selection (para páginas web) ───
  const doc = res.html();
  const title = doc.find('h1').text();
  const links = doc.find('a[href]').toArray();
  const csrfToken = doc.find('input[name="csrf_token"]').attr('value');
  
  // ─── JSON path extraction ───
  const userId = res.json('data.user.id');
  const items = res.json('data.items');
  const firstItemName = res.json('data.items.0.name');
}
```

### File upload

```javascript
import http from 'k6/http';
import { FormData } from 'https://jslib.k6.io/formdata/0.0.2/index.js';

// Método 1: open() para archivos binarios
const binFile = open('./data/test_image.png', 'b'); // binary

export default function () {
  // Upload con http.file()
  const res = http.post('https://api.example.com/upload', {
    file: http.file(binFile, 'test_image.png', 'image/png'),
    description: 'Load test upload',
  });
  
  // Upload con FormData (múltiples archivos)
  const fd = new FormData();
  fd.append('file1', http.file(binFile, 'image1.png', 'image/png'));
  fd.append('file2', http.file(binFile, 'image2.png', 'image/png'));
  fd.append('metadata', JSON.stringify({ album: 'test' }));
  
  const res2 = http.post('https://api.example.com/gallery/upload', fd.body(), {
    headers: { 'Content-Type': `multipart/form-data; boundary=${fd.boundary}` },
  });
}
```

---

## 8. Checks y Validaciones

### Check API completa

```javascript
import http from 'k6/http';
import { check } from 'k6';

export default function () {
  const res = http.get('https://api.example.com/api/users');
  
  // Checks básicos
  const success = check(res, {
    'status is 200': (r) => r.status === 200,
    'status is not 500': (r) => r.status !== 500,
    'response time < 500ms': (r) => r.timings.duration < 500,
    'body is not empty': (r) => r.body.length > 0,
    'content-type is JSON': (r) => r.headers['Content-Type'].includes('application/json'),
  });
  
  // Checks de contenido JSON
  check(res, {
    'has items array': (r) => Array.isArray(r.json('items')),
    'items count > 0': (r) => r.json('items').length > 0,
    'first item has id': (r) => r.json('items.0.id') !== undefined,
    'total count matches': (r) => r.json('meta.total') >= r.json('items').length,
  });
  
  // Checks con tags (para thresholds granulares)
  check(res, {
    'login success': (r) => r.status === 200,
  }, { endpoint: 'login', critical: 'true' });
  
  // Check retorna boolean - puedes usarlo para lógica
  if (!success) {
    console.warn(`Request failed: ${res.status} - ${res.body.substring(0, 200)}`);
  }
}
```

Checks de negocio (múltiples, con control de flujo a partir del resultado):

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

---

## 9. Thresholds (Criterios Pass/Fail)

### Todos los tipos de thresholds

```javascript
export const options = {
  thresholds: {
    // ─── HTTP Request Duration ───
    http_req_duration: [
      'p(50)<200',     // Mediana < 200ms
      'p(90)<500',     // P90 < 500ms
      'p(95)<1000',    // P95 < 1s
      'p(99)<2000',    // P99 < 2s
      'max<5000',      // Máximo < 5s
      'avg<300',       // Promedio < 300ms
      'med<200',       // Mediana < 200ms
      'min<50',        // Mínimo > 50ms (sanity check)
    ],
    
    // ─── HTTP Request Failed ───
    http_req_failed: [
      'rate<0.01',     // < 1% error rate
    ],
    
    // ─── HTTP Requests (throughput) ───
    http_reqs: [
      'rate>100',      // > 100 RPS
      'count>10000',   // Al menos 10000 requests total
    ],
    
    // ─── Checks ───
    checks: [
      'rate>0.99',     // > 99% de checks pasaron
    ],
    
    // ─── Custom metrics ───
    'my_custom_trend': ['p(95)<1000'],
    'my_custom_rate': ['rate>0.95'],
    'my_custom_counter': ['count>100'],
    
    // ─── Por tag (granular) ───
    'http_req_duration{endpoint:login}': ['p(95)<500'],
    'http_req_duration{endpoint:checkout}': ['p(95)<2000'],
    'http_req_duration{scenario:browse}': ['p(95)<800'],
    'http_req_failed{critical:true}': ['rate<0.001'],  // 0.1% para críticos
    
    // ─── Por nombre de request (tag name) ───
    'http_req_duration{name:Login}': ['p(95)<1500'],
    'http_req_duration{name:Search}': ['p(95)<3000'],
    'http_req_duration{name:Checkout}': ['p(95)<5000'],
    
    // ─── Thresholds de custom metrics de negocio ───
    'purchase_success_rate': ['rate>0.95'],   // 95% success
    'checkout_duration': ['p(95)<10000'],     // Checkout < 10s
    'group_duration{group:::User Login Flow}': ['p(95)<3000'],
    
    // ─── Abort on threshold breach ───
    http_req_duration: [
      { threshold: 'p(95)<2000', abortOnFail: true, delayAbortEval: '30s' },
    ],
    // Si P95 > 2s por más de 30s → ABORTAR el test
  },
};
```

### Thresholds como SLOs

```javascript
// Umbrales por endpoint (usando el tag `name`) y por métrica de negocio
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

```javascript
// Mapear SLOs de producción a thresholds de k6
export const options = {
  thresholds: {
    // SLO: 99.9% de requests exitosos
    http_req_failed: ['rate<0.001'],
    
    // SLO: P95 < 500ms para lectura, P95 < 2s para escritura
    'http_req_duration{type:read}': ['p(95)<500'],
    'http_req_duration{type:write}': ['p(95)<2000'],
    
    // SLO: Homepage carga en < 1s P99
    'http_req_duration{page:home}': ['p(99)<1000'],
    
    // SLO: Checkout completo < 5s P95
    'group_duration{group:::Checkout Flow}': ['p(95)<5000'],
    
    // Apdex target: 0.9 (satisfied < 500ms, tolerating < 1500ms)
    // Implementar con custom metric
    'apdex_score': ['value>0.9'],
  },
};
```

---

## 10. Métricas Built-in y Custom

### Métricas built-in de HTTP

```
┌──────────────────────────────────────────────────────────────────┐
│ MÉTRICA                     │ TIPO    │ DESCRIPCIÓN              │
├─────────────────────────────┼─────────┼──────────────────────────┤
│ http_reqs                   │ Counter │ Total de HTTP requests   │
│ http_req_duration           │ Trend   │ Tiempo total del request │
│ http_req_blocked            │ Trend   │ Tiempo esperando conexión│
│ http_req_connecting         │ Trend   │ Tiempo de TCP connect    │
│ http_req_tls_handshaking    │ Trend   │ Tiempo de TLS handshake  │
│ http_req_sending            │ Trend   │ Tiempo enviando datos    │
│ http_req_waiting            │ Trend   │ TTFB (waiting)           │
│ http_req_receiving          │ Trend   │ Tiempo recibiendo datos  │
│ http_req_failed             │ Rate    │ % de requests fallidos   │
├─────────────────────────────┼─────────┼──────────────────────────┤
│ iteration_duration          │ Trend   │ Duración de 1 iteración  │
│ iterations                  │ Counter │ Total de iteraciones     │
│ vus                         │ Gauge   │ VUs activos ahora        │
│ vus_max                     │ Gauge   │ Máximo VUs configurados  │
│ data_sent                   │ Counter │ Bytes enviados           │
│ data_received               │ Counter │ Bytes recibidos          │
│ checks                      │ Rate    │ % de checks exitosos     │
│ group_duration              │ Trend   │ Duración de un group()   │
└─────────────────────────────┴─────────┴──────────────────────────┘
```

### Custom metrics

```javascript
import http from 'k6/http';
import { Trend, Counter, Rate, Gauge } from 'k6/metrics';

// ─── Definir custom metrics ───
const loginDuration = new Trend('login_duration', true);   // true = time values
const orderCount = new Counter('orders_created');
const checkoutSuccess = new Rate('checkout_success_rate');
const activeCartSize = new Gauge('active_cart_size');

// ─── Apdex custom ───
const apdexSatisfied = new Counter('apdex_satisfied');
const apdexTolerated = new Counter('apdex_tolerated');
const apdexFrustrated = new Counter('apdex_frustrated');

export default function () {
  // Login y medir con custom trend
  const loginStart = Date.now();
  const loginRes = http.post('https://api.example.com/login', /* ... */);
  loginDuration.add(Date.now() - loginStart);
  
  // Contar órdenes creadas
  const orderRes = http.post('https://api.example.com/orders', /* ... */);
  if (orderRes.status === 201) {
    orderCount.add(1);
    checkoutSuccess.add(true);   // éxito
  } else {
    checkoutSuccess.add(false);  // falla
  }
  
  // Gauge (último valor)
  const cartRes = http.get('https://api.example.com/cart');
  if (cartRes.status === 200) {
    activeCartSize.add(cartRes.json('items').length);
  }
  
  // Semántica de cada tipo:
  //   Counter: valor acumulativo
  //   Rate:    porcentaje (true/false)
  //   Trend:   distribución (para percentiles)
  //   Gauge:   valor actual (gana el último)

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
  
  // Calcular Apdex
  const duration = loginRes.timings.duration;
  if (duration < 500) {
    apdexSatisfied.add(1);
  } else if (duration < 1500) {
    apdexTolerated.add(1);
  } else {
    apdexFrustrated.add(1);
  }
}

export const options = {
  thresholds: {
    login_duration: ['p(95)<1000'],
    checkout_success_rate: ['rate>0.98'],
    orders_created: ['count>50'],
  },
};
```

---

## 11. Datos de Prueba y Parametrización

### SharedArray (datos compartidos eficientes)

```javascript
import { SharedArray } from 'k6/data';

// SharedArray carga datos UNA vez y los comparte entre TODOS los VUs
// Sin duplicar memoria (read-only)
const users = new SharedArray('users', function () {
  return JSON.parse(open('./data/users.json'));
  // Retornar array. Cada elemento accesible por índice.
});

const products = new SharedArray('products', function () {
  return open('./data/products.csv').split('\n').slice(1).map(line => {
    const [id, name, price, category] = line.split(',');
    return { id, name, price: parseFloat(price), category };
  });
});

export default function () {
  // Acceso por VU (cada VU tiene su propio dato)
  const user = users[__VU % users.length];
  
  // Acceso aleatorio
  const product = products[Math.floor(Math.random() * products.length)];
  
  // Acceso secuencial por iteración
  const idx = (__VU - 1) * 10 + __ITER;  // VU-based offset
  const item = products[idx % products.length];
}
```

### CSV con papaparse (jslib)

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

### Archivos y templates

```javascript
// open() lee archivos en INIT phase (no durante ejecución)
const jsonData = JSON.parse(open('./data/config.json'));
const templateBody = open('./templates/order.json');
const binaryFile = open('./files/document.pdf', 'b');

export default function () {
  // Usar template con interpolación
  const body = templateBody
    .replace('{{USER_ID}}', `user_${__VU}`)
    .replace('{{TIMESTAMP}}', Date.now().toString())
    .replace('{{AMOUNT}}', (Math.random() * 100).toFixed(2));
  
  http.post('https://api.example.com/orders', body, {
    headers: { 'Content-Type': 'application/json' },
  });
}
```

### Execution context variables

```javascript
export default function () {
  // Variables de contexto de ejecución
  __VU;          // ID del VU actual (1-based)
  __ITER;        // Iteración actual del VU (0-based)
  __ENV.MY_VAR;  // Variable de entorno
  
  // Execution API (más detallada)
  import exec from 'k6/execution';
  
  exec.vu.idInTest;           // ID global del VU
  exec.vu.idInInstance;       // ID en esta instancia
  exec.vu.iterationInInstance; // Iteración del VU
  exec.vu.iterationInScenario; // Iteración en el scenario
  exec.scenario.name;         // Nombre del scenario actual
  exec.scenario.executor;     // Tipo de executor
  exec.scenario.startTime;    // Timestamp de inicio
  exec.scenario.progress;     // Progreso (0.0 - 1.0)
  exec.scenario.iterationInTest; // Iteración global
  exec.instance.vusActive;    // VUs activos ahora
  exec.instance.currentTestRunDuration; // Duración actual
}
```

---

## 12. Grupos y Tags

### Groups (agrupación lógica)

```javascript
import http from 'k6/http';
import { group, check, sleep } from 'k6';

export default function () {
  // Groups crean métricas agregadas: group_duration
  group('Homepage', function () {
    const res = http.get('https://example.com/');
    check(res, { 'homepage loaded': (r) => r.status === 200 });
    
    // Sub-groups
    group('Load Resources', function () {
      http.batch([
        ['GET', 'https://example.com/style.css'],
        ['GET', 'https://example.com/app.js'],
        ['GET', 'https://example.com/logo.png'],
      ]);
    });
  });
  
  sleep(2);
  
  group('Checkout Flow', function () {
    group('Add to Cart', function () {
      http.post('https://example.com/cart/add', JSON.stringify({item: 1}));
    });
    sleep(1);
    group('Submit Payment', function () {
      http.post('https://example.com/checkout', JSON.stringify({pay: true}));
    });
  });
}

// Threshold por grupo:
export const options = {
  thresholds: {
    'group_duration{group:::Homepage}': ['p(95)<3000'],
    'group_duration{group:::Checkout Flow}': ['p(95)<5000'],
    'group_duration{group:::Checkout Flow::Submit Payment}': ['p(95)<2000'],
  },
};
```

### Tags (etiquetas para filtrar métricas)

```javascript
import http from 'k6/http';

export default function () {
  // Tags por request
  http.get('https://api.example.com/products', {
    tags: { endpoint: 'products', type: 'read', priority: 'high' },
  });
  
  http.post('https://api.example.com/orders', JSON.stringify({}), {
    headers: { 'Content-Type': 'application/json' },
    tags: { endpoint: 'orders', type: 'write', priority: 'critical' },
  });
}

export const options = {
  thresholds: {
    // Thresholds usando tags
    'http_req_duration{type:read}': ['p(95)<500'],
    'http_req_duration{type:write}': ['p(95)<2000'],
    'http_req_failed{priority:critical}': ['rate<0.001'],
    'http_req_duration{endpoint:products}': ['avg<200'],
  },
};
```

### Tag `name`: agrupar requests dinámicos

Payload nombrado (POST con objeto `payload` y tag `name`), útil cuando el mismo
endpoint se invoca con cuerpos distintos:

```javascript
const payload = {
  username: 'user@example.com',
  password: 'password123',
};

const res = http.post('https://api.example.com/login', payload, {
  headers: { 'Content-Type': 'application/json' },
  tags: { name: 'Login' },
});
```

```javascript
import http from 'k6/http';

export default function() {
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

  const res2 = http.post('https://api.example.com/login', payload, {
    headers: { 'Content-Type': 'application/json' },
    tags: { name: 'Login' },
  });

  // Batch requests (parallel)
  const responses = http.batch([
    ['GET', 'https://api.example.com/users', null, { tags: { name: 'GetUsers' } }],
    ['GET', 'https://api.example.com/products', null, { tags: { name: 'GetProducts' } }],
    ['GET', 'https://api.example.com/config', null, { tags: { name: 'GetConfig' } }],
  ]);
}
```

### Grupos como marcadores de transacción

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

---

## 13. Módulos y Organización de Código

### Estructura modular

```
k6-tests/
├── tests/
│   ├── load.js              # Test principal
│   ├── stress.js            # Stress test
│   ├── spike.js             # Spike test
│   └── soak.js              # Soak test
├── src/
│   ├── api/
│   │   ├── auth.js          # Módulo de autenticación
│   │   ├── products.js      # Módulo de productos
│   │   └── checkout.js      # Módulo de checkout
│   ├── utils/
│   │   ├── helpers.js       # Funciones helper
│   │   └── config.js        # Configuración
│   └── scenarios/
│       ├── browse.js        # Scenario: navegar
│       ├── search.js        # Scenario: buscar
│       └── purchase.js      # Scenario: comprar
├── data/
│   ├── users.json
│   └── products.csv
├── reports/
└── package.json             # (opcional, para bundler)
```

### Ejemplo de módulos

```javascript
// src/utils/config.js
export const BASE_URL = __ENV.TARGET_HOST || 'https://api.staging.example.com';
export const THINK_TIME = { min: 1, max: 5 };

export const THRESHOLDS = {
  http_req_duration: ['p(95)<2000'],
  http_req_failed: ['rate<0.01'],
  checks: ['rate>0.99'],
};
```

```javascript
// src/api/auth.js
import http from 'k6/http';
import { check } from 'k6';
import { BASE_URL } from '../utils/config.js';

export function login(email, password) {
  const res = http.post(`${BASE_URL}/api/auth/login`,
    JSON.stringify({ email, password }),
    { headers: { 'Content-Type': 'application/json' }, tags: { endpoint: 'login' } }
  );
  
  const success = check(res, {
    'login status 200': (r) => r.status === 200,
    'login has token': (r) => r.json('access_token') !== undefined,
  });
  
  if (success) {
    return {
      token: res.json('access_token'),
      userId: res.json('user.id'),
    };
  }
  return null;
}

export function getAuthHeaders(token) {
  return {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  };
}
```

```javascript
// tests/load.js - Test principal usando módulos
import { sleep } from 'k6';
import { SharedArray } from 'k6/data';
import { login, getAuthHeaders } from '../src/api/auth.js';
import { browseProducts } from '../src/scenarios/browse.js';
import { BASE_URL, THRESHOLDS, THINK_TIME } from '../src/utils/config.js';

const users = new SharedArray('users', () => JSON.parse(open('../data/users.json')));

export const options = {
  scenarios: {
    load_test: {
      executor: 'ramping-vus',
      stages: [
        { duration: '2m', target: 50 },
        { duration: '10m', target: 50 },
        { duration: '2m', target: 0 },
      ],
    },
  },
  thresholds: THRESHOLDS,
};

export default function () {
  const user = users[__VU % users.length];
  const auth = login(user.email, user.password);
  
  if (auth) {
    browseProducts(getAuthHeaders(auth.token));
  }
  
  sleep(Math.random() * (THINK_TIME.max - THINK_TIME.min) + THINK_TIME.min);
}
```

---

## 14. Protocolos Adicionales (gRPC, WebSocket, Browser)

### gRPC

```javascript
import grpc from 'k6/net/grpc';
import { check, sleep } from 'k6';

const client = new grpc.Client();
client.load(['definitions'], 'payment_service.proto');

export default function () {
  client.connect('grpc.example.com:443', { plaintext: false });
  
  const response = client.invoke('payment.PaymentService/ProcessPayment', {
    user_id: 'user_123',
    amount: 29.99,
    currency: 'USD',
  });
  
  check(response, {
    'gRPC status OK': (r) => r && r.status === grpc.StatusOK,
    'payment processed': (r) => r && r.message.status === 'PROCESSED',
  });
  
  client.close();
  sleep(1);
}
```

### WebSocket

```javascript
import ws from 'k6/ws';
import { check, sleep } from 'k6';

export default function () {
  const url = 'wss://ws.example.com/chat';
  const params = { headers: { 'Authorization': 'Bearer token' } };
  
  const res = ws.connect(url, params, function (socket) {
    socket.on('open', function () {
      socket.send(JSON.stringify({ action: 'join', room: 'general' }));
    });
    
    socket.on('message', function (msg) {
      const data = JSON.parse(msg);
      check(data, {
        'message received': (d) => d.type !== undefined,
      });
    });
    
    socket.on('error', function (e) {
      console.error('WebSocket error:', e.error());
    });
    
    // Enviar mensajes periódicamente
    socket.setInterval(function () {
      socket.send(JSON.stringify({
        action: 'message',
        text: `Hello from VU ${__VU}`,
      }));
    }, 2000);
    
    // Cerrar después de 30 segundos
    socket.setTimeout(function () {
      socket.close();
    }, 30000);
  });
  
  check(res, { 'WS status 101': (r) => r && r.status === 101 });
}
```

### Browser Testing (k6 browser module)

```javascript
import { browser } from 'k6/browser';
import { check } from 'k6';

export const options = {
  scenarios: {
    browser_test: {
      executor: 'constant-vus',
      vus: 5,
      duration: '5m',
      options: {
        browser: {
          type: 'chromium',
        },
      },
    },
  },
};

export default async function () {
  const page = await browser.newPage();
  
  try {
    // Navegar
    await page.goto('https://example.com/login');
    
    // Llenar formulario
    await page.locator('#email').fill('test@example.com');
    await page.locator('#password').fill('password123');
    await page.locator('button[type="submit"]').click();
    
    // Esperar navegación
    await page.waitForNavigation();
    
    // Verificar
    const heading = await page.locator('h1').textContent();
    check(heading, {
      'logged in successfully': (h) => h.includes('Dashboard'),
    });
    
    // Medir Web Vitals
    const performanceMetrics = await page.evaluate(() => ({
      lcp: performance.getEntriesByType('largest-contentful-paint')[0]?.startTime,
      fid: performance.getEntriesByType('first-input')[0]?.processingStart,
      cls: performance.getEntriesByType('layout-shift')
        .reduce((sum, entry) => sum + entry.value, 0),
    }));
    
    console.log(`LCP: ${performanceMetrics.lcp}ms`);
    
  } finally {
    await page.close();
  }
}
```

Variante mínima con `locator.type()` y escenario anidado en `options` (forma corta):

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

## 15. Environment Variables y Options

### Options completas

```javascript
export const options = {
  // ─── Scenarios (ver sección 5) ───
  scenarios: { /* ... */ },
  
  // ─── O usar shortcuts (sin scenarios) ───
  vus: 50,
  duration: '5m',
  // stages: [{ duration: '2m', target: 100 }, ...],
  // iterations: 1000,
  
  // ─── Thresholds ───
  thresholds: { /* ... */ },
  
  // ─── HTTP ───
  httpDebug: 'full',        // 'full' o '' para debug HTTP
  insecureSkipTLSVerify: true, // Ignorar TLS errors
  userAgent: 'k6-load-test/1.0',
  batch: 20,                // Max parallel requests en batch()
  batchPerHost: 6,          // Max parallel por host
  
  // ─── DNS ───
  dns: {
    ttl: '5m',              // Cache DNS 5 minutos
    select: 'roundRobin',   // roundRobin, random, first
    policy: 'preferIPv4',   // preferIPv4, preferIPv6, onlyIPv4, onlyIPv6, any
  },
  
  // ─── Tags por defecto ───
  tags: {
    environment: 'staging',
    team: 'platform',
    build: __ENV.BUILD_ID || 'local',
  },
  
  // ─── No-connection-reuse ───
  noConnectionReuse: false,  // true = nueva conexión por request
  noVUConnectionReuse: false, // true = nueva conexión por iteración
  
  // ─── Abort conditions ───
  // abortOnFail thresholds (ver thresholds)
  
  // ─── Cloud options (Grafana Cloud k6) ───
  cloud: {
    projectID: 12345,
    name: 'My Load Test',
    note: 'Sprint 42 regression test',
  },
};
```

### Environment variables

```bash
# Variables de entorno accesibles via __ENV
k6 run script.js \
  -e TARGET_HOST=https://api.staging.com \
  -e API_TOKEN=secret123 \
  -e USERS=200 \
  -e DURATION=10m

# O con export:
export K6_VUS=100
export K6_DURATION=5m
export TARGET_HOST=https://api.prod.com
k6 run script.js
```

```javascript
// Acceso en el script
const host = __ENV.TARGET_HOST || 'https://api.staging.com';
const token = __ENV.API_TOKEN;
const targetUsers = parseInt(__ENV.USERS || '100');
```

---

## 16. Extensions (xk6)

### Extensiones populares

| Extension | Funcionalidad |
|-----------|--------------|
| `xk6-browser` | Browser automation (built-in desde k6 v0.43) |
| `xk6-dashboard` | Real-time HTML dashboard |
| `xk6-sql` | Database testing (PostgreSQL, MySQL, SQLite) |
| `xk6-kafka` | Apache Kafka producer/consumer |
| `xk6-amqp` | RabbitMQ testing |
| `xk6-redis` | Redis commands |
| `xk6-output-prometheus-remote` | Prometheus Remote Write |
| `xk6-disruptor` | Fault injection (chaos) |
| `xk6-faker` | Fake data generation |
| `xk6-exec` | Execute OS commands |

### Compilar k6 con extensions

```bash
# Instalar xk6 builder
go install go.k6.io/xk6/cmd/xk6@latest

# Compilar k6 custom con extensiones
xk6 build latest \
  --with github.com/grafana/xk6-sql \
  --with github.com/mostafa/xk6-kafka \
  --with github.com/grafana/xk6-dashboard

# El binario resultante incluye las extensiones
./k6 run script.js --out dashboard
```

### Ejemplo: xk6-sql (Database testing)

```javascript
import sql from 'k6/x/sql';
import { check } from 'k6';

const db = sql.open('postgres', 'postgres://user:pass@localhost:5432/testdb?sslmode=disable');

export function setup() {
  db.exec(`CREATE TABLE IF NOT EXISTS perf_test (
    id SERIAL PRIMARY KEY,
    value TEXT,
    created_at TIMESTAMP DEFAULT NOW()
  )`);
}

export default function () {
  // INSERT
  db.exec(`INSERT INTO perf_test (value) VALUES ('test_${__VU}_${__ITER}')`);
  
  // SELECT
  const results = sql.query(db, 'SELECT COUNT(*) as cnt FROM perf_test');
  check(results, {
    'has rows': (r) => r.length > 0,
    'count > 0': (r) => r[0].cnt > 0,
  });
}

export function teardown() {
  db.exec('DROP TABLE IF EXISTS perf_test');
  db.close();
}
```

---

## 17. Output y Exportación de Resultados

### Outputs disponibles

```bash
# Stdout (default) - summary al final
k6 run script.js

# JSON (todas las métricas punto por punto)
k6 run --out json=results.json script.js

# CSV
k6 run --out csv=results.csv script.js

# InfluxDB
k6 run --out influxdb=http://localhost:8086/k6 script.js

# Prometheus Remote Write
k6 run --out experimental-prometheus-rw script.js

# Grafana Cloud k6
k6 cloud run script.js

# Múltiples outputs simultáneos
k6 run \
  --out json=results.json \
  --out influxdb=http://influxdb:8086/k6 \
  script.js

# xk6-dashboard (real-time web dashboard)
k6 run --out dashboard script.js
# Abre http://localhost:5665
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

### handleSummary (reportes custom)

```javascript
import { textSummary } from 'https://jslib.k6.io/k6-summary/0.1.0/index.js';
import { htmlReport } from 'https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js';

export function handleSummary(data) {
  return {
    // Stdout (siempre incluir)
    stdout: textSummary(data, { indent: '→', enableColors: true }),
    
    // JSON summary
    'reports/summary.json': JSON.stringify(data, null, 2),
    
    // HTML report
    'reports/report.html': htmlReport(data),
    
    // Custom format (JUnit XML para CI/CD)
    'reports/junit.xml': generateJUnitXML(data),
  };
}

function generateJUnitXML(data) {
  const failures = Object.entries(data.metrics)
    .filter(([_, m]) => m.thresholds && Object.values(m.thresholds).some(t => !t.ok))
    .length;
  
  let xml = `<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite name="k6" tests="${Object.keys(data.metrics).length}" failures="${failures}">`;
  
  for (const [name, metric] of Object.entries(data.metrics)) {
    if (metric.thresholds) {
      for (const [threshold, result] of Object.entries(metric.thresholds)) {
        xml += `
    <testcase name="${name}: ${threshold}" classname="k6.thresholds">
      ${!result.ok ? `<failure message="Threshold breached: ${threshold}"/>` : ''}
    </testcase>`;
      }
    }
  }
  
  xml += `
  </testsuite>
</testsuites>`;
  return xml;
}
```

---

> **Secciones extraídas a la guía canónica común.**
> Versión canónica: [00_Comunes_Guia_Herramientas.md](00_Comunes_Guia_Herramientas.md) (CI/CD, troubleshooting, mejores prácticas, proyecto de referencia).
> Delta de esta herramienta: `K6_CLOUD_TOKEN` para Grafana Cloud, `test_type` como input choice del workflow, instalación por apt con el keyring de k6 y stack local InfluxDB + Grafana. Detalle en las secciones 1.2, 1.3 y 1.6 de la guía común; Grafana Cloud en la sección 19.

## 19. Integración con Grafana Cloud

```javascript
// Ejecutar en Grafana Cloud k6
// k6 cloud run script.js

export const options = {
  cloud: {
    projectID: 3645712,
    name: 'API Load Test - Sprint 42',
    note: 'Testing new payment microservice',
  },
  
  scenarios: {
    load: {
      executor: 'ramping-vus',
      stages: [
        { duration: '5m', target: 100 },
        { duration: '20m', target: 100 },
        { duration: '5m', target: 0 },
      ],
    },
  },
  
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};
```

```bash
# Login a Grafana Cloud
k6 cloud login --token YOUR_TOKEN

# Ejecutar en la nube (carga distribuida)
k6 cloud run script.js

# Ejecutar local pero enviar resultados a la nube
k6 run --out cloud script.js
```

---

## 20. Patrones Avanzados

### 20.1 Token refresh automático

```javascript
import http from 'k6/http';
import { sleep } from 'k6';
import exec from 'k6/execution';

let token = null;
let tokenExpiry = 0;

function getToken() {
  if (token && Date.now() < tokenExpiry - 30000) {
    return token;  // Token aún válido
  }
  
  const res = http.post('https://api.example.com/auth/token', JSON.stringify({
    grant_type: 'client_credentials',
    client_id: __ENV.CLIENT_ID,
    client_secret: __ENV.CLIENT_SECRET,
  }), { headers: { 'Content-Type': 'application/json' }, tags: { endpoint: 'auth' } });
  
  if (res.status === 200) {
    token = res.json('access_token');
    tokenExpiry = Date.now() + (res.json('expires_in') * 1000);
  }
  return token;
}

export default function () {
  const authToken = getToken();
  const params = {
    headers: { 'Authorization': `Bearer ${authToken}`, 'Content-Type': 'application/json' },
  };
  
  http.get('https://api.example.com/api/data', params);
  sleep(1);
}
```

### 20.2 Ramping por escenario con datos

```javascript
import http from 'k6/http';
import { SharedArray } from 'k6/data';
import exec from 'k6/execution';

const testData = new SharedArray('data', () => JSON.parse(open('./data/test_cases.json')));

export const options = {
  scenarios: {
    smoke: {
      executor: 'shared-iterations',
      vus: 1,
      iterations: 5,
      exec: 'smokeTest',
      startTime: '0s',
    },
    ramp: {
      executor: 'ramping-arrival-rate',
      startRate: 1,
      timeUnit: '1s',
      stages: [
        { duration: '2m', target: 50 },
        { duration: '5m', target: 50 },
        { duration: '2m', target: 0 },
      ],
      preAllocatedVUs: 20,
      maxVUs: 100,
      exec: 'mainTest',
      startTime: '30s',  // Empieza después del smoke
    },
  },
};

export function smokeTest() {
  const res = http.get('https://api.example.com/health');
  if (res.status !== 200) {
    exec.test.abort('Smoke test failed! System not healthy.');
  }
}

export function mainTest() {
  const item = testData[exec.scenario.iterationInTest % testData.length];
  http.post('https://api.example.com/api/process', JSON.stringify(item));
}
```

### 20.3 Circuit breaker pattern en test

```javascript
import http from 'k6/http';
import { sleep } from 'k6';
import { Rate } from 'k6/metrics';
import exec from 'k6/execution';

const errorRate = new Rate('circuit_breaker_errors');
let consecutiveFailures = 0;
const FAILURE_THRESHOLD = 10;

export default function () {
  const res = http.get('https://api.example.com/api/critical');
  
  if (res.status >= 500) {
    consecutiveFailures++;
    errorRate.add(true);
    
    if (consecutiveFailures >= FAILURE_THRESHOLD) {
      console.error(`Circuit breaker OPEN: ${consecutiveFailures} consecutive failures`);
      exec.test.abort('Too many consecutive failures - system appears down');
    }
  } else {
    consecutiveFailures = 0;
    errorRate.add(false);
  }
  
  sleep(1);
}
```

### 20.4 Correlación (extracción de valores dinámicos)

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

## 21. Testing de Performance en Microservicios

```javascript
// Test multi-servicio con scenarios dedicados
import http from 'k6/http';
import { check, group, sleep } from 'k6';

const SERVICES = {
  auth: __ENV.AUTH_URL || 'https://auth.example.com',
  products: __ENV.PRODUCTS_URL || 'https://products.example.com',
  orders: __ENV.ORDERS_URL || 'https://orders.example.com',
  payments: __ENV.PAYMENTS_URL || 'https://payments.example.com',
};

export const options = {
  scenarios: {
    auth_service: {
      executor: 'constant-arrival-rate',
      rate: 50, timeUnit: '1s', duration: '10m',
      preAllocatedVUs: 20, maxVUs: 100,
      exec: 'testAuth',
      tags: { service: 'auth' },
    },
    products_service: {
      executor: 'constant-arrival-rate',
      rate: 200, timeUnit: '1s', duration: '10m',
      preAllocatedVUs: 50, maxVUs: 300,
      exec: 'testProducts',
      tags: { service: 'products' },
    },
    orders_service: {
      executor: 'constant-arrival-rate',
      rate: 30, timeUnit: '1s', duration: '10m',
      preAllocatedVUs: 15, maxVUs: 80,
      exec: 'testOrders',
      tags: { service: 'orders' },
    },
  },
  thresholds: {
    'http_req_duration{service:auth}': ['p(95)<200'],
    'http_req_duration{service:products}': ['p(95)<300'],
    'http_req_duration{service:orders}': ['p(95)<1000'],
    'http_req_failed{service:auth}': ['rate<0.001'],
    'http_req_failed{service:products}': ['rate<0.01'],
    'http_req_failed{service:orders}': ['rate<0.01'],
  },
};

export function testAuth() {
  const res = http.post(`${SERVICES.auth}/token`,
    JSON.stringify({ grant_type: 'client_credentials' }),
    { headers: { 'Content-Type': 'application/json' }, tags: { service: 'auth' } }
  );
  check(res, { 'auth 200': (r) => r.status === 200 });
}

export function testProducts() {
  const res = http.get(`${SERVICES.products}/api/v1/products?limit=20`,
    { tags: { service: 'products' } }
  );
  check(res, {
    'products 200': (r) => r.status === 200,
    'has items': (r) => r.json('items').length > 0,
  });
}

export function testOrders() {
  const res = http.post(`${SERVICES.orders}/api/v1/orders`,
    JSON.stringify({ product_id: 'P001', quantity: 1 }),
    { headers: { 'Content-Type': 'application/json' }, tags: { service: 'orders' } }
  );
  check(res, { 'order created': (r) => r.status === 201 });
}
```

---

> **Secciones extraídas a la guía canónica común.**
> Versión canónica: [00_Comunes_Guia_Herramientas.md](00_Comunes_Guia_Herramientas.md) (CI/CD, troubleshooting, mejores prácticas, proyecto de referencia).
> Delta de esta herramienta: `k6 inspect` valida el script sin ejecutarlo y `open()` solo funciona en init phase (sección 2.1); `SharedArray` para no duplicar el dataset en RAM y `thresholds` como SLO (sección 3.3); `grafana/dashboards/k6-dashboard.json` y targets `cloud`/`dashboard` del Makefile (secciones 4.3-4.4).

## Referencias

- [k6 Official Documentation](https://grafana.com/docs/k6/latest/)
- [k6 GitHub Repository](https://github.com/grafana/k6)
- [k6 JavaScript API Reference](https://grafana.com/docs/k6/latest/javascript-api/)
- [k6 Examples](https://github.com/grafana/k6/tree/master/examples)
- [xk6 Extensions Registry](https://grafana.com/docs/k6/latest/extensions/)
- [Grafana Cloud k6](https://grafana.com/products/cloud/k6/)
- [k6 Browser Module](https://grafana.com/docs/k6/latest/using-k6-browser/)
- [k6 jslib (utility libraries)](https://jslib.k6.io/)
- [k6 Community](https://community.grafana.com/c/grafana-k6/)
- [k6 Blog](https://grafana.com/blog/tags/k6/)

---

> 💡 **k6 es la herramienta más eficiente para load testing moderno.**
> Su combinación de scripting en JavaScript, motor en Go, y integración nativa con Grafana la hace ideal para equipos DevOps que necesitan tests rápidos, eficientes, y fácilmente integrables en CI/CD. Un solo binario, sin dependencias externas.
