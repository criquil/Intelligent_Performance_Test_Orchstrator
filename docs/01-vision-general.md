# 01 — Visión general

## Qué es

**Intelligent Performance Test Orchestrator v3** es una base de conocimiento del Performance Test Life Cycle (PTLC) operada por Claude Code. Un único agente, `ptlc-orchestrator`, recibe todo request, detecta el dominio y orquesta el ciclo completo de performance testing cargando una skill por fase. Ver [03](03-agente-orquestador.md) y el [índice maestro](../.claude/skills/README.md).

## Objetivos

- Conducir el PTLC de extremo a extremo: requisitos → diagnóstico → procedimiento → plan formal → ejecución → análisis.
- Centralizar el conocimiento (estándares ISTQB/IEEE-829, ISO 25010, workload modeling, RCA) como skills navegables en 3 niveles.
- Generar entregables trazables por ciclo: plan activo, plan formal, scripts y reporte con veredicto.
- Mantener el contexto barato: cheat sheets primero, envelope acumulado, presupuestos de tokens.

## Para quién es

| Perfil | Uso |
|--------|-----|
| Equipos que prueban APIs/servicios | Piden pruebas en lenguaje natural; el orquestador guía el ciclo |
| Performance engineers | Consultan el knowledge base (tipos de prueba, métricas, scripting, RCA) |
| Desarrolladores de skills | Amplían el knowledge base siguiendo las convenciones de `CLAUDE.md` / `CONVENTIONS.md` |

## Estado actual (v3.0)

Existe y es funcional:

- **1 agente:** `ptlc-orchestrator` (entry point obligatorio declarado en `CLAUDE.md` y definido como subagente). Ver [definición](../.claude/agents/ptlc-orchestrator.md).
- **18 skills:** 6 del pipeline (`ptlc-intake`, `ptlc-diagnostics`, `ptlc-procedure-plan`, `ptlc-test-plan`, `ptlc-execution`, `ptlc-analysis`) + 12 temáticas de conocimiento.
- **Knowledge base:** ~650 KB y 48 documentos bajo `.claude/skills/` (reemplaza la antigua carpeta `DOCs/`).
- **Guías operativas:** k6, JMeter, Gatling y Locust en `ptlc-herramientas/` + matriz de decisión.
- **Gobernanza:** `CLAUDE.md`, mapa de arquitectura (`ptlc-arquitectura-mapas/MAP.md`), PRD (`ptlc-roadmap-decisiones/PRD.yaml`), medición con `scripts/measure_tokens.py`.

## Qué NO es

- **No hay código de aplicación.** El repo no contiene una app que compilar o desplegar; no existe pipeline de build/test/lint.
- **Los scripts de prueba se generan on-demand** en la fase 5 (`ptlc-execution`), una herramienta por ciclo; no hay scripts pre-creados.
- **No ejecuta sin aprobación explícita.** La ejecución real requiere confirmación del usuario (approval gate).

## Componentes

| Componente | Ruta | Responsabilidad |
|------------|------|-----------------|
| Memoria del proyecto | `CLAUDE.md` | Reglas persistentes (entry point, niveles, tokens) |
| Configuración | `.claude/settings.json` | Permisos y configuración de Claude Code |
| Agente | `.claude/agents/ptlc-orchestrator.md` | Orquestación pura del ciclo |
| Skills pipeline (6) | `.claude/skills/ptlc-{intake,…,analysis}/` | Procedimiento de cada fase |
| Skills conocimiento (12) | `.claude/skills/ptlc-{fundamentos,…,roadmap-decisiones}/` | Knowledge base temática |
| Índice maestro | `.claude/skills/README.md` | Punto de entrada del knowledge base |
| Mapa arquitectura | `.claude/skills/ptlc-arquitectura-mapas/MAP.md` | Diagramas y decisiones críticas |
| Medición tokens | `scripts/measure_tokens.py` | Valida presupuestos (`--strict`) |
| Entregables | `docs/plan/{plan_id}/`, `docs/*.md`, `tests/performance/{tool}/` | Estado, planes, scripts y reportes por ciclo |

Siguiente: [02 Arquitectura](02-arquitectura.md) · [03 Agente orquestador](03-agente-orquestador.md).
