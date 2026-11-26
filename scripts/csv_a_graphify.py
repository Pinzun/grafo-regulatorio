"""Adaptador determinista: CSV de la ontología -> extracción Graphify (sin LLM).

Uso: python3 -I scripts/csv_a_graphify.py [salida_json]
     (por defecto graphify-out/.graphify_extract.json)

1. Lee las tablas "Tipos de nodo" y "Extremos válidos por relación" de ontologia/ontologia.md.
2. Valida nodos_normas.csv, nodos_articulos.csv y relaciones.csv contra esas tablas: tipo de nodo,
   tipo de relación, tipos de origen/destino, metodo, estado, fuente, regla llm->inferida y nivel
   de reglamenta. Cualquier error detiene el proceso (código 1) sin escribir nada.
3. Escribe el JSON de extracción de Graphify. Como el grafo dirigido de Graphify admite una sola arista
   por par (origen, destino), las filas con el mismo (origen, relacion, destino) se agrupan en una
   arista que conserva la lista de cambios, fuentes y estados; relaciones.csv sigue siendo la fuente
   fila a fila.

Mapeo de confianza Graphify: verificada -> EXTRACTED (1.0); inferida con metodo=regla -> INFERRED (0.7);
inferida con metodo=llm -> INFERRED (0.5); metodo=manual siempre es verificada -> EXTRACTED (1.0).
Cada norma lleva cobertura (completa/parcial), modificaciones_pendientes y articulos_truncados. Los atributos
`estado` y `metodo` de la ontología se guardan en la arista y son los que mandan.
"""
import csv
import json
import os
import re
import sys
from collections import OrderedDict

ONT = "ontologia"
csv.field_size_limit(10_000_000)  # el art. 1 de la Ley 20.936 supera los 131.072 caracteres por defecto
NORMA_TIPOS = None  # se llena desde la ontología


def tabla_md(texto, titulo):
    """Devuelve las filas (dict) de la primera tabla markdown bajo el encabezado `titulo`."""
    m = re.search(r"^#+\s*" + re.escape(titulo) + r"\s*$", texto, re.M)
    if not m:
        raise SystemExit(f"ontologia.md: no se encontró la sección '{titulo}'")
    filas = []
    for ln in texto[m.end():].splitlines():
        ln = ln.strip()
        if not ln:
            if filas:
                break
            continue
        if not ln.startswith("|"):
            if filas:
                break
            continue
        celdas = [c.strip() for c in ln.strip("|").split("|")]
        if all(re.fullmatch(r"-+", c) for c in celdas):
            continue
        filas.append(celdas)
    cab, *datos = filas
    return [dict(zip(cab, f)) for f in datos]


def lista(celda):
    return [x.strip() for x in celda.split(",") if x.strip()]


def cargar_ontologia():
    txt = open(os.path.join(ONT, "ontologia.md"), encoding="utf-8").read()
    tipos = {r["tipo"]: r["categoria"] for r in tabla_md(txt, "Tipos de nodo")}
    normas = {t for t, c in tipos.items() if c == "norma"}

    def expandir(cats):
        out = set()
        for c in lista(cats):
            out |= normas if c == "norma" else {c}
        desconocidos = out - set(tipos)
        if desconocidos:
            raise SystemExit(f"ontologia.md: tipos desconocidos en tabla de extremos: {desconocidos}")
        return out

    rel = {}
    for r in tabla_md(txt, "Extremos válidos por relación"):
        rel[r["relacion"]] = {
            "origen": expandir(r["origen"]), "destino": expandir(r["destino"]),
            "metodos": set(lista(r["metodos"])), "estados": set(lista(r["estados"])),
            "requiere_fuente": r["requiere_fuente"].lower() == "si",
        }
    coberturas = {r["cobertura"] for r in tabla_md(txt, "Valores de cobertura")}
    return tipos, rel, coberturas


def leer_csv(nombre):
    with open(os.path.join(ONT, nombre), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def etiqueta_norma(n):
    t = {"ley": "Ley", "resolucion": "Res."}.get(n["tipo"], n["tipo"])
    if n["numero"].startswith("DFL"):
        return f"{n['numero']} de {n['anio']} (LGSE)"
    return f"{t} {n['numero']} de {n['anio']}"


def main():
    salida = sys.argv[1] if len(sys.argv) > 1 else "graphify-out/.graphify_extract.json"
    tipos, reglas, coberturas = cargar_ontologia()
    normas, articulos, relaciones = leer_csv("nodos_normas.csv"), leer_csv("nodos_articulos.csv"), leer_csv("relaciones.csv")
    errores = []

    # ---------------------------------------------------------------- nodos
    nodos = OrderedDict()
    etiquetas_norma = {n["id"]: etiqueta_norma(n) for n in normas}
    for n in normas:
        if n["tipo"] not in tipos:
            errores.append(f"nodo {n['id']}: tipo '{n['tipo']}' no está en la ontología")
        cob, pend, trunc = n.get("cobertura", ""), n.get("modificaciones_pendientes", ""), n.get("articulos_truncados", "")
        if cob not in coberturas:
            errores.append(f"norma {n['id']}: cobertura '{cob}' no válida (válidas: {sorted(coberturas)})")
        elif not pend.isdigit():
            errores.append(f"norma {n['id']}: modificaciones_pendientes '{pend}' no es un entero")
        elif (cob == "parcial") != (int(pend) > 0 or bool(trunc)):
            errores.append(f"norma {n['id']}: cobertura '{cob}' incoherente con pendientes={pend}, truncados='{trunc}'")
        if n.get("articulos_truncados_recuperados_pdf") and not re.fullmatch(r"[0-9a-f]{64}", n.get("pdf_sha256", "")):
            errores.append(f"norma {n['id']}: declara artículos recuperados del PDF sin pdf_sha256 válido")
        nodos[n["id"]] = {
            "id": n["id"], "label": etiquetas_norma[n["id"]], "file_type": "document",
            "articulos_truncados_recuperados_pdf": n.get("articulos_truncados_recuperados_pdf", ""),
            "pdf_sha256": n.get("pdf_sha256", ""),
            "cobertura": cob, "modificaciones_pendientes": int(pend) if pend.isdigit() else pend,
            "articulos_truncados": trunc,
            "source_file": "ontologia/nodos_normas.csv", "source_location": f"idNorma={n['id_bcn']}",
            "source_url": n["url_fuente"], "captured_at": None, "author": None, "contributor": None,
            "tipo": n["tipo"], "numero": n["numero"], "anio": n["anio"], "id_bcn": n["id_bcn"],
            "titulo": n.get("titulo", ""), "organo_emisor": n["organo_emisor"],
            "fecha_publicacion": n.get("fecha_publicacion", ""), "fecha_promulgacion": n.get("fecha_promulgacion", ""),
            "estado_vigencia": n.get("estado_vigencia", ""),
        }
    for a in articulos:
        if a["tipo"] not in tipos:
            errores.append(f"nodo {a['id']}: tipo '{a['tipo']}' no está en la ontología")
        if a["id"] in nodos:
            errores.append(f"nodo duplicado: {a['id']}")
        base = etiquetas_norma.get(a["norma_contenedora"], a["norma_contenedora"])
        # Cobertura de la historia (solo artículos del DFL 4, que es la norma modificada)
        ch, falt = a.get("cobertura_historia", ""), a.get("leyes_faltantes", "")
        if a["norma_contenedora"] == "ley_dfl4_2006":
            if ch not in coberturas:
                errores.append(f"nodo {a['id']}: cobertura_historia '{ch}' no válida (válidas: {sorted(coberturas)})")
            elif (ch == "parcial") != bool(falt):
                errores.append(f"nodo {a['id']}: cobertura_historia '{ch}' incoherente con leyes_faltantes='{falt}'")
        # El aviso va en source_location porque es lo que muestran `graphify explain` y `query`
        loc = f"idParte={a['id_parte']}"
        if a.get("derogado") == "derogado":
            loc += f" · DEROGADO (vigente hasta {a['vigente_hasta']})" if a.get("vigente_hasta") else " · DEROGADO"
        if ch == "parcial":
            loc += " · HISTORIA INCOMPLETA: faltan leyes " + ", ".join(f"{l[:2]}.{l[2:]}" for l in falt.split(";"))
        elif ch == "completa":
            loc += " · historia completa"
        nodos[a["id"]] = {
            "id": a["id"], "label": f"{base} — art. {a['numero']}", "file_type": "document",
            "cobertura_historia": ch, "leyes_modificatorias_bcn": a.get("leyes_modificatorias_bcn", ""),
            "leyes_faltantes": falt,
            "source_file": "ontologia/nodos_articulos.csv", "source_location": loc,
            "source_url": a["url_fuente"], "captured_at": None, "author": None, "contributor": None,
            "tipo": a["tipo"], "norma_contenedora": a["norma_contenedora"], "numero": a["numero"],
            "id_parte": a["id_parte"], "fecha_version_bcn": a["fecha_version_bcn"],
            "vigente_desde": a["vigente_desde"], "vigente_hasta": a["vigente_hasta"],
            "derogado": a["derogado"], "estado_extraccion": a["estado_extraccion"], "texto": a["texto"],
        }

    # ---------------------------------------------------------------- aristas
    grupos = OrderedDict()
    for i, r in enumerate(relaciones, start=2):
        donde = f"relaciones.csv línea {i} ({r['origen']} -{r['relacion']}-> {r['destino']})"
        regla = reglas.get(r["relacion"])
        if regla is None:
            errores.append(f"{donde}: relación '{r['relacion']}' no está en la ontología")
            continue
        o, d = nodos.get(r["origen"]), nodos.get(r["destino"])
        if o is None:
            errores.append(f"{donde}: origen no existe como nodo")
        elif o["tipo"] not in regla["origen"]:
            errores.append(f"{donde}: origen de tipo '{o['tipo']}' no permitido (válidos: {sorted(regla['origen'])})")
        if d is None:
            errores.append(f"{donde}: destino no existe como nodo")
        elif d["tipo"] not in regla["destino"]:
            errores.append(f"{donde}: destino de tipo '{d['tipo']}' no permitido (válidos: {sorted(regla['destino'])})")
        if r.get("metodo") not in regla["metodos"]:
            errores.append(f"{donde}: metodo '{r.get('metodo')}' no permitido (válidos: {sorted(regla['metodos'])})")
        if r["estado"] not in regla["estados"]:
            errores.append(f"{donde}: estado '{r['estado']}' no permitido (válidos: {sorted(regla['estados'])})")
        if r.get("metodo") == "llm" and r["estado"] != "inferida":
            errores.append(f"{donde}: metodo llm exige estado inferida")
        if r.get("metodo") == "manual":
            if r["estado"] != "verificada":
                errores.append(f"{donde}: metodo manual exige estado verificada")
            if not re.search(r"revisado: .+ \d{4}-\d{2}-\d{2}", r.get("observaciones", "")):
                errores.append(f"{donde}: metodo manual exige 'revisado: <persona> <AAAA-MM-DD>' en observaciones")
        if regla["requiere_fuente"] and not (r.get("fuente_url") and r.get("fuente_id_parte")):
            errores.append(f"{donde}: sin fuente (url e idParte)")
        if r["estado"] == "inferida" and not r.get("observaciones"):
            errores.append(f"{donde}: inferida sin motivo en observaciones")
        if r["relacion"] == "contiene" and d and d.get("norma_contenedora") != r["origen"]:
            errores.append(f"{donde}: el artículo pertenece a '{d.get('norma_contenedora')}', no a '{r['origen']}'")
        if r["relacion"] == "reglamenta" and o and d:
            if (o["tipo"], d["tipo"]) not in {("reglamento", "ley"), ("norma_tecnica", "reglamento")}:
                errores.append(f"{donde}: reglamenta debe ir al nivel inmediato superior")
        grupos.setdefault((r["origen"], r["destino"]), []).append(r)

    aristas = []
    for (o, d), filas in grupos.items():
        rels = {f["relacion"] for f in filas}
        if len(rels) > 1:
            errores.append(f"par {o} -> {d} tiene varias relaciones {sorted(rels)}; el grafo dirigido no las admite")
            continue
        estados = sorted({f["estado"] for f in filas})
        metodos = sorted({f["metodo"] for f in filas})
        inferida = "inferida" in estados
        if not inferida:
            conf, score = "EXTRACTED", 1.0
        elif metodos == ["regla"]:
            conf, score = "INFERRED", 0.7
        else:
            conf, score = "INFERRED", 0.5
        aristas.append({
            "source": o, "target": d, "relation": filas[0]["relacion"],
            "confidence": conf, "confidence_score": score,
            "source_file": "ontologia/relaciones.csv",
            "source_location": "idParte=" + ",".join(OrderedDict.fromkeys(f["fuente_id_parte"] for f in filas)),
            "weight": float(len(filas)),
            "estado": "inferida" if inferida else "verificada",
            "metodo": ",".join(metodos), "n_filas": len(filas),
            "tipos_cambio": ",".join(OrderedDict.fromkeys(f["tipo_cambio"] for f in filas if f["tipo_cambio"])),
            "fecha_vigencia": ",".join(OrderedDict.fromkeys(f["fecha_vigencia"] for f in filas if f["fecha_vigencia"])),
            "fuente_url": ",".join(OrderedDict.fromkeys(f["fuente_url"] for f in filas)),
            "detalle": " || ".join(f["detalle"] for f in filas),
            "observaciones": " || ".join(f["observaciones"] for f in filas if f["observaciones"]),
        })

    if errores:
        print(f"VALIDACIÓN FALLIDA: {len(errores)} error(es)", file=sys.stderr)
        for e in errores:
            print("  - " + e, file=sys.stderr)
        raise SystemExit(1)

    os.makedirs(os.path.dirname(salida) or ".", exist_ok=True)
    extraccion = {"nodes": list(nodos.values()), "edges": aristas, "hyperedges": [],
                  "input_tokens": 0, "output_tokens": 0}
    with open(salida, "w", encoding="utf-8") as f:
        json.dump(extraccion, f, ensure_ascii=False, indent=1)
    from collections import Counter
    print(f"Validación OK contra ontologia.md: {len(nodos)} nodos, {len(relaciones)} filas -> {len(aristas)} aristas")
    print("  aristas por (relacion, estado, metodo):",
          dict(Counter((a["relation"], a["estado"], a["metodo"]) for a in aristas)))
    for n in normas:
        if n["cobertura"] != "completa":
            print(f"  ADVERTENCIA cobertura parcial: {etiquetas_norma[n['id']]} — {n['modificaciones_pendientes']} "
                  f"modificaciones pendientes; artículos truncados: {n['articulos_truncados'] or 'ninguno'}")


if __name__ == "__main__":
    main()
