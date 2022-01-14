from tkinter import Canvas
from jpg.color.converter import ColorConverter
from jpg.functions import remove_ff00
from jpg.huffman.huffman import Huffman
from jpg.huffman.table import HuffmanTable
from jpg.matrix.matrix import Matrix
from jpg.stream.stream import Stream


class Scanner:
    """Skaner do tresci obrazu"""

    def __init__(self, w: Canvas, width: int, height: int, huffman_table: HuffmanTable, quant: dict, quant_mapping: list) -> None:
        self.w = w
        self.width = width
        self.height = height
        self.huffman_table = huffman_table
        self.quant = quant
        self.quant_mapping = quant_mapping

    # Skanowanie pliku
    def scan(self, data: bytes, data_length: int) -> int:
        data, length = remove_ff00(data[data_length:])

        stream = Stream(data)
        Y_coeff, Cl_coeff, Cr_coeff = 0, 0, 0

        matrix_builder = Matrix(self.huffman_table)

        for y in range(self.height // 8):
            for x in range(self.width // 8):
                matrixL, Y_coeff = matrix_builder.build(
                    stream, Y_coeff, self.quant_mapping[0], self.quant[self.quant_mapping[0]])

                matrixCl, Cl_coeff = matrix_builder.build(
                    stream, Cl_coeff, self.quant_mapping[1], self.quant[self.quant_mapping[1]])

                matrixCr, Cr_coeff = matrix_builder.build(
                    stream, Cr_coeff, self.quant_mapping[2], self.quant[self.quant_mapping[2]])

                self.draw(x, y, matrixL.transformed_matrix,
                          matrixCr.transformed_matrix, matrixCl.transformed_matrix)

        return length + data_length

    # Rysowanie obrazu na płó†nie
    def draw(self, x: int, y: int, matL: list, matCr:  list, matCl: list) -> None:
        for yy in range(8):
            for xx in range(8):
                c = "#%02x%02x%02x" % ColorConverter.toRGB(
                    matL[yy][xx], matCr[yy][xx], matCl[yy][xx]
                )
                x1, y1 = (x * 8 + xx) * 2, (y * 8 + yy) * 2
                x2, y2 = (x * 8 + (xx + 1)) * 2, (y * 8 + (yy + 1)) * 2
                self.w.create_rectangle(x1, y1, x2, y2, fill=c, outline=c)
