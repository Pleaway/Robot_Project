from Algorithms.Q_learning import training
from Game_Engine.grid import Grid
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def comparison(rows=100, cols=100, nb_training=25000, alphas=[0.1], gammas=[0.9], min_length=75):
    G = Grid(rows=100, cols=100, proba=0.2)

    for alpha in alphas:
        for gamma in gammas:
            print(f'\r Comparaison {alphas.index(alpha)*len(gammas) + gammas.index(gamma) + 1}/{len(alphas)*len(gammas)} :      ', end='')

            Q, step_list = training(grid=G, num_training=nb_training, stats=True, alpha=alpha, gamma=gamma)

            if step_list[-1] < min_length:
                print(f'\r Redémarrage, longueur insuffisante ({step_list[-1]})')
                comparison(rows, cols, nb_training, alphas, gammas, min_length)

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

comparison(alphas=alphas, gammas=gammas)