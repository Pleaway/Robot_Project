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

# Set APF parameters :  (crit_dist_att, crit_dist_rep, w_att, w_rep)
APF = (2, 2, 3, 1)

# Create and display window
app = QApplication(sys.argv)
window = Window(Q=Q, grid=G, cell_size=35, APF=APF)
window.show()
sys.exit(app.exec())
