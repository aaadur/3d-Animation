import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation

# Paramètres du cylindre
radius = 1.0
height = 0.2
num_points = 100

# Création des données pour le cylindre
theta = np.linspace(0, 2 * np.pi, num_points)
z = np.linspace(-height / 2, height / 2, 10)
theta_grid, z_grid = np.meshgrid(theta, z)
x_grid = radius * np.cos(theta_grid)
y_grid = radius * np.sin(theta_grid)

# Initialisation de la figure et des axes 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(-2, 2)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Plateau cylindrique 3D (Utilisez les touches A, Q, L, M, O, P)')

# Création du cylindre
cylinder = ax.plot_surface(x_grid, y_grid, z_grid, color='lightblue', edgecolor='black')

# Variables pour les rotations
angle_x = 0
angle_y = 0
angle_z = 0

# Fonction pour mettre à jour la vue
def update_view():
    ax.view_init(elev=angle_x, azim=angle_z)
    ax.dist = 8
    plt.draw()

# Fonction pour gérer les événements clavier
def on_key(event):
    global angle_x, angle_y, angle_z

    if event.key == 'a':
        angle_x += 5
    elif event.key == 'q':
        angle_x -= 5
    elif event.key == 'l':
        angle_y += 5
    elif event.key == 'm':
        angle_y -= 5
    elif event.key == 'o':
        angle_z += 5
    elif event.key == 'p':
        angle_z -= 5

    update_view()

# Connexion de l'événement clavier
fig.canvas.mpl_connect('key_press_event', on_key)

# Affichage initial
update_view()
plt.tight_layout()
plt.show()
