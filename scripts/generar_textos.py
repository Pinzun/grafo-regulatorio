"""Genera un Markdown por artículo del DFL 4 y un índice, de forma determinista (sin LLM).

Uso: python3 -I scripts/generar_textos.py     (lo llama también scripts/construir_grafo.py)

Salidas:
  textos/dfl4/art_<número>.md  encabezado (norma, versión BCN, idParte, vigencia, cobertura, bloque),
                               "Texto vigente" (XML del DFL 4, o PDF oficial si el XML lo trunca),
                               "Historia de modificaciones" (una línea por fila de relaciones.csv que llega
                               al artículo, ordenada por fecha de vigencia) y "Texto modificatorio" (numeral
                               literal de cada ley, del mismo texto XML/PDF que usó el extractor).
  textos/indice.md             una fila por artículo: bloque de transmisión validado primero, luego el resto.

Fuentes: datos/raw (XML y PDF), ontologia/*.csv, datos/derivados/{historia_articulos,bloque_transmision}.csv.
Solo artículos permanentes (los transitorios del DFL 4 repiten numeración y no tienen aristas).
La salida no lleva fecha de generación: regenerar sin cambios no produce diferencias.
"""
import csv
import glob
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extraer_modificaciones as E  # noqa: E402
from csv_a_graphify import etiqueta_norma  # noqa: E402

csv.field_size_limit(10_000_000)
SALIDA = "textos"
DIR_ART = os.path.join(SALIDA, "dfl4")
RE_ENCABEZADO = re.compile(r'^"?\s*Art[íi]culo\s+(\d+)\s*[°º]?\s*(?:-\s*(\d+))?\s*(' + E.SUFIJOS + r')?\s*[°º]?\s*\.\s*-', re.I)
RE_ELIMINADO = re.compile(r'^"?\s*Art[íi]culo\s+[^.]*?\.\s*-\s*(Eliminado|Suprimido|Derogado)\.?$', re.I)
RE_NUMERAL = re.compile(r"^(N° \d+(?: letra [a-zñ]\)(?: (?:[ivx]+|[a-zñ]\.\d+)\))?)?|letra [a-zñ]\)|texto completo)")


def leer(path, **kw):
    with open(path, encoding=kw.pop("encoding", "utf-8"), newline="") as f:
        return list(csv.DictReader(f, **kw))


def art_ley(suf):
    """'art_unico' -> 'art. único'; 'art_1' -> 'art. 1'; 'art_primero' -> 'art. primero'."""
    n = suf.removeprefix("art_")
    return "art. único" if n == "unico" else f"art. {n}"


def archivo(clave):
    return f"art_{clave.replace(' ', '_')}.md"


def orden_xml():
    """Artículos permanentes del DFL 4 en el orden del XML, con la parte siguiente (para recortar el PDF)."""
    todas = list(E.partes(E.cargar("ley_dfl4_2006")))
    idx = E.indice_dfl4()
    por_id = {v["id_parte"]: k for k, v in idx.items()}
    out = []
    for n, (ef, txt, _) in enumerate(todas):
        k = por_id.get(ef.attrib["idParte"])
        if k:
            out.append((k, txt, todas[n + 1][1] if n + 1 < len(todas) else ""))
    return idx, out


def recortar_pdf(cuerpo, txt, siguiente):
    """Artículo completo en el PDF. Primero delimita con la parte siguiente del XML (como el extractor); si
    esa parte no aparece igual en el PDF (p. ej. un encabezado de título), corta en el siguiente
    'Artículo …-' y exige igualmente que el XML truncado sea prefijo del resultado."""
    try:
        return E.articulo_en_pdf(cuerpo, txt, siguiente)
    except SystemExit:
        pars = [p.strip() for p in re.split(r"\n\s*\n", cuerpo) if p.strip()]
        ini = E.solo_letras(txt)[:80]
        k = next((n for n, p in enumerate(pars) if E.solo_letras(p).startswith(ini)), None)
        if k is None:
            return None
        fin = next((n for n in range(k + 1, len(pars))
                    if RE_ENCABEZADO.match(pars[n]) or re.match(r"(CAP[IÍ]TULO|Cap[íi]tulo|T[IÍ]TULO|T[íi]tulo)\b", pars[n])),
                   len(pars))
        texto = "\n\n".join(pars[k:fin])
        return texto if E.solo_letras(texto).startswith(E.solo_letras(txt)) else None


def texto_vigente(txt, siguiente, pdf_dfl4, cortado_en_imagen=False):
    if (E.texto_truncado(txt) or cortado_en_imagen) and pdf_dfl4:
        completo = recortar_pdf(pdf_dfl4["cuerpo"], txt, siguiente)
        if completo:
            motivo = ("el XML BCN incrusta una tabla como imagen y su texto se corta ahí; la tabla tampoco está "
                      "como texto en el PDF" if cortado_en_imagen else "el XML BCN trunca este artículo")
            return completo, f"PDF oficial Ley Chile (sha256 {pdf_dfl4['sha256'][:12]}…): {motivo}"
    return "\n\n".join(E.parrafos(txt)), "XML BCN del DFL 4 (servicio de exportación de Ley Chile)"


def seccion_tablas(info, articulo, imagenes, validadas, discrepancias, por_sha):
    """Sección 'Tabla (transcripción)' de un artículo cuyo texto trae tablas como imagen, y el estado de cada
    una ([(imagen, estado)]). Muestra la pasada 2 (lectura visual) con enlace a la imagen original."""
    imgs = imagenes.get(info["id_parte"], [])
    if not imgs:
        return [], []
    md = ["## Tabla (transcripción)", "",
          "*El texto oficial trae estas tablas como imagen (ni el XML ni el PDF las tienen como texto). Se "
          "transcribieron en dos pasadas independientes, OCR determinista (`scripts/transcribir_ocr.py`) y lectura "
          "visual con un LLM, comparadas celda por celda (`datos/derivados/transcripciones_discrepancias.csv`); se "
          "muestra la lectura visual. '←' = celda combinada con la de la izquierda; '↑' = con la de arriba. Una "
          "transcripción automática no es texto oficial: verifíquela contra la imagen antes de citarla.*", ""]
    estados = []
    for r in imgs:
        img = r["archivo"]
        estado = E.estado_transcripcion(articulo, img, validadas)
        estados.append((img, estado))
        disc = discrepancias.get(img, [])
        md += [f"### Tabla {r['k']} — imagen original: [{img}](../../datos/raw/imagenes/{img})", "",
               f"- **Estado:** {estado}",
               f"- **Ubicación en el artículo:** después de «…{r['texto_previo'][-90:]}»",
               f"- **Discrepancias OCR / lectura visual:** {len(disc)} celda(s)"
               + (": " + "; ".join(f"fila {d['fila']} col. {d['columna']}: OCR «{d['pasada1_ocr']}» / visual "
                                   f"«{d['pasada2_vision']}»" for d in disc[:8]) + (" …" if len(disc) > 8 else "")
                  if disc else "")]
        iguales = [x for x in por_sha.get(r["sha256"], []) if x != img]
        if iguales:
            md.append(f"- **Misma imagen (sha256) en:** {', '.join(iguales)}")
        md += ["", E.tabla_transcrita(img) or "*(sin transcripción: POR_COMPLETAR)*", ""]
    return md, estados


def numerales_por_ley():
    """{norma: {n: (item, fuente, url)}} leídos del mismo texto que usó el extractor."""
    out = {}
    for norma in E.MODIFICATORIAS:
        tm = E.texto_modificatorio(norma)
        items, _ = E.numerales(tm["texto"])
        url_xml = f"https://www.leychile.cl/Consulta/obtxml?opt=7&idNorma={tm['meta']['id_bcn']}"
        out[norma] = {}
        for it in items:
            f = E.fuente_numeral(it, tm)
            out[norma][it["n"]] = (it, f.upper(), tm["pdf"]["url"] if f == "pdf" else url_xml)
    return out


def bloque_articulo(it, clave):
    """Si el numeral inserta o sustituye varios artículos, devuelve solo los párrafos del artículo `clave`."""
    pars = it["todos"]
    heads = [i for i, p in enumerate(pars) if RE_ENCABEZADO.match(p)]
    if len(heads) < 2:
        return None
    for j, i in enumerate(heads):
        if E.clave_art(*RE_ENCABEZADO.match(pars[i]).groups()) == clave:
            fin = heads[j + 1] if j + 1 < len(heads) else len(pars)
            return pars[i:fin]
    return None


def main():
    idx, orden = orden_xml()
    pdf_dfl4 = E.pdf_de("258171")
    version_dfl4 = E.ident(E.cargar("ley_dfl4_2006"))["fecha_version_bcn"]
    normas = {n["id"]: n for n in leer("ontologia/nodos_normas.csv")}
    etiqueta = {k: etiqueta_norma(v) for k, v in normas.items()}
    nodos = {r["numero"]: r for r in leer("ontologia/nodos_articulos.csv") if r["norma_contenedora"] == "ley_dfl4_2006"}
    historia = {r["articulo"]: r for r in leer("datos/derivados/historia_articulos.csv")}
    bloque = {r["articulo"]: r for r in leer("datos/derivados/bloque_transmision.csv", encoding="utf-8-sig", delimiter=";")}
    entrantes, otras = defaultdict(list), defaultdict(list)
    for r in leer("ontologia/relaciones.csv"):
        if not r["destino"].startswith("ley_dfl4_2006__art_"):
            continue
        k = r["destino"].split("__art_")[1].replace("_", " ")
        if r["relacion"] in ("modifica", "deroga"):
            entrantes[k].append(r)
        elif r["relacion"] != "contiene":  # contiene (DFL 4 -> artículo) no aporta a la historia
            otras[k].append(r)
    nums = numerales_por_ley()
    imagenes = E.imagenes_por_parte()
    validadas = E.transcripciones_validadas()
    discrepancias, por_sha = defaultdict(list), defaultdict(list)
    if os.path.exists("datos/derivados/transcripciones_discrepancias.csv"):
        for d in leer("datos/derivados/transcripciones_discrepancias.csv"):
            discrepancias[d["imagen"]].append(d)
    for rs in imagenes.values():
        for r in rs:
            por_sha[r["sha256"]].append(r["archivo"])

    os.makedirs(DIR_ART, exist_ok=True)
    escritos, filas_indice, avisos = set(), [], defaultdict(list)
    validados = [o for o in orden if bloque.get(o[0], {}).get("validado") == "si"]
    resto = [o for o in orden if bloque.get(o[0], {}).get("validado") != "si"]
    for grupo, lista in (("bloque", validados), ("resto", resto)):
        for clave, txt, siguiente in lista:
            info, nodo, h, b = idx[clave], nodos.get(clave, {}), historia.get(clave, {}), bloque.get(clave)
            texto, fuente_texto = texto_vigente(txt, siguiente, pdf_dfl4, info.get("cortado_en_imagen", False))
            derogado = info["derogado"] == "derogado"
            # Texto consolidado reducido a "Eliminado / Suprimido / Derogado" aunque el XML no lo marque derogado
            eliminado_txt = bool(RE_ELIMINADO.match(E.norm_ws(texto))) and not derogado
            hasta = nodo.get("vigente_hasta") or info.get("fecha_derogacion") or ""
            if derogado:
                vigencia = f"derogado (vigente hasta {hasta})" if hasta else "derogado (fecha no informada por la BCN)"
            elif eliminado_txt:
                d = next((r for r in entrantes.get(clave, []) if r["relacion"] == "deroga"), None)
                vigencia = "eliminado según el texto consolidado (el XML BCN no lo marca derogado; " + (
                    f"arista deroga {d['estado']} de {etiqueta.get(d['origen'].split('__')[0], d['origen'])}, "
                    f"vigente hasta {d['fecha_vigencia']})" if d else "fecha no informada)")
            else:
                vigencia = "vigente"
            cob = nodo.get("cobertura_historia") or h.get("cobertura_historia", "POR_COMPLETAR")
            faltan = (nodo.get("leyes_faltantes") or h.get("leyes_faltantes", "")).split(";")
            faltan = [f"{l[:2]}.{l[2:]}" for l in faltan if l]
            if b and b["validado"] == "si":
                txt_bloque = f"{b['propuesta']} (validado) — {b['titulo']}" + (f" / {b['capitulo']}" if b["capitulo"] else "")
            elif b:
                txt_bloque = f"{b['propuesta']} (sin validar) — {b['titulo']}"
            else:
                txt_bloque = "fuera del bloque de transmisión"
            filas = sorted(entrantes.get(clave, []), key=lambda r: (r["fecha_vigencia"], r["origen"], r["detalle"]))
            ep = E.norm_ws(re.sub(r'^\s*"?Art[íi]culo\s+[^.]*?\.\s*-\s*', "", texto))
            epigrafe = ep.split(".")[0][:120] if len(ep.split(".")[0]) <= 120 else ""

            md = [f"# DFL 4 — artículo {clave}", "",
                  f"- **Norma:** {etiqueta['ley_dfl4_2006']} — {normas['ley_dfl4_2006'].get('titulo', '')}",
                  f"- **Versión del texto consolidado:** DFL 4 versión BCN {version_dfl4}; última versión de este artículo según la BCN: {info['fecha_version_bcn']}",
                  f"- **idParte:** {info['id_parte']} (https://www.bcn.cl/leychile/navegar?idNorma=258171&idParte={info['id_parte']})",
                  f"- **Vigencia:** {vigencia}",
                  f"- **Cobertura de la historia:** {cob}" + (f" — faltan en el grafo las leyes {', '.join(faltan)}" if faltan else ""),
                  f"- **Bloque:** {txt_bloque}", "",
                  "## Texto vigente", "", f"*Fuente: {fuente_texto}.*", "", texto or "*(sin texto)*", "",
                  ]
            tablas_md, estados = seccion_tablas(info, f"ley_dfl4_2006__art_{clave.replace(' ', '_')}", imagenes,
                                                validadas, discrepancias, por_sha)
            md += tablas_md + ["## Historia de modificaciones", ""]
            if filas:
                for r in filas:
                    num = RE_NUMERAL.match(r["detalle"]).group(1) or "numeral POR_COMPLETAR"
                    norma_o, art_o = r["origen"].split("__")
                    tipo = "deroga" if r["relacion"] == "deroga" else r["tipo_cambio"]
                    sup = re.search(r"superada: (\S+) (.+?) sustituyó el artículo completo \(([\d-]+)\)", r["observaciones"])
                    md.append(f"- {r['fecha_vigencia']} · {etiqueta.get(norma_o, norma_o)} ({art_ley(art_o)}) · {num} · "
                              f"{tipo} · {r['estado']} · {r['metodo']} · idParte {r['fuente_id_parte']}"
                              + (f" · **superada** por {etiqueta.get(sup.group(1), sup.group(1))} {sup.group(2)} "
                                 f"({sup.group(3)}), que sustituyó el artículo completo" if sup else ""))
            else:
                md.append("*Sin modificaciones registradas en el grafo.*")
            if faltan:
                md += ["", f"> ⚠️ Historia incompleta: la BCN anota modificaciones de las leyes {', '.join(faltan)}, que no están en el grafo."]
            elif not filas:
                md += ["", "> Texto original del DFL 4: la BCN no anota modificaciones posteriores a su publicación (2007-02-05)."]
            for r in sorted(otras.get(clave, []), key=lambda r: r["origen"]):
                md += ["", f"- Otra relación: {etiqueta.get(r['origen'], r['origen'])} **{r['relacion']}** este artículo "
                           f"({r['estado']}, {r['metodo']}, idParte {r['fuente_id_parte']})."]

            md += ["", "## Texto modificatorio", ""]
            vistos = set()
            for r in filas:
                norma_o = r["origen"].split("__")[0]
                mn = re.match(r"N° (\d+)|letra ([a-zñ])\)|texto completo", r["detalle"])
                n = (int(mn.group(1)) if mn.group(1) else E.LETRAS.index(mn.group(2)) + 1 if mn.group(2) else 1) if mn else None
                if (norma_o, n) in vistos or n is None:
                    continue
                vistos.add((norma_o, n))
                it, fuente, url = nums[norma_o][n]
                extracto = bloque_articulo(it, clave)
                md += [f"### {etiqueta[norma_o]} — {art_ley(E.MODIFICATORIAS[norma_o])}, {E.etiqueta_item(it)}", "",
                       f"*Fuente: {fuente} ({url}).*" + (" *Extracto: el numeral inserta o sustituye varios artículos; se "
                                                         "muestra solo el de este artículo.*" if extracto else ""), "",
                       (f"{it['etiqueta'].removeprefix('letra ')} {it['texto']}" if it.get("etiqueta", "").startswith("letra")
                        else it["texto"] if it.get("etiqueta") == "texto completo"
                        else f"{E.etiqueta_item(it)}. {it['texto']}"), ""]
                md += [p + "\n" for p in (extracto if extracto else it["todos"])]
            if not vistos:
                md.append("*No hay texto modificatorio: el artículo no tiene modificaciones en el grafo.*")

            nombre = archivo(clave)
            with open(os.path.join(DIR_ART, nombre), "w", encoding="utf-8") as f:
                f.write("\n".join(md).rstrip() + "\n")
            escritos.add(nombre)

            if eliminado_txt:
                avisos["eliminado_sin_marca"].append(clave)
            elif len(E.solo_letras(texto)) < 25 and not derogado:
                avisos["sin_texto"].append(clave)
            if faltan:
                avisos["historia_incompleta"].append(f"{clave} (faltan {', '.join(faltan)})")
            leyes = sorted({etiqueta[r["origen"].split("__")[0]].replace(" de ", " (").replace("(LGSE)", "") + ")"
                            for r in filas}, key=lambda s: re.sub(r"\D", "", s))
            if estados:
                val = sum(e.startswith("validada") for _, e in estados)
                avisos["tablas"].append(f"{clave} ({len(estados)} tabla(s), {val} validada(s))")
            filas_indice.append((grupo, b, clave, epigrafe, leyes, faltan, vigencia, nombre, estados))

    for viejo in glob.glob(os.path.join(DIR_ART, "art_*.md")):
        if os.path.basename(viejo) not in escritos:
            os.remove(viejo)

    ix = ["# Índice de artículos del DFL 4 (LGSE)", "",
          f"Texto consolidado: DFL 4, versión BCN {version_dfl4}. Generado por `scripts/generar_textos.py` desde "
          "los CSV de la ontología y los textos descargados (sin LLM; la única excepción son las transcripciones de "
          "tablas incrustadas como imagen, marcadas como tales). Primero el bloque de transmisión validado, "
          "luego el resto de los artículos permanentes.", ""]
    for grupo, titulo in (("bloque", "Bloque de transmisión (validado)"), ("resto", "Resto del DFL 4")):
        sel = [f for f in filas_indice if f[0] == grupo]
        ix += [f"## {titulo} ({len(sel)} artículos)", "",
               "| Art. | Epígrafe | Leyes que lo modificaron | Vigencia | Tablas (transcripción) |", "|---|---|---|---|---|"]
        for _, b, clave, ep, leyes, faltan, vig, nombre, estados in sel:
            ley_txt = ", ".join(leyes) or "—"
            if faltan:
                ley_txt += f" ⚠️ faltan {', '.join(faltan)}"
            tab = "—"
            if estados:
                val = sum(e.startswith("validada") for _, e in estados)
                tab = f"{len(estados)}: " + ("validadas" if val == len(estados) else
                                             f"{len(estados) - val} automática(s), sin validar")
            ix.append(f"| [{clave}](dfl4/{nombre}) | {ep.replace('|', '/') or '—'} | {ley_txt} | {vig} | {tab} |")
        ix.append("")
    ix += ["## Avisos", ""]
    ix.append(f"- Artículos con tablas incrustadas como imagen, transcritas (sección 'Tabla (transcripción)'): "
              f"{'; '.join(avisos['tablas']) or 'ninguno'}. Estado según ontologia/transcripciones_validadas.csv.")
    ix.append(f"- Artículos sin texto: {', '.join(avisos['sin_texto']) or 'ninguno'}.")
    ix.append(f"- Artículos cuyo texto consolidado dice solo 'Eliminado/Suprimido' sin marca de derogación en el XML BCN: "
              f"{', '.join(avisos['eliminado_sin_marca']) or 'ninguno'}.")
    ix.append(f"- Artículos con historia incompleta ({len(avisos['historia_incompleta'])}): "
              f"{'; '.join(avisos['historia_incompleta']) or 'ninguno'}.")
    with open(os.path.join(SALIDA, "indice.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(ix).rstrip() + "\n")

    print(f"textos: {len(escritos)} artículos ({len(validados)} del bloque validado, {len(resto)} resto)")
    print(f"  sin texto: {avisos['sin_texto'] or 'ninguno'}")
    print(f"  eliminados sin marca de derogación en el XML: {avisos['eliminado_sin_marca'] or 'ninguno'}")
    print(f"  historia incompleta: {len(avisos['historia_incompleta'])}"
          f" (del bloque validado: {sum(1 for f in filas_indice if f[0] == 'bloque' and f[5])})")


if __name__ == "__main__":
    main()
