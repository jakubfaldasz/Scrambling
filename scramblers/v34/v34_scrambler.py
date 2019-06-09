"""
Implementacja w oparciu o
https://en.wikipedia.org/wiki/Scrambler#Multiplicative_(self-synchronizing)_scramblers
"""

from operator import xor

from scramblers.scrambler_base import Scrambler_BaseClass


class V34_Scrambler(Scrambler_BaseClass):
    """
    Klasa skramblująca sekwencję bitów.
    Dziedziczy metody po Scrambler_BaseClass
    """

    def __init__(self, input_seq=[], treat_as_pseudorandom_generator=False):
        # Scrambler_BaseClass.__init__(self, 23, 22, 17)
        Scrambler_BaseClass.__init__(self, input_seq=input_seq, val1_index=22, val2_index=17, register_length=23, treat_as_pseudorandom_generator=treat_as_pseudorandom_generator)

    def scramble_pixel(self, input_bits):
        output_bits = []
        input_string = self.convert_to_str(input_bits)
        for bit in input_string:
            generated_bit = xor(self.seq_state[self.val1_index], self.seq_state[self.val2_index])
            output_bit = xor(int(bit), generated_bit)
            output_bits.append(output_bit)
            self.seq_state.insert(0, output_bit)  # dodaj element na początku listy
            del self.seq_state[-1]  # usuń ostatni element z listy
        return self.convert_to_dec(output_bits)

