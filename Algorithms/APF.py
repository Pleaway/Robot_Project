from math import sqrt
import numpy as np


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
#    else:
#        return inf
# À quoi sert ce troisième cas ?


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


def norm(vector):
    '''Calcule la norme euclidienne, une autre norme de R² serait-elle + pertinente?'''
    return sqrt(vector[0]**2 + vector[1]**2)


def attractive_gradient(grid, i_q, j_q, critical_distance, weight):
    q = (i_q, j_q)
    d_c = critical_distance
    w = weight
    q0 = grid.end
    d = grid.distance(q, q0)
    if d <= d_c:
        return tuple(w * (np.array(q) - np.array(q0)))
    elif d > d_c:
        return tuple(((d_c*w)/d) * (np.array(q) - np.array(q0)))


def repulsive_gradient(grid, i_q, j_q, critical_distance, weight):
    d_c = critical_distance
    w = weight
    d = grid.closest_obstacle_distance(i_q, j_q)
    if d <= d_c:
        return (w / d**2) * ((1 / d_c) - (1 / d)) * grid.grad_closest_obs_dist(i_q, j_q)
    elif d > d_c:
        return 0


def gradient(grid, i_q, j_q, crit_dist_att=1, crit_dist_rep=1, w_att=1, w_rep=40):
    rep = repulsive_gradient(grid, i_q, j_q, crit_dist_rep, w_rep)
    attr = attractive_gradient(grid, i_q, j_q, crit_dist_att, w_att)
    return rep + attr


def gradient_descent(q_start, threshold, alpha, grid, apf_param):
    path = [q_start]
    i = 0
    while norm(gradient(total_potential(grid, path[i][0], path[i][1], *apf_param))) > threshold:
        q = path[i] - alpha*gradient(total_potential(grid, path[i][0], path[i][1], *apf_param))
        path.append(q)
        i += 1

    return path
