# Fases 4-6: Entorno, Scripts y Ejecución

## FASE 4: CONFIGURACIÓN DEL ENTORNO

### Infraestructura como Código (IaC) para Performance Testing

#### Terraform Example - Performance Test Environment

```hcl
# Performance Test Environment - AWS
module "perf_test_env" {
  source = "./modules/perf-environment"
  
  # Application Tier
  app_instances = {
    count         = 4
    instance_type = "m5.2xlarge"
    ami           = var.app_ami_id
    subnet_ids    = var.private_subnets
  }
  
  # Database Tier
  database = {
    instance_class    = "db.r5.4xlarge"
    engine            = "postgres"
    engine_version    = "15.4"
    allocated_storage = 500
    read_replicas     = 2
    multi_az          = false  # Cost saving for test env
  }
  
  # Cache Tier
  cache = {
    node_type       = "cache.r6g.large"
    engine          = "redis"
    engine_version  = "7.0"
    num_cache_nodes = 1
  }
  
  # Load Generators
  load_generators = {
    count         = 4
    instance_type = "c5.2xlarge"
    ami           = var.loadgen_ami_id
    subnet_ids    = var.public_subnets
  }
  
  # Monitoring
  monitoring = {
    prometheus_instance = "m5.large"
    grafana_instance    = "t3.medium"
  }
  
  tags = {
    Environment = "performance-test"
    Project     = var.project_name
    AutoShutdown = "true"  # Cost control
  }
}
```

### Validación del Entorno

#### Script de validación automatizada
```bash
#!/bin/bash
# environment_validation.sh

echo "=== Performance Test Environment Validation ==="
echo ""

# 1. Application servers
echo "[1/7] Checking application servers..."
for server in ${APP_SERVERS[@]}; do
  status=$(curl -s -o /dev/null -w "%{http_code}" http://$server:8080/health)
  if [ "$status" = "200" ]; then
    echo "  ✅ $server - healthy"
  else
    echo "  ❌ $server - unhealthy (status: $status)"
    FAILURES=$((FAILURES+1))
  fi
done

# 2. Database connectivity
echo "[2/7] Checking database..."
pg_isready -h $DB_HOST -p 5432 -U $DB_USER
if [ $? -eq 0 ]; then
  echo "  ✅ Database accepting connections"
  # Verify data volume
  RECORD_COUNT=$(psql -h $DB_HOST -U $DB_USER -t -c "SELECT COUNT(*) FROM users")
  echo "  📊 Users table: $RECORD_COUNT records"
else
  echo "  ❌ Database not ready"
fi

# 3. Cache
echo "[3/7] Checking Redis cache..."
redis-cli -h $REDIS_HOST ping
echo "  📊 Memory: $(redis-cli -h $REDIS_HOST info memory | grep used_memory_human)"

# 4. Load balancer
echo "[4/7] Checking load balancer..."
curl -s -o /dev/null -w "%{http_code}" https://$LB_URL/health

# 5. Monitoring
echo "[5/7] Checking monitoring stack..."
curl -s -o /dev/null -w "%{http_code}" http://$GRAFANA_HOST:3000/api/health
curl -s -o /dev/null -w "%{http_code}" http://$PROMETHEUS_HOST:9090/-/healthy

# 6. Load generators
echo "[6/7] Checking load generators..."
for gen in ${LOAD_GENERATORS[@]}; do
  k6_version=$(ssh $gen "k6 version" 2>/dev/null)
  echo "  ✅ $gen - k6 $k6_version"
done

# 7. Network
echo "[7/7] Checking network connectivity..."
for server in ${APP_SERVERS[@]}; do
  latency=$(ping -c 3 $server | tail -1 | awk '{print $4}' | cut -d '/' -f 2)
  echo "  📊 Latency to $server: ${latency}ms"
done

echo ""
echo "=== Validation Complete ==="
if [ $FAILURES -eq 0 ]; then
  echo "✅ Environment READY for performance testing"
else
  echo "❌ $FAILURES checks FAILED - resolve before testing"
fi
```

---

## FASE 5: DESARROLLO DE SCRIPTS

### Framework de Scripts (k6 Example)

#### Estructura del proyecto

```
performance-tests/
├── config/
│   ├── environments.js          # Environment-specific configs
│   ├── thresholds.js            # SLA thresholds
│   └── options/
│       ├── load-test.js         # Load test options
│       ├── stress-test.js       # Stress test options
│       ├── endurance-test.js    # Endurance test options
│       └── spike-test.js        # Spike test options
├── data/
│   ├── users.csv                # User credentials
│   ├── products.csv             # Product IDs
│   ├── search_terms.csv         # Search keywords
│   └── addresses.json           # Shipping addresses
├── lib/
│   ├── auth.js                  # Authentication helpers
│   ├── api.js                   # API request builders
│   ├── checks.js                # Common assertions
│   ├── data-loader.js           # Data loading utilities
│   └── metrics.js               # Custom metrics
├── scenarios/
│   ├── browse.js                # Browse scenario
│   ├── search.js                # Search scenario
│   ├── purchase.js              # Purchase flow
│   ├── account.js               # Account management
│   └── api-direct.js            # Direct API calls
├── tests/
│   ├── load-test.js             # Load test orchestrator
│   ├── stress-test.js           # Stress test orchestrator
│   ├── endurance-test.js        # Soak test orchestrator
│   └── spike-test.js            # Spike test orchestrator
├── utils/
│   ├── helpers.js               # Utility functions
│   └── reporting.js             # Report generation
├── package.json
└── README.md
```

#### Script de escenario completo (k6)

```javascript
// scenarios/purchase.js
import http from 'k6/http';
import { check, group, sleep } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';
import { randomItem } from '../lib/data-loader.js';
import { getAuthHeaders, login } from '../lib/auth.js';
import { BASE_URL } from '../config/environments.js';

// Custom metrics
const purchaseSuccess = new Rate('purchase_success_rate');
const checkoutDuration = new Trend('checkout_duration');
const cartAbandonment = new Counter('cart_abandonments');

export function purchaseFlow(userData, productData) {
  let headers = {};
  let cartId = null;
  let orderId = null;
  
  // Transaction 1: Login
  group('T01_Login', () => {
    const loginRes = login(userData.username, userData.password);
    
    const loginOk = check(loginRes, {
      'login successful': (r) => r.status === 200,
      'login response time OK': (r) => r.timings.duration < 2000,
      'received auth token': (r) => r.json('token') !== undefined,
    });
    
    if (!loginOk) {
      cartAbandonment.add(1);
      return; // Abort flow if login fails
    }
    
    headers = getAuthHeaders(loginRes.json('token'));
  });
  
  sleep(randomThinkTime(5, 12));
  
  // Transaction 2: Search Product
  group('T02_Search', () => {
    const searchTerm = randomItem(productData.searchTerms);
    const searchRes = http.get(
      `${BASE_URL}/api/v2/search?q=${encodeURIComponent(searchTerm)}&limit=20`,
      { headers, tags: { name: 'Search' } }
    );
    
    check(searchRes, {
      'search returns 200': (r) => r.status === 200,
      'search has results': (r) => r.json('results.length') > 0,
      'search response time OK': (r) => r.timings.duration < 2000,
    });
    
    // Correlate: extract first product ID
    if (searchRes.status === 200 && searchRes.json('results.length') > 0) {
      const products = searchRes.json('results');
      userData.selectedProduct = products[Math.floor(Math.random() * products.length)];
    }
  });
  
  sleep(randomThinkTime(3, 8));
  
  // Transaction 3: View Product
  group('T03_ViewProduct', () => {
    if (!userData.selectedProduct) return;
    
    const productRes = http.get(
      `${BASE_URL}/api/v2/products/${userData.selectedProduct.id}`,
      { headers, tags: { name: 'ViewProduct' } }
    );
    
    check(productRes, {
      'product page loads': (r) => r.status === 200,
      'product has price': (r) => r.json('price') > 0,
      'product in stock': (r) => r.json('in_stock') === true,
    });
  });
  
  sleep(randomThinkTime(8, 20));  // User reads product details
  
  // Transaction 4: Add to Cart
  group('T04_AddToCart', () => {
    if (!userData.selectedProduct) return;
    
    const cartRes = http.post(
      `${BASE_URL}/api/v2/cart/items`,
      JSON.stringify({
        product_id: userData.selectedProduct.id,
        quantity: 1,
      }),
      { headers: { ...headers, 'Content-Type': 'application/json' },
        tags: { name: 'AddToCart' } }
    );
    
    check(cartRes, {
      'item added to cart': (r) => r.status === 201,
      'cart ID returned': (r) => r.json('cart_id') !== undefined,
    });
    
    if (cartRes.status === 201) {
      cartId = cartRes.json('cart_id');
    }
  });
  
  sleep(randomThinkTime(2, 5));
  
  // Transaction 5: Checkout
  const checkoutStart = Date.now();
  
  group('T05_Checkout', () => {
    if (!cartId) {
      cartAbandonment.add(1);
      return;
    }
    
    // Step 5a: Enter shipping
    const shippingRes = http.post(
      `${BASE_URL}/api/v2/checkout/shipping`,
      JSON.stringify({
        cart_id: cartId,
        address: userData.address,
      }),
      { headers: { ...headers, 'Content-Type': 'application/json' },
        tags: { name: 'EnterShipping' } }
    );
    
    check(shippingRes, {
      'shipping accepted': (r) => r.status === 200,
    });
    
    sleep(randomThinkTime(10, 25));  // User reviews shipping
    
    // Step 5b: Process payment
    const paymentRes = http.post(
      `${BASE_URL}/api/v2/checkout/payment`,
      JSON.stringify({
        cart_id: cartId,
        payment_method: userData.paymentMethod,
      }),
      { headers: { ...headers, 'Content-Type': 'application/json' },
        tags: { name: 'ProcessPayment' } }
    );
    
    const paymentOk = check(paymentRes, {
      'payment processed': (r) => r.status === 200,
      'order confirmed': (r) => r.json('status') === 'confirmed',
      'order ID received': (r) => r.json('order_id') !== undefined,
      'payment response time OK': (r) => r.timings.duration < 5000,
    });
    
    purchaseSuccess.add(paymentOk);
    
    if (paymentOk) {
      orderId = paymentRes.json('order_id');
    }
  });
  
  const checkoutEnd = Date.now();
  checkoutDuration.add(checkoutEnd - checkoutStart);
  
  sleep(randomThinkTime(30, 90));  // Between iterations
  
  return { orderId, success: orderId !== null };
}

function randomThinkTime(min, max) {
  // Normal distribution approximation
  const mean = (min + max) / 2;
  const stddev = (max - min) / 4;
  let val = mean + stddev * (Math.random() + Math.random() + Math.random() - 1.5) * 2;
  return Math.max(min, Math.min(max, val));
}
```

#### Test Orchestrator (Load Test)

```javascript
// tests/load-test.js
import { SharedArray } from 'k6/data';
import { browseFlow } from '../scenarios/browse.js';
import { searchFlow } from '../scenarios/search.js';
import { purchaseFlow } from '../scenarios/purchase.js';
import { accountFlow } from '../scenarios/account.js';
import { thresholds } from '../config/thresholds.js';

// Load test data
const users = new SharedArray('users', () => 
  JSON.parse(open('../data/users.json'))
);

export const options = {
  scenarios: {
    browse: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '30m', target: 450 },  // 45% of 1000
        { duration: '2h', target: 450 },
        { duration: '10m', target: 0 },
      ],
      exec: 'browsing',
    },
    search: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '30m', target: 250 },  // 25% of 1000
        { duration: '2h', target: 250 },
        { duration: '10m', target: 0 },
      ],
      exec: 'searching',
    },
    purchase: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '30m', target: 150 },  // 15% of 1000
        { duration: '2h', target: 150 },
        { duration: '10m', target: 0 },
      ],
      exec: 'purchasing',
    },
    account: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '30m', target: 100 },  // 10% of 1000
        { duration: '2h', target: 100 },
        { duration: '10m', target: 0 },
      ],
      exec: 'managing_account',
    },
  },
  thresholds: thresholds,
};

export function browsing() {
  const user = users[__VU % users.length];
  browseFlow(user);
}

export function searching() {
  const user = users[__VU % users.length];
  searchFlow(user);
}

export function purchasing() {
  const user = users[__VU % users.length];
  purchaseFlow(user);
}

export function managing_account() {
  const user = users[__VU % users.length];
  accountFlow(user);
}
```

---

## FASE 6: EJECUCIÓN DE PRUEBAS

### Procedimiento de Ejecución

#### Runbook de ejecución

```markdown
# Performance Test Execution Runbook

## Pre-execution (30 minutes before)

1. [ ] Verify environment health (run validation script)
2. [ ] Confirm no deployments in progress
3. [ ] Reset test data (restore DB snapshot)
4. [ ] Clear application caches
5. [ ] Verify monitoring is active and collecting
6. [ ] Notify team in #perf-testing channel
7. [ ] Open monitoring dashboards
8. [ ] Start screen recording (optional)

## Execution

### Step 1: Smoke Test (5 minutes)
- Run with 2 VUs for 2 minutes
- Verify all transactions complete successfully
- Check assertions pass
- Verify monitoring captures data

### Step 2: Baseline (15 minutes)  
- Run with 50 VUs for 10 minutes
- Record baseline metrics
- Verify stable performance at low load

### Step 3: Main Test Execution
- Start the main test (load/stress/endurance)
- Monitor real-time dashboards
- Document any observations

### Step 4: During Execution - Monitor
Every 15 minutes check:
- [ ] Error rate within acceptable range
- [ ] Response times not degrading unexpectedly
- [ ] Server resources not saturating
- [ ] No alerts triggered
- [ ] Load generators healthy (CPU < 80%)

## Post-execution (immediately after)

1. [ ] Save all monitoring data/screenshots
2. [ ] Export raw results from testing tool
3. [ ] Document any incidents during test
4. [ ] Note environment conditions
5. [ ] Do NOT restart servers (preserve state for analysis)
6. [ ] Take thread dumps/heap dumps if issues detected
```

---

### Gestión de Incidentes Durante Ejecución

```yaml
incident_response_during_test:
  
  severity_1_abort:
    triggers:
      - "Complete system failure"
      - "Data corruption detected"
      - "Shared infrastructure affected"
    actions:
      - "STOP test immediately"
      - "Notify team leads"
      - "Preserve all logs and state"
      - "Document timeline of events"
      
  severity_2_pause:
    triggers:
      - "Error rate > 20% for 5+ minutes"
      - "Single component crash with no recovery"
      - "Monitoring failure"
    actions:
      - "Pause test (reduce to minimal load)"
      - "Investigate root cause"
      - "Decide: fix and continue, or abort"
      
  severity_3_document:
    triggers:
      - "Error rate spike (temporary)"
      - "Single transaction failing"
      - "Resource utilization approaching limits"
    actions:
      - "Document observation with timestamp"
      - "Continue test execution"
      - "Flag for post-test analysis"
```

---

*Documento de referencia - Performance Test Life Cycle*
*Última actualización: Junio 2026*
