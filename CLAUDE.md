# Grafo regulatorio del sector eléctrico (piloto)

Grafo de conocimiento de normativa eléctrica chilena: DFL 4 (LGSE), Ley 20.936, Ley 21.721 y
Res. Ex. 156/2025. La fuente de verdad es `ontologia/ontologia.md`: no inventes tipos de nodo ni de
relación; si hace falta uno nuevo, pregúntalo.

## ⚠️ Cobertura parcial

El XML de la BCN trunca algunos artículos (ver `docs/diagnostico_truncamiento_bcn.md`). Hoy:

| Norma | Cobertura | Pendientes |
|---|---|---|
| Ley 21.721 | parcial | 6 modificaciones al DFL 4 sin extraer |
| Ley 20.936 | parcial | 66 modificaciones al DFL 4 sin extraer |
| DFL 4 | parcial | 0 pendientes; arts. 34 bis y 161 con texto truncado |
| Res. Ex. 156 | completa | — |

Al responder "qué artículos modificó X", **advierte siempre si la norma tiene cobertura parcial**
(atributo `cobertura` del nodo) y menciona los candidatos de
`datos/derivados/candidatos_por_fechaversion.csv`, que **no** son aristas del grafo.

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
- Lee los atributos de la arista: `estado` (verificada/inferida), `metodo` (regla/llm/manual),
  `observaciones` (motivo si es inferida) y `source_location` (idParte en la BCN). Cita idParte al responder.

## No hacer

- **No ejecutes `/graphify .` ni el pipeline completo de Graphify en este repo.** Extrae con LLM y
  sobrescribiría `graph.json` con relaciones fuera de la ontología. El grafo se construye solo con los
  scripts de abajo. Para consultar, usa explain/path/query sobre el grafo existente.
- No edites `ontologia/relaciones.csv` a mano: se regenera. Las revisiones humanas van en
  `ontologia/revisiones_manuales.csv` (confirmar/descartar, con `revisado: <persona> <AAAA-MM-DD>`).
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
