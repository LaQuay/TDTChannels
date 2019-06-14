# TODO Create TVChannel and RadioChannel
class Channel:
    def __init__(self, name, web, resolution, logo, epg_id, extra_info):
        self.name = name
        self.web = web
        self.resolution = resolution
        self.logo = logo
        self.epg_id = epg_id
        self.options = []
        self.extra_info = extra_info

    def add_option(self, format, url, info):
        self.options.append(self.Web(format, url, info))

    def get_name(self):
        return self.name

    def get_resolution(self):
        return self.get_resolution

    def get_logo(self):
        return self.logo

    def get_epg(self):
        return self.epg_id

    def get_options(self):
        return self.options

    def get_extra_info(self):
        return self.extra_info

    def __str__(self):
        options_string = ""
        for option in self.options:
            options_string += f"[Format: {option.get_format()}, URL: {option.get_url()}]"
        return self.name + " " + options_string

    def __options_to_json__(self):
        options_list = []
        for option in self.options:
            options_list.append(option.to_json())
        return options_list

    def to_json(self):
        return {
            "name": self.name,
            "web": self.web,
            "logo": self.logo,
            "resolution": self.resolution,
            "epg_id": self.epg_id,
            "options": self.__options_to_json__(),
            "extra_info": self.extra_info
        }

    def to_m3u8(self, ambit_name, option):
        info = '#EXTINF:-1'
        if self.epg_id != "":
            info += f' tvg-id="{self.epg_id}"'
        if self.logo != "":
            info += f' tvg-logo="{self.logo}"'
        if ambit_name != "":
            info += f' group-title="{ambit_name}"'

        info += f',{self.name}'
        info += f'\n{option.get_url()}\n'

        return info

    def to_enigma2(self, option, counter):
        info = f'#SERVICE 4097:0:1:{counter}:0:0:0:0:0:0'
        info += f':{option.get_url(double_dot=False)}'
        info += f':{self.name}\n'
        info += f'#DESCRIPTION {self.name}\n'

        return info

    class Web:
        def __init__(self, format, url, info):
            self.format = format
            self.url = url
            self.info = info

        def is_m3u8_valid(self):
            return self.format == "m3u8"

        def get_format(self):
            return self.format

        def get_url(self, double_dot=True):
            if double_dot:
                return self.url
            else:
                return self.url.replace(":", "%3a")

        def __str__(self):
            return self.format + ", " + self.url

        def to_json(self):
            return {
                "format": self.format,
                "url": self.url,
                "extra_info": self.info
            }
