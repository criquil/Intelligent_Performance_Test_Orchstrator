# ADR-001: Evolución de Orquestrador - v1.0 vs v2.0

## Status
**SUPERSEDED** (v1.0 — GitHub Copilot CLI) | **IMPLEMENTED** (v2.0 — gem-orchestrator, 2026-06-17)

## Context

El framework PTLC ha sido ejecutado en v1.0 usando **GitHub Copilot CLI como orquestrador único**. Para versiones futuras que requieran mayor escala, rigor y paralelismo, se propone migrar a **gem-orchestrator (Gem-Team)**.

### Decisión v1.0 (Actual)
```
Orquestrador: GitHub Copilot CLI (directo)
├─ Eficiente para scope simple (1 endpoint, 1 tool)
├─ Velocidad: Rápido (no overhead de coordinación)
├─ Quality: Buena (manual review integrado)
└─ Escalabilidad: Limitada (lineal, single-threaded)
```

### Decisión Propuesta v2.0
```
Orquestrador: gem-orchestrator
├─ Escalable para scope complejo (multi-endpoint, multi-tool)
├─ Velocidad: Más lento por overhead, pero paralelismo compensa
├─ Quality: Excelente (multi-stage review)
└─ Escalabilidad: Alta (paralelo, multi-agente)
```

---

## Decision

**USAR GEM-ORCHESTRATOR EN v2.0** como orquestador central para coordinar:
- gem-planner (descomposición de tareas)
- gem-researcher (investigación PTLC)
- gem-implementer (implementación multi-tool)
- gem-reviewer (quality gates multi-stage)
- gem-documentation-writer (reportes automáticos)

**MANTENER CLI EN v1.0** por eficiencia (sin cambios retroactivos).

---

## Rationale

### Por qué v1.0 fue correcto con CLI directo

```
Criterios de decisión       | Evaluación
────────────────────────────|──────────────
Scope simple                | ✅ Sí (1 endpoint)
Herramienta directa         | ✅ Sí (JMeter)
Skill especializada         | ✅ Sí (jmeter-workflow)
Velocidad crítica           | ✅ Sí
Necesidad de paralelismo    | ❌ No
Necesidad de review múltiple | ❌ No
Complejidad arquitectónica  | ❌ Baja (simple)
Escalabilidad futura        | ⚠️ No (limitada)
```

**RESULTADO**: CLI directo fue pragmático y eficiente para v1.0.

### Por qué v2.0 necesita Gem-Orchestrator

```
v2.0 Requirements           | Solución
────────────────────────────|──────────────────
Multi-tool support         | gem-implementer × N
Parallelismo needed        | gem-orchestrator DAG
Comparative analysis       | gem-implementer task
Advanced RCA               | gem-implementer + researcher
Multi-stage review         | gem-reviewer
Auto-documentation         | gem-documentation-writer
Historical tracking        | gem-planner task
Complexity increase        | Requiere coordinación
```

**RESULTADO**: Gem-orchestrator necesario para v2.0+ complexity.

---

## Implications

### Para v1.0 (Sin cambios)
```
✅ Mantener CLI direct approach
✅ Mantener jmeter-performance-workflow skill
✅ Mantener estructura actual (sin refactor)
⚠️ Documentar decisión para v2.0
```

### Para v2.0 (Roadmap)
```
🔄 Refactor architecture → gem-orchestrator
📋 Crear task decomposition DAG
👥 Activar todos los gem-agents
🛠️ Agregar multi-tool support (k6, Locust)
📊 Implementar comparative analysis
✅ Multi-stage review gates
```

### Esfuerzo Estimado

```
Componente              | v1.0 | v2.0 (Estimado)
────────────────────────|────  |─────────────────
CLI orchestration       | ✅ Done | Refactor: 4h
Gem-orchestrator setup  | N/A  | 2h
Task decomposition      | N/A  | 4h
Multi-tool impl (k6)    | N/A  | 8h
Multi-tool impl (Locust)| N/A  | 8h
RCA v2.0                | ✅ Done | Enhance: 6h
Review gates            | N/A  | 4h
Documentation gen       | N/A  | 4h
Testing & QA            | N/A  | 8h
────────────────────────|──────|─────────────────
TOTAL                   | ~30h | ~48h (v2.0)
```

---

## Alternatives Considered

### 1. Mantener CLI directo también en v2.0
```
Pros:
  + Velocidad (sin overhead)
  + Simplicidad (sin refactor)
  
Cons:
  - No escalable
  - No paralelismo
  - Review manual
  - Documentación manual
  
REJECTED: Limita v2.0 capabilities
```

### 2. Usar ptlc-orchestrator en lugar de gem-orchestrator
```
Pros:
  + Específico para PTLC
  + Conocimiento de domain
  
Cons:
  - No disponible (custom skill)
  - Requeriría construcción propia
  - Gem-team es más general y robusto
  
REJECTED: Mejor usar gem-team existing
```

### 3. Usar solo gem-implementer sin orchestrator
```
Pros:
  + Menos overhead
  
Cons:
  - Sin coordinación central
  - Sin task dependencies
  - Sin review gates
  - No paralelismo controlado
  
REJECTED: Necesita orquestación
```

---

## Concerns & Mitigation

### Concern 1: "v2.0 será más lento"
```
RISK: Overhead de coordinación gem-orchestrator

MITIGATION:
  ├─ Overhead esperado: +10-15%
  ├─ Compesado por paralelismo: -30% aprox
  ├─ Net result: -15-20% faster overall
  └─ Benchmark: Run time tests en v2.0
```

### Concern 2: "gem-team no es especializado en PTLC"
```
RISK: Falta de contexto PTLC en agentes

MITIGATION:
  ├─ Proporcionar Knowledge Base PTLC a cada agente
  ├─ Crear task descriptions con contexto
  ├─ Implementar skills PTLC especializadas
  └─ Review manual de arquitectura
```

### Concern 3: "Complejidad aumentará mucho"
```
RISK: Mayor complejidad en código

MITIGATION:
  ├─ Usar DAG-based task decomposition
  ├─ Documentar cada etapa
  ├─ Mantener scripts simples por tool
  ├─ Crear ejemplos de uso
  └─ Training en DAG patterns
```

---

## Acceptance Criteria

### v1.0 (Already Met ✅)
```
✅ Baseline reproducible
✅ RCA integrado
✅ Documentación clara
✅ Health Score 98/100
✅ Production-ready para 1 tool
```

### v2.0 (To Be Met)
```
[ ] Gem-orchestrator integrado
[ ] Support para JMeter + k6 + Locust
[ ] Comparative analysis working
[ ] Multi-stage review gates
[ ] Auto-documentation generation
[ ] Trend analysis functional
[ ] CI/CD fully integrated
[ ] Test coverage >80%
[ ] Performance regression <5%
[ ] Documentation complete
```

---

## Timeline

### v1.0 (Actual)
```
Status: COMPLETE ✅
Duration: 1 day
Release: 2026-06-11
```

### v1.1 (Quick Enhancement)
```
Status: PLANNED
Duration: 1-2 weeks
Scope:
  ├─ Add k6 support (basic)
  ├─ Improve RCA comparatives
  └─ Documentation updates
Release: 2026-06-25 (target)
```

### v2.0 (Major Refactor)
```
Status: PROPOSED
Duration: 4-6 weeks
Scope:
  ├─ Migrate to gem-orchestrator
  ├─ Full multi-tool support
  ├─ Advanced RCA
  └─ CI/CD integration
Release: 2026-07-15 (target)
```

### v2.1 (Polish)
```
Status: PROPOSED
Duration: 2-3 weeks
Scope:
  ├─ Prometheus integration
  ├─ Grafana dashboards
  ├─ Advanced trends
  └─ Automated recommendations
Release: 2026-08-01 (target)
```

---

## Related Records

- [MAPA_FUNCIONAL_PROCESO.md](./MAPA_FUNCIONAL_PROCESO.md) - v1.0 architecture
- [MAPA_AGENTES_SKILLS.md](./MAPA_AGENTES_SKILLS.md) - CLI orchestration detail
- [FRAMEWORK_v2_0_ROADMAP.md](FRAMEWORK_v2_0_ROADMAP.md) - Detailed v2.0 roadmap

---

## Sign-Off

| Role | Decision | Date | Notes |
|------|----------|------|-------|
| Implementation | CLI OK for v1.0 ✅ | 2026-06-11 | Pragmatic choice |
| Architecture | Gem-team for v2.0 ✅ | 2026-06-11 | Recommended |
| Product | Approved | Pending | Pending sign-off |

---

## Comments

### Rationale Summary
```
v1.0: "Perfect is the enemy of good"
      └─ CLI directo fue excelente para MVP
      └─ Baseline establecido, RCA integrado, ready

v2.0: "Scalability requires orchestration"
      └─ Gem-team para multi-tool + paralelismo
      └─ Advanced RCA + comparative analysis
      └─ Enterprise-grade quality gates
```

**Decisión: Pragmática para v1.0, pero escalable a v2.0 con Gem-Team.** ✅
