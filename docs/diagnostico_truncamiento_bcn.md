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

## Qué se puede hacer (vías legítimas)

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
