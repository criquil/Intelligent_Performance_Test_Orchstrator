---
name: ptlc-herramientas
description: "Compara k6, JMeter, Gatling, Locust: guia y matriz"
---

# 05 — Herramientas de Performance Testing

> Índice intermedio. **Cuándo leer:** elegir herramienta o navegación rápida. Usa [`00b_Cheat_Sheet_Herramientas.md`](00b_Cheat_Sheet_Herramientas.md) para decisión rápida y acceso directo a todas las secciones comunes.

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

### [`00b_Cheat_Sheet_Herramientas.md`](00b_Cheat_Sheet_Herramientas.md) — matriz de decisión y referencia única (~1.5 KB)
- Para qué: elección rápida de herramienta + acceso directo a todas las secciones comunes.
- Consultar si: eliges herramienta o buscas executors, thresholds, correlación, feeders, CI/CD, troubleshooting.

> **Nota:** Esta skill ahora contiene solo la referencia central. Toda información detallada sobre k6, JMeter, Gatling y Locust está en las guías oficiales del ecosistema. Usa este cheat sheet para navegación rápida y decisión de herramienta.

---

## 🔗 Relación con otras categorías

| Desde aquí puedo ir a... | Para... |
|--------------------------|---------|
| [ptlc-tipos-de-pruebas](../ptlc-tipos-de-pruebas/SKILL.md) | Saber qué tipo de test implementar |
| [ptlc-workload-modeling](../ptlc-workload-modeling/SKILL.md) | Calcular el modelo de carga antes de scripting |
| [ptlc-scripting](../ptlc-scripting/SKILL.md) | Patrones avanzados de scripting (agnósticos de herramienta) |
| [ptlc-mejores-practicas](../ptlc-mejores-practicas/SKILL.md) | CI/CD pipelines con estas herramientas |
