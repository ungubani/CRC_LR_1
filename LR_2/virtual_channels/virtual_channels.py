from multipledispatch import dispatch
import matplotlib.pyplot as plt
import numpy as np
import random


@dispatch(float, int)
def virtual_channels(p: float, tau: int):
    count_messages = 10_000 * (tau + 1)
    return virtual_channels(p, tau, count_messages)

@dispatch(float, int, int)
def virtual_channels(p: float, tau: int, count_messages):
    channels = [[] for _ in range(tau + 1)]  # Логирование происходящего в каналах

    need_deliver_messages = count_messages

    TOTAL_TIME = 0
    vch_tx_work_status = [False] * (tau + 1)  #
    vch_rx_ack = [True] * (tau + 1)  # Готовность к приему [равно (+) квитанции до этого]

    translate_flag = False

    step = 0
    while need_deliver_messages > 0 or translate_flag:
        # print(f"step= {step}")
        step += 1

        for i in range(tau + 1):
            channels[i].extend([None] * (TOTAL_TIME - len(channels[i])))  # Выравнивание канала во времени

            TOTAL_TIME += 1

            if need_deliver_messages > 0 and vch_rx_ack[i] == True:
                vch_tx_work_status[i] = True
                channels[i].append(need_deliver_messages % (2 * tau + 2))
                need_deliver_messages -= 1

            elif need_deliver_messages <= 0 and vch_rx_ack[i] == True:
                vch_tx_work_status[i] = False

            # Разыгрываем будет доставлено сообщение или нет
            vch_rx_ack[i] = False if random.random() < p else True

        translate_flag = any(vch_tx_work_status)

    return channels


@dispatch(list)
def virtual_channels(p_list: list):
    count_messages = 10_000 * len(p_list)
    return virtual_channels(p_list, count_messages)


@dispatch(list, int)
def virtual_channels(p_list: list, count_messages: int):
    channels = [[] for _ in range(len(p_list))]  # Логирование первой отправки пакета в каналах
    acknowledgements = [[] for _ in range(len(p_list))]  # Логирование квитанций
    tau = len(channels) - 1

    need_deliver_messages = count_messages

    TOTAL_TIME = 0
    vch_tx_work_status = [False] * (tau + 1)  #
    vch_rx_ack = [True] * (tau + 1)  # Готовность к приему [равно (+) квитанции до этого]

    translate_flag = False

    # step = 0
    while need_deliver_messages > 0 or translate_flag:
        # print(f"step= {step}")
        # step += 1

        for i in range(tau + 1):
            channels[i].extend([None] * (TOTAL_TIME - len(channels[i])))  # Выравнивание канала во времени
            acknowledgements[i].extend([None] * (TOTAL_TIME + tau + 1 - len(acknowledgements[i])))

            TOTAL_TIME += 1

            if need_deliver_messages > 0 and vch_rx_ack[i] == True:
                vch_tx_work_status[i] = True
                channels[i].append(1 + need_deliver_messages % (2 * tau + 2))
                need_deliver_messages -= 1

            elif need_deliver_messages <= 0 and vch_rx_ack[i] == True:
                vch_tx_work_status[i] = False

            # Разыгрываем будет доставлено сообщение или нет
            if vch_tx_work_status[i]:
                ack = False if random.random() < p_list[i] else True
                acknowledgements[i].append(ack)
                vch_rx_ack[i] = ack

        translate_flag = any(vch_tx_work_status)

    return channels, acknowledgements


def plot_virtual_channels(p_list, count_messages):
    channels, acknowledgements = virtual_channels(p_list, count_messages)

    for i in range(len(channels)):
        print(len(channels[i]), len(acknowledgements[i]))

    for i in range(len(channels)):
        channel_status = channels[i]
        ch_timeline = list(range(len(channel_status)))

        ack_status = acknowledgements[i]
        ack_timeline = list(range(len(ack_status)))
        fig, (packages, acks) = plt.subplots(2, 1, figsize=(10, 8))

        packages.set_title(f"Передача пакетов для канала {i+1} (p={p_list[i]})")
        packages.stem(ch_timeline, channel_status, basefmt=" ")
        packages.set_ylabel('Номер пакета')
        packages.set_xlabel('Время')
        packages.grid(True)

        acks.set_title(f"Полученные квитанции для канала {i + 1} (p={p_list[i]})")
        acks.stem(ack_timeline, ack_status, basefmt=" ")
        acks.set_ylabel('ACK статус')
        acks.set_xlabel('Время')
        acks.set_yticks([0, 1])
        acks.set_yticklabels(['-', '+'])
        acks.grid(True)

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    COUNT_MESSAGES = 50_000

    p_list_example = [0.1, 0.3, 0.9999]  # Вероятности для каналов
    count_messages_example = 100  # Количество сообщений
    plot_virtual_channels(p_list_example, count_messages_example)

