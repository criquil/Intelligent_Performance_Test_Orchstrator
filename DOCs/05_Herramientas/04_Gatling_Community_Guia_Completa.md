# 🚀 Gatling Community Edition - Guía Completa de Referencia

## Índice

1. [Introducción y Filosofía](#1-introducción-y-filosofía)
2. [Arquitectura Interna](#2-arquitectura-interna)
3. [Instalación y Setup de Proyecto](#3-instalación-y-setup-de-proyecto)
4. [DSLs Disponibles (Java, Kotlin, Scala)](#4-dsls-disponibles-java-kotlin-scala)
5. [Estructura de una Simulation](#5-estructura-de-una-simulation)
6. [Scenarios y Estructura de Ejecución](#6-scenarios-y-estructura-de-ejecución)
7. [HTTP Protocol Configuration](#7-http-protocol-configuration)
8. [Requests y Actions](#8-requests-y-actions)
9. [Checks y Validaciones](#9-checks-y-validaciones)
10. [Session API y Estado del Virtual User](#10-session-api-y-estado-del-virtual-user)
11. [Feeders (Parametrización de Datos)](#11-feeders-parametrización-de-datos)
12. [Injection Profiles (Open vs Closed Model)](#12-injection-profiles-open-vs-closed-model)
13. [Control de Flujo (Loops, Conditions, Errors)](#13-control-de-flujo-loops-conditions-errors)
14. [Pause, Pacing y Think Time](#14-pause-pacing-y-think-time)
15. [Assertions (Criterios de Aceptación)](#15-assertions-criterios-de-aceptación)
16. [Gatling Recorder](#16-gatling-recorder)
17. [Reportes y Análisis](#17-reportes-y-análisis)
18. [Protocolos Adicionales (WebSocket, SSE, JMS)](#18-protocolos-adicionales-websocket-sse-jms)
19. [Integración con CI/CD](#19-integración-con-cicd)
20. [Patrones Avanzados](#20-patrones-avanzados)
21. [Debugging y Troubleshooting](#21-debugging-y-troubleshooting)
22. [Community vs Enterprise Edition](#22-community-vs-enterprise-edition)
23. [Mejores Prácticas y Antipatrones](#23-mejores-prácticas-y-antipatrones)
24. [Proyecto de Referencia Completo](#24-proyecto-de-referencia-completo)

---

## 1. Introducción y Filosofía

### ¿Qué es Gatling?

**Gatling** es una herramienta open-source de load testing de alto rendimiento diseñada para aplicaciones web. Está construida sobre **Akka** (actor model) y **Netty** (async I/O), lo que le permite manejar miles de usuarios virtuales concurrentes con recursos mínimos.

### Filosofía de diseño

| Principio | Implementación |
|-----------|---------------|
| **Code as tests** | DSL expressivo en Java/Kotlin/Scala |
| **Async non-blocking** | Akka actors + Netty NIO |
| **Developer-friendly** | IDE support, Maven/Gradle/SBT |
| **Realistic simulation** | Open & Closed workload models |
| **Beautiful reports** | HTML reports detallados out-of-the-box |
| **CI/CD first** | Plugin para todos los build tools |

### Community Edition — Licencia y Limitaciones

```
┌────────────────────────────────────────────────────────────────┐
│           GATLING COMMUNITY EDITION (Apache 2.0)               │
├────────────────────────────────────────────────────────────────┤
│ ✅ INCLUIDO                    │ ❌ NO INCLUIDO (Enterprise)   │
├────────────────────────────────┼───────────────────────────────┤
│ HTTP/HTTPS protocol            │ Distributed testing           │
│ WebSocket protocol             │ Cloud load generators         │
│ SSE (Server-Sent Events)       │ Real-time dashboards          │
│ JMS protocol                   │ MQTT protocol                 │
│ Java / Kotlin / Scala DSL      │ JDBC protocol                 │
│ Maven / Gradle / SBT plugins   │ Advanced analytics & trends   │
│ HTML reports                   │ Team management / SSO         │
│ Gatling Recorder               │ Scheduled/automated runs      │
│ CI/CD integration (basic)      │ API for triggering tests      │
│ Open & Closed workload models  │ Commercial support / SLA      │
│ Assertions                     │ Load sharding (multi-node)    │
│ Feeders (CSV, JSON, JDBC)      │ Enterprise CI/CD plugins      │
└────────────────────────────────┴───────────────────────────────┘
```

### Cuándo usar Gatling

✅ **Ideal para:**
- Equipos Java/Kotlin que quieren tests como código
- Alto throughput necesario con pocos recursos
- Tests HTTP/REST/GraphQL con lógica compleja
- Necesidad de reportes visuales HTML sin configuración extra
- Integración nativa con Maven/Gradle en proyectos existentes
- Workload modeling preciso (open + closed model)

❌ **Considerar alternativas si:**
- Necesitas testing distribuido gratis (→ Locust, k6)
- El equipo no trabaja en JVM (→ k6 para JS, Locust para Python)
- Necesitas protocolo MQTT/JDBC sin Enterprise (→ JMeter)
- Prefieres scripting más simple sin compilación (→ k6)

---

## 2. Arquitectura Interna

### Stack tecnológico

```
┌─────────────────────────────────────────────────────────────────┐
│                    GATLING ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │                    SIMULATION DSL                         │     │
│  │     Java DSL / Kotlin DSL / Scala DSL                    │     │
│  └─────────────────────────────┬───────────────────────────┘     │
│                                │                                  │
│  ┌─────────────────────────────▼───────────────────────────┐     │
│  │                    GATLING CORE                           │     │
│  │  ┌──────────┐  ┌──────────────┐  ┌──────────────────┐  │     │
│  │  │ Scenario │  │  Injection   │  │   Stats Engine   │  │     │
│  │  │ Engine   │  │  Controller  │  │   (Aggregator)   │  │     │
│  │  └──────────┘  └──────────────┘  └──────────────────┘  │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │                    AKKA FRAMEWORK                         │     │
│  │  Actor System → Message passing → Non-blocking I/O       │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │                    NETTY (NIO)                            │     │
│  │  Async HTTP Client → Connection Pooling → SSL/TLS        │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │              REPORT GENERATOR (HTML/JSON)                 │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Modelo de concurrencia

```
Comparación de modelos de concurrencia:

┌──────────────┬──────────────────────────────────────────────────┐
│ Herramienta  │ Modelo                                           │
├──────────────┼──────────────────────────────────────────────────┤
│ JMeter       │ 1 Thread por usuario → alto consumo RAM          │
│ Locust       │ 1 Greenlet por usuario → cooperativo (Python GIL)│
│ k6           │ Goroutines → muy eficiente                       │
│ Gatling      │ Akka Actors + Async I/O → NO 1 thread/user      │
└──────────────┴──────────────────────────────────────────────────┘

Gatling NO crea un thread por virtual user.
Usa message-passing entre actors:
- Actor Controller: coordina inyección de usuarios
- Actor User: representa cada VU (lightweight, no es un thread)
- Actor Stats: agrega métricas en tiempo real

Resultado: ~10,000-60,000 usuarios concurrentes con 1 máquina (8 cores)
```

### Flujo de ejecución

```
1. COMPILACIÓN
   └─ Simulation (Java/Kotlin/Scala) → bytecode JVM

2. SETUP PHASE
   └─ setUp() define: scenarios + injection profiles + protocols + assertions

3. INJECTION PHASE
   └─ Injection controller crea virtual users según el perfil

4. EXECUTION PHASE
   └─ Cada VU ejecuta su scenario:
      exec → check → pause → exec → check → ...

5. STATS COLLECTION
   └─ Cada request reporta: response time, status, size

6. REPORT GENERATION
   └─ Genera HTML report con gráficos, percentiles, timelines
```

---

## 3. Instalación y Setup de Proyecto

### Opción 1: Maven (Recomendado para Java)

```xml
<!-- pom.xml -->
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>com.company</groupId>
  <artifactId>performance-tests</artifactId>
  <version>1.0-SNAPSHOT</version>

  <properties>
    <maven.compiler.source>17</maven.compiler.source>
    <maven.compiler.target>17</maven.compiler.target>
    <gatling.version>3.11.5</gatling.version>
    <gatling-maven-plugin.version>4.9.6</gatling-maven-plugin.version>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  </properties>

  <dependencies>
    <dependency>
      <groupId>io.gatling.highcharts</groupId>
      <artifactId>gatling-charts-highcharts</artifactId>
      <version>${gatling.version}</version>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>io.gatling</groupId>
      <artifactId>gatling-app</artifactId>
      <version>${gatling.version}</version>
      <scope>test</scope>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <groupId>io.gatling</groupId>
        <artifactId>gatling-maven-plugin</artifactId>
        <version>${gatling-maven-plugin.version}</version>
        <configuration>
          <simulationClass>simulations.LoadTestSimulation</simulationClass>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
```

```bash
# Crear proyecto desde archetype
mvn archetype:generate \
  -DarchetypeGroupId=io.gatling.highcharts \
  -DarchetypeArtifactId=gatling-highcharts-maven-archetype \
  -DarchetypeVersion=3.11.5

# Ejecutar test
mvn gatling:test

# Ejecutar simulación específica
mvn gatling:test -Dgatling.simulationClass=simulations.LoadTestSimulation

# Con parámetros del sistema
mvn gatling:test -Dusers=200 -Dduration=600 -DtargetHost=https://api.staging.com
```

### Opción 2: Gradle (Recomendado para Kotlin)

```kotlin
// build.gradle.kts
plugins {
    java
    id("io.gatling.gradle") version "3.11.5.2"
}

repositories {
    mavenCentral()
}

gatling {
    // Configuración del plugin
    logLevel = "WARN"
    logHttp = io.gatling.gradle.LogHttp.FAILURES

    // Configuración de JVM
    jvmArgs = listOf(
        "-server",
        "-Xmx4g",
        "-XX:+UseG1GC",
        "-XX:+ParallelRefProcEnabled",
        "-XX:MaxInlineLevel=20",
        "-XX:MaxTrivialSize=12"
    )

    // Simulaciones a ejecutar
    // simulationClass = "simulations.LoadTestSimulation"
}

dependencies {
    gatling("io.gatling.highcharts:gatling-charts-highcharts:3.11.5")
    gatling("io.gatling:gatling-app:3.11.5")
    // Dependencias adicionales para los tests
    gatling("com.google.code.gson:gson:2.10.1")
}
```

```bash
# Ejecutar tests
./gradlew gatlingRun

# Ejecutar simulación específica
./gradlew gatlingRun-simulations.LoadTestSimulation

# Con propiedades
./gradlew gatlingRun -Dusers=200 -Dduration=600
```

### Opción 3: SBT (Para Scala)

```scala
// build.sbt
enablePlugins(GatlingPlugin)

scalaVersion := "2.13.14"

val gatlingVersion = "3.11.5"

libraryDependencies ++= Seq(
  "io.gatling.highcharts" % "gatling-charts-highcharts" % gatlingVersion % "test,it",
  "io.gatling"            % "gatling-test-framework"    % gatlingVersion % "test,it"
)

// project/plugins.sbt
addSbtPlugin("io.gatling" % "gatling-sbt" % "4.9.2")
```

```bash
# Ejecutar
sbt Gatling/test
sbt "Gatling/testOnly simulations.LoadTestSimulation"
```

### Opción 4: Standalone (Bundle ZIP)

```bash
# Descargar bundle
curl -L -o gatling.zip \
  https://repo1.maven.org/maven2/io/gatling/highcharts/gatling-charts-highcharts-bundle/3.11.5/gatling-charts-highcharts-bundle-3.11.5.zip

unzip gatling.zip
cd gatling-charts-highcharts-bundle-3.11.5

# Estructura del bundle
# ├── bin/
# │   ├── gatling.sh / gatling.bat    (ejecutar simulaciones)
# │   └── recorder.sh / recorder.bat  (grabar scripts)
# ├── conf/
# │   ├── gatling.conf                (configuración global)
# │   └── logback.xml                 (logging)
# ├── lib/                            (JARs)
# ├── results/                        (reportes generados)
# └── user-files/
#     ├── simulations/                (tus tests aquí)
#     ├── resources/                  (feeders, bodies, etc.)
#     └── lib/                        (dependencias custom)

# Ejecutar
./bin/gatling.sh
```

### Estructura de proyecto recomendada (Maven)

```
performance-tests/
├── pom.xml
├── src/
│   └── test/
│       ├── java/                          # Java DSL simulations
│       │   └── simulations/
│       │       ├── LoadTestSimulation.java
│       │       ├── StressTestSimulation.java
│       │       └── SpikeTestSimulation.java
│       ├── kotlin/                        # Kotlin DSL (alternativa)
│       │   └── simulations/
│       │       └── LoadTestSimulation.kt
│       ├── scala/                         # Scala DSL (alternativa)
│       │   └── simulations/
│       │       └── LoadTestSimulation.scala
│       └── resources/
│           ├── gatling.conf               # Configuración Gatling
│           ├── logback-test.xml           # Logging config
│           ├── feeders/                   # Archivos de datos
│           │   ├── users.csv
│           │   ├── products.json
│           │   └── search_terms.csv
│           ├── bodies/                    # Request body templates
│           │   ├── create_order.json
│           │   └── update_profile.json
│           └── recorder/                  # Recordings
│               └── RecordedSimulation.java
├── target/
│   └── gatling/                           # Reports generados
└── Makefile
```

### Configuración de Gatling (gatling.conf)

```hocon
# src/test/resources/gatling.conf
gatling {
  core {
    # Nombre del directorio de salida de resultados
    # outputDirectoryBaseName = ""

    # Encoding para archivos de simulación
    encoding = "utf-8"

    # Número de usuarios simulados
    # Se puede overridear con -Dgatling.core.simulationClass
  }

  http {
    # Configuración de conexiones HTTP
    fetchedCssCacheMaxCapacity = 200
    fetchedHtmlCacheMaxCapacity = 200
    perUserCacheMaxCapacity = 200
    warmUpUrl = "https://gatling.io"

    # Connection pooling
    pooledConnectionIdleTimeout = 60000  # ms
    requestTimeout = 60000              # ms
    enableHostnameVerification = true

    # DNS
    dns {
      queryTimeout = 5000   # ms
      maxQueriesPerResolve = 6
    }
  }

  data {
    # Directorio de data files (feeders)
    # dataWriterBufferSize = 8192
  }

  charting {
    # Configuración de reportes
    indicators {
      lowerBound = 800    # ms - línea verde en gráficos
      higherBound = 1200  # ms - línea roja en gráficos
      # Percentiles mostrados en reportes
      percentile1 = 50
      percentile2 = 75
      percentile3 = 95
      percentile4 = 99
    }
  }
}
```

---

## 4. DSLs Disponibles (Java, Kotlin, Scala)

### Comparativa de sintaxis

El mismo test en los 3 DSLs:

#### Java DSL

```java
package simulations;

import io.gatling.javaapi.core.*;
import io.gatling.javaapi.http.*;
import java.time.Duration;

import static io.gatling.javaapi.core.CoreDsl.*;
import static io.gatling.javaapi.http.HttpDsl.*;

public class BasicSimulation extends Simulation {

    HttpProtocolBuilder httpProtocol = http
        .baseUrl("https://api.example.com")
        .acceptHeader("application/json")
        .contentTypeHeader("application/json");

    ScenarioBuilder scn = scenario("Basic Test")
        .exec(
            http("Get Users")
                .get("/api/users")
                .check(status().is(200))
        )
        .pause(Duration.ofSeconds(2));

    {
        setUp(
            scn.injectOpen(
                rampUsers(100).during(Duration.ofMinutes(2))
            )
        ).protocols(httpProtocol);
    }
}
```

#### Kotlin DSL

```kotlin
package simulations

import io.gatling.javaapi.core.*
import io.gatling.javaapi.core.CoreDsl.*
import io.gatling.javaapi.http.HttpDsl.*
import java.time.Duration

class BasicSimulation : Simulation() {

    val httpProtocol = http
        .baseUrl("https://api.example.com")
        .acceptHeader("application/json")
        .contentTypeHeader("application/json")

    val scn = scenario("Basic Test")
        .exec(
            http("Get Users")
                .get("/api/users")
                .check(status().`is`(200))
        )
        .pause(Duration.ofSeconds(2))

    init {
        setUp(
            scn.injectOpen(
                rampUsers(100).during(Duration.ofMinutes(2))
            )
        ).protocols(httpProtocol)
    }
}
```

#### Scala DSL

```scala
package simulations

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import scala.concurrent.duration._

class BasicSimulation extends Simulation {

  val httpProtocol = http
    .baseUrl("https://api.example.com")
    .acceptHeader("application/json")
    .contentTypeHeader("application/json")

  val scn = scenario("Basic Test")
    .exec(
      http("Get Users")
        .get("/api/users")
        .check(status.is(200))
    )
    .pause(2.seconds)

  setUp(
    scn.inject(
      rampUsers(100).during(2.minutes)
    )
  ).protocols(httpProtocol)
}
```

### ¿Cuál DSL elegir?

| Criterio | Java | Kotlin | Scala |
|----------|------|--------|-------|
| Equipo conoce | Java ✅ | Kotlin ✅ | Scala ✅ |
| Verbosidad | Alta | Media | Baja |
| IDE support | Excelente | Excelente | Bueno |
| Compilación | Rápida | Rápida | Lenta |
| Comunidad | Grande | Creciente | Histórica |
| Recomendado | ⭐ Equipos Java | ⭐ Equipos Kotlin/Android | Legacy/experimentados |

> 📝 **Nota:** A partir de Gatling 3.7+, Java DSL es la opción recomendada oficialmente para nuevos proyectos. Los ejemplos en esta guía usan **Java DSL** por defecto, con notas en Scala donde aplique.

---

## 5. Estructura de una Simulation

### Anatomía completa

```java
package simulations;

import io.gatling.javaapi.core.*;
import io.gatling.javaapi.http.*;
import java.time.Duration;
import java.util.*;

import static io.gatling.javaapi.core.CoreDsl.*;
import static io.gatling.javaapi.http.HttpDsl.*;

public class FullSimulation extends Simulation {

    // ═══════════════════════════════════════════════════════
    // 1. CONFIGURACIÓN DE PROTOCOLO
    // ═══════════════════════════════════════════════════════
    
    private HttpProtocolBuilder httpProtocol = http
        .baseUrl(System.getProperty("targetHost", "https://api.example.com"))
        .acceptHeader("application/json")
        .contentTypeHeader("application/json")
        .acceptEncodingHeader("gzip, deflate")
        .userAgentHeader("Gatling/PerformanceTest")
        .shareConnections()           // Compartir pool de conexiones
        .maxConnectionsPerHost(10)    // Conexiones por host
        .disableFollowRedirect();     // No seguir redirects automáticamente

    // ═══════════════════════════════════════════════════════
    // 2. FEEDERS (Datos de prueba)
    // ═══════════════════════════════════════════════════════
    
    private FeederBuilder<String> userFeeder = csv("feeders/users.csv").random();
    private FeederBuilder<Object> productFeeder = jsonFile("feeders/products.json").circular();

    // ═══════════════════════════════════════════════════════
    // 3. CHAINS REUTILIZABLES
    // ═══════════════════════════════════════════════════════
    
    private ChainBuilder login = exec(
        http("POST /auth/login")
            .post("/api/v1/auth/login")
            .body(StringBody("{\"email\":\"#{email}\",\"password\":\"#{password}\"}"))
            .check(
                status().is(200),
                jmesPath("access_token").saveAs("token"),
                jmesPath("expires_in").saveAs("tokenExpiry")
            )
    );

    private ChainBuilder setAuthHeader = exec(session -> 
        session.set("authHeader", "Bearer " + session.getString("token"))
    );

    // ═══════════════════════════════════════════════════════
    // 4. SCENARIOS
    // ═══════════════════════════════════════════════════════
    
    private ScenarioBuilder browseScenario = scenario("Browse Products")
        .feed(userFeeder)
        .exec(login)
        .exec(setAuthHeader)
        .pause(Duration.ofSeconds(2), Duration.ofSeconds(5))
        .repeat(5).on(
            exec(
                http("GET /products")
                    .get("/api/v1/products")
                    .header("Authorization", "#{authHeader}")
                    .queryParam("page", "#{counter}")
                    .check(status().is(200))
            )
            .pause(Duration.ofSeconds(3), Duration.ofSeconds(10))
        );

    private ScenarioBuilder purchaseScenario = scenario("Purchase Flow")
        .feed(userFeeder)
        .feed(productFeeder)
        .exec(login)
        .exec(setAuthHeader)
        .pause(Duration.ofSeconds(1), Duration.ofSeconds(3))
        .exec(
            http("POST /cart/items")
                .post("/api/v1/cart/items")
                .header("Authorization", "#{authHeader}")
                .body(StringBody("{\"product_id\":\"#{productId}\",\"quantity\":1}"))
                .check(
                    status().is(201),
                    jmesPath("cart_id").saveAs("cartId")
                )
        )
        .pause(Duration.ofSeconds(2), Duration.ofSeconds(5))
        .exec(
            http("POST /checkout")
                .post("/api/v1/checkout")
                .header("Authorization", "#{authHeader}")
                .body(StringBody("{\"cart_id\":\"#{cartId}\",\"payment\":\"test_card\"}"))
                .check(status().is(200))
        );

    // ═══════════════════════════════════════════════════════
    // 5. SETUP (Injection + Protocol + Assertions)
    // ═══════════════════════════════════════════════════════
    
    {
        int targetUsers = Integer.parseInt(System.getProperty("users", "100"));
        int durationSec = Integer.parseInt(System.getProperty("duration", "600"));

        setUp(
            browseScenario.injectOpen(
                nothingFor(Duration.ofSeconds(5)),
                rampUsers(targetUsers).during(Duration.ofMinutes(2)),
                constantUsersPerSec(targetUsers / 10.0).during(Duration.ofSeconds(durationSec))
            ),
            purchaseScenario.injectOpen(
                nothingFor(Duration.ofSeconds(30)),
                rampUsers(targetUsers / 5).during(Duration.ofMinutes(2)),
                constantUsersPerSec(targetUsers / 50.0).during(Duration.ofSeconds(durationSec))
            )
        )
        .protocols(httpProtocol)
        .assertions(
            global().responseTime().percentile3().lt(3000),    // P95 < 3s
            global().successfulRequests().percent().gt(99.0),  // > 99% success
            forAll().responseTime().max().lt(10000),           // Ningún request > 10s
            details("POST /checkout").responseTime().mean().lt(2000)  // Checkout avg < 2s
        );
    }
}
```

---

## 6. Scenarios y Estructura de Ejecución

### Chains reutilizables

```java
// Definir chains que se pueden reutilizar en múltiples scenarios

// Chain de autenticación
ChainBuilder authenticate = feed(userFeeder)
    .exec(
        http("Login")
            .post("/auth/login")
            .body(StringBody("{\"user\":\"#{username}\",\"pass\":\"#{password}\"}"))
            .check(jmesPath("token").saveAs("authToken"))
    )
    .exec(session -> session.set("authHeader", "Bearer " + session.getString("authToken")));

// Chain de búsqueda
ChainBuilder searchProducts = feed(searchTermFeeder)
    .exec(
        http("Search")
            .get("/api/search")
            .header("Authorization", "#{authHeader}")
            .queryParam("q", "#{searchTerm}")
            .queryParam("limit", "20")
            .check(
                status().is(200),
                jmesPath("results[*].id").ofList().saveAs("resultIds")
            )
    );

// Chain de ver detalle (usa resultado de búsqueda)
ChainBuilder viewProductDetail = 
    doIf(session -> !session.getList("resultIds").isEmpty()).then(
        exec(session -> {
            List<String> ids = session.getList("resultIds");
            String randomId = ids.get(new Random().nextInt(ids.size()));
            return session.set("selectedProductId", randomId);
        })
        .exec(
            http("Product Detail")
                .get("/api/products/#{selectedProductId}")
                .header("Authorization", "#{authHeader}")
                .check(status().is(200))
        )
    );

// Componer scenarios con chains
ScenarioBuilder browserScenario = scenario("Browser User")
    .exec(authenticate)
    .pause(2, 5)
    .exec(searchProducts)
    .pause(3, 8)
    .exec(viewProductDetail);
```

### Scenarios secuenciales (andThen)

```java
// Scenario que se ejecuta DESPUÉS de que el primero termine
ScenarioBuilder warmup = scenario("Warmup")
    .exec(http("Health Check").get("/health").check(status().is(200)));

ScenarioBuilder mainTest = scenario("Main Load")
    .exec(/* ... */);

ScenarioBuilder cooldown = scenario("Cooldown Verification")
    .exec(http("Final Check").get("/health").check(status().is(200)));

setUp(
    warmup.injectOpen(atOnceUsers(1))
        .andThen(
            mainTest.injectOpen(rampUsers(200).during(Duration.ofMinutes(5)))
        )
        .andThen(
            cooldown.injectOpen(atOnceUsers(1))
        )
).protocols(httpProtocol);
```

### Scenarios concurrentes

```java
// Múltiples scenarios ejecutándose en paralelo
setUp(
    // 70% browsing
    browseScenario.injectOpen(
        rampUsers(700).during(Duration.ofMinutes(5))
    ),
    // 20% searching
    searchScenario.injectOpen(
        nothingFor(Duration.ofSeconds(30)),
        rampUsers(200).during(Duration.ofMinutes(5))
    ),
    // 10% purchasing
    purchaseScenario.injectOpen(
        nothingFor(Duration.ofMinutes(1)),
        rampUsers(100).during(Duration.ofMinutes(5))
    )
).protocols(httpProtocol);
```

---

## 7. HTTP Protocol Configuration

### Configuración completa del protocolo HTTP

```java
HttpProtocolBuilder httpProtocol = http
    // ─── Base URL ───
    .baseUrl("https://api.example.com")
    // Para multi-host (round-robin):
    // .baseUrls("https://api1.example.com", "https://api2.example.com")
    
    // ─── Headers globales ───
    .acceptHeader("application/json")
    .acceptEncodingHeader("gzip, deflate, br")
    .acceptLanguageHeader("en-US,en;q=0.9,es;q=0.8")
    .contentTypeHeader("application/json")
    .userAgentHeader("Gatling/3.11 (Performance Test)")
    .header("X-Request-Source", "gatling-load-test")
    
    // ─── Connection management ───
    .shareConnections()                    // Compartir pool entre VUs
    .maxConnectionsPerHost(6)             // Max conexiones por host
    // .perUserNameResolution()            // DNS resolution per user
    
    // ─── Redirect behavior ───
    .disableFollowRedirect()              // No seguir 301/302 automáticamente
    // .redirectNamingStrategy(...)
    
    // ─── Proxy ───
    // .proxy(Proxy("proxy.corp.com", 8080))
    // .proxy(Proxy("proxy.corp.com", 8080).credentials("user", "pass"))
    
    // ─── SSL/TLS ───
    // .useAllLocalAddresses()
    // .perUserKeyManagerFactory(...)
    
    // ─── Timeouts ───
    .requestTimeout(Duration.ofSeconds(30))
    
    // ─── Checks implícitos (globales) ───
    .check(status().not(500), status().not(502), status().not(503))
    
    // ─── Response handling ───
    .disableAutoReferer()
    .disableCaching()
    // .inferHtmlResources()               // Descargar CSS/JS/IMG como browser
    // .inferHtmlResources(AllowList(...))
    
    // ─── Logging (para debug) ───
    // .enableHttp2()                      // HTTP/2 support
    ;
```

### Múltiples protocolos

```java
// Protocolo para API principal
HttpProtocolBuilder apiProtocol = http
    .baseUrl("https://api.example.com")
    .contentTypeHeader("application/json");

// Protocolo para servicio de autenticación
HttpProtocolBuilder authProtocol = http
    .baseUrl("https://auth.example.com")
    .contentTypeHeader("application/x-www-form-urlencoded");

// Usar protocolo específico por scenario
setUp(
    apiScenario.injectOpen(rampUsers(100).during(Duration.ofMinutes(2)))
        .protocols(apiProtocol),
    authScenario.injectOpen(rampUsers(10).during(Duration.ofSeconds(30)))
        .protocols(authProtocol)
);
```

---

## 8. Requests y Actions

### GET requests

```java
// Simple GET
http("Get Home").get("/")

// GET con query params
http("Search Products")
    .get("/api/products")
    .queryParam("category", "electronics")
    .queryParam("page", "#{pageNum}")
    .queryParam("limit", "20")
    .queryParam("sort", "price_asc")

// GET con headers custom
http("Get User Profile")
    .get("/api/users/#{userId}/profile")
    .header("Authorization", "Bearer #{token}")
    .header("X-Request-ID", session -> UUID.randomUUID().toString())
```

### POST requests

```java
// POST con body string
http("Create User")
    .post("/api/users")
    .body(StringBody("""
        {
            "name": "#{userName}",
            "email": "#{userEmail}",
            "role": "customer"
        }
    """))
    .asJson()  // Shortcut para Content-Type: application/json

// POST con template de archivo
http("Create Order")
    .post("/api/orders")
    .body(RawFileBody("bodies/create_order.json"))
    .asJson()

// POST con template EL (Expression Language)
http("Create Order EL")
    .post("/api/orders")
    .body(ElFileBody("bodies/create_order_template.json"))  // #{variables} resueltas
    .asJson()

// POST form-urlencoded
http("Login Form")
    .post("/auth/login")
    .formParam("username", "#{username}")
    .formParam("password", "#{password}")
    .formParam("grant_type", "password")

// POST multipart (file upload)
http("Upload Avatar")
    .post("/api/users/#{userId}/avatar")
    .header("Authorization", "Bearer #{token}")
    .bodyPart(
        RawFileBodyPart("file", "data/test_image.png")
            .fileName("avatar.png")
            .contentType("image/png")
    )
    .bodyPart(StringBodyPart("description", "Profile photo"))
```

### PUT, PATCH, DELETE

```java
// PUT (reemplazo completo)
http("Update Product")
    .put("/api/products/#{productId}")
    .header("Authorization", "Bearer #{token}")
    .body(StringBody("""{"name":"Updated","price":29.99}"""))
    .asJson()

// PATCH (actualización parcial)
http("Patch User")
    .patch("/api/users/#{userId}")
    .header("Authorization", "Bearer #{token}")
    .body(StringBody("""{"status":"active"}"""))
    .asJson()

// DELETE
http("Delete Item")
    .delete("/api/cart/items/#{itemId}")
    .header("Authorization", "Bearer #{token}")
    .check(status().is(204))
```

### GraphQL

```java
// GraphQL query
http("GraphQL - Get Products")
    .post("/graphql")
    .body(StringBody("""
        {
            "query": "query GetProducts($category: String!, $limit: Int) { products(category: $category, limit: $limit) { id name price stock } }",
            "variables": {
                "category": "#{category}",
                "limit": 20
            }
        }
    """))
    .asJson()
    .check(
        jmesPath("data.products[0].id").exists(),
        jmesPath("errors").notExists()
    )
```

---

## 9. Checks y Validaciones

### Tipos de checks

```java
// ─── Status checks ───
.check(status().is(200))
.check(status().not(404))
.check(status().in(200, 201, 202))

// ─── Header checks ───
.check(header("Content-Type").is("application/json"))
.check(header("X-RateLimit-Remaining").saveAs("rateLimitRemaining"))
.check(headerRegex("Set-Cookie", "session=([^;]+)").saveAs("sessionCookie"))

// ─── Response time checks ───
.check(responseTimeInMillis().lt(2000))  // < 2 segundos

// ─── Body string checks ───
.check(bodyString().exists())
.check(substring("success").exists())
.check(regex("\"id\":\\s*\"([^\"]+)\"").saveAs("extractedId"))

// ─── JSON checks (JMESPath - recomendado) ───
.check(jmesPath("id").saveAs("resourceId"))
.check(jmesPath("status").is("active"))
.check(jmesPath("items").ofList().saveAs("itemsList"))
.check(jmesPath("items[0].name").exists())
.check(jmesPath("length(items)").ofInt().gt(0))
.check(jmesPath("metadata.total_count").ofInt().saveAs("totalCount"))

// ─── JSON checks (JsonPath - alternativa) ───
.check(jsonPath("$.data.user.id").saveAs("userId"))
.check(jsonPath("$.results[*].id").findAll().saveAs("allIds"))
.check(jsonPath("$.results").count().gt(0))

// ─── XML checks (XPath) ───
.check(xpath("//response/status/text()").is("OK"))
.check(xpath("//item/@id").findAll().saveAs("itemIds"))

// ─── CSS selector checks ───
.check(css("h1.title").is("Welcome"))
.check(css("input[name='csrf']", "value").saveAs("csrfToken"))
```

### Checks avanzados con transformación

```java
// Transformar valor extraído
.check(
    jmesPath("price")
        .ofString()
        .transform(price -> String.valueOf(Double.parseDouble(price) * 1.21))  // +21% IVA
        .saveAs("priceWithTax")
)

// Validación custom
.check(
    jmesPath("items")
        .ofList()
        .validate("has items", list -> !list.isEmpty())
)

// Check condicional (solo validar si existe)
.check(
    jmesPath("optional_field").optional().saveAs("maybeField")
)

// Check con default value
.check(
    jmesPath("missing_field").withDefault("default_value").saveAs("field")
)

// Multiple valores del mismo response
.check(
    jmesPath("user.id").saveAs("userId"),
    jmesPath("user.name").saveAs("userName"),
    jmesPath("user.email").saveAs("userEmail"),
    jmesPath("user.roles[0]").saveAs("primaryRole")
)
```

### Check scope (response vs time)

```java
// Check que el response time sea aceptable
http("Critical Endpoint")
    .get("/api/critical")
    .check(
        status().is(200),
        responseTimeInMillis().lt(500),      // < 500ms
        jmesPath("status").is("healthy")
    )

// Combinar checks - TODOS deben pasar
http("Full Validation")
    .get("/api/users/#{userId}")
    .check(
        status().is(200),
        header("Content-Type").is("application/json; charset=utf-8"),
        jmesPath("id").is("#{userId}"),
        jmesPath("email").exists(),
        jmesPath("created_at").exists(),
        bodyBytes().transform(bytes -> bytes.length).lt(10240)  // < 10KB
    )
```

---

## 10. Session API y Estado del Virtual User

### Concepto de Session

Cada virtual user tiene su propia **Session** — un Map inmutable que almacena el estado durante la ejecución del scenario.

```java
// ─── Escribir en session ───
exec(session -> session.set("myKey", "myValue"))
exec(session -> session.setAll(Map.of("key1", "val1", "key2", "val2")))

// ─── Leer de session ───
exec(session -> {
    String token = session.getString("token");
    int count = session.getInt("count");
    List<String> items = session.getList("items");
    
    // Verificar existencia
    boolean hasToken = session.contains("token");
    
    return session;
})

// ─── Remover de session ───
exec(session -> session.remove("temporaryData"))

// ─── Uso en Expression Language (EL) ───
// En strings: "#{variableName}" se resuelve desde la session
http("Get User")
    .get("/api/users/#{userId}")  // userId viene de la session
    .header("Authorization", "Bearer #{token}")
```

### Manipulación avanzada de session

```java
// Contador manual
ChainBuilder incrementCounter = exec(session -> {
    int current = session.contains("counter") ? session.getInt("counter") : 0;
    return session.set("counter", current + 1);
});

// Construir lista progresivamente
ChainBuilder addToList = exec(session -> {
    List<String> items = session.contains("myList") 
        ? new ArrayList<>(session.getList("myList"))
        : new ArrayList<>();
    items.add("new_item_" + items.size());
    return session.set("myList", items);
});

// Timestamp para correlación
ChainBuilder setTimestamp = exec(session -> 
    session.set("requestTimestamp", System.currentTimeMillis())
);

// Random selection from session data
ChainBuilder selectRandom = exec(session -> {
    List<String> ids = session.getList("productIds");
    if (ids != null && !ids.isEmpty()) {
        String randomId = ids.get(ThreadLocalRandom.current().nextInt(ids.size()));
        return session.set("selectedId", randomId);
    }
    return session;
});
```

### Expression Language (Gatling EL)

```java
// El Gatling EL resuelve #{...} desde la session

// Acceso simple
"#{username}"          // session.getString("username")
"#{userId}"            // session.getString("userId")

// Acceso a elementos de lista
"#{myList(0)}"         // Primer elemento
"#{myList.random()}"   // Elemento aleatorio
"#{myList.size()}"     // Tamaño de la lista

// Acceso a Map
"#{myMap.key1}"        // Valor de key1 en el map

// En body templates (ElFileBody)
// bodies/template.json:
// {"user": "#{username}", "items": #{itemCount}, "token": "#{authToken}"}
```

---

## 11. Feeders (Parametrización de Datos)

### Tipos de feeders

```java
// ─── CSV Feeder ───
FeederBuilder<String> csvFeeder = csv("feeders/users.csv");
// Archivo: email,password,name
// user1@test.com,pass123,John
// user2@test.com,pass456,Jane

// ─── JSON Feeder ───
FeederBuilder<Object> jsonFeeder = jsonFile("feeders/products.json");
// Archivo: [{"id": "P001", "name": "Laptop", "price": 999}, ...]

// ─── JDBC Feeder (requiere driver) ───
// FeederBuilder jdbcFeeder = jdbcFeeder(
//     "jdbc:postgresql://localhost:5432/testdb",
//     "dbuser", "dbpass",
//     "SELECT id, email, name FROM users WHERE active = true"
// );

// ─── Inline Feeder (para datos pequeños) ───
Iterator<Map<String, Object>> customFeeder = Stream.generate(() -> {
    Map<String, Object> map = new HashMap<>();
    map.put("randomId", UUID.randomUUID().toString());
    map.put("randomPrice", ThreadLocalRandom.current().nextDouble(10, 1000));
    map.put("timestamp", Instant.now().toString());
    return map;
}).iterator();
```

### Estrategias de acceso

```java
// ─── queue (default): cada registro una sola vez, falla si se acaba ───
FeederBuilder<String> queueFeeder = csv("users.csv").queue();

// ─── random: selección aleatoria (puede repetir) ───
FeederBuilder<String> randomFeeder = csv("users.csv").random();

// ─── shuffle: todos una vez pero en orden aleatorio ───
FeederBuilder<String> shuffleFeeder = csv("users.csv").shuffle();

// ─── circular: round-robin, vuelve al inicio ───
FeederBuilder<String> circularFeeder = csv("users.csv").circular();

// Uso en scenario
ScenarioBuilder scn = scenario("Test")
    .feed(circularFeeder)          // Alimenta la session con una fila
    .exec(
        http("Request")
            .get("/api/users/#{email}")  // Usa #{column_name} del CSV
    );
```

### Feeders avanzados

```java
// ─── Feeder programático con Faker ───
import com.github.javafaker.Faker;

Faker faker = new Faker();

Iterator<Map<String, Object>> fakerFeeder = Stream.generate(() -> {
    Map<String, Object> data = new HashMap<>();
    data.put("firstName", faker.name().firstName());
    data.put("lastName", faker.name().lastName());
    data.put("email", faker.internet().emailAddress());
    data.put("phone", faker.phoneNumber().cellPhone());
    data.put("address", faker.address().fullAddress());
    data.put("creditCard", faker.finance().creditCard());
    return Collections.unmodifiableMap(data);
}).iterator();

// ─── Feeder con transformación ───
FeederBuilder<Object> transformedFeeder = csv("users.csv")
    .transform((key, value) -> {
        if ("email".equals(key)) {
            return value.toLowerCase();
        }
        return value;
    })
    .circular();

// ─── Batch feeding (múltiples registros a la vez) ───
ScenarioBuilder batchScenario = scenario("Batch")
    .feed(productFeeder, 5)  // Alimenta 5 registros a la vez
    // Acceso: #{productId(0)}, #{productId(1)}, ... #{productId(4)}
    .exec(
        http("Batch Request")
            .post("/api/batch")
            .body(StringBody("""
                {"ids": ["#{productId(0)}", "#{productId(1)}", "#{productId(2)}"]}
            """))
    );
```

---

## 12. Injection Profiles (Open vs Closed Model)

### Open Model (llegada de usuarios)

```java
// ═══════════════════════════════════════════════════════════════
// OPEN MODEL: Controla la TASA DE LLEGADA de nuevos usuarios
// Los usuarios terminan cuando completan su scenario
// ═══════════════════════════════════════════════════════════════

setUp(
    scn.injectOpen(
        // 1. Pausa inicial (warmup de la app)
        nothingFor(Duration.ofSeconds(10)),
        
        // 2. Inyectar N usuarios de golpe
        atOnceUsers(10),
        
        // 3. Ramp: N usuarios distribuidos en un período
        rampUsers(100).during(Duration.ofMinutes(2)),
        
        // 4. Tasa constante: N usuarios/segundo
        constantUsersPerSec(20).during(Duration.ofMinutes(10)),
        
        // 5. Tasa constante con distribución aleatoria
        constantUsersPerSec(20).during(Duration.ofMinutes(5)).randomized(),
        
        // 6. Ramp de tasa: de N a M usuarios/segundo
        rampUsersPerSec(10).to(50).during(Duration.ofMinutes(5)),
        
        // 7. Ramp de tasa aleatorizada
        rampUsersPerSec(10).to(50).during(Duration.ofMinutes(5)).randomized(),
        
        // 8. Heaviside step (curva S suave)
        stressPeakUsers(1000).during(Duration.ofSeconds(30))
    )
);
```

### Closed Model (usuarios concurrentes fijos)

```java
// ═══════════════════════════════════════════════════════════════
// CLOSED MODEL: Controla el NÚMERO CONCURRENTE de usuarios
// Cuando un usuario termina, otro comienza inmediatamente
// ═══════════════════════════════════════════════════════════════

setUp(
    scn.injectClosed(
        // 1. Mantener N usuarios concurrentes
        constantConcurrentUsers(50).during(Duration.ofMinutes(10)),
        
        // 2. Ramp de concurrencia: de N a M usuarios
        rampConcurrentUsers(10).to(100).during(Duration.ofMinutes(5))
    )
);
```

### Stairs / Step Load (Escalera)

```java
// ─── Open Model Stairs ───
setUp(
    scn.injectOpen(
        // Escalones de 10, 20, 30, 40, 50 users/sec
        // Cada escalón dura 2 minutos
        // Rampa entre escalones: 30 segundos
        incrementUsersPerSec(10.0)
            .times(5)
            .eachLevelLasting(Duration.ofMinutes(2))
            .separatedByRampsLasting(Duration.ofSeconds(30))
            .startingFrom(10.0)  // Empezar en 10 users/sec
    )
);

// ─── Closed Model Stairs ───
setUp(
    scn.injectClosed(
        // Escalones de 20, 40, 60, 80, 100 concurrent users
        incrementConcurrentUsers(20)
            .times(5)
            .eachLevelLasting(Duration.ofMinutes(3))
            .separatedByRampsLasting(Duration.ofSeconds(30))
            .startingFrom(20)
    )
);
```

### Perfiles de carga compuestos

```java
// ═══════════════════════════════════════════════════════════════
// LOAD TEST CLÁSICO: ramp-up → hold → ramp-down
// ═══════════════════════════════════════════════════════════════
setUp(
    scn.injectOpen(
        // Ramp up: 0 → 100 users/sec en 5 minutos
        rampUsersPerSec(0).to(100).during(Duration.ofMinutes(5)),
        // Hold: 100 users/sec constante por 30 minutos
        constantUsersPerSec(100).during(Duration.ofMinutes(30)),
        // Ramp down: 100 → 0 users/sec en 2 minutos
        rampUsersPerSec(100).to(0).during(Duration.ofMinutes(2))
    )
);

// ═══════════════════════════════════════════════════════════════
// SPIKE TEST
// ═══════════════════════════════════════════════════════════════
setUp(
    scn.injectOpen(
        // Baseline
        constantUsersPerSec(10).during(Duration.ofMinutes(2)),
        // SPIKE
        stressPeakUsers(500).during(Duration.ofSeconds(10)),
        // Sustained spike
        constantUsersPerSec(50).during(Duration.ofMinutes(3)),
        // Back to baseline
        rampUsersPerSec(50).to(10).during(Duration.ofSeconds(30)),
        constantUsersPerSec(10).during(Duration.ofMinutes(2))
    )
);

// ═══════════════════════════════════════════════════════════════
// SOAK TEST (endurance)
// ═══════════════════════════════════════════════════════════════
setUp(
    scn.injectClosed(
        rampConcurrentUsers(0).to(50).during(Duration.ofMinutes(5)),
        constantConcurrentUsers(50).during(Duration.ofHours(4))  // 4 horas
    )
);
```

### Open vs Closed — ¿Cuándo usar cada uno?

```
┌─────────────────────────────────────────────────────────────────┐
│                OPEN vs CLOSED WORKLOAD MODEL                     │
├───────────────────────────────┬─────────────────────────────────┤
│         OPEN MODEL            │         CLOSED MODEL            │
├───────────────────────────────┼─────────────────────────────────┤
│ Controla: tasa de llegada     │ Controla: concurrencia fija     │
│                               │                                 │
│ "20 usuarios NUEVOS cada      │ "Siempre hay EXACTAMENTE 50    │
│  segundo, sin importar        │  usuarios ejecutando, cuando   │
│  cuántos están activos"       │  uno termina, otro empieza"    │
│                               │                                 │
│ Realista para: web público    │ Realista para: call centers,   │
│ (usuarios llegan sin control) │ APIs con pool fijo de clientes │
│                               │                                 │
│ Si el server se pone lento:   │ Si el server se pone lento:   │
│ → se acumulan más usuarios    │ → el throughput BAJA           │
│ → la concurrencia SUBE        │ → la concurrencia se MANTIENE  │
│ → puede causar avalancha      │ → efecto auto-regulador        │
│                               │                                 │
│ Más agresivo (realista)       │ Más conservador (controlado)   │
├───────────────────────────────┼─────────────────────────────────┤
│ USAR PARA:                    │ USAR PARA:                      │
│ • Load testing web público    │ • Capacity planning             │
│ • Stress testing              │ • Baseline testing              │
│ • Spike testing               │ • Sistemas batch/queue          │
│ • Tests de resiliencia        │ • APIs con SLA de concurrencia │
└───────────────────────────────┴─────────────────────────────────┘
```

---

## 13. Control de Flujo (Loops, Conditions, Errors)

### Condiciones (doIf, doIfOrElse, doSwitch)

```java
// ─── doIf: ejecutar si condición es true ───
.doIf(session -> session.getString("role").equals("admin")).then(
    exec(http("Admin Dashboard").get("/admin/dashboard"))
)

// ─── doIf con Expression Language ───
.doIf("#{isLoggedIn}").then(
    exec(http("Profile").get("/profile"))
)

// ─── doIfOrElse ───
.doIfOrElse(session -> session.getInt("cartItems") > 0).then(
    exec(http("Checkout").post("/checkout"))
).orElse(
    exec(http("Continue Shopping").get("/products"))
)

// ─── doSwitch ───
.doSwitch("#{userType}").on(
    Choice.withKey("premium", exec(http("Premium Features").get("/premium"))),
    Choice.withKey("standard", exec(http("Standard Features").get("/standard"))),
    Choice.withKey("trial", exec(http("Trial Features").get("/trial")))
)

// ─── doSwitchOrElse ───
.doSwitchOrElse("#{region}").on(
    Choice.withKey("US", exec(http("US API").get("/api/us/data"))),
    Choice.withKey("EU", exec(http("EU API").get("/api/eu/data")))
).orElse(
    exec(http("Global API").get("/api/global/data"))
)

// ─── randomSwitch (probabilístico) ───
.randomSwitch().on(
    Choice.withWeight(60.0, exec(http("Browse").get("/products"))),    // 60%
    Choice.withWeight(30.0, exec(http("Search").get("/search"))),      // 30%
    Choice.withWeight(10.0, exec(http("Purchase").post("/checkout")))  // 10%
)

// ─── uniformRandomSwitch (equiprobable) ───
.uniformRandomSwitch().on(
    exec(http("Option A").get("/a")),
    exec(http("Option B").get("/b")),
    exec(http("Option C").get("/c"))
)

// ─── roundRobinSwitch ───
.roundRobinSwitch().on(
    exec(http("Server 1").get("http://server1/api")),
    exec(http("Server 2").get("http://server2/api")),
    exec(http("Server 3").get("http://server3/api"))
)
```

### Loops (repeat, foreach, during, forever)

```java
// ─── repeat: N iteraciones ───
.repeat(10).on(
    exec(http("Repeated Request").get("/api/data"))
    .pause(1)
)

// ─── repeat con counter ───
.repeat(5, "pageNum").on(
    exec(
        http("Page #{pageNum}")
            .get("/api/products?page=#{pageNum}")
    )
    .pause(2)
)

// ─── foreach: iterar sobre lista de session ───
.foreach("#{productIds}", "productId").on(
    exec(
        http("Get Product #{productId}")
            .get("/api/products/#{productId}")
    )
    .pause(1)
)

// ─── during: ejecutar durante un tiempo ───
.during(Duration.ofMinutes(5)).on(
    exec(http("Continuous Request").get("/api/stream"))
    .pause(1, 3)
)

// ─── asLongAs: mientras condición sea true ───
.asLongAs(session -> session.getInt("retryCount") < 3).on(
    exec(
        http("Retry Request")
            .get("/api/eventually-consistent")
            .check(
                jmesPath("status").saveAs("currentStatus")
            )
    )
    .doIf(session -> !"ready".equals(session.getString("currentStatus"))).then(
        exec(session -> session.set("retryCount", session.getInt("retryCount") + 1))
        .pause(Duration.ofSeconds(5))
    )
)

// ─── forever: loop infinito (controlado por injection duration) ───
.forever().on(
    exec(http("Heartbeat").get("/api/health"))
    .pause(Duration.ofSeconds(30))
)
```

### Error handling

```java
// ─── exitHereIfFailed: parar si el request anterior falló ───
.exec(http("Login").post("/auth/login").check(status().is(200)))
.exitHereIfFailed()  // Si login falla, este usuario termina aquí
.exec(http("Dashboard").get("/dashboard"))

// ─── tryMax: reintentar N veces si falla ───
.tryMax(3).on(
    exec(
        http("Flaky Request")
            .get("/api/sometimes-fails")
            .check(status().is(200))
    )
).exitHereIfFailed()

// ─── exitBlockOnFail: salir del bloque actual si falla ───
.exitBlockOnFail().on(
    exec(http("Step 1").get("/step1").check(status().is(200)))
    .exec(http("Step 2").get("/step2").check(status().is(200)))
    .exec(http("Step 3").get("/step3").check(status().is(200)))
)
// Si cualquier step falla, salta al siguiente bloque

// ─── Manejo de errores con doIf ───
.exec(
    http("Might Fail")
        .get("/api/resource")
        .check(status().saveAs("lastStatus"))
)
.doIf(session -> session.getInt("lastStatus") == 404).then(
    exec(http("Create Resource").post("/api/resource").body(StringBody("{}")))
)
```

---

## 14. Pause, Pacing y Think Time

### Tipos de pause

```java
// ─── Pause fija ───
.pause(5)                                    // 5 segundos exactos
.pause(Duration.ofMillis(500))              // 500ms exactos

// ─── Pause aleatoria uniforme ───
.pause(2, 8)                                 // Random 2-8 segundos
.pause(Duration.ofSeconds(1), Duration.ofSeconds(5))

// ─── Pause con Expression Language ───
.pause("#{thinkTime}")                       // Valor de session

// ─── Pause con función ───
.pause(session -> Duration.ofMillis(
    ThreadLocalRandom.current().nextLong(1000, 5000)
))

// ─── Disable pause (para debug o stress puro) ───
// En el protocolo:
// .disablePauses()
// .uniformPausesPlusOrMinusPercentage(20)  // ±20% variación
// .customPauses(session -> 0L)             // Sin pausa (stress)
```

### Pace (control de throughput por iteración)

```java
// pace() garantiza que cada iteración tome EXACTAMENTE N tiempo
// Si la iteración tarda menos, espera la diferencia
// Si tarda más, NO espera (continúa inmediatamente)

.forever().on(
    pace(Duration.ofSeconds(5))  // 1 iteración cada 5 segundos
    .exec(
        http("Paced Request").get("/api/data")
        // Si este request tarda 1s → espera 4s
        // Si tarda 4s → espera 1s
        // Si tarda 6s → no espera (ya excedió)
    )
)

// Pace aleatorio
.forever().on(
    pace(Duration.ofSeconds(3), Duration.ofSeconds(8))  // 3-8 sec entre iteraciones
    .exec(/* ... */)
)
```

### Configuración global de pauses

```java
HttpProtocolBuilder httpProtocol = http
    .baseUrl("https://api.example.com")
    // Estrategias de pause globales:
    .pauses(constantPauses())           // Default: respetar valores exactos
    // .pauses(uniformPauses(0.2))      // ±20% variación sobre el valor
    // .pauses(customPauses(session -> Duration.ZERO))  // Sin pauses
    // .pauses(disabledPauses())        // Desactivar completamente
    ;
```

---

## 15. Assertions (Criterios de Aceptación)

### Assertions disponibles

```java
setUp(/* ... */)
.assertions(
    // ═══════ SCOPE: global (todos los requests) ═══════
    
    // Response time
    global().responseTime().mean().lt(1000),           // Average < 1s
    global().responseTime().max().lt(10000),           // Max < 10s
    global().responseTime().percentile1().lt(500),     // P50 < 500ms
    global().responseTime().percentile2().lt(800),     // P75 < 800ms
    global().responseTime().percentile3().lt(2000),    // P95 < 2s
    global().responseTime().percentile4().lt(5000),    // P99 < 5s
    
    // Success rate
    global().successfulRequests().percent().gt(99.0),  // > 99% success
    global().failedRequests().percent().lt(1.0),       // < 1% failures
    global().failedRequests().count().lt(100L),        // < 100 failures total
    
    // Throughput
    global().requestsPerSec().gt(500.0),              // > 500 req/sec
    
    // ═══════ SCOPE: forAll (cada request individualmente) ═══════
    
    forAll().responseTime().max().lt(15000),           // Ningún request > 15s
    forAll().failedRequests().percent().lt(5.0),       // Cada endpoint < 5% fail
    
    // ═══════ SCOPE: details (request específico) ═══════
    
    details("POST /auth/login")
        .responseTime().percentile3().lt(1000),       // Login P95 < 1s
    details("POST /checkout")
        .responseTime().mean().lt(2000),              // Checkout avg < 2s
    details("GET /api/products")
        .requestsPerSec().gt(200.0),                  // Products > 200 RPS
    
    // ═══════ SCOPE: details con grupo ═══════
    
    details("Purchase Flow", "POST /checkout")
        .successfulRequests().percent().gt(98.0)
);
```

### Assertions como Quality Gate en CI/CD

```java
// Si CUALQUIER assertion falla:
// - El exit code de Gatling será != 0
// - Maven/Gradle build falla
// - CI/CD pipeline se detiene

// Esto permite usar assertions como quality gate:
setUp(
    scn.injectOpen(constantUsersPerSec(50).during(Duration.ofMinutes(5)))
)
.protocols(httpProtocol)
.assertions(
    // Quality Gate para deploy a producción
    global().responseTime().percentile3().lt(2000),    // SLO: P95 < 2s
    global().successfulRequests().percent().gt(99.5),  // SLO: 99.5% success
    global().requestsPerSec().gt(100.0)               // Capacity: > 100 RPS
);
```

---

## 16. Gatling Recorder

### ¿Qué es?

El Gatling Recorder captura tráfico HTTP/HTTPS y genera automáticamente simulaciones Gatling.

### Modos de operación

```
┌─────────────────────────────────────────────────────────────┐
│                    GATLING RECORDER                           │
├─────────────────────────┬───────────────────────────────────┤
│   PROXY MODE            │   HAR CONVERTER MODE              │
├─────────────────────────┼───────────────────────────────────┤
│ Actúa como proxy HTTP   │ Convierte archivo HAR             │
│ entre browser y server  │ (exportado desde DevTools)        │
│                         │                                    │
│ Browser → Recorder →    │ Browser graba → Export HAR →      │
│   Server               │   Recorder convierte              │
│                         │                                    │
│ Captura todo en         │ No requiere configurar proxy      │
│ tiempo real             │ Más simple pero menos control     │
└─────────────────────────┴───────────────────────────────────┘
```

### Uso del Recorder

```bash
# Iniciar el recorder (bundle)
./bin/recorder.sh

# Iniciar el recorder (Maven)
mvn gatling:recorder

# Iniciar el recorder (Gradle)
./gradlew gatlingRecorder
```

### Configuración del Recorder

```
1. Listening port: 8000 (configurar browser proxy a localhost:8000)
2. HTTPS mode: Certificate Authority (generar cert para HTTPS)
3. Simulation class name: RecordedSimulation
4. Output folder: src/test/java/simulations/
5. Format: Java 17 (o Kotlin/Scala)

Filtros recomendados (excluir):
- .*\.(css|js|ico|png|jpg|gif|svg|woff|woff2|ttf|eot)
- .*google-analytics.*
- .*facebook.*
- .*hotjar.*
```

### Post-procesamiento del recording

```java
// Código generado por el recorder (antes de limpiar):
public class RecordedSimulation extends Simulation {
    
    // El recorder genera requests literales - hay que parametrizar:
    
    // ANTES (generado):
    http("request_1").get("/api/users/12345")
    
    // DESPUÉS (parametrizado):
    http("Get User Profile")
        .get("/api/users/#{userId}")
        .check(jmesPath("name").saveAs("userName"))
    
    // ANTES (hardcoded token):
    .header("Authorization", "Bearer eyJhbGciOiJIUzI1NiI...")
    
    // DESPUÉS (dinámico):
    .header("Authorization", "Bearer #{authToken}")
}
```

---

## 17. Reportes y Análisis

### Reporte HTML automático

Gatling genera automáticamente un reporte HTML detallado al finalizar cada test.

```
target/gatling/[simulation-name]-[timestamp]/
├── index.html              ← Reporte principal (abrir en browser)
├── js/
├── style/
└── simulation.log          ← Raw data (para análisis custom)
```

### Contenido del reporte

```
┌─────────────────────────────────────────────────────────────────┐
│                    GATLING HTML REPORT                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  📊 GLOBAL INFORMATION                                           │
│  ├── Total requests / OK / KO                                    │
│  ├── Min / Max / Mean / Std Dev response time                    │
│  ├── Percentiles: P50, P75, P95, P99                            │
│  └── Requests/sec                                                │
│                                                                   │
│  📈 RESPONSE TIME DISTRIBUTION                                   │
│  └── Histograma de distribución de tiempos                      │
│                                                                   │
│  📉 RESPONSE TIME PERCENTILES OVER TIME                          │
│  └── P50, P75, P95, P99 a lo largo del test                    │
│                                                                   │
│  👥 ACTIVE USERS OVER TIME                                       │
│  └── Usuarios activos concurrentes durante el test              │
│                                                                   │
│  🔄 REQUESTS PER SECOND                                          │
│  └── Throughput a lo largo del tiempo                            │
│                                                                   │
│  ❌ RESPONSES PER SECOND                                         │
│  └── OK vs KO responses por segundo                             │
│                                                                   │
│  📋 REQUEST DETAILS (por cada request)                           │
│  └── Stats individuales por nombre de request                    │
│                                                                   │
│  ⚡ ASSERTIONS RESULTS                                           │
│  └── PASSED / FAILED para cada assertion definida               │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Análisis del simulation.log

```bash
# El simulation.log contiene raw data en formato tabular
# Útil para análisis custom con pandas, Excel, etc.

# Formato de cada línea:
# REQUEST\tscenario\tuserId\tname\tstart\tend\tstatus\tmessage
# RUN\tsimulationName\tdescription\tstart\tend

# Ejemplo de análisis con scripts:
# Extraer requests fallidos
grep "KO" simulation.log | head -20

# Contar requests por endpoint
awk -F'\t' '/^REQUEST/ {print $4}' simulation.log | sort | uniq -c | sort -rn
```

### Integración con Grafana (via InfluxDB)

```hocon
# En gatling.conf - enviar métricas a Graphite/InfluxDB
gatling {
  data {
    writers = [console, file, graphite]
    
    graphite {
      host = "influxdb.monitoring.svc"
      port = 2003
      protocol = "tcp"
      rootPathPrefix = "gatling"
      bufferSize = 8192
      writePeriod = 1  # segundo
    }
  }
}
```

---

## 18. Protocolos Adicionales (WebSocket, SSE, JMS)

### WebSocket

```java
import static io.gatling.javaapi.http.HttpDsl.*;

ScenarioBuilder wsScenario = scenario("WebSocket Test")
    .exec(
        http("Connect")
            .get("/")  // Página que inicia WebSocket
    )
    .exec(
        ws("Connect WS")
            .connect("/ws/chat")
            .onConnected(
                exec(
                    ws("Join Room")
                        .sendText("{\"action\":\"join\",\"room\":\"general\"}")
                )
            )
    )
    .pause(1)
    .exec(
        ws("Send Message")
            .sendText("{\"action\":\"message\",\"text\":\"Hello from Gatling!\"}")
            .await(Duration.ofSeconds(5)).on(
                ws.checkTextMessage("Check Response")
                    .check(jmesPath("type").is("message_ack"))
            )
    )
    .pause(2)
    .repeat(10).on(
        exec(
            ws("Send Ping")
                .sendText("{\"action\":\"ping\"}")
                .await(Duration.ofSeconds(3)).on(
                    ws.checkTextMessage("Pong")
                        .check(jmesPath("action").is("pong"))
                )
        )
        .pause(1)
    )
    .exec(ws("Close").close());
```

### Server-Sent Events (SSE)

```java
ScenarioBuilder sseScenario = scenario("SSE Test")
    .exec(
        sse("Connect SSE")
            .connect("/api/events/stream")
            .await(Duration.ofSeconds(10)).on(
                sse.checkMessage("First Event")
                    .check(jmesPath("type").is("connected"))
            )
    )
    .pause(Duration.ofSeconds(5))
    .exec(
        sse("Wait for Data")
            .setCheck()
            .await(Duration.ofSeconds(30)).on(
                sse.checkMessage("Data Event")
                    .check(jmesPath("data.value").exists())
            )
    )
    .exec(sse("Close SSE").close());
```

### JMS (Java Messaging Service)

```java
import static io.gatling.javaapi.jms.JmsDsl.*;

JmsProtocolBuilder jmsProtocol = jms
    .connectionFactory(
        new ActiveMQConnectionFactory("tcp://localhost:61616")
    )
    .credentials("admin", "admin")
    .listenerThreadCount(5);

ScenarioBuilder jmsScenario = scenario("JMS Test")
    .exec(
        jms("Send Order")
            .send()
            .destination(queue("orders.input"))
            .textMessage("{\"orderId\":\"#{orderId}\",\"amount\":99.99}")
            .property("JMSType", "OrderRequest")
    )
    .exec(
        jms("Request-Reply")
            .requestReply()
            .destination(queue("orders.process"))
            .replyDestination(queue("orders.reply"))
            .textMessage("{\"action\":\"process\"}")
            .check(
                jmesPath("status").is("processed"),
                simpleCheck(msg -> msg != null)
            )
    );
```

---

## 19. Integración con CI/CD

### GitHub Actions

```yaml
# .github/workflows/performance-test.yml
name: Performance Test

on:
  pull_request:
    branches: [main, develop]
  schedule:
    - cron: '0 4 * * 1-5'  # Lun-Vie 4 AM
  workflow_dispatch:
    inputs:
      users:
        description: 'Target users per second'
        default: '50'
      duration:
        description: 'Test duration (seconds)'
        default: '300'

jobs:
  gatling-test:
    runs-on: ubuntu-latest
    environment: staging
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'
          cache: 'maven'
      
      - name: Run Gatling Load Test
        run: |
          mvn gatling:test \
            -Dgatling.simulationClass=simulations.LoadTestSimulation \
            -DtargetHost=${{ secrets.STAGING_URL }} \
            -Dusers=${{ inputs.users || '50' }} \
            -Dduration=${{ inputs.duration || '300' }}
        continue-on-error: false  # Falla si assertions fallan
      
      - name: Upload Gatling Report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: gatling-report-${{ github.run_id }}
          path: target/gatling/**/index.html
          retention-days: 30
      
      - name: Publish Report to GitHub Pages
        if: github.ref == 'refs/heads/main'
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: target/gatling/
          destination_dir: performance-reports/${{ github.run_id }}
```

### Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent { label 'performance' }
    
    parameters {
        string(name: 'USERS', defaultValue: '100', description: 'Target users')
        string(name: 'DURATION', defaultValue: '600', description: 'Duration (seconds)')
        choice(name: 'ENVIRONMENT', choices: ['staging', 'preprod'], description: 'Target env')
    }
    
    stages {
        stage('Run Gatling') {
            steps {
                sh """
                    mvn gatling:test \
                        -Dgatling.simulationClass=simulations.LoadTestSimulation \
                        -Dusers=${params.USERS} \
                        -Dduration=${params.DURATION} \
                        -DtargetHost=${env."${params.ENVIRONMENT}_URL"}
                """
            }
            post {
                always {
                    gatlingArchive()  // Jenkins Gatling plugin
                }
            }
        }
    }
}
```

### Maven profiles para diferentes tipos de test

```xml
<!-- pom.xml profiles -->
<profiles>
    <profile>
        <id>smoke</id>
        <properties>
            <gatling.simulationClass>simulations.SmokeTestSimulation</gatling.simulationClass>
            <users>5</users>
            <duration>60</duration>
        </properties>
    </profile>
    <profile>
        <id>load</id>
        <properties>
            <gatling.simulationClass>simulations.LoadTestSimulation</gatling.simulationClass>
            <users>100</users>
            <duration>1800</duration>
        </properties>
    </profile>
    <profile>
        <id>stress</id>
        <properties>
            <gatling.simulationClass>simulations.StressTestSimulation</gatling.simulationClass>
            <users>500</users>
            <duration>600</duration>
        </properties>
    </profile>
    <profile>
        <id>soak</id>
        <properties>
            <gatling.simulationClass>simulations.SoakTestSimulation</gatling.simulationClass>
            <users>50</users>
            <duration>14400</duration>
        </properties>
    </profile>
</profiles>
```

```bash
# Ejecutar con profile
mvn gatling:test -Psmoke
mvn gatling:test -Pload
mvn gatling:test -Pstress -DtargetHost=https://staging.example.com
```

---

## 20. Patrones Avanzados

### 20.1 Correlation (Extracción dinámica)

```java
// Extraer token de login → usar en requests siguientes
ChainBuilder loginAndExtract = exec(
    http("Login")
        .post("/api/auth/login")
        .body(StringBody("{\"email\":\"#{email}\",\"password\":\"#{password}\"}"))
        .check(
            jmesPath("access_token").saveAs("token"),
            jmesPath("refresh_token").saveAs("refreshToken"),
            jmesPath("user.id").saveAs("userId")
        )
);

// Crear recurso → extraer ID → usar en operaciones posteriores
ChainBuilder createAndUse = exec(
    http("Create Order")
        .post("/api/orders")
        .header("Authorization", "Bearer #{token}")
        .body(ElFileBody("bodies/order.json"))
        .check(
            status().is(201),
            jmesPath("order_id").saveAs("orderId"),
            header("Location").saveAs("orderUrl")
        )
)
.pause(2)
.exec(
    http("Get Order Status")
        .get("/api/orders/#{orderId}/status")
        .header("Authorization", "Bearer #{token}")
        .check(jmesPath("status").is("pending"))
);
```

### 20.2 Polling (esperar condición asíncrona)

```java
// Polling hasta que un proceso asíncrono termine
ChainBuilder pollUntilComplete = exec(session -> session.set("pollAttempts", 0))
    .asLongAs(session -> 
        !"completed".equals(session.getString("jobStatus")) 
        && session.getInt("pollAttempts") < 20
    ).on(
        exec(session -> session.set("pollAttempts", session.getInt("pollAttempts") + 1))
        .exec(
            http("Poll Job Status")
                .get("/api/jobs/#{jobId}/status")
                .header("Authorization", "Bearer #{token}")
                .check(
                    jmesPath("status").saveAs("jobStatus")
                )
        )
        .pause(Duration.ofSeconds(3))  // Esperar 3s entre polls
    )
    .doIf(session -> !"completed".equals(session.getString("jobStatus"))).then(
        exec(session -> {
            System.out.println("Job did not complete in time!");
            return session.markAsFailed();
        })
    );
```

### 20.3 Token refresh automático

```java
// Refresh token cuando está por expirar
ChainBuilder refreshTokenIfNeeded = doIf(session -> {
    long expiry = session.getLong("tokenExpiry");
    return System.currentTimeMillis() / 1000 > expiry - 60; // 60s antes de expirar
}).then(
    exec(
        http("Refresh Token")
            .post("/api/auth/refresh")
            .body(StringBody("{\"refresh_token\":\"#{refreshToken}\"}"))
            .check(
                jmesPath("access_token").saveAs("token"),
                jmesPath("expires_in").ofInt()
                    .transform(exp -> String.valueOf(System.currentTimeMillis() / 1000 + exp))
                    .saveAs("tokenExpiry")
            )
    )
);

// Usar antes de cada request protegido
ScenarioBuilder secureScenario = scenario("Secure Flow")
    .exec(loginAndExtract)
    .repeat(100).on(
        exec(refreshTokenIfNeeded)
        .exec(http("Protected Request").get("/api/data").header("Authorization", "Bearer #{token}"))
        .pause(5, 15)
    );
```

### 20.4 File download con validación

```java
ChainBuilder downloadAndValidate = exec(
    http("Download Report")
        .get("/api/reports/#{reportId}/download")
        .header("Authorization", "Bearer #{token}")
        .check(
            status().is(200),
            header("Content-Type").is("application/pdf"),
            header("Content-Length").ofInt().gt(1000),  // > 1KB
            bodyBytes().transform(bytes -> bytes.length).gt(1000).saveAs("fileSize")
        )
);
```

### 20.5 Simulación realista con grupos

```java
// Groups agrupa requests bajo un nombre común en el reporte
ScenarioBuilder realisticScenario = scenario("E-Commerce Journey")
    .exec(loginAndExtract)
    .group("Homepage").on(
        exec(http("GET /").get("/"))
        .exec(http("GET /api/featured").get("/api/featured"))
        .exec(http("GET /api/banners").get("/api/banners"))
    )
    .pause(3, 8)
    .group("Product Discovery").on(
        exec(http("Search").get("/api/search?q=#{searchTerm}"))
        .pause(2, 5)
        .exec(http("Product Detail").get("/api/products/#{productId}"))
        .exec(http("Product Reviews").get("/api/products/#{productId}/reviews"))
    )
    .pause(5, 15)
    .group("Checkout").on(
        exec(http("Add to Cart").post("/api/cart/items").body(/* ... */))
        .pause(1, 3)
        .exec(http("Get Cart").get("/api/cart"))
        .pause(2, 5)
        .exec(http("Checkout").post("/api/checkout").body(/* ... */))
    );
```

---

## 21. Debugging y Troubleshooting

### Logging configuration

```xml
<!-- src/test/resources/logback-test.xml -->
<configuration>
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} [%-5level] %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>

    <!-- Gatling core logging -->
    <logger name="io.gatling" level="WARN"/>
    
    <!-- HTTP request/response logging (SOLO para debug) -->
    <!-- NUNCA activar en tests reales - destruye el rendimiento -->
    <logger name="io.gatling.http.engine.response" level="DEBUG"/>
    
    <!-- Tus simulaciones -->
    <logger name="simulations" level="DEBUG"/>

    <root level="WARN">
        <appender-ref ref="CONSOLE"/>
    </root>
</configuration>
```

### Debug de session

```java
// Imprimir session completa (SOLO para debug, NUNCA bajo carga)
.exec(session -> {
    System.out.println("=== SESSION STATE ===");
    System.out.println("User ID: " + session.userId());
    System.out.println("Scenario: " + session.scenario());
    session.asMap().forEach((k, v) -> System.out.println("  " + k + " = " + v));
    System.out.println("====================");
    return session;
})

// Verificar que un valor existe
.doIf(session -> !session.contains("token")).then(
    exec(session -> {
        System.err.println("WARNING: No token in session for user " + session.userId());
        return session.markAsFailed();
    })
)
```

### Problemas comunes

```
┌─────────────────────────────────────────────────────────────────┐
│ PROBLEMA                    │ CAUSA                │ SOLUCIÓN    │
├─────────────────────────────┼──────────────────────┼─────────────┤
│ "Session attribute not      │ Check no guardó el   │ Verificar   │
│  found: token"              │ valor (request falló)│ exitHere... │
│                             │                      │             │
│ "Connection refused"        │ Target no levantado  │ Verificar   │
│                             │ o puerto incorrecto  │ host/port   │
│                             │                      │             │
│ "Request timeout"           │ Server no responde   │ Aumentar    │
│                             │ en tiempo            │ timeout     │
│                             │                      │             │
│ OutOfMemoryError            │ Demasiados VUs o     │ Más heap:   │
│                             │ body responses huge  │ -Xmx4g     │
│                             │                      │             │
│ "Feeder is now empty"       │ queue() feeder sin   │ Usar        │
│                             │ más datos            │ circular()  │
│                             │                      │             │
│ CPU 100% en load gen        │ Demasiados VUs para  │ Reducir VUs │
│                             │ una máquina          │ o distribuir│
│                             │                      │             │
│ Checks siempre fallan       │ Status != esperado   │ Log HTTP    │
│                             │ (auth, redirect)     │ response    │
└─────────────────────────────┴──────────────────────┴─────────────┘
```

### JVM Tuning para Gatling

```bash
# Configurar JVM para alto rendimiento
export JAVA_OPTS="\
  -server \
  -Xms2g -Xmx4g \
  -XX:+UseG1GC \
  -XX:+ParallelRefProcEnabled \
  -XX:MaxInlineLevel=20 \
  -XX:MaxTrivialSize=12 \
  -XX:-UseBiasedLocking \
  -XX:+OptimizeStringConcat"

# O en Maven:
mvn gatling:test -DargLine="-Xms2g -Xmx4g -XX:+UseG1GC"
```

---

## 22. Community vs Enterprise Edition

### Tabla comparativa detallada

| Feature | Community (Free) | Enterprise (Paid) |
|---------|:----------------:|:-----------------:|
| Java/Kotlin/Scala DSL | ✅ | ✅ |
| HTTP/HTTPS Protocol | ✅ | ✅ |
| WebSocket Protocol | ✅ | ✅ |
| SSE Protocol | ✅ | ✅ |
| JMS Protocol | ✅ | ✅ |
| MQTT Protocol | ❌ | ✅ |
| JDBC Protocol | ❌ | ✅ |
| gRPC Protocol | ❌ | ✅ |
| HTML Reports | ✅ | ✅ |
| Real-time Dashboards | ❌ | ✅ |
| Distributed Testing | ❌ | ✅ |
| Cloud Load Generators | ❌ | ✅ |
| CI/CD Plugins (advanced) | ❌ | ✅ |
| Trend Analysis | ❌ | ✅ |
| Team Management | ❌ | ✅ |
| SSO/LDAP | ❌ | ✅ |
| API for triggering tests | ❌ | ✅ |
| Scheduled runs | ❌ | ✅ |
| Commercial Support | ❌ | ✅ |
| Recorder | ✅ | ✅ |
| Assertions | ✅ | ✅ |
| Feeders | ✅ | ✅ |
| Maven/Gradle/SBT | ✅ | ✅ |
| Max users (1 machine) | ~50,000 | Unlimited (distributed) |

### Workarounds para limitaciones de Community

```
Limitación: Sin distributed testing
Workaround:
  - Ejecutar múltiples instancias contra el mismo target
  - Agregar resultados manualmente
  - Usar CI/CD para coordinar múltiples runners
  - Considerar: k6 (cloud) o Locust (distribuido gratis)

Limitación: Sin dashboards real-time  
Workaround:
  - Configurar Graphite writer → InfluxDB → Grafana
  - Ver métricas en tiempo real via Grafana
  
Limitación: Sin MQTT/JDBC/gRPC
Workaround:
  - MQTT: usar Paho client dentro de exec(session -> ...)
  - JDBC: usar JDBC directo en session functions
  - gRPC: usar stubs generados con protobuf
```

---

## 23. Mejores Prácticas y Antipatrones

### ✅ Mejores Prácticas

```java
// 1. USAR EXPRESSION LANGUAGE PARA VALORES DINÁMICOS
// BUENO:
.get("/api/users/#{userId}")
// MALO (concatenación):
.get(session -> "/api/users/" + session.getString("userId"))
// EL es más eficiente y legible

// 2. AGRUPAR REQUESTS DINÁMICOS
// BUENO:
.get("/api/products/#{productId}")
// Gatling agrupa automáticamente por nombre del request

// 3. USAR exitHereIfFailed DESPUÉS DE REQUESTS CRÍTICOS
.exec(http("Login").post("/auth").check(status().is(200)))
.exitHereIfFailed()  // No continuar sin auth

// 4. CHAINS REUTILIZABLES PARA DRY
ChainBuilder auth = exec(/* login */).exec(/* set headers */);
// Reutilizar en múltiples scenarios

// 5. PARÁMETROS EXTERNALIZADOS
int users = Integer.parseInt(System.getProperty("users", "100"));
String host = System.getProperty("targetHost", "https://staging.example.com");

// 6. FEEDERS CIRCULARES PARA TESTS LARGOS
csv("data.csv").circular()  // No se acaban los datos

// 7. ASSERTIONS COMO QUALITY GATES
.assertions(
    global().responseTime().percentile3().lt(2000),
    global().successfulRequests().percent().gt(99.0)
)
```

### ❌ Antipatrones

```java
// ANTIPATRÓN 1: Blocking I/O en session functions
exec(session -> {
    // ❌ NUNCA hacer esto - bloquea el actor system
    HttpClient.newHttpClient().send(request, handler);
    Thread.sleep(1000);
    Files.readAllBytes(Path.of("/huge/file"));
    return session;
})

// ANTIPATRÓN 2: System.out.println bajo carga
exec(session -> {
    // ❌ sysout es blocking I/O
    System.out.println("User " + session.userId());
    return session;
})
// ✅ Usar logging framework con nivel apropiado

// ANTIPATRÓN 3: No manejar fallos de extracción
.exec(http("Get Data").get("/api/data"))
// Si el check falla, "token" no existirá en session
.exec(http("Use Token").get("/api/protected").header("Auth", "#{token}"))
// ✅ Usar .exitHereIfFailed() o .doIf(session.contains("token"))

// ANTIPATRÓN 4: Think time = 0 (no es realista)
.pause(0)  // ❌ Esto no simula usuarios reales
// ✅ Usar pauses basados en datos de producción

// ANTIPATRÓN 5: Un solo scenario monolítico gigante
// ❌ 500 líneas en un solo scenario
// ✅ Dividir en chains, componer scenarios

// ANTIPATRÓN 6: Ignorar el modelo de carga
setUp(scn.injectOpen(atOnceUsers(10000)))  // ❌ Spike irreal
// ✅ Ramp realista: rampUsers(10000).during(5.minutes)

// ANTIPATRÓN 7: No configurar timeouts
// ❌ Default timeout puede ser muy largo
// ✅ Configurar requestTimeout apropiado para tu SLA
```

---

## 24. Proyecto de Referencia Completo

### Estructura final del proyecto

```
gatling-perf-tests/
├── pom.xml
├── Makefile
├── README.md
├── .github/
│   └── workflows/
│       └── performance.yml
├── src/
│   └── test/
│       ├── java/
│       │   ├── config/
│       │   │   ├── TestConfig.java          # Configuración centralizada
│       │   │   └── Protocols.java           # HTTP protocols
│       │   ├── chains/
│       │   │   ├── AuthChain.java           # Login/token management
│       │   │   ├── ProductChain.java        # CRUD de productos
│       │   │   └── CheckoutChain.java       # Flujo de compra
│       │   ├── feeders/
│       │   │   └── CustomFeeders.java       # Feeders programáticos
│       │   └── simulations/
│       │       ├── SmokeTestSimulation.java
│       │       ├── LoadTestSimulation.java
│       │       ├── StressTestSimulation.java
│       │       ├── SpikeTestSimulation.java
│       │       ├── SoakTestSimulation.java
│       │       └── BreakpointSimulation.java
│       └── resources/
│           ├── gatling.conf
│           ├── logback-test.xml
│           ├── feeders/
│           │   ├── users.csv
│           │   ├── products.json
│           │   └── search_terms.csv
│           └── bodies/
│               ├── create_order.json
│               └── update_user.json
└── target/
    └── gatling/                             # Reports (gitignored)
```

### Ejemplo: Config centralizada

```java
// config/TestConfig.java
package config;

public class TestConfig {
    
    // Target
    public static final String BASE_URL = 
        System.getProperty("targetHost", "https://api.staging.example.com");
    
    // Users
    public static final int TARGET_USERS = 
        Integer.parseInt(System.getProperty("users", "100"));
    
    public static final int RAMP_DURATION_SEC = 
        Integer.parseInt(System.getProperty("rampDuration", "120"));
    
    public static final int HOLD_DURATION_SEC = 
        Integer.parseInt(System.getProperty("duration", "600"));
    
    // Thresholds
    public static final int P95_MAX_MS = 
        Integer.parseInt(System.getProperty("p95Max", "2000"));
    
    public static final double MIN_SUCCESS_RATE = 
        Double.parseDouble(System.getProperty("minSuccessRate", "99.0"));
    
    // Think time
    public static final int THINK_TIME_MIN_SEC = 2;
    public static final int THINK_TIME_MAX_SEC = 8;
}
```

### Makefile para el proyecto

```makefile
.PHONY: smoke load stress spike soak breakpoint recorder clean

# Variables
HOST ?= https://api.staging.example.com
USERS ?= 100
DURATION ?= 600

smoke:
	mvn gatling:test -Psmoke -DtargetHost=$(HOST)

load:
	mvn gatling:test -Pload -DtargetHost=$(HOST) -Dusers=$(USERS) -Dduration=$(DURATION)

stress:
	mvn gatling:test -Pstress -DtargetHost=$(HOST)

spike:
	mvn gatling:test \
		-Dgatling.simulationClass=simulations.SpikeTestSimulation \
		-DtargetHost=$(HOST)

soak:
	mvn gatling:test -Psoak -DtargetHost=$(HOST)

breakpoint:
	mvn gatling:test \
		-Dgatling.simulationClass=simulations.BreakpointSimulation \
		-DtargetHost=$(HOST)

recorder:
	mvn gatling:recorder

report:
	@echo "Opening latest report..."
	@open target/gatling/$$(ls -t target/gatling/ | head -1)/index.html 2>/dev/null || \
		xdg-open target/gatling/$$(ls -t target/gatling/ | head -1)/index.html

clean:
	mvn clean
	rm -rf target/gatling/
```

---

## Referencias

- [Gatling Official Documentation](https://docs.gatling.io/)
- [Gatling GitHub Repository](https://github.com/gatling/gatling)
- [Gatling Academy (Free Courses)](https://academy.gatling.io/)
- [Gatling Community Forum](https://community.gatling.io/)
- [Gatling Maven Plugin](https://docs.gatling.io/reference/extensions/build-tools/maven-plugin/)
- [Gatling Gradle Plugin](https://docs.gatling.io/reference/extensions/build-tools/gradle-plugin/)
- [Gatling Highcharts (Reports)](https://github.com/gatling/gatling-highcharts)
- [Akka Documentation (underlying framework)](https://akka.io/docs/)
- [Netty Project](https://netty.io/)

---

> 💡 **Gatling Community Edition es ideal para equipos JVM que necesitan alto rendimiento local con reportes elegantes.**
> Su modelo actor-based y I/O no-bloqueante permiten simular decenas de miles de usuarios con una sola máquina, y su DSL en Java/Kotlin hace que los tests sean mantenibles como código de producción.
