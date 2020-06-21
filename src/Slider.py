from Point import Point
from utils import showText
import pygame

class Slider: # Used for controlling the values of variables in the given range
    def __init__(self, text, variable, x, y,startValue, endValue, parentWindow,
                 parentObject, width, height, typeOfValues, default):
        # The object to which the variable belongs
        self.parentObject = parentObject
        self.width = width  # Size of silder
        self.height = height
        self.text = text # Text of variable
        self.parentWindow = parentWindow
        self.screen = self.parentWindow.screen
        self.variableName = variable # Name of variable
        self.variable = None # Value of variable
        self.x = x  # Position of top left corner of slider
        self.y = y
        self.startValue = startValue # Left end of slider
        self.endValue = endValue # Right end of slider
        # Pointer to drag and change the value of the variable
        self.pointer = Point(parentWindow, False)
        self.pointer.parentWindow = self
        self.radius = 10
        self.movePointer = False # To determine if the user wants to
        self.typeOfValues = typeOfValues # Integer or float type values
        self.setValue(default)
        self.setVariable()
        self.windowOpen = False

    def window(self): # Sliderwindow
        self.root = Tk()
        self.windowOpen = True
        self.parentWindow.listOfWindowSliders.append(self)
        # Ensures that the window will be in focus
        self.root.after(1, lambda: self.root.focus_force())
        self.windowOpen = True
        # Makes sure that the window opens on top of the Pygame window.
        self.root.attributes('-topmost', True)
        self.root.title('Slider Properties')

        cord = str(pygame.mouse.get_pos()[0]+10)+'+'+str(pygame.mouse.get_pos()[1]+10)
        self.root.geometry('260x60+'+cord) # 'width x height + xcor + ycor'
        # Label for the start value of the slider
        self.startlabel = Label(self.root, text='start=')
        self.startlabel.place(relx=0.05,rely=0.1)
        # Label for the end value of the slider
        self.endlabel = Label(self.root, text='end=')
        self.endlabel.place(relx=0.25,rely=0.1)
        # Label for the start value of the slider variable
        self.valuelabel = Label(self.root, text='value=')
        self.valuelabel.place(relx=0.45,rely=0.1)
        # User input for the start value of the slider
        self.startent = Entry(self.root, width = 5)
        self.startent.insert(0,self.startValue)
        self.startent.place(relx=0.05,rely=0.4)
        # User input for the end value of the slider
        self.endent = Entry(self.root, width = 5)
        self.endent.insert(0,self.endValue)
        self.endent.place(relx=0.25,rely=0.4)
        # User input for the value of the slider variable
        self.valueent = Entry(self.root, width = 5)
        self.valueent.insert(0,self.variable)
        self.valueent.place(relx=0.45,rely=0.4)

        self.apply = Button(self.root,text='Apply',
                            command = lambda: self.changeValues(self.startent.get(),
                                                              self.endent.get(),
                                                              self.valueent.get()))
        # This button will effectively create the point (if the inputs are valid)
        self.apply.place(relx=0.8,rely=0.1)

        self.close = Button(self.root,text='Close',
                            command = lambda: self.root.destroy())
        self.close.place(relx=0.8,rely=0.5)


    def changeValues(self, start, end, value):
        start = eval(syntaxCorrection(start))
        end = eval(syntaxCorrection(end))
        value = eval(syntaxCorrection(value))
        if (start <= value <= end):
            (self.startValue,self.endValue) = (start,end)
            self.setValue(value)
            self.setVariable()
            if (self.text in ['a','b','c','d','e']):
                self.parentObject.calculatePoints()
            self.root.destroy()

    def mouseOverSlider(self):
        if (self.x < pygame.mouse.get_pos()[0] < self.x+self.width
            and self.y < pygame.mouse.get_pos()[1] < self.y+self.height):
            return True
        return False

    def setValue(self, value):
        self.variable = value
        unit = (self.endValue - self.startValue)/self.width
        self.pointer.setCor(self.x + int((value-self.startValue)/unit),
                            int(self.y+self.height*0.75), 0)
        self.pointer.screenPos = (self.pointer.x, self.pointer.y)

    # Finds what percentage of the way the pointer is and adds that percentage
    # of the range to the start value
    def calculateValue(self):
        self.variable = self.startValue
        ratio = (self.pointer.x - self.x)/self.width
        self.variable += abs((self.endValue - self.startValue) * ratio)
        self.variable = round(self.variable, 3)

        if (self.typeOfValues == 'integers'):
            self.variable = int(self.variable)

    def setVariable(self):
        self.calculateValue()
        exec('self.parentObject.' + self.variableName + '=' + str(self.variable))
        try:
            a = self.parentObject.a
            b = self.parentObject.b
            c = self.parentObject.c
            d = self.parentObject.d
        except:
            pass


        if (self.text == 'limit1'):
            self.parentObject.limit1 = self.variable
            t = self.variable
            if (self.parentObject.yEquation != ''):
                try:
                    self.parentObject.limit1Point1.setCor(self.variable, 0, 0)
                    self.parentObject.limit1Point2.setCor(self.variable,
                                                          eval(syntaxCorrection(self.parentObject.yEquation)),
                                                          0)
                except:
                    pass
        elif (self.text == 'limit2'):
            self.parentObject.limit2 = self.variable
            t = self.variable
            if (self.parentObject.yEquation != ''):
                try:
                    self.parentObject.limit2Point1.setCor(self.variable, 0, 0)
                    self.parentObject.limit2Point2.setCor(self.variable,
                                                          eval(syntaxCorrection(self.parentObject.yEquation)),
                                                          0)
                except:
                    pass

    def drawSlider(self):
        # Displays the value of the variable
        showText(self.screen,self.text+' = '+str(round(self.variable,2)),
                 self.pointer.x, self.pointer.y-20, (255, 0, 0), (255, 255, 255), 20)
        # Draws the scroll line
        pygame.draw.line(self.screen, self.parentObject.colour,
                         (int(self.x), int(self.y+self.height*0.75)),
                         (int(self.x+self.width), int(self.y+self.height*0.75)), 1)
        #pygame.draw.rect(self.screen, (0,0,0), (self.x, self.y, self.width,
        # self.height), 1) # Draws the border of the slider panel
         # Draws pointer
        pygame.draw.circle(self.screen, (0,0,200),
                           (int(self.pointer.x), self.pointer.y), self.radius, 0)
