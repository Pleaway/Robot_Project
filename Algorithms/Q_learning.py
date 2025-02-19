import random
import sys
from math import inf

from PyQt6.QtWidgets import QApplication

from Game_Engine.grid import Grid
from Game_Engine.window import Window


def argmax(lst):
    max_value = max(lst)
    return random.choice([i for i, x in enumerate(lst) if x == max_value])


alpha = 0.1  # Si trop haut apprentissage instable (Q mis à jour trop souvent), et difficultés à converger vers une solution
gamma = 0.9

epsilon = 0.4
epsilon_min = 0.01
epsilon_decay = 0.99

num_training = 100


def choose_action(Q, e, i, j):
    if random.random() < e:
        return random.randint(0, 3)
    return argmax(Q[i][j])


def action_to_pos(a, i, j):
    moves = [(i, j + 1), (i + 1, j), (i, j - 1), (i - 1, j)]
    return moves[a]


def step(action, i, j, grid):
    next_pos = action_to_pos(action, i, j)
    if next_pos in grid.action_list(i, j):
        i, j = next_pos
    return i, j, grid.get_value(i, j)


def training(grid):
    Q = [[[0, 0, 0, 0] for _ in range(grid.cols)] for _ in range(grid.rows)]

    global epsilon
    for phase in range(num_training):
        state = grid.start

        while state != grid.end:
            action = choose_action(Q, epsilon, state[0], state[1])
            i, j, reward = step(action, state[0], state[1], grid)

            Q[state[0]][state[1]][action] += alpha * (reward + gamma * max(Q[i][j]) - Q[state[0]][state[1]][action])
            state = (i, j)

        # Réduction d'epsilon après chaque épisode (encore pour la convergence), quand on réduit epsilon, on exploite plus les solutions trouvées jusqu'alors et on se rapproche donc de la bonne solution
        epsilon = max(epsilon_min, epsilon * epsilon_decay)

    return Q


def affichage(Q):
    emojie = ["⬆️", "➡️", "⬇️", "⬅️"]
    for row in Q:
        print("".join(emojie[argmax(cell)] for cell in row))


G = Grid(5, 5)
Q = training(G)

affichage(Q)

app = QApplication(sys.argv)
window = Window(G, 100)
window.show()
sys.exit(app.exec())
