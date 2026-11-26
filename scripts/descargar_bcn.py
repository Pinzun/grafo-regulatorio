"""Descarga el XML crudo de las normas del piloto desde el servicio de exportación de Ley Chile (BCN).

Uso: python3 -I scripts/descargar_bcn.py [directorio_destino] [idNorma ...]
     Sin idNorma descarga todas; con idNorma solo esas (las demás filas de descargas.csv se conservan).

- Endpoint: https://www.leychile.cl/Consulta/obtxml?opt=7&idNorma=<id>
- El servicio aplica un límite de uso anónimo (responde una página HTML "API-KEY" en vez de XML);
  por eso se reintenta con espera y se valida que la respuesta sea XML con <Norma normaId=id>.
- Si existe la variable de entorno BCN_API_KEY se envía como cabecera (la nueva API de la BCN la exige).
- Escribe además datos/raw/descargas.csv con idNorma, url, fecha de consulta y sha256.
"""
import csv
import datetime as dt
import hashlib
import os
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

NORMAS = {
    "258171": "ley_dfl4_2006",
    "1092695": "ley_20936_2016",
    "1209692": "ley_21721_2024",
    "1212350": "res_156_2025",
    "1221363": "ley_21804_2026",
    "1184572": "ley_21505_2022",
    "1194043": "ley_21582_2023",
    "1226550": "ley_21833_2026",
    "1179524": "ley_21472_2022",
    "1203005": "ley_21667_2024",
    "1055073": "ley_20701_2013",
    "1154423": "ley_21304_2021",
    "1140301": "ley_21194_2019",
    "1074277": "ley_20805_2015",
    "1008692": "ley_20402_2009",
}
URL = "https://www.leychile.cl/Consulta/obtxml?opt=7&idNorma={}"
NS = "{http://www.leychile.cl/esquemas}"


def bajar(id_norma, intentos=6):
    url = URL.format(id_norma)
    headers = {"User-Agent": "Mozilla/5.0 (grafo-regulatorio)"}
    if os.environ.get("BCN_API_KEY"):
        headers["api-key"] = os.environ["BCN_API_KEY"]
    for k in range(intentos):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=180) as r:
                data = r.read()
        except urllib.error.HTTPError as e:
            if e.code not in (401, 429):  # 401/429: límite de uso anónimo; se espera, no se evita
                raise
            data = b""
        try:
            root = ET.fromstring(data)
            if root.tag == NS + "Norma" and root.attrib.get("normaId") == id_norma:
                return url, data
        except ET.ParseError:
            pass
        espera = 30 * (k + 1)
        print(f"  {id_norma}: respuesta no XML (límite de uso), reintento en {espera}s", file=sys.stderr)
        time.sleep(espera)
    raise SystemExit(f"No se pudo descargar idNorma={id_norma}")


def main():
    destino = sys.argv[1] if len(sys.argv) > 1 else "datos/raw"
    pedidas = sys.argv[2:] or list(NORMAS)
    desconocidas = [i for i in pedidas if i not in NORMAS]
    if desconocidas:
        raise SystemExit(f"idNorma sin nodo en NORMAS: {desconocidas}")
    os.makedirs(destino, exist_ok=True)
    reg = os.path.join(destino, "descargas.csv")
    previas = []
    if os.path.exists(reg):
        with open(reg, encoding="utf-8") as f:
            previas = [r for r in csv.DictReader(f) if r["id_norma"] not in pedidas]
    filas = []
    for id_norma in pedidas:
        nodo = NORMAS[id_norma]
        url, data = bajar(id_norma)
        nombre = f"{nodo}__idNorma_{id_norma}.xml"
        with open(os.path.join(destino, nombre), "wb") as f:
            f.write(data)
        filas.append({
            "id_norma": id_norma, "nodo": nodo, "archivo": nombre, "url": url,
            "fecha_consulta": dt.date.today().isoformat(),
            "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
        })
        print(f"OK {nombre} ({len(data)} bytes)")
    orden = list(NORMAS)
    todas = sorted(previas + filas, key=lambda r: orden.index(r["id_norma"]) if r["id_norma"] in orden else 99)
    with open(reg, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(todas)


if __name__ == "__main__":
    main()
