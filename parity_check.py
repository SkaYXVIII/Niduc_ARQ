import numpy as np


def parity_check_encode(array: np.ndarray) -> np.ndarray:
    number_of_ones = 0
    for element in array:
        if element:
            number_of_ones += 1
    if number_of_ones % 2 == 0:
        return np.append(array, 0)
    else:
        return np.append(array, 1)


def parity_check_decode(array: np.ndarray) -> bool:
    if array.size > 1:
        number_of_ones = 0
        for element in array:
            if element:
                number_of_ones += 1
        if number_of_ones % 2 == 0:
            return True
        else:
            return False
