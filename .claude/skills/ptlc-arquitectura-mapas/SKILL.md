---
name: ptlc-arquitectura-mapas
description: "Mapea PTLC: pipeline, agentes, skills, convenciones"
---

# ptlc-arquitectura-mapas — Mapas y convenciones del repositorio

> Mapa único de la arquitectura del repo y convenciones del knowledge base. **Cuándo leer:** ver la estructura del sistema, el flujo agentes ↔ skills o las reglas del knowledge base.

## 📂 Contenido

| Archivo | Para qué |
|---------|----------|
| [CONVENTIONS.md](CONVENTIONS.md) | Convenciones del repo: navegación, organización, agentes, entregables |
| [MAP.md](MAP.md) | **Mapa único**: arquitectura, pipeline 6-wave, tabla de fases (lecturas/entradas/salidas), guías por agente, principios y decisiones críticas, selección de herramienta, cobertura del knowledge base por fase, estructura de archivos, navegación en 3 niveles, entregables y tiempos por fase |

## 🗺️ Secciones de MAP.md

| # | Sección | Para qué |
|---|---------|----------|
| 1 | [Arquitectura general](MAP.md#1-arquitectura-general) | Diagrama raíz: repo, skills, agentes |
| 2 | [Pipeline v3.0](MAP.md#2-pipeline-v30-ptlc-orchestrator-como-entry-point-obligatorio) | Flujo `ptlc-orchestrator` → 6 waves; los no-PTLC se resuelven con subagentes integrados (`general-purpose`/`Explore`) o el knowledge base |
| 3 | [Fases del pipeline](MAP.md#3-fases-del-pipeline-lecturas-procesos-y-salidas) | Tabla entradas → lecturas → proceso → salida por wave, incluido el approval gate |
| 4 | [Guías por agente](MAP.md#4-guías-por-agente) | Qué `SKILL.md` debe leer cada skill de fase |
| 5 | [Principios y decisiones](MAP.md#5-principios-de-arquitectura-y-decisiones-críticas) | Principios v3.0 y decisiones de diseño (tool única, on-demand, paths, idioma) |
| 6 | [Selección de herramienta](MAP.md#6-selección-de-herramienta-de-prueba) | Árbol de decisión protocolo → herramienta |
| 7 | [Cobertura del knowledge base](MAP.md#7-cobertura-del-knowledge-base-por-fase) | Qué documentos lee cada fase |
| 8 | [Estructura de archivos](MAP.md#8-estructura-de-archivos) | Árbol de directorios y carpetas clave |
| 9 | [Navegación 3 niveles](MAP.md#9-modelo-de-navegación-3-niveles) | README → SKILL.md → documentoNN |
| 10 | [Entregables y artefactos](MAP.md#10-entregables-y-artefactos-por-ciclo) | Qué genera cada wave en disco |
| 11 | [Tiempos por fase](MAP.md#11-tiempos-estimados-por-fase) | Duración estimada de cada wave |

> Los tres mapas previos (agentes ↔ skills, funcional simplificado y funcional v1.0) se consolidaron en `MAP.md` y se eliminaron. El histórico v1.0 (JMeter + Simpsons API, CLI) no se conservó por carecer de valor operativo en v3.0.

## 🔗 Relación con otras skills

| Desde aquí puedo ir a... | Para... |
|--------------------------|---------|
| `ptlc-roadmap-decisiones` | Consultar ADRs, roadmap y decisiones de arquitectura |
| `ptlc-fases-del-ciclo` | Profundizar en las fases del ciclo |
| Guías operativas de herramientas en `ptlc-herramientas/` | Consultar los flujos de scripting y ejecución por herramienta |