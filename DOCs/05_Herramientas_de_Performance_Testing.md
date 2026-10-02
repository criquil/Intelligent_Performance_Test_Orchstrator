# 05 — Herramientas de Performance Testing

> **Rol de este archivo:** Índice intermedio. Compara las herramientas disponibles y dirige a la guía exhaustiva de cada una.  
> **Cuándo leer este archivo:** Cuando necesitas elegir una herramienta, comparar opciones, o saber qué guía consultar.  
> **Carpeta detallada:** [`05_Herramientas/`](05_Herramientas/)

---

## Comparativa Rápida de Herramientas

| Herramienta | Lenguaje | Modelo de ejecución | Protocolos | Curva de aprendizaje | Mejor para |
|-------------|----------|---------------------|------------|---------------------|------------|
| **k6** | JavaScript | Go engine, goja runtime | HTTP, gRPC, WS, Browser | Baja-Media | Developers, CI/CD, código como config |
| **JMeter** | Java/XML | Thread-per-user | HTTP, JDBC, JMS, FTP, LDAP, TCP, SMTP | Media | Multi-protocolo, equipos legacy, GUI |
| **Gatling** | Java/Kotlin/Scala | Akka actors, async NIO | HTTP, WS, SSE, JMS | Media-Alta | Alta concurrencia, equipos JVM |
| **Locust** | Python | gevent greenlets | HTTP (extensible a cualquiera) | Baja | Python teams, custom protocols, rapid prototyping |

### Decision Matrix — ¿Cuál elegir?

| Criterio | k6 | JMeter | Gatling | Locust |
|----------|-----|--------|---------|--------|
| CI/CD nativo | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Scripts como código | ⭐⭐⭐ | ⭐ (XML) | ⭐⭐⭐ | ⭐⭐⭐ |
| Comunidad y plugins | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| Multi-protocolo | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ (custom) |
| Performance del engine | ⭐⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐ |
| GUI / low-code | ⭐ | ⭐⭐⭐ | ⭐⭐ (recorder) | ⭐⭐ (web UI) |
| Distributed testing | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Cloud offering | Grafana Cloud | BlazeMeter | Gatling Enterprise | Locust Cloud |

---

## 📂 Contenido de la Subcarpeta

### [`01_k6_Guia_Completa.md`](05_Herramientas/01_k6_Guia_Completa.md) — Referencia Rápida (14 KB)
**Contenido:** Introducción · Instalación · Conceptos fundamentales · Scripting avanzado · Scenarios múltiples · Output y reporting · CI/CD integration · Extensiones xk6

**Ir aquí si necesitas:** Una referencia compacta para empezar con k6 rápidamente.

---

### [`02_JMeter_Gatling_Locust.md`](05_Herramientas/02_JMeter_Gatling_Locust.md) — Comparativa Sintáctica (14 KB)
**Contenido:** Mismo escenario implementado en JMeter, Gatling y Locust · Comparativa de estructura · Ejecución · Decision matrix detallada

**Ir aquí si necesitas:** Ver el mismo test en las 3 herramientas para comparar sintaxis directamente.

---

### [`03_Locust_Guia_Completa.md`](05_Herramientas/03_Locust_Guia_Completa.md) — EXHAUSTIVA (97 KB, 22 secciones)
**Secciones:**
1. Introducción y Filosofía
2. Instalación y Configuración
3. Arquitectura Interna (greenlets, gevent)
4. Fundamentos del Locustfile
5. User Classes en Profundidad
6. Tasks y Control de Flujo
7. HTTP Client y Validaciones
8. Wait Times y Pacing
9. **Custom Load Shapes** (ramp, step, spike, time-based)
10. **Modo Distribuido** (master/worker, Docker, K8s)
11. Event Hooks y Extensibilidad
12. **FastHttpUser** (5-6x más rendimiento)
13. **Protocolos No-HTTP** (gRPC, WebSocket, MQTT, custom)
14. Datos de Prueba y Parametrización
15. Métricas, Reportes y Exportación
16. Integración con CI/CD
17. Plugins y Ecosistema
18. Patrones Avanzados
19. Debugging y Troubleshooting
20. Comparativa con Otras Herramientas
21. Mejores Prácticas y Antipatrones
22. Proyecto de Referencia Completo

**Ir aquí si necesitas:** Cualquier aspecto de Locust en profundidad — desde hello world hasta distributed gRPC testing.

---

### [`04_Gatling_Community_Guia_Completa.md`](05_Herramientas/04_Gatling_Community_Guia_Completa.md) — EXHAUSTIVA (95 KB, 24 secciones)
**Secciones:**
1. Introducción y Filosofía
2. Arquitectura Interna (Akka, Netty NIO)
3. Instalación y Setup de Proyecto (Maven/Gradle)
4. **DSLs Disponibles** (Java, Kotlin, Scala)
5. Estructura de una Simulation
6. Scenarios y Estructura de Ejecución
7. HTTP Protocol Configuration
8. Requests y Actions
9. **Checks y Validaciones**
10. **Session API** y Estado del Virtual User
11. **Feeders** (CSV, JSON, JDBC, custom)
12. **Injection Profiles** (Open vs Closed Model)
13. Control de Flujo (Loops, Conditions, Errors)
14. Pause, Pacing y Think Time
15. **Assertions** (Criterios de Aceptación global)
16. Gatling Recorder
17. Reportes y Análisis (HTML reports)
18. Protocolos Adicionales (WebSocket, SSE, JMS)
19. Integración con CI/CD
20. Patrones Avanzados
21. Debugging y Troubleshooting
22. Community vs Enterprise Edition
23. Mejores Prácticas y Antipatrones
24. Proyecto de Referencia Completo

**Ir aquí si necesitas:** Cualquier aspecto de Gatling CE — desde setup con Maven hasta injection profiles avanzados.

---

### [`05_JMeter_Guia_Completa.md`](05_Herramientas/05_JMeter_Guia_Completa.md) — EXHAUSTIVA (69 KB, 25 secciones)
**Secciones:**
1. Introducción y Filosofía
2. Arquitectura Interna
3. Instalación y Configuración
4. Estructura del Test Plan
5. **Thread Groups** (Standard, Stepping, Ultimate, Arrivals)
6. **Samplers** (HTTP, JDBC, JMS, TCP, JSR223)
7. Config Elements (defaults, headers, cookies, cache)
8. Pre-Processors y Post-Processors
9. **Extractors y Correlation** (Regex, JSON, XPath, Boundary)
10. Assertions (Response, Duration, Size, JSON Schema)
11. **Timers** (Constant, Gaussian, Uniform, Poisson, Throughput)
12. **Logic Controllers** (If, While, Loop, ForEach, Transaction, Module)
13. Listeners (Reportes en tiempo real)
14. **Scripting JSR223 / Groovy** (no BeanShell!)
15. Parametrización y Data Driven Testing
16. **Testing Distribuido** (master/slave, RMI)
17. Ejecución en Modo CLI (Non-GUI) — SIEMPRE para tests reales
18. **Plugins Esenciales** (Custom Thread Groups, Throughput Shaping Timer, PerfMon)
19. Protocolos Avanzados (JDBC, JMS, SMTP)
20. Integración con CI/CD
21. HTML Dashboard Report
22. Patrones Avanzados
23. Troubleshooting y Performance Tuning del propio JMeter
24. Mejores Prácticas y Antipatrones
25. Proyecto de Referencia Completo

**Ir aquí si necesitas:** Cualquier aspecto de JMeter — desde thread groups hasta distributed testing y correlación dinámica.

---

### [`06_k6_Guia_Completa_Expandida.md`](05_Herramientas/06_k6_Guia_Completa_Expandida.md) — EXHAUSTIVA (73 KB, 24 secciones)
**Secciones:**
1. Introducción y Filosofía
2. **Arquitectura Interna** (Go engine, goja — NO es Node.js)
3. Instalación y Configuración
4. **Lifecycle** de un Script k6 (init, setup, VU code, teardown)
5. **Executors en Profundidad** (6 tipos: shared-iterations, per-vu-iterations, constant-vus, ramping-vus, constant-arrival-rate, ramping-arrival-rate)
6. **Scenarios** (Multi-scenario testing)
7. HTTP API Completa
8. Checks y Validaciones
9. **Thresholds** (Criterios Pass/Fail como SLOs)
10. **Métricas Built-in y Custom** (Counter, Gauge, Rate, Trend)
11. Datos de Prueba y Parametrización (SharedArray, open())
12. Grupos y Tags
13. Módulos y Organización de Código
14. **Protocolos Adicionales** (gRPC, WebSocket, Browser)
15. Environment Variables y Options
16. **Extensions (xk6)** — compilar extensiones custom en Go
17. Output y Exportación de Resultados
18. Integración con CI/CD
19. **Grafana Cloud** integration
20. Patrones Avanzados
21. Testing de Performance en Microservicios
22. Debugging y Troubleshooting
23. Mejores Prácticas y Antipatrones
24. Proyecto de Referencia Completo

**Ir aquí si necesitas:** Cualquier aspecto de k6 en profundidad — desde executors y scenarios hasta xk6 extensions y browser testing.

---

## 🔗 Relación con otras categorías

| Desde aquí puedo ir a... | Para... |
|--------------------------|---------|
| [02_Tipos_de_Pruebas](02_Tipos_de_Pruebas_de_Rendimiento.md) | Saber qué tipo de test implementar |
| [06_Workload](06_Workload_Modeling_y_Diseno_de_Escenarios.md) | Calcular el modelo de carga antes de scripting |
| [08_Scripts](08_Desarrollo_de_Scripts.md) | Patrones avanzados de scripting (agnósticos de herramienta) |
| [10_Mejores_Practicas](10_Mejores_Practicas_y_Errores_Comunes.md) | CI/CD pipelines con estas herramientas |
