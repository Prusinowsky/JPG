import copy
import math
from jpg.huffman.table import HuffmanTable
from jpg.number.number import Number
from jpg.stream.stream import Stream
from jpg.transform.inverse_discrete_cosine_transform import InverseDiscreteCosineTransform


class Matrix:

    def __init__(self, huffman_table: HuffmanTable) -> None:
        self.huffman_table = huffman_table

    # Buduje macierz
    def build(self, stream: Stream, _dc_coeff: int, idx: int, quant: list) -> tuple:
        transform = InverseDiscreteCosineTransform()

        bits_length = self.huffman_table[0 + idx].get_code(stream)
        bits = stream.get_bit_n(bits_length)
        dc_coeff = _dc_coeff + Number.decode_u2(bits, bits_length)

        transform.vector[0] = dc_coeff * quant[0]

        i = 1
        while i < 64:
            bits_length = self.huffman_table[16 + idx].get_code(stream)
            if bits_length == 0:
                break

            # The first part of the AC quantization table
            # is the number of leading zeros
            if bits_length > 15:
                i += bits_length >> 4
                bits_length = bits_length & 0x0F

            bits = stream.get_bit_n(bits_length)

            if i < 64:
                coeff = Number.decode_u2(bits, bits_length)
                transform.vector[i] = coeff * quant[i]
                i += 1

        transform.zigzag()
        transform.transform()

        return transform, dc_coeff