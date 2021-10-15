from slider import *
from buttons import *
from utils import random_colour
from string_formatting import syntax_correction
from maths.math_functions import *


# This class is used to represent a graph inputted by the user
class Equation:  # Used for plotting graphs
    def __init__(self, parentWindow, equationType):
        self.type = equationType  # Parametric or Cartesian
        self.parent_window = parentWindow
        self.window_open = True

        # These are local constants which may be used in the equation and can be controlled using sliders
        self.a = 1
        self.b = 1
        self.c = 1
        self.d = 1

        self.slider_width = 180

        # These three expressions represent the x,y and z coordinates in terms of a fourth variable 't'
        # These attributes will only be used if the equation is parametric type
        self.x_equation = str()
        self.y_equation = str()
        self.z_equation = str()

        # This attribute is a string which represents the equation using the
        # variables x, y and z (in the given domain)
        self.cartesian_equation = None

        # These start and end values are used for Cartesian equations to reduce
        # the amount of time the program takes to search for all the points.
        # This is useful for spheres for example where the points are only
        # located in the domain -radius <= x,y,z <= radius
        self.start_x = '-1'
        self.end_x = '1'
        self.start_y = '-1'
        self.endY = '1'
        self.start_z = '-1'
        self.endZ = '1'

        # This is the domain of the parametric variable
        self.start_value = '-1'
        self.end_value = '1'

        # A list of Point objects with coordinates that satisfy the equation
        self.points = []

        self.limit1 = 0
        self.limit1Point1 = Point(self.parent_window)
        self.limit1_point2 = Point(self.parent_window)
        self.limit2 = 0
        self.limit2Point1 = Point(self.parent_window)
        self.limit2_point2 = Point(self.parent_window)

        # A list of Slider objects that will be displayed and active when the graph of the equation is selected
        self.sliders = [Slider('a', 'a', 0, self.parent_window.height - 60,
                               -10, 10, self.parent_window, self, 180, 60, '', 1),
                        Slider('b', 'b', 180, self.parent_window.height - 60,
                               -10, 10, self.parent_window, self, 180, 60, '', 1),
                        Slider('c', 'c', 360, self.parent_window.height - 60,
                               -10, 10, self.parent_window, self, 180, 60, '', 1),
                        Slider('d', 'd', 540, self.parent_window.height - 60,
                               -10, 10, self.parent_window, self, 180, 60, '', 1),
                        Slider('e', 'e', 720, self.parent_window.height - 60,
                               -10, 10, self.parent_window, self, 180, 60, '', 1),
                        Slider('limit1', 'limit1', 0, self.parent_window.height - 110,
                               -10, 10, self.parent_window, self, 180, 50, '', 0),
                        Slider('limit2', 'limit2', 200, self.parent_window.height - 110,
                               -10, 10, self.parent_window, self, 180, 50, '', 0)]

        self.parent_window = parentWindow
        self.showSliders = False
        self.isSelected = True
        # Colour of the lines used to draw the curve or the points satisfying
        # the equation
        self.colour = random_colour()
        self.thickness = 1

        # Tkinter root
        self.root = None

        # The amount by which the parametric variable or x,y and z will be
        # incremented to calculate or check valid points
        # Lower the increment, greater the detail but longer the time it takes
        # to calculate the points and vice versa
        self.accuracy = '0.1'

        # Temporary variable to get the general shape of the graph in a short time
        self.error = 5
        self.listOfSides = []

    def get_points(self):
        return self.points

    def draw_graph(self):
        if self.type == 'parametric':
            self.draw_parametric()

        # Cartesian equation will be represented only as individual points because
        # it is very difficult to represent curved surfaces
        elif self.type == 'cartesian':
            for point in self.points2:
                point.calculate_screen_pos()
                point.show()  # Draws point

    def draw_parametric(self):
        add = 1  # To skip points
        i = add
        # Remember that the screenPos of a point is a tuple containing the
        # display coordinates of the point
        while i < len(self.points2) - add:

            if (self.points2[i] != '' and
                    self.points2[i - add] != ''):
                if (self.points2[i].visible() or
                        self.points2[i - add].visible()):
                    plot = True

                elif (self.points2[i].screen_pos[0] < 0
                      and self.points2[i - add].screen_pos[0] < 0
                      or self.points2[i].screen_pos[0] > self.parent_window.width
                      and self.points2[i - add].screen_pos[0] > self.parent_window.width):
                    plot = False

                elif (self.points2[i].screen_pos[1] < 0
                      and self.points2[i - add].screen_pos[1] < 0
                      or self.points2[i].screen_pos[1] > self.parent_window.height
                      and self.points2[i - add].screen_pos[1] > self.parent_window.height):
                    plot = False

                else:
                    plot = True

                if plot:
                    self.points2[i].show()
                    # Drawing a line between adjacent points
                    if self.thickness == 1:
                        # A smoother line drawing function which only allows one thickness
                        pygame.draw.aaline(self.parent_window.get_screen(),
                                           self.colour,
                                           self.points2[i - add].screen_pos,
                                           self.points2[i].screen_pos)
                    elif self.thickness == 2:
                        # Not as smooth but allows different thicknesses
                        pygame.draw.line(self.parent_window.get_screen(),
                                         self.colour,
                                         self.points2[i - add].screen_pos,
                                         self.points2[i].screen_pos,
                                         self.thickness)

            i = i + add

    # This is used to check if the user is hovering the mouse over any point on
    # the graph of the equation
    def mouse_over_graph(self):
        # Checks if the user has clicked on any of the points in the graph for the equation

        if self.type == 'cartesian':  # If the user hasn't clicked on any of the
            return self.mouse_over_cartesian()
        # Similar to the Line class, checks if the user has clicked on any
        # line between adjacent points
        elif self.type == 'parametric':
            return self.mouse_over_parametric()

    def mouse_over_parametric(self):
        for point in self.points:
            if point == '' or point.screen_pos is not None:
                continue
            if point.mouse_over_point():
                return True

        i = 1
        while i < len(self.points) - 1:  # Iterates through all the points
            if (self.points[i] != '' and
                    self.points[i - 1] != ''):  # To ensure it is not an undefined point
                point1 = self.points[i]
                point2 = self.points[i - 1]
                try:
                    if (point2.screen_pos[0] - pygame.mouse.get_pos()[0] == 0
                            # When one of the lines is vertical (to avoid zero division error)
                            or point2.screen_pos[0] - point1.screen_pos[0] == 0):
                        if (point2.screen_pos[0] - pygame.mouse.get_pos()[0] == 0
                                and point2.screen_pos[0] - point1.screen_pos[0] == 0
                                and min(point1.cor[1], self.point2.cor[1]) < pygame.mouse.get_pos()[1] < max(
                                    point1.cor[1], point2.cor[1])):
                            return True
                        else:
                            return False

                    # First checks if the mouse is in the rectangle which has the line as a diagonal
                    if (min(point1.screen_pos[0], point2.screen_pos[0]) < pygame.mouse.get_pos()[0] < max(
                            point1.screen_pos[0], point2.screen_pos[0])
                            and min(point1.screen_pos[1], point2.screen_pos[1]) < pygame.mouse.get_pos()[1] < max(
                                point1.screen_pos[1], point2.screen_pos[1])):
                        # Gradient of line joining two adjacent points on the curve
                        dy = (point1.screen_pos[1] - point2.screen_pos[1])
                        dx = (point1.screen_pos[0] - point2.screen_pos[0])
                        gradient1 = dy / dx
                        # Gradient of line joining the point on the curve and the point where the mouse has been
                        # clicked
                        dy = point1.screen_pos[1] - pygame.mouse.get_pos()[1]
                        dx = point1.screen_pos[0] - pygame.mouse.get_pos()[0]
                        gradient2 = dy / dx
                        if gradient1 == 0:
                            if abs(round(gradient2, 2)) <= 0.1:  # For small gradients
                                return True
                        elif (abs(round(gradient1, 2)) * 0.9 <=
                              abs(round(gradient2, 2)) <=
                              abs(round(gradient1, 2)) * 1.1
                              and gradient1 * gradient2 >= 0):  # Compares gradients
                            return True
                        else:
                            return False
                except:
                    pass
            i += 1

    def mouse_over_cartesian(self):
        # Checks if the user has clicked on any of the points in the graph for the equation
        for point in self.points:
            if point == '' or point.screen_pos is not None:
                continue
            if point.mouse_over_point():
                return True
        return False

    # These are the windows that will be created when the user wants to add a
    # new parametric or Cartesian equation or edit them.
    # When these windows are open the rest of the program will stop functioning
    # (unless the required methods are specifically called).
    def window(self, x=None, y=None):  # Equationwindow
        self.root = Tk()
        self.window_open = True
        self.root.title('Equation Properties')
        self.root.after(1, lambda: self.root.focus_force())
        # Makes sure that the root opens on top of the Pygame root.
        self.root.attributes('-topmost', True)
        if x is None:
            (x, y) = (pygame.mouse.get_pos()[0] + 10, pygame.mouse.get_pos()[1] + 10)

        # self.settings_window.geometry('300x200+'+str(x)+'+'+str(y))

        Label(self.root, text='step =', font='Caibri 10').grid(column=1, row=4)

        self.accuracy_ent = Entry(self.root, width=5, font='Calibri 10')
        self.accuracy_ent.grid(column=0, row=4)

        if self.type == 'parametric':
            self.parametric_window()

        elif self.type == 'cartesian':
            self.cartesian_window()

    def cartesian_window(self):
        self.parent_window.cartesian_equations_windows.append(self)
        Label(self.root, text='Equation:').grid(column=0, row=0)
        self.cartesian_equation_ent = Entry(self.root, font='Calibri 15')
        self.cartesian_equation_ent.grid(column=0, row=1)
        self.start_x_ent = Entry(self.root, width=7, font='Calibri 12')
        self.start_x_ent.place(relx=0.2, rely=0.25)
        self.x_range_label = Label(self.root, text='≤ x ≤', font='Calibri 12')
        self.x_range_label.place(relx=0.4, rely=0.25)
        self.end_x_ent = Entry(self.root, width=7, font='Calibri 12')
        self.end_x_ent.place(relx=0.6, rely=0.25)
        self.start_y_ent = Entry(self.root, width=7, font='Calibri 12')
        self.start_y_ent.place(relx=0.2, rely=0.35)
        Label(self.root, text='≤ y ≤', font='Calibri 12').grid(column=1, row=3)
        self.end_y_ent = Entry(self.root, width=7, font='Calibri 12')
        self.end_y_ent.place(relx=0.6, rely=0.35)
        self.start_z_ent = Entry(self.root, width=7, font='Calibri 12')
        self.start_z_ent.place(relx=0.2, rely=0.45)
        Label(self.root, text='≤ z ≤', font='Calibri 12').grid(column=1, row=4)
        self.end_z_ent = Entry(self.root, width=7, font='Calibri 12')
        self.end_z_ent.place(relx=0.6, rely=0.45)
        self.apply = Button(self.root, text='Apply',
                            command=lambda: self.set_info_cartesian(self.cartesian_equation_ent.get(),
                                                                    self.start_x_ent.get(),
                                                                    self.end_x_ent.get(),
                                                                    self.start_y_ent.get(),
                                                                    self.end_y_ent.get(),
                                                                    self.start_z_ent.get(),
                                                                    self.end_z_ent.get(),
                                                                    self.accuracy_ent.get(),
                                                                    self.error_ent.get()))
        self.apply.place(relx=0.8, rely=0.8)
        self.delete = Button(self.root, text='Delete',
                             command=lambda: self.delete_equation())
        self.delete.place(relx=0.1, rely=0.8)
        self.close = Button(self.root, text='Close',
                            command=lambda: self.close_window())
        self.close.place(relx=0.5, rely=0.8)
        self.convert_button = Button(self.root, text='Convert',
                                     command=lambda: self.convert())
        self.convert_button.place(relx=0.8, rely=0.7)
        self.error_label = Label(self.root, text='error=')
        self.error_label.place(relx=0.1, rely=0.55)
        self.error_ent = Entry(self.root, width=5)
        self.error_ent.place(relx=0.3, rely=0.55)
        if self.cartesian_equation != None:
            self.cartesian_equation_ent.insert(0, self.cartesian_equation)
        # Inserts the current values of the variables (which will be default
        # if the Equation object has been created for the first time)
        self.start_x_ent.insert(0, self.start_x)
        self.end_x_ent.insert(0, self.end_x)
        self.start_y_ent.insert(0, self.start_y)
        self.end_y_ent.insert(0, self.endY)
        self.start_z_ent.insert(0, self.start_z)
        self.end_z_ent.insert(0, self.endZ)
        self.accuracy_ent.insert(0, self.accuracy)
        self.error_ent.insert(0, self.error)

    def parametric_window(self):
        self.parent_window.parametric_equation_windows.append(self)
        Label(self.root, text='x =', font='Calibri 15').grid(column=0, row=0)
        Label(self.root, text='y =', font='Calibri 15').grid(column=0, row=1)
        Label(self.root, text='z =', font='Calibri 15').grid(column=0, row=2)
        self.x_equation_ent = Entry(self.root, font='Calibri 15')
        self.x_equation_ent.grid(column=1, row=0)
        self.y_equation_ent = Entry(self.root, font='Calibri 15')
        self.y_equation_ent.grid(column=1, row=1)
        self.z_equation_ent = Entry(self.root, font='Calibri 15')
        self.z_equation_ent.grid(column=1, row=2)
        apply = Button(self.root, text='Apply',
                       command=lambda: self.set_info_parametric(self.x_equation_ent.get(),
                                                                self.y_equation_ent.get(),
                                                                self.z_equation_ent.get(),
                                                                self.start_value_ent.get(),
                                                                self.end_value_ent.get(),
                                                                self.accuracy_ent.get()))
        apply.grid(column=5, row=5)
        delete = Button(self.root, text='Delete',
                        command=lambda: self.delete_equation())
        delete.grid(column=1, row=5)
        close = Button(self.root, text='Close',
                       command=lambda: self.close_window())
        close.grid(column=2, row=5)
        self.start_value_ent = Entry(self.root, width=7, font='Calibri 10')
        self.start_value_ent.grid(column=2, row=3)
        self.end_value_ent = Entry(self.root, width=7, font='Calibri 10')
        self.end_value_ent.place(relx=0.7, rely=0.65)
        self.t_range_label = Label(self.root, text='≤ t ≤', font='Calibri 10')
        self.t_range_label.place(relx=0.6, rely=0.65)
        # Inserts the current values of the variables if they exist
        if self.x_equation is not None:
            self.x_equation_ent.insert(0, self.x_equation)
            self.y_equation_ent.insert(0, self.y_equation)
            self.z_equation_ent.insert(0, self.z_equation)
        self.start_value_ent.insert(0, self.start_value)
        self.end_value_ent.insert(0, self.end_value)
        self.accuracy_ent.insert(0, self.accuracy)

    def convert(self):
        self.parent_window.equations.remove(self)  # Removes any record of the equation
        for point in self.points:  # Iterates throiugh list of points
            point.equation = None  # Sets equation to None
            self.parent_window.points.append(point)  # Adds point to points
            if self in self.parent_window.selected_equations:  # If the equation was selected,
                self.parent_window.selected_points.append(point)  # so will the points

        if self in self.parent_window.selected_equations:
            self.parent_window.selected_equations.remove(self)  # Removes any record of the equation
        self.root.destroy()  # Closes root

    # Closes the tkinter root after which the rest of the program will continue to run
    def close_window(self):
        self.root.destroy()
        self.window_open = False

    def slider_settings(self):
        if not self.showSliders:
            for equation in self.parent_window.equations:
                equation.showSliders = False
            self.showSliders = True

    # Removes the Equation object from the Graph object's listOfEquations and
    # all the Point objects from the points
    def delete_equation(self):
        if self in self.parent_window.equations:
            self.parent_window.equations.remove(self)

        if self in self.parent_window.selected_equations:
            self.parent_window.selected_equations.remove(self)

        self.close_window()

    def calculate_points(self):
        # Attributes aliased as local variables so that the eval() function
        # will use these values
        a = self.a
        b = self.b
        c = self.c
        d = self.d
        # Ensures that all the required variables have been converted to the
        # right data type
        start_value = eval(syntax_correction(self.start_value))
        end_value = eval(syntax_correction(self.end_value))
        x_equation = syntax_correction(self.x_equation)
        y_equation = syntax_correction(self.y_equation)
        z_equation = syntax_correction(self.z_equation)
        accuracy = eval(self.accuracy)

        # Removes all the older points before the new points are calculated
        for point in self.points:
            if point in self.parent_window.points:
                self.parent_window.points.remove(point)

        self.points = []  # Initialises new list
        self.points2 = []  # Initialises new list
        try:
            t = self.sliders[len(self.sliders) - 2].variable
            self.limit1_point2.set_cor(t, eval(syntax_correction(self.y_equation)), 0)
            t = self.sliders[len(self.sliders) - 1].variable
            self.limit2_point2.set_cor(t, eval(syntax_correction(self.y_equation)), 0)
        except:
            pass

        # Loops through all the values of 't' in the given range and increment
        if self.type == 'parametric':
            self.calculate_parametric_points(accuracy, end_value, start_value, x_equation, y_equation, z_equation)

        elif self.type == 'cartesian':
            self.calculate_cartesian_points()

        for point in self.points2:
            if point != '':
                self.points.append(point)

    def calculate_cartesian_points(self):
        if True:
            # All the attributes are evaluated and changed to local variables
            # of the same name
            start_x = eval(syntax_correction(self.start_x))
            end_x = eval(syntax_correction(self.end_x))
            start_y = eval(syntax_correction(self.start_y))
            end_y = eval(syntax_correction(self.endY))
            start_z = eval(syntax_correction(self.start_z))
            end_z = eval(syntax_correction(self.endZ))
            accuracy = eval(self.accuracy)

            tracker_x = 0
            tracker_y = 0
            tracker_z = 0

            # This loop is equivalent to iterating through a three-dimensional array
            x = start_x
            while x <= end_x:
                y = start_y  # Resets y
                while y <= end_y:
                    z = start_z  # Resets z
                    while z <= end_z:
                        try:
                            equation = list(syntax_correction(self.cartesian_equation))
                            l = len(equation)
                            i = 0
                            while i < l:
                                if equation[i] == '=':
                                    equation.insert(i, '=')
                                    l = l + 1
                                    i = i + 2
                                else:
                                    i = i + 1

                            if eval(''.join(equation)):
                                p = Point(self.parent_window)
                                p.equation = self
                                p.set_cor(x, y, z)
                                self.points2.append(p)
                            else:
                                lhs = eval(self.listOfSides[0])
                                i = 1
                                # Iterates through all the indivudual
                                # expressions that must be equal ot each other
                                while i < len(self.listOfSides):
                                    rhs = eval(self.listOfSides[i])
                                    # This condition is there because the
                                    # second condition doesn't work if one
                                    # of the values is zero
                                    if round(lhs, 3) == round(rhs, 3):
                                        if i == len(self.listOfSides) - 1:
                                            # Creates Point object with
                                            # satisfying coordinates
                                            p = Point(self.parent_window)
                                            p.equation = self
                                            p.set_cor(x, y, z)
                                            self.points2.append(p)
                                    # Allows a margin of error as
                                    # expressions may not be exactly equal
                                    elif (lhs * rhs >= 0
                                          and 1 - (self.error / 100) <=
                                          abs(lhs / rhs) <= 1 + (self.error / 100)):
                                        # If loop has reached the last
                                        # expressions then the Point object is created
                                        if i == len(self.listOfSides) - 1:
                                            p = Point(self.parent_window)
                                            p.equation = self
                                            p.set_cor(x, y, z)
                                            self.points2.append(p)
                                    else:
                                        break
                                    i = i + 1
                        except:
                            pass

                        z = z + accuracy  # Increments z coordinate
                        if z > end_z and tracker_z == 0:  # To ensure that the last
                            z = end_z
                            tracker_z = 1
                    y = y + accuracy
                    if y > end_y and tracker_y == 0:
                        tracker_y = 1
                x = x + accuracy
                if x > end_x and tracker_x == 0:
                    x = end_x
                    tracker_x = 1

            self.parent_window.get_screen().fill((255, 255, 255))

    def calculate_parametric_points(self, accuracy, end_value, start_value, x_equation, y_equation, z_equation):
        t = start_value
        tracker = 0
        while t <= end_value:
            try:
                # Each coordinate is evaluated based on the value of t and
                # the alphabetical constants
                x = eval(x_equation)
                y = eval(y_equation)
                z = eval(z_equation)
                # Creates Point object, sets the coordinates and adds it to
                # the points so that they are transformed with the
                # rest of the points
                # Python automatically calculates complex solutions of an
                # equation which cannot be plotted
                if (type(x), type(y), type(z)) != (complex, complex, complex):
                    p = Point(self.parent_window)
                    p.equation = self
                    p.set_cor(x, y, z)
                    self.points2.append(p)
                else:
                    if not self.points:
                        # Represents an undefined point so that there is a
                        # gap in the graph at this point
                        self.points2.append('')
                    elif self.points[len(self.points) - 1] != '':
                        # Represents an undefined point so that there is a
                        # gap in the graph at this point
                        self.points2.append('')
            except:
                # If there is an error while evaluating the expression, such
                # as ZeroDivision or TypeError
                if not self.points:
                    # Represents an undefined point so that there is a gap in
                    # the graph at this point
                    self.points2.append('')
                elif self.points2[len(self.points) - 1] != '':
                    self.points.append('')

            t = round(t + accuracy, 3)  # Increments the variable by the
            # To ensure that the last point given in the range is also included
            if t > end_value and tracker == 0:
                t = end_value
                tracker = 1  # To prevent the code being stuck in an infinite loop

    # ZeroDivisionError or TypeError or NameError

    def set_info_parametric(self, xEquation, yEquation, zEquation, startValue,
                            endValue, accuracy='0.05'):
        a = self.a
        b = self.b
        c = self.c
        d = self.d
        e = self.e
        # Assigns values to the correct variable
        self.x_equation = xEquation
        self.y_equation = yEquation
        self.z_equation = zEquation
        self.start_value = startValue
        self.end_value = endValue
        self.accuracy = accuracy

        self.calculate_points()  # Calculates the points using the above information

        self.slider_settings()
        # Adds Equation object to list of equation of Graph class
        if self not in self.parent_window.equations:
            self.parent_window.equations.append(self)
        try:
            t = self.limit1
            self.limit1Point1.set_cor(self.limit1, 0, 0)
            self.limit1_point2.set_cor(self.limit1,
                                       eval(syntax_correction(self.y_equation)), 0)
            t = self.limit2
            self.limit2Point1.set_cor(self.limit2, 0, 0)
            self.limit2_point2.set_cor(self.limit2,
                                       eval(syntax_correction(self.y_equation)), 0)
        except:
            pass

        self.parent_window.main()  # Runs the main method to quickly plot graph

    def set_info_cartesian(self, cartesian_equation, startX, endX, startY, endY,
                           startZ, endZ, accuracy, error):
        # Attributes to local variables with same name
        a = self.a
        b = self.b
        c = self.c
        d = self.d
        self.cartesian_equation = cartesian_equation  # Expression to calculate points
        cartesian_equation = syntax_correction(cartesian_equation)  # Equation in Python syntax

        # Assigns attributes to the values given by user
        self.start_x = startX
        self.end_x = endX
        self.start_y = startY
        self.endY = endY
        self.start_z = startZ
        self.endZ = endZ
        self.accuracy = accuracy
        self.error = eval(error)

        self.listOfSides = cartesian_equation.split("=")  # Lists of individual expressions

        self.parent_window.showFact()  # Shows an interesting fact while calculating points
        self.calculate_points()  # Calculates points
        self.slider_settings()
        if self not in self.parent_window.equations:  # Adds Equation object to list of equations
            self.parent_window.equations.append(self)

        self.parent_window.main()  # Runs the main method to quickly plot graph

    def __get_state__(self):
        attributes = self.__dict__.copy()
        try:
            for attr in ('root',):
                del attributes[attr]
        except:
            pass

        return attributes
