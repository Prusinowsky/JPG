# Techniki Realizacji Algorytmów Cyfrowego Przetwarzania Sygnałów
## Projekt
```

Tytuł:                  JPG - Dekompresja
Autor:                  Patryk Prusinowski
Język programowania:    Python 3

```

## Cel projektu

Celem projektu jest realizacja algorytmu dekompresji JPG. 

## Algorytm

1. Otworzenie pliku w formie odczytywania bitowego
```python
img = JPG("images/profile.jpeg")
img.decode(w)
```
2. Rozpoczęcie dekodowania obrazu oraz wyszukiwanie marketów pliku JPG
```python
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
    self.height, self.width, self.quant_mapping = Frame.decode(
        chunk)

# Skanowanie obrazu
if marker == 0xffda:
    scanner = Scanner(w, self.width, self.height, self.huffman_table,
                        self.quant, self.quant_mapping)
    chunk_length = scanner.scan(data, chunk_length)
```

3. Odczytywania tabeli kwantyzacji z obrazu
4. Odczytywanie drzewa Huffmana 
    - odczytywanie nagłówka (klasy) tabeli Huffmana

        ```python
        header, = unpack("B", data[offset: offset + 1])
        ```
    - odczytanie tablicy długości bitów dla kazdej wartosci

        ```python
        lengths = get_array("B", data[offset: offset + 16], 16)
        ```

    - odczytanie wartości zakodowanych w drzewie Huffmana

        ```python
        elements = []
        for i in lengths:
            elements += get_array("B", data[offset: offset + i], i)
            offset += i
        ```
    - utworzenie obiektu tablicy Huffmana

5. Odczytywanie ramki, czyli informacji o obrazie
6. Odczytywanie treści obrazu
    - odczytywanie wektorów danych dla 3-ch kanałów YIG

        ```python
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
        ```

    - konwersja wektorów danych na macierze 8x8

        ```python
        self.original_matrix = copy.deepcopy(self.zigzag_path_matrix)
        for x in range(self.precision):
            for y in range(self.precision):
                self.original_matrix[x][y] = self.vector[self.original_matrix[x][y]]

        return self.original_matrix
        ```

    - konwersja macierzy 8x8 za pomocą odwrotnej dyskretnej transformaty cosinusowej


        ```python
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
        ```

    - konwersja palety barwnej z YIG do RGB

        ```python
        R = Cr * (2 - 2 * 0.299) + Y
        B = Cb * (2 - 2 * 0.114) + Y
        G = (Y - 0.114 * B - 0.299 * R) / 0.587

        return (
            int(ColorConverter.clamp(R + 128)),
            int(ColorConverter.clamp(G + 128)),
            int(ColorConverter.clamp(B + 128))
        )
        ```
    
    - wyświetlenie obrazu



## Zródła

http://www.zsk.ict.pwr.wroc.pl/zsk/repository/dydaktyka/ioc/in_obr_wyk_2.pdf
https://d33wubrfki0l68.cloudfront.net/bdc1363abbd5744200ec5283d4154e55143df86c/8c624/images/decoding_jpeg/jpegrgb_dissected.png