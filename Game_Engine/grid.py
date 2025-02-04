from random import random, randint



class Grid:
    def __init__(self, rows=50, cols=50, proba=0.1):
        self.rows = rows
        self.cols = cols
        self.proba = proba
        self.grid = [[0 for i in range(cols)] for j in range(rows)]
        self.init_grid()

    def init_obstacles(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if random() < self.proba:
                    self.grid[i][j] = 1

    def init_grid(self):
        self.init_obstacles()
        start_x, start_y = randint(0, self.rows - 1), randint(0, self.cols - 1)
        end_x, end_y = start_x, start_y
        while end_x == start_x and end_y == start_y:
            end_x, end_y = randint(0, self.rows - 1), randint(0, self.cols - 1)
        self.grid[start_x][start_y] = 2
        self.grid[end_x][end_y] = 3
        self.start = (start_x, start_y)
        self.end = (end_x, end_y)
    
    def is_empty(self, i, j):
        return (self.grid[i][j] == 0 or self.grid[i][j] == 2 or self.grid[i][j] == 3)

    def is_start(self, i, j):
        return self.grid[i][j] == 2

    def is_target(self, i, j):
        return self.grid[i][j] == 3

    def __str__(self):
        text = ''
        for i in self.grid:
            for j in i:
                text += str(j) + " "
            text += "\n"
        return text

print(Grid())