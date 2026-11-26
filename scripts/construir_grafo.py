"""Construye el grafo con Graphify a partir de los CSV de la ontología (sin LLM).

Uso (desde la raíz del repo, con el Python del .venv donde está graphifyy):
    .venv/bin/python scripts/construir_grafo.py
    .venv/bin/graphify export html     # visualización graphify-out/graph.html

Al final exporta la bóveda de Obsidian (graphify-out/obsidian/, una nota por nodo y un enlace por arista) y
regenera datos/derivados/bloque_transmision.csv y textos/ (scripts/generar_textos.py, que enlaza a esas notas).

Pasos: valida y convierte con scripts/csv_a_graphify.py -> build_from_json(directed=True,
dedup=False) -> comunidades -> graph.json + GRAPH_REPORT.md.

dedup=False: todos los nodos vienen del mismo CSV y Graphify, por defecto, fusiona nodos por
(archivo, etiqueta); los ids de la ontología ya son canónicos.
"""
import json
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

from graphify.analyze import god_nodes, suggest_questions, surprising_connections
from graphify.build import build_from_json
from graphify.cluster import cluster, score_all
from graphify.diagnostics import diagnose_extraction, format_diagnostic_report
from graphify.export import to_json
from graphify.report import generate

RAIZ = Path(__file__).resolve().parent.parent
OUT = RAIZ / "graphify-out"
EXTRACT = OUT / ".graphify_extract.json"
CORPUS = ["ontologia/ontologia.md", "ontologia/nodos_normas.csv", "ontologia/nodos_articulos.csv",
          "ontologia/relaciones.csv"]


def etiqueta_comunidad(G, miembros):
    """Etiqueta determinista: norma más frecuente entre los miembros + rango de artículos."""
    normas = Counter(G.nodes[n].get("norma_contenedora") or n for n in miembros
                     if G.nodes[n].get("tipo") == "articulo")
    leyes = [G.nodes[n]["label"] for n in miembros if G.nodes[n].get("tipo") != "articulo"]
    partes = []
    if leyes:
        partes.append(" + ".join(sorted(leyes)))
    if normas:
        norma, _ = normas.most_common(1)[0]
        arts = sorted((G.nodes[n]["numero"] for n in miembros if G.nodes[n].get("norma_contenedora") == norma),
                      key=lambda k: [int(x) if x.isdigit() else x for x in k.replace(" ", "-").split("-")])
        etiqueta = G.nodes[norma]["label"] if norma in G else norma
        partes.append(f"{etiqueta}: arts. {arts[0]}…{arts[-1]}" if len(arts) > 1 else f"{etiqueta}: art. {arts[0]}")
    return " | ".join(partes)[:90] or "Comunidad"


def insertar_cobertura(report, G):
    """Agrega al reporte, antes de '## Summary', la cobertura de cada norma y los métodos de las aristas."""
    filas = ["## Cobertura de las normas", "",
             "| Norma | Cobertura | Modificaciones pendientes | Artículos truncados (idParte) |", "|---|---|---|---|"]
    parciales = 0
    for n, d in G.nodes(data=True):
        if d.get("tipo") == "articulo":
            continue
        parciales += d.get("cobertura") == "parcial"
        filas.append(f"| {d['label']} | {d.get('cobertura')} | {d.get('modificaciones_pendientes')} | "
                     f"{d.get('articulos_truncados') or '—'} |")
    filas.append("")
    if parciales:
        filas.append(f"> **Advertencia:** {parciales} norma(s) con cobertura parcial. Las respuestas sobre qué "
                     "artículos modificó una ley pueden estar incompletas; los candidatos pendientes están en "
                     "`datos/derivados/candidatos_por_fechaversion.csv` y la causa en "
                     "`docs/diagnostico_truncamiento_bcn.md`.")
        filas.append("")
    # Historia por artículo del DFL 4 (notas BCN): leyes posteriores al DFL 4 que no están en el grafo
    arts = [d for _, d in G.nodes(data=True) if d.get("norma_contenedora") == "ley_dfl4_2006"]
    parc = [d for d in arts if d.get("cobertura_historia") == "parcial"]
    filas += ["## Cobertura de la historia por artículo", "",
              f"{len(arts) - len(parc)} de {len(arts)} artículos del DFL 4 en el grafo tienen historia completa "
              "(todas las leyes posteriores al DFL 4 que la BCN anota en el artículo están en el grafo). "
              "Detalle de todo el DFL 4 en `datos/derivados/historia_articulos.csv`.", ""]
    if parc:
        filas += ["| Artículo | Leyes que faltan |", "|---|---|"]
        clave = lambda d: [int(x) if x.isdigit() else x for x in d["numero"].replace(" ", "-").split("-")]
        filas += [f"| {d['numero']} | {d['leyes_faltantes'].replace(';', ', ')} |" for d in sorted(parc, key=clave)]
        filas.append("")
    metodos = Counter((d["relation"], d.get("estado"), d.get("metodo")) for _, _, d in G.edges(data=True))
    filas += ["Aristas por relación, estado y método: " +
              "; ".join(f"{r}/{e}/{m}: {c}" for (r, e, m), c in sorted(metodos.items())), "", ""]
    marca = "## Summary"
    return report.replace(marca, "\n".join(filas) + marca, 1) if marca in report else report + "\n" + "\n".join(filas)


def main():
    OUT.mkdir(exist_ok=True)
    r = subprocess.run([sys.executable, "-I", str(RAIZ / "scripts/csv_a_graphify.py"), str(EXTRACT)], cwd=RAIZ)
    if r.returncode:
        raise SystemExit("La validación contra la ontología falló; no se construye el grafo.")
    extraction = json.loads(EXTRACT.read_text(encoding="utf-8"))

    salud = diagnose_extraction(extraction, directed=True, root=str(RAIZ))
    print(format_diagnostic_report(salud))

    G = build_from_json(extraction, root=str(RAIZ), directed=True, dedup=False)
    if G.number_of_nodes() != len(extraction["nodes"]) or G.number_of_edges() != len(extraction["edges"]):
        raise SystemExit(f"Graphify alteró el grafo: {G.number_of_nodes()} nodos / {G.number_of_edges()} aristas, "
                         f"se esperaban {len(extraction['nodes'])} / {len(extraction['edges'])}")
    communities = cluster(G)
    cohesion = score_all(G, communities)
    labels = {cid: etiqueta_comunidad(G, m) for cid, m in communities.items()}
    gods = god_nodes(G)
    surprises = surprising_connections(G, communities)
    questions = suggest_questions(G, communities, labels)

    # force=True: el grafo se reconstruye completo y de forma determinista desde los CSV, así que
    # un grafo más chico es intencional (p. ej. si se corrigió una fila).
    to_json(G, communities, str(OUT / "graph.json"), force=True, community_labels=labels)
    words = sum(len((RAIZ / p).read_text(encoding="utf-8").split()) for p in CORPUS)
    detection = {"total_files": len(CORPUS), "total_words": words,
                 "warning": "Grafo generado por adaptador determinista (scripts/csv_a_graphify.py), sin extracción LLM."}
    report = generate(G, communities, cohesion, labels, gods, surprises, detection,
                      {"input": 0, "output": 0}, str(RAIZ), suggested_questions=questions)
    report = insertar_cobertura(report, G)
    (OUT / "GRAPH_REPORT.md").write_text(report, encoding="utf-8")
    (OUT / ".graphify_labels.json").write_text(json.dumps({str(k): v for k, v in labels.items()},
                                                          ensure_ascii=False), encoding="utf-8")
    (OUT / ".graphify_root").write_text(str(RAIZ), encoding="utf-8")
    (OUT / ".graphify_python").write_text(sys.executable, encoding="utf-8")
    print(f"Grafo: {G.number_of_nodes()} nodos, {G.number_of_edges()} aristas, {len(communities)} comunidades "
          f"(dirigido={G.is_directed()})")
    print("Relaciones:", dict(Counter(d["relation"] for _, _, d in G.edges(data=True))))
    for cid, lab in labels.items():
        print(f"  comunidad {cid}: {lab} ({len(communities[cid])} nodos)")

    # Bóveda de Obsidian: una nota por nodo, un enlace por arista (graphify export obsidian). Se borra y se
    # rehace para que no queden notas de nodos que ya no existen. Determinista; no se edita a mano.
    boveda = OUT / "obsidian"
    if boveda.exists():
        shutil.rmtree(boveda)
    r = subprocess.run([str(Path(sys.executable).parent / "graphify"), "export", "obsidian", "--dir", str(boveda)],
                       cwd=RAIZ, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"graphify export obsidian falló: {r.stderr}")
    print(f"Obsidian: {sum(1 for _ in boveda.glob('*.md'))} notas en {boveda.relative_to(RAIZ)}/")

    # Textos por artículo: se regeneran junto con el grafo, desde los mismos CSV (primero el bloque,
    # del que dependen). Sin LLM.
    for script in ("bloque_transmision.py", "generar_textos.py"):
        r = subprocess.run([sys.executable, "-I", str(RAIZ / "scripts" / script)], cwd=RAIZ)
        if r.returncode:
            raise SystemExit(f"{script} falló")


if __name__ == "__main__":
    main()
