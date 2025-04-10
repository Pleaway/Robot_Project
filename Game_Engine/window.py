from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor, QBrush
from PyQt6.QtCore import Qt
import time
from Game_Engine.grid import Grid
from Algorithms.APF import build_potentials_list

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
    def __init__(self, Q=None, grid=Grid(), cell_size=20, APF=False):
        super().__init__()
        self.apf_status = APF
        self.setWindowTitle("Robot IA")
        self.grid = grid
        self.agent = Agent(start=grid.start)
        self.rows = grid.rows
        self.cols = grid.cols
        self.cell_size = cell_size
        self.setFixedSize(self.cols * cell_size, self.rows * cell_size)
        self.setStyleSheet("background-color: white;")
        self.update()
        self.Q = Q

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.apf_status:
            self.draw_potential_field(painter)
        self.draw_obstacles(painter)
        self.draw_grid(painter)
        if self.Q is not None:
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
            row * self.cell_size + 10, col * self.cell_size + 10, self.cell_size - 20, self.cell_size - 20
        )

    def potential_to_color(self, value, min_val, max_val):
        if value == float("inf"):
            return QColor(0, 0, 0)  # noir pour l'infini (obstacles)

        # Normalisation [0,1]
        normalized = (value - min_val) / (max_val - min_val + 1e-9)
        normalized = max(0.0, min(1.0, normalized))  # clamp

        red = int(255 * (1 - normalized))
        green = int(255 * (1 - normalized))
        blue = 255

        return QColor(red, green, blue)

    def draw_potential_field(self, painter):
        potentials, min_val, max_val = build_potentials_list(self.grid)
        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                color = self.potential_to_color(potentials[i][j], min_val, max_val)
                painter.setBrush(QBrush(color, Qt.BrushStyle.SolidPattern))
                painter.setPen(Qt.GlobalColor.transparent)
                painter.drawRect(i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size)

    def draw_Qlearn_path(self, painter, color=(50, 150, 50, 255)):
        painter.setBrush(QBrush(QColor(color[0], color[1], color[2], color[3]), Qt.BrushStyle.SolidPattern))
        painter.setPen(QColor(color[0], color[1], color[2], color[3]))
        state = self.grid.start
        row = state[0]
        col = state[1]
        target = self.grid.end
        while state != target:
            print(state)
            painter.drawRect(
                row * self.cell_size + 15, col * self.cell_size + 15, self.cell_size - 30, self.cell_size - 30
            )
            data = argmax(self.Q[state[0]][state[1]])
            new_state = action_to_pos(data, state[0], state[1])
            row = new_state[0]
            col = new_state[1]
            state = new_state
        self.agent.row = target[0]
        self.agent.col = target[1]
