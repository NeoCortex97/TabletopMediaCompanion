from typing import List, Dict, Any, Tuple
from MidiCs.ManufacturerName import MANUFACTURER_NAME
from MidiCs.ManufacturerId import MANUFACTURER_ID
from MidiCs.SysexConstants import SYSEX_NAMES, SYSEX_IDS


class Field:
    def __init__(self, **kwargs):
        self.content = 0
        self.name = self.__class__.__name__[:-5]
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def parse(self, message: List[int]) -> List[int]:
        self.content = message[0]
        return message[1:]

    def dump(self, result: Dict[str, Any]) -> Dict[str, Any]:
        result[self.name] = self.content
        return result

    def encode(self) -> List[int]:
        return [self.content]


class TwoByteField(Field):
    def __init__(self, **kwargs):
        super(TwoByteField, self).__init__(**kwargs)

    def parse(self, message: List[int]) -> List[int]:
        self.content = message[:2]
        return message[2:]


class FourByteField(Field):
    def __init__(self, **kwargs):
        super(FourByteField, self).__init__(**kwargs)

    def parse(self, message: List[int]) -> List[int]:
        self.content = message[:4]
        return message[4:]


class RealTimeField(Field):
    def __init__(self, **kwargs):
        super(RealTimeField, self).__init__(**kwargs)

    def dump(self, result: Dict[str, Any]) -> Dict[str, Any]:
        if self.content == 127:
            result[self.name] = True
        elif self.content == 126:
            result[self.name] = False
        else:
            raise ValueError("Invalid realtime command input! {} is not a valid value!".format(self.content))
        return result

    def encode(self) -> List[int]:
        if type(self.content) == bool:
            return [126 + int(self.content)]
        elif type(self.content) == int:
            return [self.content]


class SysexChannelField(Field):
    def __init__(self, **kwargs):
        super(SysexChannelField, self).__init__(**kwargs)

    def dump(self, result: Dict[str, Any]) -> Dict[str, Any]:
        if self.content == 127:
            result[self.name] = '*'
        else:
            result[self.name] = self.content
        return result

    def encode(self) -> List[int]:
        if type(self.content) == str:
            return [127]
        elif type(self.content) == int:
            return [self.content]


class SysexIdField(TwoByteField):
    def __init__(self, **kwargs):
        super(SysexIdField, self).__init__(**kwargs)
        self.command_names = kwargs.get("options", SYSEX_NAMES)

    def dump(self, result: Dict[str, Any]) -> Dict[str, Any]:
        if tuple(self.content) in self.command_names:
            result[self.name] = self.command_names[tuple(self.content)]
        else:
            result[self.name] = 'UNKNOWN'
        return result

    def encode(self) -> List[int]:
        if type(self.content) == str:
            return SYSEX_IDS[self.content]
        elif type(self.content) == List[int]:
            return self.content


class ManufacturerField(Field):
    def __init__(self, **kwargs):
        super(ManufacturerField, self).__init__(**kwargs)

    def parse(self, message: List[int]) -> List[int]:
        if message[0] == 0:
            self.content = message[:3]
            return message[3:]
        else:
            self.content = [message[0]]
            return message[1:]

    def dump(self, result: Dict[str, Any]) -> Dict[str, Any]:
        result[self.name] = MANUFACTURER_NAME[tuple(self.content)]
        return result

    def encode(self) -> List[int]:
        if type(self.content) == str:
            return list(MANUFACTURER_ID[self.content])
        elif type(self.content) == Tuple[int]:
            return list(self.content)


class FamilyIdField(TwoByteField):
    def __init__(self, **kwargs):
        super(FamilyIdField, self).__init__(**kwargs)


class ProductIdField(TwoByteField):
    def __init__(self, **kwargs):
        super(ProductIdField, self).__init__(**kwargs)


class SoftwareVersionField(FourByteField):
    def __init__(self, **kwargs):
        super(SoftwareVersionField, self).__init__(**kwargs)

    def dump(self, result: Dict[str, Any]) -> Dict[str, Any]:
        if 0 in self.content:
            self.content.remove(0)
        result[self.name] = "".join([str(item) for item in self.content])
        return result


if __name__ == "__main__":
    data = [240, 126, 0, 6, 2, 0, 32, 41, 105, 0, 0, 0, 0, 1, 6, 2, 247]
    print(data)
    data = data[1:-1]
    template = [RealTimeField, SysexChannelField, SysexIdField, ManufacturerField, FamilyIdField, ProductIdField, SoftwareVersionField]
    result = []
    for field in template:
        tmp = field()
        data = tmp.parse(data)
        result.append(tmp)
    # print(data)
    fields = {}
    for i in result:
        fields = i.dump(fields)
    print(fields)
