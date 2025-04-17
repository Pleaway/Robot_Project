import sys

from PyQt6.QtWidgets import QApplication

from Algorithms.Q_learning import affichage, training
from Game_Engine.grid import Grid
from Game_Engine.window import Window


# Set APF parameters :  (crit_dist_att, crit_dist_rep, w_att, w_rep)
APF = (1, 3, 30, 20)

# Grid parameters : set grid size, APF parameters
G = Grid(rows=8, cols=8, apf_param=APF)

# Create the Q matrix with Q learning
Q = training(grid=G)

print(Q)
# Display Q matrix in terminal with emojis
affichage(Q, G)


# Create and display window
app = QApplication(sys.argv)
window = Window(grid=G, cell_size=80)
window.show()
sys.exit(app.exec())
