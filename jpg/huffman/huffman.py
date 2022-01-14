from struct import unpack
from jpg.functions import get_array
from jpg.huffman.table import HuffmanTable


class Huffman:
    """Klasa słuzaca do dekodowania ciagu bitow Hoffmana"""

    # Dekodowanie ciągu bitów do słownika z drzewem Huffmana
    def decode(data: bytes) -> dict:
        offset = 0
        header, = unpack("B", data[offset: offset + 1])
        offset += 1

        lengths = get_array("B", data[offset: offset + 16], 16)
        offset += 16

        elements = []
        for i in lengths:
            elements += get_array("B", data[offset: offset + i], i)
            offset += i

        huffman_table = HuffmanTable()
        huffman_table.make(lengths, elements)

        data = data[offset:]

        return {header: huffman_table}
