# 🪶 Apache JMeter - Guía Completa de Referencia

## Índice

1. [Introducción y Filosofía](#1-introducción-y-filosofía)
2. [Arquitectura Interna](#2-arquitectura-interna)
3. [Instalación y Configuración](#3-instalación-y-configuración)
4. [Estructura del Test Plan](#4-estructura-del-test-plan)
5. [Thread Groups (Grupos de Hilos)](#5-thread-groups-grupos-de-hilos)
6. [Samplers (Protocolos)](#6-samplers-protocolos)
7. [Config Elements](#7-config-elements)
8. [Pre-Processors y Post-Processors](#8-pre-processors-y-post-processors)
9. [Extractors y Correlation](#9-extractors-y-correlation)
10. [Assertions (Validaciones)](#10-assertions-validaciones)
11. [Timers (Think Time)](#11-timers-think-time)
12. [Logic Controllers](#12-logic-controllers)
13. [Listeners (Reportes)](#13-listeners-reportes)
14. [Scripting (JSR223 / Groovy)](#14-scripting-jsr223--groovy)
15. [Parametrización y Data Driven Testing](#15-parametrización-y-data-driven-testing)
16. [Testing Distribuido](#16-testing-distribuido)
17. [Ejecución en Modo CLI (Non-GUI)](#17-ejecución-en-modo-cli-non-gui)
18. [Plugins Esenciales](#18-plugins-esenciales)
19. [Protocolos Avanzados (JDBC, JMS, SMTP)](#19-protocolos-avanzados-jdbc-jms-smtp)
20. [Integración con CI/CD](#20-integración-con-cicd)
21. [HTML Dashboard Report](#21-html-dashboard-report)
22. [Patrones Avanzados](#22-patrones-avanzados)
23. [Troubleshooting y Performance Tuning](#23-troubleshooting-y-performance-tuning)
24. [Mejores Prácticas y Antipatrones](#24-mejores-prácticas-y-antipatrones)
25. [Proyecto de Referencia Completo](#25-proyecto-de-referencia-completo)

---

## 1. Introducción y Filosofía

### ¿Qué es Apache JMeter?

**Apache JMeter** es una aplicación open-source 100% Java diseñada para realizar load testing, performance testing y functional testing de aplicaciones. Originalmente diseñada para testing de aplicaciones web, ahora soporta prácticamente cualquier protocolo.

### Historia y evolución

| Año | Hito |
|-----|------|
| 1998 | Stefano Mazzocchi crea JMeter como proyecto Apache |
| 2001 | JMeter 1.0 - solo HTTP |
| 2003 | JMeter 2.0 - múltiples protocolos |
| 2011 | JMeter 2.5 - mejoras de rendimiento |
| 2016 | JMeter 3.0 - reporte HTML dashboard |
| 2019 | JMeter 5.0 - soporte HTTP/2 |
| 2023 | JMeter 5.6 - mejoras Groovy, HTTP/2 nativo |
| 2024 | JMeter 5.6.3 - versión estable actual |

### Filosofía de diseño

| Principio | Implementación |
|-----------|---------------|
| **Multi-protocolo** | HTTP, HTTPS, FTP, JDBC, LDAP, JMS, SMTP, TCP, etc. |
| **GUI + CLI** | Diseño visual en GUI, ejecución en CLI |
| **Extensible** | Sistema de plugins, scripting JSR223 |
| **Portátil** | 100% Java, corre en cualquier OS con JVM |
| **Comunidad** | Apache Foundation, miles de plugins, gran comunidad |

### Cuándo usar JMeter

✅ **Ideal para:**
- Testers no-programadores (GUI drag-and-drop)
- Tests multi-protocolo (HTTP + JDBC + JMS en un test)
- Equipos que necesitan grabación visual (HTTP Proxy)
- Testing de bases de datos directamente
- Organizaciones con procesos establecidos (legacy)
- Tests funcionales además de performance

❌ **Considerar alternativas si:**
- Necesitas máximo throughput (→ k6, Gatling)
- Prefieres código puro sobre GUI (→ k6, Locust)
- El equipo no quiere XML (→ k6, Gatling)
- Necesitas ejecución liviana en CI/CD (→ k6)
- Browser-level rendering (→ Playwright)

---

## 2. Arquitectura Interna

### Modelo de concurrencia

```
┌─────────────────────────────────────────────────────────────────┐
│                    JMETER ARCHITECTURE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │                    TEST PLAN (XML / .jmx)                │     │
│  └────────────────────────────┬────────────────────────────┘     │
│                               │                                   │
│  ┌────────────────────────────▼────────────────────────────┐     │
│  │                    JMETER ENGINE                          │     │
│  │                                                          │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐             │     │
│  │  │ Thread 1 │  │ Thread 2 │  │ Thread N │             │     │
│  │  │ (User 1) │  │ (User 2) │  │ (User N) │             │     │
│  │  │          │  │          │  │          │             │     │
│  │  │ Sampler  │  │ Sampler  │  │ Sampler  │             │     │
│  │  │ Timer    │  │ Timer    │  │ Timer    │             │     │
│  │  │ Assert   │  │ Assert   │  │ Assert   │             │     │
│  │  └──────────┘  └──────────┘  └──────────┘             │     │
│  │                                                          │     │
│  └──────────────────────────────────────────────────────────┘     │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │              RESULT COLLECTORS (Listeners)                 │    │
│  │  Summary Report │ Results Tree │ HTML Dashboard            │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

⚠️ IMPORTANTE: 1 Thread = 1 Virtual User = ~1 MB RAM
   1,000 users ≈ 1-2 GB RAM (+ overhead del test plan)
```

### Orden de ejecución de elementos

```
Para CADA Thread (Virtual User):

1. Configuration Elements (una vez al inicio)
   └── HTTP Defaults, CSV Data, Cookies, Cache

2. Pre-Processors (antes de cada Sampler)
   └── JSR223, User Parameters, HTML Link Parser

3. Timer (pausa antes del Sampler)
   └── Constant, Random, Gaussian, Throughput

4. Sampler (la request real)
   └── HTTP, JDBC, JMS, TCP, etc.

5. Post-Processors (después del Sampler)
   └── Regular Expression, JSON, XPath, CSS Extractors

6. Assertions (validar la respuesta)
   └── Response, Duration, JSON, Size

7. Listeners (recopilar resultados)
   └── Summary, Tree, Aggregate, HTML Report

SCOPE: Los elementos aplican a su nivel y todos los hijos
(un Timer en Thread Group aplica a TODOS los samplers dentro)
```

---

## 3. Instalación y Configuración

### Requisitos

```
- Java 8+ (Java 17 recomendado para JMeter 5.6+)
- RAM: mínimo 512 MB, recomendado 4-8 GB para tests grandes
- Disco: 200 MB para JMeter + espacio para resultados
```

### Instalación

```bash
# Descargar (Linux/Mac)
wget https://dlcdn.apache.org/jmeter/binaries/apache-jmeter-5.6.3.tgz
tar -xzf apache-jmeter-5.6.3.tgz
cd apache-jmeter-5.6.3

# Windows: descargar .zip y extraer
# https://jmeter.apache.org/download_jmeter.cgi

# Estructura del directorio
# ├── bin/
# │   ├── jmeter.sh / jmeter.bat         (GUI mode)
# │   ├── jmeter-server / jmeter-server.bat (distributed)
# │   ├── jmeter.properties               (configuración principal)
# │   └── user.properties                 (override de usuario)
# ├── lib/
# │   ├── ext/                            (plugins aquí)
# │   └── junit/                          (JUnit samplers)
# ├── extras/                             (Ant build files)
# └── docs/                               (documentación)
```

### Configuración clave (jmeter.properties)

```properties
# ══════════════════════════════════════════════════════════════
# jmeter.properties - Configuración optimizada para load testing
# ══════════════════════════════════════════════════════════════

# ─── HTTP ───
httpclient4.retrycount=0
httpclient.timeout=30000
httpsampler.max_redirects=5

# ─── Resultados ───
jmeter.save.saveservice.output_format=csv
jmeter.save.saveservice.response_data=false
jmeter.save.saveservice.samplerData=false
jmeter.save.saveservice.requestHeaders=false
jmeter.save.saveservice.responseHeaders=false
jmeter.save.saveservice.url=true
jmeter.save.saveservice.thread_counts=true
jmeter.save.saveservice.timestamp_format=ms

# ─── Distributed testing ───
remote_hosts=worker1:1099,worker2:1099,worker3:1099
server.rmi.ssl.disable=true
mode=Standard

# ─── Performance ───
summariser.interval=30
summariser.log=true
summariser.out=true
```

### user.properties (override por usuario/proyecto)

```properties
# user.properties - Propiedades específicas del proyecto

# Target
target.host=api.staging.example.com
target.port=443
target.protocol=https

# Test parameters
test.users=100
test.rampup=300
test.duration=1800
test.loops=-1

# Paths
test.datadir=data
test.reportdir=reports
```

---

## 4. Estructura del Test Plan

### Test Plan completo en XML (.jmx)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0" jmeter="5.6.3">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="E-Commerce Performance Test">
      <boolProp name="TestPlan.functional_mode">false</boolProp>
      <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>
      <elementProp name="TestPlan.user_defined_variables" elementType="Arguments">
        <collectionProp name="Arguments.arguments">
          <elementProp name="HOST" elementType="Argument">
            <stringProp name="Argument.name">HOST</stringProp>
            <stringProp name="Argument.value">${__P(target.host,api.example.com)}</stringProp>
          </elementProp>
          <elementProp name="PROTOCOL" elementType="Argument">
            <stringProp name="Argument.name">PROTOCOL</stringProp>
            <stringProp name="Argument.value">${__P(target.protocol,https)}</stringProp>
          </elementProp>
        </collectionProp>
      </elementProp>
    </TestPlan>
    <hashTree>
      <!-- Thread Groups, Samplers, etc. van aquí -->
    </hashTree>
  </hashTree>
</jmeterTestPlan>
```

### Jerarquía visual de elementos

```
Test Plan
├── User Defined Variables (HOST, PORT, TOKEN)
├── HTTP Request Defaults (base URL, timeouts)
├── HTTP Cookie Manager
├── HTTP Cache Manager
├── HTTP Header Manager
│
├── Thread Group: Browse Users (70%)
│   ├── CSV Data Set Config (users.csv)
│   ├── Transaction Controller: Login
│   │   ├── HTTP Request: POST /auth/login
│   │   │   ├── JSON Extractor ($.token → authToken)
│   │   │   └── Response Assertion (status = 200)
│   │   └── HTTP Header Manager (Authorization: Bearer ${authToken})
│   ├── Gaussian Random Timer (2000-8000ms)
│   ├── Loop Controller (5 iterations)
│   │   └── HTTP Request: GET /api/products
│   └── View Results Tree (DEBUG ONLY)
│
├── Thread Group: Purchase Users (30%)
│   ├── Once Only Controller
│   │   └── HTTP Request: POST /auth/login
│   ├── HTTP Request: POST /cart/add
│   ├── HTTP Request: POST /checkout
│   └── Duration Assertion (< 5000ms)
│
├── Thread Group: tearDown
│   └── HTTP Request: POST /admin/cleanup
│
└── Summary Report (Listener)
```

---

## 5. Thread Groups (Grupos de Hilos)

### Thread Group estándar

```xml
<ThreadGroup guiclass="ThreadGroupGui" testname="Standard Users">
  <!-- Número de virtual users -->
  <stringProp name="ThreadGroup.num_threads">${__P(test.users,100)}</stringProp>
  <!-- Ramp-up: tiempo para crear todos los threads -->
  <stringProp name="ThreadGroup.ramp_time">${__P(test.rampup,300)}</stringProp>
  <!-- Loops: -1 = infinito (usar con Scheduler) -->
  <intProp name="ThreadGroup.num_threads">100</intProp>
  <!-- Scheduler -->
  <boolProp name="ThreadGroup.scheduler">true</boolProp>
  <stringProp name="ThreadGroup.duration">${__P(test.duration,1800)}</stringProp>
  <stringProp name="ThreadGroup.delay">0</stringProp>
  <!-- Acción on error -->
  <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
  <!-- continue | startnextloop | stopthread | stoptest | stoptestnow -->
</ThreadGroup>
```

### Tipos de Thread Groups (con plugins)

```
┌──────────────────────────────────────────────────────────────────┐
│                    THREAD GROUP TYPES                              │
├────────────────────────┬─────────────────────────────────────────┤
│ TIPO                   │ USO                                      │
├────────────────────────┼─────────────────────────────────────────┤
│ Thread Group           │ Básico: N users, ramp-up, loops         │
│ (built-in)             │                                          │
├────────────────────────┼─────────────────────────────────────────┤
│ Stepping Thread Group  │ Escalera: agregar N users cada M seg    │
│ (plugin)               │ Ideal para encontrar breakpoints         │
├────────────────────────┼─────────────────────────────────────────┤
│ Ultimate Thread Group  │ Perfil complejo: múltiples rampas       │
│ (plugin)               │ con hold, ramp-up y ramp-down por tramo │
├────────────────────────┼─────────────────────────────────────────┤
│ Concurrency Thread Grp │ Mantiene N users concurrentes exactos   │
│ (plugin)               │ (reemplaza users que terminan)           │
├────────────────────────┼─────────────────────────────────────────┤
│ Arrivals Thread Group  │ Controla tasa de llegada (arrivals/sec) │
│ (plugin)               │ Modelo open (como Gatling)               │
├────────────────────────┼─────────────────────────────────────────┤
│ setUp Thread Group     │ Se ejecuta ANTES del test (prep data)   │
│ (built-in)             │                                          │
├────────────────────────┼─────────────────────────────────────────┤
│ tearDown Thread Group  │ Se ejecuta DESPUÉS del test (cleanup)   │
│ (built-in)             │                                          │
└────────────────────────┴─────────────────────────────────────────┘
```

### Ultimate Thread Group (configuración visual)

```
Ejemplo de perfil con Ultimate Thread Group:

Filas de configuración:
┌────────┬───────────┬──────────┬──────────┬───────────┬───────────┐
│ Threads│Start Delay│ Ramp-Up  │Hold Load │ Ramp-Down │ Perfil    │
├────────┼───────────┼──────────┼──────────┼───────────┼───────────┤
│ 50     │ 0s        │ 60s      │ 300s     │ 30s       │ Browsers  │
│ 30     │ 30s       │ 60s      │ 300s     │ 30s       │ Searchers │
│ 20     │ 60s       │ 120s     │ 300s     │ 60s       │ Buyers    │
└────────┴───────────┴──────────┴──────────┴───────────┴───────────┘

Timeline resultante:
Users
100 ─┐
     │         ┌────────────────────────┐
80  ─┤         │                        │
     │    ┌────┤                        ├───┐
50  ─┤    │    │                        │   │
     │ ┌──┤    │                        │   ├──┐
0   ─┤─┘  └────┘                        └───┘  └──
     0   60  120                        420  480  540  (seconds)
```

---

## 6. Samplers (Protocolos)

### HTTP Request Sampler

```xml
<HTTPSamplerProxy guiclass="HttpTestSampleGui" testname="GET Products">
  <stringProp name="HTTPSampler.domain">${HOST}</stringProp>
  <stringProp name="HTTPSampler.port">${PORT}</stringProp>
  <stringProp name="HTTPSampler.protocol">${PROTOCOL}</stringProp>
  <stringProp name="HTTPSampler.path">/api/v1/products</stringProp>
  <stringProp name="HTTPSampler.method">GET</stringProp>
  <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
  <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
  <stringProp name="HTTPSampler.connect_timeout">5000</stringProp>
  <stringProp name="HTTPSampler.response_timeout">30000</stringProp>
  <!-- Query Parameters -->
  <elementProp name="HTTPsampler.Arguments" elementType="Arguments">
    <collectionProp name="Arguments.arguments">
      <elementProp name="page" elementType="HTTPArgument">
        <stringProp name="Argument.name">page</stringProp>
        <stringProp name="Argument.value">${pageNum}</stringProp>
      </elementProp>
      <elementProp name="limit" elementType="HTTPArgument">
        <stringProp name="Argument.name">limit</stringProp>
        <stringProp name="Argument.value">20</stringProp>
      </elementProp>
    </collectionProp>
  </elementProp>
</HTTPSamplerProxy>
```

### HTTP POST con JSON Body

```xml
<HTTPSamplerProxy testname="POST Create Order">
  <stringProp name="HTTPSampler.path">/api/v1/orders</stringProp>
  <stringProp name="HTTPSampler.method">POST</stringProp>
  <boolProp name="HTTPSampler.postBodyRaw">true</boolProp>
  <elementProp name="HTTPsampler.Arguments" elementType="Arguments">
    <collectionProp name="Arguments.arguments">
      <elementProp name="" elementType="HTTPArgument">
        <stringProp name="Argument.value">
{
  "user_id": "${userId}",
  "items": [
    {"product_id": "${productId}", "quantity": ${quantity}}
  ],
  "shipping": "${shippingMethod}",
  "payment_token": "${paymentToken}"
}
        </stringProp>
      </elementProp>
    </collectionProp>
  </elementProp>
</HTTPSamplerProxy>
```

### Otros Samplers disponibles

| Sampler | Protocolo | Uso |
|---------|-----------|-----|
| HTTP Request | HTTP/HTTPS/HTTP2 | Web APIs, páginas web |
| JDBC Request | SQL databases | Queries directas a DB |
| JMS Publisher/Subscriber | JMS (ActiveMQ, RabbitMQ) | Message queues |
| TCP Sampler | TCP raw | Protocolos custom |
| SMTP Sampler | Email | Envío de emails |
| FTP Request | FTP/SFTP | Transferencia de archivos |
| LDAP Request | LDAP | Directorio services |
| Java Request | Java classes | Custom samplers |
| JSR223 Sampler | Cualquiera | Código Groovy/Java |
| OS Process Sampler | CLI | Ejecutar comandos |
| Debug Sampler | N/A | Ver variables (debug) |

---

## 7. Config Elements

### HTTP Request Defaults

```xml
<!-- Aplica a TODOS los HTTP Requests dentro del scope -->
<ConfigTestElement guiclass="HttpDefaultsGui" testname="HTTP Defaults">
  <stringProp name="HTTPSampler.domain">${HOST}</stringProp>
  <stringProp name="HTTPSampler.port">${PORT}</stringProp>
  <stringProp name="HTTPSampler.protocol">${PROTOCOL}</stringProp>
  <stringProp name="HTTPSampler.connect_timeout">5000</stringProp>
  <stringProp name="HTTPSampler.response_timeout">30000</stringProp>
  <stringProp name="HTTPSampler.implementation">HttpClient4</stringProp>
</ConfigTestElement>
```

### HTTP Header Manager

```xml
<HeaderManager guiclass="HeaderPanel" testname="API Headers">
  <collectionProp name="HeaderManager.headers">
    <elementProp name="" elementType="Header">
      <stringProp name="Header.name">Content-Type</stringProp>
      <stringProp name="Header.value">application/json</stringProp>
    </elementProp>
    <elementProp name="" elementType="Header">
      <stringProp name="Header.name">Accept</stringProp>
      <stringProp name="Header.value">application/json</stringProp>
    </elementProp>
    <elementProp name="" elementType="Header">
      <stringProp name="Header.name">Authorization</stringProp>
      <stringProp name="Header.value">Bearer ${authToken}</stringProp>
    </elementProp>
    <elementProp name="" elementType="Header">
      <stringProp name="Header.name">X-Request-ID</stringProp>
      <stringProp name="Header.value">${__UUID()}</stringProp>
    </elementProp>
  </collectionProp>
</HeaderManager>
```

### HTTP Cookie Manager

```xml
<!-- Gestiona cookies automáticamente (como un browser) -->
<CookieManager guiclass="CookiePanel" testname="Cookie Manager">
  <boolProp name="CookieManager.clearEachIteration">false</boolProp>
  <boolProp name="CookieManager.controlledByThreadGroup">true</boolProp>
  <stringProp name="CookieManager.policy">standard</stringProp>
  <!-- Policies: standard, netscape, ignoreCookies, default -->
</CookieManager>
```

### HTTP Cache Manager

```xml
<!-- Simula cache del browser -->
<CacheManager guiclass="CacheManagerGui" testname="Cache Manager">
  <boolProp name="clearEachIteration">true</boolProp>
  <boolProp name="useExpires">true</boolProp>
  <intProp name="maxSize">5000</intProp>
</CacheManager>
```

---

## 8. Pre-Processors y Post-Processors

### JSR223 PreProcessor (Groovy)

```groovy
// Generar datos dinámicos antes del request
import java.util.UUID
import java.time.Instant

// Generar request ID único
vars.put("requestId", UUID.randomUUID().toString())

// Timestamp ISO
vars.put("timestamp", Instant.now().toString())

// Calcular HMAC signature
import javax.crypto.Mac
import javax.crypto.spec.SecretKeySpec

def secret = "my-api-secret"
def message = vars.get("requestId") + vars.get("timestamp")
def mac = Mac.getInstance("HmacSHA256")
mac.init(new SecretKeySpec(secret.getBytes(), "HmacSHA256"))
def signature = mac.doFinal(message.getBytes()).encodeHex().toString()
vars.put("signature", signature)

// Random data
def random = new Random()
vars.put("randomAmount", String.valueOf(random.nextInt(10000) / 100.0))
```

### JSR223 PostProcessor (Groovy)

```groovy
// Procesar respuesta después del request
import groovy.json.JsonSlurper

def response = prev.getResponseDataAsString()
def json = new JsonSlurper().parseText(response)

// Extraer y transformar datos
if (json.items) {
    // Guardar lista de IDs
    def ids = json.items.collect { it.id }
    vars.put("itemCount", ids.size().toString())
    
    // Guardar como lista para ForEach Controller
    ids.eachWithIndex { id, idx ->
        vars.put("itemId_${idx + 1}", id)
    }
    vars.put("itemId_matchNr", ids.size().toString())
    
    // Seleccionar uno aleatorio
    def randomId = ids[new Random().nextInt(ids.size())]
    vars.put("selectedItemId", randomId)
}

// Log para debug
log.info("Extracted ${vars.get('itemCount')} items")
```

---

## 9. Extractors y Correlation

### JSON Extractor (JSONPath)

```xml
<JSONPostProcessor guiclass="JSONPostProcessorGui" testname="Extract Token">
  <stringProp name="JSONPostProcessor.referenceNames">authToken</stringProp>
  <stringProp name="JSONPostProcessor.jsonPathExprs">$.access_token</stringProp>
  <stringProp name="JSONPostProcessor.match_numbers">1</stringProp>
  <!-- match_numbers: 1=first, 0=random, -1=all, N=Nth -->
  <stringProp name="JSONPostProcessor.defaultValues">TOKEN_NOT_FOUND</stringProp>
</JSONPostProcessor>

<!-- Extraer múltiples valores -->
<JSONPostProcessor testname="Extract User Data">
  <stringProp name="JSONPostProcessor.referenceNames">userId;userName;userEmail</stringProp>
  <stringProp name="JSONPostProcessor.jsonPathExprs">$.user.id;$.user.name;$.user.email</stringProp>
  <stringProp name="JSONPostProcessor.match_numbers">1;1;1</stringProp>
  <stringProp name="JSONPostProcessor.defaultValues">;;;</stringProp>
</JSONPostProcessor>

<!-- Extraer todos los IDs de un array -->
<JSONPostProcessor testname="Extract All Product IDs">
  <stringProp name="JSONPostProcessor.referenceNames">productId</stringProp>
  <stringProp name="JSONPostProcessor.jsonPathExprs">$.products[*].id</stringProp>
  <stringProp name="JSONPostProcessor.match_numbers">-1</stringProp>
  <!-- Resultado: productId_1, productId_2, ..., productId_matchNr -->
</JSONPostProcessor>
```

### Regular Expression Extractor

```xml
<RegexExtractor guiclass="RegexExtractorGui" testname="Extract CSRF Token">
  <stringProp name="RegexExtractor.useHeaders">false</stringProp>
  <!-- false=body, true=headers, URL, code, message -->
  <stringProp name="RegexExtractor.refname">csrfToken</stringProp>
  <stringProp name="RegexExtractor.regex">name="csrf_token" value="([^"]+)"</stringProp>
  <stringProp name="RegexExtractor.template">$1$</stringProp>
  <stringProp name="RegexExtractor.match_nr">1</stringProp>
  <stringProp name="RegexExtractor.default">CSRF_NOT_FOUND</stringProp>
</RegexExtractor>
```

### XPath Extractor (para XML/HTML)

```xml
<XPathExtractor guiclass="XPathExtractorGui" testname="Extract from XML">
  <stringProp name="XPathExtractor.refname">orderId</stringProp>
  <stringProp name="XPathExtractor.xpathQuery">//order/id/text()</stringProp>
  <stringProp name="XPathExtractor.default">ORDER_NOT_FOUND</stringProp>
  <boolProp name="XPathExtractor.tolerant">true</boolProp>
</XPathExtractor>
```

### Boundary Extractor (simple y rápido)

```xml
<BoundaryExtractor testname="Extract Session ID">
  <stringProp name="BoundaryExtractor.refname">sessionId</stringProp>
  <stringProp name="BoundaryExtractor.lboundary">session_id=</stringProp>
  <stringProp name="BoundaryExtractor.rboundary">;</stringProp>
  <stringProp name="BoundaryExtractor.match_number">1</stringProp>
  <stringProp name="BoundaryExtractor.default">SESSION_NOT_FOUND</stringProp>
</BoundaryExtractor>
```

### Correlation completa (flujo ejemplo)

```
┌─────────────────────────────────────────────────────────────────┐
│                    CORRELATION FLOW                               │
│                                                                   │
│  Request 1: POST /auth/login                                     │
│  Response: {"token": "eyJ...", "user_id": "U123"}               │
│  Extract: authToken = eyJ..., userId = U123                      │
│                          │                                        │
│                          ▼                                        │
│  Request 2: GET /api/users/${userId}/profile                     │
│  Header: Authorization: Bearer ${authToken}                      │
│  Response: {"cart_id": "C456", "items": [...]}                  │
│  Extract: cartId = C456                                          │
│                          │                                        │
│                          ▼                                        │
│  Request 3: POST /api/carts/${cartId}/checkout                  │
│  Header: Authorization: Bearer ${authToken}                      │
│  Body: {"cart_id": "${cartId}", "user_id": "${userId}"}        │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10. Assertions (Validaciones)

### Response Assertion

```xml
<!-- Verificar contenido del response -->
<ResponseAssertion guiclass="AssertionGui" testname="Verify Success">
  <stringProp name="Assertion.test_field">Assertion.response_data</stringProp>
  <!-- response_data, response_code, response_message, response_headers -->
  <intProp name="Assertion.test_type">2</intProp>
  <!-- 1=Match, 2=Contains, 8=Equals, 16=Substring, NOT=4 -->
  <collectionProp name="Asserion.test_strings">
    <stringProp name="0">"status":"success"</stringProp>
  </collectionProp>
</ResponseAssertion>

<!-- Verificar status code -->
<ResponseAssertion testname="Status 200">
  <stringProp name="Assertion.test_field">Assertion.response_code</stringProp>
  <intProp name="Assertion.test_type">8</intProp>
  <collectionProp name="Asserion.test_strings">
    <stringProp name="0">200</stringProp>
  </collectionProp>
</ResponseAssertion>
```

### Duration Assertion

```xml
<!-- Response time máximo permitido -->
<DurationAssertion guiclass="DurationAssertionGui" testname="Max 3 seconds">
  <stringProp name="DurationAssertion.duration">3000</stringProp>
</DurationAssertion>
```

### JSON Assertion

```xml
<JSONPathAssertion guiclass="JSONPathAssertionGui" testname="Verify JSON">
  <stringProp name="JSON_PATH">$.data.items</stringProp>
  <stringProp name="EXPECTED_VALUE"></stringProp>
  <boolProp name="JSONVALIDATION">false</boolProp>
  <boolProp name="EXPECT_NULL">false</boolProp>
  <boolProp name="INVERT">false</boolProp>
  <boolProp name="ISREGEX">false</boolProp>
</JSONPathAssertion>
```

### JSR223 Assertion (Custom con Groovy)

```groovy
// JSR223 Assertion - validación compleja
import groovy.json.JsonSlurper

def response = prev.getResponseDataAsString()
def responseTime = prev.getTime()

// Validar estructura JSON
try {
    def json = new JsonSlurper().parseText(response)
    
    // Validar campos requeridos
    assert json.data != null : "Missing 'data' field"
    assert json.data.id != null : "Missing 'data.id' field"
    assert json.data.items instanceof List : "'items' must be a list"
    assert json.data.items.size() > 0 : "'items' must not be empty"
    
    // Validar business logic
    def total = json.data.items.sum { it.price * it.quantity }
    assert Math.abs(total - json.data.total) < 0.01 : 
        "Total mismatch: calculated=${total}, response=${json.data.total}"
    
    // Validar response time
    if (responseTime > 5000) {
        AssertionResult.setFailure(true)
        AssertionResult.setFailureMessage("Response too slow: ${responseTime}ms")
    }
    
} catch (Exception e) {
    AssertionResult.setFailure(true)
    AssertionResult.setFailureMessage("Validation error: ${e.message}")
}
```

---

## 11. Timers (Think Time)

### Constant Timer

```xml
<!-- Pausa fija de 3 segundos -->
<ConstantTimer guiclass="ConstantTimerGui" testname="3s Think Time">
  <stringProp name="ConstantTimer.delay">3000</stringProp>
</ConstantTimer>
```

### Uniform Random Timer

```xml
<!-- Random entre 2000 y 5000ms (offset + random 0 a max) -->
<UniformRandomTimer testname="Random 2-5s">
  <stringProp name="ConstantTimer.delay">2000</stringProp>
  <stringProp name="RandomTimer.range">3000</stringProp>
  <!-- Total: 2000 + random(0, 3000) = 2000-5000ms -->
</UniformRandomTimer>
```

### Gaussian Random Timer

```xml
<!-- Distribución gaussiana (más realista) -->
<GaussianRandomTimer testname="Gaussian Think Time">
  <stringProp name="ConstantTimer.delay">3000</stringProp>
  <stringProp name="RandomTimer.range">1000</stringProp>
  <!-- Media: 3000ms, Desviación: 1000ms -->
</GaussianRandomTimer>
```

### Precise Throughput Timer (Plugin)

```
Controla throughput EXACTO independientemente del número de threads.

Configuración:
- Target throughput: 100 samples/sec
- Throughput period: 60 sec (ventana de cálculo)
- Duration: test duration

Comportamiento:
- Si los threads terminan rápido → agrega delay
- Si los threads son lentos → reduce delay
- Garantiza tasa exacta de requests/segundo
```

### Synchronizing Timer (Rendezvous Point)

```xml
<!-- Acumula threads y los libera todos juntos -->
<SyncTimer guiclass="TestBeanGUI" testname="Rendezvous">
  <!-- Número de threads a acumular antes de liberar -->
  <intProp name="groupSize">50</intProp>
  <!-- Timeout en ms (0 = esperar indefinidamente) -->
  <longProp name="timeoutInMs">10000</longProp>
</SyncTimer>

<!-- Uso: simular pico de concurrencia simultánea
     Todos los threads llegan aquí → esperan →
     se liberan TODOS al mismo tiempo → pico de carga -->
```

---

## 12. Logic Controllers

### Controladores principales

```
┌──────────────────────────────────────────────────────────────────┐
│                    LOGIC CONTROLLERS                               │
├────────────────────────┬─────────────────────────────────────────┤
│ Controller             │ Función                                  │
├────────────────────────┼─────────────────────────────────────────┤
│ Simple Controller      │ Agrupa elementos (organizativo)          │
│ Loop Controller        │ Repite N veces                           │
│ While Controller       │ Repite mientras condición=true           │
│ ForEach Controller     │ Itera sobre variables numeradas          │
│ If Controller          │ Ejecuta si condición=true                │
│ Switch Controller      │ Selecciona hijo por índice               │
│ Random Controller      │ Ejecuta un hijo aleatorio                │
│ Random Order Controller│ Ejecuta todos en orden random            │
│ Throughput Controller  │ Ejecuta solo un % de veces               │
│ Once Only Controller   │ Ejecuta solo en primera iteración        │
│ Transaction Controller │ Agrupa requests para métricas            │
│ Interleave Controller  │ Round-robin entre hijos                  │
│ Module Controller      │ Referencia a Test Fragment               │
│ Runtime Controller     │ Ejecuta durante N segundos               │
│ Critical Section       │ Mutex (un thread a la vez)               │
└────────────────────────┴─────────────────────────────────────────┘
```

### Transaction Controller (agrupación de métricas)

```xml
<!-- Agrupa varios requests bajo un nombre para reporting -->
<TransactionController guiclass="TransactionControllerGui" 
                       testname="Checkout Flow">
  <boolProp name="TransactionController.includeTimers">false</boolProp>
  <boolProp name="TransactionController.parent">true</boolProp>
  <!-- parent=true: genera un sample padre con el tiempo total -->
</TransactionController>
<!-- Hijos: Add to Cart + Apply Coupon + Submit Payment + Confirm -->
<!-- Resultado: "Checkout Flow" con tiempo total de toda la transacción -->
```

### If Controller

```xml
<IfController guiclass="IfControllerPanel" testname="If Admin">
  <stringProp name="IfController.condition">
    ${__groovy(vars.get("userRole") == "admin")}
  </stringProp>
  <boolProp name="IfController.evaluateAll">false</boolProp>
  <boolProp name="IfController.useExpression">true</boolProp>
</IfController>
```

### ForEach Controller

```xml
<!-- Itera sobre variables extraídas: productId_1, productId_2, ... -->
<ForeachController guiclass="ForeachControlPanel" testname="For Each Product">
  <stringProp name="ForeachController.inputVal">productId</stringProp>
  <stringProp name="ForeachController.returnVal">currentProductId</stringProp>
  <boolProp name="ForeachController.useSeparator">true</boolProp>
  <stringProp name="ForeachController.startIndex">0</stringProp>
  <stringProp name="ForeachController.endIndex"></stringProp>
</ForeachController>
<!-- Dentro: HTTP Request usando ${currentProductId} -->
```

### While Controller

```xml
<WhileController guiclass="WhileControllerGui" testname="Poll Until Ready">
  <stringProp name="WhileController.condition">
    ${__groovy(vars.get("jobStatus") != "completed" && vars.get("pollCount").toInteger() < 20)}
  </stringProp>
</WhileController>
<!-- Dentro: GET /job/status + JSR223 to increment pollCount + Timer 5s -->
```

---

## 13. Listeners (Reportes)

### Listeners disponibles

| Listener | Uso en producción | Descripción |
|----------|:-----------------:|-------------|
| View Results Tree | ❌ Debug only | Muestra request/response completo |
| Summary Report | ✅ | Tabla resumen por sampler |
| Aggregate Report | ✅ | Percentiles, throughput, error % |
| Backend Listener | ✅ | Envía a InfluxDB/Graphite en real-time |
| Simple Data Writer | ✅ | Escribe .jtl para post-análisis |
| Generate Summary Results | ✅ | Output en consola (CLI mode) |
| Response Time Graph | ❌ | Solo GUI, alto consumo |
| Graph Results | ❌ | Solo GUI, impreciso |

### Backend Listener (InfluxDB)

```xml
<BackendListener guiclass="BackendListenerGui" testname="InfluxDB Writer">
  <stringProp name="classname">
    org.apache.jmeter.visualizers.backend.influxdb.InfluxdbBackendListenerClient
  </stringProp>
  <elementProp name="arguments" elementType="Arguments">
    <collectionProp name="Arguments.arguments">
      <elementProp name="influxdbUrl" elementType="Argument">
        <stringProp name="Argument.value">http://influxdb:8086/write?db=jmeter</stringProp>
      </elementProp>
      <elementProp name="application" elementType="Argument">
        <stringProp name="Argument.value">ecommerce-api</stringProp>
      </elementProp>
      <elementProp name="measurement" elementType="Argument">
        <stringProp name="Argument.value">jmeter</stringProp>
      </elementProp>
      <elementProp name="summaryOnly" elementType="Argument">
        <stringProp name="Argument.value">false</stringProp>
      </elementProp>
      <elementProp name="samplersRegex" elementType="Argument">
        <stringProp name="Argument.value">.*</stringProp>
      </elementProp>
      <elementProp name="testTitle" elementType="Argument">
        <stringProp name="Argument.value">Load Test ${__time(yyyy-MM-dd HH:mm)}</stringProp>
      </elementProp>
    </collectionProp>
  </elementProp>
</BackendListener>
```

---

## 14. Scripting (JSR223 / Groovy)

### ¿Por qué Groovy?

```
Performance comparison (iterations/sec):
┌──────────────┬───────────────┐
│ Lenguaje     │ Rendimiento   │
├──────────────┼───────────────┤
│ Groovy       │ 100% (base)   │  ← RECOMENDADO
│ Java (JSR223)│ ~95%          │
│ JavaScript   │ ~60%          │
│ BeanShell    │ ~15%          │  ← EVITAR
└──────────────┴───────────────┘

⚠️ REGLA: SIEMPRE usar Groovy + "Compile and cache" activado
```

### JSR223 Sampler (request custom)

```groovy
// JSR223 Sampler - Request custom completo
import groovy.json.JsonOutput
import groovy.json.JsonSlurper
import java.net.http.HttpClient
import java.net.http.HttpRequest
import java.net.http.HttpResponse

// Construir request
def client = HttpClient.newBuilder()
    .connectTimeout(java.time.Duration.ofSeconds(5))
    .build()

def body = JsonOutput.toJson([
    action: "complex_operation",
    user_id: vars.get("userId"),
    timestamp: System.currentTimeMillis(),
    data: [
        items: (1..5).collect { [id: it, quantity: new Random().nextInt(3) + 1] }
    ]
])

def request = HttpRequest.newBuilder()
    .uri(URI.create("${vars.get('PROTOCOL')}://${vars.get('HOST')}/api/v2/operations"))
    .header("Authorization", "Bearer ${vars.get('authToken')}")
    .header("Content-Type", "application/json")
    .POST(HttpRequest.BodyPublishers.ofString(body))
    .build()

// Ejecutar
def startTime = System.currentTimeMillis()
def response = client.send(request, HttpResponse.BodyHandlers.ofString())
def duration = System.currentTimeMillis() - startTime

// Reportar a JMeter
SampleResult.setResponseCode(response.statusCode().toString())
SampleResult.setResponseData(response.body(), "UTF-8")
SampleResult.setSuccessful(response.statusCode() == 200)
SampleResult.setResponseMessage(response.statusCode() == 200 ? "OK" : "Error")
SampleResult.setLatency(duration)

// Extraer datos para próximos requests
if (response.statusCode() == 200) {
    def json = new JsonSlurper().parseText(response.body())
    vars.put("operationId", json.operation_id)
}
```

### Funciones JMeter más usadas

```
┌──────────────────────────────────────────────────────────────────┐
│                    JMETER FUNCTIONS                                │
├────────────────────────────┬─────────────────────────────────────┤
│ Función                    │ Ejemplo                              │
├────────────────────────────┼─────────────────────────────────────┤
│ ${__UUID()}                │ Genera UUID aleatorio                │
│ ${__time()}                │ Timestamp actual (ms)                │
│ ${__time(yyyy-MM-dd)}      │ Fecha formateada                    │
│ ${__Random(1,100,var)}     │ Número aleatorio 1-100              │
│ ${__RandomString(10)}      │ String aleatorio 10 chars           │
│ ${__threadNum}             │ Número del thread actual             │
│ ${__iterationNum}          │ Número de iteración                  │
│ ${__P(prop,default)}       │ Leer property                        │
│ ${__setProperty(name,val)} │ Escribir property (cross-thread)    │
│ ${__counter(TRUE)}         │ Contador per-thread                  │
│ ${__counter(FALSE)}        │ Contador global                      │
│ ${__CSVRead(file,col)}     │ Leer CSV sin CSVDataSet             │
│ ${__groovy(code)}          │ Ejecutar Groovy inline              │
│ ${__jexl3(expression)}     │ Ejecutar JEXL expression            │
│ ${__base64Encode(text)}    │ Encode a base64                     │
│ ${__base64Decode(text)}    │ Decode de base64                    │
│ ${__digest(SHA-256,text)}  │ Hash SHA-256                        │
│ ${__char(10)}              │ Carácter especial (newline)         │
│ ${__escapeHtml(text)}      │ Escape HTML entities                │
└────────────────────────────┴─────────────────────────────────────┘
```

---

## 15. Parametrización y Data Driven Testing

### CSV Data Set Config

```xml
<CSVDataSet guiclass="TestBeanGUI" testname="User Data">
  <stringProp name="filename">data/users.csv</stringProp>
  <stringProp name="variableNames">email,password,firstName,lastName</stringProp>
  <stringProp name="delimiter">,</stringProp>
  <stringProp name="fileEncoding">UTF-8</stringProp>
  <boolProp name="ignoreFirstLine">true</boolProp>
  <boolProp name="quotedData">true</boolProp>
  <stringProp name="recycle">true</stringProp>
  <stringProp name="stopThread">false</stringProp>
  <stringProp name="shareMode">shareMode.all</stringProp>
  <!-- shareMode: all (todos comparten), group, thread -->
</CSVDataSet>

<!-- CSV file (data/users.csv):
email,password,firstName,lastName
user1@test.com,Pass123!,John,Doe
user2@test.com,Pass456!,Jane,Smith
user3@test.com,Pass789!,Bob,Johnson
-->
```

### Share Modes explicados

```
┌─────────────────────────────────────────────────────────────────┐
│ SHARE MODE     │ COMPORTAMIENTO                                  │
├────────────────┼────────────────────────────────────────────────┤
│ All threads    │ TODOS los threads comparten el mismo cursor     │
│ (shareMode.all)│ Thread 1 → fila 1, Thread 2 → fila 2, etc.   │
│                │ Cada fila se usa UNA vez (hasta recycle)        │
│                │ ✅ Datos únicos por request                     │
├────────────────┼────────────────────────────────────────────────┤
│ Current group  │ Threads del MISMO Thread Group comparten        │
│ (shareMode.    │ Diferentes Thread Groups tienen cursor propio   │
│  group)        │ ✅ Datos únicos dentro del grupo                │
├────────────────┼────────────────────────────────────────────────┤
│ Current thread │ Cada thread tiene su PROPIO cursor              │
│ (shareMode.    │ Thread 1 → fila 1,1,1... Thread 2 → fila 1,1..│
│  thread)       │ ✅ Mismo usuario repite sus datos               │
└────────────────┴────────────────────────────────────────────────┘
```

---

## 16. Testing Distribuido

### Arquitectura Master-Slave

```
┌─────────────────────────────────────────────────────────────────┐
│                    DISTRIBUTED TESTING                            │
│                                                                   │
│  ┌──────────────────────┐                                        │
│  │      MASTER          │  Controla el test                      │
│  │  (tu máquina / CI)   │  Agrega resultados                    │
│  │                      │  Genera reportes                       │
│  └──────────┬───────────┘                                        │
│             │ RMI (port 1099)                                    │
│    ┌────────┼────────┬────────────┐                              │
│    │        │        │            │                               │
│  ┌─▼──┐  ┌─▼──┐  ┌──▼─┐  ┌────▼───┐                           │
│  │Slave│  │Slave│  │Slave│  │Slave   │  Ejecutan la carga       │
│  │ 1   │  │ 2  │  │ 3  │  │ N      │  cada uno genera N users │
│  └─────┘  └─────┘  └─────┘  └────────┘                          │
│                                                                   │
│  Si Master configura 1000 users y hay 4 slaves:                  │
│  → Cada slave ejecuta 250 users                                  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Configuración

```bash
# EN CADA SLAVE:
# 1. Instalar JMeter (misma versión que Master)
# 2. Copiar plugins y test data
# 3. Iniciar servidor:
./bin/jmeter-server

# EN EL MASTER:
# 1. Configurar remote_hosts en jmeter.properties:
remote_hosts=192.168.1.101:1099,192.168.1.102:1099,192.168.1.103:1099

# 2. Ejecutar test distribuido (CLI):
./bin/jmeter -n -t test_plan.jmx -r \
  -l results.jtl \
  -e -o reports/

# O con hosts específicos:
./bin/jmeter -n -t test_plan.jmx \
  -R 192.168.1.101,192.168.1.102 \
  -l results.jtl
```

### Consideraciones para testing distribuido

```
✅ HACER:
- Misma versión de JMeter en todos los nodos
- Sincronizar reloj (NTP) entre todos los nodos
- Copiar datos (CSV, JSON) a cada slave
- Usar ruta relativa para archivos
- Deshabilitar SSL para RMI en testing interno:
  server.rmi.ssl.disable=true

❌ EVITAR:
- Listeners gráficos en slaves
- Archivos de resultado locales en slaves (centralizar en master)
- Diferentes versiones de plugins
- Firewalls bloqueando RMI (1099) y puertos dinámicos
```

---

## 17. Ejecución en Modo CLI (Non-GUI)

### Comando básico

```bash
# Ejecución básica
jmeter -n -t test_plan.jmx -l results.jtl

# Con generación de reporte HTML
jmeter -n -t test_plan.jmx -l results.jtl -e -o reports/html/

# Con properties
jmeter -n -t test_plan.jmx -l results.jtl \
  -Jtarget.host=api.staging.com \
  -Jtest.users=200 \
  -Jtest.rampup=300 \
  -Jtest.duration=1800

# Con log file
jmeter -n -t test_plan.jmx -l results.jtl \
  -j logs/jmeter.log \
  -e -o reports/

# Opciones completas
jmeter \
  -n                              # Non-GUI mode
  -t test_plan.jmx               # Test plan file
  -l results/results.jtl         # Results file
  -j logs/jmeter.log             # JMeter log
  -e                              # Generate report after test
  -o reports/dashboard/           # Report output directory
  -Jproperty=value               # Set JMeter property
  -Gproperty=value               # Set property on ALL remote servers
  -r                              # Run remote servers
  -R server1,server2             # Specific remote servers
  -H proxy_host                   # Proxy host
  -P proxy_port                   # Proxy port
```

### Optimización de JVM para CLI

```bash
# Editar bin/jmeter (Linux) o bin/jmeter.bat (Windows)
# Configurar HEAP:

# Linux/Mac (bin/jmeter):
HEAP="-Xms2g -Xmx4g -XX:MaxMetaspaceSize=512m"

# Windows (bin/jmeter.bat):
set HEAP=-Xms2g -Xmx4g -XX:MaxMetaspaceSize=512m

# Recomendaciones por número de threads:
# 100-500 threads:   -Xmx2g
# 500-1000 threads:  -Xmx4g
# 1000-2000 threads: -Xmx8g
# 2000+ threads:     -Xmx16g + distributed
```

---

## 18. Plugins Esenciales

### Instalación del Plugin Manager

```bash
# Descargar plugin manager JAR
curl -L -o lib/ext/jmeter-plugins-manager-1.10.jar \
  https://jmeter-plugins.org/get/

# Reiniciar JMeter → Options → Plugins Manager
# O instalar desde CLI:
java -jar lib/cmdrunner-2.3.jar \
  --tool org.jmeterplugins.repository.PluginManagerCMDInstaller

# Instalar plugins desde CLI:
./bin/PluginsManagerCMD.sh install \
  jpgc-casutg,jpgc-tst,jpgc-perfmon,jpgc-graphs-basic,jpgc-graphs-additional
```

### Plugins recomendados

| Plugin ID | Nombre | Uso |
|-----------|--------|-----|
| `jpgc-casutg` | Custom Thread Groups | Ultimate, Stepping, Concurrency TG |
| `jpgc-tst` | Throughput Shaping Timer | Control preciso de TPS |
| `jpgc-perfmon` | PerfMon Metrics Collector | Monitoreo de servidores |
| `jpgc-graphs-basic` | Basic Graphs | Gráficos en tiempo real |
| `jpgc-graphs-additional` | Additional Graphs | Response times, TPS graphs |
| `jpgc-cmd` | Command-Line Graph Rendering | Generar gráficos desde CLI |
| `jpgc-synthesis` | Filter Results | Filtrar y analizar resultados |
| `jpgc-dummy` | Dummy Sampler | Testing del test plan |
| `jpgc-functions` | Custom Functions | Funciones adicionales |
| `jpgc-json` | JSON Plugins | JSON Path Assertion mejorado |
| `jpgc-webdriver` | WebDriver Sampler | Browser real (Selenium) |

### Throughput Shaping Timer (control de TPS)

```
Configuración (tabla de steps):
┌──────────────────┬──────────┬──────────┬──────────┐
│ Start RPS        │ End RPS  │ Duration │ Resultado│
├──────────────────┼──────────┼──────────┼──────────┤
│ 0                │ 50       │ 120s     │ Ramp-up  │
│ 50               │ 50       │ 600s     │ Hold     │
│ 50               │ 200      │ 180s     │ Ramp     │
│ 200              │ 200      │ 300s     │ Peak     │
│ 200              │ 0        │ 60s      │ Ramp-down│
└──────────────────┴──────────┴──────────┴──────────┘

IMPORTANTE: Combinar con Concurrency Thread Group
que auto-ajusta el número de threads necesarios.
```

---

## 19. Protocolos Avanzados (JDBC, JMS, SMTP)

### JDBC Request (Base de datos)

```xml
<!-- JDBC Connection Configuration -->
<JDBCDataSource guiclass="TestBeanGUI" testname="PostgreSQL Connection">
  <stringProp name="dataSource">pgPool</stringProp>
  <stringProp name="dbUrl">jdbc:postgresql://db.example.com:5432/testdb</stringProp>
  <stringProp name="driver">org.postgresql.Driver</stringProp>
  <stringProp name="username">${__P(db.user,perftest)}</stringProp>
  <stringProp name="password">${__P(db.pass,secret)}</stringProp>
  <stringProp name="poolMax">10</stringProp>
  <stringProp name="timeout">10000</stringProp>
  <stringProp name="autocommit">true</stringProp>
</JDBCDataSource>

<!-- JDBC Request -->
<JDBCSampler guiclass="TestBeanGUI" testname="Query Products">
  <stringProp name="dataSource">pgPool</stringProp>
  <stringProp name="queryType">Select Statement</stringProp>
  <stringProp name="query">
    SELECT id, name, price, stock 
    FROM products 
    WHERE category = ? AND price BETWEEN ? AND ?
    ORDER BY ${sortColumn} ${sortDirection}
    LIMIT 20 OFFSET ?
  </stringProp>
  <stringProp name="queryArguments">${category},${minPrice},${maxPrice},${offset}</stringProp>
  <stringProp name="queryArgumentsTypes">VARCHAR,DECIMAL,DECIMAL,INTEGER</stringProp>
  <stringProp name="variableNames">id,name,price,stock</stringProp>
  <stringProp name="resultVariable">queryResults</stringProp>
</JDBCSampler>
```

### JMS Point-to-Point

```xml
<!-- JNDI Configuration for ActiveMQ -->
<JMSSampler guiclass="JMSSamplerGui" testname="Send Order Message">
  <stringProp name="JMSSampler.queueConnectionFactory">ConnectionFactory</stringProp>
  <stringProp name="JMSSampler.SendQueue">orders.input</stringProp>
  <stringProp name="JMSSampler.ReceiveQueue">orders.reply</stringProp>
  <boolProp name="JMSSampler.isNonPersistent">false</boolProp>
  <stringProp name="JMSSampler.timeout">5000</stringProp>
  <!-- Contenido del mensaje -->
  <stringProp name="HTTPSampler.xml_data">
    {"order_id": "${orderId}", "amount": ${amount}, "user": "${userId}"}
  </stringProp>
</JMSSampler>
```

---

## 20. Integración con CI/CD

### GitHub Actions

```yaml
name: Performance Test (JMeter)

on:
  schedule:
    - cron: '0 5 * * 1-5'
  workflow_dispatch:
    inputs:
      users:
        description: 'Number of users'
        default: '100'
      duration:
        description: 'Duration in seconds'
        default: '600'

jobs:
  jmeter-test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'
      
      - name: Install JMeter
        run: |
          wget -q https://dlcdn.apache.org/jmeter/binaries/apache-jmeter-5.6.3.tgz
          tar -xzf apache-jmeter-5.6.3.tgz
          echo "JMETER_HOME=$(pwd)/apache-jmeter-5.6.3" >> $GITHUB_ENV
          echo "$(pwd)/apache-jmeter-5.6.3/bin" >> $GITHUB_PATH
      
      - name: Install Plugins
        run: |
          cd $JMETER_HOME
          wget -q -O lib/ext/jmeter-plugins-manager-1.10.jar \
            https://jmeter-plugins.org/get/
          java -jar lib/cmdrunner-2.3.jar \
            --tool org.jmeterplugins.repository.PluginManagerCMDInstaller
          ./bin/PluginsManagerCMD.sh install jpgc-casutg,jpgc-tst
      
      - name: Run JMeter Test
        run: |
          jmeter -n \
            -t tests/performance/load_test.jmx \
            -l results/results.jtl \
            -e -o results/dashboard/ \
            -Jtarget.host=${{ secrets.STAGING_HOST }} \
            -Jtest.users=${{ inputs.users || '100' }} \
            -Jtest.duration=${{ inputs.duration || '600' }} \
            -Xmx4g
      
      - name: Check Results
        run: |
          # Parse JTL and check thresholds
          python scripts/check_jmeter_results.py \
            --jtl results/results.jtl \
            --p95-max 2000 \
            --error-max 1.0
      
      - name: Upload Report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: jmeter-report-${{ github.run_id }}
          path: results/dashboard/
```

---

## 21. HTML Dashboard Report

### Generación

```bash
# Generar durante el test
jmeter -n -t test.jmx -l results.jtl -e -o report/

# Generar desde JTL existente (post-test)
jmeter -g results.jtl -o report/

# Con propiedades custom de reporte
jmeter -g results.jtl -o report/ \
  -Jjmeter.reportgenerator.overall_granularity=1000 \
  -Jjmeter.reportgenerator.apdex_satisfied_threshold=500 \
  -Jjmeter.reportgenerator.apdex_tolerated_threshold=1500
```

### Configuración del reporte (reportgenerator.properties)

```properties
# Granularidad de gráficos (ms)
jmeter.reportgenerator.overall_granularity=60000

# APDEX thresholds
jmeter.reportgenerator.apdex_satisfied_threshold=500
jmeter.reportgenerator.apdex_tolerated_threshold=1500

# Percentiles personalizados
jmeter.reportgenerator.graph.responseTimePercentiles.property.set_granularity=60000

# Filtrar samplers del reporte
jmeter.reportgenerator.sample_filter=
# Ejemplo: solo incluir algunos:
# jmeter.reportgenerator.sample_filter=Login|Search|Checkout
```

---

## 22. Patrones Avanzados

### Patrón: Login Once + Reuse Token

```
setUp Thread Group (1 user, 1 loop):
  └── POST /auth/login
      └── JSON Extractor → ${AUTH_TOKEN}
      └── JSR223 PostProcessor:
          props.put("sharedToken", vars.get("AUTH_TOKEN"))

Main Thread Group (100 users):
  └── JSR223 PreProcessor:
      vars.put("authToken", props.get("sharedToken"))
  └── HTTP Header Manager: Authorization: Bearer ${authToken}
  └── HTTP Requests...
```

### Patrón: Retry con backoff

```groovy
// JSR223 Sampler con retry logic
import groovy.json.JsonSlurper

int maxRetries = 3
int baseDelay = 1000  // 1 segundo

for (int attempt = 0; attempt <= maxRetries; attempt++) {
    def response = new URL("${vars.get('PROTOCOL')}://${vars.get('HOST')}/api/resource")
        .getText([requestProperties: [Authorization: "Bearer ${vars.get('authToken')}"]])
    
    def json = new JsonSlurper().parseText(response)
    
    if (json.status == "ready") {
        vars.put("resourceStatus", "ready")
        SampleResult.setSuccessful(true)
        SampleResult.setResponseData(response, "UTF-8")
        break
    }
    
    if (attempt < maxRetries) {
        def delay = baseDelay * Math.pow(2, attempt)
        Thread.sleep((long) delay)
    } else {
        SampleResult.setSuccessful(false)
        SampleResult.setResponseMessage("Resource not ready after ${maxRetries} retries")
    }
}
```

### Patrón: Data-driven con JSON externo

```groovy
// JSR223 PreProcessor - Cargar escenario completo desde JSON
import groovy.json.JsonSlurper

// Leer archivo de escenario
def scenarioFile = new File("data/scenarios/${vars.get('scenarioId')}.json")
def scenario = new JsonSlurper().parse(scenarioFile)

// Configurar todas las variables para el thread
scenario.each { key, value ->
    vars.put(key, value.toString())
}

// Configurar headers específicos del escenario
if (scenario.headers) {
    scenario.headers.each { name, value ->
        sampler.getHeaderManager().add(
            new org.apache.jmeter.protocol.http.control.Header(name, value)
        )
    }
}
```

---

## 23. Troubleshooting y Performance Tuning

### Problemas comunes

| Problema | Causa | Solución |
|----------|-------|----------|
| OutOfMemoryError | Heap insuficiente | Aumentar `-Xmx` |
| Resultados lentos | Listeners gráficos activos | Deshabilitar en CLI |
| CPU 100% en JMeter | Demasiados threads | Distribuir carga |
| "Connection reset" | Pool agotado | Aumentar timeouts |
| Variables vacías | Extractor no matchea | Verificar con Results Tree |
| CSV "sharing" incorrecto | ShareMode mal configurado | Revisar scope |
| Throughput no alcanza target | Threads insuficientes | Más threads o Arrivals TG |

### Optimización para carga alta

```properties
# user.properties - Optimización para alto rendimiento

# Deshabilitar funciones no necesarias
CookieManager.save.cookies=false
CookieManager.check.cookies=false

# Reducir logging
log_level.jmeter=WARN
log_level.jmeter.engine=WARN

# Optimizar HTTP
httpclient4.retrycount=0
hc.parameters.file=hc.parameters

# Resultados mínimos (solo lo necesario)
jmeter.save.saveservice.output_format=csv
jmeter.save.saveservice.data_type=false
jmeter.save.saveservice.label=true
jmeter.save.saveservice.response_code=true
jmeter.save.saveservice.response_data=false
jmeter.save.saveservice.response_data.on_error=false
jmeter.save.saveservice.response_message=false
jmeter.save.saveservice.successful=true
jmeter.save.saveservice.thread_name=true
jmeter.save.saveservice.time=true
jmeter.save.saveservice.connect_time=true
jmeter.save.saveservice.bytes=true
jmeter.save.saveservice.sent_bytes=true
jmeter.save.saveservice.thread_counts=true
jmeter.save.saveservice.url=false
jmeter.save.saveservice.requestHeaders=false
jmeter.save.saveservice.responseHeaders=false
jmeter.save.saveservice.samplerData=false
```

---

## 24. Mejores Prácticas y Antipatrones

### ✅ Mejores Prácticas

1. **SIEMPRE ejecutar en modo CLI (non-GUI) para tests reales**
2. **Usar Groovy (JSR223) con "Compile and cache" activado**
3. **Externalizar datos en CSV/JSON, no hardcoded**
4. **Usar Transaction Controllers para medir flujos completos**
5. **Configurar assertions solo donde sea necesario**
6. **Deshabilitar View Results Tree antes de load test**
7. **Usar properties para configuración dinámica**
8. **Versionar .jmx en Git (es XML legible)**
9. **Un Thread Group por perfil de usuario**
10. **Nombres descriptivos para todos los elementos**

### ❌ Antipatrones

1. ❌ **Ejecutar load tests en modo GUI** (consume recursos del test)
2. ❌ **Usar BeanShell** (5-10x más lento que Groovy)
3. ❌ **Listeners gráficos durante el test** (memory leak)
4. ❌ **Think time = 0** (no es realista, satura artificialmente)
5. ❌ **Ignorar el ramp-up** (spike irreal al inicio)
6. ❌ **No validar correlación** (variables vacías causan cascada de errores)
7. ❌ **Un solo Thread Group gigante** (dificulta análisis)
8. ❌ **Guardar response data en JTL** (archivos enormes)
9. ❌ **No usar HTTP Request Defaults** (repetir host/port en cada request)
10. ❌ **Regular Expression en lugar de JSON Extractor para JSON** (ineficiente)

---

## 25. Proyecto de Referencia Completo

### Estructura

```
jmeter-perf-tests/
├── test-plans/
│   ├── load_test.jmx
│   ├── stress_test.jmx
│   ├── smoke_test.jmx
│   └── soak_test.jmx
├── data/
│   ├── users.csv
│   ├── products.csv
│   └── search_terms.csv
├── scripts/
│   ├── groovy/
│   │   ├── setup_auth.groovy
│   │   └── validate_response.groovy
│   ├── check_jmeter_results.py
│   └── generate_data.py
├── config/
│   ├── user.properties
│   └── reportgenerator.properties
├── plugins/
│   └── (custom JARs)
├── results/                    # gitignored
├── reports/                    # gitignored
├── Makefile
├── Dockerfile
└── README.md
```

### Makefile

```makefile
JMETER_HOME ?= /opt/apache-jmeter-5.6.3
JMETER = $(JMETER_HOME)/bin/jmeter
HOST ?= api.staging.example.com
USERS ?= 100
DURATION ?= 600

.PHONY: smoke load stress soak report clean

smoke:
	$(JMETER) -n -t test-plans/smoke_test.jmx -l results/smoke.jtl \
		-Jtarget.host=$(HOST) -Jtest.users=5 -Jtest.duration=60 \
		-e -o reports/smoke/

load:
	$(JMETER) -n -t test-plans/load_test.jmx -l results/load.jtl \
		-Jtarget.host=$(HOST) -Jtest.users=$(USERS) -Jtest.duration=$(DURATION) \
		-e -o reports/load/ -Xmx4g

stress:
	$(JMETER) -n -t test-plans/stress_test.jmx -l results/stress.jtl \
		-Jtarget.host=$(HOST) -Jtest.users=500 -Jtest.duration=900 \
		-e -o reports/stress/ -Xmx8g

report:
	$(JMETER) -g results/load.jtl -o reports/latest/

clean:
	rm -rf results/*.jtl reports/*/
```

---

## Referencias

- [Apache JMeter Official Documentation](https://jmeter.apache.org/usermanual/)
- [JMeter Best Practices](https://jmeter.apache.org/usermanual/best-practices.html)
- [JMeter Plugins](https://jmeter-plugins.org/)
- [JMeter GitHub Repository](https://github.com/apache/jmeter)
- [Blazemeter University (Free Courses)](https://www.blazemeter.com/university)
- [JMeter Distributed Testing](https://jmeter.apache.org/usermanual/jmeter_distributed_testing_step_by_step.html)
- [JMeter Dashboard Report](https://jmeter.apache.org/usermanual/generating-dashboard.html)
- [JMeter Functions Reference](https://jmeter.apache.org/usermanual/functions.html)
- [Groovy Documentation](https://groovy-lang.org/documentation.html)

---

> 💡 **JMeter sigue siendo la herramienta más versátil para multi-protocolo y la más accesible para testers no-programadores.**
> Su GUI permite diseño rápido y su modo CLI permite ejecución eficiente. La clave es SIEMPRE ejecutar tests reales en non-GUI mode y usar Groovy para cualquier scripting.
