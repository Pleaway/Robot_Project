import random
import sys
from math import inf

from PyQt6.QtWidgets import QApplication

from Game_Engine.grid import Grid
from Game_Engine.window import Window

def argmax(list):
    return list.index(max(list))

alpha = 0.9
gamma = 0.9

epsilon = 0.4

num_episodes = 500

num_training = 100


def choose_action(Q, e, i, j):
    if random.random() < e :
        return random.randint(0, 3)
    else :
        return argmax(Q[i][j])

def action_to_pos(a, i, j):
    if a == 0:
        return (i, j+1)
    elif a == 1:
        return (i+1, j)
    elif a == 2:
        return (i, j-1)
    elif a == 3:
        return (i-1, j)

def step(action, i,j, grid = Grid()):
    if action_to_pos(action, i, j) in grid.action_list(i, j):
        i, j = action_to_pos(action, i, j)[0], action_to_pos(action, i, j)[1]
    return i, j, grid.get_value(i, j)

def training(grid = Grid()):
    target = grid.end
    Q = [[[0, 0, 0, 0] for i in range(grid.cols)] for j in range(grid.rows)]
    for phase in range(num_training):
        state = grid.start

        while state != target:
            action = choose_action(Q,epsilon,state[0], state[1])

            i , j , reward = step(i = state[0], j = state[1], action = action, grid = grid)

            Q[state[0]][state[1]][action] += alpha * (reward + gamma * max(Q[i][j]) - Q[state[0]][state[1]][action])

            state = (i, j)

    #global epsilon
    #epsilon = max(epsilon_min, epsilon * epsilon_decay)

    return Q

def affichage(Q):
    emojie = ["⬆️", "➡️", "⬇️", "⬅️"]

    for i in Q:
        u = ""
        for j in i:
            u += emojie[argmax(j)]
        print(u)

G = Grid(5,5)
Q = training(grid = G)

print(Q)
affichage(Q)
app = QApplication(sys.argv)
window = Window(G, 100)
window.show()
sys.exit(app.exec())