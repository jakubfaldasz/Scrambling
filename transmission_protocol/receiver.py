from operator import xor

from PIL import Image

from scramblers.scrambler_base import Scrambler_BaseClass
from scramblers.v34.v34_descrambler import V34_Descrambler
from scramblers.v34.v34_scrambler import V34_Scrambler
from scramblers.dvb.dvb_scrambler import DvbScrambler
from transmitter_receiver.transmitter import Transmitter


class Receiver:

    def __init__(self, scrambler: Scrambler_BaseClass, descrambler: Scrambler_BaseClass, noise: float, frame_size: int, sync_size: int, is_synchronous: bool):
        """
        noise: poziom zakłóceń; prawdopodobieństwo, że bit zostanie przekłamany
        """
        self.input_data = []
        self.descrambler = descrambler
        self.frame_size = frame_size
        self.pixels_in_frame = int(self.frame_size/8)
        self.sync_word = int(sync_size/2)*[1,0]
        self.scr_bits_counter = 0
        self.transmitter = Transmitter(scrambler, noise, frame_size, sync_size, is_synchronous)
        self.is_synchronous = is_synchronous

    def generate_input(self, input_image_name, output_image_name):
        self.input_data = self.transmitter.generate_output(input_image_name)
        img = Image.open(input_image_name)
        img_mode = img.mode
        img_size = img.size
        pixels = []

        self.descrambler.seq_state = self.transmitter.get_orig_seq()[:]

        while len(self.input_data) > 0:
            if self.is_synchronous:
                if self.input_data[0: len(self.sync_word)] == self.sync_word:
                    del self.input_data[0: len(self.sync_word)]
                    self.descrambler.seq_state = self.transmitter.get_orig_seq()[:]
                else:
                    del self.input_data[0: len(self.sync_word)]
            else:
                del self.input_data[0: len(self.sync_word)]

            frame = self.input_data[0: self.frame_size]
            del self.input_data[0: self.frame_size]

            crc = self.input_data[0: 32]
            del self.input_data[0: 32]

            if self.check_CRC(frame, crc):
                while len(frame) > 0:
                    pixel = self.descrambler.convert_to_dec(frame[0:8])
                    pixel = self.descrambler.scramble_pixel(pixel)
                    del frame[0:8]
                    pixels.append(pixel)
            else:
                pixels.extend(self.pixels_in_frame * [0])


        img = Image.new(img_mode, img_size)
        img.putdata(pixels)
        img.save(output_image_name)
        return img

    def check_CRC(self, partOrig: list, crc: list) -> list:
        # jako argument przyjmuje kawałek danych w postaci listy
        # sprawdza CRC, zwraca TRUE jeśli jest poprawne
        part = partOrig[:]
        part.extend(crc)
        original_div = [1,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,1,0,0,0,1,1,1,0,1,1,0,1,1,0,1,1,1]

        divider = []

        result = part[:]
        while len(result) >= len(original_div) and result.count(1) != 0:
            divider = self.shift_divider(result, divider, original_div)

            temp_result = []
            for j in range(0, len(result)):
                temp_result.append(xor(result[j], divider[j]))

            result = temp_result[:]
            if result.count(1) > 0:
                del result[0: result.index(1)]

        if result.count(1) > 0:
            return False
        else:
            return True

    def shift_divider(self, data: list, divider: list, original_div: list):
        divider.clear()
        i = data.index(1)

        divider.extend(i * [0])
        divider.extend(original_div)
        divider.extend((len(data) - len(divider)) * [0])

        return divider


rcv = Receiver(V34_Scrambler(), V34_Descrambler(), 0.00002, 320, 10, False)
rcv.generate_input("../assets/goldenGate.png", "received-V34.png")