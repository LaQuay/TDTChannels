class Ambito:
    def __init__(self, name, channels):
        self.name = name
        self.channels = channels

    def add_channels(self, channels_to_add):
        if self.channels:
            self.channels += channels_to_add

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
                    channels_list += channel.to_m3u8(self.name, option)
        return channels_list

    def to_m3u8(self):
        return self.__channels_to_m3u8__()

    def __channels_to_enigma2__(self):
        channels_list = ""
        counter = 3
        for channel in self.channels:
            for option in channel.get_options():
                if option.is_m3u8_valid():
                    channels_list += channel.to_enigma2(option, counter)
                    counter += 2
        return channels_list

    def to_enigma2(self):
        return self.__channels_to_enigma2__()

    def __str__(self):
        return self.name
