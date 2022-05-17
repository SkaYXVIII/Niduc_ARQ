import numpy as np
from numpy import random

class CyclicRedundancyCheck:
    def __init__(self):
        self.__polynomial = random.randint(2, size=33)
        self.__number_of_bits = 32

    def encode(self, array: np.ndarray) -> np.ndarray:
        data_array = np.append(array, np.full(self.__number_of_bits, 0))
        integer_value_of_array = data_array.dot(2 ** np.arange(data_array.size)[::-1])
        divisor = np.append(self.__polynomial, np.full(data_array.size - self.__polynomial.size, 0))
        integer_value_of_divisor = divisor.dot(2 ** np.arange(divisor.size)[::-1])

        while integer_value_of_array > (2 ** self.__number_of_bits - 1):
            if integer_value_of_divisor <= ((2 ** (np.floor(np.log2(integer_value_of_array)) + 1)) - 1):
                integer_value_of_array = integer_value_of_array ^ integer_value_of_divisor
            integer_value_of_divisor = integer_value_of_divisor >> 1

        crc_code = np.fromstring(np.binary_repr(integer_value_of_array).zfill(self.__number_of_bits),
                                 dtype='S1').astype(int)
        return np.append(array, crc_code)

    def check(self, array: np.ndarray) -> bool:
        if array.size > self.__number_of_bits:
            integer_value_of_array = (array.dot(2 ** np.arange(array.size)[::-1]))
            divisor = np.append(self.__polynomial, np.full(array.size - self.__polynomial.size, 0))
            integer_value_of_divisor = divisor.dot(2 ** np.arange(divisor.size)[::-1])

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
