"""
Implementacja w oparciu o
https://en.wikipedia.org/wiki/Scrambler#Multiplicative_(self-synchronizing)_scramblers
"""

from abc import ABC, abstractmethod
from random import randint
from operator import xor

from PIL import Image


class Scrambler_BaseClass(ABC):
    """
    Klasa bazowa skramblera
    """

    seq_state = []  # obiekt przechowujący aktualny stan sekwencji bitów

    def __init__(self, val1_index: int, val2_index: int, input_seq: list, register_length=10, treat_as_pseudorandom_generator=False):
        """
        input_seq: [bool]
            tablica wartości int
        val1_index: int
            index wartości użytej do generowania kolejnego bitu w sekwencji
        val2_index: int
            index wartości użytej do generowania kolejnego bitu w sekwencji
        """

        self.input_seq = input_seq
        # inicjalizacja zmiennych w klasie
        if len(input_seq) == 0:
            self.input_seq = self.gen_seed(register_length)
        self.val1_index = val1_index
        self.val2_index = val2_index
        self.seq_state = self.input_seq[:]
        self.period = 0
        self.treat_as_pseudorandom_generator = treat_as_pseudorandom_generator

        # sprawdzienie poprawności danych
        if (self.val1_index < 0 or self.val2_index < 0 or
                self.val1_index > len(self.input_seq) or self.val2_index > len(self.input_seq)):
            raise Exception('indexes should point to input_seq array values')

        if len(self.input_seq) < 2:
            raise Exception('length of input_seqence should be at least 2')

    def next(self, input_bit):
        """
        `input_bit`: wartośc do zeskramblowania
        zwraca: zeskramblowaną wartość
        """
        generated_bit = 0
        if self.val1_index != self.val2_index:
            # nie ma sensu XOR'ować takich samych wartości, bo zawsze da to wynik = 0
            generated_bit = xor(self.seq_state[self.val1_index], self.seq_state[self.val2_index])
        else:
            generated_bit = self.seq_state[self.val1_index]

        output = 0
        # skrambler XOR'uje wynik z wartością na wejściu (input)
        # w przypadku generatora pseudolosowego pomijamy ten krok
        if self.treat_as_pseudorandom_generator:
            output = generated_bit
        else:
            output = xor(input_bit, generated_bit)

        # dodaj na początek sekwencji skramblującej nową wartość
        self.seq_state.insert(0, output)
        # usuń ostatnią wartość z sekwencji skramblującej
        del self.seq_state[-1]

        return output

    def generate_output_for(self, input):
        """
        Generuje zeskrablowana tablicę

        :param input: tablica z danymi wejsciowymi do zescramblowania
        :return: tablica zeskramblowanych bitow
        """
        output_sequence = []
        for i in input:
            output_sequence.append(self.next(i))
        return output_sequence

    def generate_random_output(self, size):
        output_sequence = []
        for x in range(size):
            i = randint(0, 1)
            output_sequence.append(self.next(i))
        return output_sequence

    """
    --------------
    METODY DO SCRAMBLOWANIA OBRAZOW PONIZEJ:
    --------------
    """

    @abstractmethod
    def scramble_pixel(self, input_bits):
        pass

    def convert_to_str(self, input_bits):
        string = str(bin(input_bits))
        string = string[2:]

        string = (8 - len(string)) * str(0) + string

        return string

    def convert_to_dec(self, xs):
        sum = 0
        i = 1
        for x in reversed(xs):
            sum += x * i
            i *= 2
        return sum

    def gen_seed(self, length):
        xs = []
        for i in range(0, length):
            xs.append(randint(0, 1))

        return xs

    def generate_scrambled_pixels(self, input_pixels):
        output_seq = []
        for i in input_pixels:
            output_seq.append(self.scramble_pixel(i))

        return output_seq

    def scramble_image(self, input_image, output_image):
        img = Image.open(input_image)
        pix_val = list(img.getdata())
        scrambled_pixels = self.generate_scrambled_pixels(pix_val)
        img2 = Image.new(img.mode, img.size)
        img2.putdata(scrambled_pixels)
        img2.save(output_image)
        return img2

    def period_counter (self):
        self.next(0)
        self.period += 1
        while self.input_seq != self.seq_state:
            self.next(0)
            self.period +=1
        return self.period


