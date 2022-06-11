import numpy as np


class RepetitionCode:
    def __init__(self):
        self.__repetition = 3
        self.__packet_length = 0

    def encode(self, array: np.ndarray) -> np.ndarray:
        encoded = []
        self.__packet_length = array.size

        for i in range(self.__repetition):
            encoded = np.append(encoded, array)

        return encoded

    def check(self, array: np.ndarray) -> bool:
        array = self.separate_packets(array)
        errors = 0
        var = array[0]

        for arr in array:
            if not np.array_equal(var, arr):
                errors += 1

        if errors >= 1:
            return False
        return True

    def separate_packets(self, array: np.ndarray) -> np.ndarray:
        return array.reshape(self.__repetition, self.__packet_length)

    def get_packet_length(self):
        return self.__packet_length
