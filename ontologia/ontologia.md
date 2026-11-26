# Ontología del grafo de conocimiento regulatorio (versión 0.4, piloto)

Dominio: normativa del sector eléctrico chileno. Fecha de la definición: 2026-11-25.
Cambios v0.2 (2026-11-25): nueva relación `contiene`; redefinición de `inferida`; columna `metodo`; tablas legibles por máquina.
Cambios v0.3 (2026-11-25): atributo `cobertura` de las normas; valor `manual` en `metodo`.
Cambios v0.4 (2026-11-25): atributo `cobertura_historia` de los artículos.

## Tipos de nodo

### Normas (jerarquía normativa)
- **ley**: leyes y DFL (los DFL tienen fuerza de ley). Ejemplo: DFL 4 de 2006 (LGSE), Ley 20.936, Ley 21.721.
- **reglamento**: decretos supremos que desarrollan una ley. Nivel inferior a la ley.
- **norma_tecnica**: desarrolla un reglamento. Nivel inferior al reglamento.
- **resolucion**: resoluciones (por ejemplo, resoluciones exentas). Tipo aparte, NO es norma técnica. Ejemplo: Resolución Exenta 156 de 2025.

Atributos de una norma: tipo, número, año, órgano emisor, fecha de publicación, id BCN, url fuente, estado de vigencia, cobertura.

**cobertura**: qué tan completo está el texto descargado para el grafo.
- `completa`: sin modificaciones pendientes y sin artículos con texto truncado.
- `parcial`: hay modificaciones pendientes de extraer (`modificaciones_pendientes` > 0) o artículos con texto truncado en la fuente (`articulos_truncados`).
- `modificaciones_pendientes`: número de modificaciones que la norma hizo y que no se pudieron extraer (candidatos en `datos/derivados/candidatos_por_fechaversion.csv`).
- `articulos_truncados`: idParte de los artículos cuyo texto llega cortado en el XML y **no** se pudo recuperar.
- `articulos_truncados_recuperados_pdf`: idParte de los artículos cortados en el XML cuyo texto completo se tomó del PDF oficial de Ley Chile (`pdf_sha256` identifica el archivo).

### Otros nodos
- **articulo**: unidad de trabajo real. Las modificaciones se hacen a artículos, no a normas completas. Atributos: norma contenedora, número, texto, vigente_desde, vigente_hasta, cobertura_historia.
  - **cobertura_historia** (artículos del DFL 4): `completa` si todas las leyes posteriores al DFL 4 que la BCN anota en el artículo están en el grafo; `parcial` si falta alguna (`leyes_faltantes`). `leyes_modificatorias_bcn` lista las anotadas. Las leyes anteriores a la publicación del DFL 4 (2007-02-05) no cuentan: su contenido ya está en el texto refundido. Usa los mismos valores de la tabla de cobertura.
- **organo**: Ministerio de Energía, CNE, Coordinador Eléctrico Nacional, etc.
- **instrumento**: plan de expansión, listado de obras necesarias y urgentes, etc.
- **concepto**: transmisión, obras necesarias y urgentes, tarifas, etc.

## Tipos de relación

- **modifica**: una norma cambia un artículo de otra. Guardar fecha de vigencia del cambio.
- **deroga**: elimina una norma o un artículo completo ("Suprímese / Derógase / Elimínase el artículo X"). Es `verificada` si el XML BCN de la norma modificada marca el artículo `derogado`; si no coinciden, `inferida` con motivo. El nodo derogado lleva en `vigente_hasta` la fecha de vigencia de la derogación. Las supresiones parciales (un inciso, una frase, un número) son `modifica` con `tipo_cambio` = `elimina`.
- **reglamenta**: de un nivel al inmediato superior: reglamento -> ley, norma_tecnica -> reglamento.
- **implementa**: una resolución implementa un artículo o una norma. Ejemplo: Resolución Exenta 156 implementa art. 91 bis de la Ley 21.721 / LGSE.
- **cita**: una norma menciona a otra sin cambiarla.
- **regula**: une un artículo con un concepto. Única relación donde se permite inferencia con LLM.
- **contiene**: una norma contiene un artículo (norma -> articulo). Siempre `verificada`: sale de la estructura del XML de la BCN (idParte).

## Metadatos obligatorios en cada relación
- **fuente**: de dónde salió (url BCN, id de norma, parte, fecha de consulta).
- **estado**: `verificada` (consta literalmente en el texto de la norma o en su estructura, o fue revisada por una persona) o `inferida` (no consta literalmente en el texto; deducida por regla o LLM, pendiente de revisión; el motivo va en `observaciones`).
- **metodo**: `regla` (parseo determinista del XML y expresiones regulares), `llm` (propuesta de un modelo de lenguaje) o `manual` (una persona revisó la arista contra el texto). Una arista `manual` queda `verificada` y en `observaciones` se anota quién la revisó, la fecha y el texto consultado.

## Reglas
1. Las relaciones modifica, deroga, reglamenta, implementa y contiene deben tener `metodo` = `regla` o `manual`; nunca `llm`. Pueden quedar `inferida` solo con `metodo` = `regla` y motivo en `observaciones`, y requieren revisión humana antes de darse por ciertas. Al revisarlas, pasan a `metodo` = `manual` y `estado` = `verificada` (o se eliminan si la revisión las descarta).
2. El LLM solo propone aristas `regula` y `cita`, siempre con estado `inferida` y `metodo` = `llm`.
3. Toda arista lleva fuente.
4. `contiene` es siempre `verificada`.
5. Toda arista con `metodo` = `manual` debe estar `verificada` y tener `observaciones` con revisor y fecha (formato `revisado: <persona> <AAAA-MM-DD>`).

## Tablas para validación automática

El script `scripts/csv_a_graphify.py` lee estas tablas; cualquier tipo o extremo fuera de ellas detiene la generación del grafo.

### Tipos de nodo

| tipo | categoria |
|---|---|
| ley | norma |
| reglamento | norma |
| norma_tecnica | norma |
| resolucion | norma |
| articulo | articulo |
| organo | otro |
| instrumento | otro |
| concepto | otro |

### Extremos válidos por relación

`norma` = ley, reglamento, norma_tecnica o resolucion.

| relacion | origen | destino | metodos | estados | requiere_fuente |
|---|---|---|---|---|---|
| modifica | norma, articulo | articulo | regla, manual | verificada, inferida | si |
| deroga | norma, articulo | norma, articulo | regla, manual | verificada, inferida | si |
| reglamenta | reglamento, norma_tecnica | ley, reglamento | regla, manual | verificada, inferida | si |
| implementa | resolucion, articulo | norma, articulo | regla, manual | verificada, inferida | si |
| contiene | norma | articulo | regla, manual | verificada | si |
| cita | norma, articulo | norma, articulo | regla, llm, manual | verificada, inferida | si |
| regula | articulo | concepto | regla, llm, manual | verificada, inferida | si |

Restricciones adicionales: en `reglamenta`, reglamento -> ley y norma_tecnica -> reglamento (nivel inmediato superior). Toda fila con `metodo` = `llm` debe tener `estado` = `inferida`. Toda fila con `metodo` = `manual` debe tener `estado` = `verificada` y revisor y fecha en `observaciones`.

### Valores de cobertura

| cobertura | condicion |
|---|---|
| completa | modificaciones_pendientes = 0 y sin articulos_truncados |
| parcial | modificaciones_pendientes > 0 o con articulos_truncados |
