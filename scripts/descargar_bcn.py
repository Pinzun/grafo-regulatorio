"""Descarga el XML crudo de las normas del piloto desde el servicio de exportación de Ley Chile (BCN).

Uso: python3 -I scripts/descargar_bcn.py [directorio_destino]

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
import urllib.request
import xml.etree.ElementTree as ET

NORMAS = {
    "258171": "ley_dfl4_2006",
    "1092695": "ley_20936_2016",
    "1209692": "ley_21721_2024",
    "1212350": "res_156_2025",
}
URL = "https://www.leychile.cl/Consulta/obtxml?opt=7&idNorma={}"
NS = "{http://www.leychile.cl/esquemas}"


def bajar(id_norma, intentos=6):
    url = URL.format(id_norma)
    headers = {"User-Agent": "Mozilla/5.0 (grafo-regulatorio)"}
    if os.environ.get("BCN_API_KEY"):
        headers["api-key"] = os.environ["BCN_API_KEY"]
    for k in range(intentos):
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=180) as r:
            data = r.read()
        try:
            root = ET.fromstring(data)
            if root.tag == NS + "Norma" and root.attrib.get("normaId") == id_norma:
                return url, data
        except ET.ParseError:
            pass
        espera = 10 * (k + 1)
        print(f"  {id_norma}: respuesta no XML (límite de uso), reintento en {espera}s", file=sys.stderr)
        time.sleep(espera)
    raise SystemExit(f"No se pudo descargar idNorma={id_norma}")


def main():
    destino = sys.argv[1] if len(sys.argv) > 1 else "datos/raw"
    os.makedirs(destino, exist_ok=True)
    filas = []
    for id_norma, nodo in NORMAS.items():
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
    with open(os.path.join(destino, "descargas.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)


if __name__ == "__main__":
    main()
