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

from LR_2.virtual_channels.vch_ETA import effiency_channel


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



def compute_avg_N(K, tau, p_values, max_N=10**7, p_back=0):
    avg_transmissions = []

    for p_forw in p_values:
        timeline, source_timeline, _ = wait_algo(K, tau, p_forw, p_back=p_back, max_N=max_N)
        num_transmissions = sum(1 for x in source_timeline if x is not None)
        avg = num_transmissions / K
        avg_transmissions.append(avg)

    return avg_transmissions


def plot_avg_N_2_1_nonlimited(K=100, tau=3, p_values=np.linspace(0.01,0.99,20)):
    """
    2.1. Нахождение среднего числа передач в алгоритме
    с ожиданием при ___неограниченном___ числе повторных передач
    """
    N_avg_vals = compute_avg_N(K, tau, p_values)

    plt.figure(figsize=(10, 6))
    plt.plot(p_values, N_avg_vals, marker='o', label=f'$N_{{ср}}$($p_{{forw}}$)')
    plt.plot(p_values, [1 / (1 - p) for p in p_values], linestyle=":", marker="+", label=f"$N_{{теор}}$")

    plt.xlabel(f'$p_{{forw}}$')
    plt.ylabel(f'$N_{{ср}}($p_{{forw}}$)$')
    plt.title(f'2.1 Алгоритм с ожиданием, n=$\infty$. '
              f'\nСреднее число передач ($p_{{back}}$=0)')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_avg_N_2_2_limited(K=100, tau=3, max_N=8, p_values=np.linspace(0,0.99,20)):
    """
    2.2. Нахождение среднего числа передач в алгоритме
    с ожиданием при ___ограниченном___ числе повторных передач
    """
    avg_transmissions = compute_avg_N(K, tau, p_values, max_N)

    plt.figure(figsize=(8, 5))
    plt.plot(p_values, avg_transmissions, marker='o', label=f'$N_{{ср}}$(p, $max_N$={max_N})')
    plt.plot(p_values, [(1 - p ** max_N) / (1 - p) for p in p_values], marker="+",
             label=f"$N_{{ср}}$(p, $max_N={max_N}$) - теория", linestyle=":")
    plt.title(f'2.2 Алгоритм с ожиданием, ограничение n повторных передач. '
              f'\nСреднее число передач ($p_{{back}}$=0)')
    plt.xlabel(f'$p_{{forw}}$')
    plt.ylabel(f'$N_{{ср}}$')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_avg_N_2_3_nonlimited(K=100, tau=3, p_values=np.linspace(0,0.99,20),
                              p_back_list=np.linspace(0,0.9,3)):
    """
    2.3. Нахождение среднего числа передач в алгоритме
    с ожиданием при наличии ошибок в обратном канале
    при ___неограниченном___ числе повторных передач
    """

    plt.figure(figsize=(10, 6))
    for p_back in p_back_list:
        N_avg_vals = compute_avg_N(K, tau, p_values, p_back=p_back)
        plt.plot(p_values, N_avg_vals, marker='o', label=f'$N_{{ср}}$($p_{{forw}}$, $p_{{back}}$={p_back})')
        plt.plot(p_values, [1 / ((1 - p) * (1 - p_back)) for p in p_values],
                 linestyle=":", marker="+", label=f"$N_{{теор}}$($p_{{forw}}$, $p_{{back}}={p_back}$)")

    plt.xlabel(f'$p_{{forw}}$')
    plt.ylabel(f'$N_{{ср}}$')
    plt.title(f'Алгоритм с ожиданием, n=$\infty$. '
              f'\nСреднее число передач ($p_{{back}}\\neq0$)')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_avg_N_2_3_limited(K=100, tau=3, p_values=np.linspace(0,0.99,20), max_N=8,
                           p_back_list=np.linspace(0,0.9,3)):
    """
    2.3. Нахождение среднего числа передач в алгоритме
    с ожиданием при наличии ошибок в обратном канале
    при ___ограниченном___ числе повторных передач
    """

    plt.figure(figsize=(10, 6))
    for p_back in p_back_list:
        N_avg_vals = compute_avg_N(K=K, tau=tau, p_values=p_values, max_N=max_N, p_back=p_back)
        plt.plot(p_values, N_avg_vals, marker='o', label=f'$N_{{ср}}$($p_{{forw}}$, p_back={p_back})')
        plt.plot(p_values, [(1 - (p + p_back - p * p_back) ** max_N) /
                            ((1 - p) * (1 - p_back)) for p in p_values],
                 linestyle=":", marker="+", label=f"$N_{{теор}}($p_{{forw}}$, p_back={p_back})$")

    plt.xlabel(f'$p_{{forw}}$')
    plt.ylabel(f'$N_{{ср}}$')
    plt.title(f'Алгоритм с ожиданием, n={{$\infty$}}. '
              f'\nСреднее число передач ($p_{{back}}\\neq0$)')
    plt.grid(True)
    plt.legend()
    plt.show()



def plot_efficiency_2_4_nonlimited(K=500, p_forw=0.2, taus=[1, 2, 3, 4, 5]):
    efficiencies = []
    efficiencies_theor = []

    for idx, tau in enumerate(taus):
        timeline, source_timeline, ack_timeline = wait_algo(K, tau, p_forw)

        eta = K / len(timeline)
        efficiencies.append((tau, eta))
        efficiencies_theor.append((tau, (1 - p_forw) / (1 + tau)))

    plt.figure(figsize=(8, 4))
    taus_list, eta_list = zip(*efficiencies)
    taus_list, eta_list_theor = zip(*efficiencies_theor)

    plt.plot(taus_list, eta_list, marker='o')
    plt.plot(taus_list, eta_list_theor, linestyle=":", marker='+')
    plt.title('Коэффициент использования канала η(τ)')
    plt.xlabel('Задержка квитанции τ')
    plt.ylabel('$\eta$()')
    plt.grid(True)
    plt.show()


def plot_diagram_2_4(K=50, tau=3, p_forw=0.2, p_back=0.1):
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





if __name__ == "__main__":
    # plot_avg_N_2_1_nonlimited()
    # plot_avg_N_2_2_limited()
    # plot_avg_N_2_3_nonlimited()
    # plot_avg_N_2_3_limited()
    # plot_efficiency_2_4_nonlimited()
    plot_diagram_2_4()

