# -*- coding: utf-8 -*-
import time
from typing import List, Dict

import rtmidi2

from MidiCs.Field import RealTimeField, ChannelField, SysexIdField, ManufacturerField, FamilyIdField, ProductIdField, \
    SoftwareVersionField
from MidiCs.SysexMessage import SysexMessage

DEVICE_INQUIRY_REQUEST = [240, 126, 127, 6, 1, 247]
DEVICE_INQUIRY_RESPONSE = [240, 126, 'id', 6, 2, 'manufacturer', 'manufacturer*', 'manufacturer*', 'family', 'family', 'product', 'product', 'fw', 'fw', 'fw', 'fw', 247]

LAUNCHPAD_PRO_FID = [81, 0]
LAUNCHPAD_PRO_PID = [0, 0]
LAUNCHPAD_MK2_FID = [105, 0]

# Launchpad pro prog
#


def enum_ports() -> Dict[str, List[Dict[str, str or int]]]:
    inputs = rtmidi2.get_in_ports()
    outputs = rtmidi2.get_out_ports()
    result_both = [{'name': str(item[1]), 'out_port': int(item[0]), 'in_port': inputs.index(item[1])} for item in enumerate(outputs) if item[1] in inputs]
    result_input = [{'name': str(item[1]), 'in_port': int(item[0])} for item in enumerate(inputs) if item[1] not in outputs]
    result_output = [{'name': str(item[1]), 'out_port': int(item[0])} for item in enumerate(outputs) if item[1] not in inputs]
    return {'inputs': result_input, 'outputs': result_output, 'both': result_both}


def run_query(inp: rtmidi2.MidiIn, out: rtmidi2.MidiOut, query, trigger: int = 240, ignore: bool = True):
    queue = []

    def callback(message, timestamp):
        if message[0] == trigger:
            queue.append(message)
        else:
            print(message)

    cb = inp.callback
    inp.callback = callback
    inp.ignore_types(False)
    out.send_raw(*query)
    while len(queue) < 1:
        time.sleep(0.1)
    inp.callback = cb
    inp.ignore_types(ignore)
    return queue[0]


def decode_query_response(response, template) -> Dict[str, List[int] or int or str]:
    print(response, len(response))
    # print(template, len(template))
    raw_fields = [item for item in template if type(item) == str]
    fields = set([item.replace("*", '') for item in raw_fields])
    fields = {item: {'min': raw_fields.count(item), 'optional': raw_fields.count(item + '*')} for item in fields}
    print(fields)
    result = {}
    if len(response) != len(template):
        return {'error': "response and template are different lengths. Potential missmatch"}
    for index in range(len(response)):
        if (type(template[index]) is int) and (response[index] != template[index]):
            return {'error': "fixed value of template and matching response value are unequal. Missmatch!"}
        elif type(template[index]) is str:
            if template[index] in result.keys():
                if type(result[template[index]]) is not list:
                    result[template[index]] = [result[template[index]]]
                result[template[index]].append(response[index])
            else:
                result[template[index]] = response[index]
    return result


def main():
    template = [RealTimeField, ChannelField, SysexIdField, ManufacturerField, FamilyIdField, ProductIdField, SoftwareVersionField]
    ports = enum_ports()
    # print(ports)
    for port in ports['both']:
        print(port['name'])
        in_port = rtmidi2.MidiIn()
        in_port.open_port(port["in_port"])
        out_port = rtmidi2.MidiOut()
        out_port.open_port(port['out_port'])
        response = run_query(in_port, out_port, DEVICE_INQUIRY_REQUEST)
        try:
            print(SysexMessage(template, response).contents)
        except IndexError:
            print("Unable to parse response.")
        out_port.close_port()
        in_port.close_port()


if __name__ == "__main__":
    main()
