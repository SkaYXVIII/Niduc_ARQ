import numpy as np


class CyclicRedundancyCheck:
    def __init__(self):
        self.__polynomial = np.array(
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1])
        self.__number_of_bits = 32

    def divide(self, array: np.ndarray) -> np.ndarray:
        tmp = array.copy()
        for i in range(tmp.size - self.__number_of_bits):
            index = 0
            if tmp[i] == 0:
                continue

            for j in range(i, i + self.__number_of_bits + 1):
                tmp[j] = tmp[j] ^ self.__polynomial[index]
                index += 1
        return tmp

    def encode(self, array: np.ndarray) -> np.ndarray:
        data_array = np.append(array, np.full(self.__number_of_bits, 0))
        tmp = self.divide(data_array)
        crc_code = tmp[(self.__number_of_bits * -1):]
        return np.append(array, crc_code)

    def check(self, array: np.ndarray) -> bool:
        if array.size > self.__number_of_bits:
            tmp = self.divide(array)

            if np.array_equal(tmp, np.full(tmp.size, 0)):
                return True
            else:
                return False
        else:
            return False
