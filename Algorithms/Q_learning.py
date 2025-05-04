import random
from Game_Engine.grid import Grid


def argmax(list):
    return list.index(max(list))

def choose_action(Q, e, i, j):
    if random.random() < e:
        return random.randint(0, 3)
    else:
        return argmax(Q[i][j])


def action_to_pos(a, i, j):
    if a == 0:
        return i - 1, j
    elif a == 1:
        return i, j + 1
    elif a == 2:
        return i + 1, j
    elif a == 3:
        return i, j - 1


def step(action, i, j, grid=Grid()):
    if action_to_pos(action, i, j) in grid.action_list(i, j):
        i, j = action_to_pos(action, i, j)[0], action_to_pos(action, i, j)[1]

    return i, j, grid.get_value(i, j)


def training(grid=Grid(), num_training=10000, alpha=0.1, gamma=0.9, epsilon=1, epsilon_min=0, epsilon_decay=0.995, stats=False):
    target = grid.end
    Q = [[[0, 0, 0, 0] for i in range(grid.cols)] for j in range(grid.rows)]
    length_list = []
    for phase in range(num_training):
        state = grid.start
        steps = 0

        while state != target:
            action = choose_action(Q, epsilon, state[0], state[1])

            i, j, reward = step(i=state[0], j=state[1], action=action, grid=grid)

            Q[state[0]][state[1]][action] += alpha * (reward + gamma * max(Q[i][j]) - Q[state[0]][state[1]][action])

            state = (i, j)
            steps+=1

        epsilon = max(epsilon_min, epsilon * epsilon_decay)

        if stats:
            length_list.append(steps)
            if phase % (num_training/100) == 0:
                if round(phase/num_training*100, 1) < 11:
                    print('\b'*5, end='')
                else:
                    print('\b'*6, end='')
                print(round(phase/num_training*100, 1), "%", end='')
    print('\r 100 %', end='')


    grid.Q = Q
    if stats:
        return Q, length_list
    else :
        return Q


def affichage(Q, grid):
    emojie = ["⬅️", "⬇️", "➡️", "⬆️", "⛔"]
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

# Ne devrait visiblement pas être là ? Peut-être un reste d'un brouillon pour window?
# def draw_path(self, painter, Q):
#     painter.setPen(Qt.GlobalColor.lightblue)
#     pass
