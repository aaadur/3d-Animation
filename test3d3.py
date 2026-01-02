import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from tkinter import ttk
import threading
import mouse
from time import sleep

# Paramètres de l'aile delta
length = 2.0   # Longueur de l'aile (axe Y)
width = 1.5    # Largeur maximale de l'aile (axe X)
thickness = 0.1  # Épaisseur de l'aile (axe Z)

# Coordonnées des 3 sommets de l'aile delta (triangle isocèle)
# Pointe avant (Y positif)
tip_x, tip_y, tip_z = 0, length/2, 0
# Base arrière (deux points en Y négatif)
base_x = [-width/2, width/2]
base_y = [-length/2, -length/2]
base_z = [0, 0]

# Coordonnées des sommets (pour une aile plate)
x_wing = np.array([tip_x, base_x[0], base_x[1]])
y_wing = np.array([tip_y, base_y[0], base_y[1]])
z_wing = np.array([tip_z, base_z[0], base_z[1]])

# Variables globales pour les angles
angle_x, angle_y, angle_z = 0, 0, 0

# Fonction pour appliquer les rotations
def rotate_points(points, angle_x, angle_y, angle_z):
    x, y, z = points
    # Rotation autour de l'axe X
    y_rot = y * np.cos(np.radians(angle_x)) - z * np.sin(np.radians(angle_x))
    z_rot = y * np.sin(np.radians(angle_x)) + z * np.cos(np.radians(angle_x))
    x_new, y_new, z_new = x, y_rot, z_rot

    # Rotation autour de l'axe Y
    x_rot = x_new * np.cos(np.radians(angle_y)) + z_new * np.sin(np.radians(angle_y))
    z_rot = -x_new * np.sin(np.radians(angle_y)) + z_new * np.cos(np.radians(angle_y))
    x_new, y_new, z_new = x_rot, y_new, z_rot

    # Rotation autour de l'axe Z
    x_rot = x_new * np.cos(np.radians(angle_z)) - y_new * np.sin(np.radians(angle_z))
    y_rot = x_new * np.sin(np.radians(angle_z)) + y_new * np.cos(np.radians(angle_z))
    x_new, y_new, z_new = x_rot, y_rot, z_new

    return x_new, y_new, z_new

# Fonction pour créer la figure 3D
def create_figure():
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-1, 1)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Aile Delta 3D')
    return fig, ax

# Fonction pour mettre à jour l'aile delta
def update_wing(ax, angle_x, angle_y, angle_z):
    ax.cla()
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-1, 1)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Aile Delta 3D')

    # Rotation des sommets
    tip_rot = rotate_points((tip_x, tip_y, tip_z), angle_x, angle_y, angle_z)
    base_rot = [rotate_points((x, y, z), angle_x, angle_y, angle_z) for x, y, z in zip(base_x, base_y, base_z)]

    # Coordonnées après rotation
    x_rot = np.array([tip_rot[0], base_rot[0][0], base_rot[1][0]])
    y_rot = np.array([tip_rot[1], base_rot[0][1], base_rot[1][1]])
    z_rot = np.array([tip_rot[2], base_rot[0][2], base_rot[1][2]])

    # Dessin de l'aile delta (surface triangulaire)
    ax.plot_trisurf(
        [x_rot[0], x_rot[1], x_rot[2]],
        [y_rot[0], y_rot[1], y_rot[2]],
        [z_rot[0], z_rot[1], z_rot[2]],
        color='lightblue', edgecolor='black'
    )

    canvas.draw()


# Fonction pour lire les données depuis le port série
def read_serial_data(ax, ref):
    global angle_x, angle_y, angle_z
    xRef,yRef = ref
    while True:
        try:
            xPos,yPos = mouse.get_position()
            line = str(xPos-xRef)+"."+str(yPos-yRef)+".0"         
            print (line)
            if line:
                angles = line.split('.')
                if len(angles) == 3:
                    angle_x = float(angles[0])
                    angle_y = float(angles[1])
                    angle_z = float(angles[2])
                    update_wing(ax, angle_x, angle_y, angle_z)
        except Exception as e:
            print(f"Erreur lors de la lecture série : {e}")

# Création de la fenêtre Tkinter
root = tk.Tk()
root.title("Visualisation 3D d'une aile delta")

# Création de la figure et intégration dans Tkinter
fig, ax = create_figure()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Affichage initial de l'aile delta
update_wing(ax, angle_x, angle_y, angle_z)

ref = mouse.get_position()

# Lancement du thread pour lire les données série
serial_thread = threading.Thread(target=read_serial_data, args=(ax, ref, ), daemon=True)
serial_thread.start()

# Affichage de la fenêtre
tk.mainloop()
