class Agent:
    def __init__(self, start):
        self.col = start[1]
        self.row = start[0]

    def move_up(self):
        self.row -= 1
        return

    def move_down(self):
        self.row += 1
        return

    def move_left(self):
        self.col -= 1
        return

    def move_right(self):
        self.col += 1
        return