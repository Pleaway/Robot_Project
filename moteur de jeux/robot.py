class Robot:
    def __init__(self, grid):
        self.grid = grid
        self.x = 0  # Position colonne
        self.y = 0  # Position ligne
        self.obstacles = set()

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < self.grid.cols and 0 <= new_y < self.grid.rows and (new_x, new_y) not in self.obstacles:
            self.x = new_x
            self.y = new_y

    def add_obstacle(self, x, y):
        if 0 <= x < self.grid.cols and 0 <= y < self.grid.rows:
            self.obstacles.add((x, y))