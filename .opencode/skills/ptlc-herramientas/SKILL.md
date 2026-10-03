---
name: ptlc-herramientas
description: "Compara k6, JMeter, Gatling, Locust: guia y matriz"
---

# 05 — Herramientas de Performance Testing

> Índice intermedio. **Cuándo leer:** elegir herramienta, comparar opciones o saber qué guía consultar. Detalle en los documentos de esta skill (abajo).

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

### [`00b_Cheat_Sheet_Herramientas.md`](00b_Cheat_Sheet_Herramientas.md) — matriz de decisión y mapa tarea→sección (≤600 tokens)
- Para qué: obtener de un golpe la elección de herramienta y la sección+línea exacta a leer en cada guía.
- Consultar si: eliges herramienta o buscas executors, thresholds, correlación, feeders o CLI.

### [`00_Comunes_Guia_Herramientas.md`](00_Comunes_Guia_Herramientas.md) — CANÓNICA compartida (~24 KB)
- Para qué: versión única de las secciones que las 4 guías repetían.
- Consultar si: CI/CD (esqueleto GitHub Actions, Jenkins, quality gate) · troubleshooting (tabla de síntomas, logging, tuning) · mejores prácticas y antipatrones · proyecto de referencia (árboles, comandos Make, config)

### [`02_JMeter_Gatling_Locust.md`](02_JMeter_Gatling_Locust.md) — mismo test en 3 herramientas (14 KB)
- Para qué: comparar sintaxis del mismo escenario.
- Consultar si: JMeter · Gatling · Locust (estructura, ejecución, decision matrix)

### [`03_Locust_Guia_Completa.md`](03_Locust_Guia_Completa.md) — EXHAUSTIVA (84 KB, mapa de 20 secciones)
- Para qué: Locust en profundidad, de hello world a distributed gRPC.
- Consultar si: custom load shapes y FastHttpUser (5-6x rendimiento) · modo distribuido (master/worker, Docker, K8s) · protocolos no-HTTP (gRPC, WebSocket, MQTT)

### [`04_Gatling_Community_Guia_Completa.md`](04_Gatling_Community_Guia_Completa.md) — EXHAUSTIVA (84 KB, mapa de 22 secciones)
- Para qué: Gatling CE, del setup con Maven a injection profiles.
- Consultar si: DSLs (Java/Kotlin/Scala), Simulation, Session API y Feeders · injection profiles (open vs closed) y assertions · CE vs Enterprise Edition

### [`05_JMeter_Guia_Completa.md`](05_JMeter_Guia_Completa.md) — EXHAUSTIVA (65 KB, mapa de 23 secciones)
- Para qué: JMeter completo, de thread groups a distributed testing.
- Consultar si: Extractors y correlación (Regex, JSON, XPath, Boundary) · plugins esenciales y ejecución CLI non-GUI (siempre para tests reales) · scripting JSR223/Groovy (nunca BeanShell)

### [`06_k6_Guia_Completa_Expandida.md`](06_k6_Guia_Completa_Expandida.md) — EXHAUSTIVA (69 KB, mapa de 22 secciones)
- Para qué: k6 en profundidad: executors, scenarios, xk6 y browser.
- Consultar si: los 6 executors y thresholds como SLOs · extensiones xk6 compiladas en Go y browser testing · lifecycle del script, output y testing en microservicios

> Las 4 guías tienen un **mapa de secciones** al inicio (`grep -n "^## "`): pide solo el offset que necesites en lugar de leer el archivo entero. Sus secciones de CI/CD, troubleshooting, mejores prácticas y proyecto de referencia apuntan a [`00_Comunes_Guia_Herramientas.md`](00_Comunes_Guia_Herramientas.md).

---

## 🔗 Relación con otras categorías

| Desde aquí puedo ir a... | Para... |
|--------------------------|---------|
| [ptlc-tipos-de-pruebas](../ptlc-tipos-de-pruebas/SKILL.md) | Saber qué tipo de test implementar |
| [ptlc-workload-modeling](../ptlc-workload-modeling/SKILL.md) | Calcular el modelo de carga antes de scripting |
| [ptlc-scripting](../ptlc-scripting/SKILL.md) | Patrones avanzados de scripting (agnósticos de herramienta) |
| [ptlc-mejores-practicas](../ptlc-mejores-practicas/SKILL.md) | CI/CD pipelines con estas herramientas |