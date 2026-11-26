# Grafo regulatorio del sector eléctrico (piloto)

Grafo de conocimiento de normativa eléctrica chilena: DFL 4 (LGSE), Ley 20.936, Ley 21.721,
Ley 21.804 (2026, sistemas medianos), Ley 21.505 (2022, almacenamiento y electromovilidad),
Ley 21.582 (2023, notarios; su art. 10 modifica la LGSE), Ley 21.833 (2026, protección tarifaria),
Ley 21.472 (2022, Fondo de Estabilización de Tarifas), Ley 21.667 (2024, estabilización tarifaria)
y Res. Ex. 156/2025. La fuente de verdad es `ontologia/ontologia.md`: no inventes tipos de nodo ni de
relación; si hace falta uno nuevo, pregúntalo.

## Cobertura

Las 4 normas tienen hoy `cobertura` completa. Los artículos que el XML de la BCN trunca se toman del
PDF oficial (`datos/raw/pdf/`, ver `docs/diagnostico_truncamiento_bcn.md`), y cada arista indica en
`fuente_url` si salió del XML o del PDF. Si una norma nueva queda `parcial` (atributo `cobertura` del
nodo), **adviértelo siempre** al responder qué artículos modificó, y menciona los candidatos de
`datos/derivados/candidatos_por_fechaversion.csv`, que no son aristas.

Los arts. 73-122 del DFL 4 tienen su texto base en la Ley 20.936 (el N° 4 sustituye el Título III
completo); 52 aristas `metodo=manual`, revisadas por el usuario el 2026-11-25. Varios fueron modificados
después por otras leyes (en el piloto, la Ley 21.721: arts. 77, 87, 91, 95, 96, 99, 102, 114 y 115; según las
notas BCN también otras leyes). La Ley 21.804 modifica los arts. 72-1, 72-10, 83, 84 bis y 85 de
transmisión y gran parte del régimen de sistemas medianos (Título I bis, arts. 130-199 bis, 225).

Cada artículo del DFL 4 tiene `cobertura_historia` (atributo del nodo, también visible en
`source_location`, que muestra `graphify explain`): si dice **HISTORIA INCOMPLETA**, advierte qué leyes
faltan al responder sobre la historia o vigencia de ese artículo. El **bloque de transmisión**, validado por el
usuario el 2026-11-25, está en `datos/derivados/bloque_transmision.csv`: Título III (núcleo, 54 arts.) y
Títulos II bis y VI bis (relacionados, 36 arts.), todos con historia completa. Los 7 artículos marcados
`revisar` (7, 162, 174-178) no están validados como transmisión.

Los cambios que no recaen en un artículo (p. ej. epígrafes de capítulos) no son aristas: están en
`datos/derivados/modificaciones_no_articulo.csv`.

Un artículo puede tener varias aristas `modifica` entrantes, una por ley. Para su historia, ordénalas por
el atributo `fecha_vigencia` de la arista (está en `graph.json`; `explain` no lo muestra).

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
- Una norma llega a sus artículos por `contiene`, y sus artículos a los del DFL 4 por `modifica`. Para
  "qué modificó la Ley X", parte del nodo de su artículo modificatorio (`… — art. único`, `… — art. 1`).
- **Preguntas de intersección** ("artículos tocados por ambas leyes"): `path` muestra solo un camino
  aunque avise "N equal-length routes"; para la lista completa compara los `explain --all` de ambos artículos
  modificatorios.
- **¿Sigue vigente un artículo?** Mira si tiene una arista `deroga` entrante y el atributo `vigente_hasta`
  del nodo; `explain` lo muestra como `DEROGADO (vigente hasta AAAA-MM-DD)` en la línea Source. Las
  supresiones parciales (inciso, frase) son `modifica` con `tipo_cambio = elimina` y no afectan la vigencia
  del artículo.
- Lee los atributos de la arista: `estado` (verificada/inferida), `metodo` (regla/llm/manual),
  `observaciones` (motivo si es inferida) y `source_location` (idParte en la BCN). Cita idParte al responder.

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
python3 -I scripts/descargar_bcn.py            # solo si hay que volver a descargar (cambia sha256 y fecha)
python3 -I scripts/extraer_modificaciones.py   # XML -> relaciones.csv, nodos_*.csv, candidatos
.venv/bin/python scripts/construir_grafo.py    # valida contra la ontología y construye el grafo
.venv/bin/graphify export html                 # graphify-out/graph.html
```

`construir_grafo.py` se detiene si alguna fila viola la ontología (tipos, extremos, método, estado,
fuente o cobertura). Commits pequeños y con mensaje claro.
