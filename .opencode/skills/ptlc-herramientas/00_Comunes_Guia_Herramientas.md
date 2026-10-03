# 🔧 Común — CI/CD, Troubleshooting, Mejores Prácticas y Proyecto de Referencia

Versión canónica única de las secciones que las guías `03`-`06` repetían casi idénticas; las guías apuntan aquí y conservan solo sus deltas. Herramientas: **k6**, **Apache JMeter**, **Gatling CE**, **Locust**.

## Mapa de secciones

Usa `grep -n "^## "` para localizar cada sección y lee solo la que necesites en lugar de cargar el archivo entero:
**1.** CI/CD · **2.** Troubleshooting (síntomas, logging, tuning) · **3.** Mejores prácticas y antipatrones · **4.** Proyecto de referencia.

---

## 1. Integración con CI/CD

### 1.1 Esqueleto GitHub Actions (matriz de herramientas)

Un único workflow con `matrix.tool`; cada runner instala su tool, ejecuta el test parametrizado y falla el job si los umbrales se incumplen.

```yaml
# .github/workflows/performance-test.yml
name: Performance Test
on:
  pull_request: { branches: [main] }
  schedule: [{ cron: '0 5 * * 1-5' }]          # Lun-Vie 5 AM
  workflow_dispatch:
    inputs:
      tool:     { type: choice, options: [k6, jmeter, gatling, locust], default: k6 }
      users:    { description: 'Users / arrival rate', default: '100' }
      duration: { description: 'Test duration', default: '300s' }
jobs:
  load-test:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - name: Install tool
        run: bash ci/install-${{ inputs.tool }}.sh            # comandos en 1.2
      - name: Run load test
        run: bash ci/run-${{ inputs.tool }}.sh ${{ inputs.users }} ${{ inputs.duration }}
      - name: Check thresholds (quality gate)
        run: python scripts/check_thresholds.py --p95-max 1000 --error-rate-max 1.0 --min-rps 50
      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v4
        with: { name: perf-results-${{ inputs.tool }}-${{ github.run_id }}, path: results/ }
```

El mismo job puede declararse como matriz (`strategy: { fail-fast: false, matrix: { tool: [k6, jmeter, gatling, locust] } }`) para correr las 4 herramientas en paralelo; cada rama instala/ejecuta según la tabla 1.2.

### 1.2 Comandos por herramienta

| Herramienta | Instalar | Ejecutar (CI, no interactivo) | Cargar objetivo | Duración | Reporte / artefacto | Quality gate |
|---|---|---|---|---|---|---|
| **k6** | binario único (tar.gz o apt) | `k6 run tests/load.js` | `-e TARGET_HOST=…` | `options` o `--duration` | `--out json=results/output.json`; dashboards Grafana | `thresholds` + exit code |
| **JMeter** | tarball + `PluginsManagerCMD` | `jmeter -n -t test.jmx -l r.jtl` | `-Jtarget.host=…` | `-Jtest.duration=…` | `-e -o results/dashboard/` (HTML) | assertions + `check_jmeter_results.py` |
| **Gatling CE** | `gatling-maven-plugin` o Gradle | `mvn gatling:test -Dgatling.simulationClass=…` | `-DtargetHost=…` | `-Dduration=…` | `target/gatling/**/index.html` | assertions (fallan el build) |
| **Locust** | `pip install locust` + `requirements.txt` | `locust -f locustfile.py --headless` | `--host …` | `--run-time 5m` | `--csv results/perf --html results/report.html` | `--exit-code-on-error 1` |

Extras: JVM `setup-java` 17 con `-Xmx4g` (JMeter) o `cache: maven` (Gatling); Python 3.11 con `cache: pip` (Locust); k6 no requiere runtime. Publicación: k6 y Locust comentan el PR (`github-script`), JMeter sube el dashboard HTML como artifact, Gatling publica en GitHub Pages (`peaceiris/actions-gh-pages`).

### 1.3 Detalles de workflow por herramienta

Lo que cambia y no cabe en el esqueleto común:

| Detalle | k6 | JMeter | Gatling CE | Locust |
|---|---|---|---|---|
| Workflow / job id | `Performance Tests (k6)` / `k6-test` | `Performance Test (JMeter)` / `jmeter-test` | `Performance Test` / `gatling-test` | `Performance Test` / `load-test` |
| Branches en PR | `[main]` | — | `[main, develop]` | `[main]` |
| Cron | `0 5 * * 1-5` | `0 5 * * 1-5` | `0 4 * * 1-5` | `0 6 * * 1-5` |
| Inputs `workflow_dispatch` | `test_type` (choice: smoke, load, stress, spike; default load) | `users` (100), `duration` (600) | `users` (50, "target users/s"), `duration` (300 s) | `users` (100), `duration` (5m) |
| Artifact | `k6-results-${{ github.run_id }}` | `jmeter-report-${{ github.run_id }}` (`results/dashboard/`) | `gatling-report-${{ github.run_id }}` (`target/gatling/**/index.html`, 30 días) | `performance-results` |

```bash
# Instalar (el runner no trae la tool)
k6:     curl -sL https://github.com/grafana/k6/releases/download/v0.57.0/k6-v0.57.0-linux-amd64.tar.gz | tar xvz && sudo mv k6-v0.57.0-linux-amd64/k6 /usr/local/bin/   # o apt+keyring: gpg --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69, repo dl.k6.io/deb
jmeter: wget -q https://dlcdn.apache.org/jmeter/binaries/apache-jmeter-5.6.3.tgz && tar -xzf apache-jmeter-5.6.3.tgz && export JMETER_HOME=$PWD/apache-jmeter-5.6.3 && wget -O $JMETER_HOME/lib/ext/jmeter-plugins-manager-1.10.jar https://jmeter-plugins.org/get/ && $JMETER_HOME/bin/PluginsManagerCMD.sh install jpgc-casutg,jpgc-tst
locust: pip install -r requirements-perf.txt          # gatling: actions/setup-java@v4 (temurin 17, cache maven)
# Ejecutar ($HOST=${{ secrets.STAGING_URL }}, $N=users, $T=duration; k6 puede anteponer smoke: k6 run --vus 5 --duration 30s tests/smoke.js)
k6:      k6 run tests/load.js -e TARGET_HOST=$HOST --out json=results/output.json
jmeter:  jmeter -n -t test-plans/load_test.jmx -l results/results.jtl -e -o results/dashboard/ -Jtarget.host=$HOST -Jtest.users=$N -Jtest.duration=$T -Xmx4g
gatling: mvn gatling:test -Pload -DtargetHost=$HOST -Dusers=$N -Dduration=$T
locust:  locust -f src/locustfile.py --headless --host $HOST -u $N -r 10 --run-time $T --csv results/perf --html results/report.html --exit-code-on-error 1
```

### 1.4 Jenkins Pipeline (Gatling)

```groovy
// Jenkinsfile
pipeline {
    agent { label 'performance' }
    parameters {
        string(name: 'USERS', defaultValue: '100', description: 'Target users')
        string(name: 'DURATION', defaultValue: '600', description: 'Duration (seconds)')
        choice(name: 'ENVIRONMENT', choices: ['staging', 'preprod'], description: 'Target env')
    }
    stages {
        stage('Run Gatling') {
            steps {
                sh "mvn gatling:test -Dgatling.simulationClass=simulations.LoadTestSimulation -Dusers=${params.USERS} -Dduration=${params.DURATION} -DtargetHost=${env."${params.ENVIRONMENT}_URL"}"
            }
            post { always { gatlingArchive() } }   // Jenkins Gatling plugin
        }
    }
}
```

### 1.5 Maven profiles por tipo de test (Gatling)

`pom.xml` define un `<profile>` por tipo de test (properties `gatling.simulationClass`, `users`, `duration`):

| Profile | `gatling.simulationClass` | users | duration |
|---|---|---|---|
| smoke | `simulations.SmokeTestSimulation` | 5 | 60 |
| load | `simulations.LoadTestSimulation` | 100 | 1800 |
| stress | `simulations.StressTestSimulation` | 500 | 600 |
| soak | `simulations.SoakTestSimulation` | 50 | 14400 |

Ejecutar: `mvn gatling:test -Psmoke|load|stress|soak [-DtargetHost=…]` (p. ej. `mvn gatling:test -Pstress -DtargetHost=https://staging.example.com`).

### 1.6 Docker Compose local (k6 + InfluxDB + Grafana)

```yaml
version: '3.8'
services:
  k6:
    image: grafana/k6:latest
    volumes: [./tests:/scripts, ./data:/data, ./results:/results]
    environment: [TARGET_HOST=http://app:8080, K6_OUT=influxdb=http://influxdb:8086/k6]
    command: run /scripts/load.js
    depends_on: [influxdb, grafana]
  influxdb:
    image: influxdb:1.8
    ports: ["8086:8086"]
    environment: [INFLUXDB_DB=k6]
  grafana:
    image: grafana/grafana:latest
    ports: ["3000:3000"]
    environment: [GF_AUTH_ANONYMOUS_ENABLED=true, GF_AUTH_ANONYMOUS_ORG_ROLE=Admin]
    volumes: [./grafana/dashboards:/var/lib/grafana/dashboards, ./grafana/provisioning:/etc/grafana/provisioning]
```

### 1.7 Quality gate (check_thresholds.py)

Vive fuera de la herramienta para que el resultado sea comparable entre las 4. Para Locust el input es el CSV de stats; para JMeter, el JTL (`scripts/check_jmeter_results.py` con `--p95-max 2000 --error-max 1.0`).

```python
#!/usr/bin/env python3
"""check_thresholds.py — exit 1 si el CSV agregado rompe los umbrales."""
import csv, sys, argparse

def check(csv_path, p95_max, err_max, min_rps):
    fails = []
    for row in csv.DictReader(open(csv_path)):
        if row["Name"] != "Aggregated": continue
        p95 = float(row.get("95%", 0))
        total, bad = int(row.get("Request Count", 0)), int(row.get("Failure Count", 0))
        err = bad / total * 100 if total else 0
        rps = float(row.get("Requests/s", 0))
        if p95 > p95_max: fails.append(f"❌ P95 {p95:.0f}ms > {p95_max}ms")
        if err > err_max: fails.append(f"❌ Error rate {err:.2f}% > {err_max}%")
        if rps < min_rps: fails.append(f"❌ RPS {rps:.1f} < {min_rps}")
    if fails:
        print("\n🚨 THRESHOLDS VIOLATED:"); [print("  "+f) for f in fails]; sys.exit(1)
    print("\n✅ All performance thresholds passed!")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--csv", required=True)
    p.add_argument("--p95-max", type=float, default=1000)
    p.add_argument("--error-rate-max", type=float, default=1.0)
    p.add_argument("--min-rps", type=float, default=50)
    a = p.parse_args(); check(a.csv, a.p95_max, a.error_rate_max, a.min_rps)
```

---

## 2. Debugging y Troubleshooting

### 2.1 Síntomas, causas y comprobaciones

| Síntoma | Causa probable | Comprobación / solución | Herramienta(s) |
|---|---|---|---|
| Throughput 0 o muy bajo | `wait_time` alto, tasks bloqueantes, generador saturado | ejecutar con 1 usuario y mirar CPU/RAM del runner | Todas |
| CPU 100% en el generador | demasiados VUs para una instancia o código CPU-heavy | `-u`/`rate` por core; más workers o distribuir; Locust `FastHttpUser`; k6 bajar `preAllocatedVUs`/`maxVUs` o `--execution-segment` | Todas (Locust, k6) |
| Errores de conexión / `Connection reset` / `ConnectionError` / Max retries | pool o timeout agotado, SUT saturado | subir pool (`http.MaxConnections`; Locust `HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=0)`) y timeout | Todas |
| Memoria crece sin parar / OOM | acumular datos por VU o guardar response bodies | colecciones acotadas: `SharedArray` (k6), `deque(maxlen=)` (Locust); `-Xmx4g` (Gatling/JMeter); `response_data=false` | Todas |
| Checks fallan en cascada / variables vacías | correlación rota: un extractor falló y la variable va vacía | loggear la primera respuesta; Results Tree (JMeter); `exitHereIfFailed`/`doIf(session.contains("token"))` (Gatling) | JMeter, Gatling, k6, Locust |
| "Feeder/datos agotados" | `queue()` sin más datos o ShareMode mal configurado | feeders `.circular()` (Gatling); revisar scope/ShareMode (JMeter) | Gatling, JMeter |
| Resultados lentos / throughput no alcanza | listeners gráficos activos o threads insuficientes | deshabilitar View Results Tree; subir threads o Arrivals TG | JMeter |
| `dial tcp: lookup … no such host` / Request timeout | DNS/host incorrecto o servidor lento | verificar host/DNS; subir timeout (options k6; `requestTimeout` Gatling) | k6, Gatling |
| `open()` fuera de init / `MaxVUs reached` / dropped iterations | `open()` dentro de `default`; SUT más lento que la rate | mover lectura a init; subir `maxVUs`/ajustar rate | k6 |
| "All users are waiting" / `time.sleep` bloquea el greenlet | `wait_time` alto, tasks que no retornan o sleep no cooperativo | revisar `wait_time`/bloqueos; `from gevent import sleep` | Locust |
| "Session attribute not found: token" / `Connection refused` | un check no guardó el valor; target o puerto erróneo | `exitHereIfFailed`/`doIf`; verificar host/port | Gatling |
| HTTP debug | — | `k6 run --http-debug="full"`; `--verbose` | k6 |
| Depurar con 1 usuario | — | k6 `k6 run --vus 1 --iterations 1`, `k6 inspect` (solo sintaxis); JMeter `-Jusers=1 -Jjmeterengine.force.system.exit=true`; Gatling `mvn gatling:test -Dusers=1 -Dduration=30`; Locust `-u 1 -r 1 --run-time 30s --loglevel DEBUG`, `python -m pdb -c continue locustfile.py` | Todas |

### 2.2 Logging (solo para debug, nunca en el hot path)

```python
# Locust
import logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)   # silenciar libraries
logging.getLogger("requests").setLevel(logging.WARNING)
# en la task: logger.error(f"status={resp.status_code} body={resp.text[:200]} headers={dict(resp.headers)}")
```

```xml
<!-- Gatling: src/test/resources/logback-test.xml (activar response logging SOLO para debug) -->
<logger name="io.gatling" level="WARN"/>
<logger name="io.gatling.http.engine.response" level="DEBUG"/>
<logger name="simulations" level="DEBUG"/>
```

```properties
# JMeter: user.properties - reducir logging
log_level.jmeter=WARN
log_level.jmeter.engine=WARN
```

Debug de sesión en Gatling (solo local, nunca bajo carga): `.exec(session -> { session.asMap().forEach((k,v) -> System.out.println(k+" = "+v)); return session; })` y avisar si falta un valor con `.doIf(session -> !session.contains("token")).then(exec(session -> session.markAsFailed()))`.

### 2.3 Tuning del generador de carga

```bash
# Gatling / JVM
export JAVA_OPTS="-server -Xms2g -Xmx4g -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxInlineLevel=20 -XX:MaxTrivialSize=12 -XX:-UseBiasedLocking -XX:+OptimizeStringConcat"
mvn gatling:test -DargLine="-Xms2g -Xmx4g -XX:+UseG1GC"
```

```properties
# JMeter: user.properties - rendimiento
CookieManager.save.cookies=false
CookieManager.check.cookies=false
httpclient4.retrycount=0
jmeter.save.saveservice.output_format=csv
jmeter.save.saveservice.response_data=false
jmeter.save.saveservice.response_data.on_error=false
jmeter.save.saveservice.url=false
jmeter.save.saveservice.requestHeaders=false
jmeter.save.saveservice.responseHeaders=false
jmeter.save.saveservice.samplerData=false
```

- **k6**: un solo binario; si se satura, reduce `preAllocatedVUs`/`maxVUs` o reparte con `--execution-segment`.
- **Locust**: más workers (`--processes`), `FastHttpUser` para HTTP y nada de CPU-heavy en tasks.

---

## 3. Mejores Prácticas y Antipatrones

Las prácticas y antipatrones son transversales a las 4 herramientas; los detalles propios de cada una van anotados inline.

### 3.1 Prácticas

1. **Umbrales/SLOs siempre declarados**: el test debe fallar solo, sin análisis manual posterior.
2. **Modo no interactivo** en CI: `--headless` (Locust), `-n` (JMeter), `mvn gatling:test`, `k6 run`.
3. **Think time realista** basado en producción; nunca 0.
4. **Ramp-up explícito**; un spike instantáneo no es un test de carga.
5. **Parametrizar objetivo y carga** por CLI/properties/environment, sin hosts ni usuarios hardcodeados (k6 `__ENV`, Gatling `System.getProperty`, JMeter `-J`, Locust `locust.conf`).
6. **Agrupar URLs dinámicas** para no fragmentar métricas (`name=` en Locust, `tags`/`group` en k6, `#{id}` en Gatling).
7. **Validar la correlación**: comprobar que los extractores devuelven valor antes de usarlos.
8. **Reutilizar conexiones**: sesión pooled, nunca una por request.
9. **Datos fuera del código** (CSV/JSON) y memoria compartida si el dataset es grande.
10. **Sin logging en el hot path**: `console.log`, `System.out.println` y listeners gráficos destruyen el throughput.
11. **Separar lectura y escritura**: cada user escribe sobre sus propios datos.
12. **Versionar tests y datos** en Git; resultados y reportes fuera (`gitignore`).

### 3.2 Antipatrones

1. ❌ Cargar producción por tener el host hardcodeado.
2. ❌ Medir sin think time (`constant(0)`, `.pause(0)`, sin `sleep`).
3. ❌ Ignorar el modelo de carga (un único Thread Group/scenario gigante, spike irreal, `atOnceUsers(10000)`).
4. ❌ Guardar response bodies completos en los resultados (archivos enormes, OOM).
5. ❌ Confundir bottleneck del generador con el del SUT (vigilar CPU/RAM del runner).
6. ❌ No separar smoke de load: un error de configuración se descubre tarde.
7. ❌ Encadenar requests sobre variables vacías sin validar la extracción.
8. ❌ Listeners/reportes gráficos activos durante la medición.
9. ❌ `open()` fuera de init (k6), `BeanShell` en vez de Groovy (JMeter, 5–10x más lento), blocking I/O en session functions (Gatling), shared mutable state sin lock y `time.sleep` sin gevent (Locust).

### 3.3 Flags y config por herramienta (inline)

- **k6**: `thresholds` (`http_req_duration: ['p(95)<500']`), `SharedArray` para datos grandes, `tags`/`group` para granularidad, `sleep(1-5s)`, `abortOnFail: true` en errores críticos, `check()` antes de `res.json()`. Evitar `JSON.parse` global (N copias), acumular arrays, `console.log` bajo carga y POST sin `Content-Type`.
- **JMeter**: CLI non-GUI, Groovy JSR223 con "Compile and cache", datos CSV/JSON externos, Transaction Controllers, HTTP Request Defaults, properties para config, `.jmx` versionado, un Thread Group por perfil. Evitar GUI para load real, BeanShell, View Results Tree activo, response data en JTL y Regex Extractor para JSON (usar JSON Extractor).
- **Gatling**: Expression Language `#{userId}`, `exitHereIfFailed()` tras auth, chains reutilizables, `System.getProperty("users","100")`, feeders `.circular()`, assertions como quality gates. Evitar concatenar strings en session, `System.out.println`, `.pause(0)`, scenario monolítico, `atOnceUsers(10000)` y omitir `requestTimeout`.
- **Locust**: `name="/api/users/[id]"`, `catch_response` (5xx falla; 429 = `success()`), `on_start` para login, `deque(maxlen=)`, `FastHttpUser`, datos propios por user. Evitar shared state sin lock, `time.sleep`, `requests.Session()` por request, correr sin `--headless` y `constant(0)`.

---

## 4. Proyecto de Referencia Completo

### 4.1 Estructura canónica

Independientemente de la herramienta, el proyecto de performance testing sigue esta forma:

```
performance-tests/
├── <entrypoint>            # k6: tests/load.js · JMeter: load_test.jmx · Gatling: Simulation · Locust: locustfile.py
├── src/ o app/             # Código de negocio del test
├── data/                   # users.csv, products.json, traffic_profile.csv
├── scripts/                # check_thresholds.py, generate_report.py, setup_test_data.py
├── config/                 # Propiedades de tuning y reporte
├── grafana/ o plugins/     # Dashboards / JARs de plugins
├── reports/                # Salida (gitignored)
├── Dockerfile
├── docker-compose.yml      # Stack local (k6 + InfluxDB + Grafana / cluster Locust)
├── Makefile                # smoke, load, stress, spike, soak, breakpoint, report, clean
└── README.md
```

### 4.2 Equivalencias de rutas por herramienta

| Concepto | k6 | JMeter | Gatling | Locust |
|----------|----|--------|---------|--------|
| Entrypoint | `tests/load.js` | `load_test.jmx` | `simulations/LoadTestSimulation` | `src/locustfile.py` |
| Código de negocio | `src/api/`, `src/scenarios/`, `src/utils/` | `scripts/groovy/`, Pre/Post-processors | `chains/`, `feeders/` | `src/users/`, `src/tasks/`, `src/shapes/` |
| Config | `Makefile`, `__ENV` | `config/user.properties`, `-J` | `config/TestConfig.java`, `System.getProperty` | `locust.conf`, variables de entorno |
| Datos | `data/*.json` + `SharedArray` | `data/*.csv` + CSV Data Set | `resources/feeders/*.csv` | `data/*.csv` + `iter_*` |
| Umbrales | `thresholds` en `options` | Assertions + `check_jmeter_results.py` | `assertions(...)` | `catch_response` + `check_thresholds.py` |
| Reportes | `--out json=`, Grafana | `-e -o results/dashboard/` | `target/gatling/**/index.html` | `--html results/report.html` |

### 4.3 Árboles de proyecto por herramienta

- **k6** `k6-performance-tests/`: `tests/{smoke,load,stress,spike,soak,breakpoint}.js` · `src/api/{auth,products,orders,users}.js` · `src/scenarios/{browse,search,purchase}.js` · `src/utils/{config,helpers,checks}.js` · `src/thresholds/{slos,per-endpoint}.js` · `data/{users,products,search_terms}.json` · `reports/.gitkeep` · `grafana/dashboards/k6-dashboard.json` · `docker-compose.yml` · `Makefile` · `README.md`.
- **JMeter** `jmeter-perf-tests/`: `test-plans/{load,stress,smoke,soak}_test.jmx` · `data/{users,products,search_terms}.csv` · `scripts/groovy/{setup_auth,validate_response}.groovy` · `scripts/{check_jmeter_results,generate_data}.py` · `config/{user,reportgenerator}.properties` · `plugins/` (JARs custom) · `results/`, `reports/` (gitignored) · `Makefile` · `Dockerfile` · `README.md`.
- **Gatling** `gatling-perf-tests/`: `pom.xml` · `Makefile` · `README.md` · `.opencode/workflows/performance.yml` · `src/test/java/config/{TestConfig,Protocols}.java` · `src/test/java/chains/{Auth,Product,Checkout}Chain.java` · `src/test/java/feeders/CustomFeeders.java` · `src/test/java/simulations/{Smoke,Load,Stress,Spike,Soak}TestSimulation.java` + `BreakpointSimulation.java` · `src/test/resources/{gatling.conf,logback-test.xml}` · `src/test/resources/feeders/{users.csv,products.json,search_terms.csv}` · `src/test/resources/bodies/{create_order,update_user}.json` · `target/gatling/` (gitignored).
- **Locust** `performance-tests/`: `locust.conf` · `requirements.txt` · `Dockerfile` · `docker-compose.yml` · `Makefile` · `src/locustfile.py` · `src/users/{web,mobile,api}_user.py` · `src/tasks/{browse,search,checkout,admin}.py` · `src/shapes/{spike,step,production}.py` · `src/helpers/{auth,data_feeder,validators}.py` · `src/hooks/{reporting,monitoring}.py` · `data/{users.csv,products.json,traffic_profile.csv}` · `scripts/{check_thresholds,generate_report,setup_test_data}.py` · `reports/` (gitignored) · `tests/{test_data_feeder,test_validators,test_shapes}.py`.

### 4.4 Comandos Make por herramienta

Contrato común de targets: `smoke`, `load`, `stress`, `spike`, `soak`, `breakpoint`, `report`, `clean` (variables `HOST`, `USERS`, `DURATION`, `SPAWN_RATE`, `TOKEN`).

- **k6** `<t>` ∈ targets: `k6 run tests/<t>.js -e TARGET_HOST=$HOST -e API_TOKEN=$TOKEN`; load/stress/soak añaden `--out json=reports/<t>.json`. Extras: `cloud` = `k6 cloud run tests/load.js`; `dashboard` = `docker-compose up -d influxdb grafana && k6 run tests/load.js --out influxdb=http://localhost:8086/k6`; `clean` = `rm -rf reports/*.json reports/*.html`.
- **JMeter** `<t>`: `jmeter -n -t test-plans/<t>_test.jmx -l results/<t>.jtl -Jtarget.host=$HOST -e -o reports/<t>/`; smoke `-Jtest.users=5 -Jtest.duration=60`; load `-Jtest.users=$USERS -Jtest.duration=$DURATION -Xmx4g`; stress `-Jtest.users=500 -Jtest.duration=900 -Xmx8g`; `report` = `jmeter -g results/load.jtl -o reports/latest/`; `clean` = `rm -rf results/*.jtl reports/*/`.
- **Gatling** `<profile>`: `mvn gatling:test -P<profile> -DtargetHost=$HOST`; load añade `-Dusers=$USERS -Dduration=$DURATION`; spike/breakpoint usan `-Dgatling.simulationClass=simulations.{SpikeTestSimulation|BreakpointSimulation}`; `recorder` = `mvn gatling:recorder`; `report` = abrir `target/gatling/<último>/index.html`; `clean` = `mvn clean && rm -rf target/gatling/`.
- **Locust**: `install` = `pip install -r requirements.txt`; smoke = `locust -f src/locustfile.py --headless --host $HOST -u 5 -r 5 --run-time 30s --html reports/smoke.html`; load = `locust -f src/locustfile.py --headless --host $HOST -u $USERS -r $SPAWN_RATE --run-time $DURATION --csv reports/load --html reports/load.html`; spike = `locust -f src/locustfile.py -f src/shapes/spike.py --headless --csv reports/spike --html reports/spike.html`; `debug` = `-u 1 -r 1 --run-time 30s --loglevel DEBUG`; `ui` = sin `--headless`; `distributed` = `docker-compose up --scale worker=4`; `validate` = `python scripts/check_thresholds.py --csv reports/load_stats.csv --p95-max 1000 --error-rate-max 1.0 --min-rps 50`; `clean` = `rm -rf reports/*`.

### 4.5 Configuración centralizada (Gatling)

```java
// src/test/java/config/TestConfig.java — cada valor = System.getProperty(clave, default)
String BASE_URL = "targetHost" / "https://api.staging.example.com";
int TARGET_USERS = "users" / "100";
int RAMP_DURATION_SEC = "rampDuration" / "120";
int HOLD_DURATION_SEC = "duration" / "600";
int P95_MAX_MS = "p95Max" / "2000";
double MIN_SUCCESS_RATE = "minSuccessRate" / "99.0";
int THINK_TIME_MIN_SEC = 2, THINK_TIME_MAX_SEC = 8;   // think time
```

---

*Canónico compartido — Performance Test Life Cycle. Referenciado por `03_Locust`, `04_Gatling`, `05_JMeter` y `06_k6`.*
