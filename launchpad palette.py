import time

import rtmidi2

out = rtmidi2.MidiOut()
out.open_port(1)

for i in range(8):
    for j in range(9):
        out.send_noteon(0, (i + 1) * 10 + j, (i) * 8 + j)
        time.sleep(0.1)

input("pause")

for i in range(8):
    for j in range(9):
        out.send_noteon(0, (i + 1) * 10 + j, (i+1) * 8 + j + 64)
        time.sleep(0.1)