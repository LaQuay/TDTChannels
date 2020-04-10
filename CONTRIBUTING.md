Para hacer más sencillas las contribuciones, a continuación indico lo que deben cumplir los aportes hacia este repositorio, en la medida de lo posible.

Si no te atreves a lanzarlo como _Pull Request_, puedes incluirlo como Issue, pero siempre tratando de dar la mayor información posible, y, como mínimo, enlace de _stream_ y web de procedencia.

## Explicación de cada columna y posibles valores

### TV
Emplazarlo al final de su categoría, así es más sencillo para nosotros después moverlo a la posición correspondiente.

#### Canal
El nombre oficial del canal.

#### M3U8
Aunque el campo se llame m3u8, se aceptan **dos** posibles formatos de _stream_. Ambos formatos tienen obligatoria su obtención a través de la plataforma oficial del emisor.

- **m3u8**: Priorizando las opciones `master.m3u8` y `playlist.m3u8`. 
- **youtube**: En caso que la cadena emita vía _YouTube_. Priorizando el formato `https://youtu.be/XXXXXX`.

Si el canal emite:
- [geolocalizado](https://github.com/LaQuay/TDTChannels/wiki/FAQs#diferencia-entre-una-emisi%C3%B3n-geo-y-no-geo) a **nivel español**, se deberá añadir la coletilla `# GEO`. 
- [geolocalizado](https://github.com/LaQuay/TDTChannels/wiki/FAQs#diferencia-entre-una-emisi%C3%B3n-geo-y-no-geo) a **nivel catalán**, se deberá añadir la coletilla `# GEOCAT`. 
- En otro idioma que no sea el español, se deberá indicar con el código [ISO_639-1](https://es.wikipedia.org/wiki/ISO_639-1). Por ejemplo, si emite en Inglés será `[m3u8 # EN]`.
- Diferentes calidades vía enlace para forzar el _SD_ o _HD_, entonces se podrán indicar con las coletillas `# SD` o `# HD`.
- Varias opciones de emisión `p.e. +24 de TVE`, estas se podrán indicar con las coletillas `# 1`, `# 2`, etc.

Se pueden combinar diferentes opciones concatenandolas. Por ejemplo un canal en _HD_ y geolocalizado a catalunya sería `[m3u8 # GEOCAT # HD]`. Preferentemente manteniendo el orden de los puntos anteriores.

Excepciones:

No se pueden subir enlaces convertidos a _m3u8_ de _Youtube_, _Vimeo_, _Dailymotion_, pues caducan muy rápido.

#### Web
En este apartado se debería indicar la web de dónde sale el _stream_.

#### Logo
- Incluir el que más represente la emisión a mostrar.
- Fuentes de datos, en orden de preferencia: Redes sociales del canal (_Facebook_, _Twitter_), Wikipedia, propio canal, etc.
- Medida recomendada de 320x320, máximo 400x400.
- Formato PNG, y si no es posible JPG.
- Preferiblemente sin transparencias y con fondo blanco.
- No es necesaria la aparición explicita del nombre del canal en el logo.

#### EPG ID
No indiques nada en este campo, lo modificaremos nosotros a posterior.

#### Info
- `W3U`: La emisión introducida en el apartado `WEB` es reproducible por _Wiseplay_. De esta forma se incluirá como _stream_ en dicha lista.
- `NONAV`: La emisión no funciona en navegadores debido a [CORS](https://developer.mozilla.org/es/docs/Web/HTTP/Access_control_CORS).
- `CODEC`: El canal necesita de un códec especial para ser reproducido.

En caso de tener más de un `TAG` de información, concatenar con comas y sin espacios.

### Radio
Igual que la televisión a excepción que el campo `EPG ID` no existe, y de los formatos aceptados

#### Stream
_En construcción_

## Aviso general
- Únicamente se recoje información externa, no se permite subir contenidos al repositorio.

Gracias por colaborar!
