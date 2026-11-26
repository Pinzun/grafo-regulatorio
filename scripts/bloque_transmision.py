"""Propuesta del bloque de transmisión del DFL 4, para validación humana.

Uso: python3 -I scripts/bloque_transmision.py   (después de extraer_modificaciones.py)

Escribe datos/derivados/bloque_transmision.csv (separador ';' y BOM, para Excel) con los artículos
permanentes del DFL 4 agrupados por título y capítulo según la estructura del XML de Ley Chile:

  propuesta = nucleo       Título III "De los Sistemas de Transmisión Eléctrica" (todos sus capítulos).
  propuesta = relacionado  Título II BIS (coordinación y operación) y Título VI BIS (Coordinador).
  propuesta = revisar      artículo de otro título cuyo texto vigente menciona "transmisión" 3 o más
                           veces (conteo objetivo, no juicio).

La decisión es del usuario: columna `validado` (si / no) y `nota`. Al regenerar se conservan.
Incluye la cobertura de la historia de cada artículo (datos/derivados/historia_articulos.csv).
"""
import csv
import os
import re
import xml.etree.ElementTree as ET

NS = "{http://www.leychile.cl/esquemas}"
XML = "datos/raw/ley_dfl4_2006__idNorma_258171.xml"
SALIDA = "datos/derivados/bloque_transmision.csv"
HISTORIA = "datos/derivados/historia_articulos.csv"
CAMPOS = ["titulo", "capitulo", "articulo", "id_parte", "epigrafe", "propuesta", "criterio",
          "menciones_transmision", "en_grafo", "cobertura_historia", "leyes_faltantes", "validado", "nota"]
NUCLEO = re.compile(r"T[íi]tulo III\b", re.I)
RELACIONADO = re.compile(r"T[íi]tulo II BIS|T[íi]tulo VI BIS", re.I)
UMBRAL = 3


def ws(s):
    return " ".join((s or "").split())


def clave(nombre):
    n = nombre.lower().replace("º", "").replace("°", "").replace("á", "a")
    return re.sub(r"\s*-\s*", "-", re.sub(r"\s+", " ", n)).strip()


def epigrafe(texto):
    m = re.match(r"\s*Art[íi]culo\s+[^.]*?\.\s*-\s*(.+?)\.", ws(texto))
    return m.group(1)[:120] if m and len(m.group(1)) <= 120 else ""


def recorrer(el, titulo="", capitulo=""):
    efs = el.find(NS + "EstructurasFuncionales")
    if efs is None:
        return
    for ef in efs.findall(NS + "EstructuraFuncional"):
        tp, texto = ef.attrib["tipoParte"], ef.findtext(NS + "Texto") or ""
        if tp == "Título":
            yield from recorrer(ef, ws(texto), "")
        elif tp == "Capítulo":
            yield from recorrer(ef, titulo, ws(texto))
        elif tp == "Artículo" and ef.attrib.get("transitorio") != "transitorio":
            nombre = ef.findtext(NS + "Metadatos/" + NS + "NombreParte") or ""
            yield titulo, capitulo, clave(nombre), ef.attrib["idParte"], texto
            yield from recorrer(ef, titulo, capitulo)
        else:
            yield from recorrer(ef, titulo, capitulo)


def main():
    historia = {}
    if os.path.exists(HISTORIA):
        with open(HISTORIA, encoding="utf-8") as f:
            historia = {r["articulo"]: r for r in csv.DictReader(f)}
    previas = {}
    if os.path.exists(SALIDA):
        with open(SALIDA, encoding="utf-8-sig") as f:
            texto = f.read()
        sep = ";" if texto.splitlines()[0].count(";") > texto.splitlines()[0].count(",") else ","
        previas = {r["articulo"]: r for r in csv.DictReader(texto.splitlines(), delimiter=sep)}
    filas = []
    for titulo, capitulo, art, id_parte, texto in recorrer(ET.parse(XML).getroot()):
        if "Disposiciones Transitorias" in titulo:
            continue
        menciones = len(re.findall(r"transmisi[oó]n", texto, re.I))
        if NUCLEO.search(titulo):
            prop, crit = "nucleo", "Título III: De los Sistemas de Transmisión Eléctrica"
        elif RELACIONADO.search(titulo):
            prop, crit = "relacionado", f"{titulo[:60]}"
        elif menciones >= UMBRAL:
            prop, crit = "revisar", f"menciona 'transmisión' {menciones} veces fuera de los títulos de transmisión"
        else:
            continue
        h = historia.get(art, {})
        p = previas.get(art, {})
        filas.append({"titulo": titulo, "capitulo": capitulo, "articulo": art, "id_parte": id_parte,
                      "epigrafe": epigrafe(texto), "propuesta": prop, "criterio": crit,
                      "menciones_transmision": menciones, "en_grafo": h.get("en_grafo", ""),
                      "cobertura_historia": h.get("cobertura_historia", ""),
                      "leyes_faltantes": h.get("leyes_faltantes", ""),
                      "validado": p.get("validado", ""), "nota": p.get("nota", "")})
    with open(SALIDA, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS, delimiter=";")
        w.writeheader()
        w.writerows(filas)
    from collections import Counter
    print(f"{SALIDA}: {len(filas)} artículos", dict(Counter(r["propuesta"] for r in filas)))
    print("  incompletos por propuesta:",
          dict(Counter(r["propuesta"] for r in filas if r["cobertura_historia"] == "parcial")))


if __name__ == "__main__":
    main()
