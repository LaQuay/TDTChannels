# coding=utf-8

import json
import re

import requests

from ambit import Ambito
from channel import Channel
from country import Country


def stringbetween(text, start, end):
    result = re.search('(?<=' + start + ')(.*)(?=' + end + ')', text, re.DOTALL)
    return result.group(1)


def stringbetweenparantheses(text):
    return text.split("(")[1].split(")")[0]


def get_channels_from_part(text):
    line_where_first_channel_starts = 15
    attributes_per_item = 6
    channel_list = []
    list_to_iterate = text.split("|")[line_where_first_channel_starts:]
    while "\n" in list_to_iterate:
        list_to_iterate.remove("\n")
    while "\n\n" in list_to_iterate:
        list_to_iterate.remove("\n\n")
    for i in range(0, len(list_to_iterate), attributes_per_item):
        item_name = list_to_iterate[i].strip()

        item_options = list_to_iterate[i + 1].strip()

        item_web = list_to_iterate[i + 2].strip()
        if len(item_web) > 0 and item_web[0] != "-":
            item_web = stringbetweenparantheses(item_web)
        if len(item_web) == 1:
            item_web = ""

        item_resolution = list_to_iterate[i + 3].strip()
        if len(item_resolution) == 1:
            item_resolution = ""

        item_logo = list_to_iterate[i + 4].strip()
        if len(item_logo) > 0 and item_logo[0] != "-":
            item_logo = stringbetweenparantheses(item_logo)
        if len(item_logo) == 1:
            item_logo = ""

        item_epg = list_to_iterate[i + 5].strip()
        if len(item_epg) == 1:
            item_epg = ""

        item_options = item_options.split(" - ")

        channel = Channel(item_name, item_web, item_resolution, item_logo, item_epg)
        if len(item_options) > 0 and item_options[0] != "-":
            for option in item_options:
                format = (option[1:5]).replace("]", "")
                url = stringbetweenparantheses(option)
                channel.add_option(format, url)
        channel_list.append(channel)
    return channel_list


page = requests.get('https://raw.githubusercontent.com/LaQuay/TDTChannels/add-local-m3u8/TELEVISION.md',
                    headers={'Cache-Control': 'no-cache'})
content = str(page.text)

spain = Country("Spain")
international = Country("International")

content_nacional = stringbetween(content, "### Nacionales", "### Locales")
content_local = stringbetween(content, "### Locales", "## Internacionales")

canales_nacionales = stringbetween(content_nacional, "", "### Informativos")
spain.add_ambit(Ambito("Generalistas", get_channels_from_part(canales_nacionales)))

canales_informativos = stringbetween(content_nacional, "### Informativos", "### Deportivos")
spain.add_ambit(Ambito("Informativos", get_channels_from_part(canales_informativos)))

canales_deportivos = stringbetween(content_nacional, "### Deportivos", "### Infantiles")
spain.add_ambit(Ambito("Deportivos", get_channels_from_part(canales_deportivos)))

canales_infantiles = stringbetween(content_nacional, "### Infantiles", "### Musicales")
spain.add_ambit(Ambito("Infantiles", get_channels_from_part(canales_infantiles)))

canales_musicales = stringbetween(content_nacional, "### Musicales", "### Autonómicos")
spain.add_ambit(Ambito("Musicales", get_channels_from_part(canales_musicales)))

canales_autonomicos_andalucia = stringbetween(content_nacional, "#### Andalucía", "#### Aragón")
spain.add_ambit(Ambito("Andalucía", get_channels_from_part(canales_autonomicos_andalucia)))

canales_autonomicos_aragon = stringbetween(content_nacional, "#### Aragón", "#### Asturias")
spain.add_ambit(Ambito("Aragón", get_channels_from_part(canales_autonomicos_aragon)))

canales_autonomicos_asturias = stringbetween(content_nacional, "#### Asturias", "#### Canarias")
spain.add_ambit(Ambito("Asturias", get_channels_from_part(canales_autonomicos_asturias)))

canales_autonomicos_canarias = stringbetween(content_nacional, "#### Canarias", "#### Cantabria")
spain.add_ambit(Ambito("Canarias", get_channels_from_part(canales_autonomicos_canarias)))

canales_autonomicos_cantabria = stringbetween(content_nacional, "#### Cantabria", "#### Castilla La-Mancha")
spain.add_ambit(Ambito("Cantabria", get_channels_from_part(canales_autonomicos_cantabria)))

canales_autonomicos_castilla_mancha = stringbetween(content_nacional, "#### Castilla La-Mancha", "#### Castilla y León")
spain.add_ambit(Ambito("Castilla La-Mancha", get_channels_from_part(canales_autonomicos_castilla_mancha)))

canales_autonomicos_castilla_leon = stringbetween(content_nacional, "#### Castilla y León", "#### Cataluña")
spain.add_ambit(Ambito("Castilla y León", get_channels_from_part(canales_autonomicos_castilla_leon)))

canales_autonomicos_catalunya = stringbetween(content_nacional, "#### Cataluña", "#### Ceuta")
spain.add_ambit(Ambito("Cataluña", get_channels_from_part(canales_autonomicos_catalunya)))

canales_autonomicos_ceuta = stringbetween(content_nacional, "#### Ceuta", "#### Extremadura")
spain.add_ambit(Ambito("Ceuta", get_channels_from_part(canales_autonomicos_ceuta)))

canales_autonomicos_extremadura = stringbetween(content_nacional, "#### Extremadura", "#### Galicia")
spain.add_ambit(Ambito("Extremadura", get_channels_from_part(canales_autonomicos_extremadura)))

canales_autonomicos_galicia = stringbetween(content_nacional, "#### Galicia", "#### Islas Baleares")
spain.add_ambit(Ambito("Galicia", get_channels_from_part(canales_autonomicos_galicia)))

canales_autonomicos_islas_baleares = stringbetween(content_nacional, "#### Islas Baleares", "#### La Rioja")
spain.add_ambit(Ambito("Islas Baleares", get_channels_from_part(canales_autonomicos_islas_baleares)))

canales_autonomicos_la_rioja = stringbetween(content_nacional, "#### La Rioja", "#### Madrid")
spain.add_ambit(Ambito("La Rioja", get_channels_from_part(canales_autonomicos_la_rioja)))

canales_autonomicos_madrid = stringbetween(content_nacional, "#### Madrid", "#### Melilla")
spain.add_ambit(Ambito("Madrid", get_channels_from_part(canales_autonomicos_madrid)))

canales_autonomicos_melilla = stringbetween(content_nacional, "#### Melilla", "#### Murcia")
spain.add_ambit(Ambito("Melilla", get_channels_from_part(canales_autonomicos_melilla)))

canales_autonomicos_murcia = stringbetween(content_nacional, "#### Murcia", "#### Navarra")
spain.add_ambit(Ambito("Murcia", get_channels_from_part(canales_autonomicos_murcia)))

canales_autonomicos_navarra = stringbetween(content_nacional, "#### Navarra", "#### País Vasco")
spain.add_ambit(Ambito("Navarra", get_channels_from_part(canales_autonomicos_navarra)))

canales_autonomicos_pais_vasco = stringbetween(content_nacional, "#### País Vasco", "#### Valencia")
spain.add_ambit(Ambito("País Vasco", get_channels_from_part(canales_autonomicos_pais_vasco)))

canales_autonomicos_valencia = stringbetween(content_nacional, "#### Valencia", "### Locales")
spain.add_ambit(Ambito("Valencia", get_channels_from_part(canales_autonomicos_valencia)))

canales_locales_andalucia = stringbetween(content_local, "#### Andalucía", "#### Aragón")
spain.get_ambit("Andalucía").add_channels(get_channels_from_part(canales_locales_andalucia))

canales_locales_aragon = stringbetween(content_local, "#### Aragón", "#### Asturias")
spain.get_ambit("Aragón").add_channels(get_channels_from_part(canales_locales_aragon))

canales_locales_asturias = stringbetween(content_local, "#### Asturias", "#### Canarias")
spain.get_ambit("Asturias").add_channels(get_channels_from_part(canales_locales_asturias))

canales_locales_canarias = stringbetween(content_local, "#### Canarias", "#### Cantabria")
spain.get_ambit("Canarias").add_channels(get_channels_from_part(canales_locales_canarias))

canales_locales_cantabria = stringbetween(content_local, "#### Cantabria", "#### Castilla La-Mancha")
spain.get_ambit("Cantabria").add_channels(get_channels_from_part(canales_locales_cantabria))

canales_locales_castilla_mancha = stringbetween(content_local, "#### Castilla La-Mancha", "#### Castilla y León")
spain.get_ambit("Castilla La-Mancha").add_channels(get_channels_from_part(canales_locales_castilla_mancha))

canales_locales_castilla_leon = stringbetween(content_local, "#### Castilla y León", "#### Cataluña")
spain.get_ambit("Castilla y León").add_channels(get_channels_from_part(canales_locales_castilla_leon))

canales_locales_catalunya = stringbetween(content_local, "#### Cataluña", "#### Ceuta")
spain.get_ambit("Cataluña").add_channels(get_channels_from_part(canales_locales_catalunya))

canales_locales_ceuta = stringbetween(content_local, "#### Ceuta", "#### Extremadura")
spain.get_ambit("Ceuta").add_channels(get_channels_from_part(canales_locales_ceuta))

canales_locales_extremadura = stringbetween(content_local, "#### Extremadura", "#### Galicia")
spain.get_ambit("Extremadura").add_channels(get_channels_from_part(canales_locales_extremadura))

canales_locales_galicia = stringbetween(content_local, "#### Galicia", "#### Islas Baleares")
spain.get_ambit("Galicia").add_channels(get_channels_from_part(canales_locales_galicia))

canales_locales_islas_baleares = stringbetween(content_local, "### Islas Baleares", "#### La Rioja")
spain.get_ambit("Islas Baleares").add_channels(get_channels_from_part(canales_locales_islas_baleares))

canales_locales_la_rioja = stringbetween(content_local, "#### La Rioja", "#### Madrid")
spain.get_ambit("La Rioja").add_channels(get_channels_from_part(canales_locales_la_rioja))

canales_locales_madrid = stringbetween(content_local, "#### Madrid", "#### Melilla")
spain.get_ambit("Madrid").add_channels(get_channels_from_part(canales_locales_madrid))

canales_locales_melilla = stringbetween(content_local, "#### Melilla", "#### Murcia")
spain.get_ambit("Melilla").add_channels(get_channels_from_part(canales_locales_melilla))

canales_locales_murcia = stringbetween(content_local, "#### Murcia", "#### Navarra")
spain.get_ambit("Murcia").add_channels(get_channels_from_part(canales_locales_murcia))

canales_locales_navarra = stringbetween(content_local, "#### Navarra", "#### País Vasco")
spain.get_ambit("Navarra").add_channels(get_channels_from_part(canales_locales_navarra))

canales_locales_pais_vasco = stringbetween(content_local, "#### País Vasco", "#### Valencia")
spain.get_ambit("País Vasco").add_channels(get_channels_from_part(canales_locales_pais_vasco))

canales_locales_valencia = stringbetween(content_local, "#### Valencia", "## Locales")
spain.get_ambit("Valencia").add_channels(get_channels_from_part(canales_locales_valencia))

canales_internacionales = stringbetween(content, "## Internacionales", "### Andorra")
international.add_ambit(Ambito("Internacional", get_channels_from_part(canales_internacionales)))

# Save data to JSON file
json_file = open('./public/output/channels.json', "w+")
# TODO Add license
json_file.write("[")
json_file.write(json.dumps(spain.to_json()))
json_file.write(", ")
json_file.write(json.dumps(international.to_json()))
json_file.write("]")
json_file.close()

# Save data to M3U8 file	
text_file = open('./public/output/channels.m3u8', "w+")
text_file.write("#EXTM3U" + "\n")
text_file.write("# @LaQuay https://github.com/LaQuay/TDTChannels" + "\n")
text_file.write(spain.to_m3u8())
text_file.write(international.to_m3u8())
text_file.close()

print("JSON + M3U8 Updated")
