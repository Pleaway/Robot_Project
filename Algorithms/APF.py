
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
