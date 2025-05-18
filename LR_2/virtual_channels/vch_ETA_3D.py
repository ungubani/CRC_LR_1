import matplotlib.pyplot as plt
import numpy as np
import random
from mpl_toolkits.mplot3d import Axes3D

def effiency_channel(p=None, tau=None, count_messages=25_000):
    need_deliver_messages = count_messages
    TOTAL_TIME = 0
    vch_tx_work_status = [False] * (tau + 1)
    vch_rx_ack = [True] * (tau + 1)
    translate_flag = False

    step = 0
    while need_deliver_messages > 0 or translate_flag:
        step += 1
        for i in range(tau + 1):
            TOTAL_TIME += 1
            if need_deliver_messages > 0 and vch_rx_ack[i] == True:
                vch_tx_work_status[i] = True
                need_deliver_messages -= 1
            elif need_deliver_messages <= 0 and vch_rx_ack[i] == True:
                vch_tx_work_status[i] = False
            vch_rx_ack[i] = False if random.random() < p else True
        translate_flag = any(vch_tx_work_status)
    return count_messages / TOTAL_TIME


if __name__ =="__main__":
    p_values = np.linspace(0.0, 0.5, 10)
    tau_values = np.arange(1, 11, 1)

    P, T = np.meshgrid(p_values, tau_values)
    Z = np.zeros_like(P)

    for i in range(P.shape[0]):
        for j in range(P.shape[1]):
            Z[i, j] = effiency_channel(p=P[i, j], tau=T[i, j])

    # Построение графика
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(P, T, Z, cmap='viridis')

    ax.set_title("Эффективность η(p, τ)")
    ax.set_xlabel("Вероятность ошибки p")
    ax.set_ylabel("Задержка τ")
    ax.set_zlabel("Эффективность η")

    plt.tight_layout()
    plt.show()
