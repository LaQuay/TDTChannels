import re

from channel import Channel


def get_license_info():
    return {
        "source": "https://github.com/LaQuay/TDTChannels",
        "license": "https://github.com/LaQuay/TDTChannels/blob/master/LICENSE"
    }


def stringbetween(text, start, end):
    result = re.search('(?<=' + start + ')(.*)(?=' + end + ')', text, re.DOTALL)
    return result.group(1)


def stringbetweenparantheses(text):
    return text.split("(")[1].split(")")[0]


def get_channels_from_part(text):
    line_where_first_channel_starts = 17
    attributes_per_item = 7
    list_to_iterate = text.split("|")[line_where_first_channel_starts:-1]
    while "\n" in list_to_iterate:
        list_to_iterate.remove("\n")
    channel_list = []
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

        item_extra_info = list_to_iterate[i + 6].strip()
        if len(item_extra_info) == 1:
            item_extra_info = ""

        channel = Channel(item_name, item_web, item_resolution, item_logo, item_epg, item_extra_info)
        item_options = item_options.split(" - ")
        if len(item_options) > 0 and item_options[0] != "-":
            for option in item_options:
                format = (option[1:5]).replace("]", "")
                url = stringbetweenparantheses(option)
                channel.add_option(format, url)
        channel_list.append(channel)
    return channel_list
