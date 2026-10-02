# Scripting Avanzado - Parametrización, Correlación y Patrones

## Patrones de Scripting Avanzados

### 1. Chain of Requests Pattern

Cuando una secuencia de requests depende de datos de responses anteriores:

```javascript
// k6: Chain Pattern
import http from 'k6/http';
import { check } from 'k6';

export default function() {
  // Step 1: Get CSRF token
  const page = http.get(`${BASE_URL}/login`);
  const csrf = page.html().find('meta[name="csrf-token"]').attr('content');
  
  // Step 2: Login (using CSRF)
  const login = http.post(`${BASE_URL}/api/auth/login`, JSON.stringify({
    email: userData.email,
    password: userData.password,
    _csrf: csrf
  }), { headers: { 'Content-Type': 'application/json' } });
  
  const token = login.json('data.accessToken');
  const refreshToken = login.json('data.refreshToken');
  const userId = login.json('data.user.id');
  
  // Step 3: Get user profile (using token and userId)
  const profile = http.get(`${BASE_URL}/api/users/${userId}/profile`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  // Step 4: Get user's orders (using token)
  const orders = http.get(`${BASE_URL}/api/users/${userId}/orders?limit=10`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  const orderId = orders.json('data.orders[0].id');
  
  // Step 5: Get specific order detail (using orderId from previous)
  if (orderId) {
    const orderDetail = http.get(`${BASE_URL}/api/orders/${orderId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
  }
}
```

### 2. Token Refresh Pattern

Manejar tokens que expiran durante tests largos:

```javascript
// k6: Token Refresh Pattern
let authToken = null;
let tokenExpiry = 0;

function getValidToken() {
  const now = Date.now();
  
  if (!authToken || now >= tokenExpiry - 30000) { // Refresh 30s before expiry
    const res = http.post(`${BASE_URL}/api/auth/refresh`, JSON.stringify({
      refresh_token: refreshToken
    }), { headers: { 'Content-Type': 'application/json' } });
    
    if (res.status === 200) {
      authToken = res.json('access_token');
      tokenExpiry = now + (res.json('expires_in') * 1000);
    } else {
      // Re-login if refresh fails
      const loginRes = login(currentUser.email, currentUser.password);
      authToken = loginRes.json('access_token');
      tokenExpiry = now + (loginRes.json('expires_in') * 1000);
    }
  }
  
  return authToken;
}

export default function() {
  const token = getValidToken();
  const res = http.get(`${BASE_URL}/api/data`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
}
```

### 3. Retry with Backoff Pattern

```javascript
// k6: Exponential Backoff Retry
function requestWithRetry(method, url, body, params, maxRetries = 3) {
  let lastResponse = null;
  
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    if (attempt > 0) {
      const backoffMs = Math.pow(2, attempt) * 1000 + Math.random() * 1000;
      sleep(backoffMs / 1000);
    }
    
    lastResponse = method === 'GET' 
      ? http.get(url, params) 
      : http.post(url, body, params);
    
    // Success or client error (don't retry 4xx)
    if (lastResponse.status < 500) {
      return lastResponse;
    }
    
    console.warn(`Attempt ${attempt + 1} failed: ${lastResponse.status}`);
  }
  
  return lastResponse; // Return last failed response
}
```

### 4. Session State Management Pattern

```javascript
// k6: Session State across iterations
import { SharedArray } from 'k6/data';

// Per-VU state (persists across iterations within same VU)
let vuState = {
  isLoggedIn: false,
  token: null,
  cart: [],
  sessionId: null,
};

export default function() {
  // First iteration: login
  if (!vuState.isLoggedIn) {
    const loginRes = http.post(`${BASE_URL}/login`, JSON.stringify({
      username: testUsers[__VU % testUsers.length].username,
      password: testUsers[__VU % testUsers.length].password,
    }));
    
    if (loginRes.status === 200) {
      vuState.isLoggedIn = true;
      vuState.token = loginRes.json('token');
      vuState.sessionId = loginRes.json('session_id');
    }
  }
  
  // Use state in subsequent requests
  if (vuState.isLoggedIn) {
    const headers = { 'Authorization': `Bearer ${vuState.token}` };
    
    // Add items to cart (accumulates across iterations)
    const product = getRandomProduct();
    const cartRes = http.post(`${BASE_URL}/cart/add`, 
      JSON.stringify({ product_id: product.id }),
      { headers }
    );
    
    if (cartRes.status === 201) {
      vuState.cart.push(product.id);
    }
    
    // Checkout when cart has 3+ items
    if (vuState.cart.length >= 3) {
      http.post(`${BASE_URL}/checkout`, 
        JSON.stringify({ items: vuState.cart }),
        { headers }
      );
      vuState.cart = []; // Reset cart
    }
  }
  
  sleep(randomThinkTime(5, 15));
}
```

### 5. File Upload Pattern

```javascript
// k6: File Upload
import http from 'k6/http';
import { FormData } from 'https://jslib.k6.io/formdata/0.0.2/index.js';

const testFile = open('./data/test-image.png', 'b'); // binary mode

export default function() {
  const fd = new FormData();
  fd.append('file', http.file(testFile, 'upload.png', 'image/png'));
  fd.append('description', 'Performance test upload');
  fd.append('category', 'test');
  
  const res = http.post(`${BASE_URL}/api/upload`, fd.body(), {
    headers: { 
      'Content-Type': `multipart/form-data; boundary=${fd.boundary}`,
      'Authorization': `Bearer ${token}`,
    },
    timeout: '60s', // Larger timeout for uploads
  });
  
  check(res, {
    'upload successful': (r) => r.status === 200,
    'file ID returned': (r) => r.json('file_id') !== undefined,
  });
}
```

### 6. WebSocket Pattern

```javascript
// k6: WebSocket Testing
import ws from 'k6/ws';
import { check } from 'k6';

export default function() {
  const url = 'wss://api.example.com/ws';
  
  const res = ws.connect(url, { 
    headers: { 'Authorization': `Bearer ${token}` }
  }, function(socket) {
    
    socket.on('open', () => {
      // Subscribe to channel
      socket.send(JSON.stringify({
        type: 'subscribe',
        channel: 'notifications'
      }));
      
      // Send messages periodically
      socket.setInterval(function() {
        socket.send(JSON.stringify({
          type: 'ping',
          timestamp: Date.now()
        }));
      }, 5000); // Every 5 seconds
    });
    
    socket.on('message', (msg) => {
      const data = JSON.parse(msg);
      check(data, {
        'received valid message': (d) => d.type !== undefined,
        'message not error': (d) => d.type !== 'error',
      });
    });
    
    socket.on('error', (e) => {
      console.error('WebSocket error:', e.error());
    });
    
    // Keep connection open for 60 seconds
    socket.setTimeout(function() {
      socket.close();
    }, 60000);
  });
  
  check(res, {
    'WebSocket status is 101': (r) => r && r.status === 101,
  });
}
```

### 7. GraphQL Pattern

```javascript
// k6: GraphQL Testing
import http from 'k6/http';

function graphqlQuery(query, variables = {}) {
  return http.post(`${BASE_URL}/graphql`, JSON.stringify({
    query: query,
    variables: variables,
  }), {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
  });
}

export default function() {
  // Simple query
  const productsRes = graphqlQuery(`
    query GetProducts($first: Int!, $after: String) {
      products(first: $first, after: $after) {
        edges {
          node {
            id
            name
            price
            inStock
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
  `, { first: 20 });
  
  check(productsRes, {
    'graphql success': (r) => r.json('errors') === undefined || r.json('errors') === null,
    'has products': (r) => r.json('data.products.edges').length > 0,
  });
  
  // Mutation
  const orderRes = graphqlQuery(`
    mutation CreateOrder($input: OrderInput!) {
      createOrder(input: $input) {
        id
        status
        total
      }
    }
  `, { 
    input: { 
      items: [{ productId: "prod-123", quantity: 2 }],
      shippingAddress: { city: "Test City" }
    }
  });
}
```

---

## Data Management Strategies

### Estrategia 1: Pre-generated Static Data

```
Pros: Simple, reproducible, no dependencies
Cons: Limited variety, can exhaust quickly

Structure:
data/
├── users.csv          (5000 rows: email, password, name)
├── products.json      (10000 products with all attributes)
├── search_terms.csv   (500 real search terms from prod logs)
├── addresses.json     (1000 valid addresses by country)
└── credit_cards.csv   (100 test card numbers)
```

### Estrategia 2: Dynamic Data Generation

```javascript
// k6: Dynamic data generation
import { randomString, randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.4.0/index.js';

function generateUser() {
  const id = randomIntBetween(1, 1000000);
  return {
    email: `perf_user_${id}_${randomString(5)}@test.com`,
    password: 'TestPass123!',
    firstName: `User${id}`,
    lastName: `Test${randomIntBetween(1, 100)}`,
  };
}

function generateOrder() {
  return {
    items: Array.from({ length: randomIntBetween(1, 5) }, () => ({
      product_id: `PRD-${randomIntBetween(1, 10000)}`,
      quantity: randomIntBetween(1, 3),
    })),
    shipping: generateAddress(),
    notes: `Perf test order ${Date.now()}`,
  };
}
```

### Estrategia 3: Database Seeding + Cleanup

```bash
#!/bin/bash
# Pre-test: Seed database
echo "Seeding test data..."
psql -h $DB_HOST -U $DB_USER -f seed_test_data.sql
echo "Seeded: 5000 users, 10000 products, 100000 historical orders"

# Post-test: Cleanup
echo "Cleaning test data..."
psql -h $DB_HOST -U $DB_USER -c "
  DELETE FROM orders WHERE created_at > '2026-06-10';
  DELETE FROM cart_items WHERE user_id IN (SELECT id FROM users WHERE email LIKE 'perf_%');
  DELETE FROM sessions WHERE user_id IN (SELECT id FROM users WHERE email LIKE 'perf_%');
  VACUUM ANALYZE;
"
echo "Cleanup complete"
```

---

## Error Handling Best Practices

### Comprehensive Error Handling

```javascript
// k6: Robust error handling
import http from 'k6/http';
import { check, fail } from 'k6';
import { Counter } from 'k6/metrics';

const errors = {
  auth: new Counter('errors_auth'),
  timeout: new Counter('errors_timeout'),
  server: new Counter('errors_server'),
  validation: new Counter('errors_validation'),
  unknown: new Counter('errors_unknown'),
};

function categorizeError(response) {
  if (!response) {
    errors.timeout.add(1);
    return 'timeout';
  }
  if (response.status === 401 || response.status === 403) {
    errors.auth.add(1);
    return 'auth';
  }
  if (response.status >= 500) {
    errors.server.add(1);
    return 'server';
  }
  if (response.status >= 400) {
    errors.validation.add(1);
    return 'validation';
  }
  errors.unknown.add(1);
  return 'unknown';
}

function safeRequest(method, url, body, params) {
  try {
    const res = method === 'GET' 
      ? http.get(url, params) 
      : http.post(url, body, params);
    
    if (res.status >= 400) {
      const errorType = categorizeError(res);
      console.warn(`[${errorType}] ${method} ${url}: ${res.status} - ${res.body.substring(0, 200)}`);
    }
    
    return res;
  } catch (e) {
    errors.timeout.add(1);
    console.error(`[exception] ${method} ${url}: ${e.message}`);
    return null;
  }
}
```

---

## Script Maintenance

### Versionado y changelog

```markdown
# CHANGELOG - Performance Test Scripts

## v2.3.0 (2026-06-10)
### Added
- New scenario: Mobile API sync flow (SC-05)
- WebSocket testing for real-time notifications
### Changed
- Updated checkout flow for new payment API v3
- Increased think times based on fresh production data
### Fixed
- Correlation for new CSRF token format
- Token refresh handling for long endurance tests

## v2.2.1 (2026-05-15)
### Fixed
- CSV data encoding issue causing auth failures
- Race condition in shared cart operations
```

### Code Review Checklist for Perf Scripts

```
□ All dynamic values are correlated (no hardcoded tokens/IDs)
□ Data is parameterized (no hardcoded test data)
□ Think times are realistic (not 0, not fixed)
□ Assertions validate response correctness (not just status code)
□ Error handling doesn't hide real failures
□ Transaction markers cover all business flows
□ Script works with 1 VU before scaling
□ No sensitive data in script (passwords, keys)
□ Code is modular and reusable
□ Comments explain WHY, not WHAT
□ Thresholds match documented SLAs
```

---

*Documento de referencia - Performance Test Life Cycle*
*Última actualización: Junio 2026*
