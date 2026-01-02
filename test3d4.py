import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from tkinter import ttk
import serial
import threading

# Paramètres du cylindre
radius = 1.0
height = 0.2
num_points = 100

# Création des données initiales pour le cylindre
theta = np.linspace(0, 2 * np.pi, num_points)
z = np.linspace(-height / 2, height / 2, 10)
theta_grid, z_grid = np.meshgrid(theta, z)
x_grid = radius * np.cos(theta_grid)
y_grid = radius * np.sin(theta_grid)

# Variables globales pour les angles
angle_x, angle_y, angle_z = 0, 0, 0

# Fonction pour appliquer les rotations
def rotate_points(x, y, z, angle_x, angle_y, angle_z):
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
    x_new, y_new, z_new = x_rot, y_rot, z_rot

    return x_new, y_new, z_new

# Fonction pour créer la figure 3D
def create_figure():
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Plateau cylindrique 3D (Angles depuis Arduino)')
    return fig, ax

# Fonction pour mettre à jour le cylindre
def update_cylinder(ax, angle_x, angle_y, angle_z):
    ax.cla()
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Plateau cylindrique 3D (Angles depuis Arduino)')

    # Appliquer les rotations
    x_rot, y_rot, z_rot = rotate_points(x_grid, y_grid, z_grid, angle_x, angle_y, angle_z)

    # Redessiner le cylindre
    ax.plot_surface(x_rot, y_rot, z_rot, color='lightblue', edgecolor='black')
    canvas.draw()

# Fonction pour lire les données depuis le port série
def read_serial_data(ser, ax):
    global angle_x, angle_y, angle_z
    while True:
        try:
            # Lecture de la ligne envoyée par Arduino
            line = ser.readline().decode('utf-8').strip()
            if line:
                # On suppose que l'Arduino envoie les angles sous la forme "X,Y,Z"
                angles = line.split(',')
                if len(angles) == 3:
                    angle_x = float(angles[0])
                    angle_y = float(angles[1])
                    angle_z = float(angles[2])
                    # Mise à jour du cylindre
                    update_cylinder(ax, angle_x, angle_y, angle_z)
        except Exception as e:
            print(f"Erreur lors de la lecture série : {e}")

# Création de la fenêtre Tkinter
root = tk.Tk()
root.title("Visualisation 3D d'un plateau cylindrique")

# Création de la figure et intégration dans Tkinter
fig, ax = create_figure()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Affichage initial du cylindre
update_cylinder(ax, angle_x, angle_y, angle_z)

# Configuration du port série (remplace 'COM3' par le port de ton Arduino)
try:
    ser = serial.Serial('COM3', 9600, timeout=1)
    print(f"Connecté au port série : {ser.portstr}")
except serial.SerialException as e:
    print(f"Erreur lors de l'ouverture du port série : {e}")
    ser = None

# Lancement du thread pour lire les données série
if ser:
    serial_thread = threading.Thread(target=read_serial_data, args=(ser, ax), daemon=True)
    serial_thread.start()

# Affichage de la fenêtre
tk.mainloop()

# Fermeture du port série à la fin
if ser:
    ser.close()
