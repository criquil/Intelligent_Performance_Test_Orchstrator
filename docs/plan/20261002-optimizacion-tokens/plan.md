# Plan de Optimización de Consumo de Tokens — PTLC Knowledge Base

**plan_id:** `20261002-optimizacion-tokens`
**Fecha:** 2026-10-02
**Objetivo:** reducir el consumo de tokens innecesarios del repositorio (contexto siempre activo, cuerpos de agentes, lecturas obligatorias del pipeline) sin perder información autoritativa.
**Método:** medición determinista (`measure_tokens.py`, tokens ≈ chars/3.5) + auditoría de solapamiento y huérfanos.

---

## 1. Medición actual (línea base)

### 1.1 Contexto siempre activo (se paga en **cada** request)

| Componente | Tokens |
|---|---|
| `AGENTS.md` (raíz) | 2.054 |
| Descripciones de 26 skills (inyectadas en el system prompt) | 1.015 |
| Descripciones de 17 agentes | 509 |
| **Total por request** | **3.578** |

### 1.2 Cuerpos de agentes (se pagan al delegar)

| Agente | Tokens |
|---|---|
| `gem-orchestrator` | 7.434 |
| `gem-planner` | 6.042 |
| `ptlc-orchestrator` | 3.092 |
| resto (14 agentes) | 1.298 – 2.927 |
| **Total corpus de agentes** | **41.120** |

`gem-orchestrator` + `gem-planner` = 13.476 tokens (33% del corpus) y ~55% de su peso está en bloques de contrato (`agent_input_reference` YAML) que solo se necesitan al componer prompts.

### 1.3 Knowledge base

| Componente | Tokens | Archivos |
|---|---|---|
| Índices `SKILL.md` (Nivel 2) | 25.702 | 26 |
| Documentos de detalle (Nivel 3) | 205.916 | 35 |
| **Total KB** | **232.633 (~795 KB)** | 61 |

**5 documentos = 87.860 tokens (43% del detalle):**

| Documento | Tokens |
|---|---|
| `ptlc-herramientas/03_Locust_Guia_Completa.md` | 26.205 |
| `ptlc-herramientas/04_Gatling_Community_Guia_Completa.md` | 24.918 |
| `ptlc-herramientas/06_k6_Guia_Completa_Expandida.md` | 18.964 |
| `ptlc-herramientas/05_JMeter_Guia_Completa.md` | 17.773 |
| `ptlc-tipos-de-pruebas/07_Resiliency_Testing.md` | 16.410 |

### 1.4 Coste por ejecución completa del pipeline

Las listas `pre_execution` de las 6 skills de fase fuerzan **lecturas completas** de ~600–700 KB → **≈170–200k tokens por ciclo PTLC**, con re-lecturas cruzadas:

| Documento | Waves que lo leen |
|---|---|
| `01_Metricas_Exhaustivas.md` | diagnostics, procedure-plan, test-plan, analysis (4×) |
| `01_Recopilacion_de_Requisitos.md` | intake, diagnostics, test-plan (3×) |
| `01_Workload_Modeling_Exhaustivo.md` | diagnostics, procedure-plan, execution (3×) |
| `01_k6_Guia_Completa.md` / `06_k6` / `05_JMeter` / `04_Gatling` / `03_Locust` | execution (las 5 listadas, se resuelve por nota) |

`ptlc-procedure-plan` solo: **11 documentos / ~140 KB** obligatorios.

---

## 2. Diagnóstico

| # | Hallazgo | Evidencia |
|---|---|---|
| D1 | **8 de 26 skills no aportan contenido**: `performance-*` y `{tool}-performance-workflow` son stubs de 16–27 líneas que solo reformulan un `## Flujo` y remiten al `ptlc-*` equivalente. Pagan descripción en cada request y crear ambigüedad de carga (posible doble carga de la misma guía). | Auditoría §1 |
| D2 | **Solapamiento semántico, no textual**: Jaccard ≥0.30 = **0 pares**. Los 4 tipos de prueba, plan de pruebas, reporte final, Apdex y Little's Law están repetidos en 2–4 documentos con redacción distinta. Un dedupe textual no lo detecta. | Medición + auditoría §4 |
| D3 | **Guías de herramientas con secciones comunes repetidas** en las 4 guías (CI/CD, troubleshooting, mejores prácticas/antipatrones, proyecto de referencia) y duplicación total `01_k6` ↔ `06_k6`. | Auditoría §4 |
| D4 | **Índices Nivel 2 demasiado pesados**: los `SKILL.md` de las 12 skills de conocimiento promedian ~1.650 tokens porque re-describen los temas de cada documento (`**Temas:** a · b · c…`) que luego se vuelven a leer al abrir el documento. | Medición |
| D5 | **Contratos de payload incrustados** en `gem-orchestrator` (7.4k) y `gem-planner` (6.0k): ~50% del cuerpo es YAML de esquemas que solo se usa al delegar. | Lectura de ambos agentes |
| D6 | **Redundancia de mapas**: 4 documentos de arquitectura (`MAP.md`, `MAPA_AGENTES_SKILLS.md`, `MAPA_FUNCIONAL_SIMPLIFICADO.md`, `MAPA_FUNCIONAL_PROCESO.md`) describen el mismo pipeline; el último se autodeclara histórico v1.0. | Auditoría §4 |
| D7 | **Enlaces muertos** tras la migración: `ptlc-herramientas/SKILL.md → 05_Herramientas/`, `ptlc-tipos-de-pruebas/SKILL.md → 02_Tipos_de_Pruebas/` y etiquetas legacy `02_Tipos_de_Pruebas`, `03_Fases`, `04_Metricas`, `06_Workload`. | Auditoría §2 |
| D8 | `07_Resiliency_Testing.md` (16.4k) es 3–4× sus hermanos (3.5–5.9k) por asimetría de detalle. | Medición |

---

## 3. Plan de optimización

Principio rector: **el índice decide, el documento se lee solo cuando hace falta**. Nunca se pierde contenido: lo que se elimina es *copia*, y lo que se divide queda referenciado.

### Wave 1 — Recortes de bajo riesgo (ahorro por request y por delegación)

| Task | Acción | Ahorro |
|---|---|---|
| **T1** | adelgazar `AGENTS.md`: mover las 3 tablas (12 skills temáticas, 6 de pipeline, 8 operativas) a `.opencode/skills/README.md`; dejar solo reglas, entry point, comandos y 5 rutas clave. 2.054 → ~600 tokens | **-1.450** por request |
| **T2** | comprimir las 26 descripciones de skill a `nombre + 3-5 triggers` (≤15 tokens c/u), sin prosa explicativa | **-600** por request |
| **T3** | eliminar las 8 skills stub (D1) y actualizar sus referencias en agentes, skills de fase y README; la cobertura ya existe en `ptlc-*` | **-350** por request + fin de doble carga |
| **T4** | extraer `agent_input_reference` de `gem-orchestrator` a `.opencode/skills/gem-orchestrator-contracts/SKILL.md` (carga bajo demanda). 7.434 → ~3.100 | **-4.300** por delegación |

### Wave 2 — Cuerpos de agentes e índices

| Task | Acción | Ahorro |
|---|---|---|
| **T5** | adelgazar `gem-planner` (6.042) y `ptlc-orchestrator` (3.092): esquemas de payload → referencias bajo demanda; `ptlc-orchestrator` repite el mismo YAML de contexto en las 6 fases | **-4.500** por delegación |
| **T6** | comprimir los 12 `SKILL.md` de conocimiento: sustituir `**Temas:** a · b · c` por una línea de alcance por documento (D4). ~19.800 → ~7.000 | **-12.800** por lectura de índice |

### Wave 3 — Consolidación del knowledge base

| Task | Acción | Ahorro |
|---|---|---|
| **T7** | extraer de las 4 guías de herramientas las secciones repetidas a un único `ptlc-herramientas/00_Comunes_Guia_Herramientas.md` (CI/CD, troubleshooting, mejores prácticas, proyecto de referencia) y borrarlas de las guías | **-18.000** en KB |
| **T8** | dividir cada guía por tema (p. ej. `06_k6/01_executors.md`, `02_scenarios.md`, `03_thresholds.md`) para carga parcial; fusionar `01_k6_Guia_Completa.md` en `06_...Expandida.md` (D3) | **-4.100** y habilita lectura parcial |
| **T9** | dividir `07_Resiliency_Testing.md` en 3 documentos alineados con sus hermanos (D8) | **-11.000** en KB |
| **T10** | consolidar los 4 mapas de arquitectura en 1 y eliminar `MAPA_FUNCIONAL_PROCESO.md` (histórico v1.0) (D6) | **-6.500** |

### Wave 4 — Pipeline de lectura (el mayor palanca)

| Task | Acción | Ahorro |
|---|---|---|
| **T11** | sustituir lecturas completas por **lecturas por sección**: cada skill de fase recibe un índice con anclas/offset de las secciones que realmente necesita, y las listas `pre_execution` pasan a referenciar sección, no archivo | **-120.000** por ciclo |
| **T12** | eliminar re-lecturas entre waves: el orquestador mantiene un `context_envelope` con lo ya sintetizado (métricas, requisitos, workload model) y las waves 2–6 lo reutilizan en vez de releer los 3 documentos más repetidos | **-25.000** por ciclo |
| **T13** | "cheat sheets" por skill (1–2 KB): fórmulas y umbrales operativos en un archivo corto; las guías largas quedan para casos no covered (API, DSL, sintaxis) | **-40.000** en ejecuciones típicas |

### Wave 5 — Gobernanza del presupuesto

| Task | Acción |
|---|---|
| **T14** | versionar `measure_tokens.py` como `scripts/measure_tokens.py` y fijar presupuestos: contexto siempre activo ≤1.400 tokens, cuerpo de agente ≤3.200, ninguna lectura obligatoria >2.000 tokens |
| **T15** | reglas explícitas en `AGENTS.md`: "nunca leer un documento completo si el índice resuelve la duda", "preferir sección/grep", "reutilizar contexto acumulado", "no releer documentos ya sintetizados en el envelope" |
| **T16** | limpiar enlaces muertos y etiquetas legacy (D7) |

---

## 4. Impacto esperado

| Métrica | Actual | Objetivo | Reducción |
|---|---|---|---|
| Contexto por request | 3.578 | ~1.400 | **-61%** |
| Skills anunciadas | 26 (8 stubs) | 18 | -8 |
| `gem-orchestrator` (delegación) | 7.434 | ~3.100 | **-58%** |
| Corpus de agentes | 41.120 | ~30.000 | -27% |
| Índices Nivel 2 | 25.702 | ~13.000 | **-49%** |
| KB total | 232.633 | ~185.000 | -20% |
| Lecturas por ciclo PTLC | ~180.000 | ~60.000 | **-65%** |

## 5. Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Perder información al dividir/eliminar duplicados | Cada archivo eliminado o fusionado se reemplaza por un enlace/redirección en el índice temático; verificar con el medidor + grep de enlaces rotos |
| Índices que ya no bastan para resolver la duda | Regla T15 + cheat sheets: el índice dice *qué sección* leer, nunca solo *qué archivo* |
| Habilitar lecturas parciales empeora la fiabilidad | Anclar por heading estable (`## 5. Thread Groups`) y verificar con `grep -n "^## "` en el checklist |
| Sobre-condensar descripciones degrada el descubrimiento | Mantener keywords de dominio exactas (k6, JMeter, p95, Little's Law) en las descripciones |

## 6. Orden de ejecución

1. Wave 1 — sin contenido afectado, ahorro inmediato por request (medible en el siguiente turno).
2. Wave 2 — recorte de agentes.
3. Wave 3 — consolidación de KB (mayor diff, requiere validación de enlaces).
4. Wave 4 — pipeline de lectura (mayor ahorro, validar con un ciclo real de extremo a extremo).
5. Wave 5 — gobernanza y limpieza.