# coding=utf-8
import json

import requests

from ambit import Ambito
from country import Country
from utils import stringbetween, get_tv_channels_from_part, get_license_info

page = requests.get('https://raw.githubusercontent.com/LaQuay/TDTChannels/master/TELEVISION.md',
                    headers={'Cache-Control': 'no-cache'})
content = str(page.text)

print("Updating TV files")

spain = Country("Spain")
andorra = Country("Andorra")
international = Country("International")

content_nacional = stringbetween(content, "## Nacionales", "## Locales")
content_local = stringbetween(content, "## Locales", "## Internacionales")

canales_nacionales = stringbetween(content_nacional, "", "## Informativos")
spain.add_ambit(Ambito("Generalistas", get_tv_channels_from_part(canales_nacionales)))

canales_informativos = stringbetween(content_nacional, "## Informativos", "## Deportivos")
spain.add_ambit(Ambito("Informativos", get_tv_channels_from_part(canales_informativos)))

canales_deportivos = stringbetween(content_nacional, "## Deportivos", "## Infantiles")
spain.add_ambit(Ambito("Deportivos", get_tv_channels_from_part(canales_deportivos)))

canales_infantiles = stringbetween(content_nacional, "## Infantiles", "## Musicales")
spain.add_ambit(Ambito("Infantiles", get_tv_channels_from_part(canales_infantiles)))

canales_musicales = stringbetween(content_nacional, "## Musicales", "## Webcams")
spain.add_ambit(Ambito("Musicales", get_tv_channels_from_part(canales_musicales)))

canales_webcams = stringbetween(content_nacional, "## Webcams", "## Autonómicos")
spain.add_ambit(Ambito("Webcams", get_tv_channels_from_part(canales_webcams)))

canales_autonomicos_andalucia = stringbetween(content_nacional, "### Andalucía", "### Aragón")
spain.add_ambit(Ambito("Andalucía", get_tv_channels_from_part(canales_autonomicos_andalucia)))

canales_autonomicos_aragon = stringbetween(content_nacional, "### Aragón", "### Asturias")
spain.add_ambit(Ambito("Aragón", get_tv_channels_from_part(canales_autonomicos_aragon)))

canales_autonomicos_asturias = stringbetween(content_nacional, "### Asturias", "### Canarias")
spain.add_ambit(Ambito("Asturias", get_tv_channels_from_part(canales_autonomicos_asturias)))

canales_autonomicos_canarias = stringbetween(content_nacional, "### Canarias", "### Cantabria")
spain.add_ambit(Ambito("Canarias", get_tv_channels_from_part(canales_autonomicos_canarias)))

canales_autonomicos_cantabria = stringbetween(content_nacional, "### Cantabria", "### Castilla La-Mancha")
spain.add_ambit(Ambito("Cantabria", get_tv_channels_from_part(canales_autonomicos_cantabria)))

canales_autonomicos_castilla_mancha = stringbetween(content_nacional, "### Castilla La-Mancha", "### Castilla y León")
spain.add_ambit(Ambito("Castilla La-Mancha", get_tv_channels_from_part(canales_autonomicos_castilla_mancha)))

canales_autonomicos_castilla_leon = stringbetween(content_nacional, "### Castilla y León", "### Cataluña")
spain.add_ambit(Ambito("Castilla y León", get_tv_channels_from_part(canales_autonomicos_castilla_leon)))

canales_autonomicos_catalunya = stringbetween(content_nacional, "### Cataluña", "### Ceuta")
spain.add_ambit(Ambito("Cataluña", get_tv_channels_from_part(canales_autonomicos_catalunya)))

canales_autonomicos_ceuta = stringbetween(content_nacional, "### Ceuta", "### Extremadura")
spain.add_ambit(Ambito("Ceuta", get_tv_channels_from_part(canales_autonomicos_ceuta)))

canales_autonomicos_extremadura = stringbetween(content_nacional, "### Extremadura", "### Galicia")
spain.add_ambit(Ambito("Extremadura", get_tv_channels_from_part(canales_autonomicos_extremadura)))

canales_autonomicos_galicia = stringbetween(content_nacional, "### Galicia", "### Islas Baleares")
spain.add_ambit(Ambito("Galicia", get_tv_channels_from_part(canales_autonomicos_galicia)))

canales_autonomicos_islas_baleares = stringbetween(content_nacional, "### Islas Baleares", "### La Rioja")
spain.add_ambit(Ambito("Islas Baleares", get_tv_channels_from_part(canales_autonomicos_islas_baleares)))

canales_autonomicos_la_rioja = stringbetween(content_nacional, "### La Rioja", "### Madrid")
spain.add_ambit(Ambito("La Rioja", get_tv_channels_from_part(canales_autonomicos_la_rioja)))

canales_autonomicos_madrid = stringbetween(content_nacional, "### Madrid", "### Melilla")
spain.add_ambit(Ambito("Madrid", get_tv_channels_from_part(canales_autonomicos_madrid)))

canales_autonomicos_melilla = stringbetween(content_nacional, "### Melilla", "### Murcia")
spain.add_ambit(Ambito("Melilla", get_tv_channels_from_part(canales_autonomicos_melilla)))

canales_autonomicos_murcia = stringbetween(content_nacional, "### Murcia", "### Navarra")
spain.add_ambit(Ambito("Murcia", get_tv_channels_from_part(canales_autonomicos_murcia)))

canales_autonomicos_navarra = stringbetween(content_nacional, "### Navarra", "### País Vasco")
spain.add_ambit(Ambito("Navarra", get_tv_channels_from_part(canales_autonomicos_navarra)))

canales_autonomicos_pais_vasco = stringbetween(content_nacional, "### País Vasco", "### Valencia")
spain.add_ambit(Ambito("País Vasco", get_tv_channels_from_part(canales_autonomicos_pais_vasco)))

canales_autonomicos_valencia = stringbetween(content_nacional, "### Valencia", "")
spain.add_ambit(Ambito("Valencia", get_tv_channels_from_part(canales_autonomicos_valencia)))

canales_locales_andalucia = stringbetween(content_local, "### Andalucía", "### Aragón")
spain.get_ambit("Andalucía").add_channels(get_tv_channels_from_part(canales_locales_andalucia))

canales_locales_aragon = stringbetween(content_local, "### Aragón", "### Asturias")
spain.get_ambit("Aragón").add_channels(get_tv_channels_from_part(canales_locales_aragon))

canales_locales_asturias = stringbetween(content_local, "### Asturias", "### Canarias")
spain.get_ambit("Asturias").add_channels(get_tv_channels_from_part(canales_locales_asturias))

canales_locales_canarias = stringbetween(content_local, "### Canarias", "### Cantabria")
spain.get_ambit("Canarias").add_channels(get_tv_channels_from_part(canales_locales_canarias))

canales_locales_cantabria = stringbetween(content_local, "### Cantabria", "### Castilla La-Mancha")
spain.get_ambit("Cantabria").add_channels(get_tv_channels_from_part(canales_locales_cantabria))

canales_locales_castilla_mancha = stringbetween(content_local, "### Castilla La-Mancha", "### Castilla y León")
spain.get_ambit("Castilla La-Mancha").add_channels(get_tv_channels_from_part(canales_locales_castilla_mancha))

canales_locales_castilla_leon = stringbetween(content_local, "### Castilla y León", "### Cataluña")
spain.get_ambit("Castilla y León").add_channels(get_tv_channels_from_part(canales_locales_castilla_leon))

canales_locales_catalunya = stringbetween(content_local, "### Cataluña", "### Ceuta")
spain.get_ambit("Cataluña").add_channels(get_tv_channels_from_part(canales_locales_catalunya))

canales_locales_ceuta = stringbetween(content_local, "### Ceuta", "### Extremadura")
spain.get_ambit("Ceuta").add_channels(get_tv_channels_from_part(canales_locales_ceuta))

canales_locales_extremadura = stringbetween(content_local, "### Extremadura", "### Galicia")
spain.get_ambit("Extremadura").add_channels(get_tv_channels_from_part(canales_locales_extremadura))

canales_locales_galicia = stringbetween(content_local, "### Galicia", "### Islas Baleares")
spain.get_ambit("Galicia").add_channels(get_tv_channels_from_part(canales_locales_galicia))

canales_locales_islas_baleares = stringbetween(content_local, "### Islas Baleares", "### La Rioja")
spain.get_ambit("Islas Baleares").add_channels(get_tv_channels_from_part(canales_locales_islas_baleares))

canales_locales_la_rioja = stringbetween(content_local, "### La Rioja", "### Madrid")
spain.get_ambit("La Rioja").add_channels(get_tv_channels_from_part(canales_locales_la_rioja))

canales_locales_madrid = stringbetween(content_local, "### Madrid", "### Melilla")
spain.get_ambit("Madrid").add_channels(get_tv_channels_from_part(canales_locales_madrid))

canales_locales_melilla = stringbetween(content_local, "### Melilla", "### Murcia")
spain.get_ambit("Melilla").add_channels(get_tv_channels_from_part(canales_locales_melilla))

canales_locales_murcia = stringbetween(content_local, "### Murcia", "### Navarra")
spain.get_ambit("Murcia").add_channels(get_tv_channels_from_part(canales_locales_murcia))

canales_locales_navarra = stringbetween(content_local, "### Navarra", "### País Vasco")
spain.get_ambit("Navarra").add_channels(get_tv_channels_from_part(canales_locales_navarra))

canales_locales_pais_vasco = stringbetween(content_local, "### País Vasco", "### Valencia")
spain.get_ambit("País Vasco").add_channels(get_tv_channels_from_part(canales_locales_pais_vasco))

canales_locales_valencia = stringbetween(content_local, "### Valencia", "")
spain.get_ambit("Valencia").add_channels(get_tv_channels_from_part(canales_locales_valencia))

canales_internacionales = stringbetween(content, "## Internacionales", "## Andorra")
international.add_ambit(Ambito("Internacional", get_tv_channels_from_part(canales_internacionales)))

canales_andorra = stringbetween(content, "## Andorra", "")
andorra.add_ambit(Ambito("Andorra", get_tv_channels_from_part(canales_andorra)))

# Save data to JSON file
json_file = open('./public/output/channels.json', "w+")
json_file.write("[")
json_file.write(json.dumps(get_license_info()))
json_file.write(", ")
json_file.write(json.dumps(spain.to_json()))
json_file.write(", ")
json_file.write(json.dumps(international.to_json()))
json_file.write(", ")
json_file.write(json.dumps(andorra.to_json()))
json_file.write("]")
json_file.close()
print("JSON Updated")

# Save data to M3U8 file	
text_file = open('./public/output/channels.m3u8', "w+")
text_file.write("#EXTM3U @LaQuay https://github.com/LaQuay/TDTChannels" + "\n")
text_file.write(
    "#EXTM3U url-tvg=\"https://raw.githubusercontent.com/HelmerLuzo/TDTChannels_EPG/master/TDTChannels_EPG.xml\"\n")
text_file.write(spain.to_m3u8())
text_file.write(international.to_m3u8())
text_file.write(andorra.to_m3u8())
text_file.close()
print("M3U8 Updated")

# Save data to M3U file
text_file = open('./public/output/channels.m3u', "w+")
text_file.write("#EXTM3U @LaQuay https://github.com/LaQuay/TDTChannels" + "\n")
text_file.write(
    "#EXTM3U url-tvg=\"https://raw.githubusercontent.com/HelmerLuzo/TDTChannels_EPG/master/TDTChannels_EPG.xml\"\n")
text_file.write(spain.to_m3u8())
text_file.write(international.to_m3u8())
text_file.write(andorra.to_m3u8())
text_file.close()
print("M3U Updated")

# Save data to .tv file (Enigma2)
text_file = open('./public/output/userbouquet.tdtchannels.tv', "w+")
text_file.write("#NAME @LaQuay https://github.com/LaQuay/TDTChannels" + "\n")
text_file.write(spain.to_enigma2())
text_file.write(international.to_enigma2())
text_file.write(andorra.to_enigma2())
text_file.close()
print("ENIGMA2 Updated")
