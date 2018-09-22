class Ambito:
    name = None
    channels = []

    def __init__(self, name, channels):
        self.name = name
        self.channels = channels

    def __channels_to_json__(self):
        channel_list = []
        for channel in self.channels:
            channel_list.append(channel.to_json())
        return channel_list

    def to_json(self):
        return {
            "name": self.name,
            "channels": self.__channels_to_json__()
        }

    def __channels_to_m3u8__(self):
        channels_list = ""
        for channel in self.channels:
            for option in channel.get_options():
                if option.is_m3u8_valid():
                    channels_list += "#EXTINF:-1, " + channel.get_name() + "\n" + option.get_url() + "\n"
        return channels_list

    def to_m3u8(self):
        return self.__channels_to_m3u8__()

    def __str__(self):
        return self.name
