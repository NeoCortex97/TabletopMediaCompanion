import sys

import rtmidi2


def run_query(inp, out):
    res = []

    def cb(msg, ts):
        if msg[0] == 240:
            res.append(msg)

    inp.callback = cb
    out.send_sysex(126, 127, 6, 1)
    while len(res) == 0:
        pass
    return res[0]


if __name__ == "__main__":
    print("This script prints family id and ProductID and FamilyID for every device that supports general midi.")
    print("You can copy an entire line into the markdown file in 'Manuals/identity.md'.")
    max_length = max([len(dev) for dev in rtmidi2.get_in_ports()])
    print(("{:" + str(max_length) + "} | FamilyID    | ProductID").format("Device"))
    print('-' * max_length + '-+-------------+------------')
    for index, device in enumerate(rtmidi2.get_in_ports()):
        inp = rtmidi2.MidiIn()
        inp.open_port(index)
        inp.ignore_types(False, False, False)
        out = rtmidi2.MidiOut()
        out.open_port(index)
        res = run_query(inp, out)
        # print(res)
        try:
            vals = ['`{:>02}`'.format(item) for item in res[8:12]]
            print(("{0:" + str(max_length) + "} | {1[0]:>5} {1[1]:>5} | {1[2]:>5} {1[3]:>5}").format(device, vals))
        except IndexError:
            print(("{:" + str(max_length) + "} | `???` `???` | `???` `???`").format(device))
