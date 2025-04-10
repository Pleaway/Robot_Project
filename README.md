# Robot_Project
Système de Navigation Robotique Adaptatif Utilisant APF (Artificial Potential Field) et Apprentissage par Renforcement (en l'occurrence Q learning).


Le robot se déplace sur une grille, selon 4 directions; il a un point de départ et un objectif; il y a des obstacles sur la grille qu'il ne peut pas traverser.


## Usage rapide

Voir répertoire scripts:

### Exemple : main.py
Création d'une grille, puis de la matrice Q pour le Q learning, affichage de la grille (avec les potentiels définis par les méthodes APF pour chaque case) et du chemin trouvé par le Q learning dans une fenêtre séparée.




## Dépendances

Ce projet nécessite les modules Python suivants:

- math
- random
- PyQt6
- sys


**À faire** : Vérifier la liste et les versions des modules, ajouter un `requirements.txt` pour pouvoir les installer facilement avec pip.