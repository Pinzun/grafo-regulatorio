"""Construye el grafo con Graphify a partir de los CSV de la ontología (sin LLM).

Uso (desde la raíz del repo, con el Python del .venv donde está graphifyy):
    .venv/bin/python scripts/construir_grafo.py
    .venv/bin/graphify export html     # visualización graphify-out/graph.html

Pasos: valida y convierte con scripts/csv_a_graphify.py -> build_from_json(directed=True,
dedup=False) -> comunidades -> graph.json + GRAPH_REPORT.md.

dedup=False: todos los nodos vienen del mismo CSV y Graphify, por defecto, fusiona nodos por
(archivo, etiqueta); los ids de la ontología ya son canónicos.
"""
import json
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


if __name__ == "__main__":
    main()
