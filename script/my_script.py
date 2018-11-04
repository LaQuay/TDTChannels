# coding=utf-8

import json

import requests

from ambit import Ambito
from channel import Channel
from country import Country


def substring(text, match):
    return text.split(match)


def stringbetween(text, start, end):
    text_from_start_to_all = substring(text, start)[1]
    text_from_start_to_end = substring(text_from_start_to_all, end)[0]
    return text_from_start_to_end


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
            item_web = stringbetween(item_web, "(", ")")
        if len(item_web) == 1:
            item_web = ""

        item_resolution = list_to_iterate[i + 3].strip()
        if len(item_resolution) == 1:
            item_resolution = ""

        item_logo = list_to_iterate[i + 4].strip()
        if len(item_logo) > 0 and item_logo[0] != "-":
            item_logo = stringbetween(item_logo, "(", ")")
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
                url = stringbetween(option, "(", ")")
                channel.add_option(format, url)
        channel_list.append(channel)
    return channel_list


page = requests.get('https://raw.githubusercontent.com/LaQuay/TDTChannels/master/README.md',
                    headers={'Cache-Control': 'no-cache'})
content = str(page.text)

spain = Country("Spain")
international = Country("International")

canales_nacionales = stringbetween(content, "### Nacionales", "### Informativos")
spain.add_ambit(Ambito("Generalistas", get_channels_from_part(canales_nacionales)))

canales_informativos = stringbetween(content, "### Informativos", "### Deportivos")
spain.add_ambit(Ambito("Informativos", get_channels_from_part(canales_informativos)))

canales_deportivos = stringbetween(content, "### Deportivos", "### Infantiles")
spain.add_ambit(Ambito("Deportivos", get_channels_from_part(canales_deportivos)))

canales_infantiles = stringbetween(content, "### Infantiles", "### Musicales")
spain.add_ambit(Ambito("Infantiles", get_channels_from_part(canales_infantiles)))

canales_musicales = stringbetween(content, "### Musicales", "### Autonómicos")
spain.add_ambit(Ambito("Musicales", get_channels_from_part(canales_musicales)))

canales_autonomicos_andalucia = stringbetween(content, "#### Andalucía", "#### Aragón")
spain.add_ambit(Ambito("Andalucía", get_channels_from_part(canales_autonomicos_andalucia)))

canales_autonomicos_aragon = stringbetween(content, "#### Aragón", "#### Asturias")
spain.add_ambit(Ambito("Aragón", get_channels_from_part(canales_autonomicos_aragon)))

canales_autonomicos_asturias = stringbetween(content, "#### Asturias", "#### Canarias")
spain.add_ambit(Ambito("Asturias", get_channels_from_part(canales_autonomicos_asturias)))

canales_autonomicos_canarias = stringbetween(content, "#### Canarias", "#### Cantabria")
spain.add_ambit(Ambito("Canarias", get_channels_from_part(canales_autonomicos_canarias)))

canales_autonomicos_cantabria = stringbetween(content, "#### Cantabria", "#### Castilla la Mancha")
spain.add_ambit(Ambito("Cantabria", get_channels_from_part(canales_autonomicos_cantabria)))

canales_autonomicos_castilla_mancha = stringbetween(content, "#### Castilla la Mancha", "#### Castilla y León")
spain.add_ambit(Ambito("Castilla la Mancha", get_channels_from_part(canales_autonomicos_castilla_mancha)))

canales_autonomicos_castilla_leon = stringbetween(content, "#### Castilla y León", "#### Catalunya")
spain.add_ambit(Ambito("Castilla y León", get_channels_from_part(canales_autonomicos_castilla_leon)))

canales_autonomicos_catalunya = stringbetween(content, "#### Catalunya", "#### Ceuta")
spain.add_ambit(Ambito("Catalunya", get_channels_from_part(canales_autonomicos_catalunya)))

canales_autonomicos_ceuta = stringbetween(content, "#### Ceuta", "#### Extremadura")
spain.add_ambit(Ambito("Ceuta", get_channels_from_part(canales_autonomicos_ceuta)))

canales_autonomicos_extremadura = stringbetween(content, "#### Extremadura", "#### Galicia")
spain.add_ambit(Ambito("Extremadura", get_channels_from_part(canales_autonomicos_extremadura)))

canales_autonomicos_galicia = stringbetween(content, "#### Galicia", "#### Islas Baleares")
spain.add_ambit(Ambito("Galicia", get_channels_from_part(canales_autonomicos_galicia)))

canales_autonomicos_islas_baleares = stringbetween(content, "### Islas Baleares", "#### Madrid")
spain.add_ambit(Ambito("Islas Baleares", get_channels_from_part(canales_autonomicos_islas_baleares)))

canales_autonomicos_madrid = stringbetween(content, "#### Madrid", "#### Melilla")
spain.add_ambit(Ambito("Madrid", get_channels_from_part(canales_autonomicos_madrid)))

canales_autonomicos_melilla = stringbetween(content, "#### Melilla", "#### Murcia")
spain.add_ambit(Ambito("Melilla", get_channels_from_part(canales_autonomicos_melilla)))

canales_autonomicos_murcia = stringbetween(content, "#### Murcia", "#### Navarra")
spain.add_ambit(Ambito("Murcia", get_channels_from_part(canales_autonomicos_murcia)))

canales_autonomicos_navarra = stringbetween(content, "#### Navarra", "#### Pais Vasco")
spain.add_ambit(Ambito("Navarra", get_channels_from_part(canales_autonomicos_navarra)))

canales_autonomicos_pais_vasco = stringbetween(content, "#### Pais Vasco", "#### La Rioja")
spain.add_ambit(Ambito("Pais Vasco", get_channels_from_part(canales_autonomicos_pais_vasco)))

canales_autonomicos_la_rioja = stringbetween(content, "#### La Rioja", "#### Valencia")
spain.add_ambit(Ambito("La Rioja", get_channels_from_part(canales_autonomicos_la_rioja)))

canales_autonomicos_valencia = stringbetween(content, "#### Valencia", "## Internacionales")
spain.add_ambit(Ambito("Valencia", get_channels_from_part(canales_autonomicos_valencia)))

canales_internacionales = stringbetween(content, "## Internacionales", "### Andorra")
international.add_ambit(Ambito("Internacional", get_channels_from_part(canales_internacionales)))

# Save data to JSON file
json_file = open('./public/output/channels.json', "w+")
# TODO Anadir copyright
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
