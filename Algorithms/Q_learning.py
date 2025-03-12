import random
import sys
from math import inf

from PyQt6.QtWidgets import QApplication

from Game_Engine.grid import Grid
from Game_Engine.window import Window


def argmax(list):
    return list.index(max(list))

alpha = 0.1
gamma = 0.9

epsilon = 1
epsilon_min = 0.01
epsilon_decay = 0.995


num_training = 1000


def choose_action(Q, e, i, j):
    if random.random() < e :
        return random.randint(0, 3)
    else :
        return argmax(Q[i][j])

def action_to_pos(a, i, j):
    if a == 0:
        return (i-1, j)
    elif a == 1:
        return (i, j+1)
    elif a == 2:
        return (i+1, j)
    elif a == 3:
        return (i, j-1)

def step(action, i,j, grid = Grid()):
    if action_to_pos(action, i, j) in grid.action_list(i, j):
        i, j = action_to_pos(action, i, j)[0], action_to_pos(action, i, j)[1]

    return i, j, grid.get_value(i, j)

def training(grid = Grid()):
    target = grid.end
    Q = [[[0, 0, 0, 0] for i in range(grid.cols)] for j in range(grid.rows)]
    global epsilon
    for phase in range(num_training):
        state = grid.start

        while state != target:
            action = choose_action(Q,epsilon,state[0], state[1])

            i , j , reward = step(i = state[0], j = state[1], action = action, grid = grid)

            Q[state[0]][state[1]][action] += alpha * (reward + gamma * max(Q[i][j]) - Q[state[0]][state[1]][action])

            state = (i, j)


        epsilon = max(epsilon_min, epsilon * epsilon_decay)

    return Q

def affichage(Q, grid):
    emojie = ["⬅️",  "⬇️", "➡️", "⬆️", "⛔"]
    for i in range(grid.rows):
        row_display = ""
        for j in range(grid.cols):
            if not grid.is_empty(j, i):
                row_display += "⛔ "
            elif grid.is_target(j, i):
                row_display += "🚩 "
            else:
                row_display += emojie[argmax(Q[j][i])] + " "
        print(row_display)

G = Grid(6,6)
Q = training(grid = G)

print(Q)
affichage(Q, G)
app = QApplication(sys.argv)
window = Window(G, 50)
window.show()
sys.exit(app.exec())