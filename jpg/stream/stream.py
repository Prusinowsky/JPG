class Stream:

    def __init__(self, data) -> None:
        self.data = data
        self.pos = 0

    # Zwraca kolejny biy bit
    def get_bit(self) -> int:
        # Wybiera bit
        byte = self.data[self.pos >> 3]
        # Wybiera bit
        shift = 7 - (self.pos & 0x7)
        self.pos += 1

        return (byte >> shift) & 1

    #  Zwrace n kolejnych bitów
    def get_bit_n(self, length: int) -> int:
        val = 0
        for _ in range(length):
            val = val * 2 + self.get_bit()

        return val

    # Zwraca dlugosc strumyka
    def len(self) -> int:
        return len(self.data)
