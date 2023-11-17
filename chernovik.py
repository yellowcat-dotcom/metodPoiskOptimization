def button5Clicked(self):
    bee_functions = {'Sphere function': LabData.lab5_sphere,
                     'Rosenbrock function': LabData.lab5_rosenbrock,
                     'Goldstein Price Function': LabData.lab5_goldstein}

    bee_function = bee_functions[str(self.comboBox_function_5.currentText())]
    print(bee_functions[str(self.comboBox_function_5.currentText())])

    function, x, y, z, left_border, right_border, number_of_points = bee_function()
    self.drawGraphic(self.MplWidget5, function, x, y, z, left_border, right_border,
                     number_of_points)

    self.textBrowser5.setText("")
    for i in range(len(x)):
        self.textBrowser5.append(f'Result: ({x[i]}, {y[i]}, {z[i]})')




@staticmethod
    def lab5_sphere():
        number_of_points = 1000
        left_border, right_border = -100, 100

        result = beetest.bee_algorithm(0, 300, 30, 10, 15, 5, 1, 2000, 10)

        x, y, z = [], [], []
        x.append(result[0][0])
        y.append(result[0][1])
        z.append(result[1])

        return [Function.sphere_function, x, y, z, left_border, right_border, number_of_points]

    @staticmethod
    def lab5_rosenbrock():
        number_of_points = 1000
        left_border, right_border = -2, 2

        result = beetest.bee_algorithm(3, 300, 30, 10, 15, 5, 1, 2000, 10)

        x, y, z = [], [], []
        x.append(result[0][0])
        y.append(result[0][1])
        z.append(result[1])

        return [Function.rosenbrock_function, x, y, z, left_border, right_border, number_of_points]

    @staticmethod
    def lab5_goldstein():
        number_of_points = 1000
        left_border, right_border = -100, 100

        result = beetest.bee_algorithm(2, 300, 30, 10, 15, 5, 1, 2000, 10)

        x, y, z = [], [], []
        x.append(result[0][0])
        y.append(result[0][1])
        z.append(result[1])

        return [Function.goldstein_function, x, y, z, left_border, right_border, number_of_points]
