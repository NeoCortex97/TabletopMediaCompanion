from typing import List, Tuple

from Launchpad.LayoutNames import LAYOUT_IDS
from Launchpad.LedNames import launchpad_note_to_button_session, launchpad_note_to_button_drum, \
    launchpad_button_to_note_session, launchpad_button_to_note_drum
from Launchpad.palette import LAUNCHPAD_PALETTE_COLOR, LAUNCHPAD_PALETTE_INDEX
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
    def __init__(self, **kwargs):
        super(FunctionField, self).__init__(**kwargs)

    def parse(self, message: List[int]) -> List[int]:
        self.content = FUNCTION_NAMES[message[0]]
        return message[1:]

    def encode(self) -> List[int]:
        if type(self.content) == str:
            return FUNCTION_IDS[self.content]
        elif type(self.content) == int:
            return [self.content]


class LayoutField(Field):
    def __init__(self, **kwargs):
        super(LayoutField, self).__init__(**kwargs)

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
    def __init__(self, **kwargs):
        super(TextField, self).__init__(**kwargs)
        self.delimiter = kwargs.get("delimiter", 247)

    def parse(self, message: List[int]) -> List[int]:
        index = message.index(self.delimiter)
        self.content = ''.join([chr(item) for item in message[:index]])
        return message[index:]

    def encode(self) -> List[int]:
        if type(self.content) == str:
            return [ord(char) for char in self.content]
        elif type(self.content) == List[int]:
            return self.content


class PaletteField(Field):
    def __init__(self, **kwargs):
        super(PaletteField, self).__init__(**kwargs)

    def parse(self, message: List[int]) -> List[int]:
        self.content = LAUNCHPAD_PALETTE_COLOR[message[0]]
        return message[1:]

    def encode(self) -> List[int]:
        if type(self.content) == str:
            return LAUNCHPAD_PALETTE_INDEX[self.content]
        elif type(self.content) == int:
            return [self.content]


class LedField(Field):
    def __init__(self, **kwargs):
        self.layout = 'SESSION'
        super(LedField, self).__init__(**kwargs)

    def parse(self, message: List[int]) -> List[int]:
        if self.layout in ['SESSION', 'USER2']:
            self.content = launchpad_note_to_button_session(message[0])
        elif self.layout in ['USER1']:
            self.content = launchpad_note_to_button_drum(message[0])
        return message[1:]

    def encode(self) -> List[int]:
        if type(self.content) == str or Tuple[int, int]:
            if self.layout in ['SESSION', 'USER2']:
                return [launchpad_button_to_note_session(self.content)]
            elif self.layout in ['USER1']:
                return [launchpad_button_to_note_drum(self.content)]
        elif type(self.content) == int:
            return [self.content]
