"""Imports"""
import pygame
pygame.init()
from tkinter import *
import time
from math import *
import sys
import os
""""""
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (2,28) # Makes sure that the program window appears at the top left corner of the monitor screen


"""------Maths Functions----------"""
#Certain mathematical functions are not defined within the math library of Python or not represented in the way people typically write the functions.
#Therefore by defining the following funcitons the in-built eval() function will be able to evaluate expressions inputted by the user which use these functions 
#for e.g. ln(y) = arcsin(x) 
def ln(x):
    return log(x,e)

def cosec(x):
    return 1/sin(x)

def sec(x):
    return 1/cos(x)

def cot(x):
    return 1/tan(x)

def cosech(x):
  return 1/sinh(x)

def sech(x):
  return 1/cosh(x)

def coth(x):
  return 1/tanh(x)

def arcsin(x):
  return asin(x)

def arcos(x):
  return acos(x)

def arccos(x):
  return acos(x)

def arctan(x):
  return atan(x)

def acosec(x):
  return asin(1/x)

def asec(x):
  return acos(1/x)

def acot(x):
  return atan(1/x)

def acosech(x):
  return asinh(1/x)

def asech(x):
  return acosh(1/x)

def acoth(x):
  return atanh(1/x)
#
def arcosec(x):
  return asin(1/x)

def arccosec(x):
  return asin(1/x)

def arcsec(x):
  return acos(1/x)

def arccot(x):
  return atan(1/x)

def arcot(x):
  return atan(1/x)

def arcosech(x):
  return asinh(1/x)

def arccosech(x):
  return asinh(1/x)

def arcsech(x):
  return acosh(1/x)

def arcoth(x):
  return atanh(1/x)

def arccoth(x):
  return atanh(1/x)

"""-------End of Mathematical functions-------------"""

"""----------------------------------------------------------------------------------------------------------------------------------"""

"""--------Matrix Operations-----------"""
#For more informaion about why these functions are required and how they work, see the 'Algorithms' section of the doumentation 

# Calculates the dot product of two 3-dimensional vectors
def dot(m1,m2):
    dotprod = m1[0]*m2[0]+m1[1]*m2[1]+ m1[2]*m2[2]
    return dotprod

# Multiplies the transformation matrix by the point's position vector and returns the new coordinates
def transform(pv,tm):  
    image = []
    for row in tm:
        image.append(dot(pv,row))
    return image

# Multiplies any two valid matrices
def matrixMultiply(m1,m2): 
    matprod = [[0,0,0],
               [0,0,0],
               [0,0,0]]
    for row in range(0,len(m1)):
        for columnnumber in range(0,len(m2[0])):
            column = []
            for row2 in range(0,len(m2)):
                column.append(m2[row2][columnnumber])
            element = dot(m1[row],column)
            matprod[row][columnnumber] = element
    return matprod

#Adds the components of two 3-dimensional vectors
def add(m1, m2):
    matsum = [[m1[0][0]+m2[0][0]],[m1[1][0]+m2[1][0]],[m1[2][0]+m2[2][0]]]
    return matsum

"""--------------------------------------------End of matrix operations-----------------------------------------------------------------"""

# This class is used to represents individual lines created by the user
class Line:
    def __init__(self, point1, point2, parentWindow):
        self.point1 = point1 # Point object 
        self.point2 = point2 # Point object 
        self.parentWindow = parentWindow
        self.colour = (0,0,0) # The colour of the line
        self.screen = self.parentWindow.screen

    # Draws the line on-screen by using the coordinates of the points
    def drawLine(self):
        pygame.draw.aaline(self.screen, self.colour, self.point1.newPos,self.point2.newPos,2)
        
"-----------------------------------------------------------------------------------------------------------------------------------------"
# This class is used to represent a graph inputted by the user
class Equation: #Used for plotting graphs 
    def __init__(self, parentWindow, equationType):
        letters = [
           "a","b","c","d","e","f","g","h","i","k",
           "l","m","n","o","p","q","r","s","t","u",
           "v","w","x","y","z"]
        
        self.equationType = equationType # Parametric or Cartesian
        self.parentWindow = parentWindow
        self.windowOpen = True

        #These are local constants which ma be used in the equation and can be controlled using sliders
        self.a = 1
        self.b = 1
        self.c = 1
        self.d = 1
        self.e = 1

        self.sliderWidth = 180

        #These three expressions represent the x,y and z coordinates in terms of a fourth variable 't'
        #These attributes will only be used if the equation is parametric type
        self.xEquation = str()
        self.yEquation = str()
        self.zEquation = str()

        # This attribute is a string which represents the equation using the variables x,y and z (in the given domain)
        self.cartesianEquation = None

        #These start and end values are used for Cartesian equations to reduce the amount of time the program takes to search for all the points. This is useful for spheres for example where the points are only located in the domain -radius <= x,y,z <= radius 
        self.startX = -1
        self.endX = 1
        self.startY = -1
        self.endY = 1
        self.startZ = -1
        self.endZ = 1

        #This is the domain of the parametric variable
        self.startValue = -1
        self.endValue = 1

        # A listof Point objects with cordinates that satisfy the equation
        self.listOfPoints = []

        # A list of Slidre objects that will be displayed and active when the graph of the equation is
        self.listOfSliders = [Slider('a',self.a, 0,  -10, 10, self.parentWindow, self),
                              Slider('b',self.b, 180, -10, 10, self.parentWindow, self),
                              Slider('c',self.c, 360, -10, 10, self.parentWindow, self),
                              Slider('d',self.d, 540, -10, 10, self.parentWindow, self),
                              Slider('e',self.e, 720, -10, 10, self.parentWindow, self)]
        self.parentWindow = parentWindow
        self.showSliders = False
        self.isSelected = True 
        self.colour = (0,100,160) # Colour of the lines used to draw the curve or the points satisfyign the equatoin

        #Tkinter window 
        self.root = None

        # The amount by which the parametric variable or x,y and z will be incremented to calculate or check valid points
        # Lower the increment, greater the detail but longer the time it takes for to calculate the points and vice versa
        self.accuracy = 0.1 

        #Temporary variable to get the general shape of the graph in a short time 
        self.error = 5
        self.listOfSides = []
        
        
    def drawGraph(self):
      # A smooth curve or a line can only be drawn for continuous functions
      #Therefore if the Cartesian equation will by default be represented only as individual points 
        if (self.equationType == 'parametric'):
            i = 1
            add = 1
            # Remember that the newPos of a point is a tuple containig the on-screen coordinates of the point
            while (i < len(self.listOfPoints)-add):
                if (self.listOfPoints[i] != '' and self.listOfPoints[i-add] != ''):
                    self.listOfPoints[i].calculateNewPos()
                    pygame.draw.aaline(self.parentWindow.screen, self.colour, self.listOfPoints[i-add].newPos, self.listOfPoints[i].newPos, 10)
                i = i + add
                

        elif (self.equationType == 'cartesian'):
              for point in self.listOfPoints:
                if (point != ''):
                    point.calculateNewPos()
                    pygame.draw.circle(self.parentWindow.screen, (0,0,200), point.newPos, 2, 0)

    # This is used to check if the user is hovering the mose over any point on the graph of the equation
    def mouseOverCurve(self):
        for point in self.listOfPoints:
            if (point != ''):
                if (point.newPos != None):
                    if (((point.newPos[0]-pygame.mouse.get_pos()[0])**2+(point.newPos[1]-pygame.mouse.get_pos()[1])**2)**0.5 <= 5):
                        return True
        return False
    # These are the windows that will be shown when e
    def window(self):
        self.root = Tk()
        self.root.focus_force()
        self.root.overrideredirect(1)
        self.root.attributes('-topmost', True) #Makes sure that the window opens on top of the Pygame window.
        self.root.geometry('200x200+'+str(pygame.mouse.get_pos()[0])+'+'+str(pygame.mouse.get_pos()[1]))
        
        self.accuracylabel = Label(self.root, text='step=')
        self.accuracylabel.place(relx = 0.1, rely = 0.6) 

        self.accuracyent = Entry(self.root, width =5)
        self.accuracyent.place(relx = 0.3, rely = 0.6)

        
        if (self.equationType == 'parametric'):
            self.xEquationlabel = Label(self.root, text='x=')
            self.xEquationlabel.place(relx = 0.1, rely = 0.1)
            
            self.yEquationlabel = Label(self.root,text='y=')
            self.yEquationlabel.place(relx = 0.1, rely = 0.2)
            
            self.zEquationlabel = Label(self.root,text='z=')
            self.zEquationlabel.place(relx = 0.1, rely = 0.3)
            
            self.xEquationent = Entry(self.root)
            self.xEquationent.place(relx = 0.3, rely = 0.1)
            
            self.yEquationent = Entry(self.root)
            self.yEquationent.place(relx = 0.3, rely = 0.2)
            
            self.zEquationent = Entry(self.root)
            self.zEquationent.place(relx = 0.3, rely = 0.3)
            
            self.apply= Button(self.root, text='Apply', command = lambda: self.setInfoParametric(self.xEquationent.get(),self.yEquationent.get(),self.zEquationent.get(),self.startValueent.get(),self.endValueent.get(),self.accuracyent.get()))
            self.apply.place(relx = 0.8, rely = 0.8)
            
            self.delete = Button(self.root, text='Delete', command = lambda: self.deleteEquation())
            self.delete.place(relx = 0.1, rely = 0.8)
            
      
            self.close = Button(self.root, text='Close', command = lambda: self.closeWindow())
            self.close.place(relx = 0.5, rely = 0.8)
            
            self.startValueent = Entry(self.root, width = 7)
            self.startValueent.place(relx = 0.3, rely = 0.5)
                
            self.endValueent = Entry(self.root, width = 7)
            self.endValueent.place(relx = 0.7, rely = 0.5)

            self.trangelabel = Label(self.root, text='≤ t ≤')
            self.trangelabel.place(relx = 0.5, rely = 0.5)
            
            if (self.xEquation != None):
                self.xEquationent.insert(0,self.xEquation)
                self.yEquationent.insert(0,self.yEquation)
                self.zEquationent.insert(0,self.zEquation)
            self.startValueent.insert(0,self.startValue)
            self.endValueent.insert(0,self.endValue)
            self.accuracyent.insert(0,self.accuracy)
                
            self.root.mainloop()
            
        elif (self.equationType == 'cartesian'):
            self.cartesianEquationlabel = Label(self.root, text='Equation:')
            self.cartesianEquationlabel.place(relx = 0.1, rely = 0.0)
            
            self.cartesianEquationent = Entry(self.root)
            self.cartesianEquationent.place(relx = 0.1, rely = 0.1)

            self.startXent = Entry(self.root, width = 7)
            self.startXent.place(relx = 0.2, rely = 0.2)
            
            self.xrangelabel = Label(self.root, text='≤ x ≤')
            self.xrangelabel.place(relx = 0.4, rely = 0.2)
            
            self.endXent = Entry(self.root, width = 7)
            self.endXent.place(relx = 0.6, rely = 0.2)

            self.startYent = Entry(self.root, width = 7)
            self.startYent.place(relx = 0.2, rely = 0.3)
            
            self.yrangelabel = Label(self.root, text='≤ y ≤')
            self.yrangelabel.place(relx = 0.4, rely = 0.3)
            
            self.endYent = Entry(self.root, width = 7)
            self.endYent.place(relx = 0.6, rely = 0.3)

            self.startZent = Entry(self.root, width = 7)
            self.startZent.place(relx = 0.2, rely = 0.4)
            
            self.zrangelabel = Label(self.root, text='≤ z ≤')
            self.zrangelabel.place(relx = 0.4, rely = 0.4)
            
            self.endZent = Entry(self.root, width = 7)
            self.endZent.place(relx = 0.6, rely = 0.4)
            
            self.apply= Button(self.root, text='Apply', command = lambda: self.setInfoCartesian(self.cartesianEquationent.get(),self.startXent.get(),self.endXent.get(),self.startYent.get(),self.endYent.get(),self.startZent.get(),self.endZent.get(),self.accuracyent.get(), self.errorent.get()))
            self.apply.place(relx = 0.8, rely = 0.8)
            
            self.delete = Button(self.root, text='Delete', command = lambda: self.deleteEquation())
            self.delete.place(relx = 0.1, rely = 0.8)
            
      
            self.close = Button(self.root, text='Close', command = lambda: self.closeWindow())
            self.close.place(relx = 0.5, rely = 0.8) 
            
            self.errorlabel = Label(self.root, text='error=')
            self.errorlabel.place(relx = 0.1, rely = 0.5) 
    
            self.errorent = Entry(self.root, width =5)
            self.errorent.place(relx = 0.3, rely = 0.5)   
            
            if (self.cartesianEquation != None):
                self.cartesianEquationent.insert(0,self.cartesianEquation)
            self.startXent.insert(0,self.startX)
            self.endXent.insert(0,self.endX)
            self.startYent.insert(0,self.startY)
            self.endYent.insert(0,self.endY)
            self.startZent.insert(0,self.startZ)
            self.endZent.insert(0,self.endZ)
            self.accuracyent.insert(0,self.accuracy)
            self.errorent.insert(0,self.error)

            self.root.mainloop()        
            
    def closeWindow(self):
        self.root.destroy()
        self.windowOpen = False
        
        
    def sliderSettings(self):
        if (self.showSliders == False):
            for equation in self.parentWindow.listOfEquations:
                equation.showSliders = False
            self.showSliders = True
                    
    def deleteEquation(self):
        if (self in self.parentWindow.listOfEquations):
            self.parentWindow.listOfEquations.remove(self)
            for point in self.parentWindow.listOfPoints:
                if (point in self.listOfPoints):
                    self.parentWindow.listOfPoints.remove(point)
        self.root.destroy()
        
        
    def calculatePoints(self):
        a = self.a
        b = self.b
        c = self.c
        d = self.d
        e = self.e
        startValue = eval(self.startValue)
        endValue = eval(self.endValue)
        for point in self.listOfPoints:
            if (point in self.parentWindow.listOfPoints):
                self.parentWindow.listOfPoints.remove(point)
        self.listOfPoints = []
        if (self.equationType == 'parametric'):
            t = startValue
            while (t <= endValue):
                try:
                    x = eval(self.xEquation)
                    y = eval(self.yEquation)
                    z = eval(self.zEquation)
                    if (type(y) != complex and type(z) != complex):
                        p = Point(self.parentWindow)
                        p.equation = self
                        p.setCor(x, y, z)
                        self.listOfPoints.append(p)
                        self.parentWindow.listOfPoints.append(p)
                    else:
                      if (self.listOfPoints[len(self.listOfPoints)-1] != ''):
                        self.listOfPoints.append('')
                except:
                    self.listOfPoints.append('')
                t = round(t + self.accuracy,2)
                
        elif (self.equationType == 'cartesian'):
            if (1==1):
                startX = eval(self.startX)
                endX = eval(self.endX)
                startY = eval(self.endY)
                endY = eval(self.endY)
                startZ = eval(self.startZ)
                endZ = eval(self.endZ)
                x = startX
                while (x <= endX):
                    y = self.startY
                    while (y <= endY):
                        z = startZ
                        while (z <= self.endZ):
                            try:
                                lhs = eval(self.listOfSides[0])
                                i = 1
                                while (i < len(self.listOfSides)):       
                                    rhs = eval(self.listOfSides[i])
                                    if (round(lhs,3) == round(rhs,3)):
                                        if (i == len(self.listOfSides)-1):
                                            p = Point(self.parentWindow)
                                            p.equation = self
                                            p.setCor(x, y, z)
                                            self.listOfPoints.append(p)
                                            self.parentWindow.listOfPoints.append(p)
                                    elif (lhs*rhs >= 0 and  1-(self.error/100) <= abs(lhs/rhs) <= 1+(self.error/100)):
                                        if (i == len(self.listOfSides)-1):
                                            p = Point(self.parentWindow)
                                            p.equation = self
                                            p.cor = (round(x,3),round(y,3),round(z,3))
                                            p.setCor(x, y, z)
                                            self.listOfPoints.append(p)
                                            self.parentWindow.listOfPoints.append(p)
                                    else:
                                        break
                                    i = i + 1
                            except:
                                pass
                            
                            z = z + self.accuracy
                        y = y + self.accuracy
                    x = x + self.accuracy

    #(x**2+y**2-1)**3-(x**2)*(y**3)=0
    # ZeroDivisionError or TypeError or NameError
    def setInfoParametric(self, xEquation, yEquation, zEquation, startValue, endValue, accuracy):
        self.xEquation = xEquation
        self.yEquation = yEquation
        self.zEquation = zEquation
        self.startValue = eval(startValue)
        self.endValue = eval(endValue)
        self.accuracy = eval(accuracy)
        self.calculatePoints()
        self.sliderSettings()
        if (self not in self.parentWindow.listOfEquations):
            self.parentWindow.listOfEquations.append(self)
        self.root.destroy()
        self.windowOpen = False
        

    def setInfoCartesian(self, cartesianEquation, startX, endX, startY, endY, startZ, endZ, accuracy, error):
        a = self.a
        b = self.b
        c = self.c
        d = self.d
        e = self.e
        cartesinaEquation = list(cartesianEquation)
        for i in range(0,len(cartesinaEquation)):
            char = cartesinaEquation[i]
            if (char == '^'):
                cartesinaEquation[i] = '**'
        self.cartesianEquation = cartesianEquation
        self.startX = startX
        self.endX = endX
        self.startY = startY
        self.endY = endY
        self.startZ = startZ
        self.endZ = endZ
        self.accuracy = eval(accuracy)
        self.error = eval(error)
        self.listOfSides = self.cartesianEquation.split("=")
        self.calculatePoints()
        self.sliderSettings()
        
        if (self not in self.parentWindow.listOfEquations):
            self.parentWindow.listOfEquations.append(self)
        self.root.destroy()
        self.windowOpen = False
        
            
"""----------------------------------------------------------------------------------------------------------------------------------"""
class Slider: # Used for controlling variables as required by the user
    def __init__(self, text, variable, x, startValue, endValue, parentWindow, equation):
        self.equation = equation
        self.width = 180
        self.height = 60
        self.text = text
        self.parentWindow = parentWindow
        self.variable = variable
        self.x = x
        self.y = self.parentWindow.height-self.height
        self.startValue = startValue
        self.endValue = endValue
        self.pointer = Point(parentWindow)
        self.pointer.setCor(self.x+(11/20)*self.width, self.y+self.height*0.75,0)
        self.pointer.newPos = (self.pointer.x, self.pointer.y)
        self.pointer.radius = 10
        self.movePointer = False
    
    def setVariable(self):
        self.variable = self.startValue + abs((self.endValue-self.startValue))*((self.pointer.x-self.x)/self.width)

        if (self.text == 'a'):
            self.equation.a = self.variable
        elif (self.text == 'b'):
            self.equation.b  = self.variable
        elif (self.text == 'c'):
            self.equation.c = self.variable
        elif (self.text == 'd'):
            self.equation.d  = self.variable
        elif (self.text == 'd'):
            self.equation.d  = self.variable
        
    def drawSlider(self):
        if (self.equation.showSliders == True):
            self.parentWindow.showText(self.text+' = '+str(round(self.variable,2)), int(self.x+self.width/2), self.y+10, (255, 0, 0), (255, 255, 255), 20)
            pygame.draw.line(self.parentWindow.screen, (0,0,0), (int(self.x), int(self.y+self.height*0.75)), (int(self.x)+self.width, int(self.y+self.height*0.75)), 1)
            pygame.draw.rect(self.parentWindow.screen, (0,0,0), (self.x, self.y, self.width, self.height), 1)
            pygame.draw.circle(self.parentWindow.screen, (0,0,200), (int(self.pointer.x), int(self.y+self.height*0.75)), 10, 0)
"""----------------------------------------------------------------------------------------------------------------------------------"""

class Point: # Used to display individual points on the screen
    def __init__(self, parentWindow):
        self.parentWindow = parentWindow
        self.cor = ()
        self.screen = self.parentWindow.screen
        self.colour = (0,0,255)
        self.posvec = None
        self.radius = None
        self.x = None
        self.y = None
        self.z = None
        self.transformationlist = []
        self.windowOpen = False
        self.radius = 5
        self.axesTransformation = parentWindow.axesTransformation
        self.width = parentWindow.width
        self.height = parentWindow.height
        self.newPos = None
        self.colour = (0,0,255)
        self.equation = None
        
    def screenCor(self,x,y):
        x = x + self.width/2
        y = self.height/2 - y
        return (int(x),int(y))
    
    def showText(self,text, centreX, centreY, fontColour, fontBg, fontSize):
        basicfont = pygame.font.SysFont('unifont.ttf', fontSize) # initialises font for displaying text
        text = basicfont.render(text, True, fontColour, fontBg) # Text for pause
        textrect = text.get_rect()
        textrect.center = (centreX,centreY) # 
        self.screen.blit(text, textrect) # Shows text on self.screen   
    def calculateNewPos(self):
        self.axesTransformation = self.parentWindow.axesTransformation
        newPos = transform([self.posvec[0][0],self.posvec[1][0],self.posvec[2][0]],self.axesTransformation)
        newPos = self.parentWindow.screenCor(newPos)
        self.newPos = (newPos[0]+self.parentWindow.xTranslation, newPos[1]+self.parentWindow.yTranslation) 
            
    def show(self):
        self.calculateNewPos()
        
        text = '('+str(self.x)+', '+str(self.y)+', '+str(self.z)+')'
        if (self.parentWindow.showCoordinates == True and self.equation == None):
            pygame.draw.circle(self.screen, self.colour,self.newPos,self.radius,0)
            self.showText(text, self.newPos[0] + self.radius +20, self.newPos[1]+self.radius+20, (255, 0, 0), (255, 255, 255), 20)
        elif (self.equation != None and self.mouseOverPoint() == True):
            self.showText(str(self.cor), self.newPos[0] + self.radius +20, self.newPos[1]+self.radius+20, (255, 0, 0), (255, 255, 255), 20)


    def mouseOverPoint(self):
        if self.newPos != None:
            if (((self.newPos[0]-pygame.mouse.get_pos()[0])**2+(self.newPos[1]-pygame.mouse.get_pos()[1])**2)**0.5 <= self.radius):
                return True
            else:
                return False

    def closeWindow(self):
        self.root.destroy()
        self.windowOpen = False
        
        
    def window(self):  # Window for Point settings
        self.root = Tk()
        self.root.focus_force()
        self.windowOpen = True
        self.root.overrideredirect(1)
        self.root.attributes('-topmost', True) #Makes sure that the window opens on top of the Pygame window.
        self.root.title('Point Properties')
        if (self.posvec == None):
            self.root.geometry('250x60+0+'+str(pygame.mouse.get_pos()[1]+25)) # 'width x height + xcor + ycor'
        else:
            self.root.geometry('250x60+'+str(pygame.mouse.get_pos()[0]+10)+'+'+str(pygame.mouse.get_pos()[1]+10)) # 'width x height + xcor + ycor'
        #+str(pygame.mouse.get_pos()[0]+70)+'+'+str(pygame.mouse.get_pos()[1]+50)
        self.xlabel = Label(self.root, text='X=') # User input for the x coordinate of the point
        self.xlabel.place(relx=0.05,rely=0.1)
        
        self.ylabel = Label(self.root, text='Y=') # User input for the x coordinate of the point
        self.ylabel.place(relx=0.25,rely=0.1)

        self.zlabel = Label(self.root, text='Z=') # User input for the x coordinate of the point
        self.zlabel.place(relx=0.45,rely=0.1)
        
        self.xent = Entry(self.root, width = 5) # User input for the x coordinate of the point
        self.xent.place(relx=0.05,rely=0.4)
         
        self.yent = Entry(self.root, width = 5) # User input for the y coordinate of the point
        self.yent.place(relx=0.25,rely=0.4)
        
        self.zent = Entry(self.root, width = 5) # User input for the z coordinate of the point
        self.zent.place(relx=0.45,rely=0.4)
        
        if (self.posvec != None):
            self.xent.insert(0, str(self.posvec[0][0]))
            self.yent.insert(0, str(self.posvec[1][0]))
            self.zent.insert(0, str(self.posvec[2][0]))
            self.close = Button(self.root,text='Close',command=lambda: self.closeWindow())
            self.close.place(relx=0.8,rely=0.5)
            
        if (self.xent.get()!=self.x or self.yent.get()!=self.y or self.zent.get()!=self.z):
            self.apply = Button(self.root,text='Apply',command=lambda: self.corValidation())
            self.apply.place(relx=0.6,rely=0.1) # This button will effectively create the point (if the user inputs are valid)
        
        self.delete = Button(self.root,text='Delete',command=lambda: self.deletePoint())
        self.delete.place(relx=0.8,rely=0.1)



        self.root.mainloop()

        
    def deletePoint(self):
        if (self in self.parentWindow.listOfPoints):
            self.parentWindow.listOfPoints.remove(self)
        for line in self.parentWindow.listOfLines:
            if (self == line.point1 or self == line.point2):
                self.parentWindow.listOfLines.remove(line)
        self.root.destroy()
        
                
        
    def corValidation(self):
        validCor = True
        try:
            x = round(float(self.xent.get()),2) # The coordinates need to be integers because the pixels cannot be decimals
            y = round(float(self.yent.get()),2)
            z = round(float(self.zent.get()),2)
        except ValueError or TypeError:
            validCor=False
        if (validCor == True):
            self.setCor(x,y,z)
            self.parentWindow.listOfPoints.append(self)
            
        if (self.windowOpen == True):
            self.root.destroy()
            self.windowOpen = False
            
                
    def setCor(self,x,y,z):
        self.x = round(x,2)
        self.y = round(y,2)
        self.z = round(z,2)
        self.posvec = [[x],[y],[z]]
        self.cor = (round(x,3),round(y,3),round(z,3))

        
        
    def transformPoint(self,transformation,axisplane,angle,scalefactor):
        if (transformation == 'Rotation'):
            matrix = rotation(angle,axisplane) 
        elif (transformation == 'Reflection'):
            matrix = reflection(axisplane)
        elif (transformation == 'Scale'):
            matrix = scale(scalefactor)

        posvec = matrixMultiply(matrix,self.posvec)
        self.setCor(posvec[0][0],posvec[1][0],posvec[2][0])
    
"""----------------------------------------------------------------------------------------------------------------------------------"""
        
class Buttons:
    def __init__(self,title, text, x, y, width, height, radius, shape, fontSize, fontColour, borderColour, bgColour, parentWindow):
        self.parentWindow = parentWindow
        self.leftClick = False
        self.rightClick = False
        self.leftHold = False
        self.hover = False
        
        self.x = x
        self.y = y
        self.title = title
        self.text = text
        self.active = False
        self.width = width
        self.height = height
        self.shape = shape
        self.radius = radius
        self.fontColour = fontColour
        self.screen = self.parentWindow.screen 
        self.borderColour = borderColour
        self.bgColour = bgColour
        self.fontBg = self.bgColour
        self.fontSize = fontSize

    def showText(self,text, centreX, centreY, fontColour, fontBg, fontSize):
        basicfont = pygame.font.SysFont('times.ttf', fontSize) # initialises font for displaying text
        text = basicfont.render(text, True, fontColour, fontBg)
        textrect = text.get_rect()
        textrect.center = (centreX,centreY) # 
        self.screen.blit(text, textrect) # Shows text on self.screen
        
    def mouseOverButton(self):
        if (self.shape == 'circle'):
            if (((self.x - pygame.mouse.get_pos()[0])**2+(self.y - pygame.mouse.get_pos()[1])**2)**0.5 <= self.radius+5 ):
                return True
            return False
        elif (self.shape == 'rectangle'):
            if (self.x < pygame.mouse.get_pos()[0] < self.x + self.width and self.y < pygame.mouse.get_pos()[1] < self.y + self.height):
                return True
            return False
        
    def hoverCommand(self):
        pass
    
    def leftClickCommand(self):
        if (self.title == 'Add Point'):
            point = Point(self.parentWindow)
            point.window()
            
        if (self.title in self.parentWindow.listOfTransformationTypes):
            if (self.active == False):
                for transformationButtons in self.parentWindow.listOfButtons:
                    if (transformationButtons.title in self.parentWindow.listOfTransformationTypes):
                        transformationButtons.active = False
                self.active = True
            elif (self.active == True):
                self.active = False

        if (self.title == 'Coordinates'):
            if (self.parentWindow.showCoordinates == True):
                self.parentWindow.showCoordinates = False
                self.text = 'Show Coordinates'
            else:
                self.parentWindow.showCoordinates = True
                self.text = 'Hide Coordinates'

        
        if (self.title == 'PositiveXTranslation'):
            for point in self.parentWindow.listOfPoints:
                if (point in self.parentWindow.listOfSelectedPoints or self.parentWindow.listOfSelectedPoints == []):
                    point.setCor(point.x+self.parentWindow.translationAmount, point.y, point.z)
        
        if (self.title == 'NegativeXTranslation'):
            for point in self.parentWindow.listOfPoints:
                if (point in self.parentWindow.listOfSelectedPoints or self.parentWindow.listOfSelectedPoints == []):
                    point.setCor(point.x-self.parentWindow.translationAmount, point.y, point.z)
        
        if (self.title == 'PositiveYTranslation'):
            for point in self.parentWindow.listOfPoints:
                if (point in self.parentWindow.listOfSelectedPoints or self.parentWindow.listOfSelectedPoints == []):
                    point.setCor(point.x, point.y+self.parentWindow.translationAmount, point.z)
        
        if (self.title == 'NegativeYTranslation'):
            for point in self.parentWindow.listOfPoints:
                if (point in self.parentWindow.listOfSelectedPoints or self.parentWindow.listOfSelectedPoints == []):
                    point.setCor(point.x, point.y-self.parentWindow.translationAmount, point.z)

        if (self.title == 'PositiveZTranslation'):
            for point in self.parentWindow.listOfPoints:
                if (point in self.parentWindow.listOfSelectedPoints or self.parentWindow.listOfSelectedPoints == []):
                    point.setCor(point.x, point.y, point.z+self.parentWindow.translationAmount)
        
        if (self.title == 'NegativeZTranslation'):
            for point in self.parentWindow.listOfPoints:
                if (point in self.parentWindow.listOfSelectedPoints or self.parentWindow.listOfSelectedPoints == []):
                    point.setCor(point.x, point.y, point.z-self.parentWindow.translationAmount)
                
        if (self.title == 'Reset View'):
            self.parentWindow.axesSf = 40.0
            self.parentWindow.xRotation = 0.0
            self.parentWindow.yRotation = 0.0
            self.parentWindow.prevXRotation = 0.0
            self.parentWindow.prevYRotation = 0.0
            self.parentWindow.xTranslation = 0
            self.parentWindow.yTranslation = 0
            self.parentWindow.twoDMode = True
            
        if (self.title == 'Parametric Equation'):
            e = Equation(self.parentWindow, 'parametric')
            e.window()

        if (self.title == 'Cartesian Equation'):
            e = Equation(self.parentWindow, 'cartesian')
            e.window()
        
        if (self.title == 'Axes Display'):
            if (self.parentWindow.showAxes == True):
                self.parentWindow.showAxes = False
                self.text = 'Show Axes'
            else:
                self.parentWindow.showAxes = True
                self.text = 'Hide Axes'
                
        if (self.title == 'Add Line'):
            if (len(self.parentWindow.listOfSelectedPoints) == 2):
                self.parentWindow.listOfSelectedPoints[0].colour = (0,0,255)
                self.parentWindow.listOfSelectedPoints[1].colour = (0,0,255)
                l = Line(self.parentWindow.listOfSelectedPoints[0],self.parentWindow.listOfSelectedPoints[1],self.parentWindow) # Creates a new line object for the two points selected by the user
                self.parentWindow.listOfLines.append(l)
                self.parentWindow.listOfSelectedPoints = [] # Resets the lits for a new line to be created
    
            
        if (self.title == 'Close'):
            pygame.quit()
            sys.exit()
                
            
                
    def showButton(self):
        if (self.shape == 'rectangle'):
            pygame.draw.rect(self.screen, self.bgColour, (self.x, self.y, self.width,self.height), 0)
            pygame.draw.rect(self.screen, self.borderColour, (self.x,self.y, self.width,self.height), 1)
            self.showText(self.text, int(self.x+self.width/2), int(self.y+self.height/2), self.fontColour, self.bgColour, self.fontSize)
            
        elif (self.shape == 'circle'):
            pygame.draw.circle(self.screen, self.bgColour, (self.x, self.y), self.radius, 0)
            pygame.draw.circle(self.screen, self.borderColour, (self.x, self.y), self.radius, 1)
            self.showText(self.text, self.x, self.y, self.fontColour, self.bgColour, self.fontSize)

"""----------------------------------------------------------------------------------------------------------------------------------"""

def rotation(angle,axis):
    angle = radians(angle)
    if (axis == 'x'):
        matrix = [[1,         0,          0],
                  [0,cos(angle),-sin(angle)],
                  [0,sin(angle),cos(angle)]]
        
    elif (axis == 'y'):
        matrix = [[cos(angle), 0,sin(angle)],
                  [0,         1,          0],
                  [-sin(angle),0,cos(angle)]]
    elif (axis == 'z'):
        matrix = [[cos(angle),-sin(angle),0],
                  [sin(angle), cos(angle),0],
                  [0,        0,          1]]
    return matrix

def reflection(plane):
    if (plane=='x'):
        matrix = [[-1,0,0],
                  [0,1,0],
                  [0,0,1]]
    if (plane == 'y'):
        matrix = [[1,0,0],
                  [0,-1,0],
                  [0,0,1]]
    if (plane=='z'):
        matrix = [[1,0,0],
                  [0,1,0],
                  [0,0,-1]]
    return matrix

def scale(scalefactor):
    matrix = [[scalefactor,0,0],
              [0,scalefactor,0],
              [0,0,scalefactor]]
    return matrix
    
    
def cartesian(x,y):
    x = x - self.width/2
    y = y - self.height/2
    return (int(x),int(y))


def createpoint(x,y,z):
    point = Point(x,y,z)
    self.listOfPoints.append(point)
    
basicfont = pygame.font.SysFont('unifont.ttf', 40) # initialises font for displaying text

"""----------------------------------------------------------------------------------------------------------------------------------"""

class Graph:
    def __init__(self, width, height, screen, parentApp):
        self.parentApp = parentApp

        self.width = width
        self.height = height
        self.bgColour = (150,150,150)
        
        self.screen = screen
        #a = pygame.image.load('Graph 3-D icon.jpg')
        #pygame.display.set_icon(a)
        pygame.display.set_caption('Graphulator')
        
        self.listOfPoints = []
        self.listOfButtons = []
        self.listOfTransformationTypes = ['Rotation','Reflection','Scale']
        self.listOfLines = []
        self.listOfSelectedPoints = []
        self.listOfSelectedEquations = []
        
        self.axesSf = 40
        self.transformationParameters = None
        
        self.buttonsCreated = False
        self.rotationAngle = 10
        self.radius = 10
        
        self.axesTransformation = [[1,0,0],[0,1,0],[0,0,1]]
        self.rotateAxes = False
        self.axesRotationMousePos = None
        self.xRotation = 0.0
        self.yRotation = 0.0
        self.prevXRotation = 0.0
        self.prevYRotation = 0.0
        
        self.translateAxes = False
        self.translateAxesMousePos = None
        self.xTranslation = 0
        self.yTranslation = 0
        self.prevXTranslation = 0
        self.prevYTranslation = 0
        self.translationAmount = 1
        
        self.listOfAxisPoints = []
        self.x1 = Point(self)
        self.x1.setCor(-self.width,0,0)
        self.x2 = Point(self)
        self.x2.setCor(self.width,0,0)
        
        self.y1 = Point(self)
        self.y1.setCor(0,-self.width,0)
        self.y2 = Point(self)
        self.y2.setCor(0,self.width,0)
        
        self.z1 = Point(self)
        self.z1.setCor(0,0,self.width)
        self.z2 = Point(self)
        self.z2.setCor(0,0,-self.width)
        
        self.listOfAxisPoints.append(self.x1)
        self.listOfAxisPoints.append(self.x2)
        self.listOfAxisPoints.append(self.y1)
        self.listOfAxisPoints.append(self.y2)
        self.listOfAxisPoints.append(self.z1)
        self.listOfAxisPoints.append(self.z2)
        
        self.showCoordinates = True
        self.twoDMode = True
        self.listOfEquations = []
        self.showAxes = True
        
        self.showTab = False
        
    def setCor(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.posvec = [[x],[y],[z]]
        self.cor = [x,y,z]
        if (self.windowOpen == True):
            self.root.destroy()
            self.windowOpen = False
            
    def createButtons(self):
        colours = {'white':(255,255,255), 'black':(0,0,0), 'red':(255,0,0), 'blue':(0,0,255), 'green':(0,255,0)}
        '-----------------------------------------------------------------------------------------'
        '|Add Point   |Rotation|Reflection|Scale|'
        '|Add Equation|'
        #                 [title       ,text              ,x   ,y   ,width ,height ,radius ,shape,     fontSize, fontColour      ,borderColour,    bgColour,       parentWindow]
        listOfButtons = [['Close'      ,'X'     ,self.width-20 ,1   ,20    ,20     ,None,  'rectangle', 20,      colours['black'],colours['black'],colours['white'], self],
                         ['Add Point'  ,'Add Point'       ,0   ,40  ,100    ,20     ,None,  'rectangle', 20,      colours['black'],colours['black'],colours['white'], self], 
                         ['Parametric Equation','Parametric Equation',0   ,80  ,200    ,20     ,None,  'rectangle', 20,      colours['black'],colours['black'],colours['white'], self],  
                         ['Cartesian Equation','Cartesian Equation',200  ,80  ,200    ,20     ,None,  'rectangle', 20,      colours['black'],colours['black'],colours['white'], self],  
                         ['Add Line'  ,'Add Line'        ,400 ,80  ,100    ,20     ,None,  'rectangle', 20,      colours['black'],colours['black'],colours['white'], self],  
                         ['Rotation'   ,'Rotation'        ,100 ,40  ,100    ,20     ,None,  'rectangle', 20,      colours['black'],colours['black'],colours['white'], self], 
                         ['Reflection' ,'Reflection'      ,200 ,40  ,100    ,20     ,None,  'rectangle', 20,      colours['black'],colours['black'],colours['white'], self],
                         ['Scale'      ,'Scale'           ,300 ,40  ,100    ,20     ,None,  'rectangle', 20,      colours['black'],colours['black'],colours['white'], self],
                         ['Coordinates','Hide Coordinates',400 ,40  ,120    ,20     ,None,  'rectangle', 20,      colours['black'],colours['black'],colours['white'], self],
                         ['Axes Display','Hide Axes'      ,400 ,60  ,100    ,20     ,None,  'rectangle', 20,      colours['black'],colours['black'],colours['white'], self],
                         ['Reset View','Reset View'       ,100 ,60  ,100    ,20     ,None,  'rectangle', 20,      colours['black'],colours['black'],colours['white'], self],
                         ['NegativeXTranslation'  ,'-X'   ,600 ,70  ,120    ,30     ,30,     'circle',   20,      colours['black'],colours['red'], colours['white'], self],
                         ['PositiveXTranslation'  ,'+X'   ,660 ,70  ,120    ,30     ,30,     'circle',   20,      colours['black'],colours['red'], colours['white'], self],
                         ['NegativeYTranslation'  ,'-Y'   ,720 ,70  ,120    ,30     ,30,     'circle',   20,      colours['black'],colours['green'], colours['white'], self],
                         ['PositiveYTranslation'  ,'+Y'   ,780 ,70  ,120    ,30     ,30,     'circle',   20,      colours['black'],colours['green'], colours['white'], self],
                         ['NegativeZTranslation'  ,'-Z'   ,840 ,70  ,120    ,30     ,30,     'circle',   20,      colours['black'],colours['blue'], colours['white'], self],
                         ['PositiveZTranslation'  ,'+Z'   ,900 ,70  ,120    ,30     ,30,     'circle',   20,      colours['black'],colours['blue'], colours['white'], self],
                         ['Select Points'      ,'Select'  ,0   ,60  ,100    ,20     ,None,  'rectangle', 20,      colours['black'],colours['black'],colours['white'], self]]

        for button in listOfButtons: 
            buttonObject = Buttons(button[0],button[1],button[2],button[3],button[4],button[5],button[6],button[7],button[8],button[9],button[10],button[11],self)
            self.listOfButtons.append(buttonObject)

    def checkEvents(self):
        buttonselected = False
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()

            # If the user starts any mouse activity
            if (event.type == pygame.MOUSEBUTTONDOWN):
                
                if (event.button == 1): # If user left clicks                        
                    for point in self.listOfPoints:
                        if (point.mouseOverPoint() == True):
                            if (point in self.listOfSelectedPoints):
                                self.listOfSelectedPoints.remove(point)
                                point.colour = (0,0,255)
                            elif (point.equation == None):
                                self.listOfSelectedPoints.append(point)
                                point.colour = (255,0,0)
                                
                    for tab in self.parentApp.listOfTabs:
                        if (tab.mouseOverButton() == True and int(tab.title[1]) <= self.parentApp.numberOfTabs):
                            buttonselected = True
                            self.parentApp.currentTab = tab.title 
                            
                    if (self.parentApp.newTabButton.mouseOverButton() == True and self.parentApp.numberOfTabs < self.parentApp.maxTabs):
                        buttonselected = True
                        self.parentApp.numberOfTabs += 1
                        self.parentApp.newTabButton.x += 100
                        
                    for equation in self.listOfEquations:
                        if (equation.mouseOverCurve() == True):
                            equation.sliderSettings()
                            self.listOfSelectedEquations.append(equation)
                            
                    for equation in self.listOfEquations:
                        if (equation.showSliders == True):
                            for slider in equation.listOfSliders:
                                if (slider.pointer.mouseOverPoint() == True):
                                    slider.movePointer = True
                                    buttonselected = True
                        
                    # If the user clicks on a button it's command is initated
                    for button in self.listOfButtons:
                        if (button.mouseOverButton() == True):
                            button.leftHold = True
                            button.leftClick = True
                            buttonselected = True
                            
                    if (buttonselected == False):
                        self.axesTranslationMousePos = pygame.mouse.get_pos()
                        self.translateAxes = True
                        
                # If the user presser the middle button i.e. the scroll bar buttton
                if (event.button == 2):
                    self.rotateAxes = True
                    self.axesRotationMousePos = pygame.mouse.get_pos() # Records the position of the mouse when the user presses the middle button to calculate the angle by which the axes need to be rotated

                # If the user right clicks
                if (event.button == 3):
                    for point in self.listOfPoints:
                        if (point.mouseOverPoint() == True and point.equation == None):
                            point.window()
                            
                    for equation in self.listOfEquations:
                        if (equation.mouseOverCurve() == True and equation.windowOpen == False):
                            equation.windowOpen = True
                            equation.window()
                            
                #If the user scrolls up 
                if (event.button == 4):
                    self.axesSf = self.axesSf * 1.1
                    
                #If the user scrolls down
                if (event.button == 5):
                    self.axesSf = self.axesSf * 0.9
                    
            #If the user ends any mouse activity  
            if (event.type == pygame.MOUSEBUTTONUP):
                if (event.button == 1):
                    for button in self.listOfButtons:
                        if (button.leftClick == True and button.mouseOverButton() == True):
                            button.leftClickCommand()
                            button.leftClick = False
                        button.leftHold = False
                    self.translateAxes = False
                    self.prevXTranslation = self.xTranslation
                    self.prevYTranslation = self.yTranslation
                    
                    for equation in self.listOfEquations:
                        if (equation.showSliders == True):
                            for slider in equation.listOfSliders:
                                slider.movePointer = False
                                
                if (event.button == 2):
                    self.rotateAxes = False
                    self.prevXRotation = self.xRotation
                    self.prevYRotation = self.yRotation
            
            
                    
            
    def determineTransformation(self):
        for transformationbuttons in self.listOfButtons:
            if (transformationbuttons.active == True and transformationbuttons.text in self.listOfTransformationTypes):
                if (transformationbuttons.title == 'Rotation'):
                    if (pygame.key.get_pressed()[pygame.K_RIGHT] != 0):
                        self.transformationParameters = ['Rotation','y',self.rotationAngle,None]
                    if (pygame.key.get_pressed()[pygame.K_LEFT] != 0):
                        self.transformationParameters = ['Rotation','y',-self.rotationAngle,None]
                    if (pygame.key.get_pressed()[pygame.K_UP] != 0):
                        self.transformationParameters = ['Rotation','x',self.rotationAngle,None]
                    if (pygame.key.get_pressed()[pygame.K_DOWN] != 0):
                        self.transformationParameters = ['Rotation','x',-self.rotationAngle,None]
                    if (pygame.key.get_pressed()[pygame.K_z] != 0):
                        self.transformationParameters = ['Rotation','z',-self.rotationAngle,None]
                        
                elif (transformationbuttons.title == 'Reflection'):
                    if (pygame.key.get_pressed()[pygame.K_RIGHT]!=0 or pygame.key.get_pressed()[pygame.K_LEFT]!=0):
                        self.transformationParameters = ['Reflection','x',None,None]
                    if (pygame.key.get_pressed()[pygame.K_UP]!=0 or pygame.key.get_pressed()[pygame.K_DOWN]!=0):
                        self.transformationParameters = ['Reflection','y',None,None]
                    if (pygame.key.get_pressed()[pygame.K_z]!=0):
                        self.transformationParameters = ['Reflection','z',None,None]
                        
                elif (transformationbuttons.title == 'Scale'):
                    if (pygame.key.get_pressed()[pygame.K_UP] != 0):
                        self.transformationParameters = ['Scale',None,None,1.05]
                    if (pygame.key.get_pressed()[pygame.K_DOWN] != 0):
                        self.transformationParameters = ['Scale',None,None,0.95]
                    
            

    def updatePoints(self):
        if (self.transformationParameters != None):
            for point in self.listOfPoints:
                if (point in self.listOfSelectedPoints or self.listOfSelectedPoints == []):
                    point.transformPoint(self.transformationParameters[0],self.transformationParameters[1],self.transformationParameters[2],self.transformationParameters[3])
            self.transformationParameters = None
        for point in self.listOfPoints:
            point.show()
            
    def updateLines(self):
        for line in self.listOfLines:
            line.drawLine()

        
    def showText(self,text, centreX, centreY, fontColour, fontBg, fontSize):
        basicfont = pygame.font.SysFont('times.ttf', fontSize) # initialises font for displaying text
        text = basicfont.render(text, True, fontColour, fontBg)
        textrect = text.get_rect()
        textrect.center = (centreX,centreY) # 
        self.screen.blit(text, textrect) # Shows text on self.screen
        
    def screenCor(self,t):
        x = t[0]
        y = t[1]
        x = x + self.width/2
        y = self.height/2 - y
        return (int(x),int(y))
    
    def drawGrandientBackground(self):
        # Draws background
        colour = 0
        rectHeight = 10
        height = self.height - rectHeight
        
        while (height + rectHeight > 0):
            if (colour> 255):
                break
            pygame.draw.rect(self.screen, (colour,colour,colour), (0,height,self.width,rectHeight), 0)
            height -= rectHeight
            colour = 255 - int(255*(height/self.height))
            
    def drawAxes(self):
        for point in self.listOfAxisPoints:
            newPos = transform([point.posvec[0][0],point.posvec[1][0],point.posvec[2][0]],self.axesTransformation)
            newPos = (newPos[0]+self.xTranslation, newPos[1]-self.yTranslation)
            point.newPos = self.screenCor(newPos)
            
        # Draws the lines representing the axes 
        if (self.showAxes == True):
            pygame.draw.aaline(self.screen, (255,0,0), self.x1.newPos,self.x2.newPos,2)
            pygame.draw.aaline(self.screen, (0,255,0), self.y1.newPos,self.y2.newPos,2)
            pygame.draw.aaline(self.screen, (0,0,255), self.z1.newPos,self.z2.newPos,2)
            #Labels each end of the axes with the required letter
            self.showText('-X', self.x1.newPos[0], self.x1.newPos[1], (0,0,0), (200,200,200), 30)
            self.showText('+X', self.x2.newPos[0], self.x2.newPos[1], (0,0,0), (200,200,200), 30)
            
            self.showText('-Y', self.y1.newPos[0], self.y1.newPos[1], (0,0,0), (200,200,200), 30)
            self.showText('+Y', self.y2.newPos[0], self.y2.newPos[1], (0,0,0), (200,200,200), 30)
            
            if (self.twoDMode == False):
                self.showText('+Z', self.z1.newPos[0], self.z1.newPos[1], (0,0,0), (200,200,200), 30)
                self.showText('-Z', self.z2.newPos[0], self.z2.newPos[1], (0,0,0), (200,200,200), 30)
        
    def calculateAxesTransformation(self):
        # Rotates the axis by transforming the axis points by the angle and scale factor required
        if (self.translateAxes == True):
            self.xTranslation = self.prevXTranslation + int(pygame.mouse.get_pos()[0]-self.axesTranslationMousePos[0])
            self.yTranslation = self.prevYTranslation + int(pygame.mouse.get_pos()[1]-self.axesTranslationMousePos[1])
 

        if (self.rotateAxes == True): # Checks if the axes need to be rotated
            self.yRotation = self.prevYRotation + 360*(pygame.mouse.get_pos()[0]-self.axesRotationMousePos[0])/self.width
            # This takes the previous angle by which the axes were rotated and then adds the additional angle which is determined by the percentage of the distance between the point that the user pressed the middle button and the current position of the mouse
            self.xRotation =  self.prevXRotation + 360*(pygame.mouse.get_pos()[1]-self.axesRotationMousePos[1])/self.width
            self.twoDMode = False

        self.axesTransformation =  matrixMultiply(scale(self.axesSf),rotation(self.xRotation,'x'))
        self.axesTransformation =  matrixMultiply(self.axesTransformation,rotation(self.yRotation,'y'))
        
            
    def updateScreen(self):
        basicfont = pygame.font.SysFont('times.ttf', 40) # initialises font for displaying text        

        #self.drawGrandientBackground()
        self.calculateAxesTransformation()
        self.drawAxes()
        self.parentApp.newTabButton.showButton()
        # Changes the colour of the transformation buttons that are pressed

        

    def updateButtons(self):
        for tab in self.parentApp.listOfTabs:
            if (int(tab.title[1:len(tab.title)]) <= self.parentApp.numberOfTabs):
                tab.showButton()
                if (tab.title == self.parentApp.currentTab):
                    tab.fontColour = (200,0,0)
                else:
                    tab.fontColour = (0,0,0)
        for button in self.listOfButtons:
            if (button.active == True):
                #button.fontColour = (255,255,255)
                button.bgColour = (249, 207, 89)
            else:
                button.fontColour = (0,0,0)
                button.bgColour = (255,255,255)
                
            button.showButton()
            
            if (button.mouseOverButton() == True):
                button.hover = True
            else:
                button.hover = False
            if (button.hover == True):
                if (button.shape == 'rectangle'):
                    button.parentWindow.showText(button.text, int(button.x+button.width/2), int(button.y+button.height/2), button.fontColour, button.bgColour, button.fontSize+5)
                elif (button.shape == 'circle'):
                    button.parentWindow.showText(button.text, button.x, button.y, button.fontColour, button.bgColour, button.fontSize+5)
                #mouseImg = pygame.image.load('Mouse hand.png')
                #self.screen.blit(mouseImg, pygame.mouse.get_pos())

            
            
        for button in self.listOfButtons:
            if (button.leftHold == True and button.title in ['PositiveXTranslation','NegativeXTranslation', 'PositiveYTranslation','NegativeYTranslation','PositiveZTranslation','NegativeZTranslation']):
                button.leftClickCommand()
            if (button.mouseOverButton() == True):
                button.bgColour = (200,200,200)
            else:
                button.bgColour = (255,255,255)
                
    def updateEquations(self):
        for equation in self.listOfEquations:
            equation.drawGraph()
            
    def updateSliders(self):                
        for equation in self.listOfEquations:
            if (equation.showSliders == True):
                for slider in equation.listOfSliders:
                    if (equation.equationType == 'parametric'):
                        if (slider.text in equation.xEquation or slider.text in equation.yEquation or slider.text in equation.zEquation):
                            slider.drawSlider()
                    if (equation.equationType == 'cartesian'):
                         if (slider.text in equation.cartesianEquation):
                            slider.drawSlider()
                    if (slider.movePointer == True):
                        if (slider.x < pygame.mouse.get_pos()[0] < slider.x + slider.width):
                            slider.pointer.setCor(pygame.mouse.get_pos()[0], slider.pointer.y, slider.pointer.z)
                            slider.pointer.newPos = (pygame.mouse.get_pos()[0], slider.pointer.y)
                            slider.setVariable()
                            equation.calculatePoints()
                break
            
    def updateWindows(self):
        for point in self.listOfPoints:
            try:
                point.root.attributes('-topmost', True)
                point.root.update_idletasks()
                point.root.update()
            except Tcl_Error:
                #print (point)
                pass
        for equations in self.listOfEquations:
            try:
                equation.root.attributes('-topmost', True)
                equation.root.update_idletasks()
                equation.root.update()
            except Tcl_Error:
                pass

    def main(self): 
        if self.buttonsCreated == False:
            self.createButtons()
            self.buttonsCreated = True
        
        self.updateScreen()
        self.checkEvents()
        self.updateButtons()
        self.determineTransformation()
        self.updatePoints()
        self.updateLines()
        self.updateEquations()
        self.updateSliders()
        #self.updateWindows()
        pygame.display.update()
        screen.fill((255,255,255))

        

"""----------------------------------------------------------------------------------------------------------------------------------"""

class App:
    def __init__(self, screen, width, height):
        colours = {'white':(255,255,255), 'black':(0,0,0), 'red':(255,0,0), 'blue':(0,0,255), 'green':(0,255,0)}
        self.screen = screen
        #print (self.screen.get_size())         
        (width, height) = self.screen.get_size()
        self.tabs = {}
        self.maxTabs = 10
        self.numberOfTabs = 1
        self.listOfTabs = []
        self.t = None
        
        for i in range(1,self.maxTabs+1):
             exec("self.t = Buttons('t'+str(i),'Graph '+ str(i) ,100*(i-1) ,0   ,100    ,30     ,None,  'rectangle', 20,     colours['black'],colours['black'],colours['white'], self)")
             self.listOfTabs.append(self.t)
             exec("self.tabs['t"+str(i)+"'] = Graph(width, height, self.screen, self)")
	    
        self.currentTab = 't1'

        self.newTabButton = Buttons('New Tab' ,'+',120 ,15 ,100 ,30 ,15,'circle',30,colours['black'],colours['black'],colours['white'], self)            
	     
        
    def updateTabs(self):
        while (1):
            self.tabs[self.currentTab].main()
        
'''
root = Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()-75
embed = Frame(root, width = width, height = height) #creates embed frame for pygame window
#embed.grid(columnspan = (600), rowspan = 500) # Adds grid
embed.pack(side = LEFT) #packs window to the left
#buttonwin = Frame(root, width = 75, height = 500)
#buttonwin.pack(side = LEFT)
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
#os.environ['SDL_VIDEODRIVER'] = 'windib'
pygame.display.init()
screen = pygame.display.set_mode((width, height))
pygame.display.update()
'''
root = Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()-75
root.destroy()
screen = pygame.display.set_mode((width, height))
app = App(screen, width, height)
app.updateTabs()
#screen.fill((255,255,255))
'''
while (1):        
    try:
        #root.update_idletasks()
        root.update()
    except TclError:
        pygame.quit()
        sys.exit()
        break
    app.tabs[app.currentTab].main()
'''
