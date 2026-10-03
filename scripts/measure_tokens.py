# -*- coding: utf-8 -*-
"""Medidor de presupuesto de tokens del knowledge base PTLC.

Recorre `.opencode/agents/*.md` y `.opencode/skills/**` y estima el coste en
tokens de cada artefacto como `caracteres / 3.5`. Esta aproximacion es
conservadora para texto en espanol (≈3.5 caracteres por token) y no requiere
dependencias externas.

Uso:
    python scripts/measure_tokens.py                 # reporte legible
    python scripts/measure_tokens.py --strict        # falla (exit 1) si se
                                                     # supera algun presupuesto
    python scripts/measure_tokens.py --json out.json # volcado opcional
    python scripts/measure_tokens.py --root RUTA     # raiz alternativa del repo

Presupuestos aplicados con `--strict` (todos los artefactos del knowledge base):
    - contexto siempre activo  <= 1500 tokens
    - cuerpo de agente pipeline (`ptlc-orchestrator.md`) <= 3200 tokens
    - indice de cada skill `ptlc-*` (`SKILL.md`) <= 2000 tokens
    - ningun documento de detalle > 23000 tokens
      (los documentos grandes de `ptlc-herramientas/` se leen POR SECCION con
      su "Mapa de secciones": la restriccion real es "ninguna lectura
      obligatoria > 2000 tokens", verificada en los bloques <pre_execution>;
      el limite de tamano de archivo solo evita crecimiento descontrolado)

Ademas, `--strict` avisa (sin fallar) de "lecturas sin acotar": lineas de
lectura de los bloques <pre_execution> que referencian un archivo > 2000
tokens sin indicar seccion/linea (ancla `§`, `(línea`, `(NNN)` o `offset NNN`).
Es un aviso: no afecta al exit code.

Salida: secciones legibles por stdout; el log de progreso va a stderr.
"""

import argparse
import glob
import hashlib
import itertools
import json
import os
import re
import sys
from collections import defaultdict

# --- Presupuestos (tokens) -------------------------------------------------
BUDGET_ALWAYS_ON = 1500
BUDGET_AGENT_BODY = 3200
BUDGET_SKILL_INDEX = 2000
# Los documentos de detalle grandes se leen por seccion (ver docstring): el
# limite de archivo solo evita crecimiento descontrolado, no la lectura.
BUDGET_DETAIL_DOC = 23000

# Restriccion real de lectura: ninguna lectura obligatoria debe superar este
# tamano sin indicar la seccion/linea a cargar.
BUDGET_READ_MAX = 2000

PHASE_SKILLS = (
    "ptlc-intake",
    "ptlc-diagnostics",
    "ptlc-procedure-plan",
    "ptlc-test-plan",
    "ptlc-execution",
    "ptlc-analysis",
)

# Ancla valida de seccion/linea en una linea de lectura.
ANCHOR_RE = re.compile(r"§|\(línea|\boffset\s*\d+|\(\d+\)")

CHARS_PER_TOKEN = 3.5
NEAR_DUP_MIN_TOKENS = 1500
NEAR_DUP_JACCARD = 0.30
SHINGLE_SIZE = 8


def log(msg):
    """Log de progreso minimo por stderr."""
    sys.stderr.write("[measure_tokens] %s\n" % msg)


def read_text(path):
    """Lee un archivo tolerando BOM y CRLF de forma consistente."""
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return fh.read()


def tokens(text):
    """Estimacion de tokens: caracteres / 3.5 (espanol)."""
    return int(len(text) / CHARS_PER_TOKEN)


def split_frontmatter(text):
    """Devuelve (frontmatter, cuerpo). Si no hay frontmatter, fm=''."""
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?", text, re.S)
    if not m:
        return "", text
    return m.group(1), text[m.end():]


def frontmatter_description(text):
    """Extrae `description` del frontmatter (con o sin comillas)."""
    fm, _ = split_frontmatter(text)
    if not fm:
        return ""
    m = re.search(r'^description:\s*"(.*)"\s*$', fm, re.M)
    if m:
        return m.group(1)
    m = re.search(r'^description:\s*(\S.*?)\s*$', fm, re.M)
    return m.group(1) if m else ""


def rel(root, path):
    return os.path.relpath(path, root).replace("\\", "/")


def collect(root):
    """Recolecta agentes, skills y documentos de detalle."""
    skills_dir = os.path.join(root, ".opencode", "skills")
    agents_dir = os.path.join(root, ".opencode", "agents")

    report = {
        "agents": [],
        "skills": [],
        "detail": {},
        "dupes": [],
        "near_dupes": [],
    }

    # --- agentes ---
    for path in sorted(glob.glob(os.path.join(agents_dir, "*.md"))):
        text = read_text(path)
        fm_desc = frontmatter_description(text)
        _, body = split_frontmatter(text)
        report["agents"].append({
            "file": rel(root, path),
            "path": path,
            "desc_tokens": tokens(fm_desc),
            "body_tokens": tokens(body),
        })
    log("agentes: %d" % len(report["agents"]))

    # --- skills ---
    if os.path.isdir(skills_dir):
        for name in sorted(os.listdir(skills_dir)):
            skill_md = os.path.join(skills_dir, name, "SKILL.md")
            if not os.path.isfile(skill_md):
                continue
            text = read_text(skill_md)
            _, body = split_frontmatter(text)
            kids = []
            for dirpath, _, filenames in os.walk(os.path.join(skills_dir, name)):
                for fname in sorted(filenames):
                    if fname == "SKILL.md":
                        continue
                    fpath = os.path.join(dirpath, fname)
                    ktok = tokens(read_text(fpath))
                    kids.append({
                        "file": rel(root, fpath),
                        "tokens": ktok,
                    })
                    report["detail"][fpath] = ktok
            report["skills"].append({
                "skill": name,
                "desc_tokens": tokens(frontmatter_description(text)),
                "index_tokens": tokens(body),
                "detail_count": len(kids),
                "detail_tokens": sum(k["tokens"] for k in kids),
                "kids": kids,
            })
    log("skills: %d, documentos de detalle: %d"
        % (len(report["skills"]), len(report["detail"])))

    # --- duplicados exactos ---
    by_hash = defaultdict(list)
    for path, ktok in report["detail"].items():
        digest = hashlib.sha256(read_text(path).encode("utf-8")).hexdigest()
        by_hash[digest].append((path, ktok))
    for files in by_hash.values():
        if len(files) > 1:
            report["dupes"].append([rel(root, f) for f, _ in files])
    log("duplicados exactos: %d grupos" % len(report["dupes"]))

    # --- casi duplicados (Jaccard sobre shingles de 8 palabras) ---
    big = [p for p, kt in report["detail"].items() if kt >= NEAR_DUP_MIN_TOKENS]
    sig = {p: _shingles(p) for p in big}
    for a, b in itertools.combinations(big, 2):
        sa, sb = sig[a], sig[b]
        if not sa or not sb:
            continue
        jaccard = len(sa & sb) / len(sa | sb)
        if jaccard >= NEAR_DUP_JACCARD:
            report["near_dupes"].append({
                "a": rel(root, a),
                "b": rel(root, b),
                "jaccard": round(jaccard, 3),
            })
    log("cerca-duplicados (Jaccard>=%.2f): %d pares"
        % (NEAR_DUP_JACCARD, len(report["near_dupes"])))

    return report


def _shingles(path):
    words = re.findall(r"\w+", read_text(path).lower())
    return set(tuple(words[i:i + SHINGLE_SIZE])
               for i in range(len(words) - SHINGLE_SIZE + 1))


def totals(report, root):
    """Calcula agregados y el contexto siempre activo (global y en alcance)."""
    skills = report["skills"]
    agents = report["agents"]

    skill_desc_all = sum(s["desc_tokens"] for s in skills)
    agent_desc_all = sum(a["desc_tokens"] for a in agents)

    agents_md = os.path.join(root, "AGENTS.md")
    agents_md_tok = tokens(read_text(agents_md)) if os.path.isfile(agents_md) else 0

    opencode_json = os.path.join(root, "opencode.json")
    opencode_tok = (tokens(read_text(opencode_json))
                    if os.path.isfile(opencode_json) else 0)

    return {
        "skill_desc_tokens": skill_desc_all,
        "agent_desc_tokens": agent_desc_all,
        "agents_md_tokens": agents_md_tok,
        "opencode_json_tokens": opencode_tok,
        "always_on_tokens": (skill_desc_all + agent_desc_all
                             + agents_md_tok + opencode_tok),
        "agent_body_tokens": sum(a["body_tokens"] for a in agents),
        "skill_index_tokens": sum(s["index_tokens"] for s in skills),
        "detail_tokens": sum(s["detail_tokens"] for s in skills),
    }


def _resolve_read_ref(root, ref):
    """Resuelve una referencia a `.md` de un `<pre_execution>` a un path real.

    Acepta rutas relativas a la raiz (`.opencode/...`) y nombres sueltos (p. ej.
    `01_Load_Testing.md`) buscados por basename en el arbol de skills.
    Devuelve el path o None si no se puede resolver de forma inequivoca.
    """
    ref = ref.replace("\\", "/")
    direct = os.path.join(root, *ref.split("/"))
    if os.path.isfile(direct):
        return direct
    base = os.path.basename(ref)
    matches = glob.glob(os.path.join(root, ".opencode", "skills", "**", base),
                        recursive=True)
    if len(matches) == 1:
        return matches[0]
    return None


def check_unbounded_reads(report, root):
    """Avisos de lecturas sin acotar en los `<pre_execution>` de las fases.

    Recorre los bloques `<pre_execution>` de las skills de fase y, en las lineas
    que declaran lecturas (vinetas de lista o filas de tabla), avisa si
    referencian un archivo > BUDGET_READ_MAX sin indicar seccion/linea.
    No son violaciones: no afectan al exit code.
    """
    warnings = []
    for name in PHASE_SKILLS:
        skill_md = os.path.join(root, ".opencode", "skills", name, "SKILL.md")
        if not os.path.isfile(skill_md):
            continue
        text = read_text(skill_md)
        block = re.search(r"<pre_execution>(.*?)</pre_execution>", text, re.S)
        if not block:
            continue
        in_reading = False
        for line in block.group(1).splitlines():
            stripped = line.strip()
            if stripped.startswith("#") and re.search(
                    r"Documentos completos|Lecturas por secci|Secciones candidatas"
                    r"|Tipos de prueba", stripped):
                in_reading = True
                continue
            if "Usar la información" in stripped:
                in_reading = False
                continue
            if not in_reading:
                continue
            # Solo declaraciones de lectura: vineta de lista o fila de tabla.
            if not (stripped.startswith("- ") or stripped.startswith("* ")
                    or stripped.startswith("|")):
                continue
            if ANCHOR_RE.search(line):
                continue
            for ref in re.findall(r"`([^`]+\.md)`", line):
                path = _resolve_read_ref(root, ref)
                if not path:
                    continue
                ktok = tokens(read_text(path))
                if ktok > BUDGET_READ_MAX:
                    warnings.append({
                        "skill": name,
                        "artifact": rel(root, path),
                        "actual": ktok,
                        "budget": BUDGET_READ_MAX,
                        "line": stripped[:120],
                    })
    return warnings



def check_budgets(report, tot, root):
    """Devuelve la lista de violaciones de presupuesto (solo en alcance)."""
    violations = []

    if tot["always_on_tokens"] > BUDGET_ALWAYS_ON:
        violations.append({
            "scope": "contexto siempre activo",
            "actual": tot["always_on_tokens_in_scope"],
            "budget": BUDGET_ALWAYS_ON,
        })

    for agent in report["agents"]:
        if agent["body_tokens"] > BUDGET_AGENT_BODY:
            violations.append({
                "scope": "cuerpo de agente",
                "artifact": agent["file"],
                "actual": agent["body_tokens"],
                "budget": BUDGET_AGENT_BODY,
            })

    for skill in report["skills"]:
        if not skill["skill"].startswith("ptlc-"):
            continue
        if skill["index_tokens"] > BUDGET_SKILL_INDEX:
            violations.append({
                "scope": "indice SKILL.md",
                "artifact": "%s/SKILL.md" % skill["skill"],
                "actual": skill["index_tokens"],
                "budget": BUDGET_SKILL_INDEX,
            })

    for path, ktok in report["detail"].items():
        if ktok > BUDGET_DETAIL_DOC:
            violations.append({
                "scope": "documento de detalle",
                "artifact": rel(root, path),
                "actual": ktok,
                "budget": BUDGET_DETAIL_DOC,
            })

    return violations


def print_report(report, tot, violations, warnings, root):
    skills = report["skills"]
    agents = report["agents"]

    print("== CONTEXTO SIEMPRE ACTIVO (cada request) ==")
    print("descripciones de skills  : %6d tokens (%d skills)"
          % (tot["skill_desc_tokens"], len(skills)))
    print("descripciones de agentes : %6d tokens" % tot["agent_desc_tokens"])
    print("AGENTS.md (raiz)         : %6d tokens" % tot["agents_md_tokens"])
    print("opencode.json            : %6d tokens" % tot["opencode_json_tokens"])
    print("TOTAL por request        : %6d tokens  [presupuesto <= %d]"
          % (tot["always_on_tokens"], BUDGET_ALWAYS_ON))

    print("")
    print("== CUERPO DE AGENTES (se carga al delegar) ==")
    for agent in sorted(agents, key=lambda x: -x["body_tokens"]):
        print("%7d  %s" % (agent["body_tokens"], agent["file"]))
    print("TOTAL agentes: %d tokens" % tot["agent_body_tokens"])

    print("")
    print("== INDICES SKILL (se carga al invocar la skill) ==")
    for skill in sorted(skills, key=lambda x: -x["index_tokens"]):
        print("%7d  %s" % (skill["index_tokens"], skill["skill"]))
    print("TOTAL indices: %d tokens" % tot["skill_index_tokens"])

    print("")
    print("== DOCUMENTOS DETALLE (top 20 mas pesados) ==")
    for path, ktok in sorted(report["detail"].items(), key=lambda kv: -kv[1])[:20]:
        print("%7d  %s" % (ktok, rel(root, path)))
    print("TOTAL detalle: %d tokens en %d archivos"
          % (tot["detail_tokens"], len(report["detail"])))

    print("")
    print("== DUPLICADOS EXACTOS ==")
    if not report["dupes"]:
        print("  (ninguno)")
    for group in report["dupes"]:
        print("  " + " == ".join(group))

    print("== CERCA-DUPLICADOS (Jaccard >= %.2f) ==" % NEAR_DUP_JACCARD)
    if not report["near_dupes"]:
        print("  (ninguno)")
    for near in sorted(report["near_dupes"], key=lambda x: -x["jaccard"]):
        print("  %.3f  %s" % (near["jaccard"], near["a"]))
        print("         %s" % near["b"])

    print("")
    print("== TOTAL KB ==")
    kb_tokens = tot["skill_index_tokens"] + tot["detail_tokens"] + tot["skill_desc_tokens"]
    print("knowledge base : %d tokens (~%d KB)" % (kb_tokens, kb_tokens * 3.5 // 1024))
    print("corpus agentes : %d tokens (~%d KB)"
          % (tot["agent_body_tokens"], tot["agent_body_tokens"] * 3.5 // 1024))

    print("")
    print("== LECTURAS SIN ACOTAR (<pre_execution>, aviso, no falla) ==")
    if not warnings:
        print("  (ninguna: todas las lecturas >%d tokens indican seccion/linea)"
              % BUDGET_READ_MAX)
    else:
        for warn in warnings:
            print("  AVISO  %s: %s (%d > %d)"
                  % (warn["skill"], warn["artifact"], warn["actual"],
                     warn["budget"]))
            print("         %s" % warn["line"])
        print("  Total avisos: %d" % len(warnings))

    print("")
    print("== PRESUPUESTOS (--strict) ==")
    if not violations:
        print("  OK: todos los artefactos en alcance dentro de presupuesto")
    else:
        for violation in violations:
            name = violation.get("artifact", violation["scope"])
            print("  VIOLACION  %-24s %6d > %d  (%s)"
                  % (name, violation["actual"], violation["budget"],
                     violation["scope"]))
        print("  Total violaciones: %d" % len(violations))


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Mide el presupuesto de tokens del knowledge base PTLC.")
    parser.add_argument(
        "--root", default=None,
        help="Raiz del repo (por defecto, el padre del directorio del script).")
    parser.add_argument(
        "--strict", action="store_true",
        help="Falla con exit 1 si se supera algun presupuesto.")
    parser.add_argument(
        "--json", default=None,
        help="Ruta donde volcar el reporte completo en JSON.")
    args = parser.parse_args(argv)

    root = args.root
    if not root:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    root = os.path.abspath(root)
    log("root=%s" % root)

    report = collect(root)
    tot = totals(report, root)
    violations = check_budgets(report, tot, root)
    warnings = check_unbounded_reads(report, root)

    print_report(report, tot, violations, warnings, root)

    if args.json:
        payload = {
            "root": root,
            "budgets": {
                "always_on": BUDGET_ALWAYS_ON,
                "agent_body": BUDGET_AGENT_BODY,
                "skill_index": BUDGET_SKILL_INDEX,
                "detail_doc": BUDGET_DETAIL_DOC,
            },
            "totals": tot,
            "agents": [{k: v for k, v in a.items() if k != "path"}
                       for a in report["agents"]],
            "skills": [{k: v for k, v in s.items() if k != "kids"}
                       for s in report["skills"]],
            "detail": {rel(root, p): k for p, k in report["detail"].items()},
            "dupes": report["dupes"],
            "near_dupes": report["near_dupes"],
            "violations": violations,
            "unbounded_reads": warnings,
        }
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
        log("json escrito en %s" % args.json)

    if args.strict and violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
