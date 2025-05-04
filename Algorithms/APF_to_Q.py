def action_to_pos(a, i, j):
    if a == 0:
        return i - 1, j
    elif a == 1:
        return i, j + 1
    elif a == 2:
        return i + 1, j
    elif a == 3:
        return i, j - 1


def create_Q(grid, potentials):

    Q = [[[0, 0, 0, 0] for i in range(grid.cols)] for j in range(grid.rows)]

    for i in range(grid.rows):
        for j in range(grid.cols):
            if not grid.is_empty(i, j) and not grid.is_target(i, j):
                continue
            for a in range(4):
                ni, nj = action_to_pos(a, i, j)
                if (ni, nj) in grid.action_list(i, j):
                    pot = potentials[ni][nj]
                    Q[i][j][a] = 1 / (pot + 1e-6)
                else:
                    Q[i][j][a] = -(grid.rows*grid.cols + 1)
    return Q
