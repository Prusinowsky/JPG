import copy
import math


class InverseDiscreteCosineTransform:
    """Odwrotna dyskretna transformata cosinusowa"""

    def __init__(self) -> None:
        self.vector = [0] * 64
        self.original_matrix = []
        self.transformed_matrix = []
        self.precision = 8
        self.zigzag_path_matrix = [
            [0, 1, 5, 6, 14, 15, 27, 28],
            [2, 4, 7, 13, 16, 26, 29, 42],
            [3, 8, 12, 17, 25, 30, 41, 43],
            [9, 11, 18, 24, 31, 40, 44, 53],
            [10, 19, 23, 32, 39, 45, 52, 54],
            [20, 22, 33, 38, 46, 51, 55, 60],
            [21, 34, 37, 47, 50, 56, 59, 61],
            [35, 36, 48, 49, 57, 58, 62, 63],
        ]
        self.table = [
            [
                (self.norm_coeff(u) * math.cos(((2.0 * x + 1.0) * u * math.pi) / 16.0))
                for x in range(self.precision)
            ]
            for u in range(self.precision)
        ]

    # Normalizacja współczynnika
    def norm_coeff(self, n: int) -> float:
        if n == 0:
            return 1.0 / math.sqrt(2.0)
        else:
            return 1.0

    # Przeksztalcanie wektora na macierz
    def zigzag(self) -> list:
        self.original_matrix = copy.deepcopy(self.zigzag_path_matrix)
        for x in range(self.precision):
            for y in range(self.precision):
                self.original_matrix[x][y] = self.vector[self.original_matrix[x][y]]

        return self.original_matrix

    # Odwrotna transformacja DFT
    def transform(self) -> list:
        self.transformed_matrix = [list(range(8)) for _ in range(8)]

        for x in range(8):
            for y in range(8):
                local_sum = 0
                for u in range(self.precision):
                    for v in range(self.precision):
                        local_sum += (
                            self.original_matrix[v][u]
                            * self.table[u][x]
                            * self.table[v][y]
                        )
                self.transformed_matrix[y][x] = local_sum // 4

        return self.transformed_matrix
