"""Extracción determinista (XML + regex, sin LLM) de las modificaciones al DFL 4 y de la
relación implementa de la Res. Ex. 156. Regenera:

  ontologia/relaciones.csv       (aristas: modifica, implementa)
  ontologia/nodos_articulos.csv  (nodos tipo articulo involucrados)
  ontologia/nodos_normas.csv     (completa id_bcn, url, fechas desde el XML)

Uso: python3 -I scripts/extraer_modificaciones.py

Criterio de estado:
  verificada  el texto de la norma modificatoria nombra literalmente el artículo y la operación
              (o, para `contiene`, la estructura del XML lo establece).
  inferida    no consta literalmente en el texto; se deduce por regla (p. ej. sustitución de un
              Título completo, texto truncado). Motivo en `observaciones`. Requiere revisión humana.
  metodo      siempre `regla` en este script (ontología v0.2).
"""
import csv
import os
from collections import Counter
import re
import xml.etree.ElementTree as ET

RAW = "datos/raw"
ONT = "ontologia"
NS = "{http://www.leychile.cl/esquemas}"
PC = "POR_COMPLETAR"

ARCHIVOS = {
    "ley_dfl4_2006": "ley_dfl4_2006__idNorma_258171.xml",
    "ley_20936_2016": "ley_20936_2016__idNorma_1092695.xml",
    "ley_21721_2024": "ley_21721_2024__idNorma_1209692.xml",
    "res_156_2025": "res_156_2025__idNorma_1212350.xml",
}
# Artículo de cada ley que contiene las modificaciones al DFL 4 (se valida por regex abajo).
MODIFICATORIAS = {"ley_21721_2024": "art_unico", "ley_20936_2016": "art_1"}

VERBOS = {
    "reemplaza": r"reempl[aá]z(?:a|ase|ese)|sustit[uú]y(?:e|ese)",
    "agrega": r"agr[eé]g(?:a|ase|uese)|incorp[oó]r(?:a|ase|ese)|interc[aá]l(?:a|ase|ese)|a[nñ][aá]d(?:e|ese)",
    "elimina": r"elim[ií]n(?:a|ase|ese)|supr[ií]m(?:e|ese)|der[oó]g(?:a|ase|uese)",
    "modifica_contenedor": r"modif[ií]c(?:a|ase|ese)",
}
RE_VERBO = re.compile(r"\b(" + "|".join(VERBOS.values()) + r")\b", re.I)
RE_ART = re.compile(r"art[íi]culos?\s+(\d+)\s*[°º]?\s*(?:-\s*(\d+))?\s*(bis|ter|qu[aá]ter)?\b", re.I)
RE_ITEM = re.compile(r'^\s*(\d+)[\.\)]\s+(.*)', re.S)
RE_LIT = re.compile(r'^\s*([a-zñ])\)\s+(.*)', re.S)


# ---------------------------------------------------------------- utilidades XML
def cargar(nodo):
    path = os.path.join(RAW, ARCHIVOS[nodo])
    return ET.parse(path).getroot()


def ident(root):
    i = root.find(NS + "Identificador")
    return {
        "id_bcn": root.attrib["normaId"],
        "fecha_promulgacion": i.attrib.get("fechaPromulgacion", PC),
        "fecha_publicacion": i.attrib.get("fechaPublicacion", PC),
        "derogado": root.attrib.get("derogado", PC),
        "fecha_version_bcn": root.attrib.get("fechaVersion", PC),
        "titulo": root.findtext(NS + "Metadatos/" + NS + "TituloNorma") or PC,
        "organismo_bcn": "; ".join(o.text.strip() for o in i.iter(NS + "Organismo")),
        "tipo_numero_bcn": "; ".join(
            " ".join(c.text.strip() for c in t) for t in i.iter(NS + "TipoNumero")),
    }


def partes(root):
    for ef in root.iter(NS + "EstructuraFuncional"):
        yield ef, (ef.findtext(NS + "Texto") or ""), (
            ef.findtext(NS + "Metadatos/" + NS + "NombreParte") or "").strip()


def norm_ws(s):
    return re.sub(r"\s+", " ", s).strip()


def clave_art(num, guion=None, sufijo=None):
    k = num + (f"-{guion}" if guion else "")
    if sufijo:
        k += " " + sufijo.lower().replace("á", "a")
    return k


def id_art(norma, clave):
    return f"{norma}__art_" + clave.replace(" ", "_")


def parrafos(texto):
    """Párrafo = línea que empieza con sangría (>=3 espacios) o tras línea en blanco.
    Las líneas de continuación (texto con corte de línea fijo, como la Ley 20.936) se unen."""
    bloques = re.split(r"\n(?=[ \t]{3,}\S)|\n\s*\n", texto)
    return [norm_ws(b) for b in bloques if b.strip()]


def sin_citas(s):
    return re.sub(r'"[^"]*"', '""', s)


# ---------------------------------------------------------------- DFL 4 indexado
def indice_dfl4():
    root = cargar("ley_dfl4_2006")
    idx = {}
    for ef, txt, nombre in partes(root):
        if ef.attrib.get("tipoParte") != "Artículo" or ef.attrib.get("transitorio") == "transitorio":
            continue
        n = nombre.lower().replace("º", "").replace("°", "")
        n = re.sub(r"\s*-\s*", "-", re.sub(r"\s+", " ", n)).strip()
        idx[n] = {
            "id_parte": ef.attrib["idParte"], "fecha_version_bcn": ef.attrib.get("fechaVersion", PC),
            "derogado": ef.attrib.get("derogado", PC),
            "fecha_derogacion": "; ".join(x.text for x in ef.iter(NS + "FechaDerogacion") if x.text),
            "texto": norm_ws(txt),
        }
    return idx


# ---------------------------------------------------------------- vigencia (transitorios)
def reglas_vigencia(root):
    """Oraciones de artículos transitorios que mencionan 'vigencia' y los artículos que citan."""
    reglas = []
    for ef, txt, _ in partes(root):
        if ef.attrib.get("tipoParte") != "Artículo":
            continue
        cab = norm_ws(txt)[:40]
        if not re.match(r"Art[íi]culo\s+(primero|segundo|tercero|cuarto|quinto|sexto|s[ée]ptimo|octavo|noveno|d[ée]cimo|und[ée]cimo|duod[ée]cimo|decimo|vig[ée]simo|vigesimo)", cab, re.I):
            continue
        for oracion in re.split(r"(?<=\.)\s+(?=[A-ZÁÉÍÓÚ])", norm_ws(txt)):
            if "vigencia" not in oracion.lower():
                continue
            exactos, desde = set(), []
            for m in RE_ART.finditer(oracion):
                k = clave_art(*m.groups())
                exactos.add(k)
                if re.match(r"\s*[°º]?\s*(y|a)\s+siguientes", oracion[m.end():], re.I):
                    desde.append(int(m.group(1)))
            reglas.append({"id_parte": ef.attrib["idParte"], "cab": cab, "oracion": oracion,
                           "exactos": exactos, "desde": desde})
    return reglas


def vigencia_de(clave, reglas):
    base = int(re.match(r"\d+", clave).group())
    hits = [r for r in reglas
            if clave in r["exactos"] or any(base >= d and "-" not in clave for d in r["desde"])]
    return hits


# ---------------------------------------------------------------- parser de numerales
def numerales(texto):
    """Devuelve numerales de primer nivel (fuera de texto citado, numeración correlativa)
    con sus literales y el texto citado que insertan. Detecta truncamiento (comillas impares)."""
    items, actual, comillas, esperado = [], None, 0, 1
    # El artículo modificatorio suele venir entero entre comillas ("Artículo único.- ... ").
    # Se quita esa comilla envolvente para que la paridad distinga texto citado de numerales.
    texto = re.sub(r'^\s*"', "", texto, count=1)
    truncado = not re.search(r'[.;:"”]\s*$', texto)
    for p in parrafos(texto):
        fuera = comillas % 2 == 0
        m = RE_ITEM.match(p) if fuera else None
        if m and int(m.group(1)) == esperado and RE_VERBO.search(m.group(2)[:60]):
            actual = {"n": esperado, "texto": m.group(2), "literales": [], "citado": []}
            items.append(actual)
            esperado += 1
        elif actual is not None:
            ml = RE_LIT.match(p) if fuera else None
            if ml and RE_VERBO.search(ml.group(2)[:40]):
                actual["literales"].append({"l": ml.group(1), "texto": ml.group(2)})
            elif not fuera or p.startswith('"'):
                actual["citado"].append(p)
        comillas += p.count('"')
    return items, truncado


def acciones(frase):
    """Lista de (tipo_cambio, texto_accion) por cada verbo fuera de comillas."""
    s = sin_citas(frase)
    out = []
    for m in RE_VERBO.finditer(s):
        v = m.group(1).lower()
        tipo = next(t for t, rx in VERBOS.items() if re.fullmatch(rx, v, re.I))
        out.append((tipo, v))
    return out


def destino_en(frase):
    """Artículo afectado según la frase (fuera de comillas). 'el siguiente artículo X, nuevo' manda
    sobre 'a continuación del artículo Y' (Y es solo ubicación)."""
    s = sin_citas(frase)
    m = re.search(r"siguiente\s+" + RE_ART.pattern, s, re.I)
    if m:
        return clave_art(*m.groups()[-3:]), "nuevo"
    ms = [m for m in RE_ART.finditer(s)
          if not re.search(r"(a continuaci[oó]n|despu[eé]s|antes)\s+del\s*$", s[:m.start()], re.I)]
    if ms:
        return clave_art(*ms[0].groups()), "existente"
    return None, None


# ---------------------------------------------------------------- extracción
def extraer_ley(norma, dfl4, fecha_consulta):
    root = cargar(norma)
    meta = ident(root)
    parte = next(ef for ef, txt, _ in partes(root)
                 if re.search(r"Introd[uú]cense las siguientes modificaciones en el decreto con fuerza de ley N\s*°\s*4/20\.?018",
                              norm_ws(txt)[:250]))
    texto = parte.findtext(NS + "Texto")
    id_parte = parte.attrib["idParte"]
    origen = f"{norma}__{MODIFICATORIAS[norma]}"
    url = f"https://www.leychile.cl/Consulta/obtxml?opt=7&idNorma={meta['id_bcn']}"
    reglas = reglas_vigencia(root)
    items, truncado = numerales(texto)
    filas, arts = [], {}

    def fila(destino, tipo, detalle, estado, obs):
        obs = list(obs)
        info = dfl4.get(destino)
        if info is None:
            obs.append("artículo no encontrado en el XML vigente del DFL 4")
        elif info["fecha_version_bcn"] == meta["fecha_publicacion"]:
            obs.append(f"corroborado: fechaVersion BCN del artículo en DFL 4 = {info['fecha_version_bcn']}")
        else:
            obs.append(f"fechaVersion BCN del artículo en DFL 4 = {info['fecha_version_bcn']} (versión posterior; no corrobora ni contradice)")
        hits = vigencia_de(destino, reglas)
        if hits:
            base = "fecha_publicacion; REVISAR transitorio " + ", ".join(
                f"{h['cab'].split('.-')[0]} (idParte {h['id_parte']})" for h in hits)
        else:
            base = "fecha_publicacion (la norma no fija vigencia especial para este artículo)"
        filas.append({
            "origen": origen, "relacion": "modifica", "destino": id_art("ley_dfl4_2006", destino),
            "tipo_cambio": tipo, "detalle": detalle[:300],
            "fecha_vigencia": meta["fecha_publicacion"], "base_vigencia": base,
            "fuente_url": url, "fuente_id_parte": id_parte, "fecha_consulta": fecha_consulta,
            "estado": estado, "observaciones": " | ".join(obs),
        })
        arts[destino] = True

    for it in items:
        cab = it["texto"]
        dest, kind = destino_en(cab)
        acc = acciones(cab)
        tipo0 = acc[0][0] if acc else None
        etiqueta = f"N° {it['n']}: "
        # Inserción o sustitución de un Título completo
        mt = re.search(r"(?:el\s+siguiente\s+|el\s+)(T[íi]tulo\s+[IVXL]+(?:\s+BIS)?)", sin_citas(cab), re.I)
        if mt and (dest is None or kind != "nuevo"):
            titulo = mt.group(1)
            arts_cit = []
            for p in it["citado"]:
                m = re.match(r'"?\s*' + RE_ART.pattern + r"\s*[°º]?\s*\.\s*-", p, re.I)
                if m:
                    arts_cit.append(clave_art(*m.groups()))
            for i, a in enumerate(arts_cit):
                ultimo = truncado and it is items[-1] and i == len(arts_cit) - 1
                if tipo0 == "agrega" and re.search(r"nuevo", sin_citas(cab), re.I):
                    obs = [f"artículo contenido en el {titulo} nuevo que se intercala"]
                    if ultimo:
                        obs.append("texto del artículo truncado en el XML BCN")
                    fila(a, "agrega", etiqueta + cab, "inferida" if ultimo else "verificada", obs)
                else:
                    obs = [f"motivo: el N° {it['n']} sustituye el {titulo} completo; el texto no indica "
                           "correspondencia artículo a artículo (el artículo aparece en el texto sustituto)"]
                    if truncado and it is items[-1]:
                        obs.append("XML BCN truncado dentro de este numeral: lista de artículos incompleta")
                    if ultimo:
                        obs.append("texto del artículo truncado en el XML BCN")
                    fila(a, "reemplaza", etiqueta + cab, "inferida", obs)
            continue
        if tipo0 == "modifica_contenedor" and it["literales"]:
            for lit in it["literales"]:
                d2, _ = destino_en(lit["texto"])
                d2 = d2 or dest
                for tipo, verbo in acciones(lit["texto"]):
                    if tipo == "modifica_contenedor":
                        continue
                    fila(d2, tipo, f"N° {it['n']} letra {lit['l']}) [{verbo}]: {lit['texto']}", "verificada", [])
            continue
        if dest and tipo0 in ("reemplaza", "agrega", "elimina"):
            obs = []
            if kind == "nuevo":
                obs.append("artículo nuevo")
            fila(dest, tipo0, etiqueta + cab, "verificada", obs)
        else:
            filas.append({"origen": origen, "relacion": "modifica", "destino": PC, "tipo_cambio": PC,
                          "detalle": (etiqueta + cab)[:300], "fecha_vigencia": PC, "base_vigencia": PC,
                          "fuente_url": url, "fuente_id_parte": id_parte, "fecha_consulta": fecha_consulta,
                          "estado": "inferida", "observaciones": "motivo: no se pudo determinar artículo o verbo"})
    resumen = {"norma": norma, "id_parte": id_parte, "numerales": len(items), "truncado": truncado,
               "fecha_version_bcn": parte.attrib.get("fechaVersion", PC), "derogado": parte.attrib.get("derogado", PC),
               "ultimo_numeral": items[-1]["n"] if items else None}
    return filas, list(arts), origen, id_parte, norm_ws(texto), resumen


def implementa_res156(fecha_consulta):
    root = cargar("res_156_2025")
    meta = ident(root)
    for ef, txt, _ in partes(root):
        t = norm_ws(txt)
        if re.search(r"implementaci[oó]n del mecanismo", t) and \
                re.search(r"art[íi]culo\s+91\s*[°º]?\s*bis de la Ley General de Servicios El[ée]ctricos", t):
            frase = re.search(r"[^.]*implementaci[oó]n del mecanismo[^.]*\.", t).group(0)
            return {
                "origen": "res_156_2025", "relacion": "implementa", "destino": "ley_dfl4_2006__art_91_bis",
                "tipo_cambio": "", "detalle": frase[:300], "fecha_vigencia": meta["fecha_publicacion"],
                "base_vigencia": "fecha_publicacion de la resolución",
                "fuente_url": f"https://www.leychile.cl/Consulta/obtxml?opt=7&idNorma={meta['id_bcn']}",
                "fuente_id_parte": ef.attrib["idParte"], "fecha_consulta": fecha_consulta,
                "estado": "verificada",
                "observaciones": "texto literal: implementación del mecanismo regulado en el artículo 91º bis "
                                 "de la LGSE; el 91 bis es artículo del DFL 4 incorporado por Ley 21.721 N° 4",
            }, ef.attrib["idParte"]
    raise SystemExit("No se encontró en la Res. 156 la mención literal a la implementación del art. 91 bis")


# ---------------------------------------------------------------- escritura
def main():
    with open(os.path.join(RAW, "descargas.csv"), encoding="utf-8") as f:
        consultas = {r["nodo"]: r["fecha_consulta"] for r in csv.DictReader(f)}
    dfl4 = indice_dfl4()
    filas, arts_dfl4, origenes, resumenes = [], [], [], []
    for norma in ("ley_21721_2024", "ley_20936_2016"):
        fs, arts, origen, idp, texto, res = extraer_ley(norma, dfl4, consultas[norma])
        filas += fs
        arts_dfl4 += [a for a in arts if a not in arts_dfl4]
        origenes.append((origen, norma, idp, texto))
        resumenes.append(res)
    imp, _ = implementa_res156(consultas["res_156_2025"])
    filas.append(imp)
    if "91 bis" not in arts_dfl4:
        arts_dfl4.append("91 bis")

    # nodos_articulos.csv
    ca = ["id", "tipo", "norma_contenedora", "numero", "id_parte", "url_fuente", "fecha_version_bcn",
          "vigente_desde", "vigente_hasta", "derogado", "estado_extraccion", "texto"]
    nodos = []
    for (origen, norma, idp, texto), res in zip(origenes, resumenes):
        nodos.append({"id": origen, "tipo": "articulo", "norma_contenedora": norma,
                      "numero": "único" if origen.endswith("unico") else "1", "id_parte": idp,
                      "url_fuente": f"https://www.bcn.cl/leychile/navegar?idNorma={ident(cargar(norma))['id_bcn']}&idParte={idp}",
                      "fecha_version_bcn": res["fecha_version_bcn"], "vigente_desde": PC, "vigente_hasta": "",
                      "derogado": res["derogado"],
                      "estado_extraccion": "xml_bcn_truncado" if res["truncado"] else "xml_bcn",
                      "texto": texto})
    for a in sorted(arts_dfl4, key=lambda k: [int(x) if x.isdigit() else x for x in re.split(r"[- ]", k)]):
        info = dfl4.get(a)
        nodos.append({
            "id": id_art("ley_dfl4_2006", a), "tipo": "articulo", "norma_contenedora": "ley_dfl4_2006",
            "numero": a, "id_parte": info["id_parte"] if info else PC,
            "url_fuente": f"https://www.bcn.cl/leychile/navegar?idNorma=258171&idParte={info['id_parte']}" if info else PC,
            "fecha_version_bcn": info["fecha_version_bcn"] if info else PC,
            "vigente_desde": PC, "vigente_hasta": info["fecha_derogacion"] if info else PC,
            "derogado": info["derogado"] if info else PC,
            "estado_extraccion": "xml_bcn_texto_vigente" if info else "no_encontrado_en_xml",
            "texto": info["texto"] if info else PC,
        })
    with open(os.path.join(ONT, "nodos_articulos.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=ca)
        w.writeheader()
        w.writerows(nodos)

    # contiene (norma -> articulo): sale de la estructura del XML (EstructuraFuncional/idParte)
    ids_bcn = {n: ident(cargar(n))["id_bcn"] for n in ARCHIVOS}
    for n in nodos:
        if n["id_parte"] == PC:
            continue
        norma = n["norma_contenedora"]
        filas.append({
            "origen": norma, "relacion": "contiene", "destino": n["id"], "tipo_cambio": "",
            "detalle": f"EstructuraFuncional tipoParte=Artículo idParte={n['id_parte']} (artículo {n['numero']})",
            "fecha_vigencia": "", "base_vigencia": "",
            "fuente_url": f"https://www.leychile.cl/Consulta/obtxml?opt=7&idNorma={ids_bcn[norma]}",
            "fuente_id_parte": n["id_parte"], "fecha_consulta": consultas[norma],
            "estado": "verificada", "observaciones": "",
        })

    campos = ["origen", "relacion", "destino", "tipo_cambio", "detalle", "fecha_vigencia", "base_vigencia",
              "fuente_url", "fuente_id_parte", "fecha_consulta", "estado", "metodo", "observaciones"]
    for r in filas:
        r["metodo"] = "regla"  # todo este script es determinista (XML + regex)
        assert r["fuente_url"] and r["fuente_id_parte"], f"relación sin fuente: {r}"
    with open(os.path.join(ONT, "relaciones.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(filas)

    # nodos_normas.csv: completar desde el XML, conservando columnas existentes
    path = os.path.join(ONT, "nodos_normas.csv")
    with open(path, encoding="utf-8") as f:
        normas = list(csv.DictReader(f))
    extra = ["fecha_promulgacion", "fecha_publicacion", "estado_vigencia", "titulo", "organismo_bcn", "tipo_numero_bcn"]
    cn = list(normas[0].keys()) + [c for c in extra if c not in normas[0]]
    for n in normas:
        m = ident(cargar(n["id"]))
        n.update({"id_bcn": m["id_bcn"], "url_fuente": f"https://www.bcn.cl/leychile/navegar?idNorma={m['id_bcn']}",
                  "fecha_promulgacion": m["fecha_promulgacion"], "fecha_publicacion": m["fecha_publicacion"],
                  "estado_vigencia": m["derogado"], "titulo": m["titulo"], "organismo_bcn": m["organismo_bcn"],
                  "tipo_numero_bcn": m["tipo_numero_bcn"], "estado_extraccion": "id_bcn_verificado_en_xml"})
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cn)
        w.writeheader()
        w.writerows(normas)

    # Candidatos (NO son aristas): artículos del DFL 4 cuya fechaVersion BCN coincide con la
    # publicación de la ley modificatoria y que el texto truncado no permitió extraer.
    os.makedirs("datos/derivados", exist_ok=True)
    ya = {(r["origen"].split("__")[0], r["destino"]) for r in filas}
    cand = []
    for norma in ("ley_21721_2024", "ley_20936_2016"):
        fp = ident(cargar(norma))["fecha_publicacion"]
        for clave, info in dfl4.items():
            dest = id_art("ley_dfl4_2006", clave)
            if info["fecha_version_bcn"] == fp and (norma, dest) not in ya:
                cand.append({"norma_modificatoria": norma, "articulo_dfl4": dest,
                             "id_parte_dfl4": info["id_parte"], "fecha_version_bcn": info["fecha_version_bcn"],
                             "motivo": "fechaVersion BCN = fecha de publicación de la ley; texto modificatorio "
                                       "truncado en XML BCN; requiere verificar contra texto completo"})
    with open("datos/derivados/candidatos_por_fechaversion.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["norma_modificatoria", "articulo_dfl4", "id_parte_dfl4",
                                          "fecha_version_bcn", "motivo"])
        w.writeheader()
        w.writerows(cand)
    print("candidatos por fechaVersion:", Counter(c["norma_modificatoria"] for c in cand))

    for r in resumenes:
        print(r)
    print(Counter((r["origen"].split("__")[0], r["relacion"], r["estado"]) for r in filas))


if __name__ == "__main__":
    main()
