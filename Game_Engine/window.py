from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor, QBrush
from PyQt6.QtCore import Qt
from Game_Engine.grid import Grid
from Game_Engine.agent import Agent
import sys

class Window(QWidget):
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
        self.draw_potential_field(painter)
        self.draw_obstacles(painter)
        self.draw_agent(painter)
        self.draw_grid(painter)

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

    def potential_to_color(self, value, min_val, max_val):
        if value == float('inf'):
            return QColor(0, 0, 0)  # noir pour l'infini (obstacles)

        # Normalisation [0,1]
        normalized = (value - min_val) / (max_val - min_val + 1e-9)
        normalized = max(0.0, min(1.0, normalized))  # clamp

        red = int(255 * (1 - normalized))
        green = int(255 * (1 - normalized))
        blue = 255

        return QColor(red, green, blue)

    def draw_potential_field(self, painter):
        potentials = []
        for row in range(self.grid.rows):
            row_pot = []
            for col in range(self.grid.cols):
                if self.grid.is_empty(row, col) or self.grid.is_target(row, col):
                    pot = self.grid.total_potential(row, col)
                else:
                    pot = float('inf')
                row_pot.append(pot)
            potentials.append(row_pot)

        # Trouver min et max (hors inf)
        flat = [p for row in potentials for p in row if p != float('inf')]
        min_val = min(flat)
        max_val = max(flat)

        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                color = self.potential_to_color(potentials[i][j], min_val, max_val)
                painter.setBrush(QBrush(color, Qt.BrushStyle.SolidPattern))
                painter.setPen(Qt.GlobalColor.transparent)
                painter.drawRect(i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())



