---
name: ptlc-scripting
description: "Desarrollo de scripts de prueba avanzado: correlacion, refresh de tokens, manejo de datos, WebSocket, GraphQL y patronces de error handling."
---

# 08 — Desarrollo de Scripts de Performance

> **Rol de este archivo:** Índice intermedio. Resume patrones de scripting avanzados y dirige al documento con implementaciones completas.  
> **Cuándo leer este archivo:** Cuando necesitas patrones de scripting agnósticos de herramienta, estrategias de datos, o manejo de errores.  
> **Carpeta detallada:** [`.`](08_Desarrollo_de_Scripts/)

---

## Patrones de Scripting — Resumen

| Patrón | Descripción | Caso de uso |
|--------|-------------|-------------|
| **Chain Requests** | Requests secuenciales donde el output de uno es input del siguiente | Login → Get token → Use token en API calls |
| **Token Refresh** | Renovar token automáticamente cuando expira | APIs con OAuth2/JWT de corta duración |
| **Correlation** | Extraer valores dinámicos de responses para usarlos después | Session IDs, CSRF tokens, viewstate |
| **Parameterization** | Usar datos externos (CSV, JSON, DB) | Diferentes users/products por VU |
| **WebSocket** | Conexiones persistentes bidireccionales | Chat, real-time feeds, notificaciones |
| **GraphQL** | Queries/mutations con cuerpo variable | APIs GraphQL con diferentes operations |
| **Error Handling** | Manejo graceful de errores sin abortar el test | Retry logic, circuit breaker en script |

### Principios de Scripting

```
1. REALISMO    → Simular comportamiento real del usuario (think time, navigation path)
2. ROBUSTEZ    → Manejar errores sin abortar (try/catch, validation, fallbacks)
3. REUTILIZACIÓN → Modularizar (funciones, módulos, page objects)
4. MANTENIBILIDAD → Versionado, changelog, documentación inline
5. EFICIENCIA  → No desperdiciar recursos del load generator (lazy loading, shared data)
```

---

## 📂 Contenido de la Subcarpeta

### [`01_Scripting_Avanzado.md`](01_Scripting_Avanzado.md)
**Contenido completo (~13 KB):**

| Sección | Qué encontrarás |
|---------|-----------------|
| Patrones de Scripting Avanzados | 7 patrones con código completo (chain, token, WS, GraphQL, correlation, conditional, parallel) |
| Data Management Strategies | CSV loading, SharedArray, database seeding, data cleanup |
| Error Handling Best Practices | Retry patterns, graceful degradation, error categorization |
| Script Maintenance | Versionado semántico, changelog template, code review checklist |

**Ir aquí si necesitas:**
- Implementar un patrón específico con código ejemplo
- Estrategia para manejar test data a escala
- Cómo hacer retry inteligente sin contaminar resultados
- Mantener scripts a lo largo del tiempo (versionado, docs)

---

## 🔗 Relación con otras categorías

| Desde aquí puedo ir a... | Para... |
|--------------------------|---------|
| [05_Herramientas](../ptlc-herramientas/SKILL.md) | Implementación específica por herramienta |
| [06_Workload](../ptlc-workload-modeling/SKILL.md) | Modelo de carga que el script debe seguir |
| [03_Fases](../ptlc-fases-del-ciclo/SKILL.md) | Fase 5 (Desarrollo de Scripts) |
| [10_Mejores_Practicas](../ptlc-mejores-practicas/SKILL.md) | Anti-patrones a evitar |
