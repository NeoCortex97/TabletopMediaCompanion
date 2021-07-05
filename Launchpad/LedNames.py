from typing import Tuple


LAUNCHPAD_LED_NOTES_TOP = {
    'UP': 104,
    'DOWN': 105,
    'LEFT': 106,
    'RIGHT': 107,
    'SESSION': 108,
    'USER1': 109,
    'USER2': 110,
    'MIXER': 111
}


LAUNCHPAD_LED_NAMES_TOP = {value: key for key, value in LAUNCHPAD_LED_NOTES_TOP.items()}


LAUNCHPAD_LED_NOTES_SESSION = {
    'VOLUME': 89,
    'PAN': 79,
    'SEND_A': 69,
    'SEND_B': 59,
    'STOP': 49,
    'MUTE': 39,
    'SOLO': 29,
    'RECORD_ARM': 19
}


LAUNCHPAD_LED_NAMES_SESSION = {value: key for key, value in LAUNCHPAD_LED_NOTES_SESSION.items()}


LAUNCHPAD_LED_NOTES_DRUM = {
    'VOLUME': 100,
    'PAN': 101,
    'SEND_A': 102,
    'SEND_B': 103,
    'STOP': 104,
    'MUTE': 105,
    'SOLO': 106,
    'RECORD_ARM': 107
}


LAUNCHPAD_LED_NAMES_DRUM = {value: key for key, value in LAUNCHPAD_LED_NOTES_DRUM.items()}


def launchpad_button_to_note_session(btn: Tuple[int, int] or str) -> int:
    if type(btn) == str:
        if btn in LAUNCHPAD_LED_NOTES_SESSION:
            return LAUNCHPAD_LED_NOTES_SESSION[btn]
        elif btn in LAUNCHPAD_LED_NOTES_TOP:
            return LAUNCHPAD_LED_NOTES_TOP[btn]
    elif type(btn) in [tuple, list]:
        return (btn[1] + 1) * 10 + (btn[0] + 1)


def launchpad_note_to_button_session(note: int) -> str or Tuple[int, int]:
    if note in LAUNCHPAD_LED_NAMES_TOP:
        return LAUNCHPAD_LED_NAMES_TOP[note]
    elif note in LAUNCHPAD_LED_NAMES_SESSION:
        return LAUNCHPAD_LED_NAMES_SESSION[note]
    else:
        return (note % 10) - 1, (note // 10) - 1


def launchpad_button_to_note_drum(btn: Tuple[int, int] or str) -> int:
    if type(btn) == str:
        if btn in LAUNCHPAD_LED_NOTES_TOP:
            return LAUNCHPAD_LED_NOTES_TOP[btn]
        elif btn in LAUNCHPAD_LED_NOTES_DRUM:
            return LAUNCHPAD_LED_NOTES_DRUM[btn]
    elif type(btn) in [tuple, list]:
        base = 36
        if btn[0] > 3:
            base += 32
        offset = btn[0] % 4
        height = btn[1] * 4
        return base + height + offset


def launchpad_note_to_button_drum(note: int) -> Tuple[int, int]:
    if note in LAUNCHPAD_LED_NAMES_TOP:
        return LAUNCHPAD_LED_NAMES_TOP[note]
    elif note in LAUNCHPAD_LED_NAMES_DRUM:
        return LAUNCHPAD_LED_NAMES_DRUM[note]
    else:
        return note % 4 if note - 68 < 0 else (note % 4) + 4, note // 4 - (9 if note - 68 < 0 else 17)
