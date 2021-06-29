# -*- coding: utf- -*-
from typing import List, Dict, Any
from MidiCs.Field import Field


class SysexMessage:
    def __init__(self, template: List[Field], data: List[int] = None):
        self.prefix = 240
        self.postfix = 247
        self.template = template
        self.contents: Dict[str, Any] = dict()
        if data:
            self.decode(data)

    def decode(self, data: List[int]) -> Dict[str, Any]:
        if data[0] == self.prefix and data[-1] == self.postfix:
            data = data[1:-1]
            fields = []
            for field in self.template:
                fields.append(field())
                data = fields[-1].parse(data)
            result = {}
            for field in fields:
                result = field.dump(result)
            self.contents = result
            return result
        elif data[0] != self.prefix:
            raise ValueError("Malformed sysex command. Message has to start with 240 but starts with {}".format(data[0]))
        else:
            raise ValueError("Malformed sysex command. Message has to end with 247 but ends with {}".format(data[-1]))
