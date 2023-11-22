from tkinter import *
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import task1
import task2
import task2_2
import matplotlib.animation as animation
from tkinter.ttk import Combobox, Notebook, Style
import genetic_algorithm_l3
import pchely
import beetest
def click_but1():
    x1 = float(input1.get())
    x2 = float(input2.get())
    M = int(input3.get())
    epsilon1 = float(input4.get())
    epsilon2 = float(input5.get())
    tk = float(input6.get())
    # Вызываем функцию task1.task_1 с полученными параметрами
    grafik , result = task1.task_1(x1, x2, M, epsilon1, epsilon2, tk)
    result_labe.config(text=result,font=("Aria Bold",13))
    result_labe.place(x=400, y=400)
    canvas = FigureCanvasTkAgg(grafik, master=frame1)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=400, y=0)

def command1():
    simplex_function, x, y, z, left_border, right_border, number_of_points = task2.lab2()
    x1_range = np.linspace(-6, 6, 100)
    x2_range = np.linspace(-6, 6, 100)

    # Create a grid of (x1, x2) values
    X1, X2 = np.meshgrid(x1_range, x2_range)

    # Calculate the function values for each (x1, x2) pair
    Z = task2.simplex_function(X1, X2)

    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the surface
    surface = ax.plot_surface(X1, X2, Z, cmap='viridis')

    # Add a color bar which maps values to colors
    fig.colorbar(surface, shrink=0.5, aspect=5, label='Function Value')
    points = [x, y, z]
    print(points)
    ax.plot([points[0]], [points[1]], [points[2]], markerfacecolor='k', markeredgecolor='r', marker='.', markersize=10,
            alpha=1)
    # Set labels for the axes
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    ax.set_zlabel('Function Value')
    ax.set_title('3D Plot of simplex_function')
    canvas = FigureCanvasTkAgg(fig, master=frame2)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=400, y=0)
    result_label = ttk.Label(frame2, text="Точка: (" + str("%.4f" % points[0][0]) + ";" + str("%.4f" %points[1][0]) + ";" + str(
        "%.4f" % points[2][0]) + ")",
                             font=("Arial Bold", 15))

    result_label.place(x=400, y=500)

def command2():
    x, y = task2_2.example()
    x1_range = np.linspace(-6, 6, 100)
    x2_range = np.linspace(-6, 6, 100)
    X1, X2 = np.meshgrid(x1_range, x2_range)
    Z = task2_2.simplex_function(X1, X2)

    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the surface
    surface = ax.plot_surface(X1, X2, Z, cmap='viridis')

    # Add a color bar which maps values to colors
    fig.colorbar(surface, shrink=0.5, aspect=5, label='Function Value')
    points = [x[0], x[1], y]
    print(points)
    ax.plot([points[0]], [points[1]], [points[2]], markerfacecolor='k', markeredgecolor='r', marker='.', markersize=10,
            alpha=1)
    # Set labels for the axes
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    ax.set_zlabel('Function Value')
    ax.set_title('3D Plot of simplex_function')
    canvas = FigureCanvasTkAgg(fig, master=frame2)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=400, y=0)
    result_label = ttk.Label(frame2, text="Точка: (" + str("%.4f" % x[0]) + "; " + str("%.4f" % x[1]) + ";" + str( "%.4f" % y) + ")",
                             font=("Arial Bold", 15))

    result_label.place(x=400, y=500)

def rosenbrock(x):
    return np.sum(100.0 * (x[1:] - x[:-1] ** 2.0) ** 2.0 + (1 - x[:-1]) ** 2.0)

def rosenbrock_2(x, y):
    return (1.0 - x) ** 2 + 100.0 * (y - x * x) ** 2

def make_data_lab_3():
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    x_grid, y_grid = np.meshgrid(x, y)
    z = rosenbrock_2(x_grid, y_grid)
    return x_grid, y_grid, z

def draw_lab_3():
    x, y, z = make_data_lab_3()

    pop_number = int(txt_1_tab_3.get())
    iter_number = int(txt_2_tab_3.get())
    survive = float(txt_3_tab_3.get())
    mutation = float(txt_4_tab_3.get())
    delay = float(txt_5_tab_3.get())

    if combo_tab_3.get() == "Min":
        min_max = True
    else:
        min_max = False

    fig = plt.Figure()
    ax = fig.add_subplot(111, projection='3d')
    surface = ax.plot_surface(x, y, z, rstride=5, cstride=5, alpha=0.5, cmap='viridis')
    fig.colorbar(surface, shrink=0.5, aspect=5, label='Function Value')

    canvas = FigureCanvasTkAgg(fig, master=frame3)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()
    canvas_widget.place(x=400, y=0)

    result_label_tab_3 = ttk.Label(frame3, text="", font=("Arial Bold", 15))
    result_label_tab_3.pack(anchor=NW, padx=60, pady=0)

    def update_plot(frame):
        nonlocal ax, fig
        ax.clear()
        surface = ax.plot_surface(x, y, z, rstride=5, cstride=5, alpha=0.5, cmap='viridis')

        for j in range(pop_number):
            ax.scatter(genetic.population[j][0], genetic.population[j][1], genetic.population[j][2], c="black", s=1, marker="s")

        genetic.select()
        genetic.mutation(frame)

        gen_stat = genetic.statistic()
        best_x, best_y, best_z = gen_stat[0], gen_stat[1], gen_stat[2]

        ax.plot([best_x], [best_y], [best_z], markerfacecolor='red', markeredgecolor='red', marker='o', markersize=5)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        result_label_tab_3.config(text="Точка: (" + str("%.4f" % best_x) + ", " +
                                   str("%.4f" % best_y) + ", " +
                                   str("%.4f" % best_z) + ")")
        canvas.draw()
        if frame == iter_number - 1:
            messagebox.showinfo('Уведомление', 'Готово')

    genetic = genetic_algorithm_l3.GeneticAlgorithmL3(rosenbrock_2, iter_number, min_max, mutation, survive, pop_number)
    genetic.generate_start_population(5, 5)

    ani = animation.FuncAnimation(fig, update_plot, frames=iter_number, repeat=False)

    root.mainloop()

def make_sphere_lab_4():
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    x_grid, y_grid = np.meshgrid(x, y)
    z = pchely.sphere_function(x_grid, y_grid)
    return x_grid, y_grid, z

def make_rast_lab_4():
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    x_grid, y_grid = np.meshgrid(x, y)
    z=pchely.rastrigin_function(x_grid,y_grid)
    return x_grid, y_grid, z

def make_shvefe_lab_4():
    x = np.linspace(-1000,1000, 1000)
    y = np.linspace(-1000,1000, 1000)
    x_grid, y_grid = np.meshgrid(x, y)
    z=pchely.schwefel_function(x_grid,y_grid)
    return x_grid, y_grid, z


def draw_lab_4(name):
    if name=="Сферы":
        x, y, z = make_sphere_lab_4()
    if name=="Растригина":
        x,y,z = make_rast_lab_4()
    if name=="Швефеля":
        x, y, z = make_shvefe_lab_4()

    fig = plt.Figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(x, y, z, cmap='viridis', alpha=0.3)  # Отобразить поверхность функции

    canvas = FigureCanvasTkAgg(fig, master=frame4)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()
    canvas_widget.place(x=400, y=0)

    result_label_tab_4 = ttk.Label(frame4, text="", font=("Arial Bold", 15))
    result_label_tab_4.pack(anchor=NW, padx=60, pady=0)

    # Предполагается, что pchely.lab4_rastrigin() возвращает результаты для x_2, y_2, z_2
    if name=="Сферы":
        result = pchely.lab4_sphere()
    if name=="Растригина":
        result = pchely.lab4_rastrigin()
    if name=="Швефеля":
        result = pchely.lab4_schwefel()

    x_2 = result[1]
    y_2 = result[2]
    z_2 = result[3]

    result_label_tab_4.config(text="Точка: (" + str("%.10f" % x_2[-1]) + ",\n " +
                                            str("%.10f" % y_2[-1]) + ",\n " +
                                            str("%.10f" % z_2[-1]) + ")")
    ax.scatter(x_2[-1], y_2[-1], z_2[-1], c='r', marker='o',label='Points')

    root.mainloop()

def draw_lab_5(name):
    # done
    if name=="Розенброка":
        x, y, z = make_data_lab_3()

    # from before lab 4
    if name=="Химмельблау":
        x,y,z = make_rast_lab_4()

    # done
    if name=="Растригина":
        x, y, z = make_rast_lab_4()


    fig = plt.Figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(x, y, z, cmap='viridis', alpha=0.3)  # Отобразить поверхность функции

    canvas = FigureCanvasTkAgg(fig, master=frame5)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()
    canvas_widget.place(x=400, y=0)

    result_label_tab_5 = ttk.Label(frame5, text="", font=("Arial Bold", 15))
    result_label_tab_5.pack(anchor=NW, padx=60, pady=0)


    if name=="Розенброка":
        result = beetest.bee_algorithm(0, 300, 30, 10, 15, 5, 1, 2000, 10)
    if name=="Химмельблау":
        result = pchely.lab4_rastrigin()


    if name=="Растригина":
        result = beetest.bee_algorithm(1, 300, 30, 10, 15, 5, 1, 2000, 10)




    # Corrected variable names
    x_result, y_result, z_result = [], [], []

    x_result.append(result[0][0])
    y_result.append(result[0][1])
    z_result.append(result[1])

    print(x_result, y_result, z_result)

    ax.scatter(x_result[-1], y_result[-1], y_result[-1], c='r', marker='o', label='Points')

    result_label_tab_5.config(text="Точка: (" + str("%.10f" % x_result[-1]) + ",\n " +
                                            str("%.10f" % y_result[-1]) + ",\n " +
                                            str("%.10f" % z_result[0]) + ")")

    root.mainloop()



root = Tk()
root.title("LABS")
root.geometry("1100x650")

# создаем набор вкладок
notebook = ttk.Notebook()
notebook.pack(expand=True, fill=BOTH)

# создаем пару фреймвов
frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)
frame3 = ttk.Frame(notebook)
frame4 = ttk.Frame(notebook)
frame5 = ttk.Frame(notebook)

frame1.pack(fill=BOTH, expand=True)
frame2.pack(fill=BOTH, expand=True)
frame3.pack(fill=BOTH, expand=True)
frame4.pack(fill=BOTH, expand=True)
frame5.pack(fill=BOTH, expand=True)

# добавляем фреймы в качестве вкладок
notebook.add(frame1, text="ЛР_1")
notebook.add(frame2, text="ЛР_2")
notebook.add(frame3, text="ЛР_3")
notebook.add(frame4, text="ЛР_4")
notebook.add(frame5, text="ЛР_5")


#                ВКЛАДКА 1
label1= ttk.Label(frame1,text="Введите данные:",font=("Aria Bold",20))
label1.pack(anchor=NW,padx= 60, pady= 10)

label2= ttk.Label(frame1,text="x1:",font=("Aria Bold",15))
label2.pack(anchor=NW,padx= 60, pady= 0)
input1 = ttk.Entry(frame1)
input1.pack( anchor=NW, padx=60, pady=0)
label3= ttk.Label(frame1,text="x2:",font=("Aria Bold",15))
label3.pack(anchor=NW,padx= 60, pady= 0)
input2 = ttk.Entry(frame1)
input2.pack( anchor=NW, padx=60, pady=0)
label4= ttk.Label(frame1,text="M (кол-во шагов):",font=("Aria Bold",15))
label4.pack(anchor=NW,padx= 60, pady= 0)
input3 = ttk.Entry(frame1)
input3.pack( anchor=NW, padx=60, pady=0)
label4= ttk.Label(frame1,text="e1:",font=("Aria Bold",15))
label4.pack(anchor=NW,padx= 60, pady= 0)
input4 = ttk.Entry(frame1)
input4.pack( anchor=NW, padx=60, pady=0)
label5= ttk.Label(frame1,text="e2:",font=("Aria Bold",15))
label5.pack(anchor=NW,padx= 60, pady= 0)
input5 = ttk.Entry(frame1)
input5.pack( anchor=NW, padx=60, pady=0)
label6= ttk.Label(frame1,text="t_k (шаг):",font=("Aria Bold",15))
label6.pack(anchor=NW,padx= 60, pady= 0)
input6 = ttk.Entry(frame1)
input6.pack( anchor=NW, padx=60, pady=0)

btn_1=ttk.Button(frame1,text="Результат", command=click_but1)
btn_1.pack( anchor=NW, padx=60, pady=0)

label7= ttk.Label(frame1,text="Результат для функции:\nf(x)=2x₁+x₁x₂-x₂²",font=("Aria Bold",15))
label7.pack(anchor=NW,padx= 60, pady= 0)

result_labe = ttk.Label(frame1, text="", font=("Arial Bold", 15))
result_labe.pack(anchor=NW, padx=60, pady=0)

#   ВКЛАДКА 2
label9= ttk.Label(frame2,text="Вариант 1: \nf(x)=2x₁²+2x₁x₂+2x₂²-4x₁-6x₂->min \nx₁+2x₂≤2 \nx₁≥0, x₂≥0",font=("Aria Bold",15))
label9.pack(anchor=NW,padx= 60, pady= 0)

button1 = ttk.Button(frame2, text="Показать решение", command=command1)
button1.pack(anchor=NW, padx=60, pady=0)


label8= ttk.Label(frame2,text="\nВариант 2:\nf(x)=2x₁²+3x₂²+4x₁x₂-6x₁-3x₂->min\nx₁+2x₂≤1\n2x₁+3x₂≤4\nx₁≥0, x₂≥0",font=("Aria Bold",15))
label8.pack(anchor=NW,padx= 60, pady= 0)

button2 = ttk.Button(frame2, text="Показать решение", command=command2)
button2.pack(anchor=NW, padx=60, pady=0)

# Создаем вторую кнопку с несколькими командами


result_label = ttk.Label(frame2)
result_label.place(x=60, y=400)

# ВКЛАДКА 3
lbl_6_tab_3 = Label(frame3, text="Функция Розенброка")
lbl_6_tab_3.pack(anchor=NW,padx= 60, pady= 0)

lbl_1_tab_3 = Label(frame3, text="Размер популяции")
lbl_1_tab_3.pack(anchor=NW,padx= 60, pady= 0)
txt_1_tab_3 = Entry(frame3)
txt_1_tab_3.insert(0,"50")
txt_1_tab_3.pack(anchor=NW,padx= 60, pady= 0)

lbl_2_tab_3 = Label(frame3, text="Количество итераций")
lbl_2_tab_3.pack(anchor=NW,padx= 60, pady= 0)
txt_2_tab_3 = Entry(frame3)
txt_2_tab_3.insert(0,"50")
txt_2_tab_3.pack(anchor=NW,padx= 60, pady= 0)

lbl_3_tab_3 = Label(frame3, text="Выживаемость")
lbl_3_tab_3.pack(anchor=NW,padx= 60, pady= 0)
txt_3_tab_3 = Entry(frame3)
txt_3_tab_3.insert(0,"0.7")
txt_3_tab_3.pack(anchor=NW,padx= 60, pady= 0)

lbl_7_tab_3 = Label(frame3, text="Шанс мутации")
lbl_7_tab_3.pack(anchor=NW,padx= 60, pady= 0)
txt_4_tab_3 = Entry(frame3)
txt_4_tab_3.insert(0,"0.2")
txt_4_tab_3.pack(anchor=NW,padx= 60, pady= 0)


lbl_5_tab_3 = Label(frame3, text="Задержка в секундах")
lbl_5_tab_3.pack(anchor=NW,padx= 60, pady= 0)
txt_5_tab_3 = Entry(frame3)
txt_5_tab_3.insert(0,"0.01")
txt_5_tab_3.pack(anchor=NW,padx= 60, pady= 0)

btn_tab_3 = Button(frame3, text="Выполнить", foreground="black", command=draw_lab_3)
btn_tab_3.pack(anchor=NW,padx= 60, pady= 0)

combo_tab_3 = Combobox(frame3)
combo_tab_3['values'] = ("Min", "Max")
combo_tab_3.set("Min")

# ЛАБА 4
def on_combobox_select(event):
    selected_value = combobox.get()
    print(selected_value)
    draw_lab_4(str(selected_value))

frame_4_tab1 = Label(frame4, text="Алгоритм роя частиц", font="Verdana 12 bold")
frame_4_tab1.pack(anchor=NW,padx= 60, pady= 10)
values = ["Сферы", "Растригина", "Швефеля"]
combobox = ttk.Combobox(frame4,state="readonly", values=values, font="Verdana 12 bold")
combobox.set("Выберите функцию")  # Значение по умолчанию
combobox.pack(anchor=NW,padx= 60, pady= 30)
combobox.bind("<<ComboboxSelected>>", on_combobox_select)

# ВКЛАДКА 5

def on_combobox_select_5_lab(event):
    selected_value = combobox.get()
    print(selected_value)
    draw_lab_5(str(selected_value))

frame_5_tab1 = Label(frame5, text="Алгоритм роя пчел", font="Verdana 12 bold")
frame_5_tab1.pack(anchor=NW,padx= 60, pady= 10)

values = ["Розенброка", "Химмельблау", "Растригина"]
combobox = ttk.Combobox(frame5,state="readonly", values=values, font="Verdana 12 bold")
combobox.set("Выберите функцию")  # Значение по умолчанию
combobox.pack(anchor=NW,padx= 60, pady= 30)
combobox.bind("<<ComboboxSelected>>", on_combobox_select_5_lab)



root.mainloop()