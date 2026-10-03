---
name: gatling-performance-workflow
description: Usa esta skill para diseñar y validar simulaciones de Gatling con DSL JVM, feeders, checks, assertions y perfiles de inyección open/closed.
---

# Gatling Performance Workflow

## Referencias
- [.opencode/skills/ptlc-herramientas/04_Gatling_Community_Guia_Completa.md](../ptlc-herramientas/04_Gatling_Community_Guia_Completa.md)

## Flujo
1. Define simulation y scenario alineados al journey real de usuario.
2. Configura `injection profile` (open o closed model).
3. Implementa `checks`, `feeders` y `assertions` como criterios de aceptación.
4. Ejecuta prueba y compara contra baseline previo.
5. Reporta desviaciones con hipótesis de causa.
