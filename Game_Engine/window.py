from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor, QBrush
from PyQt6.QtCore import Qt
import time

from Game_Engine import grid
from Game_Engine.grid import Grid
from Game_Engine.agent import Agent
import sys


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
    def __init__(self, Q, grid=Grid(), cell_size=20):
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
        self.Q = Q


    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_obstacles(painter)
        self.draw_grid(painter)
        self.draw_path(painter)
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
                    painter.drawRect(row*self.cell_size, col*self.cell_size, self.cell_size, self.cell_size)
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
        painter.drawRect(row*self.cell_size+10, col*self.cell_size+10, self.cell_size-20, self.cell_size-20)

    def draw_path(self, painter):
        painter.setBrush(QBrush(Qt.GlobalColor.blue, Qt.BrushStyle.SolidPattern))
        painter.setPen(Qt.GlobalColor.blue)
        state = self.grid.start
        row = state[0]
        col = state[1]
        target = self.grid.end
        while state != target:
            print(state)
            painter.drawRect(row * self.cell_size + 15, col * self.cell_size + 15, self.cell_size - 30, self.cell_size - 30)
            data = argmax(self.Q[state[0]][state[1]])
            new_state = action_to_pos(data, state[0], state[1])
            row = new_state[0]
            col = new_state[1]
            state = new_state
        self.agent.row = target[0]
        self.agent.col = target[1]










if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())



