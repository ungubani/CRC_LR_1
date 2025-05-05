"""
2.1. Нахождение среднего числа передач в алгоритме
с ожиданием при неограниченном числе повторных передач

2.2. Нахождение среднего числа передач в алгоритме
с ожиданием при ограниченном числе повторных передач

2.3. Нахождение среднего числа передач в алгоритме
с ожиданием при наличии ошибок в обратном канале

2.4. Моделирование алгоритма с ожиданием
для определения коэффициента использования канала при τ > 0
"""

import matplotlib.pyplot as plt
import numpy as np
import random


def wait_algo_cycle(number_package, tau, p_forw, p_back=0, max_N=10**7):
    ack_timeline = []  # История принятых квитанций на стороне источника
    source_timeline = []  # История принятых пакетов на стороне источника

    while max_N > 0:
        max_N -= 1

        # Имитация отправки сообщения и ожидания квитанции
        source_timeline.append(number_package)
        source_timeline.extend([None] * (tau))

        # Уровень 1 - отрицательная (-) квитанция
        # Уровень 2 - искаженная (+-) квитанция
        # Уровень 3 - положительная (+) квитанция
        ack = 1 if random.random() < p_forw else 3
        if p_back != 0 and random.random() < p_back:
            ack = 2

        ack_timeline.extend([None] * (tau))
        ack_timeline.append(ack)

        if ack == 3: break  # Если (+) квитанция, цикл закончен

    return source_timeline, ack_timeline


def wait_algo(K, tau, p_forw, p_back=0, max_N=10**7):
    """
    :param K: Количество успешно доставленных пакетов при моделировании
    :param tau: Время доставки квитанции по обратному каналу
    :param p_forw: Вероятность ошибки пакета в прямом канале
    :param p_back: Вероятность искажения квитанции
    :param max_N: Ограничение на количество повторных передач
    :return: timeline - временные метки,
    source_timeline - номера отправленных источником сообщений во времени,
    ack_timeline - статус зафиксированных источником квитанций
    """

    source_timeline = []
    ack_timeline = []

    number_package = 1

    while K > 0:
        K -= 1
        src_tl, ack_tl = wait_algo_cycle(number_package, tau, p_forw, p_back, max_N)

        source_timeline.extend(src_tl)
        ack_timeline.extend(ack_tl)

        number_package = number_package % 2 + 1  # Достаточно лишь двух пакетов для визуализации

    timeline = list(range(len(source_timeline)))

    return timeline, source_timeline, ack_timeline


def plot_avg_transmissions_2_1(K=100, tau=3, samples=20):
    p_vals = np.linspace(0.01, 0.99, samples)
    N_avg_vals = []

    for p_forw in p_vals:
        print(p_forw)
        _, source_timeline, _ = wait_algo(K, tau, p_forw)
        total_sent = sum(1 for s in source_timeline if s is not None)
        N_avg = total_sent / K
        N_avg_vals.append(N_avg)

    plt.figure(figsize=(10, 6))
    plt.plot(p_vals, N_avg_vals, marker='o', color='blue', label='N_ср(p_forw)')
    plt.xlabel('Вероятность ошибки в прямом канале (p_forw)')
    plt.ylabel('Среднее число передач N_ср')
    plt.title('2.1. Среднее число передач при ожидании (p_back=0)')
    plt.grid(True)
    plt.legend()
    plt.show()


plot_avg_transmissions_2_1()


def compute_avg_transmissions_limited(K, tau, p_values, max_N):
    avg_transmissions = []

    for p_forw in p_values:
        timeline, source_timeline, _ = wait_algo(K, tau, p_forw, p_back=0, max_N=max_N)
        num_transmissions = sum(1 for x in source_timeline if x is not None)
        avg = num_transmissions / K
        avg_transmissions.append(avg)

    return avg_transmissions

def plot_avg_transmissions_vs_p_limited():
    K = 100
    tau = 3
    max_N = 8  # Ограничение на число повторных попыток
    p_values = np.linspace(0, 0.9, 10)

    avg_transmissions = compute_avg_transmissions_limited(K, tau, p_values, max_N)

    plt.figure(figsize=(8, 5))
    plt.plot(p_values, avg_transmissions, marker='s', color='orange', label=f'N_ср (max_N={max_N})')
    plt.title(f'2.2 Среднее число передач N_ср(p), ограничение max_N={max_N}')
    plt.xlabel('Вероятность ошибки в прямом канале (p)')
    plt.ylabel('Среднее число передач N_ср')
    plt.grid(True)
    plt.legend()
    plt.show()

# Вызов построения графика для 2.2
plot_avg_transmissions_vs_p_limited()


def plot_time_diagrams_and_efficiency(K, p_forw=0.2, p_back=0.6, taus=[1, 3, 5]):
    plt.figure(figsize=(15, 5 * len(taus)))

    efficiencies = []

    for idx, tau in enumerate(taus):
        timeline, source_timeline, ack_timeline = wait_algo(K, tau, p_forw, p_back)

        # Расчёт коэффициента использования канала
        eta = K / len(timeline)
        efficiencies.append((tau, eta))

        # Построение графика с использованием bins (subplot из двух графиков)
        ax1 = plt.subplot(len(taus), 2, 2 * idx + 1)
        ax1.set_title(f'Передача сообщений (tau={tau})')
        ax1.plot(timeline, [x if x is not None else 0 for x in source_timeline],
                 drawstyle='steps-post', color='blue', label='source_timeline')
        ax1.set_ylabel('Номер пакета')
        ax1.set_xlabel('Время')
        ax1.grid(True)
        ax1.legend()

        ax2 = plt.subplot(len(taus), 2, 2 * idx + 2)
        ax2.set_title(f'Квитанции (tau={tau})')
        ax2.plot(timeline, [x if x is not None else 0 for x in ack_timeline],
                 drawstyle='steps-post', color='green', label='ack_timeline')
        ax2.set_ylabel('ACK статус')
        ax2.set_xlabel('Время')
        ax2.set_yticks([0, 1, 2, 3])
        ax2.set_yticklabels(['None', '-', '+-', '+'])
        ax2.grid(True)
        ax2.legend()

    plt.tight_layout()
    plt.show()

    # График коэффициента использования
    plt.figure(figsize=(8, 4))
    taus_list, eta_list = zip(*efficiencies)
    plt.plot(taus_list, eta_list, marker='o', color='purple')
    plt.title('Коэффициент использования канала η(τ)')
    plt.xlabel('Задержка квитанции τ')
    plt.ylabel('η = K / len(timeline)')
    plt.grid(True)
    plt.show()


# Вызов функции для построения графиков по пункту 2.4
plot_time_diagrams_and_efficiency(K=50, taus=[1, 3, 5, 7], p_forw=0.2, p_back=0.6)


def plot_24_my(K=50, tau=3, p_forw=0.2, p_back=0.6):
    timeline, source_timeline, ack_timeline = wait_algo(K, tau, p_forw, p_back)

    packages = plt.subplot(2, 1, 1)
    packages.set_title("Передача пакетов")
    packages.stem(timeline, source_timeline)
    packages.set_ylabel('Номер пакета')
    packages.set_xlabel('Время')
    packages.grid(True)

    ack_status = plt.subplot(2, 1, 2)
    ack_status.set_title("Полученные квитанции")
    ack_status.stem(timeline, ack_timeline)
    ack_status.set_ylabel('ACK статус')
    ack_status.set_xlabel('Время')
    ack_status.set_yticks([1, 2, 3])
    ack_status.set_yticklabels(['-', '+-', '+'])
    ack_status.grid(True)

    plt.show()

plot_24_my()
