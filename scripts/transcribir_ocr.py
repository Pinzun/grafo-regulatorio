"""Pasada 1 de la transcripción de tablas: OCR determinista celda por celda (Tesseract), sin LLM.

Uso (desde la raíz del repo; necesita numpy, Pillow y el binario tesseract con el idioma 'spa'):
    ~/envs/ocr/bin/python -I scripts/transcribir_ocr.py

Para cada imagen de datos/raw/imagenes/imagenes.csv escribe
datos/derivados/transcripciones/<imagen>.ocr.md con la grilla física de la tabla en Markdown:

  1. Detecta las líneas horizontales de la tabla (filas con un trazo oscuro largo) y, dentro de cada banda
     entre dos líneas, las verticales (columnas oscuras en casi toda la altura de la banda). Así una celda
     combinada en horizontal (sin vertical en esa banda) abarca varias columnas globales.
  2. Recorta cada celda y la pasa por `tesseract -l spa --psm 6` (ampliada ×3 si la imagen es de baja
     resolución).
  3. Convención, igual que la pasada visual (*.vision.md): '←' = la celda de la izquierda se extiende hasta
     aquí; '↑' = la celda de arriba se extiende hasta aquí (no hay línea horizontal sobre esta celda).

La pasada 2 (*.vision.md) es la lectura visual hecha con un LLM; scripts/comparar_transcripciones.py
compara ambas celda por celda.
"""
import csv
import io
import os
import subprocess

import numpy as np
from PIL import Image

IMG = "datos/raw/imagenes"
OUT = "datos/derivados/transcripciones"
UMBRAL_OSCURO = 160


def corridas(v):
    """[(inicio, fin)] de tramos True consecutivos de un vector booleano."""
    out, ini = [], None
    for i, x in enumerate(list(v) + [False]):
        if x and ini is None:
            ini = i
        elif not x and ini is not None:
            out.append((ini, i - 1))
            ini = None
    return out


def agrupar(valores, tol):
    grupos = []
    for v in sorted(valores):
        if grupos and v - grupos[-1][-1] <= tol:
            grupos[-1].append(v)
        else:
            grupos.append([v])
    return grupos


def lineas_horizontales(osc):
    """[(y0, y1, x0, x1)] de las líneas horizontales: filas con un trazo oscuro de al menos 40% del ancho de
    la tabla. x0, x1 = extensión del trazo (para saber qué celdas cubre)."""
    xs = np.where(osc.any(axis=0))[0]
    ancho = xs.max() - xs.min() + 1
    filas = []
    for y in range(osc.shape[0]):
        rs = corridas(osc[y])
        if rs:
            a, b = max(rs, key=lambda r: r[1] - r[0])
            if b - a + 1 >= 0.4 * ancho:
                filas.append((y, a, b))
    lineas = []
    for g in agrupar([f[0] for f in filas], 1):
        sel = [f for f in filas if g[0] <= f[0] <= g[-1]]
        lineas.append((g[0], g[-1], min(f[1] for f in sel), max(f[2] for f in sel)))
    return lineas


def verticales_en_banda(osc, y0, y1):
    """Centros x de las verticales que cruzan la banda [y0, y1] (oscuras en >= 90% de su altura)."""
    banda = osc[y0:y1 + 1]
    if banda.shape[0] < 3:
        return []
    frac = banda.mean(axis=0)
    return [(a + b) / 2 for a, b in corridas(frac >= 0.9)]


def ocr(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    r = subprocess.run(["tesseract", "stdin", "stdout", "-l", "spa", "--psm", "6"], input=buf.getvalue(),
                       capture_output=True, check=True)
    return " ".join(r.stdout.decode("utf-8").split())


def transcribir(path):
    gris = Image.open(path).convert("L")
    osc = np.array(gris) < UMBRAL_OSCURO
    escala = 3 if gris.info.get("dpi", (100, 100))[0] < 200 else 1
    hs = lineas_horizontales(osc)
    bandas = [(hs[i], hs[i + 1]) for i in range(len(hs) - 1)]
    vert = {i: verticales_en_banda(osc, sup[1] + 1, inf[0] - 1) for i, (sup, inf) in enumerate(bandas)}
    tol = 6 * (1 if escala == 3 else 3)
    globales = [sum(g) / len(g) for g in agrupar([x for v in vert.values() for x in v], tol)]

    def indice(x):
        return min(range(len(globales)), key=lambda i: abs(globales[i] - x))

    ncol = len(globales) - 1
    grilla, cajas = [], {}  # cajas: (fila, col) de la celda de origen -> [x0, y0, x1, y1]
    for i, (sup, inf) in enumerate(bandas):
        fila = [""] * ncol
        vs = sorted(vert[i])
        for a, b in zip(vs, vs[1:]):
            ca, cb = indice(a), indice(b)
            if cb <= ca:
                continue
            # ¿hay línea sobre esta celda? (fracción oscura del borde superior dentro de la celda)
            x0, x1 = int(a) + 3, int(b) - 3
            borde = osc[sup[0]:sup[1] + 1, x0:x1 + 1].any(axis=0).mean() if x1 > x0 else 1
            if i > 0 and borde < 0.5:
                fila[ca] = "↑"
                # la celda de origen (arriba) se extiende hasta el fondo de esta banda: su texto puede seguir aquí
                r = i - 1
                while r > 0 and grilla[r][ca] == "↑":
                    r -= 1
                if (r, ca) in cajas:
                    cajas[(r, ca)][3] = inf[0] - 3
            else:
                fila[ca] = None
                cajas[(i, ca)] = [x0 + 2, sup[1] + 3, x1 - 2, inf[0] - 3]
            for j in range(ca + 1, cb):
                fila[j] = "←"
        grilla.append(fila)
    for (i, ca), caja in cajas.items():
        recorte = gris.crop(tuple(caja))
        if escala > 1:
            recorte = recorte.resize((recorte.width * escala, recorte.height * escala), Image.LANCZOS)
        grilla[i][ca] = ocr(recorte)  # --psm 6; --psm 7 en celdas de una línea dio más errores (75 vs 72)
    return grilla


def a_markdown(grilla):
    esc = [[c.replace("|", "\\|") for c in f] for f in grilla]
    lineas = ["| " + " | ".join(esc[0]) + " |", "|" + "---|" * len(esc[0])]
    lineas += ["| " + " | ".join(f) + " |" for f in esc[1:]]
    return "\n".join(lineas) + "\n"


def main():
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(IMG, "imagenes.csv"), encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    for r in filas:
        grilla = transcribir(os.path.join(IMG, r["archivo"]))
        nombre = r["archivo"][:-4] + ".ocr.md"
        with open(os.path.join(OUT, nombre), "w", encoding="utf-8") as f:
            f.write(a_markdown(grilla))
        print(f"{nombre}: {len(grilla)} filas x {len(grilla[0]) if grilla else 0} columnas")


if __name__ == "__main__":
    main()
