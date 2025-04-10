import sys

from PyQt6.QtWidgets import QApplication

from Algorithms.Q_learning import affichage, training
from Game_Engine.grid import Grid
from Game_Engine.window import Window


# Grid parameters : set grid size
G = Grid(20, 20)

# Create the Q matrix with Q learning
Q = training(grid=G)

print(Q)
# Display Q matrix in terminal with emojis
affichage(Q, G)

# Create and display window
app = QApplication(sys.argv)
window = Window(Q, G, 35)
window.show()
sys.exit(app.exec())
