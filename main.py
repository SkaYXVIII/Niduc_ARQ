import numpy as np
import CRC32_code as crc
import parity_check
from numpy import random
import math
import komm

resending_counter = 0
crc_code = crc.CyclicRedundancyCheck()

# poniższe parametry zmieniamy, aby wyszły rózne wyniki
data_size = 800
packets_size = 4
error_probability = 0.05


def restart_counters():
    global resending_counter
    resending_counter = 0


def split_into_packets(array: np.ndarray) -> np.ndarray:
    packets_counter = math.ceil(data_size / packets_size)
    return np.array(np.array_split(array, packets_counter), dtype=object)


def test(packets: np.ndarray, code_type):
    if code_type == 1 or code_type == 2:
        if code_type == 1:
            print("CRC32: ")
        if code_type == 2:
            print("Parity: ")
        global resending_counter
        errors_detected = 0
        errors_not_detected = 0
        unchanged_packets = 0
        array = []

        for packet in packets:
            bsc = komm.BinarySymmetricChannel(error_probability)

            if code_type == 1:
                encoded_packet = crc_code.encode(packet)
            if code_type == 2:
                encoded_packet = parity_check.parity_check_encode(packet)
            packet_after_noise = bsc(encoded_packet)

            if code_type == 1:
                if crc_code.check(packet_after_noise):
                    if np.array_equal(encoded_packet, packet_after_noise):
                        unchanged_packets += 1
                    else:
                        errors_not_detected += 1
                else:
                    errors_detected += 1
                    array.append(packet)

            if code_type == 2:
                if parity_check.parity_check_decode(packet_after_noise):
                    if np.array_equal(encoded_packet, packet_after_noise):
                        unchanged_packets += 1
                    else:
                        errors_not_detected += 1
                else:
                    errors_detected += 1
                    array.append(packet)

        print("Pomyslnie przeslane pakiety", unchanged_packets)
        print("Wykryte bledy", errors_detected)
        print("Niewykryte bledy", errors_not_detected)
        print()

        if len(array) > 0:
            resending_counter += 1
            print("Ponowne przesyłanie pakietów")
            print()
            test(np.array(array), code_type)


if __name__ == '__main__':
    test_array = random.randint(2, size=data_size)
    test_packets = split_into_packets(test_array)
    test(test_packets, 1)
    print("Ile razy ponownie przesyłano pakiety CRC: ", resending_counter)
    print()
    print("---------------------------------------------------")
    restart_counters()
    test(test_packets, 2)
    print("Ile razy ponownie przesyłano pakiety Parzystość: ", resending_counter)
