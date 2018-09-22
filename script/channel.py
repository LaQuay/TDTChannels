class Channel:
    name = None
    options = []

    def __init__(self, name):
        self.name = name
        self.options = []

    def add_option(self, format, url):
        self.options.append(self.Web(format, url))

    def get_name(self):
        return self.name

    def get_options(self):
        return self.options

    def __str__(self):
        options_string = ""
        for option in self.options:
            options_string += "[Format: " + option.get_format() + ", URL: " + option.get_url() + "]"
        return (self.name + " " + options_string)

    def __options_to_json__(self):
        options_list = []
        for option in self.options:
            options_list.append(option.to_json())
        return options_list

    def to_json(self):
        return {
            "name": self.name,
            "options": self.__options_to_json__()
        }

    class Web:
        format = None
        url = None

        def __init__(self, format, url):
            self.format = format
            self.url = url

        def is_m3u8_valid(self):
            return self.format == "m3u8"

        def get_format(self):
            return self.format

        def get_url(self):
            return self.url

        def __str__(self):
            return (self.format + ", " + self.url)

        def to_json(self):
            return {
                "format": self.format,
                "url": self.url
            }
