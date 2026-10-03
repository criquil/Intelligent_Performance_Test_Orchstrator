---
name: ptlc-scripting
description: "Escribe scripts: correlacion, WebSocket, GraphQL"
---

# 08 — Desarrollo de Scripts de Performance

> Índice intermedio. **Cuándo leer:** patrones de scripting agnósticos de herramienta, datos y manejo de errores. Detalle en los documentos de esta skill (abajo).

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

### [`01_Scripting_Avanzado.md`](01_Scripting_Avanzado.md) — 7 patrones con código, datos, errores
- Para qué: implementar patrones de scripting con código real.
- Consultar si: necesitas correlación, WebSocket, GraphQL o token refresh · escalas test data (CSV, SharedArray, DB seeding, cleanup) · versionas scripts y defines el changelog

---

## 🔗 Relación con otras categorías

| Desde aquí puedo ir a... | Para... |
|--------------------------|---------|
| [ptlc-herramientas](../ptlc-herramientas/SKILL.md) | Implementación específica por herramienta |
| [ptlc-workload-modeling](../ptlc-workload-modeling/SKILL.md) | Modelo de carga que el script debe seguir |
| [ptlc-fases-del-ciclo](../ptlc-fases-del-ciclo/SKILL.md) | Fase 5 (Desarrollo de Scripts) |
| [ptlc-mejores-practicas](../ptlc-mejores-practicas/SKILL.md) | Anti-patrones a evitar |