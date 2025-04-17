from PyQt6.QtWidgets import QWidget
# from PyQt6.QtWidgets import QMainWindow, QApplication,
from PyQt6.QtGui import QPainter, QColor, QBrush
from PyQt6.QtCore import Qt
# import time
from Game_Engine.grid import Grid

# from Game_Engine import grid
# from Game_Engine.grid import Grid
from Game_Engine.agent import Agent


def action_to_pos(a, i, j):
    if a == 0:
        return i - 1, j
    elif a == 1:
        return i, j + 1
    elif a == 2:
        return i + 1, j
    elif a == 3:
        return i, j - 1


def argmax(list):
    return list.index(max(list))


class Window(QWidget):
    '''Q : Q matrix for Q learning; grid : Grid object; APF : tuple, APF parameters (set to False to not use APF);
    cell_size : int'''
    def __init__(self, grid=Grid(), cell_size=20):
        super().__init__()

        self.setWindowTitle("Robot IA")
        self.grid = grid
        self.agent = Agent(start=grid.start)
        self.rows = grid.rows
        self.cols = grid.cols
        self.cell_size = cell_size
        self.setFixedSize(self.cols * cell_size, self.rows * cell_size)
        self.setStyleSheet("background-color: white;")
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.grid.apf_param:
            self.draw_potential_field(painter)
        self.draw_obstacles(painter)
        self.draw_grid(painter)
        if self.grid.Q is not None:
            self.draw_Qlearn_path(painter)
        self.draw_agent(painter)

    def draw_grid(self, painter):
        painter.setPen(Qt.GlobalColor.black)
        for row in range(self.grid.rows + 1):
            painter.drawLine(0, row * self.cell_size, self.width(), row * self.cell_size)
        for col in range(self.grid.cols + 1):
            painter.drawLine(col * self.cell_size, 0, col * self.cell_size, self.height())

    def draw_obstacles(self, painter):
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                if not self.grid.is_empty(row, col):
                    painter.setBrush(QBrush(Qt.GlobalColor.black, Qt.BrushStyle.SolidPattern))
                    painter.setPen(Qt.GlobalColor.black)
                    painter.drawRect(row * self.cell_size, col * self.cell_size, self.cell_size, self.cell_size)
                elif self.grid.is_start(row, col):
                    painter.setBrush(QBrush(Qt.GlobalColor.green, Qt.BrushStyle.SolidPattern))
                    painter.setPen(Qt.GlobalColor.green)
                    painter.drawRect(row * self.cell_size, col * self.cell_size, self.cell_size, self.cell_size)
                elif self.grid.is_target(row, col):
                    painter.setBrush(QBrush(Qt.GlobalColor.red, Qt.BrushStyle.SolidPattern))
                    painter.setPen(Qt.GlobalColor.red)
                    painter.drawRect(row * self.cell_size, col * self.cell_size, self.cell_size, self.cell_size)

    def draw_agent(self, painter):
        painter.setBrush(QBrush(Qt.GlobalColor.blue, Qt.BrushStyle.SolidPattern))
        painter.setPen(Qt.GlobalColor.blue)
        row = self.agent.row
        col = self.agent.col
        painter.drawRect(
            row * self.cell_size + self.cell_size//4, col * self.cell_size + self.cell_size//4,
            self.cell_size//2, self.cell_size//2
        )

    def potential_to_color(self, value, min_val, max_val):
        if value == float("inf"):
            return QColor(0, 0, 0)  # noir pour l'infini (obstacles)

        # Normalisation [0,1]
        normalized = (value - min_val) / (max_val - min_val)
        # normalized = max(0.0, min(1.0, normalized))  # clamp

        red = int(255 * (1 - normalized))
        green = int(255 * (1 - normalized))
        blue = 255

        return QColor(red, green, blue)

    def draw_potential_field(self, painter):
        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                color = self.potential_to_color(self.grid.potentials[i][j], self.grid.min_val, self.grid.max_val)
                painter.setBrush(QBrush(color, Qt.BrushStyle.SolidPattern))
                painter.setPen(Qt.GlobalColor.transparent)
                painter.drawRect(i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size)

    def draw_Qlearn_path(self, painter, color=(240, 120, 50, 255)):
        painter.setBrush(QBrush(QColor(*color), Qt.BrushStyle.SolidPattern))
        painter.setPen(QColor(*color))
        state = self.grid.start
        row = state[0]
        col = state[1]
        target = self.grid.end
        while state != target:
            print(state)
            painter.drawRect(
                row * self.cell_size + self.cell_size//5, col * self.cell_size + self.cell_size//5,
                self.cell_size//5, self.cell_size//5
            )
            data = argmax(self.grid.Q[state[0]][state[1]])
            new_state = action_to_pos(data, state[0], state[1])
            row = new_state[0]
            col = new_state[1]
            state = new_state
        self.agent.row = target[0]
        self.agent.col = target[1]
