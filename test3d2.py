from time import sleep
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk

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

# Initialisation des angles de rotation
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
    x_new, y_new, z_new = x_rot, y_rot, z_new

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
    ax.set_title('Plateau cylindrique 3D (A/Q: X, L/M: Y, O/P: Z)')
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
    ax.set_title('Plateau cylindrique 3D (A/Q: X, L/M: Y, O/P: Z)')
    print("b1")
    # Appliquer les rotations
    x_rot, y_rot, z_rot = rotate_points(x_grid, y_grid, z_grid, angle_x, angle_y, angle_z)
    d("rot") 
    # Redessiner le cylindre
    ax.plot_surface(x_rot, y_rot, z_rot, color='lightblue',edgecolor='black')
    print("b3")
    plt.draw()

# Fonction pour gérer les événements clavier
def d(t):
    global angle_x, angle_y, angle_z

    print(t," ",angle_x," ",angle_y," ", angle_z)


# Fonction pour gérer les événements clavier
def on_key(event, ax):
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
    d("a1")
    update_cylinder(ax, angle_x, angle_y, angle_z)
    d("a2")

# Création de la fenêtre Tkinter
print("a")
root = tk.Tk()
root.title("Visualisation 3D d'un plateau cylindrique")
print("b")

# Création de la figure et intégration dans Tkinter
fig, ax = create_figure()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
print("c")

# Liaison des événements clavier
canvas.mpl_connect('key_press_event', lambda event: on_key(event, ax))

# Affichage initial du cylindre
update_cylinder(ax, angle_x, angle_y, angle_z)
print("d")

# Affichage de la fenêtre
sleep(1000000)
tk.mainloop()
print("e")

