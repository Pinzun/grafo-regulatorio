"""Compara celda por celda las dos pasadas independientes de cada tabla transcrita.

Uso: python3 -I scripts/comparar_transcripciones.py

  pasada 1  datos/derivados/transcripciones/<imagen>.ocr.md     OCR determinista (scripts/transcribir_ocr.py)
  pasada 2  datos/derivados/transcripciones/<imagen>.vision.md  lectura visual hecha con un LLM

Ambas usan la grilla física de la tabla ('←' / '↑' para celdas combinadas). Escribe
datos/derivados/transcripciones_discrepancias.csv con una fila por celda distinta (o por diferencia de
forma) y la clasifica:

  forma        distinto número de filas o columnas (no se comparan celdas fuera de la grilla común)
  numerica     cambian los dígitos (p. ej. '$606.856' / '$66.856')
  puntuacion   mismos dígitos y letras; cambia la puntuación o los símbolos (p. ej. '0.00%' / '0,00%')
  texto        cambian letras (p. ej. 'Antigiiedad' / 'Antigüedad')

Se compara tras colapsar espacios; nada más se normaliza, para no ocultar diferencias reales.
"""
import csv
import glob
import os
import re

DIR = "datos/derivados/transcripciones"
SALIDA = "datos/derivados/transcripciones_discrepancias.csv"
CAMPOS = ["imagen", "fila", "columna", "tipo", "pasada1_ocr", "pasada2_vision"]


def leer_tabla(path):
    """Grilla (lista de filas) de una tabla Markdown; ignora la línea separadora |---|."""
    filas = []
    with open(path, encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea.startswith("|") or re.fullmatch(r"\|(\s*:?-+:?\s*\|)+", linea):
                continue
            celdas = re.split(r"(?<!\\)\|", linea.strip("|"))
            filas.append([" ".join(c.replace("\\|", "|").split()) for c in celdas])
    return filas


def tipo(a, b):
    if re.sub(r"\D", "", a) != re.sub(r"\D", "", b):
        return "numerica"
    if re.sub(r"[\W_]", "", a.lower()) == re.sub(r"[\W_]", "", b.lower()) and a.lower() != b.lower():
        return "puntuacion"
    return "texto"


def comparar(base):
    a = leer_tabla(os.path.join(DIR, base + ".ocr.md"))
    b = leer_tabla(os.path.join(DIR, base + ".vision.md"))
    out = []
    forma_a = (len(a), max((len(f) for f in a), default=0))
    forma_b = (len(b), max((len(f) for f in b), default=0))
    if forma_a != forma_b:
        out.append({"imagen": base + ".jpg", "fila": "", "columna": "", "tipo": "forma",
                    "pasada1_ocr": f"{forma_a[0]}x{forma_a[1]}", "pasada2_vision": f"{forma_b[0]}x{forma_b[1]}"})
    for i, (fa, fb) in enumerate(zip(a, b), start=1):
        for j, (ca, cb) in enumerate(zip(fa, fb), start=1):
            if ca != cb:
                out.append({"imagen": base + ".jpg", "fila": i, "columna": j, "tipo": tipo(ca, cb),
                            "pasada1_ocr": ca, "pasada2_vision": cb})
    return out, sum(len(f) for f in b)


def main():
    bases = sorted(os.path.basename(p)[:-len(".vision.md")] for p in glob.glob(os.path.join(DIR, "*.vision.md")))
    faltan = [x for x in bases if not os.path.exists(os.path.join(DIR, x + ".ocr.md"))]
    if faltan:
        raise SystemExit(f"falta la pasada OCR de: {faltan} (correr scripts/transcribir_ocr.py)")
    filas, total = [], 0
    for base in bases:
        d, n = comparar(base)
        filas += d
        total += n
        print(f"{base}: {len(d)} discrepancias en {n} celdas")
    with open(SALIDA, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        w.writerows(filas)
    from collections import Counter
    print(f"{SALIDA}: {len(filas)} discrepancias en {total} celdas;", dict(Counter(r["tipo"] for r in filas)))


if __name__ == "__main__":
    main()
