def action_to_pos(a, i, j):
    if a == 0:
        return i - 1, j
    elif a == 1:
        return i, j + 1
    elif a == 2:
        return i + 1, j
    elif a == 3:
        return i, j - 1

def attractive_potential(grid, i_q, j_q, critical_distance, weight):
    q = (i_q, j_q)
    d_c = critical_distance
    w = weight
    q0 = grid.end
    d = grid.distance(q, q0)
    if d <= d_c:
        return (w / 2) * d**2
    else:
        return d_c * w * d - (w / 2) * d_c**2


def repulsive_potential(grid, i_q, j_q, critical_distance, weight):
    d_c = critical_distance
    w = weight
    d = grid.closest_obstacle_distance(i_q, j_q)
    if d <= d_c:
        return (w / 2) * ((1 / d - 1 / d_c) ** 2)
    elif d > d_c:
        return 0


def total_potential(grid, i_q, j_q, crit_dist_att=1, crit_dist_rep=1, w_att=1, w_rep=40):
    attractive = attractive_potential(grid, i_q, j_q, crit_dist_att, w_att)
    repulsive = repulsive_potential(grid, i_q, j_q, crit_dist_rep, w_rep)
    return attractive + repulsive


def build_potentials_list(grid, crit_dist_att=1, crit_dist_rep=1, w_att=10, w_rep=1):
    potentials = []
    for row in range(grid.rows):
        row_pot = []
        for col in range(grid.cols):
            if grid.is_empty(row, col) or grid.is_target(row, col):
                pot = total_potential(grid, row, col, crit_dist_att, crit_dist_rep, w_att, w_rep)
            else:
                pot = float("inf")
            row_pot.append(pot)
        potentials.append(row_pot)
    # Trouver min et max (hors inf)
    flat = [p for row in potentials for p in row if p != float("inf")]
    min_val = min(flat)
    max_val = max(flat)

    return potentials, min_val, max_val


def find_adjacent_lowest(grid, i, j):
    neighbours = grid.action_list(i, j)
    pot_list = []
    for pos in neighbours:
        pot_list.append(grid.potentials[pos[0]][pos[1]])
    min_pot = min(pot_list)
    return min_pot, neighbours[pot_list.index(min_pot)]

def create_Q(grid, crit_dist_att=1, crit_dist_rep=1, w_att=10, w_rep=1):
    potentials, min_pot, max_pot = build_potentials_list(grid, crit_dist_att, crit_dist_rep, w_att, w_rep)
    #grid.potentials = potentials
    Q = [[[0, 0, 0, 0] for i in range(grid.cols)] for j in range(grid.rows)]
    for i in range(grid.rows):
        for j in range(grid.cols):
            if not grid.is_empty(i, j) and not grid.is_target(i, j):
                continue
            for a in range(4):
                ni, nj = action_to_pos(a, i, j)
                if (ni, nj) in grid.action_list(i, j):
                    pot = potentials[ni][nj]
                    range_pot = max(max_pot - min_pot, 1e-3)
                    norm_val = (max_pot - pot) / range_pot
                    norm_val = max(0.0, min(1.0, norm_val))
                    Q[i][j][a] = norm_val
                else:
                    Q[i][j][a] = -(grid.rows*grid.cols + 1)
    return Q
