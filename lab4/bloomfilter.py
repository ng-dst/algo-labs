import math
import mmh3

from bitarray import bitarray


class BloomFilter:
    def __init__(self, items_count, fp_prob):
        self.fp_prob = fp_prob
        self.items_count = items_count
        self.size = self.get_size(items_count, fp_prob)
        self.hash_count = self.get_hash_count(self.size, items_count)
        self.bit_array = bitarray(self.size)
        self.bit_array.setall(0)

    def add(self, item):
        for i in range(self.hash_count):
            index = mmh3.hash(item, i) % self.size
            self.bit_array[index] = True

    def __contains__(self, item):
        for i in range(self.hash_count):
            index = mmh3.hash(item, i) % self.size
            if not self.bit_array[index]:
                return False
        return True

    @classmethod
    def get_size(cls, n, p):
        return int(-(n * math.log(p)) / (math.log(2) ** 2))

    @classmethod
    def get_hash_count(cls, m, n):
        return int((m / n) * math.log(2))
