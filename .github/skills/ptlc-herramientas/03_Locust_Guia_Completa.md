# 🦗 Locust - Guía Completa de Referencia

## Índice

1. [Introducción y Filosofía](#1-introducción-y-filosofía)
2. [Instalación y Configuración](#2-instalación-y-configuración)
3. [Arquitectura Interna](#3-arquitectura-interna)
4. [Fundamentos del Locustfile](#4-fundamentos-del-locustfile)
5. [User Classes en Profundidad](#5-user-classes-en-profundidad)
6. [Tasks y Control de Flujo](#6-tasks-y-control-de-flujo)
7. [HTTP Client y Validaciones](#7-http-client-y-validaciones)
8. [Wait Times y Pacing](#8-wait-times-y-pacing)
9. [Custom Load Shapes](#9-custom-load-shapes)
10. [Modo Distribuido](#10-modo-distribuido)
11. [Event Hooks y Extensibilidad](#11-event-hooks-y-extensibilidad)
12. [FastHttpUser (Alto Rendimiento)](#12-fasthttpuser-alto-rendimiento)
13. [Testing de Protocolos No-HTTP](#13-testing-de-protocolos-no-http)
14. [Datos de Prueba y Parametrización](#14-datos-de-prueba-y-parametrización)
15. [Métricas, Reportes y Exportación](#15-métricas-reportes-y-exportación)
16. [Integración con CI/CD](#16-integración-con-cicd)
17. [Plugins y Ecosistema](#17-plugins-y-ecosistema)
18. [Patrones Avanzados](#18-patrones-avanzados)
19. [Debugging y Troubleshooting](#19-debugging-y-troubleshooting)
20. [Comparativa con Otras Herramientas](#20-comparativa-con-otras-herramientas)
21. [Mejores Prácticas y Antipatrones](#21-mejores-prácticas-y-antipatrones)
22. [Proyecto de Referencia Completo](#22-proyecto-de-referencia-completo)

---

## 1. Introducción y Filosofía

### ¿Qué es Locust?

**Locust** es una herramienta open-source de performance testing escrita en Python que permite definir el comportamiento de usuarios virtuales mediante código Python puro. Su nombre proviene de las langostas (locust), conocidas por su comportamiento de enjambre.

### Filosofía de diseño

| Principio | Implementación |
|-----------|---------------|
| **Code as tests** | Python puro, sin XML/GUI/DSL propietario |
| **Distributed by design** | Master-Worker nativo con comunicación ZeroMQ |
| **Lightweight users** | Greenlets (gevent) → miles de usuarios por máquina |
| **Hackable** | Arquitectura de plugins, event hooks, custom clients |
| **Protocol agnostic** | HTTP por defecto, extensible a cualquier protocolo |

### Cuándo usar Locust

✅ **Ideal para:**
- Equipos con desarrolladores Python
- APIs REST/GraphQL
- Tests que requieren lógica compleja (decisiones, loops, cálculos)
- Custom load shapes (perfiles de carga no lineales)
- Protocolos no-HTTP (gRPC, WebSocket, MQTT, custom TCP)
- Integración con ecosistema Python (pandas, numpy, requests)
- Tests donde el comportamiento del usuario es más complejo que simple HTTP

❌ **Considerar alternativas si:**
- Necesitas máximo throughput por máquina (→ k6, Gatling)
- El equipo no conoce Python (→ k6 con JavaScript)
- Necesitas grabador de scripts visual (→ JMeter)
- Browser real rendering es requerido (→ Playwright, Cypress)

### Comparación rápida de rendimiento

```
Usuarios simulados por máquina (8 cores, 16GB RAM):
┌──────────────┬─────────────────┬───────────────────────┐
│ Herramienta  │ Usuarios aprox. │ Requests/seg aprox.   │
├──────────────┼─────────────────┼───────────────────────┤
│ Locust       │ 5,000 - 10,000  │ 5,000 - 15,000       │
│ k6           │ 10,000 - 50,000 │ 50,000 - 300,000     │
│ Gatling      │ 10,000 - 30,000 │ 20,000 - 100,000     │
│ JMeter       │ 1,000 - 3,000   │ 2,000 - 10,000       │
└──────────────┴─────────────────┴───────────────────────┘
* Locust compensa con FastHttpUser y modo distribuido fácil
```

---

## 2. Instalación y Configuración

### Instalación básica

```bash
# Instalación con pip
pip install locust

# Con extras para mayor rendimiento
pip install locust[fasthttp]

# Versión específica
pip install locust==2.29.1

# Desde source (desarrollo)
git clone https://github.com/locustio/locust.git
cd locust
pip install -e ".[dev]"
```

### Instalación con dependencias de proyecto

```txt
# requirements.txt
locust==2.29.1
geventhttpclient>=2.0.2
locust-plugins>=4.4.0
faker>=28.0.0
pandas>=2.0.0
```

### Configuración via archivo (locust.conf)

```ini
# locust.conf - Configuración por defecto del proyecto
[locust]
locustfile = src/tests/locustfile.py
host = https://api.staging.example.com
users = 100
spawn-rate = 10
run-time = 5m
headless = true
html = reports/report.html
csv = reports/results
loglevel = INFO
logfile = logs/locust.log

# Modo distribuido
# master = true
# expect-workers = 4
```

### Variables de entorno

```bash
# Configuración via environment variables
export LOCUST_HOST=https://api.example.com
export LOCUST_USERS=500
export LOCUST_SPAWN_RATE=20
export LOCUST_RUN_TIME=30m
export LOCUST_HEADLESS=true
export LOCUST_LOCUSTFILE=src/load_test.py
```

### Docker

```dockerfile
# Dockerfile para Locust
FROM locustio/locust:2.29.1

# Copiar tests y dependencias
COPY requirements.txt /home/locust/
RUN pip install -r /home/locust/requirements.txt

COPY src/ /home/locust/src/
COPY data/ /home/locust/data/
COPY locust.conf /home/locust/

WORKDIR /home/locust
```

```yaml
# docker-compose.yml - Cluster distribuido
version: '3.8'

services:
  master:
    image: locustio/locust:2.29.1
    ports:
      - "8089:8089"
    volumes:
      - ./src:/home/locust/src
      - ./data:/home/locust/data
    command: >
      -f /home/locust/src/locustfile.py
      --master
      --host https://api.example.com
      --expect-workers 4

  worker:
    image: locustio/locust:2.29.1
    volumes:
      - ./src:/home/locust/src
      - ./data:/home/locust/data
    command: >
      -f /home/locust/src/locustfile.py
      --worker
      --master-host master
    deploy:
      replicas: 4
    depends_on:
      - master
```

---

## 3. Arquitectura Interna

### Modelo de concurrencia

```
┌─────────────────────────────────────────────────────────────────┐
│                    LOCUST ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    GEVENT EVENT LOOP                      │    │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐     ┌─────────┐  │    │
│  │  │Greenlet │ │Greenlet │ │Greenlet │ ... │Greenlet │  │    │
│  │  │ User 1  │ │ User 2  │ │ User 3  │     │ User N  │  │    │
│  │  └─────────┘ └─────────┘ └─────────┘     └─────────┘  │    │
│  │                                                          │    │
│  │  Cooperative multitasking (yield on I/O)                │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌───────────────┐  ┌───────────────┐  ┌──────────────────┐    │
│  │ Stats Engine  │  │ Event System  │  │  Web UI (Flask)  │    │
│  │ (aggregation) │  │   (hooks)     │  │   Port 8089      │    │
│  └───────────────┘  └───────────────┘  └──────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Greenlets vs Threads

```python
# Cada usuario es un greenlet (coroutine cooperativa)
# NO es un thread del OS → muy bajo overhead de memoria

# Un greenlet ocupa ~4-8 KB (vs ~1 MB de un thread)
# 10,000 usuarios = ~80 MB RAM (solo greenlets)

# IMPORTANTE: Cooperative scheduling
# El greenlet SOLO cede control cuando hace I/O (network, sleep)
# Código CPU-bound bloqueará TODOS los greenlets
```

### Flujo de ejecución de un usuario

```
User.on_start()
    │
    ▼
┌─── Loop ────────────────────────────────┐
│                                          │
│  1. Seleccionar task (random weighted)   │
│  2. Ejecutar task                        │
│  3. Aplicar wait_time                    │
│  4. Repetir                              │
│                                          │
└──────────────────────────────────────────┘
    │
    ▼ (cuando Locust para el usuario)
User.on_stop()
```

### Arquitectura distribuida

```
┌─────────────────────────────────────────────────────────────────┐
│                    DISTRIBUTED MODE                               │
│                                                                   │
│  ┌──────────────────────┐          ┌──────────────────────┐     │
│  │       MASTER         │  ZeroMQ  │      WORKER 1        │     │
│  │                      │◄────────►│                      │     │
│  │ • Web UI             │          │ • Runs N users       │     │
│  │ • Stats aggregation  │          │ • Reports stats      │     │
│  │ • User distribution  │          │ • Executes tasks     │     │
│  │ • Test coordination  │          └──────────────────────┘     │
│  │                      │                                        │
│  │                      │  ZeroMQ  ┌──────────────────────┐     │
│  │                      │◄────────►│      WORKER 2        │     │
│  │                      │          └──────────────────────┘     │
│  │                      │                                        │
│  │                      │  ZeroMQ  ┌──────────────────────┐     │
│  │                      │◄────────►│      WORKER N        │     │
│  └──────────────────────┘          └──────────────────────┘     │
│                                                                   │
│  Comunicación: ZeroMQ (tcp://master:5557, tcp://master:5558)     │
│  Worker → Master: stats cada 3 segundos (configurable)           │
│  Master → Worker: spawn/stop commands                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Fundamentos del Locustfile

### Estructura mínima

```python
from locust import HttpUser, task

class MyUser(HttpUser):
    @task
    def my_task(self):
        self.client.get("/api/health")
```

### Estructura completa de producción

```python
"""
Performance Test: E-Commerce API
Author: Performance Team
Version: 2.1.0
"""

import os
import json
import random
import logging
from datetime import datetime

from locust import HttpUser, task, between, tag, events
from locust.runners import MasterRunner, WorkerRunner

# Configuración
logger = logging.getLogger(__name__)
BASE_URL = os.getenv("TARGET_HOST", "https://api.staging.example.com")

# Datos compartidos (cargados una vez)
PRODUCTS = []
USERS_DATA = []


@events.init.add_listener
def on_locust_init(environment, **kwargs):
    """Se ejecuta al iniciar Locust (antes de los tests)."""
    global PRODUCTS, USERS_DATA
    
    # Solo cargar datos en master o standalone
    if isinstance(environment.runner, WorkerRunner):
        return
    
    logger.info("Loading test data...")
    with open("data/products.json") as f:
        PRODUCTS = json.load(f)
    with open("data/users.json") as f:
        USERS_DATA = json.load(f)
    logger.info(f"Loaded {len(PRODUCTS)} products, {len(USERS_DATA)} users")


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Se ejecuta cuando inicia el test."""
    logger.info(f"Test starting at {datetime.now().isoformat()}")
    logger.info(f"Target host: {environment.host}")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Se ejecuta cuando termina el test."""
    logger.info(f"Test completed at {datetime.now().isoformat()}")
    stats = environment.runner.stats
    logger.info(f"Total requests: {stats.total.num_requests}")
    logger.info(f"Total failures: {stats.total.num_failures}")


class ECommerceUser(HttpUser):
    """Usuario típico de e-commerce que navega, busca y compra."""
    
    host = BASE_URL
    wait_time = between(1, 5)
    
    # Atributos de instancia
    token = None
    cart_id = None
    
    def on_start(self):
        """Login al iniciar el usuario virtual."""
        user_data = random.choice(USERS_DATA)
        response = self.client.post(
            "/api/v1/auth/login",
            json={"email": user_data["email"], "password": user_data["password"]},
            name="/api/v1/auth/login"
        )
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            self.client.headers.update({
                "Authorization": f"Bearer {self.token}"
            })
        else:
            logger.warning(f"Login failed for {user_data['email']}: {response.status_code}")
    
    def on_stop(self):
        """Logout al terminar el usuario virtual."""
        if self.token:
            self.client.post("/api/v1/auth/logout", name="/api/v1/auth/logout")
    
    @task(10)
    @tag("browse", "read")
    def browse_catalog(self):
        """Navegar catálogo de productos."""
        page = random.randint(1, 20)
        self.client.get(
            f"/api/v1/products?page={page}&limit=20",
            name="/api/v1/products?page=[N]"
        )
    
    @task(5)
    @tag("search", "read")
    def search_products(self):
        """Buscar productos."""
        terms = ["laptop", "phone", "headphones", "tablet", "watch"]
        query = random.choice(terms)
        self.client.get(
            f"/api/v1/search?q={query}&sort=relevance",
            name="/api/v1/search?q=[term]"
        )
    
    @task(3)
    @tag("detail", "read")
    def view_product_detail(self):
        """Ver detalle de un producto."""
        if PRODUCTS:
            product = random.choice(PRODUCTS)
            self.client.get(
                f"/api/v1/products/{product['id']}",
                name="/api/v1/products/[id]"
            )
    
    @task(2)
    @tag("cart", "write")
    def add_to_cart(self):
        """Agregar producto al carrito."""
        if PRODUCTS:
            product = random.choice(PRODUCTS)
            response = self.client.post(
                "/api/v1/cart/items",
                json={"product_id": product["id"], "quantity": random.randint(1, 3)},
                name="/api/v1/cart/items [POST]"
            )
            if response.status_code == 201:
                self.cart_id = response.json().get("cart_id")
    
    @task(1)
    @tag("checkout", "write", "critical")
    def checkout(self):
        """Proceso de checkout (flujo completo)."""
        if not self.cart_id:
            # Primero agregar algo al carrito
            self.add_to_cart()
        
        if self.cart_id:
            # Checkout
            response = self.client.post(
                "/api/v1/checkout",
                json={
                    "cart_id": self.cart_id,
                    "payment_method": "test_card",
                    "shipping_address_id": "addr_default"
                },
                name="/api/v1/checkout [POST]"
            )
            if response.status_code in (200, 201):
                self.cart_id = None  # Reset cart after successful checkout
```

---

## 5. User Classes en Profundidad

### Jerarquía de User Classes

```
User (base abstracta)
├── HttpUser (HTTP/HTTPS via requests)
├── FastHttpUser (HTTP de alto rendimiento via geventhttpclient)
└── Custom User (cualquier protocolo)
```

### Múltiples User Types

```python
from locust import HttpUser, task, between, constant

class WebUser(HttpUser):
    """Usuarios web browsing - 70% del tráfico."""
    weight = 7
    wait_time = between(2, 8)
    
    @task(5)
    def browse(self):
        self.client.get("/api/products")
    
    @task(2)
    def search(self):
        self.client.get("/api/search?q=test")
    
    @task(1)
    def view_profile(self):
        self.client.get("/api/profile")


class MobileUser(HttpUser):
    """Usuarios mobile - 25% del tráfico."""
    weight = 25
    wait_time = between(3, 15)  # Mobile users son más lentos
    
    def on_start(self):
        self.client.headers.update({
            "User-Agent": "MobileApp/3.2.1 (iOS 17.0)",
            "X-Platform": "ios",
            "X-App-Version": "3.2.1"
        })
    
    @task(8)
    def browse_feed(self):
        self.client.get("/api/v2/feed?limit=10")
    
    @task(2)
    def sync_data(self):
        self.client.post("/api/v2/sync", json={"last_sync": "2024-01-01T00:00:00Z"})


class APIIntegrationUser(HttpUser):
    """Integraciones B2B API - 5% del tráfico."""
    weight = 5
    wait_time = constant(1)  # APIs automáticas, ritmo constante
    
    def on_start(self):
        self.client.headers.update({
            "X-API-Key": "test-api-key-12345",
            "Content-Type": "application/json"
        })
    
    @task
    def batch_query(self):
        self.client.post("/api/v1/batch", json={
            "queries": [{"id": i} for i in range(10)]
        })


class AdminUser(HttpUser):
    """Admin - siempre exactamente 1 usuario."""
    fixed_count = 1  # Ignora weight, siempre 1 instancia
    wait_time = constant(60)  # Una acción por minuto
    
    @task
    def check_dashboard(self):
        self.client.get("/admin/api/dashboard/stats")
    
    @task
    def export_report(self):
        self.client.get("/admin/api/reports/daily")
```

### Herencia de User Classes

```python
from locust import HttpUser, task, between
import json

class BaseAuthenticatedUser(HttpUser):
    """Base class con autenticación compartida."""
    abstract = True  # No instanciar directamente
    
    token = None
    
    def on_start(self):
        resp = self.client.post("/api/auth/token", json={
            "client_id": "load_test",
            "client_secret": "secret123"
        })
        if resp.ok:
            self.token = resp.json()["access_token"]
            self.client.headers["Authorization"] = f"Bearer {self.token}"
    
    def authenticated_get(self, path, **kwargs):
        """Helper para GET autenticado con refresh automático."""
        resp = self.client.get(path, **kwargs)
        if resp.status_code == 401:
            self.on_start()  # Refresh token
            resp = self.client.get(path, **kwargs)
        return resp


class ReadOnlyUser(BaseAuthenticatedUser):
    """Usuario que solo lee datos."""
    weight = 8
    wait_time = between(1, 3)
    
    @task
    def read_data(self):
        self.authenticated_get("/api/data")


class ReadWriteUser(BaseAuthenticatedUser):
    """Usuario que lee y escribe."""
    weight = 2
    wait_time = between(2, 5)
    
    @task(3)
    def read_data(self):
        self.authenticated_get("/api/data")
    
    @task(1)
    def write_data(self):
        self.client.post("/api/data", json={"value": "test"})
```

---

## 6. Tasks y Control de Flujo

### TaskSets (Agrupación de tareas)

```python
from locust import HttpUser, TaskSet, task, between, SequentialTaskSet

class BrowsingTasks(TaskSet):
    """Conjunto de tareas de navegación."""
    
    @task(5)
    def view_homepage(self):
        self.client.get("/")
    
    @task(3)
    def view_category(self):
        self.client.get("/category/electronics")
    
    @task(1)
    def stop_browsing(self):
        self.interrupt()  # Volver al parent (User o TaskSet padre)


class PurchaseTasks(TaskSet):
    """Conjunto de tareas de compra."""
    
    @task(3)
    def add_to_cart(self):
        self.client.post("/cart/add", json={"item": 1})
    
    @task(1)
    def checkout(self):
        self.client.post("/checkout")
        self.interrupt()  # Compra completa, volver


class ShoppingUser(HttpUser):
    wait_time = between(1, 5)
    tasks = {BrowsingTasks: 7, PurchaseTasks: 3}  # 70% browsing, 30% purchase
```

### SequentialTaskSet (Tareas en orden)

```python
from locust import HttpUser, SequentialTaskSet, task, between

class CheckoutFlow(SequentialTaskSet):
    """Flujo de checkout ejecutado en orden estricto."""
    
    @task
    def add_items(self):
        """Paso 1: Agregar items al carrito."""
        for _ in range(3):
            self.client.post("/api/cart/items", json={
                "product_id": random.randint(1, 100),
                "quantity": 1
            })
    
    @task
    def view_cart(self):
        """Paso 2: Ver carrito."""
        resp = self.client.get("/api/cart")
        self.cart_total = resp.json().get("total", 0)
    
    @task
    def apply_coupon(self):
        """Paso 3: Aplicar cupón (50% probabilidad)."""
        if random.random() > 0.5:
            self.client.post("/api/cart/coupon", json={"code": "SAVE10"})
    
    @task
    def enter_shipping(self):
        """Paso 4: Dirección de envío."""
        self.client.post("/api/checkout/shipping", json={
            "address": "123 Test St",
            "city": "Test City",
            "zip": "12345"
        })
    
    @task
    def submit_payment(self):
        """Paso 5: Pago."""
        self.client.post("/api/checkout/payment", json={
            "method": "credit_card",
            "card_token": "tok_test_visa"
        })
    
    @task
    def confirm_order(self):
        """Paso 6: Confirmar y finalizar."""
        self.client.post("/api/checkout/confirm")
        self.interrupt()  # Volver al User


class ECommerceUser(HttpUser):
    wait_time = between(2, 5)
    tasks = [CheckoutFlow]
```

### Control de flujo condicional

```python
from locust import HttpUser, task, between
import random

class ConditionalUser(HttpUser):
    wait_time = between(1, 3)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Estado del usuario
        self.is_logged_in = False
        self.cart_items = 0
        self.session_pages_viewed = 0
    
    @task(10)
    def browse(self):
        """Siempre puede navegar."""
        self.client.get("/products")
        self.session_pages_viewed += 1
        
        # Después de ver 5 páginas, 30% probabilidad de login
        if not self.is_logged_in and self.session_pages_viewed > 5:
            if random.random() < 0.3:
                self._login()
    
    @task(3)
    def add_to_cart(self):
        """Solo si está logueado."""
        if not self.is_logged_in:
            return  # Skip silenciosamente
        
        resp = self.client.post("/cart/add", json={"product_id": random.randint(1, 50)})
        if resp.ok:
            self.cart_items += 1
    
    @task(1)
    def checkout(self):
        """Solo si tiene items en el carrito."""
        if self.cart_items == 0:
            return
        
        resp = self.client.post("/checkout", json={"confirm": True})
        if resp.ok:
            self.cart_items = 0
    
    def _login(self):
        resp = self.client.post("/login", json={"user": "test", "pass": "test"})
        if resp.ok:
            self.is_logged_in = True
```

---

## 7. HTTP Client y Validaciones

### Métodos HTTP disponibles

```python
from locust import HttpUser, task

class APIUser(HttpUser):
    
    @task
    def all_http_methods(self):
        # GET
        self.client.get("/api/resources")
        
        # POST
        self.client.post("/api/resources", json={"name": "test"})
        
        # PUT
        self.client.put("/api/resources/1", json={"name": "updated"})
        
        # PATCH
        self.client.patch("/api/resources/1", json={"name": "patched"})
        
        # DELETE
        self.client.delete("/api/resources/1")
        
        # HEAD
        self.client.head("/api/resources")
        
        # OPTIONS
        self.client.options("/api/resources")
```

### Validación de respuestas (Response assertions)

```python
from locust import HttpUser, task

class ValidatingUser(HttpUser):
    
    @task
    def validated_request(self):
        # Método 1: catch_response=True para control manual
        with self.client.get("/api/data", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                
                # Validar estructura
                if "items" not in data:
                    response.failure("Missing 'items' key in response")
                elif len(data["items"]) == 0:
                    response.failure("Empty items list")
                elif data["items"][0].get("id") is None:
                    response.failure("Item missing 'id' field")
                else:
                    response.success()
            elif response.status_code == 429:
                # Rate limited - no contar como falla
                response.failure("Rate limited (429)")
            else:
                response.failure(f"Unexpected status: {response.status_code}")
    
    @task
    def validate_performance(self):
        """Marcar como falla si latencia excede umbral."""
        with self.client.get("/api/fast-endpoint", catch_response=True) as response:
            if response.elapsed.total_seconds() > 1.0:
                response.failure(f"Too slow: {response.elapsed.total_seconds():.2f}s")
            elif response.status_code != 200:
                response.failure(f"Status {response.status_code}")
            else:
                response.success()
    
    @task
    def validate_json_schema(self):
        """Validar schema JSON de la respuesta."""
        with self.client.get("/api/user/profile", catch_response=True) as response:
            if response.ok:
                data = response.json()
                required_fields = ["id", "email", "name", "created_at"]
                missing = [f for f in required_fields if f not in data]
                if missing:
                    response.failure(f"Missing fields: {missing}")
                else:
                    response.success()
```

### Request grouping (name parameter)

```python
from locust import HttpUser, task

class GroupingUser(HttpUser):
    
    @task
    def dynamic_urls(self):
        """Agrupar URLs dinámicas bajo un solo nombre en stats."""
        
        # SIN name → cada URL es una entrada separada en stats
        # /api/products/1, /api/products/2, ... (miles de entradas)
        
        # CON name → una sola entrada
        product_id = random.randint(1, 10000)
        self.client.get(
            f"/api/products/{product_id}",
            name="/api/products/[id]"  # Agrupado
        )
        
        # Para queries con parámetros variables
        page = random.randint(1, 100)
        category = random.choice(["electronics", "books", "clothing"])
        self.client.get(
            f"/api/search?category={category}&page={page}&sort=price",
            name="/api/search?category=[cat]&page=[n]"
        )
```

### Manejo de cookies y sesión

```python
from locust import HttpUser, task

class SessionUser(HttpUser):
    
    def on_start(self):
        # Las cookies se manejan automáticamente por sesión HTTP
        # Cada User instance tiene su propia sesión (cookies independientes)
        self.client.post("/login", data={
            "username": "user@test.com",
            "password": "password123"
        })
        # La cookie de sesión se almacena automáticamente
    
    @task
    def access_protected(self):
        # La cookie de sesión se envía automáticamente
        self.client.get("/dashboard")
    
    @task
    def manual_cookies(self):
        # Acceso manual a cookies si necesario
        cookies = self.client.cookies
        session_id = cookies.get("session_id")
        
        # Enviar cookie custom
        self.client.get("/api/data", cookies={"custom": "value"})
```

### File uploads y multipart

```python
from locust import HttpUser, task
import io

class UploadUser(HttpUser):
    
    @task
    def upload_file(self):
        """Subir archivo."""
        # Generar archivo en memoria
        file_content = b"x" * 1024 * 100  # 100KB
        files = {
            "file": ("test_document.pdf", io.BytesIO(file_content), "application/pdf")
        }
        
        self.client.post(
            "/api/upload",
            files=files,
            data={"description": "Load test file"},
            name="/api/upload [POST]"
        )
    
    @task
    def upload_multiple(self):
        """Subir múltiples archivos."""
        files = [
            ("files", ("image1.jpg", io.BytesIO(b"fake_jpg_1"), "image/jpeg")),
            ("files", ("image2.jpg", io.BytesIO(b"fake_jpg_2"), "image/jpeg")),
        ]
        self.client.post("/api/gallery/upload", files=files)
```

---

## 8. Wait Times y Pacing

### Tipos de wait_time

```python
from locust import HttpUser, task
from locust import between, constant, constant_pacing, constant_throughput

class ConstantWaitUser(HttpUser):
    """Espera fija entre tareas."""
    wait_time = constant(2)  # Siempre 2 segundos entre tasks


class RandomWaitUser(HttpUser):
    """Espera aleatoria entre min y max."""
    wait_time = between(1, 10)  # 1 a 10 segundos


class ThroughputUser(HttpUser):
    """Garantizar N ejecuciones por segundo por usuario."""
    # Cada usuario ejecuta máximo 2 tasks/segundo
    # Si el task tarda 300ms, espera 200ms adicionales
    # Si el task tarda 600ms, NO espera (ya excedió el 500ms budget)
    wait_time = constant_throughput(2)  # 2 tasks/sec/user


class PacingUser(HttpUser):
    """Garantizar un task cada N segundos."""
    # Un task cada 5 segundos (independiente de cuánto dure el task)
    # Si task dura 1s → espera 4s
    # Si task dura 4s → espera 1s
    # Si task dura 6s → NO espera (ya excedió los 5s)
    wait_time = constant_pacing(5)  # 1 task cada 5 sec/user
```

### Wait time custom

```python
from locust import HttpUser, task
import random
import math

class CustomWaitUser(HttpUser):
    """Wait time personalizado con distribución realista."""
    
    _iteration = 0
    
    def wait_time(self):
        """Distribución log-normal (más realista que uniform)."""
        # Media ~3s, con cola larga (algunos users piensan mucho más)
        return random.lognormvariate(math.log(3), 0.5)


class RampingWaitUser(HttpUser):
    """Wait time que decrece con el tiempo (usuarios se impacientan)."""
    
    _start_time = None
    
    def wait_time(self):
        import time
        if self._start_time is None:
            self._start_time = time.time()
        
        elapsed_minutes = (time.time() - self._start_time) / 60
        # Empieza en 5s, baja a 1s después de 10 minutos
        base_wait = max(1.0, 5.0 - (elapsed_minutes * 0.4))
        return base_wait + random.uniform(0, 1)
```

### Cálculo de throughput total

```
Throughput total = Número de usuarios / (task_duration + wait_time)

Ejemplo con constant_throughput(2):
  - 100 usuarios × 2 tasks/sec = 200 requests/segundo (máximo)
  
Ejemplo con between(1, 5):
  - wait_time promedio = 3s
  - task_duration promedio = 0.5s
  - 100 usuarios / (0.5 + 3.0) = ~28.5 requests/segundo

Ejemplo con constant_pacing(5):
  - 100 usuarios, 1 task cada 5s = 20 requests/segundo (constante)
  - Independiente de la latencia del servidor (hasta 5s)
```

---

## 9. Custom Load Shapes

### Concepto

Custom Load Shapes permiten definir perfiles de carga complejos (no solo ramp-up lineal) programáticamente.

### Spike Test Shape

```python
from locust import LoadTestShape, HttpUser, task, between

class SpikeShape(LoadTestShape):
    """
    Spike test: carga normal → pico súbito → carga normal.
    
    Timeline:
    0-2min:  50 users (baseline)
    2-3min:  500 users (spike up)
    3-5min:  500 users (sustained spike)
    5-6min:  50 users (spike down)
    6-8min:  50 users (recovery verification)
    """
    
    stages = [
        {"duration": 120, "users": 50, "spawn_rate": 10},    # Baseline
        {"duration": 180, "users": 500, "spawn_rate": 100},  # Spike up
        {"duration": 300, "users": 500, "spawn_rate": 100},  # Sustained
        {"duration": 360, "users": 50, "spawn_rate": 100},   # Spike down
        {"duration": 480, "users": 50, "spawn_rate": 10},    # Recovery
    ]
    
    def tick(self):
        run_time = self.get_run_time()
        
        for stage in self.stages:
            if run_time < stage["duration"]:
                return (stage["users"], stage["spawn_rate"])
        
        return None  # Test complete
```

### Step Load Shape (Escalera)

```python
class StepLoadShape(LoadTestShape):
    """
    Step load: incrementar usuarios en escalones.
    Útil para encontrar el punto de quiebre.
    
    Cada escalón dura 3 minutos:
    Step 1: 50 users
    Step 2: 100 users
    Step 3: 150 users
    ...
    Step N: hasta max_users
    """
    
    step_duration = 180  # 3 minutos por escalón
    step_increment = 50  # +50 users por escalón
    max_users = 500
    spawn_rate = 20
    
    def tick(self):
        run_time = self.get_run_time()
        current_step = int(run_time // self.step_duration) + 1
        current_users = min(current_step * self.step_increment, self.max_users)
        
        if current_users > self.max_users:
            return None  # Fin del test
        
        return (current_users, self.spawn_rate)
```

### Double Wave Shape (Onda doble - simula mañana y tarde)

```python
import math

class DoubleWaveShape(LoadTestShape):
    """
    Simula patrón de tráfico real: dos picos (mañana y tarde).
    
    Útil para soak tests de ~8 horas comprimidas en minutos.
    """
    
    min_users = 20
    max_users = 300
    total_duration = 1800  # 30 minutos (simula 1 día)
    
    def tick(self):
        run_time = self.get_run_time()
        
        if run_time > self.total_duration:
            return None
        
        # Dos ondas sinusoidales (2 picos en el período)
        progress = run_time / self.total_duration
        wave = math.sin(progress * 2 * math.pi * 2)  # 2 ciclos completos
        
        # Normalizar a rango [min_users, max_users]
        amplitude = (self.max_users - self.min_users) / 2
        center = self.min_users + amplitude
        users = int(center + amplitude * wave)
        
        # Spawn rate proporcional al cambio
        spawn_rate = max(5, abs(users - self.get_current_user_count()) // 2 + 1)
        
        return (max(users, self.min_users), spawn_rate)
```

### Ramp-Up-Hold-Ramp-Down (Patrón clásico)

```python
class ClassicLoadShape(LoadTestShape):
    """
    Patrón clásico de load test:
    - Ramp up gradual
    - Hold at target
    - Ramp down gradual
    """
    
    target_users = 200
    ramp_up_duration = 300     # 5 min ramp up
    hold_duration = 1800       # 30 min hold
    ramp_down_duration = 120   # 2 min ramp down
    spawn_rate = 5
    
    def tick(self):
        run_time = self.get_run_time()
        total = self.ramp_up_duration + self.hold_duration + self.ramp_down_duration
        
        if run_time > total:
            return None
        
        if run_time <= self.ramp_up_duration:
            # Ramp up
            progress = run_time / self.ramp_up_duration
            users = int(self.target_users * progress)
            return (max(1, users), self.spawn_rate)
        
        elif run_time <= self.ramp_up_duration + self.hold_duration:
            # Hold
            return (self.target_users, self.spawn_rate)
        
        else:
            # Ramp down
            elapsed_ramp_down = run_time - self.ramp_up_duration - self.hold_duration
            progress = elapsed_ramp_down / self.ramp_down_duration
            users = int(self.target_users * (1 - progress))
            return (max(1, users), self.spawn_rate)
```

### Shape basada en datos externos (CSV/API)

```python
import csv

class DataDrivenShape(LoadTestShape):
    """Cargar perfil de carga desde un CSV (datos de producción)."""
    
    def __init__(self):
        super().__init__()
        self.load_profile = self._load_profile("data/traffic_profile.csv")
    
    def _load_profile(self, filepath):
        """Leer perfil: timestamp_offset_seconds, target_users"""
        profile = []
        with open(filepath) as f:
            reader = csv.DictReader(f)
            for row in reader:
                profile.append({
                    "time": int(row["seconds"]),
                    "users": int(row["users"])
                })
        return sorted(profile, key=lambda x: x["time"])
    
    def tick(self):
        run_time = self.get_run_time()
        
        # Encontrar el punto en el perfil
        current_users = self.load_profile[0]["users"]
        for point in self.load_profile:
            if run_time >= point["time"]:
                current_users = point["users"]
            else:
                break
        
        # Si pasamos el último punto, terminar
        if run_time > self.load_profile[-1]["time"]:
            return None
        
        return (current_users, max(5, current_users // 10))
```

---

## 10. Modo Distribuido

### Configuración Master-Worker

```bash
# Terminal 1: Master
locust -f locustfile.py --master --host https://api.example.com

# Terminal 2-N: Workers
locust -f locustfile.py --worker --master-host 192.168.1.100
locust -f locustfile.py --worker --master-host 192.168.1.100
locust -f locustfile.py --worker --master-host 192.168.1.100

# Master con expectativa de workers
locust -f locustfile.py --master --expect-workers 4
# (el test no inicia hasta que los 4 workers se conecten)
```

### Kubernetes Deployment

```yaml
# locust-master.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: locust-master
  labels:
    app: locust
    role: master
spec:
  replicas: 1
  selector:
    matchLabels:
      app: locust
      role: master
  template:
    metadata:
      labels:
        app: locust
        role: master
    spec:
      containers:
        - name: locust
          image: myregistry/locust-tests:latest
          ports:
            - containerPort: 8089  # Web UI
            - containerPort: 5557  # Worker comm
            - containerPort: 5558  # Worker comm
          command: ["locust"]
          args:
            - "-f"
            - "/tests/locustfile.py"
            - "--master"
            - "--expect-workers"
            - "8"
            - "--host"
            - "https://api.target.com"
          resources:
            requests:
              cpu: "500m"
              memory: "512Mi"
            limits:
              cpu: "1000m"
              memory: "1Gi"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: locust-worker
  labels:
    app: locust
    role: worker
spec:
  replicas: 8
  selector:
    matchLabels:
      app: locust
      role: worker
  template:
    metadata:
      labels:
        app: locust
        role: worker
    spec:
      containers:
        - name: locust
          image: myregistry/locust-tests:latest
          command: ["locust"]
          args:
            - "-f"
            - "/tests/locustfile.py"
            - "--worker"
            - "--master-host"
            - "locust-master"
          resources:
            requests:
              cpu: "1000m"
              memory: "1Gi"
            limits:
              cpu: "2000m"
              memory: "2Gi"
---
apiVersion: v1
kind: Service
metadata:
  name: locust-master
spec:
  selector:
    app: locust
    role: master
  ports:
    - name: web
      port: 8089
    - name: worker1
      port: 5557
    - name: worker2
      port: 5558
  type: LoadBalancer
```

### Compartir datos entre Master y Workers

```python
from locust import HttpUser, task, events, between
from locust.runners import MasterRunner, WorkerRunner
import json

# Datos compartidos - distribuidos del master a los workers
test_data = {"users": [], "products": []}

@events.init.add_listener
def on_init(environment, **kwargs):
    """Distribuir datos: Master carga, Workers reciben."""
    
    if isinstance(environment.runner, MasterRunner):
        # Master: cargar datos y enviar a workers via custom message
        with open("data/test_users.json") as f:
            test_data["users"] = json.load(f)
        
        @environment.runner.register_message("test_data")
        def on_worker_ready(msg, **kw):
            pass  # Workers no envían datos al master aquí
        
        # Cuando un worker se conecta, enviarle los datos
        def send_data_to_worker(client_id, **kwargs):
            environment.runner.send_message(
                "test_data_distribution",
                {"users": test_data["users"]},
                client_id=client_id
            )
        
        environment.runner.greenlet.spawn(
            lambda: [send_data_to_worker(w.id) 
                     for w in environment.runner.clients.values()]
        )
    
    elif isinstance(environment.runner, WorkerRunner):
        # Worker: registrar handler para recibir datos
        @environment.runner.register_message("test_data_distribution")
        def on_data_received(msg, **kw):
            test_data["users"] = msg.data["users"]
            print(f"Worker received {len(test_data['users'])} users")
```

### Escalado de workers

```
Regla de dedo para dimensionar workers:

┌──────────────────────────────────────────────────────────┐
│ Usuarios objetivo │ Workers recomendados │ vCPU/Worker   │
├────────────────────┼──────────────────────┼──────────────┤
│ 100 - 500         │ 1                    │ 2 vCPU       │
│ 500 - 2,000       │ 2-4                  │ 2 vCPU       │
│ 2,000 - 10,000    │ 4-8                  │ 4 vCPU       │
│ 10,000 - 50,000   │ 8-20                 │ 4 vCPU       │
│ 50,000+           │ 20+                  │ 4-8 vCPU     │
└──────────────────────────────────────────────────────────┘

* FastHttpUser puede manejar 2-5x más users por worker
* Reducir si tasks tienen lógica CPU-heavy (cálculos, parsing)
* Monitorear CPU del worker: si > 80%, agregar workers
```

---

## 11. Event Hooks y Extensibilidad

### Sistema de eventos

```python
from locust import events, HttpUser, task
import time
import json

# ─────────────────────────────────────────────────────────
# LIFECYCLE EVENTS
# ─────────────────────────────────────────────────────────

@events.init.add_listener
def on_init(environment, **kwargs):
    """Locust se inicializa (antes de todo)."""
    print("Locust initialized")

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """El test comienza (usuarios empiezan a spawnearse)."""
    print(f"Test starting with {environment.runner.target_user_count} target users")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """El test termina."""
    print("Test stopped")

@events.spawning_complete.add_listener
def on_spawning_complete(user_count, **kwargs):
    """Todos los usuarios se han creado."""
    print(f"All {user_count} users spawned")

@events.quitting.add_listener
def on_quitting(environment, **kwargs):
    """Locust se está cerrando."""
    print("Locust quitting...")

# ─────────────────────────────────────────────────────────
# REQUEST EVENTS
# ─────────────────────────────────────────────────────────

@events.request.add_listener
def on_request(request_type, name, response_time, response_length, 
               response, context, exception, **kwargs):
    """Se ejecuta después de CADA request."""
    if exception:
        print(f"FAILED: {request_type} {name} - {exception}")
    elif response_time > 5000:  # > 5 segundos
        print(f"SLOW: {request_type} {name} - {response_time}ms")

# ─────────────────────────────────────────────────────────
# USER EVENTS
# ─────────────────────────────────────────────────────────

@events.user_error.add_listener
def on_user_error(user_instance, exception, tb, **kwargs):
    """Error no manejado en un usuario."""
    print(f"User error: {type(exception).__name__}: {exception}")
```

### Custom metrics reporting

```python
from locust import events
import time
import requests

# Enviar métricas a InfluxDB en tiempo real
INFLUX_URL = "http://influxdb:8086/write?db=locust"

@events.request.add_listener
def report_to_influxdb(request_type, name, response_time, response_length,
                       response, context, exception, **kwargs):
    """Enviar cada request a InfluxDB para dashboards Grafana."""
    
    success = 1 if exception is None else 0
    status_code = response.status_code if response else 0
    
    # Line protocol de InfluxDB
    line = (
        f"locust_requests,"
        f"method={request_type},"
        f"endpoint={name.replace(' ', '\\ ')},"
        f"status={status_code} "
        f"response_time={response_time},"
        f"response_length={response_length or 0},"
        f"success={success} "
        f"{int(time.time() * 1e9)}"  # nanosecond timestamp
    )
    
    try:
        requests.post(INFLUX_URL, data=line, timeout=1)
    except Exception:
        pass  # No fallar el test por problemas de reporting


# Enviar stats agregados cada 5 segundos
@events.init.add_listener
def setup_periodic_stats(environment, **kwargs):
    """Reportar stats agregados periódicamente."""
    import gevent
    
    def report_stats():
        while True:
            gevent.sleep(5)
            stats = environment.runner.stats
            
            for entry in stats.entries.values():
                line = (
                    f"locust_aggregated,"
                    f"endpoint={entry.name.replace(' ', '\\ ')} "
                    f"num_requests={entry.num_requests},"
                    f"num_failures={entry.num_failures},"
                    f"avg_response_time={entry.avg_response_time:.2f},"
                    f"p50={entry.get_response_time_percentile(0.5) or 0},"
                    f"p95={entry.get_response_time_percentile(0.95) or 0},"
                    f"p99={entry.get_response_time_percentile(0.99) or 0},"
                    f"current_rps={entry.current_rps:.2f}"
                )
                try:
                    requests.post(INFLUX_URL, data=line, timeout=1)
                except Exception:
                    pass
    
    if not isinstance(environment.runner, WorkerRunner):
        gevent.spawn(report_stats)
```

### Custom arguments

```python
from locust import events

@events.init_command_line_parser.add_listener
def add_custom_arguments(parser, **kwargs):
    """Agregar argumentos custom al CLI de Locust."""
    parser.add_argument(
        "--api-token",
        type=str,
        env_var="API_TOKEN",
        default="",
        help="API token for authentication"
    )
    parser.add_argument(
        "--test-environment",
        type=str,
        choices=["dev", "staging", "production"],
        default="staging",
        help="Target test environment"
    )
    parser.add_argument(
        "--think-time-factor",
        type=float,
        default=1.0,
        help="Multiply think times by this factor (0.5 = faster, 2.0 = slower)"
    )

# Uso en el User class:
class MyUser(HttpUser):
    def on_start(self):
        token = self.environment.parsed_options.api_token
        self.client.headers["Authorization"] = f"Bearer {token}"
```

---

## 12. FastHttpUser (Alto Rendimiento)

### ¿Qué es FastHttpUser?

`FastHttpUser` usa `geventhttpclient` en lugar de `requests`, ofreciendo 5-6x mejor rendimiento al costo de menos features (no soporta todas las opciones de `requests`).

```python
from locust import task, between
from locust.contrib.fasthttp import FastHttpUser

class HighPerformanceUser(FastHttpUser):
    """Usar cuando necesitas máximo throughput por worker."""
    
    wait_time = between(0.1, 0.5)
    
    # Configuración de connection pooling
    connection_timeout = 5.0
    network_timeout = 10.0
    max_retries = 0  # No reintentar (para medir latencia real)
    
    @task(10)
    def fast_read(self):
        # API idéntica a HttpUser para requests simples
        self.client.get("/api/fast-endpoint")
    
    @task(3)
    def fast_post(self):
        self.client.post("/api/data", json={"key": "value"})
    
    @task(1)
    def with_validation(self):
        with self.client.get("/api/check", catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure(f"Got {resp.status_code}")
```

### Comparación HttpUser vs FastHttpUser

```
┌─────────────────────┬───────────────────┬────────────────────┐
│ Característica      │ HttpUser          │ FastHttpUser       │
├─────────────────────┼───────────────────┼────────────────────┤
│ Library             │ requests          │ geventhttpclient   │
│ Performance         │ ~1,500 req/s      │ ~8,000 req/s       │
│ Memory per user     │ ~50 KB            │ ~20 KB             │
│ HTTP/2              │ No                │ No                 │
│ Connection pooling  │ Sí                │ Sí (más eficiente) │
│ Cookies             │ Automático        │ Automático         │
│ File upload         │ Completo          │ Limitado           │
│ Redirects           │ Automático        │ Manual             │
│ Auth (digest, etc)  │ Completo          │ Solo Basic/Bearer  │
│ catch_response      │ Sí                │ Sí                 │
│ Proxy support       │ Sí                │ Limitado           │
└─────────────────────┴───────────────────┴────────────────────┘

Regla: Usar FastHttpUser cuando:
  - Necesitas > 3,000 req/s por worker
  - Solo haces GET/POST simples con JSON
  - No necesitas features avanzadas de requests
```

---

## 13. Testing de Protocolos No-HTTP

### gRPC Testing

```python
from locust import User, task, between, events
import grpc
import time

# Importar protobuf generado
import payment_pb2
import payment_pb2_grpc


class GrpcUser(User):
    """Usuario que prueba un servicio gRPC."""
    
    abstract = True
    stub_class = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Crear canal gRPC
        self.channel = grpc.insecure_channel(self.host)
        self.stub = self.stub_class(self.channel)
    
    def on_stop(self):
        self.channel.close()


class PaymentGrpcUser(GrpcUser):
    """Test de servicio de pagos gRPC."""
    
    host = "payment-service:50051"
    stub_class = payment_pb2_grpc.PaymentServiceStub
    wait_time = between(1, 3)
    
    def _grpc_call(self, method_name, request, **kwargs):
        """Wrapper para reportar métricas de gRPC a Locust."""
        start_time = time.perf_counter()
        try:
            method = getattr(self.stub, method_name)
            response = method(request, **kwargs)
            elapsed = (time.perf_counter() - start_time) * 1000
            
            events.request.fire(
                request_type="gRPC",
                name=method_name,
                response_time=elapsed,
                response_length=response.ByteSize(),
                response=response,
                context={},
                exception=None,
            )
            return response
        except grpc.RpcError as e:
            elapsed = (time.perf_counter() - start_time) * 1000
            events.request.fire(
                request_type="gRPC",
                name=method_name,
                response_time=elapsed,
                response_length=0,
                response=None,
                context={},
                exception=e,
            )
            return None
    
    @task(5)
    def get_balance(self):
        request = payment_pb2.GetBalanceRequest(user_id="user_123")
        self._grpc_call("GetBalance", request, timeout=5)
    
    @task(2)
    def process_payment(self):
        request = payment_pb2.ProcessPaymentRequest(
            user_id="user_123",
            amount=9.99,
            currency="USD",
            merchant_id="merchant_456"
        )
        self._grpc_call("ProcessPayment", request, timeout=10)
```

### WebSocket Testing

```python
from locust import User, task, between, events
import websocket
import json
import time
import gevent

class WebSocketUser(User):
    """Test de WebSocket (chat, real-time, etc.)."""
    
    host = "wss://ws.example.com"
    wait_time = between(0.5, 2)
    
    def on_start(self):
        self.ws = websocket.create_connection(
            f"{self.host}/ws/chat",
            header={"Authorization": "Bearer test_token"}
        )
        # Listener en background para mensajes entrantes
        self._receiver = gevent.spawn(self._receive_messages)
        self.messages_received = 0
    
    def on_stop(self):
        self._receiver.kill()
        self.ws.close()
    
    def _receive_messages(self):
        """Escuchar mensajes en background."""
        while True:
            try:
                msg = self.ws.recv()
                self.messages_received += 1
            except Exception:
                break
    
    def _send_and_measure(self, name, payload):
        """Enviar mensaje y medir tiempo de round-trip."""
        start = time.perf_counter()
        try:
            self.ws.send(json.dumps(payload))
            # Esperar ACK
            response = self.ws.recv()
            elapsed = (time.perf_counter() - start) * 1000
            
            events.request.fire(
                request_type="WebSocket",
                name=name,
                response_time=elapsed,
                response_length=len(response),
                response=response,
                context={},
                exception=None,
            )
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            events.request.fire(
                request_type="WebSocket",
                name=name,
                response_time=elapsed,
                response_length=0,
                response=None,
                context={},
                exception=e,
            )
    
    @task(5)
    def send_message(self):
        self._send_and_measure("send_chat_message", {
            "type": "message",
            "room": "general",
            "text": f"Hello from user {self.greenlet.minimal_ident}"
        })
    
    @task(2)
    def join_room(self):
        self._send_and_measure("join_room", {
            "type": "join",
            "room": f"room_{random.randint(1, 10)}"
        })
```

### MQTT Testing (IoT)

```python
from locust import User, task, between, events
import paho.mqtt.client as mqtt
import time
import json
import random

class MqttUser(User):
    """Test de broker MQTT (IoT devices)."""
    
    host = "mqtt.example.com"
    wait_time = between(1, 5)
    
    def on_start(self):
        self.client_id = f"locust_{self.greenlet.minimal_ident}_{random.randint(1000, 9999)}"
        self.mqtt_client = mqtt.Client(client_id=self.client_id)
        self.mqtt_client.on_message = self._on_message
        self.mqtt_client.connect(self.host, 1883, 60)
        self.mqtt_client.loop_start()
        
        # Suscribirse a topics
        self.mqtt_client.subscribe("devices/+/telemetry", qos=1)
    
    def on_stop(self):
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()
    
    def _on_message(self, client, userdata, msg):
        """Handler para mensajes recibidos."""
        pass
    
    @task(10)
    def publish_telemetry(self):
        """Publicar datos de telemetría (simula dispositivo IoT)."""
        start = time.perf_counter()
        topic = f"devices/{self.client_id}/telemetry"
        payload = json.dumps({
            "temperature": round(random.uniform(20, 35), 1),
            "humidity": round(random.uniform(30, 80), 1),
            "timestamp": int(time.time())
        })
        
        result = self.mqtt_client.publish(topic, payload, qos=1)
        result.wait_for_publish()
        
        elapsed = (time.perf_counter() - start) * 1000
        events.request.fire(
            request_type="MQTT",
            name="publish_telemetry",
            response_time=elapsed,
            response_length=len(payload),
            response=None,
            context={},
            exception=None if result.rc == mqtt.MQTT_ERR_SUCCESS else Exception(f"MQTT error: {result.rc}"),
        )
```

---

## 14. Datos de Prueba y Parametrización

### CSV Data Feed

```python
import csv
import queue
import random
from locust import HttpUser, task, between, events
from locust.runners import MasterRunner

# Queue thread-safe para datos únicos (no repetir)
user_queue = queue.Queue()

@events.test_start.add_listener
def load_users(environment, **kwargs):
    """Cargar usuarios de CSV al inicio del test."""
    with open("data/users.csv", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            user_queue.put(row)
    print(f"Loaded {user_queue.qsize()} unique users")


class UniqueUserTest(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Cada usuario virtual obtiene credenciales únicas."""
        try:
            self.user_data = user_queue.get_nowait()
        except queue.Empty:
            # Si se acabaron los usuarios, reciclar con random
            self.user_data = {"email": f"user_{random.randint(1,9999)}@test.com", "password": "pass"}
        
        # Login con usuario único
        self.client.post("/api/login", json={
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        })
    
    def on_stop(self):
        """Devolver usuario al pool para reutilización."""
        user_queue.put(self.user_data)
```

### Faker para datos dinámicos

```python
from locust import HttpUser, task, between
from faker import Faker
import random

fake = Faker(['es_ES', 'en_US'])  # Datos en español e inglés

class DynamicDataUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def create_user(self):
        """Crear usuario con datos aleatorios realistas."""
        self.client.post("/api/users", json={
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.unique.email(),
            "phone": fake.phone_number(),
            "address": {
                "street": fake.street_address(),
                "city": fake.city(),
                "state": fake.state(),
                "zip": fake.postcode(),
                "country": fake.country_code()
            },
            "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=80).isoformat(),
            "credit_card": {
                "number": fake.credit_card_number(),
                "expiry": fake.credit_card_expire(),
                "cvv": fake.credit_card_security_code()
            }
        })
    
    @task
    def create_order(self):
        """Orden con productos aleatorios."""
        self.client.post("/api/orders", json={
            "items": [
                {
                    "product_id": fake.uuid4(),
                    "name": fake.catch_phrase(),
                    "quantity": random.randint(1, 5),
                    "price": round(random.uniform(9.99, 999.99), 2)
                }
                for _ in range(random.randint(1, 5))
            ],
            "shipping_method": random.choice(["standard", "express", "overnight"]),
            "notes": fake.sentence() if random.random() > 0.7 else None
        })
```

### Datos compartidos con iterador circular

```python
import itertools
import threading
from locust import HttpUser, task, between

class SharedDataIterator:
    """Thread-safe circular iterator para datos compartidos."""
    
    def __init__(self, data):
        self._data = data
        self._iterator = itertools.cycle(data)
        self._lock = threading.Lock()
    
    def next(self):
        with self._lock:
            return next(self._iterator)
    
    def __len__(self):
        return len(self._data)

# Datos globales
PRODUCTS = SharedDataIterator([
    {"id": 1, "sku": "LAPTOP-001"},
    {"id": 2, "sku": "PHONE-002"},
    {"id": 3, "sku": "TABLET-003"},
    # ... miles de productos
])

SEARCH_TERMS = SharedDataIterator([
    "laptop gaming", "smartphone 5G", "wireless headphones",
    "mechanical keyboard", "4K monitor", "USB hub"
])


class DataDrivenUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def search(self):
        term = SEARCH_TERMS.next()
        self.client.get(f"/api/search?q={term}", name="/api/search")
    
    @task
    def view_product(self):
        product = PRODUCTS.next()
        self.client.get(f"/api/products/{product['id']}", name="/api/products/[id]")
```

---

## 15. Métricas, Reportes y Exportación

### Métricas disponibles en Locust

```
┌──────────────────────────────────────────────────────────────────┐
│                    LOCUST METRICS                                  │
├────────────────────────┬─────────────────────────────────────────┤
│ Métrica                │ Descripción                              │
├────────────────────────┼─────────────────────────────────────────┤
│ # Requests             │ Total de requests realizados            │
│ # Failures             │ Total de requests fallidos              │
│ Median (ms)            │ P50 response time                       │
│ 95%ile (ms)            │ P95 response time                       │
│ 99%ile (ms)            │ P99 response time                       │
│ Average (ms)           │ Response time promedio                  │
│ Min (ms)               │ Response time mínimo                    │
│ Max (ms)               │ Response time máximo                    │
│ Avg Content Size       │ Tamaño promedio de respuesta (bytes)    │
│ Current RPS            │ Requests per second actual              │
│ Current Failures/s     │ Failures per second actual              │
│ Users                  │ Usuarios virtuales activos              │
└────────────────────────┴─────────────────────────────────────────┘
```

### Exportación a CSV

```bash
# Generar CSVs automáticamente
locust -f locustfile.py --headless \
  --users 100 --spawn-rate 10 --run-time 10m \
  --csv reports/test_results \
  --csv-full-history

# Genera 3 archivos:
# reports/test_results_stats.csv          → Stats por endpoint
# reports/test_results_stats_history.csv  → Stats por segundo (full history)
# reports/test_results_failures.csv       → Detalle de failures
# reports/test_results_exceptions.csv     → Excepciones
```

### HTML Report

```bash
# Generar HTML report automáticamente
locust -f locustfile.py --headless \
  --users 100 --spawn-rate 10 --run-time 10m \
  --html reports/report.html
```

### Custom metrics con Prometheus

```python
from locust import events, HttpUser, task
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Métricas Prometheus custom
REQUEST_LATENCY = Histogram(
    'locust_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint', 'status'],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]
)

REQUEST_COUNT = Counter(
    'locust_requests_total',
    'Total request count',
    ['method', 'endpoint', 'status']
)

ACTIVE_USERS = Gauge(
    'locust_active_users',
    'Number of active virtual users'
)

FAILURES = Counter(
    'locust_failures_total',
    'Total failure count',
    ['method', 'endpoint', 'error']
)


@events.init.add_listener
def start_prometheus(environment, **kwargs):
    """Iniciar servidor Prometheus en puerto 9646."""
    start_http_server(9646)
    print("Prometheus metrics available at :9646/metrics")


@events.request.add_listener
def on_request(request_type, name, response_time, response_length,
               response, context, exception, **kwargs):
    """Reportar cada request a Prometheus."""
    status = "error" if exception else str(response.status_code if response else 0)
    
    REQUEST_LATENCY.labels(
        method=request_type, endpoint=name, status=status
    ).observe(response_time / 1000.0)
    
    REQUEST_COUNT.labels(
        method=request_type, endpoint=name, status=status
    ).inc()
    
    if exception:
        FAILURES.labels(
            method=request_type, endpoint=name, error=str(type(exception).__name__)
        ).inc()


@events.spawning_complete.add_listener
def on_spawning_complete(user_count, **kwargs):
    ACTIVE_USERS.set(user_count)
```

---

## 16. Integración con CI/CD

### GitHub Actions

```yaml
# .github/workflows/load-test.yml
name: Performance Test

on:
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1-5'  # Lun-Vie 6 AM
  workflow_dispatch:
    inputs:
      users:
        description: 'Number of users'
        default: '100'
      duration:
        description: 'Test duration'
        default: '5m'

jobs:
  load-test:
    runs-on: ubuntu-latest
    environment: staging
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      
      - name: Install dependencies
        run: pip install -r requirements-perf.txt
      
      - name: Run Locust
        run: |
          locust -f tests/performance/locustfile.py \
            --host ${{ secrets.STAGING_URL }} \
            --headless \
            --users ${{ inputs.users || '100' }} \
            --spawn-rate 10 \
            --run-time ${{ inputs.duration || '5m' }} \
            --csv results/perf \
            --html results/report.html \
            --exit-code-on-error 1
        env:
          API_TOKEN: ${{ secrets.PERF_TEST_TOKEN }}
      
      - name: Check thresholds
        run: |
          python scripts/check_thresholds.py \
            --csv results/perf_stats.csv \
            --p95-max 1000 \
            --error-rate-max 1.0 \
            --min-rps 50
      
      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: performance-results
          path: results/
      
      - name: Comment on PR
        if: github.event_name == 'pull_request' && always()
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const stats = fs.readFileSync('results/perf_stats.csv', 'utf8');
            // Parse and format as markdown table...
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## 📊 Performance Test Results\n\n${formattedTable}`
            });
```

### Script de validación de thresholds

```python
#!/usr/bin/env python3
"""check_thresholds.py - Validar resultados contra umbrales."""

import csv
import sys
import argparse

def check_thresholds(csv_path, p95_max, error_rate_max, min_rps):
    failures = []
    
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Name"] == "Aggregated":
                # P95 latency
                p95 = float(row.get("95%", 0))
                if p95 > p95_max:
                    failures.append(f"❌ P95 latency {p95:.0f}ms exceeds {p95_max}ms")
                else:
                    print(f"✅ P95 latency: {p95:.0f}ms (max: {p95_max}ms)")
                
                # Error rate
                total = int(row.get("Request Count", 0))
                fails = int(row.get("Failure Count", 0))
                error_rate = (fails / total * 100) if total > 0 else 0
                if error_rate > error_rate_max:
                    failures.append(f"❌ Error rate {error_rate:.2f}% exceeds {error_rate_max}%")
                else:
                    print(f"✅ Error rate: {error_rate:.2f}% (max: {error_rate_max}%)")
                
                # RPS
                rps = float(row.get("Requests/s", 0))
                if rps < min_rps:
                    failures.append(f"❌ RPS {rps:.1f} below minimum {min_rps}")
                else:
                    print(f"✅ RPS: {rps:.1f} (min: {min_rps})")
    
    if failures:
        print("\n🚨 PERFORMANCE THRESHOLDS VIOLATED:")
        for f in failures:
            print(f"  {f}")
        sys.exit(1)
    else:
        print("\n✅ All performance thresholds passed!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--p95-max", type=float, default=1000)
    parser.add_argument("--error-rate-max", type=float, default=1.0)
    parser.add_argument("--min-rps", type=float, default=50)
    args = parser.parse_args()
    
    check_thresholds(args.csv, args.p95_max, args.error_rate_max, args.min_rps)
```

---

## 17. Plugins y Ecosistema

### locust-plugins (SvenskaSpel)

El paquete `locust-plugins` extiende Locust con funcionalidades adicionales:

```bash
pip install locust-plugins
```

```python
# ── Listeners para dashboards ──
from locust_plugins.dashboards import DashboardIntegration

# ── Readers para datos de test ──
from locust_plugins.csvreader import CSVReader

# Reader que recicla datos automáticamente
reader = CSVReader("data/users.csv")

class MyUser(HttpUser):
    @task
    def use_csv_data(self):
        data = next(reader)  # Thread-safe, recicla al final
        self.client.post("/login", json={"user": data[0], "pass": data[1]})

# ── MongoDB User ──
from locust_plugins.users import MongoUser

# ── Kafka User ──  
from locust_plugins.users import KafkaUser

# ── SocketIO User ──
from locust_plugins.users import SocketIOUser
```

### Plugins populares de la comunidad

| Plugin | Funcionalidad |
|--------|--------------|
| `locust-plugins` | CSV reader, dashboards, Kafka/Mongo users |
| `locust-influxdb-listener` | Exportar a InfluxDB |
| `locust-grafana-dashboard` | Dashboard Grafana preconfigurado |
| `locust-swarm` | Orquestación en AWS |
| `har2locust` | Convertir HAR files a locustfile |
| `locust-kubernetes` | Helm charts para K8s |

### har2locust (Generar tests desde browser)

```bash
# 1. Grabar sesión en browser (DevTools → Network → Export HAR)
# 2. Convertir HAR a locustfile
pip install har2locust
har2locust recording.har > locustfile.py

# Con filtros
har2locust recording.har \
  --filter "api.example.com" \
  --exclude "analytics|tracking" \
  > locustfile.py
```

---

## 18. Patrones Avanzados

### 18.1 Correlation (Extracción de datos dinámicos)

```python
from locust import HttpUser, task, between
import re

class CorrelationUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def transaction_with_correlation(self):
        """Simular flujo que requiere tokens/IDs dinámicos."""
        
        # Step 1: Obtener CSRF token
        resp = self.client.get("/form")
        csrf_match = re.search(r'name="csrf_token" value="([^"]+)"', resp.text)
        csrf_token = csrf_match.group(1) if csrf_match else ""
        
        # Step 2: Submit form con CSRF token extraído
        resp = self.client.post("/submit", data={
            "csrf_token": csrf_token,
            "data": "test_value"
        })
        
        # Step 3: Extraer ID del recurso creado
        if resp.ok:
            resource_id = resp.json().get("id")
            
            # Step 4: Usar el ID en siguiente request
            self.client.get(
                f"/api/resources/{resource_id}/status",
                name="/api/resources/[id]/status"
            )
```

### 18.2 Think Time realista con distribución

```python
import random
import numpy as np
from locust import HttpUser, task

class RealisticThinkTimeUser(HttpUser):
    """Think time basado en distribución log-normal (más realista)."""
    
    def wait_time(self):
        # Log-normal: mayoría piensa 2-5s, algunos hasta 30s+
        # mu=1.0, sigma=0.8 → mediana ~2.7s, media ~3.6s
        return max(0.5, random.lognormvariate(1.0, 0.8))
    
    @task
    def browse(self):
        self.client.get("/products")
    
    @task
    def read_article(self):
        self.client.get("/articles/1")
        # Tiempo extra de lectura (simular que lee el artículo)
        reading_time = random.gauss(30, 10)  # ~30s ± 10s
        import time
        time.sleep(max(5, reading_time))
```

### 18.3 Ramp-up por tipo de usuario

```python
from locust import LoadTestShape, HttpUser, task, between

class PhasedRampUpShape(LoadTestShape):
    """
    Ramp-up por fases: primero browse, luego compras.
    Simula día real: primero llegan browsers, luego compradores.
    """
    
    def tick(self):
        run_time = self.get_run_time()
        
        if run_time < 120:
            # Fase 1: Solo browsers (2 min)
            return (50, 5)  # 50 users, 5/sec spawn
        elif run_time < 300:
            # Fase 2: Browsers + algunos compradores (3 min)
            return (150, 10)
        elif run_time < 600:
            # Fase 3: Full load (5 min)
            return (300, 15)
        elif run_time < 900:
            # Fase 4: Pico (5 min)
            return (500, 20)
        elif run_time < 1200:
            # Fase 5: Descenso (5 min)
            return (100, 5)
        else:
            return None
```

### 18.4 Circuit Breaker en el test

```python
from locust import HttpUser, task, between, events
import time
import threading

class TestCircuitBreaker:
    """Circuit breaker para el TEST mismo - parar si el sistema se degrada."""
    
    def __init__(self, failure_threshold=0.1, window_seconds=30):
        self.failure_threshold = failure_threshold
        self.window = window_seconds
        self.requests = []
        self.lock = threading.Lock()
        self.is_open = False
    
    def record(self, success):
        with self.lock:
            now = time.time()
            self.requests.append((now, success))
            # Limpiar requests fuera de ventana
            self.requests = [(t, s) for t, s in self.requests if now - t < self.window]
            
            # Evaluar
            if len(self.requests) > 100:
                failures = sum(1 for _, s in self.requests if not s)
                rate = failures / len(self.requests)
                if rate > self.failure_threshold:
                    self.is_open = True

circuit_breaker = TestCircuitBreaker(failure_threshold=0.15, window_seconds=60)

@events.request.add_listener
def on_request(exception, **kwargs):
    circuit_breaker.record(exception is None)
    if circuit_breaker.is_open:
        # Parar el test si el sistema está demasiado degradado
        print("⚠️ Circuit breaker OPEN - stopping test")
        kwargs.get("environment", {}).runner.quit() if hasattr(kwargs.get("environment", {}), "runner") else None
```

### 18.5 Token Refresh automático

```python
from locust import HttpUser, task, between
import time
import threading

class TokenManagedUser(HttpUser):
    """Usuario con refresh automático de tokens JWT."""
    
    wait_time = between(1, 5)
    abstract = True
    
    token = None
    token_expiry = 0
    _refresh_lock = threading.Lock()
    
    def on_start(self):
        self._authenticate()
    
    def _authenticate(self):
        """Obtener token inicial."""
        resp = self.client.post("/auth/token", json={
            "grant_type": "client_credentials",
            "client_id": "perf_test",
            "client_secret": "secret"
        }, name="/auth/token [login]")
        
        if resp.ok:
            data = resp.json()
            self.token = data["access_token"]
            # Refresh 30 segundos antes de expirar
            self.token_expiry = time.time() + data["expires_in"] - 30
            self.client.headers["Authorization"] = f"Bearer {self.token}"
    
    def _ensure_valid_token(self):
        """Refresh token si está por expirar."""
        if time.time() >= self.token_expiry:
            with self._refresh_lock:
                # Double-check después de obtener lock
                if time.time() >= self.token_expiry:
                    self._authenticate()
    
    def authenticated_request(self, method, path, **kwargs):
        """Wrapper que asegura token válido."""
        self._ensure_valid_token()
        return getattr(self.client, method)(path, **kwargs)
```

---

## 19. Debugging y Troubleshooting

### Problemas comunes y soluciones

```python
# ═══════════════════════════════════════════════════════════════
# PROBLEMA 1: "All users are waiting" (no se generan requests)
# ═══════════════════════════════════════════════════════════════
# CAUSA: wait_time muy alto o tasks que no retornan
# SOLUCIÓN: Verificar wait_time y que no haya bloqueos

# MALO:
class BadUser(HttpUser):
    wait_time = constant(300)  # 5 minutos entre tasks!
    
    @task
    def blocking_task(self):
        import time
        time.sleep(60)  # BLOQUEA el greenlet 60s (otros users no afectados, pero este sí)

# BUENO:
class GoodUser(HttpUser):
    wait_time = between(1, 5)
    
    @task
    def non_blocking_task(self):
        from gevent import sleep
        sleep(5)  # Cooperative sleep - no bloquea otros greenlets


# ═══════════════════════════════════════════════════════════════
# PROBLEMA 2: CPU al 100% en worker (throughput se estanca)
# ═══════════════════════════════════════════════════════════════
# CAUSA: Demasiados usuarios para un solo proceso, o código CPU-heavy
# SOLUCIÓN: 
#   1. Agregar más workers
#   2. Usar FastHttpUser
#   3. Optimizar lógica en tasks

# Verificar con:
# locust -f test.py --headless -u 1000 --run-time 1m
# Si CPU > 80%, hay bottleneck en el load generator


# ═══════════════════════════════════════════════════════════════
# PROBLEMA 3: ConnectionError / Max retries exceeded
# ═══════════════════════════════════════════════════════════════
# CAUSA: Connection pool exhausted o target no responde
# SOLUCIÓN:
from locust import HttpUser

class FixedConnectionUser(HttpUser):
    # Aumentar pool size
    pool_manager = None
    
    def on_start(self):
        # Para HttpUser: configurar adapter con más connections
        from requests.adapters import HTTPAdapter
        adapter = HTTPAdapter(
            pool_connections=100,
            pool_maxsize=100,
            max_retries=0
        )
        self.client.mount("https://", adapter)
        self.client.mount("http://", adapter)


# ═══════════════════════════════════════════════════════════════
# PROBLEMA 4: Memory leak (RAM crece indefinidamente)
# ═══════════════════════════════════════════════════════════════
# CAUSA: Acumular datos en listas/dicts sin limpiar
# SOLUCIÓN: Limitar colecciones, usar deque con maxlen

from collections import deque

class MemorySafeUser(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # MALO: self.history = []  (crece infinitamente)
        # BUENO:
        self.history = deque(maxlen=100)  # Solo últimos 100
```

### Debugging con logging

```python
import logging
from locust import HttpUser, task, between, events

# Configurar logging detallado
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("perf_test")

# Desactivar logs verbosos de libraries
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)

class DebugUser(HttpUser):
    wait_time = between(1, 2)
    
    @task
    def debug_request(self):
        logger.debug(f"User {id(self)} making request...")
        
        resp = self.client.get("/api/data")
        
        if resp.status_code != 200:
            logger.error(
                f"Unexpected response: status={resp.status_code}, "
                f"body={resp.text[:200]}, "
                f"headers={dict(resp.headers)}"
            )
```

### Ejecutar un solo usuario (debug mode)

```bash
# Ejecutar con 1 solo usuario para debugging
locust -f locustfile.py --headless -u 1 -r 1 --run-time 30s --loglevel DEBUG

# O usar el debugger de Python
python -m pdb -c continue locustfile.py
```

---

## 20. Comparativa con Otras Herramientas

### Comparativa detallada

```
┌─────────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
│ Característica  │    Locust    │     k6       │   Gatling    │   JMeter     │
├─────────────────┼──────────────┼──────────────┼──────────────┼──────────────┤
│ Lenguaje        │ Python       │ JavaScript   │ Scala/Java   │ XML/GUI      │
│ Protocolo       │ Cualquiera   │ HTTP/gRPC/WS │ HTTP/WS/JMS  │ Casi todos   │
│ Concurrencia    │ Greenlets    │ Goroutines   │ Akka actors  │ Threads Java │
│ Max RPS/máq     │ ~15K         │ ~300K        │ ~100K        │ ~10K         │
│ RAM/1K users    │ ~100MB       │ ~50MB        │ ~80MB        │ ~500MB       │
│ Distributed     │ Nativo       │ k6 Cloud/xk6 │ Manual       │ Manual       │
│ Custom shapes   │ Python code  │ Scenarios    │ Injection    │ Plugins      │
│ Learning curve  │ Baja (Python)│ Baja (JS)    │ Media(Scala) │ Baja (GUI)   │
│ CI/CD friendly  │ ⭐⭐⭐⭐       │ ⭐⭐⭐⭐⭐      │ ⭐⭐⭐⭐       │ ⭐⭐⭐         │
│ Real browser    │ No           │ No (xk6-brw) │ No           │ No           │
│ Record & play   │ har2locust   │ Browser rec  │ HAR import   │ Recorder     │
│ Cloud service   │ Locust Cloud │ Grafana Cloud│ Gatling Ent. │ BlazeMeter   │
│ Costo           │ Free (MIT)   │ Free (AGPL)  │ Free (Apache)│ Free(Apache) │
│ Web UI          │ Sí (live)    │ No (output)  │ Report HTML  │ Sí (heavy)   │
└─────────────────┴──────────────┴──────────────┴──────────────┴──────────────┘
```

### Cuándo elegir Locust

| Escenario | ¿Locust? | Alternativa |
|-----------|----------|-------------|
| Equipo Python | ✅ Ideal | - |
| Máximo throughput | ⚠️ Necesita más workers | k6 |
| Protocolos custom | ✅ Extensible en Python | k6 (xk6) |
| Tests rápidos CLI | ⚠️ Funciona, no es su fuerte | k6 |
| Tests complejos con lógica | ✅ Python full | - |
| Enterprise con soporte | ⚠️ Locust Cloud (nuevo) | LoadRunner, NeoLoad |
| Grafana ecosystem | ⚠️ Plugins necesarios | k6 (nativo Grafana) |
| Kubernetes native | ✅ Con Helm charts | - |

---

## 21. Mejores Prácticas y Antipatrones

### ✅ Mejores Prácticas

```python
# 1. USAR name PARA AGRUPAR URLs DINÁMICAS
# MALO: miles de entradas en stats
self.client.get(f"/api/users/{user_id}")

# BUENO: una entrada agrupada
self.client.get(f"/api/users/{user_id}", name="/api/users/[id]")


# 2. NO HACER ASSERTIONS QUE GENEREN FALSOS POSITIVOS
# MALO: falla por cualquier respuesta no-200
with self.client.get("/api/data", catch_response=True) as r:
    if r.status_code != 200:
        r.failure("not 200")  # 429, 503 temporal = falso positivo

# BUENO: distinguir fallas reales de transitorias
with self.client.get("/api/data", catch_response=True) as r:
    if r.status_code in (500, 502, 503):
        r.failure(f"Server error: {r.status_code}")
    elif r.status_code == 429:
        r.success()  # Rate limited es comportamiento esperado
    elif r.status_code == 200:
        r.success()


# 3. USAR on_start PARA SETUP, NO PRIMER TASK
# MALO:
class BadUser(HttpUser):
    logged_in = False
    @task
    def do_stuff(self):
        if not self.logged_in:
            self.client.post("/login", ...)
            self.logged_in = True
        self.client.get("/data")

# BUENO:
class GoodUser(HttpUser):
    def on_start(self):
        self.client.post("/login", ...)
    @task
    def do_stuff(self):
        self.client.get("/data")


# 4. EVITAR CPU-HEAVY EN TASKS
# MALO: Parsear XML gigante en cada iteración
import xml.etree.ElementTree as ET
@task
def parse_heavy(self):
    resp = self.client.get("/huge-xml")
    tree = ET.fromstring(resp.text)  # CPU-heavy, bloquea greenlet
    # ... proceso complejo

# BUENO: Mínimo procesamiento, validar solo lo necesario
@task
def parse_light(self):
    with self.client.get("/huge-xml", catch_response=True) as resp:
        if resp.status_code == 200 and len(resp.content) > 1000:
            resp.success()
        else:
            resp.failure("Invalid response")


# 5. SEPARAR DATOS DE LECTURA vs ESCRITURA
# Para evitar que datos se contaminen entre users
class SafeUser(HttpUser):
    def on_start(self):
        # Datos propios del usuario (no compartidos)
        self.my_items = []
    
    @task
    def create_item(self):
        resp = self.client.post("/items", json={"name": "test"})
        if resp.ok:
            self.my_items.append(resp.json()["id"])
    
    @task
    def read_own_item(self):
        if self.my_items:
            item_id = random.choice(self.my_items)
            self.client.get(f"/items/{item_id}", name="/items/[id]")
```

### ❌ Antipatrones

```python
# ANTIPATRÓN 1: Shared mutable state sin lock
shared_list = []  # PELIGROSO: race conditions

# ANTIPATRÓN 2: Sleep largo sin gevent
import time
time.sleep(30)  # Bloquea el greenlet (otros no se ven afectados, pero este usuario queda inactivo)
# Usar: from gevent import sleep; sleep(30)

# ANTIPATRÓN 3: Crear conexiones en cada request
@task
def bad_connection(self):
    import requests
    s = requests.Session()  # NUEVA sesión cada vez
    s.get(self.host + "/api/data")
    s.close()
# Usar self.client que reutiliza conexiones

# ANTIPATRÓN 4: No usar headless en CI/CD
# locust -f test.py -u 100 -r 10  ← Se queda esperando Web UI
# locust -f test.py -u 100 -r 10 --headless --run-time 5m ← Correcto

# ANTIPATRÓN 5: Ignorar el patrón de tráfico real
# Test con constant(0) no es realista
# Usar distribuciones basadas en datos de producción
```

---

## 22. Proyecto de Referencia Completo

### Estructura de proyecto recomendada

```
performance-tests/
├── locust.conf                  # Configuración default
├── requirements.txt             # Dependencias
├── Dockerfile                   # Para ejecución containerizada
├── docker-compose.yml           # Cluster distribuido local
├── Makefile                     # Comandos comunes
│
├── src/
│   ├── __init__.py
│   ├── locustfile.py            # Punto de entrada principal
│   ├── users/
│   │   ├── __init__.py
│   │   ├── web_user.py          # User type: web
│   │   ├── mobile_user.py       # User type: mobile
│   │   └── api_user.py          # User type: API integration
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── browse.py            # TaskSet: navegación
│   │   ├── search.py            # TaskSet: búsqueda
│   │   ├── checkout.py          # TaskSet: compra
│   │   └── admin.py             # TaskSet: administración
│   ├── shapes/
│   │   ├── __init__.py
│   │   ├── spike.py             # LoadTestShape: spike
│   │   ├── step.py              # LoadTestShape: step
│   │   └── production.py        # LoadTestShape: simula prod
│   ├── helpers/
│   │   ├── __init__.py
│   │   ├── auth.py              # Token management
│   │   ├── data_feeder.py       # Data provision
│   │   └── validators.py        # Response validators
│   └── hooks/
│       ├── __init__.py
│       ├── reporting.py         # Event hooks para reporting
│       └── monitoring.py        # Prometheus/InfluxDB export
│
├── data/
│   ├── users.csv                # Test users
│   ├── products.json            # Test products
│   └── traffic_profile.csv      # Perfil de carga real
│
├── scripts/
│   ├── check_thresholds.py      # Validación post-test
│   ├── generate_report.py       # Reporte personalizado
│   └── setup_test_data.py       # Preparar datos
│
├── reports/                     # Output (gitignored)
│   ├── .gitkeep
│   └── ...
│
└── tests/                       # Unit tests del framework
    ├── test_data_feeder.py
    ├── test_validators.py
    └── test_shapes.py
```

### Makefile para comandos comunes

```makefile
# Makefile
.PHONY: test load-test spike-test debug clean

# Variables
USERS ?= 100
SPAWN_RATE ?= 10
DURATION ?= 5m
HOST ?= https://api.staging.example.com

install:
	pip install -r requirements.txt

# Test rápido (smoke)
smoke:
	locust -f src/locustfile.py --headless \
		--host $(HOST) -u 5 -r 5 --run-time 30s \
		--html reports/smoke.html

# Load test standard
load-test:
	locust -f src/locustfile.py --headless \
		--host $(HOST) -u $(USERS) -r $(SPAWN_RATE) \
		--run-time $(DURATION) \
		--csv reports/load --html reports/load.html

# Spike test
spike-test:
	locust -f src/locustfile.py -f src/shapes/spike.py --headless \
		--host $(HOST) \
		--csv reports/spike --html reports/spike.html

# Debug con 1 usuario
debug:
	locust -f src/locustfile.py --headless \
		--host $(HOST) -u 1 -r 1 --run-time 30s \
		--loglevel DEBUG

# UI mode (interactivo)
ui:
	locust -f src/locustfile.py --host $(HOST)

# Distribuido (docker)
distributed:
	docker-compose up --scale worker=4

# Limpiar reportes
clean:
	rm -rf reports/*.csv reports/*.html reports/*.json

# Validar thresholds
validate:
	python scripts/check_thresholds.py \
		--csv reports/load_stats.csv \
		--p95-max 1000 --error-rate-max 1.0 --min-rps 50
```

---

## Referencias

- [Documentación oficial de Locust](https://docs.locust.io/en/stable/)
- [GitHub: locustio/locust](https://github.com/locustio/locust)
- [GitHub: SvenskaSpel/locust-plugins](https://github.com/SvenskaSpel/locust-plugins)
- [har2locust](https://github.com/SvenskaSpel/har2locust)
- [Locust Cloud](https://locust.cloud/)
- [gevent Documentation](http://www.gevent.org/)
- [Real Python: Load Testing with Locust](https://realpython.com/python-load-testing/)

---

> 💡 **Locust destaca por su flexibilidad y código Python puro.**
> Si tu equipo domina Python y necesita lógica compleja en los tests, Locust es la elección natural. Para máximo rendimiento puro, complementa con más workers o considera FastHttpUser.
