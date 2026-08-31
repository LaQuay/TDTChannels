# Contribuir al repositorio de TDTChannels

Gracias por querer colaborar con TDTChannels.

Este repositorio recoge información pública sobre emisiones de televisión y radio disponibles en Internet a través de fuentes oficiales. El objetivo es mantener un listado útil, actualizado y verificable para los usuarios de TDTChannels, siempre respetando la emisión original de cada operador.

Si quieres proponer un canal, corregir una emisión o avisar de un error, puedes hacerlo de dos formas:

* **Formulario recomendado:** [tdtchannels.com/peticion](https://tdtchannels.com/peticion)
* **Pull Request:** si sabes editar el repositorio y aportar la fuente oficial de la emisión.

Para más información sobre el proyecto, aplicaciones, listas disponibles y ayuda general, consulta [tdtchannels.com](https://www.tdtchannels.com).

---

## Principios generales

Antes de enviar una contribución, ten en cuenta estos criterios:

* La emisión debe proceder de una **fuente oficial, pública y verificable**.
* No se aceptan enlaces obtenidos mediante métodos no autorizados, extracción de tokens privados, cookies personales, credenciales, sistemas de pago, DRM o mecanismos destinados a limitar el acceso.
* No se aceptan reemisiones, restreams, mirrors, listas IPTV de terceros ni enlaces que no puedan atribuirse claramente al emisor o a su plataforma oficial.
* No se suben contenidos audiovisuales al repositorio. Únicamente se recoge información externa: nombre del canal, web oficial, enlace de reproducción oficial, logo y metadatos.
* TDTChannels se reserva el criterio final de inclusión, ordenación, modificación o retirada de cualquier canal o emisora.

---

## Criterios de inclusión

### Canales de España

El objetivo principal de TDTChannels es incluir canales de televisión y radio que emitan de forma oficial y pública para España.

Se priorizan:

* Canales con sede, licencia, cobertura o actividad principal en España.
* Emisiones autonómicas, locales, comarcales o municipales.
* Radios y televisiones con web oficial y emisión online estable.
* Canales que sean accesibles habitualmente desde territorio español.

### Canales internacionales

Los canales internacionales pueden incluirse si tienen interés general, relevancia clara o una audiencia suficientemente significativa.

Se valorará, entre otros factores:

* Importancia pública o informativa del canal.
* Disponibilidad oficial de la emisión.
* Estabilidad del enlace.
* Accesibilidad desde España.
* Relevancia internacional o temática.
* Claridad de la fuente oficial.

No todos los canales internacionales propuestos serán aceptados.

---

## Requisitos de la emisión

Para que una emisión pueda añadirse o actualizarse:

* Debe estar publicada en Internet por el propio canal, grupo audiovisual, plataforma oficial o distribuidor autorizado.
* Debe ser una emisión en directo, salvo que se indique expresamente otro tipo de contenido aceptado por el proyecto.
* Debe ser accesible de forma gratuita. Las emisiones de pago no se aceptan.
* Si requiere registro gratuito, se estudiará caso por caso.
* Si está geobloqueada, debe indicarse correctamente.
* Debe funcionar de forma razonablemente estable.
* Debe respetar la emisión original, sin alterar, limpiar, ocultar o modificar condiciones impuestas por el emisor.

---

## Dónde colocar una nueva entrada

Añade la nueva emisión al final de su categoría.

Esto facilita la revisión posterior y permite que el equipo de TDTChannels la mueva a la posición correspondiente si finalmente se acepta.

En el caso de canales internacionales, si el país ya existe, añade el canal al final del bloque de ese país.

---

# Televisión

Las emisiones de televisión se editan en `TELEVISION.md`.

Cada entrada debe mantener el formato de tabla existente.

## Canal

Nombre oficial del canal.

Debe evitarse añadir información innecesaria al nombre salvo que sirva para diferenciar emisiones, territorios o versiones.

Ejemplos:

* `Canal Sur Andalucía`
* `TVE Internacional`
* `BBC News Reino Unido`

## M3U8 / Stream

En esta columna debe indicarse el enlace de reproducción oficial.

Formatos aceptados:

* **m3u8**: formato preferente. Se priorizan enlaces tipo `master.m3u8` o `playlist.m3u8` cuando proceden de la fuente oficial.
* **mpd**: solo si la emisión es pública, oficial y compatible con el tratamiento actual de TDTChannels.
* **youtube**: si el canal emite oficialmente en YouTube.
* **stream**: para otros formatos embebidos o enlaces oficiales que deban ser tratados por la plataforma.

No se aceptan:

* Enlaces convertidos temporalmente desde YouTube, Twitch, Dailymotion, Vimeo u otras plataformas.
* Enlaces extraídos de listas IPTV de terceros.
* URLs con tokens privados, sesiones personales, cookies o parámetros no reproducibles.
* Emisiones capturadas, reemitidas o modificadas por terceros.
* Enlaces que el emisor no publique o no permita consumir públicamente.
* Emisiones de pago, con DRM o detrás de una suscripción.

## Etiquetas del enlace

Si la emisión tiene características especiales, indícalas dentro del texto del enlace.

Ejemplos:

```md
[m3u8 # GEO](...)
[m3u8 # GEOCAT](...)
[m3u8 # EN](...)
[m3u8 # HD](...)
[m3u8 # GEO # HD](...)
```

Etiquetas habituales:

* `# GEO`: emisión geobloqueada o limitada territorialmente.
* `# GEOCAT`: emisión limitada a Cataluña.
* `# ES`, `# EN`, `# FR`, etc.: idioma principal de la emisión, usando código ISO 639-1 cuando sea necesario.
* `# SD` / `# HD`: calidad específica si existen enlaces diferenciados.
* `# 1`, `# 2`, etc.: varias opciones oficiales para una misma emisión.

Cuando se combinen varias etiquetas, mantén un orden lógico:

```md
[m3u8 # GEO # EN # HD](...)
```

## Web

Indica la página oficial desde la que se puede acceder a la emisión o verificarla.

Debe ser preferiblemente:

* Página oficial del canal.
* Página oficial de directos.
* Página del grupo audiovisual.
* Página de la plataforma oficial del emisor.

Evita webs de terceros salvo que sean distribuidores autorizados y quede claro que la emisión procede de una fuente oficial.

## Logo

El logo debe representar correctamente el canal o emisora.

Criterios recomendados:

* Fuentes: perfiles oficiales en redes sociales o plataformas verificables del canal o la web oficial del canal.
* Tamaño recomendado: 200x200 px.
* Formato preferente: PNG.
* Formato alternativo: JPG.
* Preferiblemente con fondo blanco y sin transparencias problemáticas.
* No es imprescindible que aparezca el nombre completo del canal si el logo identifica bien la emisión.

## EPG ID

No rellenes este campo salvo que sepas exactamente qué identificador corresponde.

En la mayoría de casos, deja `-`.

El equipo de TDTChannels podrá completarlo o modificarlo posteriormente.

## Info

La columna `Info` permite añadir etiquetas internas sobre el comportamiento de la emisión.

Etiquetas habituales:

* `GEO`: bloqueo regional o territorial.
* `NOEM`: el canal no dispone de emisión online, pero se incluye por motivos de indexación, información o EPG.
* `REG`: requiere registro gratuito en la plataforma oficial.
* `EXTA`: la plataforma tratará de encontrar la emisión oficial a partir del enlace indicado en la columna `web`.
* `EXTB`: la plataforma tratará de encontrar la emisión oficial a partir del enlace indicado en la columna `M3U8`.
* `EMB`: emisión embebida desde una plataforma oficial externa, como YouTube o Twitch.
* `UAG` / `UAGB`: requiere User-Agent compatible con navegador.
* `REF` / `REFI1` / `REFG1` / `REFC1`: requiere Referer.
* `EVT`: la emisión opera de forma intermitente o eventual.
* `NONAV`: la emisión no funciona correctamente en navegadores web.

Si hay más de una etiqueta, sepáralas con comas y sin espacios.

Ejemplo:

```md
GEO,EMB,NONAV
```

Algunas etiquetas son internas de administración. Si no sabes cuál usar, deja `-` o explícalo en la Pull Request.

---

# Radio

Las emisoras de radio se editan en `RADIO.md`.

El criterio general es el mismo que para televisión: fuente oficial, pública, gratuita y verificable.

## Stream

Formatos aceptados habitualmente:

* Stream directo
* M3U8
* M3U
* MP3
* AAC
* OGG

Se priorizará siempre el enlace oficial más estable y compatible.

No se aceptan restreams, mirrors, listas de terceros ni enlaces que no procedan de la emisora o de su plataforma oficial.

## Web, logo, EPG e Info

Aplican los mismos criterios descritos para televisión.

---

## Buenas prácticas antes de enviar una Pull Request

Antes de enviar una contribución:

* Comprueba que el canal o emisora no exista ya.
* Verifica que el enlace funciona.
* Aporta siempre la web oficial desde la que sale la emisión.
* No mezcles muchos cambios no relacionados en una misma Pull Request.
* Explica brevemente qué has cambiado y por qué.
* Si el enlace es geobloqueado, indícalo.
* Si no estás seguro de algún campo, déjalo claro en el comentario de la Pull Request.

---

## Cambios que pueden rechazarse

Una contribución puede rechazarse si:

* La fuente no es oficial.
* El enlace no funciona.
* El enlace procede de una lista IPTV, restream, mirror o web no autorizada.
* La emisión es de pago, requiere suscripción o está protegida por DRM.
* El enlace depende de cookies, tokens personales o parámetros temporales.
* El canal no tiene suficiente interés para el ámbito de TDTChannels.
* La información aportada es incompleta o no se puede verificar.
* La propuesta implica eludir restricciones técnicas, territoriales o comerciales del emisor.

---

## Aviso legal

TDTChannels no aloja, almacena, emite ni retransmite contenidos audiovisuales.

El repositorio contiene referencias externas a emisiones publicadas por sus respectivos operadores, grupos audiovisuales, emisoras, plataformas oficiales o distribuidores autorizados.

Los derechos de emisión, comunicación pública, distribución, marcas, logos, programación y contenidos pertenecen a sus respectivos titulares.

La inclusión de una emisión en TDTChannels no implica relación comercial, autorización específica, patrocinio ni afiliación con el titular del canal, salvo que se indique expresamente lo contrario.

Si eres titular de derechos, representante de un canal o responsable de una emisión y quieres solicitar una corrección, actualización o retirada, puedes contactar con TDTChannels desde [tdtchannels.com](https://www.tdtchannels.com).

---

## Formulario de petición

Si no sabes hacer una Pull Request, no tienes claro el formato o simplemente quieres proponer un canal, utiliza el formulario:

[tdtchannels.com/peticion](https://tdtchannels.com/peticion)

Es la vía recomendada para peticiones generales.

---

## Gracias

Gracias por ayudar a mantener TDTChannels actualizado, útil y transparente para todos.
