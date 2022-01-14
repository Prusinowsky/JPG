class ColorConverter:
    """Klasa sluzaca do przetwarzania kolorow"""

    # Przycinanie wartosci poza zakresem
    def clamp(value: int) -> int:
        value = 255 if value > 255 else value
        value = 0 if value < 0 else value

        return value

    # Zamiana modelu barwnego YUM na RGB
    def toRGB(Y, Cr, Cb) -> tuple:
        R = Cr * (2 - 2 * 0.299) + Y
        B = Cb * (2 - 2 * 0.114) + Y
        G = (Y - 0.114 * B - 0.299 * R) / 0.587

        return (
            int(ColorConverter.clamp(R + 128)),
            int(ColorConverter.clamp(G + 128)),
            int(ColorConverter.clamp(B + 128))
        )
