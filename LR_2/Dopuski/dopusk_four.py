"""
2.4 Моделирование алгоритма с ожиданием
для определения коэффициента использования канала при τ > 0
"""

import matplotlib.pyplot as plt
import random


def algo_wait(tau, p_forw, K):
    # K - количество удачно переданных пакетов
    time = []
    status = []

    current_time = 0

    while K > 0:
        time.append(current_time)
        status.append(0)

        current_time += 1

        if random.random() < p_forw:
            status.extend([-1] * tau)
            # print("Пакет поврежден")

        else:
            status.extend([1] * tau)
            K -= 1
            # print("Пакет успешно доставлен")

        time.extend([current_time] * tau)

        current_time += tau

    time.extend([current_time] * tau)
    status.extend([1] * tau)


    return time, status


def visualize(tau, p_forw, K):
    time, status = algo_wait(tau, p_forw, K)
    print("Eta_theor=", (1 - p_forw) / (1 + tau))
    print("Eta_exp=", K / time[-1])

    plt.figure(figsize=(12, 6))
    plt.step(time, status, where='post', label='Статус передачи', linewidth=2)

    # plt.axhline(0, color='grey', lw=0.5, ls='--')
    # plt.axhline(1, color='green', lw=0.5, ls='--', label='Положительная квитанция')
    # plt.axhline(-1, color='red', lw=0.5, ls='--', label='Отрицательная квитанция')

    plt.title(f'Временная диаграмма работы алгоритма с ожиданием\np={p_forw}, tau={tau}')
    plt.xlabel('Время')
    plt.ylabel('Статус передачи')
    plt.yticks([-1, 0, 1], ['Квит. (-)', 'Пакет', 'Квит. (+)'])
    plt.grid()
    plt.legend()
    plt.show()


if __name__ == "__main__":
    tau = 0
    p_forw = 0.5
    K = 100

    visualize(tau, p_forw, K)