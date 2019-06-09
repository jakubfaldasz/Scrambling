from operator import xor, not_
from random import choices

from PIL import Image

from scramblers.scrambler_base import Scrambler_BaseClass


class Transmitter:

    def __init__(self, scrambler: Scrambler_BaseClass, noise: float, frame_size: int, sync_size: int, is_synchronous: bool):
        self.scrambler = scrambler
        self.noise = noise
        self.output_data = []
        self.scr_bits_counter = 0
        self.frame_size = frame_size
        self.is_synchronous = is_synchronous
        self.pixels_in_frame = int(self.frame_size/8)
        self.sync_word = int(sync_size/2) * [1,0]

    def generate_output(self, image_name):
        img = Image.open(image_name)

        pix_val = list(img.getdata())
        processed_bits = []

        while len(pix_val) > 0 :

            scrambled_pixels = self.scrambler.generate_scrambled_pixels(pix_val[0: self.pixels_in_frame])
            del pix_val[0: self.pixels_in_frame]

            if self.is_synchronous:
                self.scrambler.seq_state = self.scrambler.input_seq[:]

            self.output_data.extend(self.sync_word)

            for pixel in scrambled_pixels:
                bits = self.scrambler.convert_to_str(pixel)
                bits = list(map(int, bits))
                processed_bits.extend(bits)

            crc = self.calculate_CRC(processed_bits)
            self.output_data.extend(processed_bits)
            self.output_data.extend(crc)
            processed_bits = []

        for g in range(0, len(self.output_data)):
            self.output_data[g] = self.noise_generator(self.output_data[g])

        return self.output_data

    def calculate_CRC(self, partOrig: list) -> list:
        # jako argument przyjmuje kawałek danych w postaci listy
        # oblicza CRC, zwraca CRC

        # dzielnik
        original_div = [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1]

        # dodanie 3 wyzerowanych bitow do ciagu danych
        part = partOrig[:]
        part.extend(32 * [0])

        if part.count(1) == 0:
            return 32 * [0]

        divider = []

        result = part[:]
        while len(result) >= len(original_div):
            divider = self.shift_divider(result, divider, original_div)

            temp_result = []
            for j in range(0, len(result)):
                temp_result.append(xor(result[j], divider[j]))

            result = temp_result[:]
            del result[0: result.index(1)]

        # dopelnienie zerami do 3 bitow
        for i in range(32 - len(result)):
            result.insert(0, 0)
        return result

    def shift_divider(self, data: list, divider: list, original_div: list):
        divider.clear()
        i = data.index(1)

        divider.extend(i * [0])
        divider.extend(original_div)
        divider.extend((len(data) - len(divider)) * [0])

        return divider

    def noise_generator(self, bit):
        # model zakłóceń BSC

        # przypisz do new_bit negację bitu z prawdopodobieństwem self.noise
        # oraz właściwy bit z prawdopodobieństwem 1-self.noise
        new_bit = choices([not_(bit), bit], [self.noise, 1-self.noise])

        return int(new_bit[0])

    def get_orig_seq(self):
        return self.scrambler.input_seq

