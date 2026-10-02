# Endurance, Spike, Volume y Scalability Testing

## 1. Endurance Testing (Soak Testing)

### Definición
El **Endurance Testing** (también llamado **Soak Testing**) somete al sistema a una carga normal-moderada durante un **período extendido** (horas o días) para detectar problemas que solo se manifiestan con el tiempo.

### ¿Por qué es necesario?
Muchos problemas de rendimiento no aparecen en tests de 1-2 horas:
- Memory leaks que tardan horas en acumularse
- Connection leaks que agotan pools gradualmente
- File handle leaks
- Log files que llenan discos
- Cache invalidation issues
- Thread leaks
- Database connection aging

### Diseño del Endurance Test

```yaml
endurance_test:
  load: "70-80% of verified capacity"  # NO máxima, sino típica
  duration: "8-72 hours"  # Mínimo 8h, ideal 24-72h
  
  monitoring_focus:
    - "Memory trend (should be flat)"
    - "Response time trend (should be flat)"
    - "Active threads over time"
    - "Open connections over time"
    - "Disk space usage"
    - "GC frequency and duration"
    - "Error rate trend"
    
  success_criteria:
    memory_growth: "< 5% total increase over test duration"
    response_time_degradation: "< 10% increase from hour 1 to hour N"
    error_rate: "No upward trend"
    disk_space: "Sufficient for full duration"
    gc_pauses: "No increasing frequency or duration"
```

### Patrones de detección

#### Memory Leak Pattern
```
Memory Usage (MB)
 4000 ┤                                          ╱
 3500 ┤                                      ╱──┘
 3000 ┤                                 ╱───┘
 2500 ┤                           ╱────┘
 2000 ┤                     ╱────┘
 1500 ┤               ╱────┘
 1000 ┤─────────╱────┘           ← Sawtooth pattern (GC)
  500 ┤────────┘                     pero con baseline creciente
    0 ┤
      └──────────────────────────────────────────────→ Time
      0h    4h    8h   12h   16h   20h   24h

PROBLEMA: Baseline de memoria crece continuamente
CAUSA PROBABLE: Memory leak (objetos no liberados)
```

#### Healthy Pattern (sin leak)
```
Memory Usage (MB)
 2000 ┤   ╱╲  ╱╲  ╱╲  ╱╲  ╱╲  ╱╲  ╱╲  ╱╲  ╱╲  ╱╲
 1500 ┤  ╱  ╲╱  ╲╱  ╲╱  ╲╱  ╲╱  ╲╱  ╲╱  ╲╱  ╲╱  ╲
 1000 ┤─╱
  500 ┤╱
    0 ┤
      └──────────────────────────────────────────────→ Time
      0h    4h    8h   12h   16h   20h   24h

OK: GC opera normalmente, baseline estable
```

#### Connection Leak Pattern
```
DB Connections
 200 ┤ (Pool max)──────────────────────────■■■■■■
 180 ┤                              ╱─────┘
 160 ┤                        ╱────┘
 140 ┤                  ╱────┘
 120 ┤            ╱────┘
 100 ┤      ╱────┘
  80 ┤╱────┘
     └──────────────────────────────────────────→ Time
     
PROBLEMA: Connections crecen sin liberarse
RESULTADO: Pool exhaustion → timeouts → errors
```

### Análisis de Endurance Test

| Síntoma | Posible causa | Investigación |
|---------|--------------|---------------|
| Memoria crece linealmente | Memory leak | Heap dump analysis, profiler |
| Response time crece gradualmente | Resource exhaustion | Thread dump, connection analysis |
| GC pauses cada vez más largos | Heap pressure | GC log analysis, heap sizing |
| Errores aparecen después de N horas | Pool exhaustion | Connection/thread pool monitoring |
| Disk space decrece | Logs, temp files | Log rotation, temp cleanup |
| Throughput decrece gradualmente | Thread starvation | Thread dump analysis |

---

## 2. Spike Testing

### Definición
El **Spike Testing** evalúa la capacidad del sistema para manejar **cambios abruptos y dramáticos** en la carga, tanto incrementos como decrementos súbitos.

### Escenarios reales de spikes
- **Black Friday / Cyber Monday**: 10-100x tráfico normal en segundos
- **Breaking news**: Pico masivo a sitio de noticias
- **Flash sales**: Apertura de venta limitada
- **Marketing campaigns**: Envío de email masivo con link
- **Ticket sales**: Venta de entradas para evento popular
- **API batch processing**: Job nocturno que genera pico

### Diseño del Spike Test

```yaml
spike_test:
  scenarios:
    
    single_spike:
      baseline: 200 users
      spike_to: 3000 users
      spike_duration: "30 seconds"  # Incremento en 30s
      hold_at_spike: "5 minutes"
      recover_to: 200 users
      recover_duration: "30 seconds"
      
    multiple_spikes:
      baseline: 200 users
      spikes:
        - { to: 2000, hold: "3 min", at: "5 min" }
        - { to: 1000, hold: "3 min", at: "12 min" }
        - { to: 3000, hold: "3 min", at: "19 min" }
        - { to: 500, hold: "3 min", at: "26 min" }
      
    exponential_spike:
      baseline: 100 users
      growth: "double every 30 seconds"
      max: 5000 users
      hold_at_max: "2 minutes"
      drop_to: 100 users  # Instantáneo
```

### Patrones de Spike

```
Spike Pattern 1: Single Spike
Users
3000 ┤       ┌────────┐
     │       │        │
2000 ┤       │        │
     │       │        │
1000 ┤       │        │
     │       │        │
 200 ┤───────┘        └──────────
     └────────────────────────────→ Time
         ↑ Spike    ↑ Recovery

Spike Pattern 2: Multiple Spikes (Wave)
Users
3000 ┤              ┌──┐
2000 ┤  ┌──┐       │  │
1000 ┤  │  │  ┌──┐ │  │  ┌──┐
 200 ┤──┘  └──┘  └─┘  └──┘  └──
     └────────────────────────────→ Time

Spike Pattern 3: Spike and Sustain
Users
3000 ┤       ┌────────────────────
     │       │
2000 ┤       │
     │       │
1000 ┤       │
     │       │
 200 ┤───────┘
     └────────────────────────────→ Time
```

### Métricas clave en Spike Testing

| Métrica | Qué medir | Aceptable |
|---------|-----------|-----------|
| **Time to respond to spike** | Tiempo desde spike hasta auto-scaling | < 2-3 min |
| **Error rate during spike** | % errores en primeros 30-60s | < 5% |
| **Recovery time** | Tiempo para volver a baseline post-spike | < 5 min |
| **Data loss** | Transacciones perdidas durante spike | 0 |
| **Queue depth** | Acumulación durante el spike | Should drain |
| **User experience** | Degradación percibida | Graceful degradation |

### Validaciones de auto-scaling

```
Timeline de un spike bien manejado:
T+0s:    Spike begins (200 → 3000 users)
T+15s:   Auto-scaler detects increased load
T+30s:   New instances requested
T+90s:   New instances ready and serving traffic
T+120s:  Load distributed, response times improving
T+180s:  Full recovery, all SLAs met

Timeline de un spike mal manejado:
T+0s:    Spike begins (200 → 3000 users)
T+15s:   Existing servers overwhelmed
T+30s:   Connection queues full
T+45s:   Timeouts begin
T+60s:   Error rate > 50%
T+120s:  Auto-scaler detects (too late)
T+300s:  New instances ready (users already gone)
```

---

## 3. Volume Testing

### Definición
El **Volume Testing** evalúa el comportamiento del sistema cuando procesa **grandes volúmenes de datos**, independientemente del número de usuarios concurrentes.

### Foco principal
- Rendimiento con datasets masivos
- Eficiencia de queries con tablas grandes
- Comportamiento de índices a gran escala
- Import/export de datos masivos
- Batch processing performance
- Report generation con mucho data

### Diseño del Volume Test

```yaml
volume_test:
  scenarios:
    
    large_database:
      description: "Test con base de datos a escala de producción"
      data_volumes:
        users: 5_000_000
        orders: 50_000_000
        products: 1_000_000
        transactions: 200_000_000
      operations:
        - "Search across 50M orders"
        - "Generate monthly report (10M records)"
        - "Paginate through results"
        - "Dashboard aggregations"
      
    data_ingestion:
      description: "Ingestión masiva de datos"
      volume: "1 million records"
      rate: "10,000 records/second"
      validations:
        - "All records ingested without loss"
        - "Processing time within SLA"
        - "No memory overflow during processing"
        
    file_processing:
      description: "Procesamiento de archivos grandes"
      files:
        - { type: "CSV", size: "5 GB", records: 50_000_000 }
        - { type: "JSON", size: "2 GB", records: 10_000_000 }
      operations:
        - "Parse and validate"
        - "Transform and load"
        - "Generate summary"
```

### Métricas específicas de Volume Testing

| Métrica | Descripción |
|---------|-------------|
| Query time vs data volume | ¿Linear, logarithmic, or exponential? |
| Index effectiveness | ¿Los índices siguen siendo eficientes? |
| Pagination performance | ¿OFFSET grandes son problemáticos? |
| Aggregation time | ¿SUMs, COUNTs, GROUPs escalan? |
| Storage growth | ¿Crecimiento predecible? |
| Backup/Restore time | ¿Factible en ventana de mantenimiento? |

### Problemas comunes detectados

```
1. OFFSET pagination ineficiente:
   SELECT * FROM orders ORDER BY date LIMIT 20 OFFSET 5000000
   → Full table scan hasta OFFSET, luego descarta
   
   SOLUCIÓN: Cursor-based pagination
   SELECT * FROM orders WHERE id > last_seen_id ORDER BY id LIMIT 20

2. COUNT(*) en tablas grandes:
   SELECT COUNT(*) FROM orders WHERE status = 'pending'
   → Full scan si no hay índice parcial
   
   SOLUCIÓN: Approximate counts, materialized views

3. N+1 queries con datasets grandes:
   Para cada orden, consultar items → 50M queries adicionales
   
   SOLUCIÓN: JOINs, batch loading, eager loading

4. Report generation timeout:
   Generar reporte de 12 meses con 200M transacciones
   
   SOLUCIÓN: Pre-aggregation, CQRS, async report generation
```

---

## 4. Scalability Testing

### Definición
El **Scalability Testing** determina la capacidad del sistema para **escalar eficientemente** cuando se agregan más recursos (horizontal o vertical) en respuesta a mayor carga.

### Tipos de escalamiento

```
ESCALAMIENTO VERTICAL (Scale Up)
├── Más CPU → ¿Throughput crece proporcionalmente?
├── Más RAM → ¿Se aprovecha la memoria adicional?
└── Mejor Disco → ¿I/O mejora proporcionalmente?

ESCALAMIENTO HORIZONTAL (Scale Out)
├── Más instancias de app → ¿Carga se distribuye?
├── Read replicas de DB → ¿Queries se balancean?
├── Más workers → ¿Processing se paraleliza?
└── Más nodos de cache → ¿Hit ratio se mantiene?
```

### Diseño del Scalability Test

```yaml
scalability_test:
  
  horizontal_scaling:
    configurations:
      - { instances: 1, users: 500, expected_tps: 200 }
      - { instances: 2, users: 1000, expected_tps: 380 }  # ~95% efficiency
      - { instances: 4, users: 2000, expected_tps: 720 }  # ~90% efficiency
      - { instances: 8, users: 4000, expected_tps: 1360 } # ~85% efficiency
    
    measure:
      - "Throughput per instance"
      - "Response time consistency"
      - "Resource utilization per instance"
      - "Scaling efficiency ratio"
      
  vertical_scaling:
    configurations:
      - { cpu: 2, ram: "4GB", users: 300 }
      - { cpu: 4, ram: "8GB", users: 600 }
      - { cpu: 8, ram: "16GB", users: 1200 }
    
    measure:
      - "Throughput improvement per resource unit"
      - "Diminishing returns point"
      - "Maximum effective vertical scale"
```

### Métricas de escalabilidad

#### Scaling Efficiency
```
Efficiency = (Actual_TPS_at_N_instances) / (TPS_1_instance × N)

Ejemplo:
1 instance:  200 TPS (baseline)
2 instances: 380 TPS → Efficiency = 380/(200×2) = 95% ✅
4 instances: 720 TPS → Efficiency = 720/(200×4) = 90% ✅
8 instances: 1200 TPS → Efficiency = 1200/(200×8) = 75% ⚠️

→ Rendimiento decreciente a partir de 4 instancias
→ Investigar: shared resources, contention, synchronization
```

#### Amdahl's Law
```
Speedup_max = 1 / (s + (1-s)/N)

Donde:
s = fracción del trabajo que es serial (no paralelizable)
N = número de procesadores/instancias

Si s = 10% (90% paralelizable):
N=2:  Speedup = 1.82x (91% efficiency)
N=4:  Speedup = 3.08x (77% efficiency)
N=8:  Speedup = 4.71x (59% efficiency)
N=16: Speedup = 6.40x (40% efficiency)
N=∞:  Speedup = 10x (máximo teórico)

CONCLUSIÓN: Siempre hay un límite de escalamiento
           determinado por la porción serial del trabajo.
```

### Patrones de escalabilidad

```
Throughput vs Instances:

TPS
2000 ┤                           ─── Ideal (linear)
     │                      ╱───
1600 ┤                 ╱───╱─── Actual
     │            ╱───╱
1200 ┤       ╱───╱
     │  ╱───╱
 800 ┤─╱───╱
     │╱──╱
 400 ┤──╱
     │╱
   0 ┤
     └────────────────────────────→ Instances
     1    2    3    4    5    6    7    8

Gap entre ideal y actual = overhead de escalamiento
(coordination, serialization, network, shared resources)
```

### Bottlenecks de escalabilidad comunes

| Bottleneck | Síntoma | Solución |
|-----------|---------|----------|
| Database single writer | TPS no crece con más app servers | Sharding, CQRS |
| Shared state/sessions | Instancias no son independientes | Stateless design, distributed cache |
| Distributed locks | Contención crece con instancias | Optimistic locking, reduce lock scope |
| Network overhead | Latencia inter-nodo | Co-location, message batching |
| Shared disk | I/O no escala | Distributed storage, local caches |
| DNS/Load balancer | Single point of congestion | Multiple LBs, DNS round-robin |

---

## Resumen Comparativo

| Tipo | Pregunta que responde | Duración | Carga | Foco |
|------|----------------------|----------|-------|------|
| **Endurance** | "¿Se degrada con el tiempo?" | 8-72 horas | Normal (70-80%) | Memory leaks, resource leaks |
| **Spike** | "¿Maneja picos súbitos?" | 30-60 min | Picos extremos | Recovery, auto-scaling |
| **Volume** | "¿Maneja grandes datos?" | 1-4 horas | Normal users, big data | Queries, storage, processing |
| **Scalability** | "¿Escala eficientemente?" | 2-6 horas | Variable, con más recursos | Eficiencia de scaling |

---

*Documento de referencia - Performance Test Life Cycle*
*Última actualización: Junio 2026*
