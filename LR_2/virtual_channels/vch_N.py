import matplotlib.pyplot as plt
import numpy as np
import random

def N_avg_channel(p, tau, count_messages=10_000):
    need_deliver_messages = count_messages

    TOTAL_SENDED = 0  # Сколько всего раз сообщения были отправлены
    vch_tx_work_status = [False] * (tau + 1)  #
    vch_rx_ack = [True] * (tau + 1)  # Готовность к приему [равно (+) квитанции до этого]

    translate_flag = False

    step = 0
    while need_deliver_messages > 0 or translate_flag:
        # print(f"step= {step}")
        step += 1

        for i in range(tau + 1):
            if need_deliver_messages > 0 and vch_rx_ack[i] == True:
                vch_tx_work_status[i] = True
                need_deliver_messages -= 1
                TOTAL_SENDED += 1

            elif need_deliver_messages <= 0 and vch_rx_ack[i] == True:
                vch_tx_work_status[i] = False

            elif vch_tx_work_status[i]:
                TOTAL_SENDED += 1

            # Разыгрываем будет доставлено сообщение или нет
            vch_rx_ack[i] = False if random.random() < p else True

        translate_flag = any(vch_tx_work_status)

    return TOTAL_SENDED / count_messages




if __name__ == "__main__":
    COUNT_MESSAGES = 50_000

    tau_list_Pconst = [1, 2, 6, 10, 30]
    p_list_Pconst = [0.1, 0.3, 0.8]

    plt.figure()
    plt.title(f"Виртуальные каналы. Среднее число передач")
    plt.xlabel(f"$\\tau$")
    plt.ylabel(f"$N_{{ср}}$(p=const, $\\tau$)")

    for p in p_list_Pconst:
        print(f"p=const, p={p}")
        N_avg_list = [N_avg_channel(p, tau, COUNT_MESSAGES) for tau in tau_list_Pconst]
        plt.plot(tau_list_Pconst, N_avg_list, label=f"p={p}", marker="o")

    plt.grid()
    plt.legend()
    plt.show()


    tau_list_TAUconst = [1, 4, 16]
    p_list_TAUconst = np.linspace(0, 0.99, 21)

    plt.figure()
    plt.title(f"Виртуальные каналы. Среднее число передач")
    plt.xlabel(f"p")
    plt.ylabel(f"$N_{{ср}}$(p, $\\tau$=const)")

    for tau in tau_list_TAUconst:
        print(f"tau=const, tau={tau}")
        N_avg_list = [N_avg_channel(p, tau, COUNT_MESSAGES) for p in p_list_TAUconst]
        plt.plot(p_list_TAUconst, N_avg_list, label=f"$\\tau$={tau}", marker="o")

    plt.plot(p_list_TAUconst, [1 / (1 - p) for p in p_list_TAUconst], label=f"$N_{{ср}}=1/(1-p)$", linestyle=":", marker="+")

    plt.grid()
    plt.legend()
    plt.show()