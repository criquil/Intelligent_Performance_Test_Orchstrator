# Documentación — Intelligent Performance Test Orchestrator

Base de conocimiento del Performance Test Life Cycle (PTLC) operada por Claude Code. Idioma primario: español.

## Índice de documentos

| Doc | Título | Propósito |
|-----|--------|-----------|
| [01](01-vision-general.md) | Visión general | Qué es el proyecto, objetivos, estado v3.0 y qué no es |
| [02](02-arquitectura.md) | Arquitectura | Estructura del repo, componentes y flujo de un request |
| [03](03-agente-orquestador.md) | Agente orquestador | Rol, phases y gates de `ptlc-orchestrator` |
| [04](04-pipeline-ptlc.md) | Pipeline PTLC | Detalle de las 6 fases F1–F6, estados y approval gate |
| [05](05-skills.md) | Catálogo de skills | Las 6 de pipeline, las 12 temáticas y el context envelope |
| [06](06-knowledge-base.md) | Knowledge base | Guías de herramientas, cheat sheets y lectura por sección |
| [07](07-optimizacion-tokens.md) | Optimización de tokens | Línea base, acciones, resultados y cómo medir |
| [08](08-gobernanza.md) | Gobernanza | Presupuestos, reglas de edición y checklist de cambios |

Fuentes primarias: [`CLAUDE.md`](../CLAUDE.md) · [`.claude/settings.json`](../.claude/settings.json) · [índice maestro de skills](../.claude/skills/README.md) · [agente orquestador](../.claude/agents/ptlc-orchestrator.md).

## Lectura recomendada

- **Usuario nuevo:** [01](01-vision-general.md) → [03](03-agente-orquestador.md) → [02](02-arquitectura.md). Objetivo: entender qué hace el orquestador y cómo pedir una prueba de performance.
- **Desarrollador de skills:** [02](02-arquitectura.md) → [índice maestro](../.claude/skills/README.md) → `SKILL.md` de su skill. Objetivo: respetar los 3 niveles de navegación y el naming `NN_Tema.md`.
- **Mantenedor:** [`CLAUDE.md`](../CLAUDE.md) → [02](02-arquitectura.md) → [mapa de arquitectura](../.claude/skills/ptlc-arquitectura-mapas/MAP.md). Objetivo: preservar el entry point único, los gates y el presupuesto de tokens (`scripts/measure_tokens.py --strict`).
