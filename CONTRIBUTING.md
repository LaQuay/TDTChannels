Para hacer más sencillas las contribuciones, a continuación indico las características que deben cumplir los aportes hacia este repositorio, en la medida de lo posible. Si no te atreves a lanzarlo como _Pull Request_, puedes incluirlo como Issue, pero siempre tratando de dar la mayor información posible, y, como mínimo, enlace de _stream_ y web de procedencia.

## Explicación de cada columna y posibles valores
Emplazar la nueva emisión al final de su categoría, así es más sencillo para nosotros después moverlo a la posición correspondiente.

### Televisión

#### Canal
El nombre oficial del canal.

#### M3U8
Se aceptan los siguientes formatos de _stream_. Ambos formatos tienen obligatoria su obtención a través de la plataforma oficial del emisor. Y siempre han de ser emisiones en directo.

- **m3u8**: Priorizando las opciones `master.m3u8` y `playlist.m3u8`. Este formato es compatible con la mayoría de reproductores.
- **youtube**: Si la cadena emite vía _YouTube_. Con formato `https://youtu.be/XXXXXX` si el tiempo de vida del stream es superior a dos semanas, y con el formato `/channel/.../live` en caso contrario. Este formato es compatible con la aplicación Android TDTChannels, la web, y la lista W3U.
- **twitch**: Si la cadena emite vía _Twitch_. Este formato únicamente es compatible con la aplicación Android TDTChannels.
- **dailymotion**: Si la cadena emite vía _Dailymotion_. Este formato únicamente es compatible con la aplicación Android TDTChannels.
- **vimeo**: Si la cadena emite vía _Vimeo_. Este formato únicamente es compatible con la aplicación Android TDTChannels.

Si el canal emite:
- [geolocalizado](https://github.com/LaQuay/TDTChannels/wiki/FAQs#diferencia-entre-una-emisi%C3%B3n-geo-y-no-geo) a **nivel español**, se deberá añadir la coletilla `# GEO`. 
- [geolocalizado](https://github.com/LaQuay/TDTChannels/wiki/FAQs#diferencia-entre-una-emisi%C3%B3n-geo-y-no-geo) a **nivel catalán**, se deberá añadir la coletilla `# GEOCAT`. 
- En otro idioma que no sea el español, se deberá indicar con el código [ISO_639-1](https://es.wikipedia.org/wiki/ISO_639-1). Por ejemplo, si emite en Inglés será `[m3u8 # EN]`.
- Diferentes calidades vía enlace para forzar el _SD_ o _HD_, entonces se podrán indicar con las coletillas `# SD` o `# HD`.
- Varias opciones de emisión `p.e. +24 de TVE`, estas se podrán indicar con las coletillas `# 1`, `# 2`, etc.

Se pueden combinar diferentes opciones concatenandolas. Por ejemplo un canal en _HD_ y geolocalizado a catalunya sería `[m3u8 # GEOCAT # HD]`. Preferentemente manteniendo el orden de los puntos anteriores.

Excepciones:
- No se pueden subir enlaces convertidos a _m3u8_ de _Youtube_, _Twitch_, _Dailymotion_, _Vimeo_, etc. Pues caducan muy rápido.

#### Web
En este apartado se debería indicar la web de dónde sale el _stream_.

#### Logo
- Incluir el que más represente la emisión a mostrar.
- Fuentes de datos, en orden de preferencia: Redes sociales del canal: _Facebook_, _Twitter_, _YouTube_; propio canal, etc.
- Medida recomendada de 200x200.
- Formato PNG, y si no es posible JPG.
- Preferiblemente sin transparencias y con fondo blanco.
- No es necesaria la aparición explicita del nombre del canal en el logo.

#### EPG ID
No indiques nada en este campo, lo modificaremos nosotros a posterior.

#### Info
- `W3U`: La emisión introducida en el apartado `WEB` es reproducible por _Wiseplay_. De esta forma se incluirá como _stream_ en dicha lista.
- `NONAV`: La emisión no funciona en navegadores debido a [CORS](https://developer.mozilla.org/es/docs/Web/HTTP/Access_control_CORS).
- `CODEC`: El canal necesita de un códec especial para ser reproducido.
- `EMB`: Para el reproductor Web y _Wiseplay_. Indica si el _stream_ ha de ser `"embed": "true"`, por ejemplo cuando se incluye un enlace a YouTube con `/live`.
- `WICE`: Exclusivamente para _Wiseplay_. Indica si el _stream_ ha de ser `"isHost": "false"`.

En caso de tener más de un `TAG` de información, concatenar con comas y sin espacios.

### Radio
Igual que la televisión a excepción de los formatos aceptados para la reproducción.

#### Stream
Aplica lo mismo que para la TV. La preferencia siempre será la de elegir el stream en _m3u8_. Formatos aceptados:

- M3U8
- M3U
- MP3
- Stream

## Aviso general
- Únicamente se recoje información externa, no se permite subir contenidos al repositorio.

Gracias por colaborar!
