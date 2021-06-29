from typing import List, Dict, Any
import MidiCs.ManufacturerName
from MidiCs.SysexConstants import SYSEX_NAMES


class Field:
    def __init__(self, name: str = None):
        self.content = 0
        if name is None:
            self.name = self.__class__.__name__[:-5]
        else:
            self.name = name

    def parse(self, message: List[int]) -> List[int]:
        self.content = message[0]
        return message[1:]

    def dump(self, result: Dict[str, Any]) -> Dict[str, Any]:
        result[self.name] = self.content
        return result


class TwoByteField(Field):
    def __init__(self, name: str = None):
        super(TwoByteField, self).__init__(name=name)

    def parse(self, message: List[int]) -> List[int]:
        self.content = message[:2]
        return message[2:]


class FourByteField(Field):
    def __init__(self, name: str = None):
        super(FourByteField, self).__init__(name=name)

    def parse(self, message: List[int]) -> List[int]:
        self.content = message[:4]
        return message[4:]


class RealTimeField(Field):
    def __init__(self, name: str = None):
        super(RealTimeField, self).__init__(name=name)

    def dump(self, result: Dict[str, Any]) -> Dict[str, Any]:
        if self.content == 127:
            result[self.name] = True
        elif self.content == 126:
            result[self.name] = False
        else:
            raise ValueError("Invalid realtime command input! {} is not a valid value!".format(self.content))
        return result


class ChannelField(Field):
    def __init__(self, name: str = None):
        super(ChannelField, self).__init__(name=name)

    def dump(self, result: Dict[str, Any]) -> Dict[str, Any]:
        if self.content == 127:
            result[self.name] = '*'
        else:
            result[self.name] = self.content
        return result


class SysexIdField(TwoByteField):
    def __init__(self, name: str = None, options=SYSEX_NAMES):
        super(SysexIdField, self).__init__(name=name)
        self.command_names = options

    def dump(self, result: Dict[str, Any]) -> Dict[str, Any]:
        if tuple(self.content) in self.command_names:
            result[self.name] = self.command_names[tuple(self.content)]
        else:
            result[self.name] = 'UNKNOWN'
        return result



class ManufacturerField(Field):
    def __init__(self, name: str = None):
        super(ManufacturerField, self).__init__(name=name)

    def parse(self, message: List[int]) -> List[int]:
        if message[0] == 0:
            self.content = message[:3]
            return message[3:]
        else:
            self.content = [message[0]]
            return message[1:]

    def dump(self, result: Dict[str, Any]) -> Dict[str, Any]:
        result[self.name] = MidiCs.ManufacturerName.MANUFACTURER_NAME[tuple(self.content)]
        return result


class FamilyIdField(TwoByteField):
    def __init__(self, name: str = None):
        super(FamilyIdField, self).__init__(name=name)


class ProductIdField(TwoByteField):
    def __init__(self, name: str = None):
        super(ProductIdField, self).__init__(name=name)


class SoftwareVersionField(FourByteField):
    def __init__(self, name: str = None):
        super(SoftwareVersionField, self).__init__(name=name)

    def dump(self, result: Dict[str, Any]) -> Dict[str, Any]:
        if 0 in self.content:
            self.content.remove(0)
        result[self.name] = "".join([str(item) for item in self.content])
        return result


if __name__ == "__main__":
    data = [240, 126, 0, 6, 2, 0, 32, 41, 105, 0, 0, 0, 0, 1, 6, 2, 247]
    print(data)
    data = data[1:-1]
    template = [RealTimeField, ChannelField, SysexIdField, ManufacturerField, FamilyIdField, ProductIdField, SoftwareVersionField]
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
