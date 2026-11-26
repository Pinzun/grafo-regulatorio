"""Prueba: XML de la BCN cortado en una tabla (imagen incrustada en <Texto>).

Uso (desde la raíz del repo): python3 -I tests/test_cortes_tabla.py
También la recoge pytest si está instalado (funciones test_*).

El XML de Ley Chile incrusta algunas tablas como imagen (<aem:ArchivoBinario>) dentro de <Texto>. findtext()
devuelve solo el texto anterior a la imagen, que termina en ':' ('…de acuerdo a la siguiente escala:'), así que
la firma de truncamiento por letra acentuada no lo detecta. El extractor debe detectarlo (cortado_en_imagen) y
tomar del PDF oficial los numerales que vienen después de la imagen.
"""
import os
import sys
import xml.etree.ElementTree as ET

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))
os.chdir(RAIZ)
import extraer_modificaciones as E  # noqa: E402

XML_CORTADO = f"""<Norma xmlns="http://www.leychile.cl/esquemas"><EstructurasFuncionales>
<EstructuraFuncional idParte="1" tipoParte="Artículo"><Texto>Artículo único.- 1. Agrégase en el artículo 9 la
siguiente escala:
<aem:ArchivoBinario xmlns:aem="http://valida.aem.gob.cl"><aem:Nombre>t.jpeg</aem:Nombre></aem:ArchivoBinario>
2. Agrégase en el artículo 10 el siguiente inciso final: "Texto.".</Texto></EstructuraFuncional>
<EstructuraFuncional idParte="2" tipoParte="Artículo"><Texto>Artículo 2.- Sin tabla.</Texto></EstructuraFuncional>
</EstructurasFuncionales></Norma>"""


def test_xml_cortado_en_tabla_se_detecta():
    partes = list(E.partes(ET.fromstring(XML_CORTADO)))
    (ef1, txt1, _), (ef2, txt2, _) = partes
    assert txt1.rstrip().endswith("escala:"), "findtext() debería devolver solo el texto previo a la imagen"
    assert not E.texto_truncado(txt1), "la firma de letra acentuada no ve este corte (por eso hace falta la otra)"
    assert E.cortado_en_imagen(ef1)
    assert not E.cortado_en_imagen(ef2)
    assert "artículo 10" not in txt1, "sin la detección se pierde el N° 2, que está después de la imagen"


def test_ley_20928_detecta_el_corte_y_usa_el_pdf():
    tm = E.texto_modificatorio("ley_20928_2016")
    assert E.cortado_en_imagen(tm["parte"])
    assert tm["truncado_xml"] and tm["usa_pdf"], "el art. único de la 20.928 debe leerse del PDF oficial"
    items, truncado = E.numerales(tm["texto"])
    assert [it["n"] for it in items] == [1, 2, 3, 4, 5, 6] and not truncado
    # el texto del PDF que sigue a la imagen es el mismo que el XML trae en la cola del elemento
    cola = "".join(c.tail or "" for c in tm["parte"].find(E.NS + "Texto"))
    assert E.solo_letras(cola)[:500] in E.solo_letras(tm["texto"])


def test_ley_20928_arts_184_191_225_desde_el_pdf():
    filas, *_ = E.extraer_ley("ley_20928_2016", E.indice_dfl4(), "2026-11-26")
    pdf = E.pdf_de("1091871")
    por_art = {}
    for f in filas:
        por_art.setdefault(f["destino"].split("__art_")[1], []).append(f)
    for art in ("184", "191", "225"):
        assert art in por_art, f"falta la arista hacia el art. {art}"
        for f in por_art[art]:
            assert f["fuente_url"] == pdf["url"], f"art. {art}: la fuente debe ser el PDF oficial"
            assert "texto del PDF oficial" in f["observaciones"]
            assert f["estado"] == "verificada"
    for art in ("131", "132"):  # antes de la imagen: siguen citando el XML
        assert all("obtxml" in f["fuente_url"] for f in por_art[art])


def test_dfl4_art_157_se_marca_cortado():
    assert E.indice_dfl4()["157"]["cortado_en_imagen"]


def test_nodos_usan_texto_completo_con_transcripcion():
    import csv
    csv.field_size_limit(10**7)
    with open("ontologia/nodos_articulos.csv", encoding="utf-8") as f:
        nodos = {r["id"]: r for r in csv.DictReader(f)}
    for nodo, despues in (("ley_dfl4_2006__art_157", "El Factor de Intensidad de cada comuna será calculado"),
                          ("ley_20928_2016__art_unico", "Incorpóranse, en el artículo 225")):
        t = nodos[nodo]["texto"]
        assert t.count("[Tabla ") == 2 and "| Máximo | Mínimo |" in t, nodo
        assert despues in t, f"{nodo}: falta el texto que sigue a la imagen"
        assert nodos[nodo]["estado_extraccion"] == "xml_bcn_con_tablas_transcritas"


if __name__ == "__main__":
    pruebas = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for p in pruebas:
        p()
        print("ok", p.__name__)
    print(f"{len(pruebas)} pruebas pasaron")
