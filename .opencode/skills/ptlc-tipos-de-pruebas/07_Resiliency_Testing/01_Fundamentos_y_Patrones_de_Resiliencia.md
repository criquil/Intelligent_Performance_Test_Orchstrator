# 🛡️ Resiliency Testing — Parte 1 de 3: Fundamentos, steady-state hypothesis y patrones de resiliencia

> Qué es la resiliencia, en qué se diferencia de stress/failover/recovery, los principios de chaos engineering, la hipótesis de estado estable y los 7 patrones de supervivencia.
>
> **Guía en 3 partes:** · **1 · Fundamentos, steady-state hypothesis y patrones de resiliencia** (este documento) · 2 · [`Fault injection, herramientas y cloud-native`](02_Fault_Injection_Herramientas_y_Cloud.md) · 3 · [`Experimentos, Game Days, métricas y código`](03_Experimentos_Metricas_y_Operacion.md)
## Índice

1. [Definición y Fundamentos](#1-definición-y-fundamentos)
2. [Diferencia con Otros Tipos de Pruebas](#2-diferencia-con-otros-tipos-de-pruebas)
3. [Principios Clave](#3-principios-clave)
4. [Steady-State Hypothesis](#4-steady-state-hypothesis)
5. [Chaos Engineering como Disciplina](#5-chaos-engineering-como-disciplina)
6. [Patrones de Resiliencia](#6-patrones-de-resiliencia)
7. [Tipos de Fault Injection](02_Fault_Injection_Herramientas_y_Cloud.md#7-tipos-de-fault-injection)
8. [Herramientas de Resiliency Testing](02_Fault_Injection_Herramientas_y_Cloud.md#8-herramientas-de-resiliency-testing)
9. [Diseño de Experimentos de Caos](03_Experimentos_Metricas_y_Operacion.md#9-diseño-de-experimentos-de-caos)
10. [Game Days](03_Experimentos_Metricas_y_Operacion.md#10-game-days)
11. [Métricas de Resiliencia](03_Experimentos_Metricas_y_Operacion.md#11-métricas-de-resiliencia)
12. [Integración con CI/CD](02_Fault_Injection_Herramientas_y_Cloud.md#12-integración-con-cicd)
13. [Ejemplos Prácticos con Código](03_Experimentos_Metricas_y_Operacion.md#13-ejemplos-prácticos-con-código)
14. [Resiliency en Arquitecturas Cloud-Native](02_Fault_Injection_Herramientas_y_Cloud.md#14-resiliency-en-arquitecturas-cloud-native)
15. [Antipatrones y Errores Comunes](03_Experimentos_Metricas_y_Operacion.md#15-antipatrones-y-errores-comunes)
16. [Checklist de Implementación](03_Experimentos_Metricas_y_Operacion.md#16-checklist-de-implementación)
- [Referencias](#referencias)

---

## 1. Definición y Fundamentos

### ¿Qué es Resiliency Testing?

**Resiliency Testing** (pruebas de resiliencia) es la disciplina que verifica la capacidad de un sistema para:

1. **Absorber perturbaciones** sin perder funcionalidad crítica
2. **Degradarse graciosamente** cuando los recursos son insuficientes
3. **Recuperarse automáticamente** a un estado operativo normal
4. **Adaptarse** a condiciones cambiantes del entorno

> 🎯 **Objetivo central:** No evitar que las fallas ocurran, sino asegurar que el sistema **sobreviva** cuando ocurren.

### Diferencia fundamental con otros enfoques

| Aspecto | Testing Tradicional | Resiliency Testing |
|---------|--------------------|--------------------|
| Premisa | "¿Funciona correctamente?" | "¿Sobrevive cuando algo falla?" |
| Enfoque | Happy path + edge cases | Fault injection + degradation |
| Entorno | Condiciones ideales | Condiciones adversas |
| Resultado esperado | Éxito/Fallo binario | Grado de degradación aceptable |
| Filosofía | Prevenir defectos | Aceptar fallas, mitigar impacto |

### Los 4 Pilares de la Resiliencia

```
┌──────────────────────────────────────────────────────────────────┐
│                    RESILIENCIA DEL SISTEMA                        │
├────────────────┬────────────────┬────────────────┬───────────────┤
│   RESISTENCIA  │   ABSORCIÓN    │  RECUPERACIÓN  │  ADAPTACIÓN   │
│                │                │                │               │
│ Resistir sin   │ Absorber el    │ Volver al      │ Aprender y    │
│ degradarse     │ impacto con    │ estado normal  │ mejorar tras  │
│ ante cargas    │ degradación    │ rápidamente    │ cada falla    │
│ esperadas      │ controlada     │                │               │
├────────────────┼────────────────┼────────────────┼───────────────┤
│ Load Testing   │ Graceful       │ Recovery       │ Auto-scaling  │
│ Baseline       │ Degradation    │ Testing        │ Self-healing  │
│                │ Circuit Breaker│ Failover       │ Feedback loops│
└────────────────┴────────────────┴────────────────┴───────────────┘
```

---

## 2. Diferencia con Otros Tipos de Pruebas

### Resiliency vs. Stress Testing

| Dimensión | Stress Testing | Resiliency Testing |
|-----------|---------------|--------------------|
| Qué se inyecta | Carga excesiva | Fallas en componentes |
| Pregunta clave | "¿A qué punto se rompe?" | "¿Cómo se comporta roto?" |
| Objetivo | Encontrar límites | Validar mecanismos de supervivencia |
| Tipo de fallo | Sobrecarga de recursos | Pérdida de dependencias |

### Resiliency vs. Failover Testing

| Dimensión | Failover Testing | Resiliency Testing |
|-----------|------------------|--------------------|
| Alcance | Componente específico | Sistema completo |
| Foco | Switchover a backup | Comportamiento sistémico |
| Duración | Corta (evento puntual) | Prolongada (condiciones sostenidas) |
| Combinación | Un fallo a la vez | Múltiples fallas simultáneas |

### Resiliency vs. Recovery Testing

| Dimensión | Recovery Testing | Resiliency Testing |
|-----------|------------------|--------------------|
| Momento evaluado | Post-falla (restauración) | Durante y post-falla |
| Métrica principal | RTO / RPO | Disponibilidad continua |
| Expectativa | Sistema se recupera | Sistema nunca deja de servir |

### ¿Cuándo usar Resiliency Testing?

- ✅ Sistemas distribuidos con múltiples dependencias
- ✅ Arquitecturas de microservicios
- ✅ Aplicaciones cloud-native
- ✅ Sistemas con SLAs de alta disponibilidad (99.9%+)
- ✅ Antes de eventos de alto tráfico (Black Friday, launches)
- ✅ Post-incidentes para validar fixes
- ✅ Regulaciones de continuidad de negocio (DORA, PCI-DSS)

---

## 3. Principios Clave

### Principios de Chaos Engineering (principlesofchaos.org)

1. **Construir una hipótesis alrededor del comportamiento de estado estable**
2. **Variar eventos del mundo real** (no eventos teóricos)
3. **Ejecutar experimentos en producción** (con controles)
4. **Automatizar experimentos para ejecución continua**
5. **Minimizar el radio de explosión** (blast radius)

### Principios adicionales de Resiliency Testing

6. **Asumir que las fallas son inevitables** — diseñar para sobrevivir, no para evitar
7. **Probar el sistema, no el componente** — las fallas emergen de interacciones
8. **Medir degradación, no solo disponibilidad** — no es binario
9. **Incluir al equipo humano** — la respuesta operacional es parte de la resiliencia
10. **Iterar progresivamente** — de ambiente de prueba → staging → producción

---

## 4. Steady-State Hypothesis

### Concepto

La **Steady-State Hypothesis** (hipótesis de estado estable) define el comportamiento "normal" del sistema mediante métricas medibles. Es el punto de referencia contra el cual se evalúa el impacto de las fallas inyectadas.

### Componentes de una Steady-State Hypothesis

```yaml
steady_state_hypothesis:
  nombre: "Sistema de pagos procesa transacciones normalmente"
  métricas:
    - nombre: "Tasa de éxito de transacciones"
      valor_normal: ">= 99.5%"
      fuente: "prometheus: sum(rate(transactions_success_total[5m]))"
      
    - nombre: "Latencia P95"
      valor_normal: "<= 500ms"
      fuente: "prometheus: histogram_quantile(0.95, rate(http_duration_seconds_bucket[5m]))"
      
    - nombre: "Throughput"
      valor_normal: ">= 800 TPS"
      fuente: "prometheus: sum(rate(http_requests_total[5m]))"
      
    - nombre: "Error Rate"
      valor_normal: "<= 0.5%"
      fuente: "prometheus: sum(rate(http_errors_total[5m])) / sum(rate(http_requests_total[5m]))"
      
  tolerancias_durante_falla:
    - nombre: "Tasa de éxito de transacciones"
      valor_aceptable: ">= 95%"  # Degradación permitida
      
    - nombre: "Latencia P95"
      valor_aceptable: "<= 2000ms"  # 4x peor aceptable
      
    - nombre: "Throughput"
      valor_aceptable: ">= 400 TPS"  # 50% mínimo
      
    - nombre: "Error Rate"
      valor_aceptable: "<= 5%"  # Hasta 10x peor temporal
```

### Proceso de validación

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. MEDIR ESTADO ESTABLE (Baseline 10 min)                       │
│    → Confirmar que métricas están dentro de "normal"            │
│                                                                  │
│ 2. FORMULAR HIPÓTESIS                                           │
│    "Si [fallo X], el sistema mantendrá [métricas] dentro de    │
│     [tolerancias] y se recuperará en [tiempo Y]"               │
│                                                                  │
│ 3. INYECTAR FALLO                                               │
│    → Activar fault injection                                    │
│                                                                  │
│ 4. OBSERVAR DURANTE FALLO (5-15 min)                           │
│    → ¿Métricas dentro de tolerancias de degradación?           │
│                                                                  │
│ 5. REMOVER FALLO                                                │
│    → Desactivar fault injection                                 │
│                                                                  │
│ 6. MEDIR RECUPERACIÓN                                           │
│    → ¿Cuánto tiempo para volver a steady state?                │
│                                                                  │
│ 7. EVALUAR HIPÓTESIS                                            │
│    → CONFIRMADA: sistema resiliente a este fallo               │
│    → REFUTADA: acción correctiva necesaria                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Chaos Engineering como Disciplina

### Origen y evolución

| Año | Hito |
|-----|------|
| 2010 | Netflix crea Chaos Monkey (termina instancias EC2 aleatoriamente) |
| 2011 | Netflix publica Simian Army (suite completa de herramientas) |
| 2014 | Netflix crea el rol "Chaos Engineer" |
| 2015 | Se publica "Principles of Chaos Engineering" |
| 2017 | Gremlin lanza plataforma comercial |
| 2018 | LitmusChaos (CNCF) para Kubernetes |
| 2019 | AWS Fault Injection Simulator |
| 2020 | Azure Chaos Studio |
| 2021 | Chaos Engineering se vuelve mainstream (DORA report lo menciona) |

### Simian Army de Netflix

```
┌─────────────────────────────────────────────────────────────┐
│                     SIMIAN ARMY                              │
├─────────────────────┬───────────────────────────────────────┤
│ Chaos Monkey        │ Mata instancias aleatoriamente        │
│ Chaos Gorilla       │ Mata zonas de disponibilidad          │
│ Chaos Kong          │ Simula pérdida de región completa     │
│ Latency Monkey      │ Inyecta latencia en servicios         │
│ Conformity Monkey   │ Detecta instancias no conformes       │
│ Doctor Monkey       │ Detecta instancias enfermas           │
│ Janitor Monkey      │ Limpia recursos no usados             │
│ Security Monkey     │ Detecta vulnerabilidades              │
│ 10-18 Monkey        │ Detecta problemas i18n/l10n           │
└─────────────────────┴───────────────────────────────────────┘
```

### Niveles de madurez en Chaos Engineering

```
Nivel 0 - BÁSICO:
  └─ Manual, ad-hoc, solo en desarrollo
  
Nivel 1 - REPETIBLE:
  └─ Experimentos documentados, staging regular
  
Nivel 2 - DEFINIDO:
  └─ Framework automatizado, métricas de resiliencia
  
Nivel 3 - GESTIONADO:
  └─ Chaos en CI/CD, alertas automáticas, game days regulares
  
Nivel 4 - OPTIMIZADO:
  └─ Chaos en producción continuo, auto-healing, ML para detección
```

---

## 6. Patrones de Resiliencia

### 6.1 Circuit Breaker (Interruptor de Circuito)

**Propósito:** Prevenir que un componente fallido cause cascada de fallas.

```
Estados del Circuit Breaker:

    ┌──────────┐    threshold     ┌──────────┐    timeout    ┌──────────────┐
    │  CLOSED  │───superado──────►│   OPEN   │──expirado───►│  HALF-OPEN   │
    │(funciona)│                  │ (rechaza)│              │  (1 intento) │
    └──────────┘◄─────────────────└──────────┘◄─fallo──────└──────────────┘
         ▲                                                        │
         └──────────────────────éxito─────────────────────────────┘
```

**Configuración típica:**

```javascript
// Ejemplo conceptual - Resilience4j / Polly style
const circuitBreakerConfig = {
  failureRateThreshold: 50,        // % de fallas para abrir
  slowCallRateThreshold: 80,       // % de llamadas lentas para abrir
  slowCallDurationThreshold: 2000, // ms para considerar "lenta"
  waitDurationInOpenState: 30000,  // ms antes de probar half-open
  permittedNumberOfCallsInHalfOpenState: 3,
  slidingWindowSize: 10,           // últimas N llamadas evaluadas
  minimumNumberOfCalls: 5,         // mínimo antes de evaluar
};
```

**Qué validar en Resiliency Testing:**
- ✅ El circuit breaker se abre cuando el servicio downstream falla
- ✅ Las requests se rechazan rápido (fail-fast) en estado OPEN
- ✅ El half-open intenta reconexión tras el timeout
- ✅ Se restaura a CLOSED cuando el downstream se recupera
- ✅ Respuestas de fallback se sirven durante OPEN

### 6.2 Bulkhead (Mampara)

**Propósito:** Aislar componentes para que la falla de uno no agote recursos de otros.

```
SIN Bulkhead:                     CON Bulkhead:
┌──────────────────┐             ┌──────┬──────┬──────┐
│   Thread Pool    │             │Pool A│Pool B│Pool C│
│   (compartido)   │             │ 10   │  20  │  10  │
│                  │             │thread│thread│thread│
│ Si Servicio A    │             │      │      │      │
│ se cuelga, agota │             │ Si A │ B y C│siguen│
│ TODO el pool     │             │cuelga│      │ ok   │
└──────────────────┘             └──────┴──────┴──────┘
```

**Tipos de Bulkhead:**
- **Thread Pool Isolation:** Cada dependencia tiene su propio pool de threads
- **Semaphore Isolation:** Limita concurrencia sin threads dedicados
- **Process Isolation:** Cada servicio en su propio proceso/container
- **Pod/Node Isolation:** Separación a nivel de infraestructura (Kubernetes)

**Qué validar:**
- ✅ Un servicio saturado no consume threads de otros servicios
- ✅ Los timeouts se respetan por pool
- ✅ Requests a servicios sanos continúan procesándose

### 6.3 Retry con Backoff Exponencial

**Propósito:** Reintentar operaciones fallidas sin saturar el servicio en recuperación.

```javascript
// Patrón de retry con jitter
function retryWithBackoff(operation, config) {
  const { maxRetries = 3, baseDelay = 1000, maxDelay = 30000 } = config;
  
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return operation();
    } catch (error) {
      if (attempt === maxRetries) throw error;
      
      // Exponential backoff con jitter
      const delay = Math.min(
        baseDelay * Math.pow(2, attempt) + Math.random() * 1000,
        maxDelay
      );
      sleep(delay);
    }
  }
}
```

**Qué validar:**
- ✅ Retries no causan "thundering herd" (avalancha de reintentos)
- ✅ Jitter distribuye los retries en el tiempo
- ✅ Se respeta el maxRetries (no retry infinito)
- ✅ Se combinan correctamente con circuit breaker

### 6.4 Timeout Pattern

**Propósito:** No esperar indefinidamente por respuestas.

```
Timeouts en cadena (cascading):

Cliente → API Gateway → Servicio A → Servicio B → Base de Datos
          timeout=10s    timeout=5s   timeout=2s    timeout=1s
          
REGLA: timeout[n] > timeout[n+1]
(cada capa tiene timeout menor que la anterior)
```

**Qué validar:**
- ✅ Timeouts configurados en cada capa
- ✅ Timeout del caller > timeout del callee
- ✅ Conexión se libera correctamente tras timeout
- ✅ Respuesta apropiada al cliente (503, retry-after)

### 6.5 Graceful Degradation

**Propósito:** Ofrecer funcionalidad reducida en vez de falla total.

```
Niveles de degradación:

Nivel 0 - NORMAL:
  └─ Todas las features activas, datos en tiempo real

Nivel 1 - DEGRADADO LEVE:
  └─ Features no-críticas deshabilitadas
  └─ Ejemplo: Desactivar recomendaciones, usar cache stale

Nivel 2 - DEGRADADO MODERADO:
  └─ Solo funcionalidad core
  └─ Ejemplo: Solo búsqueda y compra, sin reviews ni historial

Nivel 3 - MÍNIMO VIABLE:
  └─ Experiencia mínima funcional
  └─ Ejemplo: Página estática con info de contacto

Nivel 4 - MANTENIMIENTO:
  └─ Sistema offline con mensaje informativo
```

**Qué validar:**
- ✅ Feature flags funcionan para deshabilitar componentes
- ✅ La experiencia de usuario permanece coherente
- ✅ No hay errores no manejados expuestos al usuario
- ✅ La degradación es automática (no requiere intervención manual)

### 6.6 Rate Limiting y Throttling

**Propósito:** Proteger el sistema de sobrecarga controlando el flujo de entrada.

**Algoritmos comunes:**
- **Token Bucket:** Tokens se agregan a tasa fija, cada request consume un token
- **Leaky Bucket:** Requests se procesan a tasa fija, exceso se descarta/encola
- **Fixed Window:** Límite por ventana de tiempo fija
- **Sliding Window:** Límite por ventana deslizante (más suave)

**Qué validar:**
- ✅ Requests excedentes reciben HTTP 429 con header Retry-After
- ✅ Clientes prioritarios tienen limits mayores
- ✅ Rate limit no bloquea health checks
- ✅ Distribuido correctamente en multi-instancia

### 6.7 Fallback Pattern

**Propósito:** Proveer respuesta alternativa cuando el servicio principal falla.

```javascript
// Cadena de fallback
async function getProductPrice(productId) {
  try {
    // 1. Servicio principal (real-time pricing)
    return await pricingService.getPrice(productId);
  } catch (e) {
    try {
      // 2. Cache distribuido (precio reciente)
      return await redis.get(`price:${productId}`);
    } catch (e2) {
      try {
        // 3. Cache local (puede estar desactualizado)
        return localCache.get(productId);
      } catch (e3) {
        // 4. Precio default catalogado
        return catalog.getDefaultPrice(productId);
      }
    }
  }
}
```

---

## Referencias

- [Principles of Chaos Engineering](https://principlesofchaos.org/)
- [Netflix Tech Blog - Chaos Engineering](https://netflixtechblog.com/)
- [Gremlin - Chaos Engineering Resources](https://www.gremlin.com/chaos-engineering/)
- [LitmusChaos Documentation](https://docs.litmuschaos.io/)
- [Chaos Mesh Documentation](https://chaos-mesh.org/docs/)
- [AWS Fault Injection Simulator](https://docs.aws.amazon.com/fis/)
- [Azure Chaos Studio](https://learn.microsoft.com/en-us/azure/chaos-studio/)
- [Google SRE Book - Testing for Reliability](https://sre.google/sre-book/testing-reliability/)
- [Release It! - Michael Nygard](https://pragprog.com/titles/mnee2/release-it-second-edition/)
- [Chaos Engineering - Casey Rosenthal & Nora Jones](https://www.oreilly.com/library/view/chaos-engineering/9781492043850/)

---

> 💡 **Resiliency Testing no es opcional para sistemas distribuidos modernos.**
> No se trata de SI el sistema fallará, sino de CUÁNDO — y de estar preparado para sobrevivir cuando ocurra.

