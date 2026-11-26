# Grafo regulatorio del sector eléctrico (piloto)

Grafo de conocimiento de normativa eléctrica chilena: DFL 4 (LGSE), Ley 20.402 (2009, Ministerio de
Energía; su art. 13 modifica la LGSE), Ley 20.701 (2013, concesiones), Ley 20.805 (2015, licitaciones de
suministro), Ley 20.936, Ley 21.194 (2019, distribución), Ley 21.304 (2021, electrodependientes),
Ley 21.472 (2022, Fondo de Estabilización de Tarifas), Ley 21.505 (2022, almacenamiento y electromovilidad),
Ley 21.582 (2023, notarios; su art. 10 modifica la LGSE), Ley 21.667 (2024, estabilización tarifaria),
Ley 21.721, Ley 21.804 (2026, sistemas medianos), Ley 21.833 (2026, protección tarifaria) y
Res. Ex. 156/2025. La fuente de verdad es `ontologia/ontologia.md`: no inventes tipos de nodo ni de
relación; si hace falta uno nuevo, pregúntalo.

## Cobertura

De las 15 normas del grafo, 14 tienen `cobertura` completa. La Ley 20.402 es parcial: el XML trunca su
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
  `art. único` (20.701, 20.805, 21.194, 21.304, 21.505, 21.721, 21.804), `art. 1` (20.936, 21.472,
  21.833), `art. 10` (21.582), `art. 13` (20.402) y `art. primero` (21.667); por ejemplo
  `"Ley 21.667 de 2024 — art. primero"`.
- **Preguntas de intersección** ("artículos tocados por ambas leyes"): `path` muestra solo un camino
  aunque avise "N equal-length routes"; para la lista completa compara los `explain --all` de ambos artículos
  modificatorios.
- **¿Sigue vigente un artículo?** Mira si tiene una arista `deroga` entrante y el atributo `vigente_hasta`
  del nodo; `explain` lo muestra como `DEROGADO (vigente hasta AAAA-MM-DD)` en la línea Source. Las
  supresiones parciales (inciso, frase) son `modifica` con `tipo_cambio = elimina` y no afectan la vigencia
  del artículo.
- Lee los atributos de la arista: `estado` (verificada/inferida), `metodo` (regla/llm/manual),
  `observaciones` (motivo si es inferida) y `source_location` (idParte en la BCN). Cita idParte al responder.

## Textos por artículo (`textos/`)

`textos/dfl4/art_<número>.md` (p. ej. `art_91_bis.md`, `art_72-1.md`) trae, por artículo del DFL 4:
encabezado (versión BCN, idParte, vigencia, cobertura de la historia, bloque), **texto vigente íntegro**
(indica si viene del XML o del PDF), historia de modificaciones ordenada por fecha y el **numeral literal**
de cada ley modificatoria. `textos/indice.md` lista todos los artículos (primero el bloque validado) con
avisos. Para citar el texto de un artículo o de una modificación, léelo de ahí en vez de resumir de memoria.
Se regeneran solos con `construir_grafo.py`; no los edites a mano.

Los arts. 188 y 189 dicen solo "Eliminado." en el texto consolidado: los suprimió la Ley 21.194 N° 8
(2019-12-21). Como el XML BCN no los marca derogados, sus aristas `deroga` son `inferida` y están pendientes
de revisión en `ontologia/revisiones_manuales.csv`; trátalos como eliminados.

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

`construir_grafo.py` se detiene si alguna fila viola la ontología (tipos, extremos, método, estado,
fuente, cobertura de la norma o cobertura de la historia del artículo). Commits pequeños y con mensaje claro.

## Agregar una ley modificatoria

1. idNorma desde el servicio oficial, nunca de memoria: `https://www.leychile.cl/Consulta/obtxml?opt=7&idLey=<número>`
   (verificar tipo, número y fechas en el XML).
2. Agregarla a `NORMAS` en `scripts/descargar_bcn.py` y descargar solo esa:
   `python3 -I scripts/descargar_bcn.py datos/raw <idNorma>` (no vuelve a bajar las demás).
3. PDF oficial: `doc2md bcn <idNorma> --fecha <fechaVersion> --nombre "Ley NNNNN" --salida datos/raw/pdf --registro datos/raw/pdf/descargas_pdf.csv`.
   Algunas normas (20.402, 21.304) se exportan solo con la portada (1 página, ~100 bytes de Markdown): no
   registres ese PDF; si el XML no está truncado no hace falta, y si lo está la norma queda `parcial`.
4. En `scripts/extraer_modificaciones.py`: `ARCHIVOS` y `MODIFICATORIAS` (artículo que modifica la LGSE);
   agregar la fila en `ontologia/nodos_normas.csv` (el extractor completa el resto).
5. Regenerar y revisar: numerales extraídos vs. notas BCN, filas sin resolver (deben ser 0) y **regresión**:
   las aristas de las leyes anteriores deben quedar idénticas. Cada ley suele traer un patrón de redacción
   nuevo; ajustarlo en el parser sin romper los anteriores.
