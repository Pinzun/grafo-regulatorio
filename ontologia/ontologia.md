# Ontología del grafo de conocimiento regulatorio (versión 0.1, piloto)

Dominio: normativa del sector eléctrico chileno. Fecha de la definición: 2026-11-25.

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

## Metadatos obligatorios en cada relación
- **fuente**: de dónde salió (url BCN, id de norma, parte, fecha de consulta).
- **estado**: `verificada` (extraída de fuente estructurada o revisada por una persona) o `inferida` (generada por LLM, pendiente de revisión).

## Reglas
1. Las relaciones modifica, deroga, reglamenta e implementa deben ser deterministas o revisadas por humano. No se aceptan como `inferida` sin revisión.
2. El LLM solo propone aristas `regula` y `cita`, siempre con estado `inferida`.
3. Toda arista lleva fuente.
