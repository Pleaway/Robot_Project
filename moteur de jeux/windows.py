from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPainter, QColor, QKeyEvent
from PyQt6.QtCore import Qt
from grille import Grille
from robot import Robot
import sys

class GameWindow(QWidget):
    def __init__(self, rows=10, cols=10, cell_size=50):
        super().__init__()
        self.grid = Grille(rows, cols)
        self.cube = Robot(self.grid)
        self.cell_size = cell_size
        self.setWindowTitle("Jeu du Cube")
        self.setFixedSize(cols * cell_size, rows * cell_size)

        self.cube.add_obstacle(3, 3)
        self.cube.add_obstacle(5, 5)

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_grid(painter)
        self.draw_obstacles(painter)
        self.draw_cube(painter)

    def draw_grid(self, painter):
        painter.setPen(QColor(200, 200, 200))
        for row in range(self.grid.rows + 1):
            painter.drawLine(0, row * self.cell_size, self.width(), row * self.cell_size)
        for col in range(self.grid.cols + 1):
            painter.drawLine(col * self.cell_size, 0, col * self.cell_size, self.height())

    def draw_obstacles(self, painter):
        painter.setBrush(QColor(0, 0, 255))
        for x, y in self.cube.obstacles:
            painter.drawRect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)

    def draw_cube(self, painter):
        painter.setBrush(QColor(255, 0, 0))
        x = self.cube.x * self.cell_size
        y = self.cube.y * self.cell_size
        painter.drawRect(x, y, self.cell_size, self.cell_size)

    def keyPressEvent(self, event: QKeyEvent):
        key_map = {
            Qt.Key.Key_Left: (-1, 0),
            Qt.Key.Key_Right: (1, 0),
            Qt.Key.Key_Up: (0, -1),
            Qt.Key.Key_Down: (0, 1)
        }
        if event.key() in key_map:
            dx, dy = key_map[event.key()]
            self.cube.move(dx, dy)
            self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow(rows=10, cols=10, cell_size=50)
    window.show()
    sys.exit(app.exec())