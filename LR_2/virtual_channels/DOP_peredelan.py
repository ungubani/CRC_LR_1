import matplotlib.pyplot as plt
import random
from collections import deque


def upload_from_buffers(last_sended: int, buffers: deque) -> int:
    flag = True  # Было ли выгружено сообщение?

    while flag:
        flag = False

        for buffer in buffers:
            if buffer and buffer[0] == last_sended + 1:
                last_sended = buffer.popleft()
                flag = True

    return last_sended


def virtual_channels(p_list: list, p_back_list: list, count_messages: int) -> (list, list):
    tau = len(p_list) - 1

    channels = [[] for _ in range(tau + 1)]  # Логирование первой отправки пакета в каналах
    acknowledgements = [[] for _ in range(tau + 1)]  # Логирование квитанций
    buffers = [deque() for _ in range(tau + 1)]  # Находящиеся в буферах сообщения
    buffers_fullness = [[] for _ in range(tau + 1)]  # Хранится заполненность буферов (кол-во сообщений в буферах)

    need_deliver_messages = count_messages

    TOTAL_TIME = 0
    vch_tx_work_status = [False] * (tau + 1)  #
    vch_rx_ack = [True] * (tau + 1)  # Готовность к приему [равно (+) квитанции до этого]

    translate_flag = False
    last_sended = 0

    while need_deliver_messages > 0 or translate_flag:
        for i in range(tau + 1):
            channels[i].extend([None] * (TOTAL_TIME - len(channels[i])))  # Выравнивание канала во времени
            acknowledgements[i].extend([None] * (TOTAL_TIME + tau + 1 - len(acknowledgements[i])))

            TOTAL_TIME += 1

            if need_deliver_messages > 0 and vch_rx_ack[i] == True:
                number_package = count_messages - need_deliver_messages + 1

                vch_tx_work_status[i] = number_package

                channels[i].append(number_package)
                need_deliver_messages -= 1

            elif need_deliver_messages <= 0 and vch_rx_ack[i] == True:
                vch_tx_work_status[i] = False

            else:
                channels[i].append(channels[i][-(tau + 1)])

            ack = None
            # Разыгрываем были ли ошибки при передаче сообщения
            if vch_tx_work_status[i] != False:
                ack = False if random.random() < p_list[i] else True
                # Разыгрываем были ли ошибки при передаче квитанции

                if random.random() < p_back_list[i]:
                    ack = -1

                if ack == True:
                    buffers[i].append(vch_tx_work_status[i])
                    last_sended = upload_from_buffers(last_sended, buffers)

            for j in range(tau + 1):
                fullness = len(buffers[j])
                buffers_fullness[j].append((TOTAL_TIME, fullness))

            acknowledgements[i].append(ack)
            vch_rx_ack[i] = ack

        translate_flag = any(vch_tx_work_status)

    return channels, acknowledgements, buffers_fullness


def plot_virtual_channels(p_list, p_back_list, count_messages):
    channels, acknowledgements, buffers_fullness = virtual_channels(p_list, p_back_list, count_messages)

    # Отрисовка лога состояний источника и квитанций
    for i in range(len(channels)):
        print(f'Канал {i+1}, Источник + квитанции + буфер')
        channel_status = channels[i]
        ch_timeline = list(range(len(channel_status)))

        ack_status = acknowledgements[i]
        ack_timeline = list(range(len(ack_status)))
        fig, (packages, acks, buffer) = plt.subplots(3, 1, figsize=(10, 8))

        packages.set_title(f"Передача пакетов для канала {i+1} (p={p_list[i]}, $p_{{обр}}={p_back_list[i]}$)")
        packages.stem(ch_timeline, channel_status, basefmt=" ")
        packages.set_ylabel('Номер пакета')
        packages.set_xlabel('Время')
        packages.grid(True)

        acks.set_title(f"Полученные квитанции для канала {i + 1} (p={p_list[i]}, $p_{{обр}}={p_back_list[i]}$)")
        acks.stem(ack_timeline, ack_status, basefmt=" ")
        acks.set_ylabel('ACK статус')
        acks.set_xlabel('Время')
        acks.set_yticks([-1, 0, 1])
        acks.set_yticklabels(['(+-)', '(-)', '(+)'])
        acks.grid(True)

        time_line, buffer_fullness = zip(*buffers_fullness[i])

        buffer.set_title(f"Заполненность буфера для канала {i + 1} (p={p_list[i]}, $p_{{обр}}={p_back_list[i]}$)")
        buffer.scatter(time_line, buffer_fullness, marker=".")
        buffer.set_ylabel('Сообщений в буфере')
        buffer.set_xlabel('Время')
        buffer.grid(True)

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    p_list_example = [0.1, 0.9, 0.2]  # Вероятности для каналов
    p_back_list_example = [0.04, 0.3, 0.07]
    count_messages_example = 100  # Количество сообщений
    plot_virtual_channels(p_list_example, p_back_list_example, count_messages_example)

