"""Extrae las imágenes incrustadas (<aem:ArchivoBinario>) en los artículos de las normas del grafo.

Uso: python3 -I scripts/extraer_imagenes.py

El XML de Ley Chile incrusta algunas tablas y fórmulas como imagen dentro de <Texto> (ver
extraer_modificaciones.cortado_en_imagen). Este script las decodifica (base64) y escribe:

  datos/raw/imagenes/<norma>__art_<n>__img<k>.jpg   k = orden de la imagen dentro del artículo (1, 2, …)
  datos/raw/imagenes/imagenes.csv                    una fila por imagen: norma, artículo, idParte, k,
                                                     nombre original, tipo, bytes, sha256 y el texto que
                                                     la precede (para ubicarla en el artículo)

Determinista: mismos XML, mismos archivos. Recorre todas las normas de ARCHIVOS (DFL 4 y leyes).
"""
import base64
import csv
import hashlib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extraer_modificaciones as E  # noqa: E402

DIR = "datos/raw/imagenes"
AEM = "{http://valida.aem.gob.cl}"
CAMPOS = ["archivo", "norma", "articulo", "id_parte", "k", "nombre_original", "tipo_contenido", "bytes",
          "sha256", "texto_previo"]


def clave_articulo(nombre):
    """'157' -> '157'; 'ÚNICO' -> 'unico'; 'VIGESIMOQUINTO' -> 'vigesimoquinto'; '72-1' -> '72-1'."""
    n = nombre.strip().lower()
    for a, b in (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("º", ""), ("°", "")):
        n = n.replace(a, b)
    return re.sub(r"\s+", "_", re.sub(r"\s*-\s*", "-", n)).strip("_")


def imagenes_de(norma):
    """[(ef, clave, k, elemento ArchivoBinario, texto previo)] de los artículos de la norma."""
    out = []
    for ef, _, nombre in E.partes(E.cargar(norma)):
        t = ef.find(E.NS + "Texto")
        if ef.attrib.get("tipoParte") != "Artículo" or t is None:
            continue
        previo = t.text or ""
        k = 0
        for c in t:
            if c.tag.endswith("ArchivoBinario"):
                k += 1
                out.append((ef, clave_articulo(nombre), k, c, E.norm_ws(previo)[-200:]))
            previo = c.tail or ""
    return out


def archivo_de(norma, clave, k):
    return f"{norma}__art_{clave}__img{k}.jpg"


def main():
    os.makedirs(DIR, exist_ok=True)
    filas, escritos = [], set()
    for norma in E.ARCHIVOS:
        for ef, clave, k, c, previo in imagenes_de(norma):
            tipo = c.findtext(AEM + "TipoContenido") or ""
            if tipo != "image/jpeg":
                raise SystemExit(f"{norma} art. {clave}: tipo {tipo!r} no es JPEG; revisar la extensión")
            datos = base64.b64decode("".join((c.findtext(AEM + "DataCodificada") or "").split()))
            declarados = c.findtext(AEM + "CantidadBytes")
            if declarados and int(declarados) != len(datos):
                raise SystemExit(f"{norma} art. {clave} img{k}: {len(datos)} bytes, el XML declara {declarados}")
            nombre = archivo_de(norma, clave, k)
            with open(os.path.join(DIR, nombre), "wb") as f:
                f.write(datos)
            escritos.add(nombre)
            filas.append({"archivo": nombre, "norma": norma, "articulo": clave, "id_parte": ef.attrib["idParte"],
                          "k": k, "nombre_original": c.findtext(AEM + "Nombre") or "", "tipo_contenido": tipo,
                          "bytes": len(datos), "sha256": hashlib.sha256(datos).hexdigest(), "texto_previo": previo})
    for viejo in os.listdir(DIR):  # imágenes que ya no están en los XML
        if viejo.endswith(".jpg") and viejo not in escritos:
            os.remove(os.path.join(DIR, viejo))
    with open(os.path.join(DIR, "imagenes.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        w.writerows(filas)
    arts = sorted({(r["norma"], r["articulo"]) for r in filas})
    print(f"{DIR}: {len(filas)} imágenes en {len(arts)} artículos")
    for n, a in arts:
        print(f"  {n} art. {a}: {sum(1 for r in filas if (r['norma'], r['articulo']) == (n, a))}")


if __name__ == "__main__":
    main()
