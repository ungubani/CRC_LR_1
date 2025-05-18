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

    # ----------------------------------------
    # Постоянное значение вероятности ошибки p
    # ----------------------------------------

    tau_list_Pconst = list(range(1, 31))
    p_list_Pconst = [0.00001, 0.1, 0.3,  0.8]

    efficiency_lists_Pconst = []

    for p in p_list_Pconst:
        efficiency_lists_Pconst.append([effiency_channel(p, tau, COUNT_MESSAGES) for tau in tau_list_Pconst])


    plt.figure()
    plt.title(f"Эффективность использования канала. \nАлгоритм с виртуальными каналами")
    plt.xlabel(f"$\\tau$")
    plt.ylabel(f"$\eta$(p=const, $\\tau$)")
    plt.ylim([-0.05, 1.05])

    for i, p in enumerate(p_list_Pconst):
        print(f"p=const, p={p}")
        plt.plot(tau_list_Pconst, efficiency_lists_Pconst[i], label=f"p={p}", marker="o")

    plt.grid()
    plt.legend()
    plt.show()


    # ------------------------------------------------------------
    # Постоянное значение времени задержки получения квитанции tau
    # ------------------------------------------------------------
    tau_list_TAUconst = [1, 4, 16]
    p_list_TAUconst = np.linspace(0, 0.98, 11)

    efficiency_lists_TAUconst = []

    for tau in tau_list_TAUconst:
        efficiency_lists_TAUconst.append([effiency_channel(p, tau, COUNT_MESSAGES) for p in p_list_TAUconst])

    plt.figure()
    plt.title(f"Эффективность использования канала. \nАлгоритм с виртуальными каналами")
    plt.xlabel(f"p")
    plt.ylabel(f"$\eta$(p, $\\tau$=const)")
    # plt.ylim([0, 1])

    for i, tau in enumerate(tau_list_TAUconst):
        print(f"tau=const, tau={tau}")
        plt.plot(p_list_TAUconst, efficiency_lists_TAUconst[i], label=f"$\\tau$={tau}", marker="o")

    plt.plot(p_list_TAUconst, [1 - p for p in p_list_TAUconst], label=f"$\eta=(1-p)$", linestyle=":", marker="+")

    plt.grid()
    plt.legend()
    plt.show()


    # ----------------------------------
    # Сравнение с алгоритмом с возвратом
    # ----------------------------------
    plt.figure(figsize=(10,7))
    plt.title(f"Коэффициент использования канала.\nСравнение алгоритма с виртуальными каналами и алгоритма с возвратом")
    plt.xlabel(f"$\\tau$")
    plt.ylabel(f"$\eta$(p=const, $\\tau$)")
    plt.ylim([-0.05, 1.05])

    for i, p in enumerate(p_list_Pconst):
        print(f"p=const, p={p}")
        plt.plot(tau_list_Pconst, efficiency_lists_Pconst[i], label=f"А. с вирт. к., p={p}", marker="o")

        plt.plot(tau_list_Pconst, [(1 - p) / (1 + p * tau) for tau in tau_list_Pconst],
                 label=f"А. с возвратом, p={p}", linestyle="--", marker="x")

    plt.grid()
    plt.legend()
    plt.show()



    plt.figure(figsize=(10,7))
    plt.title(f"Коэффициент использования канала.\nСравнение алгоритма с виртуальными каналами и алгоритма с возвратом")
    plt.xlabel(f"p")
    plt.ylabel(f"$\eta$(p, $\\tau$=const)")
    # plt.ylim([0, 1])

    for i, tau in enumerate(tau_list_TAUconst):
        print(f"tau=const, tau={tau}")
        plt.plot(p_list_TAUconst, efficiency_lists_TAUconst[i], label=f"А. с вирт. к., $\\tau$={tau}", marker="o")

        plt.plot(p_list_TAUconst, [(1 - p) / (1 + p * tau) for p in p_list_TAUconst],
                 label=f"А. с возвратом, $\\tau$={tau}", linestyle="--", marker="x")

    plt.grid()
    plt.legend()
    plt.show()
