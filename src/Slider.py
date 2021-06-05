from Point import Point
from src.StringFormatting import syntax_correction
from utils import show_multiline_text
import pygame
from tkinter import Tk, Label, Entry, Button


class Slider:  # Used for controlling the values of variables in the given range
    def __init__(self, text, variable, x, y, startValue, endValue, parentWindow,
                 parentObject, width, height, typeOfValues, default):
        # The object to which the variable belongs
        self.parentObject = parentObject
        self.width = width  # Size of silder
        self.height = height
        self.text = text  # Text of variable
        self.parentWindow = parentWindow
        self.variableName = variable  # Name of variable
        self.variable = None  # Value of variable
        self.x = x  # Position of top left corner of slider
        self.y = y
        self.startValue = startValue  # Left end of slider
        self.endValue = endValue  # Right end of slider
        # Pointer to drag and change the value of the variable
        self.pointer = Point(parentWindow, False)
        self.pointer.parent_window = self
        self.radius = 10
        self.move_pointer = False  # To determine if the user wants to
        self.typeOfValues = typeOfValues  # Integer or float type values
        self.set_value(default)
        self.set_variable()
        self.windowOpen = False

    def window(self):  # Sliderwindow
        self.root = Tk()
        self.windowOpen = True
        self.parentWindow.slider_windows.append(self)
        # Ensures that the root will be in focus
        self.root.after(1, lambda: self.root.focus_force())
        self.windowOpen = True
        # Makes sure that the root opens on top of the Pygame root.
        self.root.attributes('-topmost', True)
        self.root.title('Slider Properties')

        cord = str(pygame.mouse.get_pos()[0] + 10) + '+' + str(pygame.mouse.get_pos()[1] + 10)
        self.root.geometry('260x60+' + cord)  # 'width x height + xcor + ycor'
        # Label for the start value of the slider
        self.startlabel = Label(self.root, text='start=')
        self.startlabel.place(relx=0.05, rely=0.1)
        # Label for the end value of the slider
        self.endlabel = Label(self.root, text='end=')
        self.endlabel.place(relx=0.25, rely=0.1)
        # Label for the start value of the slider variable
        self.valuelabel = Label(self.root, text='value=')
        self.valuelabel.place(relx=0.45, rely=0.1)
        # User input for the start value of the slider
        self.startent = Entry(self.root, width=5)
        self.startent.insert(0, self.startValue)
        self.startent.place(relx=0.05, rely=0.4)
        # User input for the end value of the slider
        self.endent = Entry(self.root, width=5)
        self.endent.insert(0, self.endValue)
        self.endent.place(relx=0.25, rely=0.4)
        # User input for the value of the slider variable
        self.valueent = Entry(self.root, width=5)
        self.valueent.insert(0, self.variable)
        self.valueent.place(relx=0.45, rely=0.4)

        self.apply = Button(self.root, text='Apply',
                            command=lambda: self.change_values(self.startent.get(),
                                                               self.endent.get(),
                                                               self.valueent.get()))
        # This button will effectively create the point (if the inputs are valid)
        self.apply.place(relx=0.8, rely=0.1)

        self.close = Button(self.root, text='Close',
                            command=lambda: self.root.destroy())
        self.close.place(relx=0.8, rely=0.5)

    def change_values(self, start, end, value):
        start = eval(syntax_correction(start))
        end = eval(syntax_correction(end))
        value = eval(syntax_correction(value))

        if start <= value <= end:
            (self.startValue, self.endValue) = (start, end)
            self.set_value(value)
            self.set_variable()
            if self.text in ['a', 'b', 'c', 'd', 'e']:
                self.parentObject.calculate_points()

            self.root.destroy()

    def mouse_over_slider(self):
        if (self.x < pygame.mouse.get_pos()[0] < self.x + self.width
                and self.y < pygame.mouse.get_pos()[1] < self.y + self.height):
            return True
        return False

    def set_value(self, value):
        self.variable = value
        unit = (self.endValue - self.startValue) / self.width
        self.pointer.set_cor(self.x + int((value - self.startValue) / unit),
                             int(self.y + self.height * 0.75), 0)
        self.pointer.screen_pos = (self.pointer.x, self.pointer.y)

    # Finds what percentage of the way the pointer is and adds that percentage
    # of the range to the start value
    def calculate_value(self):
        self.variable = self.startValue
        ratio = (self.pointer.x - self.x) / self.width
        self.variable += abs((self.endValue - self.startValue) * ratio)
        self.variable = round(self.variable, 3)

        if self.typeOfValues == 'integers':
            self.variable = int(self.variable)

    def set_variable(self):
        self.calculate_value()
        exec('self.parentObject.' + self.variableName + '=' + str(self.variable))
        try:
            a = self.parentObject.a
            b = self.parentObject.b
            c = self.parentObject.c
            d = self.parentObject.d
        except:
            pass

        if self.text == 'limit1':
            self.parentObject.limit1 = self.variable
            t = self.variable
            if self.parentObject.y_equation != '':
                try:
                    self.parentObject.limit1Point1.set_cor(self.variable, 0, 0)
                    self.parentObject.limit1_point2.set_cor(self.variable,
                                                            eval(syntax_correction(self.parentObject.y_equation)), 0)
                except:
                    pass

        elif self.text == 'limit2':
            self.parentObject.limit2 = self.variable
            t = self.variable
            if self.parentObject.y_equation != '':
                try:
                    self.parentObject.limit2Point1.set_cor(self.variable, 0, 0)
                    self.parentObject.limit2_point2.set_cor(self.variable,
                                                            eval(syntax_correction(self.parentObject.y_equation)), 0)
                except:
                    pass

    def draw_slider(self):
        # Displays the value of the variable
        show_multiline_text(self.parentWindow.get_screen(), self.text + ' = ' + str(round(self.variable, 2)),
                            self.pointer.x, self.pointer.y - 20, (255, 0, 0), (255, 255, 255), 20)
        # Draws the scroll line
        pygame.draw.line(self.parentWindow.get_screen(), self.parentObject.colour,
                         (int(self.x), int(self.y + self.height * 0.75)),
                         (int(self.x + self.width), int(self.y + self.height * 0.75)), 1)
        # pygame.draw.rect(self.parent_window.getScreen(), (0,0,0), (self.x, self.y, self.width,
        # self.height), 1) # Draws the border of the slider panel
        # Draws pointer
        pygame.draw.circle(self.parentWindow.get_screen(), (0, 0, 200),
                           (int(self.pointer.x), self.pointer.y), self.radius, 0)
