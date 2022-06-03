import numpy as np
import CRC32_code as crc
import parity_check
import repetition_code
from numpy import random
import math
import komm

resending_counter = 0
crc_code = crc.CyclicRedundancyCheck()
repetition = repetition_code.RepetitionCode()

# poniższe parametry zmieniamy, aby wyszły rózne wyniki
data_size = 100
packets_size = 31  #max 31
error_probability = 0.01

bsc = komm.BinarySymmetricChannel(error_probability)


def restart_counters():
    global resending_counter
    resending_counter = 0


def split_into_packets(array: np.ndarray) -> np.ndarray:
    packets_counter = math.ceil(data_size / packets_size)
    return np.array(np.array_split(array, packets_counter), dtype=object)


def test(packets: np.ndarray, code_type):
    if code_type == 1 or code_type == 2 or code_type == 3:
        if code_type == 1:
            print("CRC32: ")
        if code_type == 2:
            print("Parity: ")
        if code_type == 3:
            print("Repetition: ")
        global resending_counter
        errors_detected = 0
        errors_not_detected = 0
        unchanged_packets = 0
        array = []


        for packet in packets:
            if code_type == 1:
                encoded_packet = crc_code.encode(packet)
            if code_type == 2:
                encoded_packet = parity_check.parity_check_encode(packet)
            if code_type == 3:
                encoded_packet = repetition.encode(packet)

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

            if code_type == 3:
                if repetition.check(packet_after_noise):
                    if np.array_equal(encoded_packet, packet_after_noise):
                        unchanged_packets += 1
                    else:
                        errors_not_detected += 1
                else:
                    errors_detected += 1
                    if repetition.should_repeat():
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


def clear_console():
    print()
    print("---------------------------------------------------")
    restart_counters()


if __name__ == '__main__':
    test_array = random.randint(2, size=data_size)
    test_packets = split_into_packets(test_array)
    test(test_packets, 1)
    print("Ile razy ponownie przesyłano pakiety CRC: ", resending_counter)
    clear_console()
    test(test_packets, 2)
    print("Ile razy ponownie przesyłano pakiety Parzystość: ", resending_counter)
    clear_console()
    test(test_packets, 3)
    print("Ile razy ponownie przesyłano pakiety kod dublowania: ", resending_counter)
