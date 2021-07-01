from typing import List

from Launchpad.LayoutNames import LAYOUT_IDS, LAYOUT_NAMES
from MidiCs.Field import TwoByteField, Field
from Launchpad.FunctionNames import FUNCTION_NAMES, FUNCTION_IDS


class MagicField(TwoByteField):
    def __init__(self, name: str = None):
        super(MagicField, self).__init__(name=name)

    def parse(self, message: List[int]) -> List[int]:
        if message[0:2] is [2, 24]:
            return message[2:]
        elif message[0] != 2:
            raise ValueError("The first magic Byte has to be 2, but was {}".format(message[0]))
        else:
            raise ValueError("The second magic byte has to be 24, but was {}".format(message[1]))

    def encode(self) -> List[int]:
        return [2, 24]


class FunctionField(Field):
    def __init__(self, name: str = None):
        super(FunctionField, self).__init__(name=name)

    def parse(self, message: List[int]) -> List[int]:
        self.content = FUNCTION_NAMES[message[0]]
        return message[1:]

    def encode(self) -> List[int]:
        if type(self.content) == str:
            return FUNCTION_IDS[self.content]
        elif type(self.content) == int:
            return [self.content]


class LayoutField(Field):
    def __init__(self, name: str = None):
        super(LayoutField, self).__init__(name=name)

    def parse(self, message: List[int]) -> List[int]:
        if message[0] not in LAYOUT_IDS.values():
            raise ValueError("Layout byte has to be between 0 and 5, but was {}".format(message[0]))
        else:
            self.content = message[0]
            return message[1:]

    def encode(self) -> List[int]:
        if type(self.content) == str:
            return [LAYOUT_IDS[self.content]]
        else:
            return [self.content]


class TextField(Field):
    def __init__(self, name: str = None, delimiter=247):
        self.delimiter = delimiter
        super(TextField, self).__init__(name=name)

    def parse(self, message: List[int]) -> List[int]:
        index = message.index(self.delimiter)
        self.content = ''.join([chr(item) for item in message[:index]])
        return message[index:]

    def encode(self) -> List[int]:
        if type(self.content) == str:
            return [ord(char) for char in self.content]
        elif type(self.content) == List[int]:
            return self.content


