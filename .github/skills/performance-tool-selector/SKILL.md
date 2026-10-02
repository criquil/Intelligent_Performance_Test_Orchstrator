---
name: performance-tool-selector
description: Usa esta skill cuando necesites elegir entre k6, JMeter, Gatling o Locust para un caso de performance testing. Aplica criterios de protocolo, complejidad, CI/CD, lenguaje del equipo y tipo de prueba.
---

# Performance Tool Selector

## Objetivo
Elegir la herramienta adecuada para un escenario de pruebas de rendimiento y justificar la decisión con criterios técnicos.

## Referencias
- [DOCs/05_Herramientas_de_Performance_Testing.md](../../../DOCs/05_Herramientas_de_Performance_Testing.md)
- [DOCs/02_Tipos_de_Pruebas_de_Rendimiento.md](../../../DOCs/02_Tipos_de_Pruebas_de_Rendimiento.md)
- [DOCs/06_Workload_Modeling_y_Diseno_de_Escenarios.md](../../../DOCs/06_Workload_Modeling_y_Diseno_de_Escenarios.md)

## Flujo
1. Identifica el objetivo principal: baseline, capacidad, estrés, soak o resiliencia.
2. Confirma protocolos y restricciones técnicas (HTTP, gRPC, WebSocket, JDBC, JMS, etc.).
3. Evalúa restricciones del equipo: lenguaje, curva de aprendizaje, integración CI/CD y operación.
4. Compara opciones con una matriz corta (pros, contras, riesgos).
5. Devuelve recomendación final y alternativa de respaldo.

## Salida Esperada
- Herramienta recomendada.
- Razones técnicas en bullets.
- Riesgos de implementación.
- Siguiente documento a leer en `DOCs/05_Herramientas/`.
