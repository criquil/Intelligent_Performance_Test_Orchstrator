# Cheat Sheet — Herramientas

**Elección rápida** (⭐ bajo → alto)
| Criterio | k6 | JMeter | Gatling | Locust |
|---|---|---|---|---|
| CI/CD nativo | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Scripts como código | ⭐⭐⭐ | ⭐ (XML) | ⭐⭐⭐ | ⭐⭐⭐ |
| Multi-protocolo | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ (custom) |
| Performance engine | ⭐⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐ |
| GUI / low-code | ⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
Detalle: [SKILL.md](SKILL.md#comparativa-rápida-de-herramientas)

**Una línea por herramienta**
- k6 — JS/goja: CI/CD, código-como-config, HTTP/gRPC/WS/browser; límite: multi-protocolo acotado, sin GUI.
- JMeter — Java/XML: multi-protocolo legacy (JDBC/JMS/FTP/LDAP/TCP/SMTP), GUI; límite: engine pesado.
- Gatling — Java/Kotlin/Scala: alta concurrencia JVM, DSL; límite: curva media-alta.
- Locust — Python/gevent: equipos Python, protocolos custom, prototyping; límite: rendimiento medio (usar FastHttpUser).
Detalle: [SKILL.md](SKILL.md#comparativa-rápida-de-herramientas)

Guías: [03 Locust](03_Locust_Guia_Completa.md) · [04 Gatling](04_Gatling_Community_Guia_Completa.md) · [05 JMeter](05_JMeter_Guia_Completa.md) · [06 k6](06_k6_Guia_Completa_Expandida.md)

**Tarea → sección (línea)**
| Tarea | Sección a leer (línea) |
|---|---|
| Executors | k6 §5 (L392) · JMeter §5 (L310) · Gatling §12 (L1303) · Locust §9 (L1032) |
| Thresholds | k6 §9 (L931) · JMeter §10 (L688) · Gatling §15 (L1689) · Locust §15 (L2023) |
| Correlación | k6 §7 (L708) · JMeter §9 (L595) · Gatling §10 (L1112) · Locust §7 (L759) |
| Feeders | k6 §11 (L1163) · JMeter §15 (L1071) · Gatling §11 (L1203) · Locust §14 (L1872) |
| CLI | k6 §3 (L179) · JMeter §17 (L1191) · Gatling §3 (L178) · Locust §2 (L81) |
Detalle: [00_Comunes_Guia_Herramientas.md](00_Comunes_Guia_Herramientas.md#mapa-de-secciones)
