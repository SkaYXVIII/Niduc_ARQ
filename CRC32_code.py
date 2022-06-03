import numpy as np
from numpy import random

class CyclicRedundancyCheck:
    def __init__(self):
        self.__polynomial = np.array([1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1])
        self.__number_of_bits = 32

    def encode(self, array: np.ndarray) -> np.ndarray:
        data_array = np.append(array, np.full(self.__number_of_bits, 0))
        help_val = np.array(2 ** (np.array(np.arange(data_array.size)[::-1], dtype=np.int64)), dtype=np.int64)
        integer_value_of_array = data_array.dot(help_val)
        divisor = np.append(self.__polynomial, np.full(data_array.size - self.__polynomial.size, 0))
        help_div = np.array(2 ** (np.array(np.arange(divisor.size)[::-1], dtype=np.int64)), dtype=np.int64)
        integer_value_of_divisor = divisor.dot(help_div)

        while integer_value_of_array > (2 ** self.__number_of_bits - 1):
            if integer_value_of_divisor <= ((2 ** (np.floor(np.log2(integer_value_of_array)) + 1)) - 1):
                integer_value_of_array = integer_value_of_array ^ integer_value_of_divisor
            integer_value_of_divisor = integer_value_of_divisor >> 1

        help1 = np.binary_repr(integer_value_of_array).zfill(self.__number_of_bits)
        crc_code = np.fromstring(help1,
                                 dtype='S1').astype(int)

        return np.append(array, crc_code)

    def check(self, array: np.ndarray) -> bool:
        if array.size > self.__number_of_bits:
            help_val = np.array(2 ** (np.array(np.arange(array.size)[::-1], dtype=np.int64)), dtype=np.int64)
            integer_value_of_array = (array.dot(help_val))
            divisor = np.append(self.__polynomial, np.full(array.size - self.__polynomial.size, 0))
            help_div = np.array(2 ** (np.array(np.arange(divisor.size)[::-1], dtype=np.int64)), dtype=np.int64)
            integer_value_of_divisor = divisor.dot(help_div)

            while integer_value_of_array > (2 ** self.__number_of_bits - 1):
                if integer_value_of_divisor <= ((2 ** (np.floor(np.log2(integer_value_of_array)) + 1)) - 1):
                    integer_value_of_array = integer_value_of_array ^ integer_value_of_divisor
                integer_value_of_divisor = integer_value_of_divisor >> 1

            if integer_value_of_array == 0:
                return True
            else:
                return False
        else:
            return False
