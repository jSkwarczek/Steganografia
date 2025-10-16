import string
from enum import StrEnum
from docx import Document

class SpaceChar(StrEnum):
    THIN = "\u2009"
    HAIR = "\u200A"
    ZERO_WIDTH = "\u200B"


CHAR_MAPPING = {
    "a": (SpaceChar.THIN, SpaceChar.THIN, SpaceChar.THIN),
    "b": (SpaceChar.THIN, SpaceChar.THIN, SpaceChar.HAIR),
    "c": (SpaceChar.THIN, SpaceChar.THIN, SpaceChar.ZERO_WIDTH),
    "d": (SpaceChar.THIN, SpaceChar.HAIR, SpaceChar.THIN),
    "e": (SpaceChar.THIN, SpaceChar.HAIR, SpaceChar.HAIR),
    "f": (SpaceChar.THIN, SpaceChar.HAIR, SpaceChar.ZERO_WIDTH),
    "g": (SpaceChar.THIN, SpaceChar.ZERO_WIDTH, SpaceChar.THIN),
    "h": (SpaceChar.THIN, SpaceChar.ZERO_WIDTH, SpaceChar.HAIR),
    "i": (SpaceChar.THIN, SpaceChar.ZERO_WIDTH, SpaceChar.ZERO_WIDTH),
    "j": (SpaceChar.HAIR, SpaceChar.THIN, SpaceChar.THIN),
    "k": (SpaceChar.HAIR, SpaceChar.THIN, SpaceChar.HAIR),
    "l": (SpaceChar.HAIR, SpaceChar.THIN, SpaceChar.ZERO_WIDTH),
    "m": (SpaceChar.HAIR, SpaceChar.HAIR, SpaceChar.THIN),
    "n": (SpaceChar.HAIR, SpaceChar.HAIR, SpaceChar.HAIR),
    "o": (SpaceChar.HAIR, SpaceChar.HAIR, SpaceChar.ZERO_WIDTH),
    "p": (SpaceChar.HAIR, SpaceChar.ZERO_WIDTH, SpaceChar.THIN),
    "q": (SpaceChar.HAIR, SpaceChar.ZERO_WIDTH, SpaceChar.HAIR),
    "r": (SpaceChar.HAIR, SpaceChar.ZERO_WIDTH, SpaceChar.ZERO_WIDTH),
    "s": (SpaceChar.ZERO_WIDTH, SpaceChar.THIN, SpaceChar.THIN),
    "t": (SpaceChar.ZERO_WIDTH, SpaceChar.THIN, SpaceChar.HAIR),
    "u": (SpaceChar.ZERO_WIDTH, SpaceChar.THIN, SpaceChar.ZERO_WIDTH),
    "v": (SpaceChar.ZERO_WIDTH, SpaceChar.HAIR, SpaceChar.THIN),
    "w": (SpaceChar.ZERO_WIDTH, SpaceChar.HAIR, SpaceChar.HAIR),
    "x": (SpaceChar.ZERO_WIDTH, SpaceChar.HAIR, SpaceChar.THIN),
    "y": (SpaceChar.ZERO_WIDTH, SpaceChar.ZERO_WIDTH, SpaceChar.THIN),
    "z": (SpaceChar.ZERO_WIDTH, SpaceChar.ZERO_WIDTH, SpaceChar.HAIR),
}

REVERSE_CHAR_MAPPING = {
    (SpaceChar.THIN, SpaceChar.THIN, SpaceChar.THIN): "a",
    (SpaceChar.THIN, SpaceChar.THIN, SpaceChar.HAIR): "b",
    (SpaceChar.THIN, SpaceChar.THIN, SpaceChar.ZERO_WIDTH): "c",
    (SpaceChar.THIN, SpaceChar.HAIR, SpaceChar.THIN): "d",
    (SpaceChar.THIN, SpaceChar.HAIR, SpaceChar.HAIR): "e",
    (SpaceChar.THIN, SpaceChar.HAIR, SpaceChar.ZERO_WIDTH): "f",
    (SpaceChar.THIN, SpaceChar.ZERO_WIDTH, SpaceChar.THIN): "g",
    (SpaceChar.THIN, SpaceChar.ZERO_WIDTH, SpaceChar.HAIR): "h",
    (SpaceChar.THIN, SpaceChar.ZERO_WIDTH, SpaceChar.ZERO_WIDTH): "i",
    (SpaceChar.HAIR, SpaceChar.THIN, SpaceChar.THIN): "j",
    (SpaceChar.HAIR, SpaceChar.THIN, SpaceChar.HAIR): "k",
    (SpaceChar.HAIR, SpaceChar.THIN, SpaceChar.ZERO_WIDTH): "l",
    (SpaceChar.HAIR, SpaceChar.HAIR, SpaceChar.THIN): "m",
    (SpaceChar.HAIR, SpaceChar.HAIR, SpaceChar.HAIR): "n",
    (SpaceChar.HAIR, SpaceChar.HAIR, SpaceChar.ZERO_WIDTH): "o",
    (SpaceChar.HAIR, SpaceChar.ZERO_WIDTH, SpaceChar.THIN): "p",
    (SpaceChar.HAIR, SpaceChar.ZERO_WIDTH, SpaceChar.HAIR): "q",
    (SpaceChar.HAIR, SpaceChar.ZERO_WIDTH, SpaceChar.ZERO_WIDTH): "r",
    (SpaceChar.ZERO_WIDTH, SpaceChar.THIN, SpaceChar.THIN): "s",
    (SpaceChar.ZERO_WIDTH, SpaceChar.THIN, SpaceChar.HAIR): "t",
    (SpaceChar.ZERO_WIDTH, SpaceChar.THIN, SpaceChar.ZERO_WIDTH): "u",
    (SpaceChar.ZERO_WIDTH, SpaceChar.HAIR, SpaceChar.THIN): "v",
    (SpaceChar.ZERO_WIDTH, SpaceChar.HAIR, SpaceChar.HAIR): "w",
    (SpaceChar.ZERO_WIDTH, SpaceChar.HAIR, SpaceChar.THIN): "x",
    (SpaceChar.ZERO_WIDTH, SpaceChar.ZERO_WIDTH, SpaceChar.THIN): "y",
    (SpaceChar.ZERO_WIDTH, SpaceChar.ZERO_WIDTH, SpaceChar.HAIR): "z",
}

BEGIN_SEQUENCE = (SpaceChar.ZERO_WIDTH, SpaceChar.ZERO_WIDTH, SpaceChar.ZERO_WIDTH)
BEGIN_SEQUENCE_STR = "".join(BEGIN_SEQUENCE)

END_SEQUENCE = (SpaceChar.ZERO_WIDTH, SpaceChar.ZERO_WIDTH, SpaceChar.ZERO_WIDTH)
END_SEQUENCE_STR = "".join(END_SEQUENCE)


def replace_space(text: str, space_idx: int, new_space: tuple[SpaceChar, ...]) -> str:
    new_space_str = "".join(new_space)
    pre = text[:space_idx]
    post = text[space_idx + 1:]
    return pre + new_space_str + post


def embed_message_us(text: str, secret: str) -> str:
    secret = secret.lower()
    if set(secret).issubset(set(string.ascii_lowercase)) is False:
        raise ValueError(
            "Only ASCII letters are allowed in the secret, "
            f"got invalid characters: {set(secret) - set(string.ascii_lowercase)}"
        )

    required_spaces_count = len(secret) + 2  # + 2, because we need begin/end sequence
    spaces_count = text.count(" ")
    
    if spaces_count < required_spaces_count:
        raise ValueError(f"Covertext is too short, need {required_spaces_count} spaces, got: {spaces_count}")

    space_idx = text.find(" ")
    text = replace_space(text, space_idx, BEGIN_SEQUENCE)

    start = space_idx + 1

    for char in secret:
        space_idx = text.find(" ", start)
        text = replace_space(text, space_idx, CHAR_MAPPING[char])

        start = space_idx + 1

    space_idx = text.find(" ", start)
    text = replace_space(text, space_idx, END_SEQUENCE)

    docx = Document()
    docx.add_paragraph(text)
    return docx


def extract_message_us(text: str) -> str:
    start = text.find(BEGIN_SEQUENCE_STR)

    if start == -1:
        raise ValueError("Begin sequence is missing in text")
    
    end = text.find(END_SEQUENCE_STR, start + 1)

    if end == -1:
        raise ValueError("End sequence is missing in text")

    text = text[start + 3:end]

    last = 0
    secret = ""
    while True:
        thin_idx = text.find(SpaceChar.THIN, last)
        hair_idx = text.find(SpaceChar.HAIR, last)
        zero_width_idx = text.find(SpaceChar.ZERO_WIDTH, last)

        if thin_idx == -1 and hair_idx == -1 and zero_width_idx == -1:
            break

        i = min(filter(lambda x: x != -1, [thin_idx, hair_idx, zero_width_idx]))

        key = tuple(SpaceChar(c) for c in (text[i], text[i+1], text[i+2]))
        secret += REVERSE_CHAR_MAPPING[key]
        last = i + 3

    return secret
