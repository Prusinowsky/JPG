from jpg.stream.stream import Stream


class HuffmanTable:
    """Tabela Huffmana"""

    def __init__(self):
        self.root = []
        self.elements = []

    # Wstawia element na odpowiedni poziom.
    def insert(self, root: list, element: int, pos: int) -> bool:
        if not isinstance(root, list):
            return False

        if pos == 0:
            if len(root) < 2:
                root.append(element)
                return True
            return False

        for leaf in [0, 1]:
            if len(root) == leaf:
                root.append([])

            if self.insert(root[leaf], element, pos - 1):
                return True

    # Tworzy drzewo Huffmana na podstawie podanych dlugosci i dostarczonych elementow
    # np. lengths = [0, 4], elements = [1, 2, 3, 4] -> [[1, 2], [[3, 4]]
    def make(self, lengths, elements):
        self.elements = elements
        ix = 0
        for pos in range(len(lengths)):
            for _ in range(lengths[pos]):
                element = elements[ix]
                self.insert(self.root, element, pos)
                ix += 1

    # Znajduje wartość dla strumienia wejsciwego
    def find(self, stream: Stream) -> int:
        node = self.root
        while isinstance(node, list):
            node = node[stream.get_bit()]

        return node

    # Zwraca kod z drzewa Huffmana dla danego strumienia
    def get_code(self, stream: Stream) -> int:
        while True:
            code = self.find(stream)
            if code != -1:
                return code

    def __str__(self) -> str:
        return f'{self.root}'
