"""
Implementacja w oparciu o
https://en.wikipedia.org/wiki/Scrambler#Multiplicative_(self-synchronizing)_scramblers
"""
from operator import xor

from scramblers.scrambler_base import Scrambler_BaseClass


class X15_Scrambler(Scrambler_BaseClass):

    def __init__(self, input_seq=[], treat_as_pseudorandom_generator=False):
        Scrambler_BaseClass.__init__(self, input_seq=input_seq, val1_index=6, val2_index=5, register_length=7, treat_as_pseudorandom_generator=treat_as_pseudorandom_generator)

    def scramble_pixel(self, input_bits):
        output_bits = []
        input_string = self.convert_to_str(input_bits)
        for bit in input_string:
            generated_bit = xor(self.seq_state[self.val1_index], self.seq_state[self.val2_index])
            output_bit = xor(int(bit), generated_bit)
            output_bits.append(output_bit)
            self.seq_state.insert(0, generated_bit)  # dodaj element na początku listy
            del self.seq_state[-1]  # usuń ostatni element z listy
        return self.convert_to_dec(output_bits)

    def descramble_image(self, inputImage, outputImage):
        self.seq_state = self.input_seq.copy()
        self.scramble_image(inputImage, outputImage)

