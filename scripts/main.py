import sys

from PyQt6.QtWidgets import QApplication

from Algorithms.Q_learning import affichage, training
from Algorithms.APF import create_Q
from Game_Engine.grid import Grid
from Game_Engine.window import Window


# Set APF parameters :  (crit_dist_att, crit_dist_rep, w_att, w_rep)
APF = (1, 3, 3, 1)

# Grid parameters : set grid size, APF parameters
G = Grid(rows=20, cols=20, apf_param=APF, proba=0.2)

#la matrice Q de l'APF
Q_APF = create_Q(G)

# Create the Q matrix with Q learning (faut mettre None dans Q_learn pour ne pas avoir la fusion)
Q = training(grid=G, Q_learn = Q_APF)

print(Q)
# Display Q matrix in terminal with emojis
affichage(Q, G)


# Create and display window
app = QApplication(sys.argv)
window = Window(grid=G, cell_size=35)
window.show()
sys.exit(app.exec())
