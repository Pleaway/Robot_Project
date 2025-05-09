import sys
from PyQt6.QtWidgets import QApplication
from Game_Engine.window import Window

from Algorithms.Q_learning import training
from Algorithms.APF import create_Q
from Game_Engine.grid import Grid
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def comparison(rows=100, cols=100, nb_training=25000, alphas=[0.1], gammas=[0.9], min_length=75):
    G = Grid(rows=100, cols=100, proba=0.2)

    app = QApplication(sys.argv)
    window = Window(grid=G, cell_size=10)
    window.show()
    app.exec()

    for alpha in alphas:
        for gamma in gammas:
            print(f'\r Comparaison {alphas.index(alpha)*len(gammas) + gammas.index(gamma) + 1}/{len(alphas)*len(gammas)} :      ', end='')

            step_list, reward_list = training(grid=G, num_training=nb_training, stats=True, alpha=alpha, gamma=gamma)

            if step_list[-1] < min_length:
                print(f'\r Redémarrage, longueur insuffisante ({step_list[-1]})')
                comparison(rows, cols, nb_training, alphas, gammas, min_length)
                exit()

            x = []
            y = []
            y_min = []
            y_max = []

            for i in range(1, nb_training//1000):
                window = step_list[i * 1000 - 50: i * 1000 + 51]
                nb_min = step_list[i*1000]
                nb_max = nb_min
                for step in window:
                    nb_min = min(nb_min, step)
                    nb_max = max(nb_max, step)

                average = sum(window) / len(window)
                x.append(i)
                y.append(average)

                # if y_min == average:
                #     y_min.append(0)
                # else:
                #     y_min.append(nb_min)
                # if y_max == average:
                #     y_max.append(0)
                # else:
                #     y_max.append(nb_max)

            # print("Etape :", i*1000, nb_min, nb_max, average)
            plt.plot(x, y, color=colors[gammas.index(gamma)], marker=markers[alphas.index(alpha)])
            # plt.errorbar(x, y, yerr=[y_min, y_max], capsize=2)


    plt.xlabel("Nombre de milliers d'entrainement")
    plt.ylabel("Longueur moyenne du parcours")
    plt.title("Évolution de la performance du Q-learning")
    plt.grid(True)
    plt.tight_layout()

    legend_elements = []
    for index, alpha in enumerate(alphas):
        legend_elements.append(Line2D([0], [0], marker=markers[index], label=f'Alpha = {alpha}'))
    for index, gamma in enumerate(gammas):
        legend_elements.append(Line2D([0], [0], color=colors[index], label=f'Gamma = {gamma}'))
    plt.legend(handles=legend_elements)


    plt.show()


alphas = [0.1, 0.3, 0.5, 0.7]
markers = ['o', 'x', 's', '^']

gammas = [0.7, 0.9, 0.99]
colors = ['r', 'g', 'b']

# comparison(alphas=alphas, gammas=gammas)


def comparison_apf(rows=100, cols=100, nb_training=2500, alpha=0.9, gamma=0.999, min_length=100):
    G = Grid(rows=100, cols=100, proba=0.2)

    print(f'\r Comparaison Q-Learning :      ', end='')
    step_list, reward_list = training(grid=G, num_training=nb_training, stats=True, alpha=alpha, gamma=gamma)

    if step_list[-1] < min_length:
        print(f'\r Redémarrage, longueur insuffisante ({step_list[-1]})')
        comparison_apf(rows, cols, nb_training, alpha, gamma, min_length)
        exit()

    APF = (1, 3, 3, 1)
    print(f'\r Calcul de l\'APF', end='')
    G.apf_add(APF)
    Q_APF = create_Q(G, APF[0], APF[1], APF[2], APF[3])
    print(f'\r Comparaison Q-Learning x APF :      ', end='')
    step_list_, reward_list_ = training(grid=G, num_training=nb_training, stats=True, alpha=alpha, gamma=gamma, Q_learn=Q_APF)

    x = []
    y = []
    z = []
    average_reward = []
    average_reward_ = []
    for i in range(1, nb_training//100):
        x.append(i)
        window = step_list[i * 100 - 50: i * 100 + 51]
        window_ = step_list_[i * 100 - 50: i * 100 + 51]

        average = sum(window) / len(window)
        average_ = sum(window_) / len(window_)

        y.append(average)
        z.append(average_)

        window = reward_list[i * 100 - 50: i * 100 + 51]
        window_ = reward_list_[i * 100 - 50: i * 100 + 51]

        average = sum(window) / len(window)
        average_ = sum(window_) / len(window_)

        average_reward.append(average)
        average_reward_.append(average_)


    plt.plot(x, y, color='r', label='Q-Learning')
    plt.plot(x, z, color='b', label='Q-Learning x APF')


    plt.xlabel("Nombre de centaines d'entrainement")
    plt.ylabel("Longueur moyenne du parcours")
    plt.title("Comparaison Q-Learning vs Q-Learning x APF")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()


    plt.figure()
    plt.plot(average_reward, color='r', label='Q-Learning')
    plt.plot(average_reward_, color='b', label='Q-Learning x APF')


    plt.xlabel("Nombre de centaines d'entrainement")
    plt.ylabel("Somme des récompenses")
    plt.title("Comparaison Q-Learning vs Q-Learning x APF")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()


    app = QApplication(sys.argv)
    window = Window(grid=G, cell_size=10)
    window.show()
    sys.exit(app.exec())

comparison_apf()