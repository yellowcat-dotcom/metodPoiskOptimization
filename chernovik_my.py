import beetest
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def himmelblau(x, y):
    return (x**2 + y - 11)**2 + (x + y**2 - 7)**2

def make_himmelblau_lab_5():
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    x_grid, y_grid = np.meshgrid(x, y)
    z = himmelblau(x_grid, y_grid)
    return x_grid, y_grid, z

def find_minima(num_minima=4, threshold=1e-3):
    minima = []

    while len(minima) < num_minima:
        result = beetest.bee_algorithm(2, 300, 30, 10, 15, 5, 1, 2000, 10)
        x_result, y_result = result[0][0], result[0][1]
        z_result = himmelblau(x_result, y_result)

        # Check if the new minimum is close to an existing minimum
        close_to_existing = any(
            np.linalg.norm(np.array([x_result, y_result, z_result]) - np.array(existing_min)) < threshold
            for existing_min in minima
        )

        if not close_to_existing:
            minima.append((round(x_result, 6), round(y_result, 6), round(z_result, 6)))

    return minima

minima_list = find_minima()

x, y, z = make_himmelblau_lab_5()

# Create the main Tkinter window
root = Tk()
root.title("Himmelblau Minima Visualization")

# Create a matplotlib figure
fig = plt.Figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, cmap='viridis', alpha=0.3)  # Plot the surface function

# Embed the matplotlib figure in the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=TOP, fill=BOTH, expand=1)

# Plot all found minima
minima_scatter = ax.scatter([], [], [], c='r', marker='o', label='Minima')

for minima in minima_list:
    ax.scatter(minima[0], minima[1], minima[2], c='r', marker='o')
    print(minima[0], minima[1], minima[2])

# Update the scatter plot data
minima_scatter._offsets3d = (minima_scatter._offsets3d[0], minima_scatter._offsets3d[1], minima_scatter._offsets3d[2])

# Start the Tkinter event loop
root.mainloop()