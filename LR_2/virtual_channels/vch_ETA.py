import matplotlib.pyplot as plt
import numpy as np
import random

def effiency_channel(p=None, tau=None, count_messages=10_000):
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
            TOTAL_TIME += 1

            if need_deliver_messages > 0 and vch_rx_ack[i] == True:
                vch_tx_work_status[i] = True
                need_deliver_messages -= 1

            elif need_deliver_messages <= 0 and vch_rx_ack[i] == True:
                vch_tx_work_status[i] = False

            # Разыгрываем будет доставлено сообщение или нет
            vch_rx_ack[i] = False if random.random() < p else True

        translate_flag = any(vch_tx_work_status)

    return count_messages / TOTAL_TIME




if __name__ == "__main__":
    COUNT_MESSAGES = 50_000

    tau_list_Pconst = [1, 2, 6, 10, 30]
    p_list_Pconst = [0.1, 0.3, 0.8]

    plt.figure()
    plt.title(f"Виртуальные каналы. Эффективность использования канала")
    plt.xlabel(f"$\\tau$")
    plt.ylabel(f"$\eta$(p=const, $\\tau$)")
    plt.ylim([0, 1])

    for p in p_list_Pconst:
        print(f"p=const, p={p}")
        efficiency_list = [effiency_channel(p, tau) for tau in tau_list_Pconst]
        plt.plot(tau_list_Pconst, efficiency_list, label=f"p={p}", marker="o")

    plt.grid()
    plt.legend()
    plt.show()


    tau_list_TAUconst = [1, 4, 16]
    p_list_TAUconst = np.linspace(0, 0.98, 11)

    plt.figure()
    plt.title(f"Виртуальные каналы. Эффективность использования канала")
    plt.xlabel(f"$\\tau$")
    plt.ylabel(f"$\eta$(p, $\\tau$=const)")
    plt.ylim([0, 1])

    for tau in tau_list_TAUconst:
        print(f"tau=const, tau={tau}")
        efficiency_list = [effiency_channel(p, tau) for p in p_list_TAUconst]
        plt.plot(p_list_TAUconst, efficiency_list, label=f"$\\tau$={tau}", marker="o")

    plt.grid()
    plt.legend()
    plt.show()