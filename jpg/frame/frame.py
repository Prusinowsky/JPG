from struct import unpack


class Frame:
    """Obsługa ramki"""

    def decode(data: bytes) -> list:
        quant_mapping = []

        presicion, height, width, components = unpack(">BHHB", data[0:6])
        print("Size %dx%d" % (width, height))

        for ix in range(components):
            component_id, sampling_factor, quantization_map_number = unpack(
                "BBB", data[6 + ix * 3: 9 + ix * 3])
            quant_mapping.append(quantization_map_number)

        return height, width, quant_mapping
