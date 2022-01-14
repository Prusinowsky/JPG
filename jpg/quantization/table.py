from jpg.functions import *
from struct import unpack


class QuantizationTable:
    """Algorytm odkodowywania informacji z Tablicy kwantyzacji"""

    def decode(data: bytes) -> dict:
        hdr, = unpack("B", data[0:1])
        quants = get_array("B", data[1: 65], 64)

        return {hdr: quants}
