# 🛡️ Resiliency Testing (Pruebas de Resiliencia)

## Índice

1. [Definición y Fundamentos](#1-definición-y-fundamentos)
2. [Diferencia con Otros Tipos de Pruebas](#2-diferencia-con-otros-tipos-de-pruebas)
3. [Principios Clave](#3-principios-clave)
4. [Steady-State Hypothesis](#4-steady-state-hypothesis)
5. [Chaos Engineering como Disciplina](#5-chaos-engineering-como-disciplina)
6. [Patrones de Resiliencia](#6-patrones-de-resiliencia)
7. [Tipos de Fault Injection](#7-tipos-de-fault-injection)
8. [Herramientas de Resiliency Testing](#8-herramientas-de-resiliency-testing)
9. [Diseño de Experimentos de Caos](#9-diseño-de-experimentos-de-caos)
10. [Game Days](#10-game-days)
11. [Métricas de Resiliencia](#11-métricas-de-resiliencia)
12. [Integración con CI/CD](#12-integración-con-cicd)
13. [Ejemplos Prácticos con Código](#13-ejemplos-prácticos-con-código)
14. [Resiliency en Arquitecturas Cloud-Native](#14-resiliency-en-arquitecturas-cloud-native)
15. [Antipatrones y Errores Comunes](#15-antipatrones-y-errores-comunes)
16. [Checklist de Implementación](#16-checklist-de-implementación)

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

## 7. Tipos de Fault Injection

### 7.1 Fallas de Red

| Tipo de Falla | Descripción | Herramienta |
|---------------|-------------|-------------|
| Latencia | Agregar delay a paquetes | tc netem, Gremlin |
| Packet Loss | Descartar % de paquetes | tc netem, iptables |
| DNS Failure | Resolver a IP incorrecta | iptables, CoreDNS |
| Partition | Aislar nodo/servicio de la red | iptables, Chaos Mesh |
| Bandwidth Limit | Reducir ancho de banda | tc, wondershaper |
| Connection Reset | Resetear conexiones TCP | iptables RST |
| SSL/TLS Error | Certificados inválidos | mitmproxy |

**Ejemplo con tc (Traffic Control):**
```bash
# Agregar 200ms de latencia con 50ms de jitter
tc qdisc add dev eth0 root netem delay 200ms 50ms

# Simular 5% de packet loss
tc qdisc add dev eth0 root netem loss 5%

# Simular packet corruption
tc qdisc add dev eth0 root netem corrupt 2%

# Combinar: latencia + loss
tc qdisc add dev eth0 root netem delay 100ms loss 3%

# Remover reglas
tc qdisc del dev eth0 root
```

### 7.2 Fallas de Compute

| Tipo de Falla | Descripción | Cómo simular |
|---------------|-------------|--------------|
| CPU Stress | Saturar CPU al 100% | stress-ng, cpu burn |
| Memory Exhaustion | Consumir toda la RAM | stress-ng --vm |
| Disk Full | Llenar el disco | fallocate, dd |
| Process Kill | Matar proceso | kill -9, Chaos Monkey |
| OOM Kill | Forzar Out of Memory | cgroups limits |
| I/O Saturation | Saturar disco I/O | fio, stress-ng |
| Fork Bomb | Agotar PIDs | ulimit + fork |

**Ejemplo con stress-ng:**
```bash
# CPU stress: 4 workers al 90% por 60 segundos
stress-ng --cpu 4 --cpu-load 90 --timeout 60s

# Memory: consumir 2GB
stress-ng --vm 2 --vm-bytes 1G --timeout 60s

# I/O: saturar disco
stress-ng --io 4 --hdd 2 --timeout 60s

# Combinado
stress-ng --cpu 2 --cpu-load 80 --vm 1 --vm-bytes 512M --io 2 --timeout 120s
```

### 7.3 Fallas de Aplicación

| Tipo de Falla | Descripción | Método |
|---------------|-------------|--------|
| Exception Injection | Lanzar excepciones en código | Feature flags, AOP |
| Response Delay | Agregar delay a responses | Service mesh (Istio) |
| Error Response | Retornar HTTP 500/503 | Proxy, mock |
| Corrupt Data | Retornar datos malformados | Proxy interceptor |
| Memory Leak | Simular leak gradual | Código controlado |
| Thread Deadlock | Bloquear threads | Código controlado |
| Connection Pool Exhaust | Agotar conexiones | Never-close connections |

### 7.4 Fallas de Dependencias

| Tipo de Falla | Descripción | Impacto esperado |
|---------------|-------------|------------------|
| Database Down | Base de datos inaccesible | Fallback a cache/queue |
| Cache Miss | Redis/Memcached caído | Ir directo a DB (mayor latencia) |
| Queue Full | Message broker saturado | Backpressure, retry |
| Third-party API Down | Servicio externo no responde | Datos cacheados/default |
| Certificate Expiry | TLS cert expirado | Connection refused |
| Auth Service Down | No se pueden validar tokens | Graceful deny o cache |

### 7.5 Fallas de Infraestructura

| Tipo de Falla | Descripción | Escala |
|---------------|-------------|--------|
| Instance Termination | Matar una VM/container | Nodo individual |
| AZ Failure | Perder zona de disponibilidad | Regional |
| Region Failure | Perder región completa | Multi-region |
| Load Balancer Failure | LB no enruta tráfico | Ingress |
| DNS Outage | Resolución DNS falla | Global |
| Storage Failure | EBS/disk no disponible | Persistencia |

---

## 8. Herramientas de Resiliency Testing

### 8.1 Comparativa de Herramientas

| Herramienta | Tipo | Entorno | Complejidad | Costo |
|-------------|------|---------|-------------|-------|
| Chaos Monkey | OSS | AWS | Baja | Gratis |
| Gremlin | Comercial | Multi-cloud | Media | $$$$ |
| LitmusChaos | OSS (CNCF) | Kubernetes | Media | Gratis |
| Chaos Mesh | OSS (CNCF) | Kubernetes | Media | Gratis |
| AWS FIS | Managed | AWS | Baja | $ (por experimento) |
| Azure Chaos Studio | Managed | Azure | Baja | $ |
| Chaos Toolkit | OSS | Agnóstico | Alta | Gratis |
| Pumba | OSS | Docker | Baja | Gratis |
| PowerfulSeal | OSS | Kubernetes | Media | Gratis |
| Toxiproxy | OSS | Cualquiera | Baja | Gratis |
| Simmy | OSS (.NET) | Aplicación | Baja | Gratis |

### 8.2 LitmusChaos (Kubernetes)

```yaml
# Ejemplo: ChaosEngine para matar pods
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: payment-service-chaos
  namespace: production
spec:
  appinfo:
    appns: 'production'
    applabel: 'app=payment-service'
    appkind: 'deployment'
  engineState: 'active'
  chaosServiceAccount: litmus-admin
  experiments:
    - name: pod-delete
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: '60'        # Duración del caos (segundos)
            - name: CHAOS_INTERVAL
              value: '10'        # Intervalo entre deletes
            - name: FORCE
              value: 'true'      # Force delete (kill -9)
            - name: PODS_AFFECTED_PERC
              value: '50'        # % de pods afectados
        probe:
          - name: "check-payment-endpoint"
            type: "httpProbe"
            httpProbe/inputs:
              url: "http://payment-service:8080/health"
              method:
                get:
                  criteria: "=="
                  responseCode: "200"
            mode: "Continuous"
            runProperties:
              probeTimeout: 5
              interval: 5
              retry: 3
```

### 8.3 Chaos Mesh (Kubernetes)

```yaml
# Ejemplo: Network chaos - agregar latencia
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: network-delay-payment
  namespace: chaos-testing
spec:
  action: delay
  mode: all
  selector:
    namespaces:
      - production
    labelSelectors:
      app: payment-service
  delay:
    latency: "500ms"
    correlation: "50"
    jitter: "100ms"
  duration: "5m"
  scheduler:
    cron: "@every 2h"  # Ejecutar cada 2 horas
```

### 8.4 AWS Fault Injection Simulator

```json
{
  "description": "Kill 30% of ECS tasks in payment service",
  "targets": {
    "payment-tasks": {
      "resourceType": "aws:ecs:task",
      "selectionMode": "PERCENT(30)",
      "resourceTags": {
        "service": "payment"
      }
    }
  },
  "actions": {
    "stop-tasks": {
      "actionId": "aws:ecs:stop-task",
      "parameters": {},
      "targets": {
        "Tasks": "payment-tasks"
      },
      "startAfter": ["wait-for-steady-state"]
    },
    "wait-for-steady-state": {
      "actionId": "aws:fis:wait",
      "parameters": {
        "duration": "PT2M"
      }
    }
  },
  "stopConditions": [
    {
      "source": "aws:cloudwatch:alarm",
      "value": "arn:aws:cloudwatch:us-east-1:123456789:alarm:PaymentErrorRate"
    }
  ],
  "roleArn": "arn:aws:iam::123456789:role/FISRole"
}
```

### 8.5 Toxiproxy (Proxy de fallas)

```bash
# Crear proxy para PostgreSQL
toxiproxy-cli create postgres_primary \
  --listen 0.0.0.0:5432 \
  --upstream postgres-primary:5432

# Agregar latencia
toxiproxy-cli toxic add postgres_primary \
  --type latency \
  --attribute latency=500 \
  --attribute jitter=100

# Simular timeout (slow_close)
toxiproxy-cli toxic add postgres_primary \
  --type slow_close \
  --attribute delay=3000

# Simular connection reset
toxiproxy-cli toxic add postgres_primary \
  --type reset_peer \
  --attribute timeout=2000

# Bandwidth limit (1KB/s - extremadamente lento)
toxiproxy-cli toxic add postgres_primary \
  --type bandwidth \
  --attribute rate=1
```

### 8.6 Chaos Toolkit (Framework agnóstico)

```json
{
  "title": "Payment Service Resilience Experiment",
  "description": "Verificar que el servicio de pagos sobrevive la caída de Redis",
  "tags": ["payment", "redis", "resilience"],
  "steady-state-hypothesis": {
    "title": "Payment service responde normalmente",
    "probes": [
      {
        "type": "probe",
        "name": "payment-health-check",
        "tolerance": 200,
        "provider": {
          "type": "http",
          "url": "http://payment-service:8080/health",
          "timeout": 3
        }
      },
      {
        "type": "probe",
        "name": "payment-success-rate",
        "tolerance": {
          "type": "range",
          "range": [95.0, 100.0]
        },
        "provider": {
          "type": "python",
          "module": "chaosprometheus.probes",
          "func": "query_instant",
          "arguments": {
            "query": "sum(rate(payment_success_total[5m])) / sum(rate(payment_total[5m])) * 100"
          }
        }
      }
    ]
  },
  "method": [
    {
      "type": "action",
      "name": "kill-redis-primary",
      "provider": {
        "type": "python",
        "module": "chaosaws.ecs.actions",
        "func": "stop_task",
        "arguments": {
          "cluster": "production",
          "task": "redis-primary",
          "reason": "Chaos experiment: Redis resilience test"
        }
      },
      "pauses": {
        "after": 60
      }
    }
  ],
  "rollbacks": [
    {
      "type": "action",
      "name": "restart-redis",
      "provider": {
        "type": "python",
        "module": "chaosaws.ecs.actions",
        "func": "start_task",
        "arguments": {
          "cluster": "production",
          "task_definition": "redis-primary:latest"
        }
      }
    }
  ]
}
```

---

## 9. Diseño de Experimentos de Caos

### Template de Experimento

```markdown
## Experimento: [NOMBRE]

### Metadata
- **ID:** CHAOS-001
- **Fecha:** 2024-XX-XX
- **Equipo:** Platform Engineering
- **Aprobado por:** [nombre]
- **Blast Radius:** [Bajo/Medio/Alto]

### Contexto
- **Sistema objetivo:** [nombre del sistema]
- **Componente afectado:** [nombre del componente]
- **Entorno:** [staging/production]
- **Ventana:** [horario de menor tráfico]

### Steady-State Hypothesis
"Creemos que [el sistema] puede tolerar [falla X] 
manteniendo [métrica Y] dentro de [umbral Z] 
y recuperándose en menos de [tiempo W]."

### Métricas a Monitorear
| Métrica | Normal | Degradado Aceptable | Crítico (abort) |
|---------|--------|--------------------:|----------------:|
| Success Rate | > 99.5% | > 95% | < 90% |
| P95 Latency | < 500ms | < 2000ms | > 5000ms |
| Error Rate | < 0.5% | < 5% | > 10% |

### Método (Pasos)
1. Confirmar steady-state (10 min observación)
2. Activar fault injection: [descripción exacta]
3. Observar durante: [X minutos]
4. Remover fault injection
5. Observar recuperación durante: [Y minutos]

### Abort Conditions (Parar inmediatamente si...)
- [ ] Error rate > 10% por más de 2 minutos
- [ ] P99 > 10 segundos
- [ ] Alertas de negocio activas
- [ ] Impacto a usuarios externos detectado
- [ ] Revenue impact > $X

### Rollback Plan
1. [Paso para revertir la fault injection]
2. [Paso para forzar recovery]
3. [Contacto de escalación]

### Resultados
- **Hipótesis:** [CONFIRMADA / REFUTADA]
- **Hallazgos:**
  - ...
- **Acciones:**
  - ...
```

### Matriz de Priorización de Experimentos

```
                     IMPACTO AL NEGOCIO
                  Bajo          Alto
              ┌──────────┬──────────────┐
        Alta  │ QUICK    │ PRIORITARIO  │
PROBABILIDAD  │ WINS     │ (hacer       │
  DE FALLA    │          │  primero)    │
              ├──────────┼──────────────┤
        Baja  │ BACKLOG  │ PLANIFICAR   │
              │ (hacer   │ (hacer       │
              │  último) │  segundo)    │
              └──────────┴──────────────┘
```

### Progresión de complejidad

```
Semana 1-2: FALLAS SIMPLES
  └─ Un componente a la vez
  └─ Entorno de staging
  └─ Duración corta (< 5 min)

Semana 3-4: FALLAS COMPUESTAS
  └─ Dos componentes simultáneos
  └─ Staging con carga realista
  └─ Duración media (5-15 min)

Mes 2: ESCENARIOS REALISTAS
  └─ Basados en post-mortems reales
  └─ Pre-producción / Canary
  └─ Duración extendida (15-60 min)

Mes 3+: PRODUCCIÓN
  └─ Game days programados
  └─ Fallas multi-servicio
  └─ Duración real (30+ min)
  └─ Con equipo de respuesta activo
```

---

## 10. Game Days

### ¿Qué es un Game Day?

Un **Game Day** es un ejercicio planificado donde un equipo inyecta fallas deliberadamente en producción (o staging) para validar la resiliencia del sistema Y la capacidad de respuesta del equipo humano.

### Estructura de un Game Day

```
┌─────────────────────────────────────────────────────────────────┐
│                        GAME DAY TIMELINE                         │
├─────────┬───────────────────────────────────────────────────────┤
│ -1 week │ Planificación, comunicación, preparación              │
│ -1 day  │ Verificar runbooks, alertas, dashboards              │
│         │                                                       │
│ T+0:00  │ Kickoff: briefing al equipo                          │
│ T+0:15  │ Validar steady-state                                 │
│ T+0:30  │ INYECTAR FALLA #1                                    │
│ T+0:45  │ Observar / Equipo responde                           │
│ T+1:00  │ INYECTAR FALLA #2 (escalar)                          │
│ T+1:15  │ Observar cascada / respuesta                         │
│ T+1:30  │ REMOVER FALLAS                                       │
│ T+1:45  │ Validar recuperación completa                        │
│ T+2:00  │ Debrief inmediato (hot wash)                         │
│         │                                                       │
│ +1 day  │ Retrospectiva detallada                              │
│ +1 week │ Action items implementados                           │
└─────────┴───────────────────────────────────────────────────────┘
```

### Roles en un Game Day

| Rol | Responsabilidad |
|-----|----------------|
| **Game Master** | Diseña escenarios, inyecta fallas, controla el ejercicio |
| **Observadores** | Monitoreán métricas, documentan comportamiento del sistema |
| **Respondedores** | Equipo que responde como si fuera un incidente real |
| **Safety Officer** | Autoridad para ABORT si se excede el blast radius |
| **Narrator** | Documenta timeline de eventos en tiempo real |

### Métricas del Game Day (no solo del sistema)

**Métricas del equipo humano:**
- **MTTD (Mean Time to Detect):** ¿Cuánto tardó el equipo en notar el problema?
- **MTTI (Mean Time to Identify):** ¿Cuánto en identificar la causa?
- **MTTR (Mean Time to Resolve):** ¿Cuánto en resolver?
- **Communication Effectiveness:** ¿Se notificó a stakeholders a tiempo?
- **Runbook Accuracy:** ¿Los runbooks sirvieron o estaban desactualizados?

---

## 11. Métricas de Resiliencia

### Métricas Cuantitativas

| Métrica | Fórmula | Objetivo típico |
|---------|---------|-----------------|
| **Availability** | uptime / (uptime + downtime) × 100 | 99.95% |
| **MTBF** | Total uptime / Número de fallas | > 720h (30 días) |
| **MTTR** | Total downtime / Número de fallas | < 5 min |
| **MTTD** | Σ(tiempo de detección) / N | < 1 min |
| **Recovery Time** | Tiempo falla → steady state | < 2 min |
| **Degradation Depth** | % de pérdida funcional durante falla | < 20% |
| **Blast Radius** | % de usuarios afectados | < 5% |
| **Error Budget Consumed** | downtime / allowable_downtime × 100 | < 80%/quarter |

### Score de Resiliencia

```
Resilience Score = Σ (peso_i × score_i) / Σ peso_i

Donde cada dimensión tiene score 0-100:

┌─────────────────────────────────────────────────────────────┐
│ Dimensión            │ Peso │ Cómo se mide                  │
├──────────────────────┼──────┼───────────────────────────────┤
│ Redundancia          │  20% │ # replicas, multi-AZ, multi-R │
│ Detección            │  15% │ MTTD, cobertura de alertas    │
│ Recuperación         │  20% │ MTTR, auto-healing rate       │
│ Degradación graceful │  15% │ % funcionalidad mantenida     │
│ Aislamiento          │  15% │ Blast radius promedio         │
│ Automatización       │  15% │ % respuestas automatizadas    │
└──────────────────────┴──────┴───────────────────────────────┘

Ejemplo:
  Redundancia:   80/100 (multi-AZ, no multi-region)
  Detección:     90/100 (alertas < 30s)
  Recuperación:  70/100 (MTTR 3 min, algo manual)
  Degradación:   60/100 (algunos servicios no tienen fallback)
  Aislamiento:   85/100 (bulkheads en 85% de servicios)
  Automatización: 75/100 (auto-scaling pero rollback manual)

Score = (20×80 + 15×90 + 20×70 + 15×60 + 15×85 + 15×75) / 100
      = (1600 + 1350 + 1400 + 900 + 1275 + 1125) / 100
      = 76.5 / 100
```

### SLIs y SLOs para Resiliencia

```yaml
# Ejemplo de SLO document
slos:
  - name: "Payment Service Availability"
    sli: "proportion of successful payment requests"
    target: 99.95%
    window: "30 days rolling"
    error_budget: "21.6 minutes / month"
    
  - name: "Recovery from single-AZ failure"
    sli: "time from AZ loss detection to full traffic redistribution"
    target: "< 60 seconds in 99% of cases"
    
  - name: "Graceful degradation under cache failure"
    sli: "proportion of requests served (potentially from fallback) during Redis outage"
    target: "100% of requests get a response (even if degraded)"
    
  - name: "Blast radius containment"
    sli: "proportion of unrelated services unaffected by a single-service failure"
    target: "> 99%"
```

---

## 12. Integración con CI/CD

### Pipeline de Resiliency Testing

```yaml
# .opencode/workflows/resilience-tests.yml
name: Resilience Tests

on:
  schedule:
    - cron: '0 2 * * 1-5'  # Lun-Vie a las 2 AM
  workflow_dispatch:
    inputs:
      experiment:
        description: 'Experiment to run'
        required: true
        type: choice
        options:
          - pod-kill
          - network-latency
          - resource-exhaustion
          - dependency-failure

jobs:
  resilience-test:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup kubectl
        uses: azure/setup-kubectl@v3
        
      - name: Connect to cluster
        run: |
          aws eks update-kubeconfig --name staging-cluster
          
      - name: Verify steady state
        run: |
          ./scripts/verify-steady-state.sh
          
      - name: Run chaos experiment
        run: |
          kubectl apply -f chaos-experiments/${{ inputs.experiment }}.yaml
          
      - name: Wait for experiment duration
        run: sleep 300  # 5 minutes
        
      - name: Verify system resilience
        run: |
          ./scripts/verify-resilience-criteria.sh
          
      - name: Cleanup chaos
        if: always()
        run: |
          kubectl delete chaosengine --all -n chaos-testing
          
      - name: Collect results
        run: |
          ./scripts/collect-experiment-results.sh > results.json
          
      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: resilience-results-${{ github.run_id }}
          path: results.json
          
      - name: Notify on failure
        if: failure()
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "⚠️ Resilience test FAILED: ${{ inputs.experiment }}"
            }
```

### Shift-Left Resilience

```
┌──────────────────────────────────────────────────────────────────┐
│                    SHIFT-LEFT RESILIENCE                          │
├──────────┬──────────────┬────────────────┬──────────────────────┤
│   DEV    │     CI       │    STAGING     │     PRODUCTION       │
├──────────┼──────────────┼────────────────┼──────────────────────┤
│ Unit     │ Integration  │ Chaos          │ Game Days            │
│ tests    │ tests con    │ experiments    │ Continuous           │
│ con      │ Toxiproxy    │ automatizados  │ chaos                │
│ Simmy/   │              │ (LitmusChaos)  │ (Chaos Monkey)       │
│ fault    │ Contract     │                │                      │
│ stubs    │ tests con    │ Full fault     │ Regional             │
│          │ timeouts     │ injection      │ failover             │
│ Timeout  │              │ suite          │ drills               │
│ tests    │ Circuit      │                │                      │
│          │ breaker      │ Game Day       │ Automated            │
│ Retry    │ validation   │ (equipo)       │ blast radius         │
│ logic    │              │                │ monitoring           │
│ tests    │              │                │                      │
└──────────┴──────────────┴────────────────┴──────────────────────┘
```

---

## 13. Ejemplos Prácticos con Código

### 13.1 Test de Resiliencia con k6 + Fault Injection

```javascript
// resilience-test.js - k6 test que valida resiliencia durante fault injection
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

// Métricas custom de resiliencia
const resilienceSuccessRate = new Rate('resilience_success_rate');
const degradedResponses = new Counter('degraded_responses');
const recoveryTime = new Trend('recovery_time_ms');

export const options = {
  scenarios: {
    // Carga constante durante todo el experimento
    constant_load: {
      executor: 'constant-arrival-rate',
      rate: 100,
      timeUnit: '1s',
      duration: '15m',  // 3 min baseline + 7 min chaos + 5 min recovery
      preAllocatedVUs: 50,
      maxVUs: 200,
    },
  },
  thresholds: {
    // Métricas de resiliencia
    'resilience_success_rate': ['rate>0.95'],          // 95% durante caos
    'http_req_duration{phase:chaos}': ['p(95)<3000'],  // 3s P95 durante caos
    'http_req_duration{phase:recovery}': ['p(95)<500'],// 500ms P95 en recovery
  },
};

// Fases del experimento
const PHASES = {
  BASELINE: { start: 0, end: 180 },      // 0-3 min
  CHAOS: { start: 180, end: 600 },        // 3-10 min
  RECOVERY: { start: 600, end: 900 },     // 10-15 min
};

function getCurrentPhase() {
  const elapsed = (__VU > 0) ? (Date.now() - __ENV.START_TIME) / 1000 : 0;
  if (elapsed < PHASES.BASELINE.end) return 'baseline';
  if (elapsed < PHASES.CHAOS.end) return 'chaos';
  return 'recovery';
}

export default function () {
  const phase = getCurrentPhase();
  
  const res = http.get('http://api.example.com/payments', {
    tags: { phase: phase },
    timeout: '10s',
  });
  
  // Evaluar resiliencia según la fase
  const isSuccess = res.status === 200 || res.status === 206; // 206 = degraded OK
  resilienceSuccessRate.add(isSuccess);
  
  if (res.status === 206) {
    degradedResponses.add(1);
  }
  
  // Validaciones por fase
  if (phase === 'baseline') {
    check(res, {
      'baseline: status 200': (r) => r.status === 200,
      'baseline: latency < 500ms': (r) => r.timings.duration < 500,
    });
  } else if (phase === 'chaos') {
    check(res, {
      'chaos: response received': (r) => r.status !== 0,
      'chaos: not server error 5xx': (r) => r.status < 500 || r.status === 503,
      'chaos: latency < 5000ms': (r) => r.timings.duration < 5000,
    });
  } else { // recovery
    check(res, {
      'recovery: status 200': (r) => r.status === 200,
      'recovery: latency < 500ms': (r) => r.timings.duration < 500,
    });
  }
  
  sleep(0.1);
}

// Setup: trigger fault injection at the right time
export function setup() {
  return { startTime: Date.now() };
}
```

### 13.2 Validación de Circuit Breaker

```javascript
// circuit-breaker-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Counter, Rate } from 'k6/metrics';

const circuitBreakerTrips = new Counter('circuit_breaker_trips');
const fastFailRate = new Rate('fast_fail_rate');

export const options = {
  scenarios: {
    trip_circuit_breaker: {
      executor: 'ramping-arrival-rate',
      startRate: 10,
      timeUnit: '1s',
      stages: [
        { duration: '30s', target: 10 },   // Baseline
        { duration: '30s', target: 200 },   // Overload (trip CB)
        { duration: '60s', target: 200 },   // Sustained overload
        { duration: '30s', target: 10 },    // Recovery
        { duration: '30s', target: 10 },    // Verify recovery
      ],
      preAllocatedVUs: 100,
      maxVUs: 500,
    },
  },
};

export default function () {
  const res = http.get('http://api.example.com/downstream-call');
  
  // Detectar circuit breaker abierto
  if (res.status === 503 && res.headers['X-Circuit-Breaker'] === 'OPEN') {
    circuitBreakerTrips.add(1);
    
    // Verificar fast-fail (< 50ms = no esperó al downstream)
    const isFastFail = res.timings.duration < 50;
    fastFailRate.add(isFastFail);
    
    check(res, {
      'CB open: fast fail < 50ms': (r) => r.timings.duration < 50,
      'CB open: fallback body present': (r) => r.body.includes('fallback'),
      'CB open: retry-after header': (r) => r.headers['Retry-After'] !== undefined,
    });
  } else if (res.status === 200) {
    check(res, {
      'CB closed: normal response': (r) => r.status === 200,
      'CB closed: normal latency': (r) => r.timings.duration < 1000,
    });
  }
  
  sleep(0.05);
}
```

### 13.3 Script de Fault Injection Orquestado

```bash
#!/bin/bash
# orchestrate-chaos.sh - Orquestador de experimentos de resiliencia

set -euo pipefail

EXPERIMENT_NAME="${1:-pod-kill}"
NAMESPACE="${2:-staging}"
DURATION="${3:-300}"  # 5 min default
STEADY_STATE_WAIT=120
RECOVERY_WAIT=180

echo "═══════════════════════════════════════════════════"
echo "  CHAOS EXPERIMENT: ${EXPERIMENT_NAME}"
echo "  Namespace: ${NAMESPACE}"
echo "  Duration: ${DURATION}s"
echo "═══════════════════════════════════════════════════"

# 1. Verificar steady state
echo "[$(date +%T)] Phase 1: Verifying steady state..."
if ! ./scripts/verify-steady-state.sh "${NAMESPACE}"; then
  echo "❌ System not in steady state. Aborting."
  exit 1
fi
echo "✅ Steady state confirmed."
sleep ${STEADY_STATE_WAIT}

# 2. Snapshot de métricas pre-chaos
echo "[$(date +%T)] Phase 2: Capturing pre-chaos metrics..."
PRE_METRICS=$(curl -s "http://prometheus:9090/api/v1/query?query=\
  {__name__=~'http_requests_total|http_errors_total|http_duration_seconds'}")
echo "${PRE_METRICS}" > /tmp/pre-chaos-metrics.json

# 3. Inyectar falla
echo "[$(date +%T)] Phase 3: Injecting chaos - ${EXPERIMENT_NAME}..."
kubectl apply -f "chaos-experiments/${EXPERIMENT_NAME}.yaml" -n "${NAMESPACE}"

# 4. Monitorear durante el caos
echo "[$(date +%T)] Phase 4: Monitoring during chaos (${DURATION}s)..."
END_TIME=$(($(date +%s) + DURATION))
ABORT=false

while [ $(date +%s) -lt ${END_TIME} ] && [ "${ABORT}" = "false" ]; do
  # Verificar abort conditions
  ERROR_RATE=$(curl -s "http://prometheus:9090/api/v1/query?query=\
    sum(rate(http_errors_total[1m]))/sum(rate(http_requests_total[1m]))" \
    | jq -r '.data.result[0].value[1]')
  
  if (( $(echo "${ERROR_RATE} > 0.10" | bc -l) )); then
    echo "⚠️  ABORT: Error rate ${ERROR_RATE} exceeds 10% threshold!"
    ABORT=true
  fi
  
  sleep 10
done

# 5. Remover falla
echo "[$(date +%T)] Phase 5: Removing chaos..."
kubectl delete -f "chaos-experiments/${EXPERIMENT_NAME}.yaml" -n "${NAMESPACE}" --ignore-not-found

# 6. Esperar y verificar recuperación
echo "[$(date +%T)] Phase 6: Waiting for recovery (${RECOVERY_WAIT}s)..."
sleep ${RECOVERY_WAIT}

echo "[$(date +%T)] Phase 7: Verifying recovery..."
if ./scripts/verify-steady-state.sh "${NAMESPACE}"; then
  echo "✅ System recovered to steady state."
  RESULT="PASSED"
else
  echo "❌ System did NOT recover to steady state!"
  RESULT="FAILED"
fi

# 7. Generar reporte
echo "[$(date +%T)] Phase 8: Generating report..."
cat << EOF > "reports/${EXPERIMENT_NAME}-$(date +%Y%m%d-%H%M).json"
{
  "experiment": "${EXPERIMENT_NAME}",
  "namespace": "${NAMESPACE}",
  "duration_seconds": ${DURATION},
  "result": "${RESULT}",
  "aborted": ${ABORT},
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

echo "═══════════════════════════════════════════════════"
echo "  RESULT: ${RESULT}"
echo "═══════════════════════════════════════════════════"

[ "${RESULT}" = "PASSED" ] && exit 0 || exit 1
```

---

## 14. Resiliency en Arquitecturas Cloud-Native

### Kubernetes Resilience Patterns

```yaml
# Deployment con todas las buenas prácticas de resiliencia
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service
spec:
  replicas: 3
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0  # Zero-downtime deploys
  template:
    spec:
      # Anti-affinity: no 2 pods en el mismo nodo
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app: payment-service
                topologyKey: kubernetes.io/hostname
      
      # Topology spread: distribuir entre AZs
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels:
              app: payment-service
      
      containers:
        - name: payment
          image: payment-service:v2.1.0
          resources:
            requests:
              cpu: "500m"
              memory: "512Mi"
            limits:
              cpu: "1000m"
              memory: "1Gi"
          
          # Probes para self-healing
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 10
            failureThreshold: 3    # 3 fallas → restart
          
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
            failureThreshold: 2    # 2 fallas → remove from LB
          
          startupProbe:
            httpGet:
              path: /healthz
              port: 8080
            failureThreshold: 30   # 30 × 2s = 60s para arrancar
            periodSeconds: 2

---
# PodDisruptionBudget: mínimo 2 pods siempre activos
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: payment-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: payment-service

---
# HorizontalPodAutoscaler: auto-scale bajo presión
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: payment-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: payment-service
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: "1000"
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 30   # Escalar rápido
      policies:
        - type: Percent
          value: 100
          periodSeconds: 30
    scaleDown:
      stabilizationWindowSeconds: 300  # Des-escalar lento (5 min)
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
```

### Service Mesh Resilience (Istio)

```yaml
# VirtualService con retry, timeout y circuit breaker
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: payment-service
spec:
  hosts:
    - payment-service
  http:
    - route:
        - destination:
            host: payment-service
      timeout: 5s
      retries:
        attempts: 3
        perTryTimeout: 2s
        retryOn: "5xx,reset,connect-failure,retriable-4xx"

---
# DestinationRule con circuit breaker y connection pool
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: payment-service
spec:
  host: payment-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
        connectTimeout: 30ms
      http:
        h2UpgradePolicy: DEFAULT
        http1MaxPendingRequests: 100
        http2MaxRequests: 1000
        maxRequestsPerConnection: 10
        maxRetries: 3
    outlierDetection:  # Circuit breaker
      consecutive5xxErrors: 5
      interval: 10s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
      minHealthPercent: 50
```

### Multi-Region Resilience

```
┌────────────────────────────────────────────────────────────────┐
│                    MULTI-REGION ARCHITECTURE                    │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│                    ┌──────────────┐                            │
│                    │  Global DNS  │                            │
│                    │ (Route 53)   │                            │
│                    └──────┬───────┘                            │
│                           │                                    │
│              ┌────────────┼────────────┐                      │
│              │            │            │                       │
│     ┌────────▼───┐  ┌────▼────┐  ┌───▼────────┐             │
│     │ US-EAST-1  │  │ EU-WEST │  │ AP-SOUTH   │             │
│     │ (Primary)  │  │ (Active)│  │ (Active)   │             │
│     ├────────────┤  ├─────────┤  ├────────────┤             │
│     │ App (3 AZ) │  │App(3 AZ)│  │ App (3 AZ) │             │
│     │ DB Primary │  │DB Replica│  │ DB Replica │             │
│     │ Cache      │  │ Cache   │  │ Cache      │             │
│     └────────────┘  └─────────┘  └────────────┘             │
│                                                                │
│  FALLA REGIÓN US-EAST-1:                                      │
│  1. Health check falla (30s)                                  │
│  2. DNS failover a EU-WEST (60s TTL)                         │
│  3. EU-WEST promueve DB replica a primary                    │
│  4. Tráfico US redistribuido a EU-WEST + AP-SOUTH            │
│  5. RTO total: < 3 minutos                                   │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

**Qué validar en Resiliency Testing multi-region:**
- DNS failover timing (< 60s)
- Database promotion timing
- Data consistency post-failover (RPO)
- Client retry behavior durante failover
- Cache warming en región de destino
- Capacidad de la región receptora para absorber tráfico adicional

---

## 15. Antipatrones y Errores Comunes

### ❌ Antipatrón 1: "Big Bang Chaos"
```
MALO: Inyectar 5 fallas simultáneas en producción sin experiencia previa
BUENO: Empezar con 1 falla simple en staging, escalar gradualmente
```

### ❌ Antipatrón 2: "Chaos sin Observabilidad"
```
MALO: Inyectar fallas sin dashboards ni alertas configuradas
BUENO: Primero observabilidad completa, LUEGO chaos
```

### ❌ Antipatrón 3: "Fire and Forget"
```
MALO: Ejecutar experimento y no analizar resultados
BUENO: Cada experimento → análisis → action items → validación
```

### ❌ Antipatrón 4: "Solo infraestructura"
```
MALO: Solo matar pods/instancias
BUENO: También probar fallas de aplicación (timeouts, datos corruptos, slow responses)
```

### ❌ Antipatrón 5: "Chaos Cowboy"
```
MALO: Un ingeniero ejecuta chaos sin avisar a nadie
BUENO: Comunicación previa, safety officer, abort conditions claras
```

### ❌ Antipatrón 6: "Retry Storm"
```
MALO: Todos los clientes reintentando simultáneamente sin backoff
BUENO: Exponential backoff + jitter + circuit breaker
```

### ❌ Antipatrón 7: "Timeout Chain Violation"
```
MALO: 
  API Gateway timeout: 5s
  Service A timeout: 10s  ← MAYOR que el gateway!
  Service B timeout: 15s  ← Aún mayor!
  
BUENO:
  API Gateway timeout: 10s
  Service A timeout: 5s
  Service B timeout: 2s
```

### ❌ Antipatrón 8: "Health Check Lie"
```
MALO: /health retorna 200 aunque el servicio no puede procesar requests
BUENO: /health verifica dependencias reales (DB, cache, downstream)
```

---

## 16. Checklist de Implementación

### Pre-requisitos (antes de hacer Resiliency Testing)

- [ ] **Observabilidad completa:** Logs, métricas, traces configurados
- [ ] **Alertas calibradas:** Alertas que detectan degradación (no solo caídas)
- [ ] **Runbooks actualizados:** Procedimientos documentados para cada escenario
- [ ] **Baseline establecido:** Métricas de estado estable documentadas
- [ ] **Equipo capacitado:** El equipo entiende chaos engineering
- [ ] **Stakeholders informados:** Management aprueba el enfoque

### Implementación Progresiva

```
□ MES 1: Foundations
  □ Definir steady-state hypothesis para servicios críticos
  □ Configurar Toxiproxy para tests de integración
  □ Agregar circuit breakers a todas las dependencias externas
  □ Implementar health checks profundos (liveness + readiness)
  □ Primer experimento manual en staging

□ MES 2: Automation
  □ Crear suite de chaos experiments automatizados
  □ Integrar resiliency tests en pipeline CI/CD (staging)
  □ Configurar LitmusChaos / Chaos Mesh en cluster staging
  □ Primer Game Day con equipo reducido
  □ Documentar resultados y crear action items

□ MES 3: Expansion
  □ Expandir a todos los servicios críticos
  □ Primer experimento en pre-producción
  □ Introducir fallas de dependencia (no solo infra)
  □ Automatizar reportes de resiliencia score
  □ Game Day con equipo completo

□ MES 4+: Production
  □ Chaos experiments regulares en producción (ventanas seguras)
  □ Continuous chaos (Chaos Monkey-style)
  □ Multi-failure scenarios
  □ Cross-team Game Days
  □ Resiliencia como parte del Definition of Done
```

### KPIs de Éxito del Programa

| KPI | Target | Cómo medir |
|-----|--------|------------|
| Experimentos ejecutados/mes | > 10 | Automation platform |
| % servicios con chaos coverage | > 80% | Inventario vs. experiments |
| MTTR improvement | -50% YoY | Incident metrics |
| Incidentes prevenidos | > 3/quarter | Post-mortem attribution |
| Game Days ejecutados | 1/month | Calendar |
| Resilience Score promedio | > 80/100 | Score card |

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
