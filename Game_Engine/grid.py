from random import random, randint
from math import sqrt, inf
from Algorithms.APF import build_potentials_list


class Grid:
    def __init__(self, rows=50, cols=50, proba=0.2, apf_param=False, Q=None):
        ''' Arguments ---
            rows, cols : nb of rows/cols ;
            proba : probability of obstacles if no grid given ;
            apf_param : tuple  (crit_dist_att, crit_dist_rep, w_att, w_rep) if APF used or False otherwise;
            Q : Q matrix generated from Q learning'''
        self.rows = rows
        self.cols = cols
        self.proba = proba
        self.grid = [[-1 for i in range(cols)] for j in range(rows)]
        self.init_grid()
        self.Q = Q
        self.apf_param = apf_param
        if apf_param:
            self.potentials, self.min_val, self.max_val = build_potentials_list(self, *apf_param)

    def init_obstacles(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if random() < self.proba:
                    self.grid[i][j] = -(self.rows*self.cols + 1)

    def init_grid(self):
        self.init_obstacles()
        start_x, start_y = randint(0, self.rows - 1), randint(0, self.cols - 1)
        end_x, end_y = start_x, start_y
        while end_x == start_x and end_y == start_y:
            end_x, end_y = randint(0, self.rows - 1), randint(0, self.cols - 1)
        self.grid[start_x][start_y] = -1
        self.grid[end_x][end_y] = 100
        self.start = (start_x, start_y)
        self.end = (end_x, end_y)

    def is_empty(self, i, j):
        return self.grid[i][j] != -(self.cols*self.rows + 1)

    def is_start(self, i, j):
        return i == self.start[0] and j == self.start[1]

    def is_target(self, i, j):
        return i == self.end[0] and j == self.end[1]

    def get_value(self, i, j):
        return self.grid[i][j]

    def action_list(self, i, j):
        actions = []
        if self.cols - 1 > i:
            actions.append((i+1, j))
        if i > 0:
            actions.append((i-1, j))
        if self.rows - 1 > j:
            actions.append((i, j+1))
        if j > 0:
            actions.append((i, j-1))
        return actions

    def __str__(self):
        text = ''
        for i in self.grid:
            for j in i:
                text += str(j) + " "
            text += "\n"
        return text

    def distance(self, q1, q2):
        return sqrt((q1[0]-q2[0])**2 + (q1[1]-q2[1])**2)

    def closest_obstacle_distance(self, i_q, j_q):
        q = (i_q, j_q)
        min_dist = inf
        for i in range(self.rows):
            for j in range(self.cols):
                if not self.is_empty(i, j) and not self.is_target(i, j):
                    d = self.distance(q, (i, j))
                    if d < min_dist:
                        min_dist = d
        return min_dist
