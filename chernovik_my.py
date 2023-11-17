import beetest
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def rosenbrock(x, y):
    return (1.0 - x) ** 2 + 100.0 * (y - x * x) ** 2

def make_rosenbrock_lab_5():
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    x_grid, y_grid = np.meshgrid(x, y)
    z = rosenbrock(x_grid, y_grid)  #z = rosenbrock2(x_grid, y_grid)
    return x_grid, y_grid, z

x, y, z = make_rosenbrock_lab_5()

# Create the main Tkinter window
root = Tk()
root.title("Your Window Title")

# Create a matplotlib figure
fig = plt.Figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, cmap='viridis', alpha=0.3)  # Plot the surface function

# Embed the matplotlib figure in the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=TOP, fill=BOTH, expand=1)

number_of_points = 1000
left_border, right_border = -100, 100

result = beetest.bee_algorithm(0, 300, 30, 10, 15, 5, 1, 2000, 10)

# Corrected variable names
x_result, y_result, z_result = [], [], []
x_result.append(result[0][0])
y_result.append(result[0][1])
y_result.append(result[1])

print(x_result, y_result, z_result)

ax.scatter(x_result[-1], y_result[-1], y_result[-1], c='r', marker='o',label='Points')

# Start the Tkinter event loop
root.mainloop()




