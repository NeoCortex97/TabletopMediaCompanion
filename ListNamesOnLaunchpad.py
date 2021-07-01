import time
import rtmidi2


def main():
    idx = None
    for index, name in enumerate(rtmidi2.get_in_ports()):
        if name.startswith("Launchpad"):
            idx = index

    inp = rtmidi2.MidiIn()
    out = rtmidi2.MidiOut()
    inp.open_port(idx)
    inp.ignore_types(False, False, False)
    out.open_port(idx)
    out.send_raw(240, 0, 32, 41, 2, 24, 14, 0, 247)
    characters = []
    text = None
    while text != '':
        text = input("> ")
        characters.extend(text.split())
    queue = []

    def cb(message, timestamp):
        if message[0] == 240:
            queue.append(message)
        else:
            print(message)

    inp.callback = cb
    speed = 4
    colors = [1, 7, 11, 15, 19, 27, 31, 35, 39, 43, 47, 51, 55, 59]
    for index, character in enumerate(characters):
        print(character)
        out.send_raw(240, 0, 32, 41, 2, 24, 20, colors[index % len(colors)], 0, speed, *[ord(char) for char in character], 247)
        while len(queue) < 1:
            time.sleep(0.2)
        queue.clear()


if __name__ == "__main__":
    main()
