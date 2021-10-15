from image import Image
from utils import random_colour, show_multiline_text, show_text
from maths.matrices import *
import pygame
from math import sqrt
from tkinter import Label, Button, Entry, Tk
from random import randint
from string_formatting import syntax_correction


class Point:  # Used to display individual points on the screen
    def __init__(self, parentWindow, createSlider=True):
        from buttons import Buttons

        self.parent_window = parentWindow
        self.cor = ()

        self.pos_vec = None
        self.radius = None

        self.x = None
        self.y = None
        self.z = None

        self.window_open = False

        self.radius = 5
        self.screen_pos = None

        self.colour = random_colour()
        self.equation = None

        self.line = None

        self.x2 = ''
        self.y2 = ''
        self.z2 = ''

        self.trace = False
        self.trace_points = []
        self.t = 0

        if createSlider:
            from slider import Slider
            self.slider = Slider('t', 't', 5, 100, -10, 10, self.parent_window,
                                 self, 100, 50, '', 0)
        try:
            self.axesTransformation = self.parent_window.axes_transformation
            self.width = self.parent_window.width
            self.height = self.parent_window.height
        except:
            pass

        self.prevCor = ''
        self.text = ''

    def visible(self):  # Checks if point is visible onscreen
        if (0 <= self.screen_pos[0] <= self.parent_window.width
                and 0 <= self.screen_pos[1] <= self.parent_window.height):
            return True
        else:
            return False

    def draw_trace(self):
        # Iterates through all the previous position points
        for i in range(0, len(self.trace_points)):
            p = self.trace_points[i]
            ratio = (i + 1) / len(self.trace_points)  # Percentage of index

            if self.parent_window.gradient_for_trace:
                colourRatio = ratio  # Percentage of index
                # colourRatio = 1/(2*(1-e**(-(i+1))))
            else:
                colourRatio = 1

            if self.parent_window.trail_effect:
                radiusRatio = ratio / 1.0  # Percentage of index
            else:
                radiusRatio = 1

            p.colour = (int(colourRatio * self.colour[0]),
                        int(colourRatio * self.colour[1]),
                        int(colourRatio * self.colour[2]))  # Sets colour
            p.calculate_screen_pos()

            if i != 0:
                # Draws line between adjacent points
                if self.parent_window.line_for_trace:
                    pygame.draw.aaline(self.parent_window.get_screen(), (0, 0, 0),
                                       self.trace_points[i - 1].screen_pos, p.screen_pos)
                if p.visible():
                    p.show(int(self.parent_window.radius * radiusRatio), False)

    def screen_cor(self, x, y):
        x = x + self.width / 2
        y = self.height / 2 - y
        return int(x), int(y)

    def calculate_screen_pos(self):
        if self.pos_vec is not None:
            self.axesTransformation = self.parent_window.axes_transformation
            screen_pos = matrix_multiply(self.axesTransformation, self.pos_vec)
            screen_pos = self.screen_cor(screen_pos[0][0], screen_pos[1][0])
            self.screen_pos = (screen_pos[0] + self.parent_window.x_translation,
                               screen_pos[1] + self.parent_window.y_translation)

    def show(self, radius=None, showLabel=True):
        if radius is None:
            radius = self.parent_window.radius

        # try:
        if (len(self.parent_window.selected_points) == 1
                and self in self.parent_window.selected_points):
            t = self.t
        else:
            t = self.parent_window.t
        # except:
        # pass

        if (self.parent_window.brownian_motion
                and self in self.parent_window.selected_points):
            self.set_cor(self.x + randint(-self.parent_window.random_speed,
                                          self.parent_window.random_speed),
                         self.y + randint(-self.parent_window.random_speed,
                                          self.parent_window.random_speed),
                         self.z + randint(-self.parent_window.random_speed,
                                          self.parent_window.random_speed))

        if 't' in self.x2:
            # try:
            self.set_cor(eval(syntaxCorrection(self.x2)), self.y, self.z)
            # except:
            # pass
        if 't' in self.y2:
            try:
                self.set_cor(self.x, eval(syntaxCorrection(self.y2)), self.z)
            except:
                pass

        if 't' in self.z2:
            try:
                self.set_cor(self.x, self.y, eval(syntaxCorrection((self.z2))))
            except:
                pass

        self.calculate_screen_pos()

        if self.equation is not None:
            if self.equation.type == 'cartesian':
                if self.equation in self.parent_window.selected_equations:
                    pygame.draw.circle(self.parent_window.get_screen(),
                                       (255, 0, 0), self.screen_pos, radius + 1, 0)

                pygame.draw.circle(self.parent_window.get_screen(),
                                   self.equation.colour, self.screen_pos, radius, 0)

            if self.mouse_over_point():
                show_text(self.parent_window.get_screen(), str(self.cor),
                          self.screen_pos[0] + int(self.parent_window.radius * 1.2),
                          self.screen_pos[1] + radius + 20, (255, 0, 0), (255, 255, 255), 20)

                pygame.draw.circle(self.parent_window.get_screen(), self.colour,
                                   self.screen_pos, radius + 1, 0)

        elif self.equation is None:
            text = '(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ')'
            if self.parent_window.show_coordinates:
                show_text(self.parent_window.get_screen(), text,
                          self.screen_pos[0] + radius + 20, self.screen_pos[1] + radius + 20,
                          (255, 0, 0), (255, 255, 255), 20)

            if self in self.parent_window.selected_points:
                pygame.draw.circle(self.parent_window.get_screen(), (255, 0, 0),
                                   self.screen_pos, radius + 2, 0)
            elif self in self.parent_window.points:
                pygame.draw.circle(self.parent_window.get_screen(), (0, 0, 0),
                                   self.screen_pos, radius + 2, 0)

            # pygame.draw.circle(self.parent_window.getScreen(), (255,255,255),self.screenPos,radius+1,0)
            pygame.draw.circle(self.parent_window.get_screen(), self.colour,
                               self.screen_pos, radius, 0)
            if showLabel and self.text != '':
                show_multiline_text(self.parent_window.get_screen(), self.text, self.screen_pos[0],
                                    self.screen_pos[1] - radius - 15, (255, 0, 0), (255, 255, 255), 25)

    def mouse_over_point(self):
        if self.screen_pos is not None:
            dx = self.screen_pos[0] - pygame.mouse.get_pos()[0]
            dy = self.screen_pos[1] - pygame.mouse.get_pos()[1]
            if sqrt(dx ** 2 + dy ** 2) <= self.parent_window.radius:
                return True

            return False

    def close_window(self):
        self.root.destroy()
        self.window_open = False

    # Window for Point settings which has Delete, Cancel and Apply buttons
    def window(self, x=None, y=None):  # Pointwindow
        self.root = Tk()
        self.set_current_window()
        self.parent_window.point_windows.append(self)
        self.root.bind('<Enter>', lambda event: self.set_current_window())
        # self.settings_window.bind('<Leave>', lambda event: self.resetCurrentWindow())
        self.window_open = True
        self.root.attributes('-topmost', True)  # Makes sure that the root opens on top of the Pygame root.
        self.root.title('Point Properties')

        if x is None:
            x, y = (pygame.mouse.get_pos()[0] + 10, pygame.mouse.get_pos()[1] + 10)

        # self.settings_window.geometry('260x80+'+str(x)+'+'+str(y)) # 'width x height + xcor + ycor'
        # User input for the x coordinate of the point
        # self.coordinateslabel = Label(self.settings_window, text='coordinates=')
        # self.coordinateslabel.grid(row = 0, column = 0, columnspan = 2)
        # User input for the x coordinate of the point

        self.coordinates_ent = Entry(self.root, width=20, font='Calibri 15')
        self.coordinates_ent.grid(row=0, column=0, columnspan=5)

        if self.pos_vec is not None:
            if 't' in self.x2 or (self.y2 or self.x2 or self.z2):
                self.coordinates_ent.insert(0, self.x2)
            else:
                self.coordinates_ent.insert(0, str(self.pos_vec[0][0]))

            if 't' in (self.y2 or self.x2 or self.z2):
                self.coordinates_ent.insert(len(self.coordinates_ent.get()), '|' + self.y2)
            else:
                self.coordinates_ent.insert(len(self.coordinates_ent.get()), ',' + str(self.pos_vec[1][0]))

            if 't' in (self.y2 or self.x2 or self.z2):
                self.coordinates_ent.insert(len(self.coordinates_ent.get()), '|' + self.z2)
            else:
                self.coordinates_ent.insert(len(self.coordinates_ent.get()), ',' + str(self.pos_vec[2][0]))

        apply = Button(self.root, text='Apply', command=lambda: self.cor_validation())
        # This button will effectively create the point (if the user inputs are valid)
        apply.grid(row=2, column=2)

        applyAndNew = Button(self.root, text='Apply and New', command=lambda: self.cor_validation(True))
        # This button will effectively create the point (if the user inputs are valid)
        applyAndNew.grid(row=2, column=3, columnspan=2)

        delete = Button(self.root, text='Delete', command=lambda: self.delete_point())
        delete.grid(row=2, column=5)

        Label(self.root, text='Label', width=5).grid(row=2, column=0)

        self.point_label = Entry(self.root, width=5, font='Calibri 15')
        self.point_label.grid(row=2, column=1)
        self.point_label.insert(0, self.text)

    def trace_setting(self):
        if self.trace:
            self.trace = False
        else:
            self.trace = True

    def delete_point(self):
        if self in self.parent_window.points:
            self.parent_window.points.remove(self)

        if self in self.parent_window.selected_points:
            self.parent_window.selected_points.remove(self)
        #  Deletes all lines which have itself as a point
        for line in self.parent_window.lines:
            if self in [line.point1, line.point2]:
                self.parent_window.lines.remove(line)
                if line in self.parent_window.selected_lines:
                    self.parent_window.selected_lines.remove(line)
        try:
            self.root.destroy()
        except:
            pass

    # To check if the coordinates entered by the user are valid
    def cor_validation(self, newPoint=False):
        valid_cor = True
        if (self in self.parent_window.selected_points
                and len(self.parent_window.selected_points) == 1):
            t = self.t
        else:
            t = self.parent_window.t

        cor = self.coordinates_ent.get().split(',')

        try:
            # The coordinates need to be integers because the pixels cannot
            # be decimals
            x = round(float(eval(syntax_correction(cor[0]))), 2)
            y = round(float(eval(syntax_correction(cor[1]))), 2)
            z = round(float(eval(syntax_correction(cor[2]))), 2)
        except:
            valid_cor = False

        if valid_cor:

            (self.x2, self.y2, self.z2) = tuple(cor)
            print((self.x2, self.y2, self.z2))
            self.set_cor(x, y, z)

            self.trace_points = []

            if self not in self.parent_window.points:
                self.parent_window.points.append(self)

            if newPoint:
                p = Point(self.parent_window)
                p.root(self.root.winfo_x(), self.root.winfo_y())

            self.text = self.point_label.get()
            self.close_window()

    def set_cor(self, x, y, z):
        (self.x, self.y, self.z) = (round(x, 3), round(y, 3), round(z, 3))
        self.pos_vec = [[x], [y], [z], [1]]
        self.cor = (round(x, 3), round(y, 3), round(z, 3))
        # (self.x2,self.y2,self.z2) = (str(x),str(y),str(z))

    # Takes the relevant information, gets the required transformation matrix
    # and transforms the point
    def transform_point(self, matrix):
        pos_vec = matrix_multiply(matrix, self.pos_vec)
        self.set_cor(pos_vec[0][0], pos_vec[1][0], pos_vec[2][0])

    def set_current_window(self):
        self.parent_window.current_window = self.root

    def reset_current_window(self):
        self.parent_window.current_window = None

    def __get_state__(self):
        attributes = self.__dict__.copy()
        try:
            for attr in ('root', 'coordinates_ent', 'point_label'):
                del attributes[attr]
        except:
            pass

        return attributes
