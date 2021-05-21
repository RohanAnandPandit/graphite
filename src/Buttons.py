import pygame
from tkinter import *
from utils import show_multiline_text, invert, show_image, IMAGES_PATH
from Equation import Equation
from Line import Line
import os


# The class is called 'Buttons' instead of 'Button' because 'Button' is a tkinter function
class Buttons:
    def __init__(self, title, text, x, y, width, height, radius, shape, font_size,
                 font_colour, border_colour, bg_colour, parent_window, image_file):
        from Point import Point
        self.parent_window = parent_window
        self.leftClick = False
        self.rightClick = False
        self.leftHold = False
        self.hover = False
        # Button properties
        self.x = x
        self.y = y
        self.title = title  # A buttons function is determined by it's title
        self.text = text
        self.active = False
        self.width = width
        self.height = height
        self.shape = shape
        self.radius = radius
        self.font_colour = font_colour
        self.border_colour = border_colour
        self.bg_colour = bg_colour
        self.font_bg = self.bg_colour
        self.font_size = font_size
        self.image = None
        self.image_file = image_file
        self.set_image()

    def set_image(self):
        if self.image_file != '':
            file_path = IMAGES_PATH + self.image_file + '.jpg'
            if os.path.exists(file_path):
                self.image = pygame.image.load(file_path).convert()

    # Determines if the mouse pointer is in the area of the button based on the shape
    def mouse_over_button(self):
        if self.shape == 'circle':
            dx = self.x - pygame.mouse.get_pos()[0]
            dy = self.y - pygame.mouse.get_pos()[1]
            if (dx ** 2 + dy ** 2) ** 0.5 <= self.radius + 5:
                return True
            return False

        elif self.shape == 'rectangle':
            if (self.x < pygame.mouse.get_pos()[0] < self.x + self.width
                    and self.y < pygame.mouse.get_pos()[1] < self.y + self.height):
                return True
            return False

    def hoverCommand(self):
        pass

    #  The procedure that need to be performed when the mouse is left clicked on the button
    def left_click_command(self):
        self.active = invert(self.active)

        if self.title == 'Add Point':
            from Point import Point
            point = Point(self.parent_window)
            point.window()

        # Makes a particular type of transformation active and the rest inactive
        if self.title in self.parent_window.transformation_types:
            if self.active:
                self.border_colour = (0, 0, 255)
                self.parent_window.active_transformations.append(self.text)

            else:
                self.border_colour = (0, 0, 0)
                self.parent_window.active_transformations.remove(self.text)

        # This button determines if the coordinates of a point should be
        # displayed on the screen
        if self.title == 'Coordinates':
            if self.parent_window.show_coordinates:
                self.parent_window.show_coordinates = False
                self.text = 'Show,Coordinates'
            else:
                self.parent_window.show_coordinates = True
                self.text = 'Hide,Coordinates'

        # Initial amount to translate by
        (x, y, z) = (0, 0, 0)
        # Depending on hte title of the button the amount is added/subtracted
        # from the local variables
        if self.title == 'PositiveXTranslation':
            x += self.parent_window.translation_amount

        if self.title == 'NegativeXTranslation':
            x -= self.parent_window.translation_amount

        if self.title == 'PositiveYTranslation':
            y += self.parent_window.translation_amount

        if self.title == 'NegativeYTranslation':
            y -= self.parent_window.translation_amount

        if self.title == 'PositiveZTranslation':
            z += self.parent_window.translation_amount

        if self.title == 'NegativeZTranslation':
            z -= self.parent_window.translation_amount

        if (x, y, z) != (0, 0, 0):
            # The coordinates of all selected points are translated
            for point in self.parent_window.selected_points:
                point.set_cor(point.x + x, point.y + y, point.z + z)

            for equation in self.parent_window.selected_equations:
                for point in equation.points:
                    if point != '':
                        point.set_cor(point.x + x, point.y + y, point.z + z)

        # Resets all the variables that affect the view to their original value
        if self.title == 'Reset View':
            self.parent_window.x_rotation = 0.0
            self.parent_window.y_rotation = 0.0
            self.parent_window.zRotation = 0.0

            self.parent_window.prev_x_rotation = 0.0
            self.parent_window.prev_y_rotation = 0.0

            self.parent_window.x_translation = 0
            self.parent_window.y_translation = 0

            self.parent_window.two_d_mode = True

        # An 'Equation' object is created even before any of it's equation and
        # ranges are assigned.
        # Calling the 'window' method allows the user to do so.
        if self.title == 'Parametric Equation':
            e = Equation(self.parent_window, 'parametric')
            e.window()

        if self.title == 'Cartesian Equation':
            e = Equation(self.parent_window, 'cartesian')
            e.window()

        # Controls whether the x,y and z axes are displayed
        if self.title == 'Axes Display':
            if self.parent_window.showAxes:
                self.parent_window.showAxes = False
                self.text = 'Show,Axes'
            else:
                self.parent_window.showAxes = True
                self.text = 'Hide,Axes'

        # When a user clicks on a mouse the point changes colour and gets added
        # to a list. Clicking on the 'Add Line' button will create a new 'Line' object
        # only if two points are selected
        if self.title == 'Add Line':
            # There must be at least two selected points to create line
            if len(self.parent_window.selected_points) >= 2:
                i = 1
                # Iterates through all the points and creates line object betewen adjacent point
                while i < len(self.parent_window.selected_points):
                    # Creates a new line object for the two points selected by the user
                    l = Line(self.parent_window.selected_points[i - 1],
                             self.parent_window.selected_points[i], self.parent_window)
                    self.parent_window.lines.append(l)
                    i = i + 1
                # If there are more than two points then creates a line between the first and last point
                if len(self.parent_window.selected_points) > 2:
                    l = Line(self.parent_window.selected_points[0],
                             self.parent_window.selected_points[-1],
                             self.parent_window)
                    self.parent_window.lines.append(l)

        if self.title == 'Zoom Out':
            self.parent_window.x_axes_sf = self.parent_window.x_axes_sf * 0.95
            self.parent_window.y_axes_sf = self.parent_window.y_axes_sf * 0.95
            self.parent_window.z_axes_sf = self.parent_window.z_axes_sf * 0.95

        if self.title == 'Zoom In':
            self.parent_window.x_axes_sf = self.parent_window.x_axes_sf * 1.05
            self.parent_window.y_axes_sf = self.parent_window.y_axes_sf * 1.05
            self.parent_window.z_axes_sf = self.parent_window.z_axes_sf * 1.05

        if self.title == 'Drop Points':
            self.parent_window.drop_point = invert(self.parent_window.drop_point)
            if self.parent_window.drop_point:
                self.border_colour = (0, 0, 255)
            else:
                self.border_colour = (0, 0, 0)

        if self.title == 'Brownian Motion':
            self.parent_window.brownian_motion = invert(self.parent_window.brownian_motion)
            if self.parent_window.brownian_motion:
                self.border_colour = (0, 0, 255)
            else:
                self.border_colour = (0, 0, 0)

        if self.title == 'Grid Lines':
            if self.text == 'Hide,Grid':
                self.text = 'Show,Grid'
            else:
                self.text = 'Hide,Grid'
            self.parent_window.draw_grid = invert(self.parent_window.draw_grid)

        if self.title == 'Turn Left':
            self.parent_window.y_rotation += 90.0
            self.parent_window.prev_y_rotation += 90.0

        if self.title == 'Turn Right':
            self.parent_window.y_rotation -= 90.0
            self.parent_window.prev_y_rotation -= 90.0

        if self.title == 'Turn Up':
            self.parent_window.x_rotation += 90.0
            self.parent_window.prev_x_rotation += 90.0

        if self.title == 'Turn Down':
            self.parent_window.x_rotation -= 90.0
            self.parent_window.prev_x_rotation -= 90.0

        if self.title == 'Select':
            self.parent_window.select = invert(self.parent_window.select)
            self.parent_window.translate_axes = False
            self.parent_window.rotate_axes = False
            if self.parent_window.select:
                self.border_colour = (0, 0, 255)
            else:
                self.border_colour = (0, 0, 0)

        if self.title == 'Delete':
            while len(self.parent_window.selected_points) > 0:
                self.parent_window.selected_points[0].delete_point()

            while len(self.parent_window.selected_lines) > 0:
                self.parent_window.selected_lines[0].delete_line()

        if self.title == 'Background':
            self.parent_window.light_background = invert(self.parent_window.light_background)
            if not self.parent_window.light_background:
                self.text = 'Light,Mode'
            else:
                self.parent_window.text = 'Dark,Mode'

        if self.title == 'Left Click Toggle':
            if self.text == 'Rotate,View':
                self.parent_window.rotate_axes = True
                self.text = 'Scroll,view'
            else:
                self.parent_window.rotate_axes = False
                self.parent_window.axes_rotation_mouse_pos = None
                self.text = 'Rotate,View'

            self.parent_window.select = False

        if self.title == 'Notes':
            self.parent_window.notes = invert(self.parent_window.notes)
            list_of_objects = self.parent_window.point_windows
            list_of_objects += self.parent_window.parametric_equation_windows
            list_of_objects += self.parent_window.artesian_equations_windows
            list_of_objects += self.parent_window.slider_windows
            list_of_objects += self.parent_window.image_windows

            for objects in list_of_objects:
                try:
                    objects.root.destroy()
                except:
                    continue

        if self.title == 'Clear':
            if self.parent_window.notes:
                if self.parent_window.collect_points:
                    # Allows current stroke to continue
                    self.parent_window.strokes = [[]]
                else:
                    self.parent_window.strokes = []  # Resets to original state
            else:
                for point in self.parent_window.points:
                    point.trace_points = []

                for equation in self.parent_window.equations:
                    for point in equation.points:
                        point.trace_points = []

        if self.title == 'Trace':
            if self.text == 'Hide Trace':
                self.text = 'Show Trace'
                self.parent_window.show_trace = False
            else:
                self.text = 'Hide Trace'
                self.parent_window.show_trace = True

        # Closes the program
        if self.title == 'Close':
            pygame.quit()
            sys.exit()

        if self.title == 'Image':
            i = Image(0, 0, self.parent_window.x_rotation, self.parent_window.y_rotation,
                      self.parent_window.zRotation, self.parent_window)
            i.window()  # Creates image object and opens it's window

        if self.title == 'LOBF':
            self.parent_window.show_line_of_best_fit = invert(self.parent_window.show_line_of_best_fit)
            if self.parent_window.show_line_of_best_fit:
                self.text = 'Hide,LOBF'
            else:
                self.text = 'Show,LOBF'

        if self.title == 'Settings':
            self.parent_window.settings_window()

    # Draws the button
    def show_button(self):
        if self.shape == 'rectangle':
            # Border
            pygame.draw.rect(self.parent_window.get_screen(), self.border_colour,
                             (self.x - 2, self.y + 2, self.width + 3, self.height + 3), 2)

            if self.image is not None:
                self.parent_window.get_screen().blit(self.image, (self.x, self.y))  # Image
            else:
                pygame.draw.rect(self.parent_window.get_screen(), self.bg_colour,
                                 (self.x, self.y, self.width, self.height), 0)  # Fill

                show_multiline_text(self.parent_window.get_screen(), self.text,
                                    int(self.x + self.width / 2),
                                    int(self.y + self.height / 2), self.font_colour,
                                    self.bg_colour, self.font_size, 20)

        elif self.shape == 'circle':
            pygame.draw.circle(self.parent_window.get_screen(), self.bg_colour,
                               (self.x, self.y),
                               self.radius, 0)  # Fill

            pygame.draw.circle(self.parent_window.get_screen(), self.border_colour,
                               (self.x, self.y),
                               self.radius, 1)  # Border

            if self.image is not None:
                try:
                    self.parent_window.get_screen().blit(self.image,
                                                         (self.x - self.radius, self.y - self.radius))
                except:
                    pass
            else:
                show_multiline_text(self.parent_window.get_screen(), self.text, self.x,
                                    self.y, (0, 0, 0), (255, 255, 255), self.font_size, 20)
