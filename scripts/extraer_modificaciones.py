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
    "ley_21804_2026": "ley_21804_2026__idNorma_1221363.xml",
    "res_156_2025": "res_156_2025__idNorma_1212350.xml",
    "ley_21505_2022": "ley_21505_2022__idNorma_1184572.xml",
    "ley_21582_2023": "ley_21582_2023__idNorma_1194043.xml",
    "ley_21833_2026": "ley_21833_2026__idNorma_1226550.xml",
}
# Artículo de cada ley que contiene las modificaciones al DFL 4 (se valida por regex abajo).
MODIFICATORIAS = {"ley_21721_2024": "art_unico", "ley_20936_2016": "art_1", "ley_21804_2026": "art_unico",
                  "ley_21505_2022": "art_unico", "ley_21582_2023": "art_10", "ley_21833_2026": "art_1"}

VERBOS = {  # singular e impersonal plural ("Reemplázase" / "Reemplázanse")
    "reemplaza": r"reempl[aá]z(?:a|ase|anse|ese|ense)|sustit[uú]y(?:e|ese|ense)",
    "agrega": r"agr[eé]g(?:a|ase|anse|uese|uense)|incorp[oó]r(?:a|ase|anse|ese|ense)|interc[aá]l(?:a|ase|anse|ese|ense)|a[nñ][aá]d(?:e|ese|ense)",
    "elimina": r"elim[ií]n(?:a|ase|anse|ese|ense)|supr[ií]m(?:e|ese|ense)|der[oó]g(?:a|ase|anse|uese|uense)",
    "modifica_contenedor": r"modif[ií]c(?:a|ase|anse|ese|ense)",
}
RE_VERBO = re.compile(r"\b(" + "|".join(VERBOS.values()) + r")\b", re.I)
SUFIJOS = r"bis|ter|qu[aá]ter|quinquies|sexies|septies|octies|nonies|decies"
RE_ART = re.compile(r"art[íi]culos?\s+(\d+)\s*[°º]?\s*(?:-\s*(\d+))?\s*(" + SUFIJOS + r")?\b", re.I)
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
        n = nombre.lower().replace("º", "").replace("°", "").replace("á", "a")
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


# ---------------------------------------------------------------- texto completo desde el PDF oficial
PDF_DIR = "datos/raw/pdf"
NO_ARTICULO = []  # modificaciones que no recaen en un artículo (p. ej. epígrafes de capítulos)
LETRAS = "abcdefghijklmnñopqrstuvwxyz"
ROMANOS = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x", "xi", "xii"]


def solo_letras(s):
    return re.sub(r"[^0-9a-záéíóúñü]+", "", s.lower())


def pdf_de(id_bcn):
    """Markdown (sin notas BCN), url, sha256 y fecha del PDF oficial registrado en descargas_pdf.csv."""
    reg = os.path.join(PDF_DIR, "descargas_pdf.csv")
    if not os.path.exists(reg):
        return None
    with open(reg, encoding="utf-8") as f:
        fila = next((r for r in csv.DictReader(f) if r["id_norma"] == id_bcn), None)
    if fila is None:
        return None
    md = os.path.join(PDF_DIR, fila["archivo"][:-4] + ".md")
    texto = open(md, encoding="utf-8").read()
    return {"md": texto, "cuerpo": re.sub(r"(?m)^> \[nota BCN\].*\n?", "", texto),
            "url": fila["url"], "sha256": fila["sha256"], "fecha": fila["fecha_descarga"], "archivo": md}


def articulo_en_pdf(cuerpo, texto_xml, texto_siguiente_xml):
    """Texto completo del artículo cuyo comienzo es `texto_xml` (truncado): desde el párrafo que contiene
    el inicio del XML hasta el párrafo donde empieza la parte siguiente del XML (`texto_siguiente_xml`).
    No se usa la paridad de comillas porque el artículo viene entre comillas envolventes que no se
    anidan con las de los textos que inserta. Exige que el XML sea prefijo exacto (solo letras)."""
    def ini(t):
        return solo_letras(t)[:80]
    pars = [p.strip() for p in re.split(r"\n\s*\n", cuerpo) if p.strip()]
    k = next((n for n, p in enumerate(pars) if solo_letras(p).startswith(ini(texto_xml))), None)
    if k is None:
        return None
    fin = next((n for n in range(k + 1, len(pars)) if solo_letras(pars[n]).startswith(ini(texto_siguiente_xml))), None)
    if fin is None:
        raise SystemExit("No se encontró en el PDF el comienzo de la parte siguiente del XML")
    texto = "\n\n".join(pars[k:fin])
    if not solo_letras(texto).startswith(solo_letras(texto_xml)):
        raise SystemExit("El texto del PDF no coincide con el XML (¿otra versión?): revise datos/raw/pdf")
    return texto


# ---------------------------------------------------------------- parser de numerales
def numerales(texto):
    """Árbol de numerales de primer nivel (fuera de texto citado, numeración correlativa), con literales
    a), b)… y sub-literales romanos i), ii)…, y el texto citado que insertan. Un numeral sin verbo
    ("En el artículo 96°:") es contenedor de sus literales."""
    items, actual, lit, comillas, esperado = [], None, None, 0, 1
    texto = re.sub(r'^\s*"', "", texto, count=1)  # comilla envolvente del artículo modificatorio
    truncado = not re.search(r'[.;:"”]\s*$', texto)
    previo = ""
    for p in parrafos(texto):
        fuera = comillas % 2 == 0
        # Resincronización: algunos textos abren comillas en cada artículo insertado y cierran solo al
        # final (Ley 21.804 N° 32), lo que desbalancea la paridad. Si el párrafo trae exactamente el
        # numeral correlativo esperado y el anterior cierra comillas, es un numeral de primer nivel.
        cierra_previo = bool(re.search(r'"\s*[.;]?\s*$', previo))
        m = RE_ITEM.match(p) if (fuera or cierra_previo) else None
        if m and not fuera and int(m.group(1)) != esperado:
            m = None
        previo = p
        if m and int(m.group(1)) == esperado and (
                RE_VERBO.search(sin_citas(m.group(2))[:90])
                or (re.match(r"En\s", m.group(2)) and m.group(2).rstrip().endswith(":") and RE_ART.search(m.group(2)))):
            # "todos": cada párrafo del numeral, para hallar encabezados "Artículo X.-" insertados aunque
            # las comillas del texto oficial estén desbalanceadas
            actual = {"n": esperado, "texto": m.group(2), "literales": [], "citado": [], "todos": []}
            items.append(actual)
            lit, esperado = None, esperado + 1
            comillas = p.count('"')  # se reinicia la paridad en cada numeral de primer nivel
            continue
        if actual is not None:
            actual["todos"].append(p)
        # literal "a)"; sub-literal romano "i)" o "i." (las letras siempre llevan paréntesis)
        # tolera la errata "a )" (espacio antes del paréntesis) presente en el texto oficial
        ml = re.match(r"^\s*([a-zñ]\s?\)|[ivx]+[.)])\s+(.*)", p, re.S) if (fuera and actual) else None
        if ml and (RE_VERBO.search(sin_citas(ml.group(2))[:90]) or ml.group(2).rstrip().endswith(":")):
            tok = ml.group(1)[:-1].strip()
            if ml.group(1).endswith(".") and tok not in ROMANOS:
                tok = None
            sig_letra = LETRAS[LETRAS.index(actual["literales"][-1]["l"]) + 1] if actual["literales"] else "a"
            sig_romano = ROMANOS[len(lit["sub"])] if lit is not None and len(lit["sub"]) < len(ROMANOS) else None
            solo_romano = ml.group(1).endswith(".")  # "i." con punto siempre es romano (Ley 21.505 N° 5 h)
            if tok == sig_letra and not solo_romano and not (lit is not None and lit["sub"] and tok == sig_romano):
                lit = {"l": tok, "texto": ml.group(2), "sub": []}
                actual["literales"].append(lit)
                comillas += p.count('"')
                continue
            if lit is not None and tok == sig_romano:
                lit["sub"].append({"l": tok, "texto": ml.group(2)})
                comillas += p.count('"')
                continue
        if actual is not None and (not fuera or p.startswith('"')):
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


def destinos_plurales(frase):
    """'Suprímense los artículos 137° y 138°' -> ['137', '138']; None si no es plural."""
    s = sin_citas(frase)
    m = re.search(r"\bart[íi]culos\s+((?:\d+\s*[°º]?\s*(?:-\s*\d+)?\s*(?:" + SUFIJOS + r")?\s*(?:,|y)?\s*)+)", s, re.I)
    if not m:
        return None
    return [clave_art(a, b, c) for a, b, c in re.findall(
        r"(\d+)\s*[°º]?\s*(?:-\s*(\d+))?\s*(" + SUFIJOS + r")?", m.group(1), re.I)]


# ---------------------------------------------------------------- extracción
RE_MODIFICA_LGSE = re.compile(
    r"^\W*Art[íi]culo\s+\S+?\s*\.\s*-\s*(?:Introd[uú]cense las siguientes modificaciones en|Modif[ií]case)\s+(?:el|la)\s+"
    r"(?:decreto con fuerza de ley N\s*[°º]\s*4/20\.?018"                                   # DFL 4 (texto refundido)
    r"|decreto con fuerza de ley N\s*[°º]\s*1,\s*de 1982,.{0,120}?Ley General de Servicios El[ée]ctricos"  # DFL 1/1982
    r"|ley General de Servicios El[ée]ctricos)", re.I)                                     # nombre de la ley


def modifica_lgse(txt):
    """¿El artículo modifica la LGSE? Las leyes la nombran de tres formas: 'DFL N° 4/20.018' (Leyes 20.936,
    21.721, 21.804, 21.833), 'DFL N° 1, de 1982, … Ley General de Servicios Eléctricos, … cuyo texto refundido
    … fue fijado por el DFL N° 4, de 2006' (Ley 21.582) o 'ley General de Servicios Eléctricos' (Ley 21.505).
    En los tres casos el texto vigente, y su numeración, es el del DFL 4."""
    t = norm_ws(txt)[:400]
    if not RE_MODIFICA_LGSE.search(t):
        return False
    if re.search(r"de 1982", t[:200]) and not re.search(r"4,\s*de 2006", t):
        return False  # DFL 1/1982 sin remisión al texto refundido: no se asume la numeración del DFL 4
    return True


def extraer_ley(norma, dfl4, fecha_consulta):
    root = cargar(norma)
    meta = ident(root)
    todas = list(partes(root))
    k = next(n for n, (ef, txt, _) in enumerate(todas)
             if ef.attrib.get("tipoParte") == "Artículo" and modifica_lgse(txt))
    parte = todas[k][0]
    texto_xml = parte.findtext(NS + "Texto")
    texto_sig = todas[k + 1][1] if k + 1 < len(todas) else ""
    id_parte = parte.attrib["idParte"]
    origen = f"{norma}__{MODIFICATORIAS[norma]}"
    url_xml = f"https://www.leychile.cl/Consulta/obtxml?opt=7&idNorma={meta['id_bcn']}"
    reglas = reglas_vigencia(root)
    _, truncado_xml = numerales(texto_xml)
    pdf = pdf_de(meta["id_bcn"]) if truncado_xml else None
    texto = articulo_en_pdf(pdf["cuerpo"], texto_xml, texto_sig) if pdf else None
    usa_pdf = texto is not None
    texto = texto or texto_xml
    xml_letras = solo_letras(texto_xml)
    items, truncado = numerales(texto)
    filas, arts = [], {}

    def fuente(it):
        """El numeral se cita al XML si está completo en él; si no, al PDF oficial."""
        bloque = " ".join([it["texto"]] + [l["texto"] for l in it["literales"]] + it["citado"])
        if not usa_pdf or solo_letras(bloque) in xml_letras:
            return url_xml, fecha_consulta, []
        return pdf["url"], pdf["fecha"], [f"texto del PDF oficial Ley Chile (sha256 {pdf['sha256'][:12]}…); "
                                          "el XML BCN está truncado en este punto"]

    def fila(it, destino, tipo, detalle, estado, obs):
        url, fecha, obs_f = fuente(it)
        obs = list(obs) + obs_f
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
            "fuente_url": url, "fuente_id_parte": id_parte, "fecha_consulta": fecha,
            "estado": estado, "observaciones": " | ".join(obs), "_numeral": it["n"],
        })
        arts[destino] = True

    def sin_resolver(it, detalle):
        url, fecha, obs_f = fuente(it)
        filas.append({"origen": origen, "relacion": "modifica", "destino": PC, "tipo_cambio": PC,
                      "detalle": detalle[:300], "fecha_vigencia": PC, "base_vigencia": PC,
                      "fuente_url": url, "fuente_id_parte": id_parte, "fecha_consulta": fecha,
                      "estado": "inferida", "_numeral": it["n"],
                      "observaciones": " | ".join(["motivo: no se pudo determinar artículo o verbo"] + obs_f)})

    def emitir(it, texto_hoja, etiqueta, dest_heredado):
        d, kind = destino_en(texto_hoja)
        d = d or dest_heredado
        acc = [(t, v) for t, v in acciones(texto_hoja) if t != "modifica_contenedor"]
        if not acc or not d:
            sin_resolver(it, etiqueta + texto_hoja)
            return
        for tipo, verbo in acc:
            plurales = destinos_plurales(texto_hoja) if tipo == "elimina" else None
            for dd in plurales or [d]:
                obs = ["artículo nuevo"] if kind == "nuevo" else []
                fila(it, dd, tipo, f"{etiqueta}[{verbo}]: {texto_hoja}", "verificada", obs)

    for it in items:
        cab = it["texto"]
        dest, kind = destino_en(cab)
        acc = acciones(cab)
        tipo0 = acc[0][0] if acc else None
        etiqueta = f"N° {it['n']}: "
        # Inserción o sustitución de un Título completo
        mt = re.search(r"(?:\bel\s+siguiente\s+|\bel\s+)(T[íi]tulo\s+[IVXL]+(?:\s+BIS)?)", sin_citas(cab), re.I)
        # Cambios a epígrafes de Título/Capítulo/Párrafo sin artículo: la ontología no tiene nodo para
        # ellos; se registran aparte en lugar de perderse.
        if dest is None and not mt and re.search(r"\bep[íi]grafe\b|\bCap[íi]tulo\b|\bT[íi]tulo\b|\bP[áa]rrafo\b", sin_citas(cab), re.I):
            NO_ARTICULO.append({"norma": norma, "numeral": it["n"], "id_parte": id_parte,
                                "tipo_cambio": tipo0 or PC, "texto": cab[:300]})
            continue
        # "los siguientes artículos X a Y" / "X y Y": inserción de varios artículos nuevos
        plural = re.search(r"\blos\s+siguientes\s+art[íi]culos\b", sin_citas(cab), re.I)
        if plural and not mt and tipo0 == "agrega":
            nuevos = []
            for p in it["todos"]:
                m = re.match(r'"?\s*' + RE_ART.pattern + r"\s*[°º]?\s*\.\s*-", p, re.I)
                if m:
                    nuevos.append(clave_art(*m.groups()))
            for a in nuevos:
                fila(it, a, "agrega", etiqueta + cab, "verificada", ["artículo nuevo (inserción de varios artículos)"])
            if not nuevos:
                sin_resolver(it, etiqueta + cab)
            continue
        if mt and (dest is None or kind != "nuevo"):
            titulo = mt.group(1)
            arts_cit = []
            for p in it["todos"]:
                m = re.match(r'"?\s*' + RE_ART.pattern + r"\s*[°º]?\s*\.\s*-", p, re.I)
                if m:
                    arts_cit.append(clave_art(*m.groups()))
            if not arts_cit:  # cambio a un Título sin artículos reconocibles: no se pierde en silencio
                NO_ARTICULO.append({"norma": norma, "numeral": it["n"], "id_parte": id_parte,
                                    "tipo_cambio": tipo0 or PC, "texto": cab[:300]})
                continue
            for i, a in enumerate(arts_cit):
                ultimo = truncado and it is items[-1] and i == len(arts_cit) - 1
                if tipo0 == "agrega":  # "Intercálase / Incorpórase el siguiente Título …": inserción
                    obs = [f"artículo contenido en el {titulo} nuevo que se intercala"]
                    if ultimo:
                        obs.append("texto del artículo truncado en la fuente")
                    fila(it, a, "agrega", etiqueta + cab, "inferida" if ultimo else "verificada", obs)
                else:
                    obs = [f"motivo: el N° {it['n']} sustituye el {titulo} completo; el texto no indica "
                           "correspondencia artículo a artículo (el artículo aparece en el texto sustituto)"]
                    if truncado and it is items[-1]:
                        obs.append("fuente truncada dentro de este numeral: lista de artículos incompleta")
                    fila(it, a, "reemplaza", etiqueta + cab, "inferida", obs)
            continue
        if it["literales"]:
            for lit in it["literales"]:
                d_lit = destino_en(lit["texto"])[0] or dest
                if lit["sub"]:
                    for sub in lit["sub"]:
                        emitir(it, sub["texto"], f"N° {it['n']} letra {lit['l']}) {sub['l']}) ", d_lit)
                else:
                    emitir(it, lit["texto"], f"N° {it['n']} letra {lit['l']}) ", dest)
            continue
        if dest and tipo0 in ("reemplaza", "agrega", "elimina"):
            emitir(it, cab, etiqueta, dest)
        else:
            sin_resolver(it, etiqueta + cab)
    resumen = {"norma": norma, "id_parte": id_parte, "numerales": len(items), "truncado": truncado,
               "truncado_xml": truncado_xml, "texto_pdf": usa_pdf,
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
def texto_truncado(txt):
    """Firma del corte observado en la BCN (docs/diagnostico_truncamiento_bcn.md): el texto termina
    a mitad de palabra, sin puntuación final, justo después de una letra acentuada (p. ej. 'Energí')."""
    t = txt.strip()
    return bool(re.search(r"[A-Za-záéíóúñÁÉÍÓÚÑ][áéíóúñ]$", t))


REVISIONES = os.path.join(ONT, "revisiones_manuales.csv")


def leer_revisiones():
    """Lee revisiones_manuales.csv tolerando lo que deja Excel en Windows: BOM y separador ';'."""
    if not os.path.exists(REVISIONES):
        return []
    with open(REVISIONES, encoding="utf-8-sig", newline="") as f:
        texto = f.read()
    sep = ";" if texto.splitlines()[0].count(";") > texto.splitlines()[0].count(",") else ","
    filas = list(csv.DictReader(texto.splitlines(), delimiter=sep))
    return [{k.strip(): (v or "").strip() for k, v in r.items() if k} for r in filas]


def aplicar_revisiones(filas):
    """Aplica ontologia/revisiones_manuales.csv sobre lo extraído, para que la revisión humana
    sobreviva a cada regeneración. Clave: (origen, relacion, destino); afecta a todas las filas del par.
    accion vacía -> pendiente de revisión (no cambia nada).
    accion = confirmar -> metodo manual, estado verificada, observaciones += revisión.
    accion = descartar -> la fila se elimina de relaciones.csv."""
    revs = leer_revisiones()
    usadas, out = set(), []
    for r in filas:
        k = (r["origen"], r["relacion"], r["destino"])
        rev = next((v for v in revs if (v["origen"], v["relacion"], v["destino"]) == k), None)
        if rev is None:
            out.append(r)
            continue
        usadas.add(k)
        accion = rev.get("accion", "").lower()
        if not accion:
            out.append(r)
            continue
        if accion not in ("confirmar", "descartar"):
            raise SystemExit(f"revisiones_manuales.csv: accion debe ser confirmar, descartar o vacía: {rev}")
        if not re.match(r"revisado: .+ \d{4}-\d{2}-\d{2}", rev.get("revision", "")):
            raise SystemExit(f"revisiones_manuales.csv: 'revision' debe ser 'revisado: <persona> <AAAA-MM-DD>': {rev}")
        if accion == "descartar":
            continue
        r = dict(r, metodo="manual", estado="verificada",
                 observaciones=" | ".join(x for x in (rev["revision"], rev.get("nota", ""), r["observaciones"]) if x))
        out.append(r)
    sobrantes = [v for v in revs if (v["origen"], v["relacion"], v["destino"]) not in usadas]
    if sobrantes:
        raise SystemExit(f"revisiones_manuales.csv: filas que no corresponden a ninguna relación extraída: {sobrantes}")
    return out


def notas_bcn_dfl4():
    """Notas al margen de la BCN en el PDF del DFL 4, por artículo permanente:
    ({clave_articulo: [nota, ...]}, [claves en orden del texto]). Se corta en 'Disposiciones Transitorias'."""
    pdf = pdf_de("258171")
    if pdf is None:
        return {}, []
    md = pdf["md"].split("\nDisposiciones Transitorias\n")[0]
    notas, actual, orden = {}, None, []
    for ln in md.splitlines():
        m = re.match(r'^Art[íi]culo\s+(\d+)\s*[°º]?\s*(?:-\s*(\d+))?\s*(' + SUFIJOS + r')?\s*\.\s*-', ln, re.I)
        if m:
            actual = clave_art(*m.groups())
            orden.append(actual)
        elif ln.startswith("> [nota BCN] ") and actual:
            notas.setdefault(actual, []).append(ln[len("> [nota BCN] "):].strip())
    return notas, orden


RE_NOTA = re.compile(r"Ley\s+(\d{5})\s+Art\.\s*(\S+?)\s+N[°º]\s*(\d+)", re.I)
LEY_DE = {n: re.match(r"ley_(\d+)_", n).group(1) for n in MODIFICATORIAS}  # nodo -> número en notas BCN


def contrastar_notas(filas):
    """Corrobora cada arista modifica con las notas BCN del DFL 4 (mismo artículo, ley y numeral) y
    escribe datos/derivados/contraste_notas_bcn.csv con las diferencias en ambos sentidos.
    Las notas son anotaciones de la BCN, no texto de la norma: corroboran, no crean aristas."""
    notas, orden = notas_bcn_dfl4()
    if not notas:
        return
    pos = {a: i for i, a in enumerate(orden)}

    def vecinos(art):
        i = pos.get(art)
        return [] if i is None else [orden[j] for j in (i - 1, i + 1) if 0 <= j < len(orden)]
    def art_ley(t):  # "único," / "ÚNICO" / "1" / "10," -> "unico" / "1" / "10"
        t = t.lower().strip(",.;")
        return t.replace("ú", "u")

    idx = {}  # ("ley:artículo de la ley", artículo DFL 4, numeral) -> nota
    for art, ns in notas.items():
        for n in ns:
            for m in RE_NOTA.finditer(n):
                idx.setdefault((f"{m.group(1)}:{art_ley(m.group(2))}", art, int(m.group(3))), n)
    vistos, usados, sin_nota = set(), set(), set()
    for r in filas:
        norma_o = r["origen"].split("__")[0]
        ley = LEY_DE.get(norma_o)
        if r["relacion"] != "modifica" or not ley or r["destino"] == PC:
            continue
        ley = f"{ley}:{MODIFICATORIAS[norma_o].removeprefix('art_')}"  # incluye el artículo de la ley
        art = r["destino"].split("__art_")[1].replace("_", " ")
        k = (ley, art, r.get("_numeral"))
        vistos.add(k)
        if k in idx:
            usados.add(k)
            r["observaciones"] = " | ".join(x for x in (r["observaciones"], f"corroborado por nota BCN del DFL 4: '{idx[k]}'") if x)
        else:
            kv = next(((ley, v, k[2]) for v in vecinos(art) if (ley, v, k[2]) in idx), None)
            if kv:
                usados.add(kv)
                r["observaciones"] = " | ".join(x for x in (r["observaciones"],
                    f"corroborado por nota BCN del DFL 4 en artículo contiguo ({kv[1]}): '{idx[kv]}'") if x)
            else:
                sin_nota.add(k)
    out = []
    for (ley, art, num), n in sorted(idx.items(), key=lambda kv: (kv[0][0], kv[0][2], kv[0][1])):
        if ley.split(":")[0] in LEY_DE.values() and (ley, art, num) not in usados:
            out.append({"ley": ley, "articulo_dfl4": art, "numeral": num, "tipo": "nota_sin_arista",
                        "nota_bcn": n, "comentario": "la BCN anota este cambio y no se extrajo arista; revisar"})
    for (ley, art, num) in sorted(sin_nota, key=lambda k: (k[0], k[2] or 0, k[1])):
        if True:
            out.append({"ley": ley, "articulo_dfl4": art, "numeral": num, "tipo": "arista_sin_nota", "nota_bcn": "",
                        "comentario": "sin nota BCN en el texto vigente (puede haberse reemplazado después)"})
    with open("datos/derivados/contraste_notas_bcn.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["ley", "articulo_dfl4", "numeral", "tipo", "nota_bcn", "comentario"])
        w.writeheader()
        w.writerows(out)
    from collections import Counter as C
    print("contraste notas BCN:", dict(C((o["ley"], o["tipo"]) for o in out)),
          "| corroboradas:", sum("corroborado por nota BCN" in r["observaciones"] for r in filas),
          "(contiguas:", sum("artículo contiguo" in r["observaciones"] for r in filas), ")")


def main():
    with open(os.path.join(RAW, "descargas.csv"), encoding="utf-8") as f:
        consultas = {r["nodo"]: r["fecha_consulta"] for r in csv.DictReader(f)}
    dfl4 = indice_dfl4()
    filas, arts_dfl4, origenes, resumenes = [], [], [], []
    for norma in MODIFICATORIAS:
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
                      "estado_extraccion": ("pdf_bcn_texto_completo (xml truncado)" if res["texto_pdf"]
                                            else "xml_bcn_truncado" if res["truncado"] else "xml_bcn"),
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

    for r in filas:
        r["metodo"] = "regla"  # lo extraído por este script es determinista (XML + regex)
        assert r["fuente_url"] and r["fuente_id_parte"], f"relación sin fuente: {r}"
    os.makedirs("datos/derivados", exist_ok=True)
    contrastar_notas(filas)
    filas = aplicar_revisiones(filas)
    campos = ["origen", "relacion", "destino", "tipo_cambio", "detalle", "fecha_vigencia", "base_vigencia",
              "fuente_url", "fuente_id_parte", "fecha_consulta", "estado", "metodo", "observaciones"]
    with open(os.path.join(ONT, "relaciones.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
        w.writeheader()
        w.writerows(filas)

    # Candidatos (NO son aristas): artículos del DFL 4 cuya fechaVersion BCN coincide con la
    # publicación de la ley modificatoria y que el texto truncado no permitió extraer.
    os.makedirs("datos/derivados", exist_ok=True)
    ya = {(r["origen"].split("__")[0], r["destino"]) for r in filas}
    cand = []
    for norma in MODIFICATORIAS:
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
    pendientes = Counter(c["norma_modificatoria"] for c in cand)
    with open("datos/derivados/modificaciones_no_articulo.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["norma", "numeral", "id_parte", "tipo_cambio", "texto"])
        w.writeheader()
        w.writerows(NO_ARTICULO)
    print("modificaciones que no recaen en artículos:", [(x["norma"], x["numeral"]) for x in NO_ARTICULO])
    print("candidatos por fechaVersion:", dict(pendientes))

    # nodos_normas.csv: completar desde el XML, conservando columnas existentes
    path = os.path.join(ONT, "nodos_normas.csv")
    with open(path, encoding="utf-8") as f:
        normas = list(csv.DictReader(f))
    extra = ["fecha_promulgacion", "fecha_publicacion", "estado_vigencia", "titulo", "organismo_bcn",
             "tipo_numero_bcn", "cobertura", "modificaciones_pendientes", "articulos_truncados",
             "articulos_truncados_recuperados_pdf", "pdf_sha256"]
    cn = list(normas[0].keys()) + [c for c in extra if c not in normas[0]]
    for n in normas:
        root = cargar(n["id"])
        m = ident(root)
        pdf = pdf_de(m["id_bcn"])
        pdf_letras = solo_letras(pdf["cuerpo"]) if pdf else ""
        trunc, recup = [], []
        for ef, txt, _ in partes(root):
            if ef.attrib.get("tipoParte") == "Artículo" and texto_truncado(txt):
                # recuperado si el texto truncado del XML aparece en el PDF oficial (que lo continúa)
                (recup if pdf and solo_letras(txt) in pdf_letras else trunc).append(ef.attrib["idParte"])
        pend = pendientes.get(n["id"], 0)
        n.update({"id_bcn": m["id_bcn"], "url_fuente": f"https://www.bcn.cl/leychile/navegar?idNorma={m['id_bcn']}",
                  "fecha_promulgacion": m["fecha_promulgacion"], "fecha_publicacion": m["fecha_publicacion"],
                  "estado_vigencia": m["derogado"], "titulo": m["titulo"], "organismo_bcn": m["organismo_bcn"],
                  "tipo_numero_bcn": m["tipo_numero_bcn"], "estado_extraccion": "id_bcn_verificado_en_xml",
                  "cobertura": "parcial" if pend or trunc else "completa",
                  "modificaciones_pendientes": str(pend), "articulos_truncados": ";".join(trunc),
                  "articulos_truncados_recuperados_pdf": ";".join(recup),
                  "pdf_sha256": pdf["sha256"] if pdf else ""})
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cn)
        w.writeheader()
        w.writerows(normas)
    for n in normas:
        print(f"cobertura {n['id']}: {n['cobertura']} (pendientes={n['modificaciones_pendientes']}, "
              f"truncados={n['articulos_truncados'] or '-'}, recuperados del PDF={n['articulos_truncados_recuperados_pdf'] or '-'})")

    for r in resumenes:
        print(r)
    print(Counter((r["origen"].split("__")[0], r["relacion"], r["estado"]) for r in filas))


if __name__ == "__main__":
    main()
