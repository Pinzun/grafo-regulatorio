"""Empaqueta el grafo como skill de Claude: dist/grafo-regulatorio.zip. Determinista, sin LLM, solo biblioteca
estándar.

Uso (desde la raíz del repo, después de construir_grafo.py): python3 -I scripts/empaquetar_skill.py

Contenido del zip (carpeta raíz grafo-regulatorio/):
  SKILL.md       instrucciones del skill + "Versión del repo: <hash corto> · generado <fecha>"
  indice.md      copia de textos/indice.md
  dfl4/art_*.md  copia de textos/dfl4/
  limites.md     qué no cubre el grafo; la cobertura parcial, las tablas sin validar y las aristas pendientes
                 se leen de los CSV, no se escriben a mano

En los .md copiados, los enlaces [[...]] de Obsidian y los enlaces Markdown que salen del paquete (notas de
graphify-out/obsidian/, imágenes de datos/raw/) pasan a texto plano; los enlaces entre archivos del paquete
(indice.md -> dfl4/art_*.md) se mantienen.

Determinismo: la fecha es la del commit HEAD (no la del reloj), los archivos van ordenados y con fecha y
permisos fijos; el mismo commit produce el mismo zip byte a byte. Si textos/, ontologia/ o datos/ tienen
cambios sin commit, la línea de versión lo dice.
"""
import csv
import os
import re
import subprocess
import sys
import zipfile
from collections import Counter
from urllib.parse import unquote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extraer_modificaciones as E  # noqa: E402
from csv_a_graphify import etiqueta_norma  # noqa: E402
from generar_textos import NOTAS_COBERTURA  # noqa: E402

RAIZ_ZIP = "grafo-regulatorio"
SALIDA = "dist/grafo-regulatorio.zip"

SKILL = """---
name: grafo-regulatorio
description: Consulta la normativa eléctrica chilena (DFL 4 / LGSE y las 27 leyes que la modifican, más la Res. Ex. 156/2025). Úsalo para preguntas sobre qué ley modificó un artículo, texto vigente, historia de modificaciones, vigencia o derogación, y bloque de transmisión.
---
# Grafo regulatorio (DFL 4 / LGSE)
Cómo consultar: abre `indice.md` (tabla de leyes y lista de artículos), luego `dfl4/art_<n>.md` del artículo (p. ej. `art_91_bis.md`, `art_72-1.md`).
Reglas:
- Responde SOLO con estos archivos; no uses memoria. Si algo no está, dilo. Reglamentos, normas técnicas e interpretación NO están cargados (ver `limites.md`).
- Cita idParte, ley, numeral y la fecha rotulada "vigencia".
- Aclara que el texto es el consolidado de la BCN, no el del Diario Oficial.
- Si una ley o artículo tiene cobertura parcial o historia incompleta, adviértelo siempre.
- Distingue arista verificada, inferida y manual, y el estado de revisión.
- Una arista "superada" es cierta para el artículo que existía en esa fecha, pero el texto vigente no viene de esa ley.
- Las tablas transcritas desde imagen: di si están validadas y remite a la imagen original.
- Para "qué modificó la ley X": parte de la tabla Leyes del índice y revisa los artículos listados.
"""

RE_WIKI = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
RE_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout.strip()


def leer(path, **kw):
    with open(path, encoding=kw.pop("encoding", "utf-8"), newline="") as f:
        return list(csv.DictReader(f, **kw))


def plano(md):
    """[[nota]] / [[nota|alias]] -> texto; [texto](../../ruta fuera del paquete) -> texto. Las imágenes de
    datos/raw conservan la ruta del repositorio como texto, para poder remitir a la imagen original."""
    md = RE_WIKI.sub(lambda m: m.group(2) or m.group(1), md)

    def link(m):
        texto, dest = m.group(1), m.group(2)
        if not dest.startswith("../../"):
            return m.group(0)  # enlace dentro del paquete (indice.md -> dfl4/…) o URL
        ruta = unquote(dest[len("../../"):])
        if ruta.startswith("graphify-out/obsidian/"):
            return texto
        return f"{texto} (en el repositorio: `{ruta}`)"
    return RE_LINK.sub(link, md)


def limites():
    normas = {n["id"]: n for n in leer("ontologia/nodos_normas.csv")}
    historia = leer("datos/derivados/historia_articulos.csv")
    relaciones = leer("ontologia/relaciones.csv")
    imagenes = leer("datos/raw/imagenes/imagenes.csv")
    validadas = E.transcripciones_validadas()
    no_articulo = leer("datos/derivados/modificaciones_no_articulo.csv")
    revisiones = {(v["origen"], v["relacion"], v["destino"]): v for v in E.leer_revisiones()}
    contraste = Counter(r["tipo"] for r in leer("datos/derivados/contraste_notas_bcn.csv", encoding="utf-8-sig"))
    et = {k: etiqueta_norma(v) for k, v in normas.items()}

    md = ["# Límites del grafo regulatorio", "",
          "Lo que este paquete NO responde. Si la pregunta cae aquí, dilo en vez de completar con memoria.", "",
          "## Fuera del alcance", "",
          "- **Reglamentos** (decretos supremos que reglamentan la LGSE): no están cargados.",
          "- **Normas técnicas** (NTSyCS y otras): no están cargadas.",
          "- **Interpretación técnico-económica**: el paquete trae texto e historia normativa; no análisis de "
          "efectos, tarifas, criterios de la CNE o del Coordinador, ni dictámenes del Panel de Expertos.",
          "- **Leyes que no modifican la LGSE**: no están. De las leyes modificatorias solo se cargó el artículo "
          "que modifica la LGSE; sus demás artículos (p. ej. disposiciones transitorias propias) no.",
          f"- **Otras resoluciones**: solo está la {et.get('res_156_2025', 'Res. Ex. 156/2025')}, como norma que "
          "implementa el art. 91 bis.",
          "- **Texto oficial**: el texto es el consolidado de la BCN (Ley Chile), no la publicación del Diario "
          "Oficial.", ""]

    md += ["## Cobertura parcial de normas", ""]
    parciales = sorted((k for k, n in normas.items() if n.get("cobertura") != "completa"), key=lambda k: et[k])
    md += [f"- {et[k]}: cobertura **{normas[k].get('cobertura') or 'POR_COMPLETAR'}** — "
           f"{NOTAS_COBERTURA.get(k, 'POR_COMPLETAR')}" for k in parciales] or ["- Ninguna."]
    md.append(f"- Normas con cobertura completa: {len(normas) - len(parciales)} de {len(normas)}.")

    md += ["", "## Historia incompleta de artículos del DFL 4", ""]
    incompletas = [h for h in historia if h["cobertura_historia"] != "completa"]
    md += [f"- art. {h['articulo']}: {h['cobertura_historia']}; faltan {h['leyes_faltantes'] or 'POR_COMPLETAR'}"
           for h in incompletas] or [f"- Ninguno: los {len(historia)} artículos tienen historia completa."]

    md += ["", "## Aristas pendientes de revisión", ""]
    pend = [r for r in relaciones if r["estado"] == "inferida"
            and not (revisiones.get((r["origen"], r["relacion"], r["destino"])) or {}).get("accion")]
    md += [f"- {r['relacion']} {r['origen']} -> {r['destino']} (idParte {r['fuente_id_parte']}): "
           f"{r['observaciones']}" for r in pend] or ["- Ninguna: no hay aristas inferidas sin revisar."]
    sup = sum("superada" in r["observaciones"] for r in relaciones)
    md.append(f"- Filas marcadas **superada** (ciertas en su fecha, pero el texto vigente no viene de esa ley): {sup}.")

    md += ["", "## Tablas transcritas desde imagen sin validar", ""]
    sin = [i for i in imagenes if (f"{i['norma']}__art_{i['articulo']}", i["archivo"]) not in validadas]
    md += [f"- {et.get(i['norma'], i['norma'])}, art. {i['articulo']}: tabla {i['k']} "
           f"(imagen `datos/raw/imagenes/{i['archivo']}`)" for i in sin] or ["- Ninguna."]
    md.append(f"- Validadas: {len(imagenes) - len(sin)} de {len(imagenes)}. Solo las del DFL 4 aparecen en "
              "`dfl4/`; las demás están en artículos de leyes que no forman parte de este paquete.")

    md += ["", "## Modificaciones que no recaen en un artículo (no están en la historia)", ""]
    md += [f"- {et.get(r['norma'], r['norma'])} N° {r['numeral']} ({r['tipo_cambio']}): {E.norm_ws(r['texto'])[:160]}"
           for r in no_articulo] or ["- Ninguna."]

    md += ["", "## Diferencias con las notas al margen de la BCN", "",
           f"- {sum(contraste.values())} diferencias entre las aristas y las notas BCN "
           f"({', '.join(f'{k}: {v}' for k, v in sorted(contraste.items()))}); no están en este paquete."]
    return "\n".join(md) + "\n"


def main():
    sucio = git("status", "--porcelain", "--", "textos", "ontologia", "datos")
    version = (f"Versión del repo: {git('rev-parse', '--short', 'HEAD')} · generado "
               f"{git('log', '-1', '--format=%cs')}" + (" (con cambios sin commit)" if sucio else ""))
    archivos = {"SKILL.md": SKILL + "\n" + version + "\n", "limites.md": limites()}
    with open("textos/indice.md", encoding="utf-8") as f:
        archivos["indice.md"] = plano(f.read())
    for nombre in sorted(os.listdir("textos/dfl4")):
        if nombre.endswith(".md"):
            with open(os.path.join("textos/dfl4", nombre), encoding="utf-8") as f:
                archivos[f"dfl4/{nombre}"] = plano(f.read())

    fecha = tuple(int(x) for x in git("log", "-1", "--format=%cs").split("-")) + (0, 0, 0)
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    with zipfile.ZipFile(SALIDA, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for ruta in sorted(archivos):
            info = zipfile.ZipInfo(f"{RAIZ_ZIP}/{ruta}", date_time=fecha)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, archivos[ruta].encode("utf-8"))
    restos = sum(len(RE_WIKI.findall(t)) + t.count("../../") for t in archivos.values())
    if restos:
        raise SystemExit(f"quedaron {restos} enlaces fuera del paquete")
    print(f"{SALIDA}: {len(archivos)} archivos ({sum(1 for r in archivos if r.startswith('dfl4/'))} artículos); {version}")


if __name__ == "__main__":
    main()
