from struct import unpack
from tkinter import Canvas

from jpg.frame.frame import Frame
from jpg.huffman.huffman import Huffman
from jpg.quantization.table import QuantizationTable
from jpg.scanner.scanner import Scanner

marker_mapping = {
    0xffd8: "Start of Image",
    0xffe0: "Application Default Header",
    0xffdb: "Quantization Table",
    0xffc0: "Start of Frame",
    0xffc4: "Define Huffman Table",
    0xffda: "Start of Scan",
    0xffd9: "End of Image"
}


class JPG:
    """Klasa słuzaca do kodowania i dekodowania obrazów JPG"""

    def __init__(self, image_file: str) -> None:
        self.height = 0
        self.height = 0
        self.huffman_table = {}
        self.quant = {}
        self.quant_mapping = []

        with open(image_file, "rb") as file:
            self.img_data = file.read()

    def decode(self, w: Canvas) -> None:
        data = self.img_data
        while True:
            marker, = unpack(">H", data[0:2])
            print(marker_mapping.get(marker))

            # Początek obrazu JPG
            if marker == 0xffd8:
                data = data[2:]
                continue

            # Koniec obrazu JPG
            if marker == 0xffd9:
                return

            # Odczytywanie długości paczki i przygotowywanie paczki danych
            chunk_length, = unpack(">H", data[2:4])
            chunk_length += 2
            chunk = data[4:chunk_length]

            # Odczytywanie tabel kwantyzacji
            if marker == 0xffdb:
                self.quant.update(QuantizationTable.decode(chunk))

            # Odczytywanie drzew Huffmana
            if marker == 0xffc4:
                self.huffman_table.update(Huffman.decode(chunk))

            # Dekodowanie ramki
            if marker == 0xffc0:
                self.height, self.width, self.quant_mapping = Frame.decode(chunk)

            # Skanowanie obrazu
            if marker == 0xffda:
                scanner = Scanner(w, self.width, self.height, self.huffman_table,
                                  self.quant, self.quant_mapping)
                chunk_length = scanner.scan(data, chunk_length)

            data = data[chunk_length:]

            if len(data) == 0:
                return
