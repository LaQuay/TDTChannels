class Country:
    name = None
    ambits = []

    def __init__(self, name):
        self.name = name
        self.ambits = []

    def add_ambit(self, ambit):
        self.ambits.append(ambit)

    # TODO Habria que filtrar los que no tienen campos de url
    def __ambits_to_json__(self):
        ambits_list = []
        for ambit in self.ambits:
            ambits_list.append(ambit.to_json())
        return ambits_list

    def to_json(self):
        return {
            "name": self.name,
            "ambits": self.__ambits_to_json__()
        }

    def __ambits_to_m3u8__(self):
        ambits_list = ""
        for ambit in self.ambits:
            ambits_list += ambit.to_m3u8()
        return ambits_list

    def to_m3u8(self):
        return self.__ambits_to_m3u8__()
