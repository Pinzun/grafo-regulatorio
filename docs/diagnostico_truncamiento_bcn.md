# Diagnóstico: textos truncados en la exportación XML de Ley Chile (BCN)

Fecha: 2026-11-25. Endpoint: `https://www.leychile.cl/Consulta/obtxml?opt=7&idNorma=<id>`.

## Qué se observa

Cuatro artículos terminan a mitad de palabra en el XML descargado:

| Norma | idParte | Caracteres exportados | Termina en |
|---|---|---|---|
| Ley 21.721, artículo único | 10530118 | 6.101 | `…Ministerio de Energí` |
| Ley 20.936, artículo 1° | 9716001 | 62.151 | `…producción de energí` |
| DFL 4, artículo 34 bis (texto vigente) | 9377939 | 1.366 | `…no afectará la suspensió` |
| DFL 4, artículo 161 (texto vigente) | 8721840 | 652 | `…distribuidora según lo señ` |

El corte está en el XML de origen: la etiqueta `</Texto>` va inmediatamente después de la palabra
cortada, y el resto del documento está bien formado.

## Qué se descarta y por qué

| Hipótesis | Evidencia | Conclusión |
|---|---|---|
| Límite de tamaño fijo de la exportación | Los cortes ocurren en 652, 1.366, 6.101 y 62.151 caracteres; el DFL 4 tiene partes completas de hasta 10.695 caracteres. | Descartada |
| Límite de uso anónimo / API-KEY | Cuando se excede el límite, el servicio responde una página HTML ("API con autenticación mediante API-KEY"), no XML parcial. Las descargas truncadas son XML válido, y dos descargas independientes dan el mismo sha256. | Descartada para el truncamiento (el límite de uso existe, pero es otro fenómeno) |
| Corte por versión de la norma | `idVersion=2016-07-20` corta en el mismo punto. | Descartada |
| Desfase simple entre bytes y caracteres | En la Ley 21.721 hay 148 caracteres no ASCII, pero tras el corte faltan al menos 3.957 caracteres del art. 91 bis (comparado con el texto consolidado del DFL 4). | Descartada como explicación exacta |

## Causa más probable

Un defecto en el texto almacenado o en su procesamiento en la BCN, no un control de acceso. Los
cuatro cortes ocurren **justo después de un carácter acentuado** (í, ó, ñ). Que pase cuatro de cuatro
veces es muy improbable por azar (en estos textos cerca de 1 de cada 40 caracteres no es ASCII), y
apunta a un problema de codificación o de segmentación del texto en el origen. No es posible
confirmarlo desde fuera: la causa exacta solo la puede confirmar la BCN.

No se comprobó si la página web de Ley Chile muestra el texto completo, porque la página se arma con
JavaScript y el usuario pidió no usarla de forma automatizada.

## Solución adoptada (2026-11-25): PDF oficial de Ley Chile

El PDF que entrega el botón "Descargar" de Ley Chile **trae el texto completo** en los cuatro casos. Se
descarga con `doc2md bcn <idNorma>` (ver `~/proyectos/ocr_libros/README.md`) a `datos/raw/pdf/`, con la
misma `fechaVersion` del XML, y se convierte a Markdown leyendo su capa de texto (sin OCR ni IA).

- Ley 21.721: el PDF tiene los numerales 1 a 10. Los numerales 5 a 10 (arts. 95, 96, 99, 102, 114 y 115)
  son exactamente los 6 candidatos por `fechaVersion`.
- Ley 20.936: el artículo 1° tiene los numerales 1) a 41).
- DFL 4: los arts. 34 bis y 161 están completos, y el PDF trae las notas al margen de la BCN con la
  norma que modificó cada artículo (fuente literal para `modifica`).
- Fidelidad: todos los artículos completos del XML aparecen literalmente en la Markdown, salvo 3 del
  DFL 4, que se explican por defectos de origen.

Implementado en `scripts/extraer_modificaciones.py`: cuando el XML está truncado, usa el artículo del
PDF (verifica que el XML sea prefijo exacto del PDF) y cita el PDF solo en los numerales que no caben en
el XML. Resultado: 0 modificaciones pendientes; 204 de 205 aristas `modifica` corroboradas por notas BCN
del DFL 4 (`datos/derivados/contraste_notas_bcn.csv`).

## Otras vías legítimas

1. **Informar el error a la BCN.** Incluir idNorma, idParte y la palabra donde se corta (tabla de arriba).
   Es la única vía para corregirlo en el origen.
2. **Solicitar la API-KEY** de la nueva API de Ley Chile en
   `https://www.bcn.cl/leychile/consulta/legislacion_abierta_web_service` (página con JavaScript: se
   abre en un navegador). No se sabe si la nueva API entrega el texto completo; conviene preguntarlo al
   pedir la clave. `scripts/descargar_bcn.py` lee la variable `BCN_API_KEY` si existe, pero el nombre de
   la cabecera **debe ajustarse a la documentación oficial** cuando se tenga.
3. **Descarga manual del texto completo** desde una fuente oficial, guardado en `datos/raw/manual/`:
   - Diario Oficial, edición del día de publicación (la Ley 21.721 indica `NumeroFuente` 44034 en su XML;
     la Ley 20.936 se publicó el 2016-07-20).
   - La página de Ley Chile en un navegador, con sus opciones de imprimir o descargar, si muestra el
     texto completo.

   Convención: un archivo por norma (`<nodo>__texto_completo.<pdf|txt|html>`) y una fila en
   `datos/raw/manual/descargas_manuales.csv` con url, fecha, sha256 y quién lo descargó. Con eso se
   puede adaptar el extractor para leer el texto manual cuando el XML esté truncado, sin mezclar fuentes:
   las aristas indicarán en `fuente_url` cuál se usó.

## Caso sin PDF: Ley 20.402 (idNorma 1008692)

El XML trunca el art. 2 de la Ley 20.402 (idParte 8811969, modifica el DL 2.224 y no la LGSE), y la
exportación PDF de Ley Chile (`hddResultadoExportar=1008692.2009-12-03.0.0`) devuelve solo la portada
(1 página, sin texto de la norma), también al reintentar el 2026-11-26. Por eso la norma queda con
`cobertura = parcial` (`articulos_truncados = 8811969`) según la ontología. Su art. 13, que modifica la
LGSE, está completo en el XML: las aristas de la 20.402 no dependen del texto truncado. Para cerrarlo,
usar la vía 3 (descarga manual desde el Diario Oficial del 2009-12-03).
