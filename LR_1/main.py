import coder
import symmetrical_channel

from matplotlib import pyplot as plt
from typing import List
import math
import random


def has_errors(errors: List[int]) -> True:
    return sum(errors) != 0


def message_random_generator(length: int, probability: float = 0.5) -> List[int]:
    # probability - вероятность "1" на i-й позиции

    message = []
    for i in range(length):
        if random.random() < probability:
            message.append(1)
        else:
            message.append(0)

    return message


if __name__ == "__main__":
    _GENERATING_POLYNOMIAL = [1, 0, 1, 1]  # Порождающий многочлен
    _Pe_BIT = 0.01  # Вероятность ошибки на бит

    epsilon = 0.01  # 0.01 - 22500 экспериментов; 0.005 - 90000 экспериментов
    numbers_experiments = math.ceil(9 / (4 * epsilon ** 2))
    print(f"Точность = {epsilon}, количество экспериментов = {numbers_experiments}")

    lengths = [i for i in range(2, 21, 2)]  # Длина кодируемой последовательности
    pe_values = []  # Здесь будет накопление данных о вероятности ошибки декодирования

    for length in lengths:
        print(f"Обрабатывается длина сообщения {length}")
        decoder_error_counter = 0  # Количество ошибок декодирования

        for _ in range(numbers_experiments):
            # Источник
            source_message = message_random_generator(length)

            # Кодер
            code_word = coder.encode(source_message, _GENERATING_POLYNOMIAL)

            # Канальный уровень
            errors = symmetrical_channel.errors_vector_generator(len(code_word), _Pe_BIT)
            channel_has_errors = has_errors(errors)
            channel_word = symmetrical_channel.adding_errors(code_word, errors)

            # Декодер
            decoder_message, decoder_decision = coder.decoder(channel_word, _GENERATING_POLYNOMIAL)

            if decoder_decision != channel_has_errors:
                # print(f"source_message= {source_message}\n"
                #       f"code_word= {code_word}\n"
                #       f"errors= {errors}\n"
                #       f"channel_has_errors= {channel_has_errors}\n"
                #       f"channel_word= {channel_word}\n"
                #       f"decoder_message= {decoder_message}\n"
                #       f"decoder_decision= {decoder_decision}\n")
                #
                # input()  # Для "остановки"
                decoder_error_counter += 1

        pe = decoder_error_counter / numbers_experiments  # Вероятность ошибки декодирования
        pe_values.append(pe)

    # print("Длины кодируемых последовательностей:", lengths)
    # print("Вероятности ошибки декодирования:", pe_values)

    plt.figure(figsize=(12, 8))
    plt.semilogy(lengths, pe_values, marker=".", label=f"Pe (СК без памяти, Pb = {_Pe_BIT})")

    plt.title(f"Вероятность ошибки декодирования CRC-{coder.degree_polynomial(_GENERATING_POLYNOMIAL)}")
    plt.xlabel("Длина кодируемой последовательности")
    plt.ylabel("Pe")

    plt.legend()
    plt.grid()
    plt.show()
