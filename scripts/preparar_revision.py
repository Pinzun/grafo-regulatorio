"""Prepara ontologia/revisiones_manuales.csv para la revisión humana.

Uso: python3 -I scripts/preparar_revision.py

- Agrega una fila por cada arista `inferida` de relaciones.csv que aún no esté en la planilla, con
  `accion` vacía (= pendiente) y columnas de contexto para revisar sin abrir otros archivos.
- Conserva intactas las filas existentes y sus decisiones (confirmar / descartar).
- Escribe con separador ';' y BOM UTF-8 para que Excel (configuración es-CL) la abra en columnas y con
  tildes. El extractor acepta tanto ';' como ','.

Cómo revisar: en `accion` escriba confirmar o descartar; en `revision`, 'revisado: <persona> <AAAA-MM-DD>';
`nota` es opcional. Las columnas de contexto (detalle, motivo, fuente_id_parte) no se usan al aplicar.
Luego: python3 -I scripts/extraer_modificaciones.py && .venv/bin/python scripts/construir_grafo.py
"""
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extraer_modificaciones import REVISIONES, leer_revisiones  # noqa: E402

CAMPOS = ["origen", "relacion", "destino", "accion", "revision", "nota", "detalle", "motivo", "fuente_id_parte"]


def orden(fila):
    clave = fila["destino"].split("__art_")[-1]
    return (fila["origen"], [int(x) if x.isdigit() else x for x in re.split(r"[-_]", clave)])


def main():
    existentes = leer_revisiones()
    claves = {(r["origen"], r["relacion"], r["destino"]) for r in existentes}
    with open("ontologia/relaciones.csv", encoding="utf-8") as f:
        rels = list(csv.DictReader(f))
    nuevas = {}
    for r in rels:
        k = (r["origen"], r["relacion"], r["destino"])
        if r["estado"] != "inferida" or k in claves or k in nuevas:
            continue
        motivo = next((o for o in r["observaciones"].split(" | ") if o.startswith("motivo:")), r["observaciones"][:200])
        nuevas[k] = {"origen": k[0], "relacion": k[1], "destino": k[2], "accion": "", "revision": "", "nota": "",
                     "detalle": r["detalle"][:200], "motivo": motivo, "fuente_id_parte": r["fuente_id_parte"]}
    filas = [{c: r.get(c, "") for c in CAMPOS} for r in existentes] + sorted(nuevas.values(), key=orden)
    with open(REVISIONES, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS, delimiter=";")
        w.writeheader()
        w.writerows(filas)
    pend = sum(1 for r in filas if not r["accion"])
    print(f"{REVISIONES}: {len(filas)} filas ({len(nuevas)} nuevas; {pend} pendientes de revisión)")


if __name__ == "__main__":
    main()
