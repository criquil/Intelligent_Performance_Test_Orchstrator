# 01 — Introducción al Performance Test Life Cycle (PTLC)

> **Rol de este archivo:** Índice intermedio. Resume el contexto general del PTLC y dirige a la documentación detallada en la subcarpeta.  
> **Cuándo leer este archivo:** Cuando necesitas entender qué es el PTLC, quién lo ejecuta, o bajo qué estándares opera.  
> **Carpeta detallada:** [`01_Introduccion_PTLC/`](01_Introduccion_PTLC/)

---

## Resumen Ejecutivo

El **Performance Test Life Cycle (PTLC)** es una metodología estructurada de 9 fases para planificar, diseñar, ejecutar y gestionar pruebas de rendimiento. Su objetivo es garantizar que los sistemas cumplan criterios de velocidad, escalabilidad y estabilidad antes de llegar a producción.

### Las 9 Fases del PTLC

```
1. Recopilación de Requisitos    →  Entender NFRs y arquitectura
2. Planificación                  →  Estrategia, alcance, herramientas
3. Diseño de Pruebas             →  Casos de prueba y modelos de carga
4. Configuración del Entorno     →  Infraestructura y monitoreo
5. Desarrollo de Scripts         →  Codificar y parametrizar
6. Ejecución                     →  Ejecutar y monitorear
7. Análisis de Resultados        →  Interpretar datos y RCA
8. Optimización y Re-testing     →  Iterar hasta cumplir SLAs
9. Cierre                        →  Reporting final y retrospectiva
```

---

## 📂 Contenido de la Subcarpeta

### [`01_Definicion_y_Fundamentos.md`](01_Introduccion_PTLC/01_Definicion_y_Fundamentos.md)
**Temas:** Qué es Performance Testing · Qué es el PTLC · Origen e historia · Principios fundamentales · NFRs (Non-Functional Requirements) · PTLC dentro del SDLC · Beneficios · Relación con otras disciplinas · Glosario completo de términos

**Ir aquí si necesitas:**
- Definir performance testing para stakeholders
- Entender la diferencia entre performance testing y otros tipos de QA
- Explicar por qué invertir en un ciclo estructurado
- Buscar la definición de un término técnico

---

### [`02_Roles_y_Responsabilidades.md`](01_Introduccion_PTLC/02_Roles_y_Responsabilidades.md)
**Temas:** Estructura del equipo de performance · Performance Engineer · Performance Architect · Test Lead · DevOps/SRE · Modelos de organización (centralizado, embedded, CoE) · Matriz RACI por fase · Career path · Comunicación y reporting a stakeholders

**Ir aquí si necesitas:**
- Armar un equipo de performance testing
- Definir responsabilidades claras por fase
- Crear un career path para el equipo
- Saber quién hace qué en cada fase del PTLC

---

### [`03_Frameworks_y_Estandares.md`](01_Introduccion_PTLC/03_Frameworks_y_Estandares.md)
**Temas:** ISO 25010 (calidad del producto) · ISTQB Performance Testing · Google SRE (SLO/SLI/SLA) · OWASP Performance · TMMi · Frameworks de ejecución · Métricas de madurez · Compliance y regulaciones · Referencias

**Ir aquí si necesitas:**
- Justificar prácticas con estándares internacionales
- Implementar SLOs/SLIs al estilo Google SRE
- Evaluar la madurez del proceso de performance testing
- Conocer regulaciones que aplican (financiero, salud, etc.)

---

## 🔗 Relación con otras categorías

| Desde aquí puedo ir a... | Para... |
|--------------------------|---------|
| [02_Tipos_de_Pruebas](02_Tipos_de_Pruebas_de_Rendimiento.md) | Entender qué tipos de pruebas existen |
| [03_Fases_del_PTLC](03_Fases_del_PTLC_Detalle.md) | Profundizar en la ejecución de cada fase |
| [04_Metricas](04_Metricas_y_KPIs.md) | Definir los KPIs que se mencionan en los NFRs |
