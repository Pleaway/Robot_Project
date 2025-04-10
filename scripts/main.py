import sys

from PyQt6.QtWidgets import QApplication

from Algorithms.Q_learning import affichage, training
from Game_Engine.grid import Grid
from Game_Engine.window import Window


G = Grid(20, 20)
Q = training(grid=G)

print(Q)
affichage(Q, G)
app = QApplication(sys.argv)
window = Window(Q, G, 35)
window.show()
sys.exit(app.exec())
