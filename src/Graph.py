from Buttons import Buttons
from Slider import Slider
from Image import Image
from Point import Point
from Line import Line
from Equation import Equation
from utils import *
from maths.Transformations import *
from maths.Matrices import *
from maths.Mathematical_Functions import *
from maths.Mathematical_Constants import *
from math import pi
from StringFormatting import syntax_correction, entry_formatter, substitute_values
from tkinter import *
import utils
import pygame


class Graph:
    def __init__(self, width, height, parent_app):
        self.parent_app = parent_app
        self.type = None
        self.width = width
        self.height = height
        self.colour = (0, 0, 0)
        self.t = 0  # Point control variable 

        # These are lists required to keep track of and access all the different
        # objects created during the execution of the program
        self.points = []
        self.buttons = []
        self.transformation_types = ['Rotation', 'Reflection', 'Scale']
        self.lines = []
        self.equations = []
        self.selected_points = []
        self.selected_equations = []
        self.selected_lines = []
        self.images = []

        self.x_axes_sf = 40  # Zoom value
        self.y_axes_sf = 40  # Zoom value
        self.z_axes_sf = 40  # Zoom value
        # Used to determine which transformation must be performed next on the selected points
        self.transformationParametersList = []

        self.buttons_created = False
        self.drop_point = False

        self.rotation_angle = 20  # How many degrees to rotate points by at every instance
        self.radius = 10  # Radius of circles representing points

        self.axes_transformation = [[1, 0, 0, 0],
                                    [0, 1, 0, 0],
                                    [0, 0, 1, 0],
                                    [0, 0, 0, 1]]
        self.active_transformations = []

        self.point_transformation = [[1, 0, 0, 0],
                                     [0, 1, 0, 0],
                                     [0, 0, 1, 0],
                                     [0, 0, 0, 1]]  # Identity matrix

        self.rotate_axes = False  # Does the user want to see the points from a different perspective?
        self.axes_rotation_mouse_pos = None  # Position of the mouse the instant the user activates the axes rotation
        # function
        self.x_rotation = 0.0  # Angle my which axes have been rotated about the x-axis
        self.y_rotation = 0.0  # Angle my which axes have been rotated about the y-axis
        self.zRotation = 0.0  # Angle my which axes have been rotated about the y-axis
        self.prev_x_rotation = 0.0  # alias for 'self.xRotation'
        self.prev_y_rotation = 0.0  # alias for 'self.yRotation'

        self.translate_axes = False  # Does the user want to scroll around the view?
        self.axes_translation_mouse_pos = None  # Position of the mouse the instant the user activates the translation
        # function
        self.x_translation = 0  # Amount to shift in horizontal direction
        self.y_translation = 0  # Amount to shift in vertical direction
        self.prev_x_translation = 0  # alias for 'self.xTranslation'
        self.prev_y_translation = 0  # alias for 'self.yTranslation'

        self.translation_amount = 1  # How many units to translate points by at every instance

        self.brownian_motion = False
        self.random_speed = 5

        self.light_background = True
        # These points will be used as a reference to draw the axes
        self.grid_lines = []
        self.axis_points = []

        self.draw_grid = True
        # Calculating points at the end of gridlines and creating line
        self.calculate_grid_points(20, 20, 20, 1, 1, 1, 0, 0, 0)

        self.x1 = Point(self)
        self.x1.set_cor(-self.width, 0, 0)
        self.x2 = Point(self)
        self.x2.set_cor(self.width, 0, 0)

        self.y1 = Point(self)
        self.y1.set_cor(0, -self.width, 0)
        self.y2 = Point(self)
        self.y2.set_cor(0, self.width, 0)

        self.z1 = Point(self)
        self.z1.set_cor(0, 0, self.width)
        self.z2 = Point(self)
        self.z2.set_cor(0, 0, -self.width)

        self.axis_points.append(self.x1)
        self.axis_points.append(self.x2)
        self.axis_points.append(self.y1)
        self.axis_points.append(self.y2)
        self.axis_points.append(self.z1)
        self.axis_points.append(self.z2)

        self.origin = Point(self)
        self.origin.set_cor(0, 0, 0)
        self.axis_points.append(self.origin)

        # View control variables
        self.show_coordinates = False

        self.showAxes = True
        self.draw_grid = True

        # Selection tool
        self.select = False  # Determines whether the user is usign the selection tool
        self.selection_point1 = ()  # The initial point where the user starts defining the area to be selected
        self.selection_point2 = ()  # The final point where the user chooses the area
        self.unselect = False
        self.temp_selected_points = []

        self.show_trace = True  # Draw trace of points
        self.gradient_for_trace = False  # Draw with gradient colour
        self.line_for_trace = False  # Draw lines between points
        self.trail_effect = False
        self.repeat_trace = False

        self.show_tab = False
        self.factList = [
            'Did you know..., that 1729 is the smallest number that can be represented as the sum of cubes of two '
            'pairs of integers:, 1729 = 9^3 + 10^3 = 12^3 + 1^3',
            'Did you know..., that the sum of the reciprocals of the squares of the natural numbers is pi^2/6?',
            'This fibonacci joke is as bad as the last two combined']
        self.jokeList = []

        x, y = 950, 0
        width, height = 100, 50
        self.sliders = [Slider('radius', 'radius', x, y, 1, 20, self,
                               self, width, height, 'integers', 10),
                        Slider('rotation angle', 'rotationAngle', x + 2 * width, y,
                               4, 90, self, self, width, height, 'integers', 30),
                        Slider('t', 't', x + 4 * width, y, -10, 10, self, self, width,
                               height, '', 0),
                        Slider('random speed', 'randomSpeed', x + 6 * width, y, 0,
                               10, self, self, width, height, 'integers', 5)]

        self.notes = False  # Determines which mode to switch to
        self.strokes = [[]]  # List of points drawn by user
        self.collect_points = False  # Determines if the current position of a mouse is part of the latest stroke

        self.fact = True

        self.point_windows = []
        self.parametric_equation_windows = []
        self.cartesian_equations_windows = []
        self.slider_windows = []
        self.image_windows = []

        self.line_of_best_fit = Equation(self, 'parametric')
        (self.line_of_best_fit.x_equation,
         self.line_of_best_fit.y_equation,
         self.line_of_best_fit.z_equation) = ('t', 'at+b', '0')
        self.show_line_of_best_fit = False

        self.show_number_line = False

        self.button_selected = False

        self.current_window = None

        self.show_xy_axes = True
        self.show_xz_axes = True
        self.show_yz_axes = True

        self.two_d_mode = False
        self.settings_window = None

    def get_screen(self):
        return utils.screen

    def create_settings_window(self):
        self.settings_window = Tk()
        self.settings_window.title('Settings')
        self.settings_window.geometry('400x500+' + str(int(self.width / 2)) + '+' + str(int(0)))
        self.settings_window.attributes('-topmost', True)

        trace_label = Label(self.settings_window, text="Trace Settings")
        trace_label.grid(row=0, column=0)

        a = BooleanVar()
        gradient_button = Checkbutton(self.settings_window, background='white',
                                      text="Gradient colouring", variable=a,
                                      onvalue=True, offvalue=False,
                                      command=lambda a=a,
                                                     self=self: exec("self.gradient_for_trace = a.get()"))
        gradient_button.grid(row=1, column=0)
        if self.gradient_for_trace:
            gradient_button.select()

        b = BooleanVar()
        trail_button = Checkbutton(self.settings_window, background='white',
                                   text="Trail effect", variable=b,
                                   onvalue=True, offvalue=False,
                                   command=lambda b=b,
                                                  self=self: exec("self.trail_effect = b.get()"))
        trail_button.grid(row=2, column=0)
        if self.trail_effect:
            trail_button.select()

        c = BooleanVar()
        line_button = Checkbutton(self.settings_window, background='white',
                                  text="Draw lines", variable=c,
                                  onvalue=True, offvalue=False,
                                  command=lambda c=c,
                                                 self=self: exec("self.line_for_trace = c.get()"))
        line_button.grid(row=3, column=0)
        if self.line_for_trace:
            line_button.select()

        d = BooleanVar()
        repeat_button = Checkbutton(self.settings_window, background='white',
                                    text="Repeat trace", variable=d,
                                    onvalue=True, offvalue=False,
                                    command=lambda d=d,
                                                   self=self: exec("self.repeat_trace = d.get()"))
        repeat_button.grid(row=4, column=0)
        if self.repeat_trace:
            repeat_button.select()

        Label(self.settings_window, text="Other").grid(row=6, column=0)
        e = BooleanVar()
        number_button = Checkbutton(self.settings_window, background='white',
                                    text="Numberline", variable=e,
                                    onvalue=True, offvalue=False,
                                    command=lambda e=e,
                                                   self=self: exec("self.show_number_line = e.get()"))

        number_button.grid(row=7, column=0)

        Label(self.settings_window, text="Axes grid").grid(row=8, column=0)
        f = BooleanVar()
        f.set(True)
        number_button = Checkbutton(self.settings_window, background='white',
                                    text="X-Y plane", variable=f,
                                    onvalue=True, offvalue=False,
                                    command=lambda f=f,
                                                   self=self: exec("self.show_xy_axes = f.get()"))
        number_button.grid(row=9, column=0)

        g = BooleanVar()
        g.set(True)
        number_button = Checkbutton(self.settings_window, background='white',
                                    text="X-Z plane", variable=g,
                                    onvalue=True, offvalue=False,
                                    command=lambda g=g,
                                                   self=self: exec("self.show_xz_axes = g.get()"))
        number_button.grid(row=9, column=1)

        h = BooleanVar()
        h.set(True)
        number_button = Checkbutton(self.settings_window, background='white',
                                    text="Y-Z plane", variable=h,
                                    onvalue=True, offvalue=False,
                                    command=lambda h=h,
                                                   self=self: exec("self.show_yz_axes = h.get()"))
        number_button.grid(row=10, column=0)

        if self.show_number_line:
            number_button.select()

    def showFact(self):
        img = pygame.image.load(IMAGES_PATH + 'Loading' + '.jpg')
        # self.parent_app.getScreen().blit(img, (int(self.width*0.4),int(self.height*0.2)))
        show_multiline_text(self.parent_app.get_screen(),
                            'Please wait while we calculate the points on your graph. Thank You',
                            int(self.width / 2), 10, (0, 0, 0), (200, 200, 200), 35)
        if self.fact:
            # self.fact = False
            randNum = randint(0, len(self.factList) - 1)
            y = int(self.height / 2)
            show_multiline_text(self.parent_app.get_screen(),
                                'Please wait while we calculate the points on your graph. Thank You',
                                int(self.width / 2), y - 50, (0, 0, 0), (200, 200, 200), 35)
            show_multiline_text(self.parent_app.get_screen(), self.factList[randNum], int(self.width / 2), y,
                                (0, 0, 0), (200, 200, 200), 35)
        else:
            jokes = ['Joke1']
            # self.fact  = True
            i = randint(1, 5)
            show_image(self.parent_app.get_screen(), 'Joke' + str(i), self.width / 4, 50)
        pygame.display.update()

    # Takes the relevant information, gets the required transformation matrix and transforms the point
    def get_transformation_matrix(self, transformation, prop1=None,
                                  prop2=None, prop3=None):
        if transformation == 'Rotation':
            matrix = rotation(prop2, prop1)

        elif transformation == 'Reflection':
            matrix = reflection(prop1)

        elif transformation == 'Scale':
            matrix = scale(prop1, prop2, prop3)

        elif transformation == 'Translation':
            matrix = translation(prop1, prop2, prop3)

        elif transformation == 'RotationAboutLine':
            matrix = [[1, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]]  # Identity matrix

            for line in self.selected_lines:  # Iterates through all the selected lines
                # Combines transformations for individual lines by multiplying the matrices
                matrix = matrix_multiply(matrix, rotation_about_line(prop2, line))

        return matrix

    def set_cor(self, x, y, z):
        self.x, self.y, self.z = round(x, 3), round(y, 3), round(z, 3)
        self.posvec = [[x], [y], [z], [1]]
        self.cor = [x, y, z]

    #  List of all the buttons and their properties which are created at the start of the program
    def create_buttons(self):

        list_of_images = ["/Close", "/Point", "/Parametric Equation", "/Cartesian Equation", "/Line", "/Rotation",
                          "/Reflection", "/Scale", "/Coordinates", "/Coordinates", "/Reset View", "/Zoom In",
                          "/Zoom Out"]
        # [title       ,text              ,x   ,y   ,width ,height ,radius ,shape,     font_size, font_colour      ,
        # border_colour,    bg_colour,       parent_window, image_file]
        listOfButtons = [
            ['Image', 'Image', self.width - 50, 1, 50, 50, None, 'rectangle', 30, colours['black'], colours['black'],
             colours['white'], ''],
            ['Add Point', 'Add,Point', 50, 40, 50, 50, None, 'rectangle', 30, colours['black'], colours['black'],
             colours['white'], 'Point'],
            ['Parametric Equation', 'Parametric,Equation', 100, 40, 50, 50, None, 'rectangle', 30, colours['black'],
             colours['black'], colours['white'], 'Parametric Equation'],
            ['Cartesian Equation', 'Cartesian,Equation', 150, 40, 50, 50, None, 'rectangle', 30, colours['black'],
             colours['black'], colours['white'], 'Cartesian Equation'],
            ['Add Line', 'Add,Line', 200, 40, 50, 50, None, 'rectangle', 30, colours['black'], colours['black'],
             colours['white'], 'Line'],
            ['Rotation', 'Rotation', 250, 40, 50, 50, None, 'rectangle', 30, colours['black'], colours['black'],
             colours['white'], 'Rotation'],
            ['Reflection', 'Reflection', 300, 40, 50, 50, None, 'rectangle', 30, colours['black'], colours['black'],
             colours['white'], 'Reflection'],
            ['Scale', 'Scale', 350, 40, 50, 50, None, 'rectangle', 30, colours['black'], colours['black'],
             colours['white'], 'Scale'],
            ['Coordinates', 'Show,Coordinates', 400, 40, 50, 50, None, 'rectangle', 30, colours['black'],
             colours['black'], colours['white'], 'Coordinates'],
            ['Axes Display', 'Hide,Axes', 450, 40, 50, 50, None, 'rectangle', 30, colours['black'], colours['black'],
             colours['white'], 'Coordinates'],
            ['Reset View', 'Reset,View', self.width - 60, self.height - 50, 50, 50, None, 'rectangle', 30,
             colours['black'], colours['black'], colours['white'], 'Reset View'],
            ['Zoom In', 'Zoom,In', self.width - 60, self.height - 150, 50, 50, None, 'rectangle', 30, colours['black'],
             colours['black'], colours['white'], 'Zoom In'],
            ['Zoom Out', 'Zoom,Out', self.width - 60, self.height - 100, 50, 50, None, 'rectangle', 30,
             colours['black'], colours['black'], colours['white'], 'Zoom Out'],
            ['NegativeXTranslation', '-X', self.width - 90, 90, 120, 30, 30, 'circle', 30, colours['black'],
             colours['red'], colours['white'], ''],
            ['PositiveXTranslation', '+X', self.width - 30, 90, 120, 30, 30, 'circle', 30, colours['black'],
             colours['red'], colours['white'], ''],
            ['NegativeYTranslation', '-Y', self.width - 90, 150, 120, 30, 30, 'circle', 30, colours['black'],
             colours['green'], colours['white'], ''],
            ['PositiveYTranslation', '+Y', self.width - 30, 150, 120, 30, 30, 'circle', 30, colours['black'],
             colours['green'], colours['white'], ''],
            ['NegativeZTranslation', '-Z', self.width - 90, 210, 120, 30, 30, 'circle', 30, colours['black'],
             colours['blue'], colours['white'], ''],
            ['PositiveZTranslation', '+Z', self.width - 30, 210, 120, 30, 30, 'circle', 30, colours['black'],
             colours['blue'], colours['white'], ''],
            ['Select', 'Select', 500, 40, 50, 50, None, 'rectangle', 30, colours['black'], colours['black'],
             colours['white'], 'Select'],
            ['Drop Points', 'Drop,Points', 550, 40, 50, 50, None, 'rectangle', 30, colours['black'], colours['black'],
             colours['white'], 'Drop Points'],
            ['Brownian Motion', 'Brownian,Motion', 600, 40, 50, 50, None, 'rectangle', 30, colours['black'],
             colours['black'], colours['white'], 'Brownian Motion'],
            ['Grid Lines', 'Hide,Grid', 650, 40, 50, 50, None, 'rectangle', 30, colours['black'], colours['black'],
             colours['white'], 'Grid'],
            ['Turn Right', 'Turn Right   ', self.width - 60, self.height - 250, 50, 50, None, 'rectangle', 30,
             colours['black'], colours['black'], colours['white'], ''],
            ['Turn Left', 'Turn Left    ', self.width - 60, self.height - 300, 50, 50, None, 'rectangle', 30,
             colours['black'], colours['black'], colours['white'], ''],
            ['Turn Up', 'Turn Up   ', self.width - 60, self.height - 350, 50, 50, None, 'rectangle', 30,
             colours['black'], colours['black'], colours['white'], ''],
            ['Turn Down', 'Turn Down    ', self.width - 60, self.height - 400, 50, 50, None, 'rectangle', 30,
             colours['black'], colours['black'], colours['white'], ''],
            ['Delete', 'Delete,Selection,', 700, 40, 50, 50, None, 'rectangle', 30, colours['black'], colours['black'],
             colours['white'], 'Delete'],
            ['Background', 'Dark,Mode', 750, 40, 50, 50, None, 'rectangle', 30, colours['black'], colours['black'],
             colours['white'], 'Background'],
            ['Left Click Toggle', 'Rotate,View', 800, 40, 50, 50, None, 'rectangle', 30, colours['black'],
             colours['black'], colours['white'], 'Left Click Toggle'],
            ['Notes', 'Notes', 850, 40, 50, 50, None, 'rectangle', 30, colours['black'], colours['black'],
             colours['white'], 'Pen'],
            ['Clear', 'Clear', self.width - 60, self.height - 200, 50, 50, None, 'rectangle', 30, colours['black'],
             colours['black'], colours['white'], ''],
            ['Trace', 'Hide Trace', self.width - 60, self.height - 450, 50, 50, None, 'rectangle', 30, colours['black'],
             colours['black'], colours['white'], ''],
            ['LOBF', 'Show,LOBF', self.width - 100, 0, 50, 50, None, 'rectangle', 30, colours['black'],
             colours['black'], colours['white'], ''],
            ['Settings', 'Settings', self.width - 150, 0, 50, 50, None, 'rectangle', 30, colours['black'],
             colours['black'], colours['white'], 'gear']]

        for button in listOfButtons:
            button_object = Buttons(button[0], button[1], button[2], button[3],
                                    button[4], button[5], button[6], button[7],
                                    button[8], button[9], button[10], button[11],
                                    self, button[12])
            self.buttons.append(button_object)

    # This function responds to the inputs given by the user. This is like the OS of the entire program.
    def check_events(self):
        self.button_selected = False
        if self.notes:  # Note mode
            self.check_note_events()
            return

        if pygame.key.get_pressed()[pygame.K_b]:
            self.brownian_motion = True

        if pygame.key.get_pressed()[pygame.K_n]:
            self.brownian_motion = False

        if pygame.key.get_pressed()[pygame.K_c]:
            for point in self.selected_points:
                point.trace_points = []

        if pygame.key.get_pressed()[pygame.K_y]:
            self.zRotation += 5

        if pygame.key.get_pressed()[pygame.K_u]:
            self.zRotation -= 5

        if pygame.key.get_pressed()[pygame.K_h]:
            self.x_axes_sf = 40
            self.y_axes_sf = 40
            self.z_axes_sf = 40

        for event in self.parent_app.get_events():
            # This is necessary for the root to close easily
            if event.type == pygame.QUIT:
                objects = self.point_windows
                objects += self.parametric_equation_windows
                objects += self.cartesian_equations_windows
                objects += self.slider_windows
                objects += self.image_windows
                for obj in objects:
                    try:
                        obj.root.destroy()
                        obj.root = None
                    except:
                        continue
                if self.settings_window:
                    self.settings_window = None
            # If the user clicks the mouse
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:  # If user left clicks
                    # If the user clicks on a button it's command is initated
                    for button in self.buttons:
                        if button.mouse_over_button():
                            button.leftHold = True
                            button.leftClick = True
                            self.button_selected = True

                    # Checks if the user wants to move any slider
                    equation = None
                    if len(self.selected_equations) > 0:
                        last_index = len(self.selected_equations) - 1
                        equation = self.selected_equations[last_index]

                    elif len(self.equations) == 1:
                        equation = self.equations[0]

                    if equation is not None:
                        for slider in equation.sliders:
                            if slider.pointer.mouse_over_point():
                                slider.move_pointer = True
                                self.button_selected = True

                    if len(self.selected_points) == 1:
                        point = self.selected_points[0]
                        slider = point.slider
                        if slider.pointer.mouse_over_point():
                            slider.move_pointer = True
                            self.button_selected = True

                    for slider in self.sliders:
                        if slider.pointer.mouse_over_point():
                            slider.move_pointer = True
                            self.button_selected = True

                    if not self.button_selected:

                        # Checks if the user has clicks on any point
                        for point in self.points:
                            # If the user has clicked on a point...
                            if point.mouse_over_point():
                                self.button_selected = True
                                # If the point was already selected ...
                                if point in self.selected_points:
                                    # It is unselected...
                                    self.selected_points.remove(point)
                                    # If the point is individual and wasn't selected
                                elif point.equation is None:
                                    # It is selected
                                    self.selected_points.append(point)
                                break

                        for equation in self.equations:
                            # If equation was already selected then it is unselected
                            if equation.mouse_over_graph():
                                self.button_selected = True
                                if equation in self.selected_equations:
                                    self.selected_equations.remove(equation)
                                    equation.thickness = 1  # Normal thickness

                                else:  # Equation is selected
                                    self.selected_equations.append(equation)
                                    equation.thickness = 2  # Bold
                                break

                        for line in self.lines:
                            if line.mouse_over_line():
                                self.button_selected = True
                                if line in self.selected_lines:
                                    self.selected_lines.remove(line)
                                    # print(self.listOfSelectedLines)

                                else:
                                    self.selected_lines.append(line)
                                    # print(self.listOfSelectedLines)
                                break

                        # If the user left-clicks but doesn't click on any
                        # button then that means the user has clicked on the screen

                        if self.select:
                            # First vertex of rectangle
                            self.selection_point1 = pygame.mouse.get_pos()
                            self.button_selected = True

                        elif self.drop_point:
                            self.create_point()
                            self.button_selected = True

                        # To determine if the user wants to move an image
                        for image in self.images:
                            if image.mouseOverImage():
                                self.button_selected = True
                                image.move = True
                                self.button_selected = True
                                break

                        if self.rotate_axes:
                            self.axes_rotation_mouse_pos = pygame.mouse.get_pos()
                        elif self.select:
                            pass
                        else:
                            self.axes_translation_mouse_pos = pygame.mouse.get_pos()
                            self.axes_rotation_mouse_pos = None
                            self.translate_axes = True
                            self.select = False

                # If the user presser the middle button i.e. the scroll bar
                # button then that means the user wants to rotate the axes
                elif event.button == 2:
                    self.rotate_axes = True
                    # Records the position of the mouse when the user
                    # presses the middle button to calculate the angle by
                    # which the axes need to be rotated
                    self.axes_rotation_mouse_pos = pygame.mouse.get_pos()

                # If the user right clicks on a point, if the point is a
                # part of an equation, then the equation's root is
                # displayed or else the point's individual root is displayed
                elif event.button == 3:
                    for point in self.points:
                        if (point.mouse_over_point()
                                and point.equation is None):
                            if not point.window_open:
                                point.root()
                        if (point.slider.mouse_over_slider()
                                and point in self.selected_points
                                and len(self.selected_points) == 1):
                            if not point.slider.window_open:
                                point.slider.root()
                    # Opens the root of an equation object if user
                    # right-clicks on graph
                    for equation in self.equations:
                        if equation != self.line_of_best_fit:
                            if (equation.mouse_over_graph()
                                    and not equation.window_open):
                                equation.root()
                            for slider in equation.sliders:
                                if (slider.mouse_over_slider()
                                        and (equation in self.selected_equations
                                             or len(self.equations) == 1)):
                                    if not slider.window_open:
                                        slider.root()

                    for slider in self.sliders:
                        if (slider.mouse_over_slider()
                                and not slider.windowOpen):
                            slider.window()

                    if self.select:
                        self.selection_point1 = pygame.mouse.get_pos()
                        # Indicates that the user wants to unselect
                        self.unselect = True

                    for image in self.images:
                        if image.mouseOverImage():
                            if not image.window_open:
                                image.root()

                # If the user scrolls up
                if event.button == 4:
                    self.x_axes_sf *= 1.1
                    self.y_axes_sf *= 1.1
                    self.z_axes_sf *= 1.1

                # If the user scrolls down
                if event.button == 5:
                    self.x_axes_sf *= 0.9
                    self.y_axes_sf *= 0.9
                    self.z_axes_sf *= 0.9

            # If the user releases any of the mouse buttons
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.collect_points = False
                    if self.rotate_axes:
                        self.axes_rotation_mouse_pos = None
                        self.prev_x_rotation = self.x_rotation
                        self.prev_y_rotation = self.y_rotation

                    if self.select:
                        if self.selection_point1 != ():
                            # Resets attributes back to original state
                            self.selection_point1 = ()
                            self.temp_selected_points = []

                    for button in self.buttons:
                        if (button.leftClick
                                and button.mouse_over_button()):
                            button.left_click_command()
                            button.leftClick = False
                        button.leftHold = False

                    self.translate_axes = False
                    self.prev_x_translation = self.x_translation
                    self.prev_y_translation = self.y_translation

                    for equation in self.equations:
                        if equation.showSliders:
                            for slider in equation.sliders:
                                slider.move_pointer = False

                    for point in self.points:
                        point.slider.move_pointer = False

                    for slider in self.sliders:
                        slider.move_pointer = False

                    for image in self.images:
                        image.move = False

                elif event.button == 2:
                    self.rotate_axes = False
                    self.prev_x_rotation = self.x_rotation
                    self.prev_y_rotation = self.y_rotation

                elif event.button == 3:
                    # Resets attributes back to the original state
                    if self.select:
                        self.unselect = False
                        self.selection_point1 = ()
                        self.temp_selected_points = []

    def check_note_events(self):
        for button in self.buttons:
            if button.title in ['Notes', 'Clear']:
                button.show_button()
        for event in self.parent_app.get_events():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Undo function
            if (pygame.key.get_pressed()[pygame.K_LCTRL]
                    and pygame.key.get_pressed()[pygame.K_z]):
                if len(self.strokes) == 1:
                    self.strokes = [[]]
                else:
                    # Deletes latest stroke
                    del self.strokes[-1]

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Only these two buttons work in this mode
                    for button in self.buttons:
                        if (button.title in ['Notes', 'Clear']
                                and button.mouse_over_button()):
                            button.left_click_command()
                            break
                    # Adds a new stroke with the current mouse position as starting point
                    self.strokes.append([pygame.mouse.get_pos()])
                    self.collect_points = True  # Marks beginning of stroke

            if event.type == pygame.MOUSEMOTION:
                if self.collect_points:
                    # Adds the current position of the mouse to the latest stroke
                    if len(self.strokes) != 0:
                        self.strokes[-1].append(pygame.mouse.get_pos())

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.collect_points = False  # Completes stroke

    def select_points(self):
        for point in self.points:  # Iterates through all the individual points
            if point.equation is None:  # Checks if the onscreen x and y coordinates are in the region of the
                # rectangle selected by the user
                if (min(self.selection_point1[0], self.selection_point2[0]) <= point.screen_pos[0] <= max(
                        self.selection_point1[0], self.selection_point2[0])
                        and min(self.selection_point1[1], self.selection_point2[1]) <= point.screen_pos[1] <= max(
                            self.selection_point1[1], self.selection_point2[1])):
                    if point not in self.selected_points:  # Selects point if not already in the list
                        self.selected_points.append(point)
                    else:  # If the point is already in the list then it is removed
                        self.selected_points.remove(point)

    # Determines the transformation that the user wants to do on the points by looking at which button is clicked and
    # which key is pressed
    def determine_transformation(self):
        if 'Rotation' in self.active_transformations:
            info = 'Press the <- and -> keys to rotate about the y-axis,Press the up and down keys to rotate about ' \
                   'the x-axis,Press the Z and X to rotate about the z-axis '
            show_multiline_text(self.parent_app.get_screen(), info, int(self.width / 2),
                                110, (0, 0, 0), (200, 200, 200), 30)
            transformation = None
            if pygame.key.get_pressed()[pygame.K_RIGHT] != 0:
                transformation = ['Rotation', 'y', self.rotation_angle, None]

            if pygame.key.get_pressed()[pygame.K_LEFT] != 0:
                transformation = ['Rotation', 'y', -self.rotation_angle, None]

            if pygame.key.get_pressed()[pygame.K_UP] != 0:
                transformation = ['Rotation', 'x', self.rotation_angle, None]

            if pygame.key.get_pressed()[pygame.K_DOWN] != 0:
                transformation = ['Rotation', 'x', -self.rotation_angle, None]

            if pygame.key.get_pressed()[pygame.K_z] != 0:
                transformation = ['Rotation', 'z', -self.rotation_angle, None]

            if pygame.key.get_pressed()[pygame.K_x] != 0:
                transformation = ['Rotation', 'z', self.rotation_angle, None]

            if pygame.key.get_pressed()[pygame.K_r] != 0:
                transformation = ['RotationAboutLine', None,
                                  self.rotation_angle, None]

            if pygame.key.get_pressed()[pygame.K_t] != 0:
                transformation = ['RotationAboutLine', None,
                                  -self.rotation_angle, None]
            if transformation is not None:
                self.transformationParametersList.append(transformation)
        else:
            if pygame.key.get_pressed()[pygame.K_RIGHT] != 0:
                self.y_rotation += 10
            if pygame.key.get_pressed()[pygame.K_LEFT] != 0:
                self.y_rotation -= 10
            if pygame.key.get_pressed()[pygame.K_UP] != 0:
                self.x_rotation += 10
            if pygame.key.get_pressed()[pygame.K_DOWN] != 0:
                self.x_rotation -= 10

        if 'Reflection' in self.active_transformations:
            if (pygame.key.get_pressed()[pygame.K_a] != 0
                    or pygame.key.get_pressed()[pygame.K_d] != 0):
                self.transformationParametersList.append(['Reflection', 'x', None, None])

            if (pygame.key.get_pressed()[pygame.K_w] != 0
                    or pygame.key.get_pressed()[pygame.K_s] != 0):
                self.transformationParametersList.append(['Reflection', 'y', None, None])

            if (pygame.key.get_pressed()[pygame.K_q] != 0
                    or pygame.key.get_pressed()[pygame.K_e] != 0):
                self.transformationParametersList.append(['Reflection', 'z', None, None])
        else:
            if pygame.key.get_pressed()[pygame.K_a]:
                self.x_translation -= 5

            if pygame.key.get_pressed()[pygame.K_d]:
                self.x_translation += 5

            if pygame.key.get_pressed()[pygame.K_w]:
                self.y_translation -= 5

            if pygame.key.get_pressed()[pygame.K_s]:
                self.y_translation += 5

        if 'Scale' in self.active_transformations:
            if pygame.key.get_pressed()[pygame.K_PERIOD]:
                self.transformationParametersList.append(['Scale', 1.05, 1, 1])
            if pygame.key.get_pressed()[pygame.K_COMMA]:
                self.transformationParametersList.append(['Scale', 0.95, 1, 1])

            if pygame.key.get_pressed()[pygame.K_RIGHTBRACKET]:
                self.transformationParametersList.append(['Scale', 1, 1.05, 1])
            if pygame.key.get_pressed()[pygame.K_LEFTBRACKET]:
                self.transformationParametersList.append(['Scale', 1, 0.95, 1])

            if pygame.key.get_pressed()[pygame.K_RSHIFT]:
                self.transformationParametersList.append(['Scale', 1, 1, 1.05])
            if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                self.transformationParametersList.append(['Scale', 1, 1, 0.95])

        else:
            if pygame.key.get_pressed()[pygame.K_PERIOD]:
                self.x_axes_sf *= 1.05
            if pygame.key.get_pressed()[pygame.K_COMMA]:
                self.x_axes_sf *= 0.95

            if pygame.key.get_pressed()[pygame.K_RIGHTBRACKET]:
                self.y_axes_sf *= 1.05
            if pygame.key.get_pressed()[pygame.K_LEFTBRACKET]:
                self.y_axes_sf *= 0.95

            if pygame.key.get_pressed()[pygame.K_RSHIFT]:
                self.z_axes_sf *= 1.05
            if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                self.z_axes_sf *= 0.95
        # Calculates the matrix that transforms the point at this instance
        self.calculate_point_transformation()

    def calculate_point_transformation(self):
        # Initialises as the identity matrix
        self.point_transformation = [[1, 0, 0, 0],
                                     [0, 1, 0, 0, ],
                                     [0, 0, 1, 0],
                                     [0, 0, 0, 1]]
        # Iterates through each list containing the transformation parameters
        for transformationParameters in self.transformationParametersList:
            matrix = self.get_transformation_matrix(transformationParameters[0],
                                                    transformationParameters[1],
                                                    transformationParameters[2],
                                                    transformationParameters[3])  # Gets matrix
            # Multiplies matrices to combines into single matrix
            self.point_transformation = matrix_multiply(self.point_transformation, matrix)

        self.transformationParametersList = []  # Resets list to empty for next cycle

    def update_points(self):
        for point in self.points:  # Iterates through all points
            point.calculate_screen_pos()
            if self.selection_point1 != () and point.visible():  # Checks if point is within the selected region
                if (min(self.selection_point1[0], pygame.mouse.get_pos()[0]) <= point.screen_pos[0] <= max(
                        self.selection_point1[0], pygame.mouse.get_pos()[0])
                        and min(self.selection_point1[1], pygame.mouse.get_pos()[1]) <= point.screen_pos[1] <= max(
                            self.selection_point1[1], pygame.mouse.get_pos()[1])):

                    if not self.unselect:  # If the user is selecting
                        # If the point is not already selected
                        if point not in self.selected_points:
                            self.selected_points.append(point)  # it is added to the list
                            # To determine whether the poimt has been selected
                            # during current session
                            self.temp_selected_points.append(point)

                    elif self.unselect:  # If the user is unselecting
                        if point in self.selected_points:  # If the point was selected
                            self.selected_points.remove(point)  # It is removed
                            # To determine that it was unselected during current session
                            self.temp_selected_points.append(point)

                else:  # If point not in the region
                    if not self.unselect:  # If user is selecting
                        # If the point had been selected in this session
                        if point in self.temp_selected_points:
                            self.selected_points.remove(point)  # It is unselected
                            self.temp_selected_points.remove(point)

                    else:  # If user is unselecting
                        # If the point has been unselected during this session
                        if point in self.temp_selected_points:
                            self.selected_points.append(point)  # If selected again
                            self.temp_selected_points.remove(point)

            if self.show_trace:
                if self.repeat_trace:
                    list_of_cor = []
                else:
                    # Creates new list with only coordinates of points
                    list_of_cor = list(map(lambda x: x.cor, point.trace_points))

                cor = (point.x, point.y, point.z)  # Current coordinates of point

                if cor not in list_of_cor:  # Avoids duplication
                    if point.x is not None:
                        p = Point(self)
                        p.set_cor(point.x, point.y, point.z)
                        point.trace_points.append(p)

            if point in self.selected_points:
                if ('t' not in
                        syntax_correction(point.x2, False)
                        + syntax_correction(point.y2, False)
                        + syntax_correction(point.z2, False)):
                    point.transform_point(self.point_transformation)

            if point.visible():
                point.show()

            point.draw_trace()

            if point.window_open:
                pygame.draw.aaline(self.parent_app.get_screen(), point.colour,
                                   point.screen_pos,
                                   (point.create_settings_window.winfo_x(), point.create_settings_window.winfo_y()))

    def update_lines(self):
        for line in self.lines:
            if line.visible():
                line.draw_line()

    def screen_cor(self, pos_vec):
        x = pos_vec[0][0]
        y = pos_vec[1][0]
        x = x + self.width / 2
        y = self.height / 2 - y

        return int(x), int(y)

    def draw_gradient_background(self):
        # Draws background
        colour = 0
        rect_height = 10
        height = self.height - rect_height

        while height + rect_height > 0:
            if colour > 255:
                break
            pygame.draw.rect(self.parent_app.get_screen(), (colour, colour, colour),
                             (0, height, self.width, rect_height), 0)
            height -= rect_height
            colour = 255 - int(255 * (height / self.height))

    def draw_axes(self):
        for point in self.axis_points:
            point.calculate_screen_pos()

        self.draw_grid_lines()
        # Draws the lines representing the axes
        if self.showAxes:
            pygame.draw.line(self.parent_app.get_screen(), (255, 0, 0),
                             self.x1.screen_pos, self.x2.screen_pos, 3)
            pygame.draw.line(self.parent_app.get_screen(), (0, 200, 0),
                             self.y1.screen_pos, self.y2.screen_pos, 3)
            pygame.draw.line(self.parent_app.get_screen(), (0, 0, 255),
                             self.z1.screen_pos, self.z2.screen_pos, 3)

            # Labels each end of the axes with the required letter
            show_multiline_text(self.parent_app.get_screen(), '-X', self.x1.screen_pos[0],
                                self.x1.screen_pos[1], (0, 0, 0), (200, 200, 200), 30)
            show_multiline_text(self.parent_app.get_screen(), '+X', self.x2.screen_pos[0],
                                self.x2.screen_pos[1], (0, 0, 0), (200, 200, 200), 30)

            show_multiline_text(self.parent_app.get_screen(), '-Y', self.y1.screen_pos[0],
                                self.y1.screen_pos[1], (0, 0, 0), (200, 200, 200), 30)
            show_multiline_text(self.parent_app.get_screen(), '+Y', self.y2.screen_pos[0],
                                self.y2.screen_pos[1], (0, 0, 0), (200, 200, 200), 30)

            if (self.x_rotation, self.y_rotation) != (0.0, 0.0):
                show_multiline_text(self.parent_app.get_screen(), '+Z', self.z1.screen_pos[0],
                                    self.z1.screen_pos[1], (0, 0, 0), (200, 200, 200), 30)
                show_multiline_text(self.parent_app.get_screen(), '-Z', self.z2.screen_pos[0],
                                    self.z2.screen_pos[1], (0, 0, 0), (200, 200, 200), 30)

    def draw_grid_lines(self):
        for line in self.grid_lines:
            if (line.point1.z == line.point2.z == 0 and not self.show_xy_axes
                    or line.point1.y == line.point2.y == 0 and not self.show_xz_axes
                    or line.point1.x == line.point2.x == 0 and not self.show_yz_axes):
                continue

            if line.visible():
                if self.light_background:
                    line.colour = (150, 150, 150)
                else:
                    line.colour = (255, 255, 255)

                if self.draw_grid:
                    line.draw_line(self.show_number_line)

    def calculate_axes_transformation(self):
        # Rotates the axis by transforming the axis points by the angle and
        # scale factor required
        if self.translate_axes:
            dx = pygame.mouse.get_pos()[0] - self.axes_translation_mouse_pos[0]
            self.x_translation = self.prev_x_translation + dx
            dy = pygame.mouse.get_pos()[1] - self.axes_translation_mouse_pos[1]
            self.y_translation = self.prev_y_translation + dy

        elif self.rotate_axes and self.axes_rotation_mouse_pos:  # Checks if the axes need to be rotated
            self.y_rotation = (self.prev_y_rotation +
                               360 * (pygame.mouse.get_pos()[0] -
                                      self.axes_rotation_mouse_pos[0]) / self.width) % 360
            # This takes the previous angle by which the axes were rotated and then adds the additional angle which
            # is determined by the percentage of the distance between the point that the user pressed the middle
            # button and the current position of the mouse
            self.x_rotation = (self.prev_x_rotation +
                               360 * (pygame.mouse.get_pos()[1] -
                                      self.axes_rotation_mouse_pos[1]) / self.width) % 360
            self.two_d_mode = False

        # self.axesTransformation =  matrixMultiply(scale(self.XAxesSf,self.YAxesSf,self.ZAxesSf),rotation(
        # self.xRotation,'x'))
        self.axes_transformation = rotation(self.x_rotation, 'x')

        self.axes_transformation = matrix_multiply(self.axes_transformation,
                                                   rotation(self.y_rotation, 'y'))

        self.axes_transformation = matrix_multiply(self.axes_transformation,
                                                   rotation(self.zRotation, 'z'))

        self.axes_transformation = matrix_multiply(self.axes_transformation,
                                                   scale(self.x_axes_sf,
                                                         self.y_axes_sf,
                                                         self.z_axes_sf))

    def update_screen(self):
        if self.notes:
            self.draw_strokes()
        else:
            if self.selection_point1 != ():
                self.selection_point2 = pygame.mouse.get_pos()
                if not self.unselect:
                    colour = (0, 200, 0)
                else:
                    colour = (200, 0, 0)

                self.draw_selection_box(colour)

            self.calculate_axes_transformation()

            if self.parent_app.number_of_tabs < self.parent_app.max_tabs:
                self.parent_app.new_tab_button.show_button()

            self.draw_axes()
        # Changes the colour of the transformation buttons that are pressed

    def draw_strokes(self):
        for stroke in self.strokes:
            # Draws a 1 pixel circle if stroke is comprised of only one point
            if len(stroke) == 1:
                pygame.draw.circle(self.parent_app.get_screen(), (0, 0, 0),
                                   stroke[0], 1, 0)

            elif len(stroke) > 1:
                # Draws lines between adjacent points
                for i in range(0, len(stroke) - 2):
                    pygame.draw.aaline(self.parent_app.get_screen(), (0, 0, 0),
                                       stroke[i], stroke[i + 1], 1)

    def draw_selection_box(self, colour):
        width = pygame.mouse.get_pos()[0] - self.selection_point1[0]
        height = pygame.mouse.get_pos()[1] - self.selection_point1[1]

        pygame.draw.rect(self.parent_app.get_screen(), colour, (self.selection_point1[0],
                                                                self.selection_point1[1],
                                                                width, height), 2)

    def update_buttons(self):
        for button in self.buttons:

            button.show_button()  # Draws button onscreen

            button.hover = button.mouse_over_button()

            if button.hover:
                if button.shape == 'rectangle':
                    # button.parent_window.showText(button.text, int(button.x+button.width/2),
                    # int(button.y+button.height/2), button.font_colour, button.bg_colour, button.font_size+5)
                    y = button.y + button.height + 7 * len(button.text.split(','))
                    show_multiline_text(self.parent_app.get_screen(),
                                        button.text, int(button.x + button.width / 2),
                                        y, (0, 0, 0), (255, 255, 255), button.font_size + 5)

                elif button.shape == 'circle':
                    show_multiline_text(self.parent_app.get_screen(), button.text, button.x, button.y,
                                        button.font_colour, button.bg_colour, button.font_size + 5)
                # mouseImg = pygame.image.load('Mouse hand.png')
                # self.parent_app.getScreen().blit(mouseImg, pygame.mouse.get_pos())

        for button in self.buttons:
            # Keeps on translating the points as long as the button is held down
            if (button.leftHold
                    and button.title in ['PositiveXTranslation', 'NegativeXTranslation',
                                         'PositiveYTranslation', 'NegativeYTranslation',
                                         'PositiveZTranslation', 'NegativeZTranslation',
                                         'Zoom In', 'Zoom Out']):
                button.left_click_command()

            if button.mouse_over_button():
                button.bg_colour = (200, 200, 200)
            else:
                button.bg_colour = (255, 255, 255)

    def update_equations(self):
        if self.show_line_of_best_fit:
            points = []
            x_values = []
            for point in self.selected_points:
                if point.z == 0.0:  # Extracts all selected points on the x-y plane
                    points.append(point.cor)
                    x_values.append(point.cor[0])

            if len(points) > 1:  # Line has to be for more than one point
                line = regression(points)
                (self.line_of_best_fit.a, self.line_of_best_fit.b) = line
                # Line is drawn across the selected points only
                (self.line_of_best_fit.start_value,
                 self.line_of_best_fit.end_value) = (str(min(x_values)),
                                                     str(max(x_values)))

                self.line_of_best_fit.calculate_points()

                for point in self.line_of_best_fit.points:
                    point.calculate_screen_pos()

                self.line_of_best_fit.draw_graph()

        for equation in self.equations:
            for point in equation.get_points():
                point.transform_point(self.point_transformation)
                point.calculate_screen_pos()

                if self.show_trace and equation in self.selected_equations:
                    capture_trace = True

                    if len(point.trace_points) > 0:
                        if point.cor == point.trace_points[-1].cor:
                            capture_trace = False

                    if capture_trace:
                        p = Point(self)
                        p.set_cor(point.x, point.y, point.z)
                        point.trace_points.append(p)

                    point.draw_trace()

            equation.draw_graph()

        equation = None

        if len(self.selected_equations) > 0:
            i = len(self.selected_equations) - 1
            equation = self.selected_equations[i]

            if (equation == self.line_of_best_fit
                    and len(self.selected_equations) > 1):
                equation = self.selected_equations[i - 1]

        elif len(self.equations) == 2:
            equation = self.equations[1]

        if equation == self.line_of_best_fit and not self.show_line_of_best_fit:
            equation = None

        if equation is not None:
            if equation.type == 'parametric':
                show_text(self.parent_app.get_screen(),
                          'x = ' + substitute_values(equation, equation.xEquation) + ' | y = ' + substitute_values(
                              equation, equation.yEquation) + ' | z = ' + substitute_values(equation,
                                                                                            equation.zEquation),
                          self.width / 2, self.height - 180, equation.colour, (255, 255, 255), 20)
            else:
                show_text(self.parent_app.get_screen(), equation.cartesianEquation, self.width / 2,
                          self.height - 180, equation.colour, (255, 255, 255), 20)

        if self.line_of_best_fit.mouse_over_graph():
            equation = self.line_of_best_fit
            show_text(self.parent_app.get_screen(),
                      'x = ' + substitute_values(equation, equation.x_equation) + ' | y = ' + substitute_values(equation,
                                                                                                                equation.y_equation) + ' | z = ' + substitute_values(
                          equation, equation.z_equation),
                      pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                      equation.colour, (255, 255, 255), 20)

    def update_sliders(self):
        slider_active = False
        equation = None
        if len(self.selected_equations) > 0:
            equation = self.selected_equations[-1]
        elif len(self.equations) == 2:
            equation = self.equations[1]

        if equation == self.line_of_best_fit:
            equation = None

        if equation is not None:
            for slider in equation.sliders:
                if equation is not None:
                    if equation.type == 'parametric':
                        if (slider.text in ['limit1', 'limit2']
                                and equation.xEquation == 't' and equation.zEquation == '0'):

                            slider.start_value = eval(syntax_correction(equation.startValue))
                            slider.end_value = eval(syntax_correction(equation.endValue))
                            slider.draw_slider()

                            equation.limit1Point1.calculate_screen_pos()
                            equation.limit1Point2.calculate_screen_pos()
                            equation.limit2Point1.calculate_screen_pos()
                            equation.limit2Point2.calculate_screen_pos()

                            try:
                                pygame.draw.aaline(self.parent_app.get_screen(), self.colour,
                                                   equation.limit1Point1.screen_pos,
                                                   equation.limit1Point2.screen_pos)
                                pygame.draw.aaline(self.parent_app.get_screen(), self.colour,
                                                   equation.limit2Point1.screen_pos,
                                                   equation.limit2Point2.screen_pos)
                            except:
                                pass
                            show_multiline_text(
                                self.parent_app.get_screen(), 'Area:,Trp: ' +
                                                              str(
                                                                  round(
                                                                      integral(equation.yEquation, equation.limit1,
                                                                               equation.limit2, rule='trapezium',
                                                                               equation=equation), 5)) + ',Smp: ' +
                                                              str(
                                                                  round(
                                                                      integral(equation.yEquation, equation.limit1,
                                                                               equation.limit2, rule='simpsons',
                                                                               equation=equation), 5)),
                                50, int(self.height / 2), (0, 0, 0), (255, 255, 255), 20)

                        if (slider.text in syntax_correction(equation.xEquation, False) or
                                slider.text in syntax_correction(equation.yEquation, False) or
                                slider.text in syntax_correction(equation.zEquation, False)):
                            slider.draw_slider()

                    elif equation.type == 'cartesian':
                        if slider.text in equation.cartesianEquation:
                            slider.draw_slider()

                if slider.move_pointer:
                    slider_active = True
                    if slider.x <= pygame.mouse.get_pos()[0] <= slider.x + slider.width:
                        slider.pointer.set_cor(pygame.mouse.get_pos()[0], slider.pointer.y, slider.pointer.z)
                        slider.pointer.screen_pos = (pygame.mouse.get_pos()[0], slider.pointer.y)
                        slider.set_variable()
                        if 'limit' not in slider.text:
                            equation.calculatePoints()

        slider = []
        if len(self.selected_points) == 1:
            slider = [self.selected_points[0].slider]

        for slider in self.sliders + slider:
            slider.draw_slider()
            if slider.move_pointer:
                slider_active = True
                if slider.x < pygame.mouse.get_pos()[0] < slider.x + slider.width:
                    slider.pointer.set_cor(pygame.mouse.get_pos()[0], slider.pointer.y, slider.pointer.z)
                    slider.pointer.screen_pos = (pygame.mouse.get_pos()[0], slider.pointer.y)
                    slider.set_variable()

        return slider_active

    # Updates the windows for different objects and formats the user entries where required
    def update_windows(self):
        for point in self.point_windows:
            try:
                entry_formatter(point.coordinates_ent)
                point.create_settings_window.update_idletasks()
                point.create_settings_window.update()
            except:
                self.point_windows.remove(point)
                point.window_open = False

        for equation in self.parametric_equation_windows:
            try:
                entry_formatter(equation.x_equation_ent)
                entry_formatter(equation.y_equation_ent)
                entry_formatter(equation.z_equation_ent)
                entry_formatter(equation.start_value_ent)
                entry_formatter(equation.end_value_ent)

                equation.create_settings_window.update_idletasks()
                equation.create_settings_window.update()
            except:
                self.parametric_equation_windows.remove(equation)
                equation.window_open = False

        for equation in self.cartesian_equations_windows:
            try:
                entry_formatter(equation.cartesian_equation_ent)
                entry_formatter(equation.start_x_ent)
                entry_formatter(equation.end_x_ent)
                entry_formatter(equation.start_y_ent)
                entry_formatter(equation.end_y_ent)
                entry_formatter(equation.start_z_ent)
                entry_formatter(equation.end_z_ent)
                equation.create_settings_window.update_idletasks()
                equation.create_settings_window.update()
            except:
                self.cartesian_equations_windows.remove(equation)
                equation.window_open = False

        for slider in self.slider_windows:
            try:
                slider.create_settings_window.update_idletasks()
                slider.create_settings_window.update()
            except:
                self.slider_windows.remove(slider)
                slider.window_open = False

        for image in self.image_windows:
            try:
                image.create_settings_window.update_idletasks()
                image.create_settings_window.update()
            except:
                self.image_windows.remove(image)
                image.window_open = False
        try:
            self.settings_window.update_idletasks()
            self.settings_window.update()
        except:
            self.window_open = False

    def update_images(self):
        for image in self.images:
            if (self.x_rotation == image.xAngle and
                    self.y_rotation == image.yAngle and
                    self.zRotation == image.zAngle):
                if image.move:
                    # Sets position of image to position of mouse
                    (image.x, image.y) = pygame.mouse.get_pos()
                # Image is only displayed if the angles are the same as when
                image.show()

    # Calls all the methods necessary for the program to function properly
    def main(self):
        if not self.buttons_created:
            self.create_buttons()  # Creates the button objects required for the module
            self.buttons_created = True

        if not self.notes:
            for i in range(0, 3000):  # Updates the windows
                self.update_windows()

        # Draws appropriate background
        if not self.light_background:
            self.draw_gradient_background()
        else:
            self.parent_app.get_screen().fill((255, 255, 255))

        self.update_images()  # Performs tasks associated with images
        self.update_screen()

        self.check_events()  # Responds to all valid user inputs

        if self.notes:
            return

        self.determine_transformation()  # Checks user inputs to identify transformations
        self.update_points()  # Performs tasks associated with points
        self.update_lines()  # Performs tasks associated with lines
        self.update_equations()  # Performs tasks associated with equations

        if not (self.rotate_axes and self.axes_rotation_mouse_pos) and not self.translate_axes:
            slider_active = self.update_sliders()  # Performs tasks associated with sliders
            if not slider_active:
                self.update_buttons()  # Performs tasks associated with buttons

    def calculate_grid_points(self, x, y, z, stepX, stepY, stepZ, x2=0, y2=0,
                              z2=0, step=1):
        # Calculating points at the end of the grid lines and creates a line
        # joining them

        i = -x
        while i <= x:
            # XY plane parallels
            k = -z2
            while k <= z2:
                if k == 0:
                    text = str(i)
                else:
                    text = ''
                # print('|'+text)
                p1 = Point(self)
                p1.set_cor(i, y, k)
                self.axis_points.append(p1)
                p2 = Point(self)
                p2.set_cor(i, -y, k)
                self.axis_points.append(p2)
                l = Line(p1, p2, self, text)
                self.grid_lines.append(l)
                k += stepZ

            # XZ plane parallels
            j = -y2
            while j <= y2:
                p1 = Point(self)
                p1.set_cor(i, j, z)
                self.axis_points.append(p1)
                p2 = Point(self)
                p2.set_cor(i, j, -z)
                self.axis_points.append(p2)
                l = Line(p1, p2, self, text)
                self.grid_lines.append(l)
                j += stepY
            i += stepX

        j = -y
        while j <= y:
            # XY plane parallels
            k = -z2
            while k <= z2:
                if k == 0:
                    text = str(j)
                else:
                    text = ''

                p1 = Point(self)
                p1.set_cor(x, j, k)
                self.axis_points.append(p1)
                p2 = Point(self)
                p2.set_cor(-x, j, k)
                self.axis_points.append(p2)
                l = Line(p1, p2, self, text)
                self.grid_lines.append(l)
                k += stepZ

            # YZ plane parallels
            i = -x2
            while i <= x2:
                p1 = Point(self)
                p1.set_cor(i, j, z)
                self.axis_points.append(p1)
                p2 = Point(self)
                p2.set_cor(i, j, -z)
                self.axis_points.append(p2)
                l = Line(p1, p2, self)
                self.grid_lines.append(l)
                i += stepX

            j += stepY

        k = -z
        while k <= z:
            # XZ plane parallels
            i = -x2
            while i <= x2:
                if i == 0:
                    text = str(k)
                else:
                    text = ''
                p1 = Point(self)
                p1.set_cor(i, y, k)
                self.axis_points.append(p1)
                p2 = Point(self)
                p2.set_cor(i, -y, k)
                self.axis_points.append(p2)
                l = Line(p1, p2, self, text)
                self.grid_lines.append(l)
                i += stepX

            # YZ plane parallels
            j = -y2
            while j <= y2:
                p1 = Point(self)
                p1.set_cor(x, j, k)
                self.axis_points.append(p1)
                p2 = Point(self)
                p2.set_cor(-x, j, k)
                self.axis_points.append(p2)
                l = Line(p1, p2, self)
                self.grid_lines.append(l)
                j += stepY
            k += stepZ

    def create_point(self):
        valid = False
        # This calculates the coordinates of the point
        a = (pygame.mouse.get_pos()[0] - self.origin.screen_pos[0]) / self.x_axes_sf
        b = -(pygame.mouse.get_pos()[1] - self.origin.screen_pos[1]) / self.y_axes_sf
        point = Point(self)  # Creates new point object
        # Determines which dimension the two coordinates correspond to and sets coordinates accordingly
        if self.y_rotation == 0.0 and self.x_rotation == 0.0:
            point.set_cor(a, b, 0)
            valid = True

        elif self.y_rotation in (90.0, -270.0) and self.x_rotation == 0.0:
            point.set_cor(0, b, a)
            valid = True

        elif self.y_rotation in (180.0, -180.0) and self.x_rotation == 0.0:
            point.set_cor(-a, b, 0)
            valid = True

        elif self.y_rotation in (270.0, -90.0) and self.x_rotation == 0.0:
            point.set_cor(-a, b, 0)
            valid = True

        elif self.x_rotation in (90.0, -270.0) and self.y_rotation == 0.0:
            point.set_cor(a, 0, -b)
            valid = True

        elif self.x_rotation in (180.0, -180.0) and self.y_rotation == 0.0:
            point.set_cor(a, -b, 0)
            valid = True

        elif self.x_rotation in (270.0, -90.0) and self.y_rotation == 0.0:
            point.set_cor(a, 0, b)
            valid = True

        point.calculate_screen_pos()

        if valid:
            self.points.append(point)
