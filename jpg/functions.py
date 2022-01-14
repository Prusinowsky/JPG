from struct import unpack

# Funkcja do odkodowywania tablicy bitowej


def get_array(type: str, l: list, length: int) -> list:
    return unpack(type * length, l[:length])

# Usuwa 0x00 po 0xff z ciagu danych obrazu


def remove_ff00(data: bytes) -> tuple:
    output = []
    i = 0

    while True:
        b, bnext = unpack("BB", data[i: i + 2])
        if b == 0xFF:
            if bnext != 0:
                break
            output.append(data[i])
            i += 2
        else:
            output.append(data[i])
            i += 1

    return output, i
