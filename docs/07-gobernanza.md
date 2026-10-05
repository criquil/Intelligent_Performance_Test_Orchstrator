# 08 · Gobernanza del repositorio

Reglas de mantenimiento del knowledge base PTLC. Documento normativo; el histórico está en [07-optimizacion-tokens](07-optimizacion-tokens.md).

## 1. Presupuesto de tokens vigente

Validado por `python scripts/measure_tokens.py --strict` (ver `../scripts/measure_tokens.py`):

| Ámbito | Límite |
|---|---|
| Contexto activo por request | ≤ **1.500** tokens |
| Cuerpo de agente (`ptlc-orchestrator.md`) | ≤ **3.200** tokens |
| Índice de skill (`SKILL.md`) | ≤ **2.000** tokens |
| Documento de detalle | ≤ **23.000** tokens |
| Ninguna lectura obligatoria (`<pre_execution>`) | > **2.000** tokens sin sección/línea |

Nota: los detalles grandes se leen **por sección** (mapa de secciones); el límite de archivo solo evita crecimiento descontrolado.

## 2. Las 4 reglas

1. **Índice antes que documento.** Dudas → `SKILL.md`/índice; detalle → `grep -n "^## "` + `read` por `offset/limit`. Nunca leer completo un doc > 2.000 tokens.
2. **Cheat sheets primero.** Fórmulas y umbrales en las 3 cheat sheets bajo `../.claude/skills/` (`ptlc-metricas-kpis`, `ptlc-workload-modeling`, `ptlc-herramientas`); el doc completo solo para API/sintaxis/ejemplos.
3. **Envelope acumulado.** Cada fase persiste su bloque en `plan/{plan_id}/context_envelope.json`; las siguientes lo cargan y no releen lo sintetizado.
4. **Medición continua.** Todo cambio que toque skills, agentes o `CLAUDE.md` se verifica con `--strict` antes de darlo por cerrado.

## 3. Convenciones de edición

- Niveles: `../.claude/skills/README.md` (Nivel 1) → `SKILL.md` (Nivel 2) → `NN_Tema.md` (Nivel 3, naming con prefijo `NN_`).
- **No duplicar**: actualizar el documento existente en lugar de crear otro.
- Al mover o renombrar: actualizar referencias en `README.md` y el `SKILL.md` padre.
- Leer el Nivel 2 antes de editar un Nivel 3.
- **Español** en documentación, output y navegación.

## 4. Checklist para skill o documento nuevo

1. ¿Cabe en un doc existente? Si sí, no crear archivo.
2. Ubicarlo en la skill correcta con naming `NN_Tema.md`.
3. Registrarlo en el `SKILL.md` padre y en `../.claude/skills/README.md` (descubrible).
4. Frontmatter `description` corto (el contexto activo lo paga cada request).
5. Si el doc > 2.000 tokens: añadir mapa de secciones y acotar `<pre_execution>` por sección/línea.
6. Verificar enlaces relativos en disco.
7. Pasar `python scripts/measure_tokens.py --strict` (cero violaciones).
