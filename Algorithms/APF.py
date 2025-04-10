from math import inf


def attractive_potential(grid, i_q, j_q, critical_distance=1, weight=1):
    q = (i_q, j_q)
    d_c = critical_distance
    w = weight
    q0 = grid.end
    d = grid.distance(q, q0)
    if d <= d_c:
        return (w / 2) * d**2
    else:
        return d_c * w * d - (w / 2) * d_c**2


def repulsive_potential(grid, i_q, j_q, critical_distance=1, weight=1):
    d_c = critical_distance
    w = weight
    d = grid.closest_obstacle_distance(i_q, j_q)
    if d <= d_c:
        return (w / 2) * ((1 / d - 1 / d_c) ** 2)
    elif d >= d_c:
        return 0
    else:
        return inf


def total_potential(grid, i_q, j_q, critical_distance_att=1, critical_distance_rep=1, weight_att=1, weight_rep=1):
    attractive = attractive_potential(grid, i_q, j_q, critical_distance_att, weight_att)
    repulsive = repulsive_potential(grid, i_q, j_q, 3, 40)
    return attractive + repulsive


def build_potentials_list(grid):
    potentials = []
    for row in range(grid.rows):
        row_pot = []
        for col in range(grid.cols):
            if grid.is_empty(row, col) or grid.is_target(row, col):
                pot = total_potential(grid, row, col)
            else:
                pot = float("inf")
            row_pot.append(pot)
        potentials.append(row_pot)
    # Trouver min et max (hors inf)
    flat = [p for row in potentials for p in row if p != float("inf")]
    min_val = min(flat)
    max_val = max(flat)

    return potentials, min_val, max_val
