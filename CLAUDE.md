# Grafo regulatorio del sector eléctrico (piloto)

Grafo de conocimiento de normativa eléctrica chilena: el DFL 4 (LGSE), las 27 leyes posteriores a su
publicación (2007-02-05) que lo modifican según las notas BCN, y la Res. Ex. 156/2025. Leyes, con el artículo
que modifica la LGSE: 20.220 (2007), 20.257 (2008), 20.273 (2008, art. 2°), 20.402 (2009, art. 13), 20.571
(2012), 20.698 (2013, art. 1), 20.701 (2013), 20.720 (2014, art. 391), 20.805 (2015), 20.897 (2016, art. 2),
20.928 (2016), 20.936 (2016, art. 1), 20.999 (2017, art. 2), 21.076 (2018), 21.118 (2018), 21.194 (2019),
21.304 (2021), 21.472 (2022, art. 1), 21.505 (2022), 21.582 (2023, art. 10), 21.647 (2023, art. 88),
21.657 (2024), 21.667 (2024, art. primero), 21.721 (2024), 21.804 (2026), 21.806 (2026, art. 101) y
21.833 (2026, art. 1); las demás, art. único. La fuente de verdad es `ontologia/ontologia.md`: no inventes tipos de nodo ni de
relación; si hace falta uno nuevo, pregúntalo.

## Cobertura

De las 29 normas del grafo, 28 tienen `cobertura` completa. La Ley 20.402 es parcial: el XML trunca su
art. 2 (modifica el DL 2.224, no la LGSE) y el PDF de Ley Chile viene sin texto; su art. 13, el que modifica
la LGSE, está completo. Los artículos que el XML de la BCN trunca se toman del
PDF oficial (`datos/raw/pdf/`, ver `docs/diagnostico_truncamiento_bcn.md`), y cada arista indica en
`fuente_url` si salió del XML o del PDF. Si una norma nueva queda `parcial` (atributo `cobertura` del
nodo), **adviértelo siempre** al responder qué artículos modificó, y menciona los candidatos de
`datos/derivados/candidatos_por_fechaversion.csv`, que no son aristas.

Los arts. 73-122 del DFL 4 tienen su texto base en la Ley 20.936 (el N° 4 sustituye el Título III
completo); 52 aristas `metodo=manual`, revisadas por el usuario el 2026-11-25. Modificaciones posteriores
en el bloque de transmisión:

| Ley | Artículos del bloque que modifica |
|---|---|
| 21.472 (2022) | 212-13, 212-14 (lo crea) |
| 21.505 (2022) | 72-2, 72-17, 72-18 |
| 21.582 (2023) | 97, 98 |
| 21.667 (2024) | 212-13, 212-14 |
| 21.721 (2024) | 77, 87, 91, 91 bis (lo crea), 95, 96, 99, 102, 114, 115 |
| 21.804 (2026) | 72-1, 72-10, 83, 84 bis, 85 |
| 21.833 (2026) | 72-9, 212-13, 212-14 |

Las leyes anteriores a 2016 también tienen aristas hacia artículos del bloque (20.402: 73, 74, 75, 83, 87,
92, 94, 97, 99, 112, 115; 20.805: 108), pero todas quedan `superada`: recaen en el Título III que la 20.936
sustituyó completo. Varias de esas leyes modifican también artículos fuera del bloque (p. ej. la 21.804, el régimen de
sistemas medianos; la 21.582, concesiones y servidumbres).

Cada artículo del DFL 4 tiene `cobertura_historia` (atributo del nodo, también visible en
`source_location`, que muestra `graphify explain`): si dice **HISTORIA INCOMPLETA**, advierte qué leyes
faltan al responder sobre la historia o vigencia de ese artículo. El **bloque de transmisión**, validado por el
usuario el 2026-11-25, está en `datos/derivados/bloque_transmision.csv`: Título III (núcleo, 54 arts.) y
Títulos II bis y VI bis (relacionados, 36 arts.), todos con historia completa. Los 7 artículos marcados
`revisar` (7, 162, 174-178) no están validados como transmisión.

Los cambios que no recaen en un artículo (p. ej. epígrafes de capítulos) no son aristas: están en
`datos/derivados/modificaciones_no_articulo.csv`.

Un artículo puede tener varias aristas `modifica` (y a lo más una `deroga`) entrantes, una por ley. Para
su historia, ordénalas por el atributo `fecha_vigencia` de la arista (está en `graph.json`; `explain` no lo
muestra). Si `observaciones` dice **superada**, una ley posterior sustituyó el artículo completo (p. ej. la
20.936 el Título III, arts. 73-122): la arista es cierta para el artículo que tenía ese número en su fecha,
pero el texto vigente no proviene de ella. Afecta sobre todo a las leyes anteriores a 2016 (20.402).

Otros archivos derivados útiles: `datos/derivados/historia_articulos.csv` (cobertura de la historia de
todo el DFL 4) y `datos/derivados/contraste_notas_bcn.csv` (diferencias entre aristas y notas BCN; p. ej.
la BCN atribuye el cambio al art. 157 a la Ley 21.833 Art. 3, pero lo hace su Art. 1).

## Cómo consultar el grafo (`graphify-out/graph.json`)

Usa `.venv/bin/graphify` con los nombres de nodo exactos (etiquetas), por ejemplo
`"Ley 21.721 de 2024 — art. único"` o `"DFL 4 de 2006 (LGSE) — art. 91 bis"`.

- **Relaciones de un nodo → `explain`.** Lista los vecinos con el tipo de relación, la confianza y el idParte de la fuente.
  `graphify explain "Ley 21.721 de 2024 — art. único" --all`
- **Conexión entre dos nodos → `path`.** El grafo es dirigido. Para hallar un artículo común a dos normas, usa `--undirected`.
  `graphify path "Ley 21.721 de 2024 — art. único" "Ley 20.936 de 2016 — art. 1" --undirected`
- **`query` busca solo en las etiquetas de los nodos** y no filtra por tipo de relación. Una pregunta
  temática ("obras necesarias y urgentes") no encuentra nada si ninguna etiqueta contiene esas
  palabras, y una pregunta amplia devuelve casi todo el grafo. No la uses para preguntas sobre relaciones.
- Una norma llega a sus artículos por `contiene`, y sus artículos a los del DFL 4 por `modifica` o
  `deroga`. Para "qué modificó la Ley X", parte del nodo de su artículo modificatorio:
  el que indica la lista del comienzo (p. ej. `art. único`, `art. 1`, `art. 13`, `art. 391`, `art. primero`);
  por ejemplo `"Ley 21.667 de 2024 — art. primero"` o `"Ley 20.720 de 2014 — art. 391"`. El nodo de la
  ley tiene una sola arista (`contiene` hacia ese artículo): en vistas como Obsidian la ley aparece como hoja
  y sus modificaciones cuelgan del nodo del artículo. No es un faltante: así lo fija la ontología (la norma
  contiene artículos; los artículos modifican artículos). Los 361 artículos del DFL 4 tienen hoy historia
  completa; solo los 244 que alguna ley modificó son nodos (los demás están en `textos/`).
- **Preguntas de intersección** ("artículos tocados por ambas leyes"): `path` muestra solo un camino
  aunque avise "N equal-length routes"; para la lista completa compara los `explain --all` de ambos artículos
  modificatorios.
- **¿Sigue vigente un artículo?** Mira si tiene una arista `deroga` entrante y el atributo `vigente_hasta`
  del nodo; `explain` lo muestra como `DEROGADO (vigente hasta AAAA-MM-DD)` en la línea Source. Las
  supresiones parciales (inciso, frase) son `modifica` con `tipo_cambio = elimina` y no afectan la vigencia
  del artículo.
- Lee los atributos de la arista: `estado` (verificada/inferida), `metodo` (regla/llm/manual),
  `observaciones` (motivo si es inferida) y `source_location` (idParte en la BCN). Cita idParte al responder.

## Obsidian (`graphify-out/obsidian/`)

Bóveda con una nota por nodo del grafo y un enlace por arista (`graphify export obsidian`; 317 notas, más
`graph.canvas`). `construir_grafo.py` la borra y la rehace en cada regeneración: no la edites a mano. Ábrela
como bóveda para ver el grafo; si abres la raíz del repo, Obsidian muestra en cambio los enlaces entre
archivos (`indice.md` en el centro, y los PDF convertidos y las transcripciones sueltos, porque no tienen
enlaces). Los `textos/dfl4/art_<n>.md` enlazan a estas notas: la línea "Nodo en el grafo" del encabezado y,
en la historia, la ley y su artículo modificatorio.

## Textos por artículo (`textos/`)

`textos/dfl4/art_<número>.md` (p. ej. `art_91_bis.md`, `art_72-1.md`) trae, por artículo del DFL 4:
encabezado (versión BCN, idParte, vigencia, cobertura de la historia, bloque), **texto vigente íntegro**
(indica si viene del XML o del PDF), historia de modificaciones ordenada por fecha (cada línea empieza con
`vigencia: AAAA-MM-DD`; bajo las aristas que fueron inferidas, una línea `Revisión: pendiente / confirmada
(revisado: …) / descartada (…)` según `revisiones_manuales.csv`) y el **numeral literal** de cada ley
modificatoria. `textos/indice.md` lista todos los artículos (primero el bloque validado), una sección
**Leyes** (las 29 normas: fecha de publicación, idNorma, artículo modificatorio, cobertura con nota, y los
artículos del DFL 4 que modifica, incluidas las aristas superadas) y avisos. No hay archivos por ley. Para citar el texto de un artículo o de una modificación, léelo de ahí en vez de resumir de memoria.
Se regeneran solos con `construir_grafo.py`; no los edites a mano.

La etiqueta de la modificación es `N° k` (numeral), `letra a)` (Ley 20.273, literales sin numerales) o
`texto completo` (Leyes 20.897, 21.076, 21.657: el artículo modificatorio es un solo cambio).

El XML BCN incrusta algunas tablas como imagen dentro de `<Texto>`: el texto leído se corta ahí sin señal.
`cortado_en_imagen()` lo detecta y el texto se toma del PDF (la tabla tampoco está como texto en el PDF).
Prueba: `python3 -I tests/test_cortes_tabla.py`.

**Tablas como imagen.** 15 imágenes (13 distintas) en 10 artículos: DFL 4 art. 157 (2, las mismas de la
Ley 20.928 art. único), Ley 20.936 art. vigesimoquinto (3), Ley 21.647 arts. 28 y 52, Ley 21.806 arts. 8, 44,
58, 60 (2) y 63. Están en `datos/raw/imagenes/<norma>__art_<n>__img<k>.jpg` (`imagenes.csv`). Cada una se
transcribió en dos pasadas independientes en `datos/derivados/transcripciones/`: `*.ocr.md` (OCR
determinista) y `*.vision.md` (lectura visual con LLM; es la que se usa). Las diferencias celda por celda
están en `datos/derivados/transcripciones_discrepancias.csv`. Las transcripciones aparecen en la sección
"Tabla (transcripción)" de `textos/dfl4/art_157.md` y dentro del `texto` de los nodos (marcadas
`[Tabla k: transcripción …]`). Son **automáticas, sin validar** hasta que el usuario agregue la fila en
`ontologia/transcripciones_validadas.csv` (`articulo,imagen,revisado: <persona> <AAAA-MM-DD>`). Al citar
una tabla, di su estado y remite a la imagen original. '←' / '↑' = celda combinada con la de la
izquierda / la de arriba.

El "artículo trigésimo" del DFL 4 es un transitorio que agregó la Ley 21.647 N° 2, aunque el XML BCN lo marca
`no transitorio`: no es nodo y su inserción está en `modificaciones_no_articulo.csv`.

Los arts. 188 y 189 dicen solo "Eliminado." en el texto consolidado: los suprimió la Ley 21.194 N° 8
(2019-12-21). El XML BCN no los marca derogados, así que el extractor deja sus aristas `deroga` como
`inferida`; el usuario las confirmó en `ontologia/revisiones_manuales.csv` (revisado: pinzun 2026-11-26) y
quedan `verificada`/`manual`. Hoy no hay aristas inferidas en el grafo.

## No hacer

- **No ejecutes `/graphify .` ni el pipeline completo de Graphify en este repo.** Extrae con LLM y
  sobrescribiría `graph.json` con relaciones fuera de la ontología. El grafo se construye solo con los
  scripts de abajo. Para consultar, usa explain/path/query sobre el grafo existente.
- No edites `ontologia/relaciones.csv` a mano: se regenera. Las revisiones humanas van en
  `ontologia/revisiones_manuales.csv`, que `scripts/preparar_revision.py` llena con las aristas inferidas
  (`accion` vacía = pendiente; `confirmar`/`descartar` + `revisado: <persona> <AAAA-MM-DD>`). Se puede
  editar en Excel: el extractor acepta `;` o `,` y BOM.
- No rellenes datos de memoria: si no está en el texto descargado, usa `POR_COMPLETAR`.
- No intentes saltarte el límite de uso de la BCN ni automatizar la web de Ley Chile (usa JavaScript).
- Las propuestas de `datos/propuestas/regula_propuestas.csv` (metodo llm) no se cargan sin aprobación.

## Texto completo (PDF)

Cuando el XML venga truncado, el texto completo está en `datos/raw/pdf/*.md`, convertido desde el PDF
oficial de Ley Chile con `doc2md bcn <idNorma> --fecha <fechaVersion> --salida datos/raw/pdf --registro
datos/raw/pdf/descargas_pdf.csv`. En esos archivos, las líneas `> [nota BCN] …` son las notas al margen
de la BCN, no texto de la norma. Usa siempre el motor `texto` (determinista) para extraer aristas;
marker queda solo para documentos escaneados.

## Regenerar

```bash
python3 -I scripts/extraer_modificaciones.py   # XML/PDF -> relaciones.csv, nodos_*.csv, derivados
python3 -I scripts/preparar_revision.py        # agrega aristas inferidas nuevas a revisiones_manuales.csv
.venv/bin/python scripts/construir_grafo.py    # valida, construye el grafo y regenera bloque y textos/
.venv/bin/graphify export html                 # graphify-out/graph.html
```

Tablas como imagen (solo si cambian los XML): `python3 -I scripts/extraer_imagenes.py`, luego
`~/envs/ocr/bin/python -I scripts/transcribir_ocr.py` (pasada OCR; necesita numpy, Pillow y tesseract spa),
escribir a mano o con un LLM la pasada `*.vision.md` de cada imagen nueva y correr
`python3 -I scripts/comparar_transcripciones.py`. Después, regenerar el grafo.

`construir_grafo.py` se detiene si alguna fila viola la ontología (tipos, extremos, método, estado,
fuente, cobertura de la norma o cobertura de la historia del artículo). Commits pequeños y con mensaje claro.

## Agregar una ley modificatoria

1. idNorma desde el servicio oficial, nunca de memoria: `https://www.leychile.cl/Consulta/obtxml?opt=7&idLey=<número>`
   (verificar tipo, número y fechas en el XML).
2. Agregarla a `NORMAS` en `scripts/descargar_bcn.py` y descargar solo esa:
   `python3 -I scripts/descargar_bcn.py datos/raw <idNorma>` (no vuelve a bajar las demás).
3. PDF oficial: `doc2md bcn <idNorma> --fecha <fechaVersion> --nombre "Ley NNNNN" --salida datos/raw/pdf --registro datos/raw/pdf/descargas_pdf.csv`.
   Algunas normas (20.402, 20.571, 21.076, 21.304) se exportan solo con la portada (1 página, ~100 bytes de Markdown): no
   registres ese PDF; si el XML no está truncado no hace falta, y si lo está la norma queda `parcial`.
4. En `scripts/extraer_modificaciones.py`: `ARCHIVOS` y `MODIFICATORIAS` (artículo que modifica la LGSE);
   agregar la fila en `ontologia/nodos_normas.csv` (el extractor completa el resto).
5. Regenerar y revisar: numerales extraídos vs. notas BCN, filas sin resolver (deben ser 0) y **regresión**:
   las aristas de las leyes anteriores deben quedar idénticas. Cada ley suele traer un patrón de redacción
   nuevo; ajustarlo en el parser sin romper los anteriores. Correr también `python3 -I tests/test_cortes_tabla.py`.
