# Ontología del grafo de conocimiento regulatorio (versión 0.2, piloto)

Dominio: normativa del sector eléctrico chileno. Fecha de la definición: 2026-11-25.
Cambios v0.2 (2026-11-25): nueva relación `contiene`; redefinición de `inferida`; columna `metodo`; tablas legibles por máquina.

## Tipos de nodo

### Normas (jerarquía normativa)
- **ley**: leyes y DFL (los DFL tienen fuerza de ley). Ejemplo: DFL 4 de 2006 (LGSE), Ley 20.936, Ley 21.721.
- **reglamento**: decretos supremos que desarrollan una ley. Nivel inferior a la ley.
- **norma_tecnica**: desarrolla un reglamento. Nivel inferior al reglamento.
- **resolucion**: resoluciones (por ejemplo, resoluciones exentas). Tipo aparte, NO es norma técnica. Ejemplo: Resolución Exenta 156 de 2025.

Atributos de una norma: tipo, número, año, órgano emisor, fecha de publicación, id BCN, url fuente, estado de vigencia.

### Otros nodos
- **articulo**: unidad de trabajo real. Las modificaciones se hacen a artículos, no a normas completas. Atributos: norma contenedora, número, texto, vigente_desde, vigente_hasta.
- **organo**: Ministerio de Energía, CNE, Coordinador Eléctrico Nacional, etc.
- **instrumento**: plan de expansión, listado de obras necesarias y urgentes, etc.
- **concepto**: transmisión, obras necesarias y urgentes, tarifas, etc.

## Tipos de relación

- **modifica**: una norma cambia un artículo de otra. Guardar fecha de vigencia del cambio.
- **deroga**: elimina una norma o un artículo.
- **reglamenta**: de un nivel al inmediato superior: reglamento -> ley, norma_tecnica -> reglamento.
- **implementa**: una resolución implementa un artículo o una norma. Ejemplo: Resolución Exenta 156 implementa art. 91 bis de la Ley 21.721 / LGSE.
- **cita**: una norma menciona a otra sin cambiarla.
- **regula**: une un artículo con un concepto. Única relación donde se permite inferencia con LLM.
- **contiene**: una norma contiene un artículo (norma -> articulo). Siempre `verificada`: sale de la estructura del XML de la BCN (idParte).

## Metadatos obligatorios en cada relación
- **fuente**: de dónde salió (url BCN, id de norma, parte, fecha de consulta).
- **estado**: `verificada` (consta literalmente en el texto de la norma o en su estructura, o fue revisada por una persona) o `inferida` (no consta literalmente en el texto; deducida por regla o LLM, pendiente de revisión; el motivo va en `observaciones`).
- **metodo**: `regla` (parseo determinista del XML y expresiones regulares) o `llm` (propuesta de un modelo de lenguaje).

## Reglas
1. Las relaciones modifica, deroga, reglamenta, implementa y contiene deben tener `metodo` = `regla` (o revisión humana). Pueden quedar `inferida` solo con `metodo` = `regla` y motivo en `observaciones`, y requieren revisión humana antes de darse por ciertas.
2. El LLM solo propone aristas `regula` y `cita`, siempre con estado `inferida` y `metodo` = `llm`.
3. Toda arista lleva fuente.
4. `contiene` es siempre `verificada`.

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
| modifica | norma, articulo | articulo | regla | verificada, inferida | si |
| deroga | norma, articulo | norma, articulo | regla | verificada, inferida | si |
| reglamenta | reglamento, norma_tecnica | ley, reglamento | regla | verificada, inferida | si |
| implementa | resolucion, articulo | norma, articulo | regla | verificada, inferida | si |
| contiene | norma | articulo | regla | verificada | si |
| cita | norma, articulo | norma, articulo | regla, llm | verificada, inferida | si |
| regula | articulo | concepto | regla, llm | verificada, inferida | si |

Restricciones adicionales: en `reglamenta`, reglamento -> ley y norma_tecnica -> reglamento (nivel inmediato superior). Toda fila con `metodo` = `llm` debe tener `estado` = `inferida`.
