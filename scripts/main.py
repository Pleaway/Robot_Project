import sys

from PyQt6.QtWidgets import QApplication

from Algorithms.Q_learning import affichage, training
from Algorithms.APF_to_Q import create_Q
from Game_Engine.grid import Grid
from Game_Engine.window import Window


# Set APF parameters :  (crit_dist_att, crit_dist_rep, w_att, w_rep)
APF = (1, 3, 3, 1)

# Grid parameters : set grid size, APF parameters
G = Grid(rows=20, cols=20, apf_param=APF, proba=0.2)
init_Q_APF = create_Q(G, G.potentials)

# Create the Q matrix with Q learning
Q = training(grid=G)
print('1er entrainement ok')

Q_APF = training(grid=G, init_matrix=init_Q_APF)
print('2eme entrainement ok')


# Display Q matrix in terminal with emojis
affichage(Q_APF, G)


# Create and display window
app = QApplication(sys.argv)
window = Window(grid=G, cell_size=35)
window.show()
sys.exit(app.exec())
