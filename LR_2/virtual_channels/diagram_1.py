import matplotlib.pyplot as plt
import numpy as np
import random

def simulate_vchannels(p=0.1, tau=10, count=1000):
    NEED_DELIVER_MESSAGES = count
    VCH_TX_WORK_STATUS = [False] * (tau + 1)
    VCH_RX_ACK = [True] * (tau + 1)

    TRANSLATE_FLAG = False
    history = [[] for _ in range(tau + 1)]  # история по каналам
    step = 0

    while NEED_DELIVER_MESSAGES > 0 or TRANSLATE_FLAG:
        for i in range(tau + 1):
            if NEED_DELIVER_MESSAGES > 0 and VCH_RX_ACK[i]:
                VCH_TX_WORK_STATUS[i] = True
                NEED_DELIVER_MESSAGES -= 1
                delivered = 1 if random.random() >= p else -1
                history[i].append(delivered)
            elif VCH_RX_ACK[i]:
                VCH_TX_WORK_STATUS[i] = False
                history[i].append(0)  # канал простаивает
            else:
                history[i].append(0)

            VCH_RX_ACK[i] = False if random.random() < p else True

        TRANSLATE_FLAG = any(VCH_TX_WORK_STATUS)
        step += 1

    return np.array(history)

def plot_heatmap(data):
    plt.figure(figsize=(16, 6))
    cmap = plt.cm.get_cmap('RdYlGn', 3)  # -1 (red), 0 (white), 1 (green)
    plt.imshow(data, aspect='auto', cmap=cmap, vmin=-1, vmax=1)
    plt.colorbar(ticks=[-1, 0, 1], label='Статус')
    plt.yticks(range(data.shape[0]), [f'Канал {i}' for i in range(data.shape[0])])
    plt.xlabel('Время')
    plt.title('Состояние виртуальных каналов во времени')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()

def plot_cumulative_delivery(data):
    total_steps = data.shape[1]
    delivered = (data == 1).sum(axis=0)
    cumulative = np.cumsum(delivered)

    plt.figure(figsize=(12, 5))
    plt.plot(range(total_steps), cumulative, label='Всего доставлено')
    plt.xlabel('Время')
    plt.ylabel('Число доставленных сообщений')
    plt.title('Кумулятивная доставка сообщений по виртуальным каналам')
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    data = simulate_vchannels(p=0.1, tau=10, count=500)
    plot_heatmap(data)
    plot_cumulative_delivery(data)
