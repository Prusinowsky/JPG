class Number:

    # Dekoduje zapis bitowy z formatu U2 na liczbę
    # https://pl.wikipedia.org/wiki/Kod_uzupe%C5%82nie%C5%84_do_dw%C3%B3ch
    def decode_u2(bits: int, length: int) -> int:
        half = 2 ** (length - 1)

        if bits >= half:
            return bits

        return bits - (2 * half - 1)
