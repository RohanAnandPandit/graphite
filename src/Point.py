from Image import Image
from utils import randomColour, showText, showText2
from maths.Matrices import *
import pygame
from math import sqrt
from tkinter import *
from random import randint
from String_Formatting import syntaxCorrection

class Point: # Used to display individual points on the screen
    def __init__(self, parentWindow, createSlider = True):
        from Buttons import Buttons

        self.parentWindow = parentWindow
        self.cor = ()
        self.screen = self.parentWindow.screen

        self.posvec = None
        self.radius = None

        self.x = None
        self.y = None
        self.z = None

        self.windowOpen = False

        self.radius = 5
        self.screenPos = None

        self.colour = randomColour()
        self.equation = None

        self.line = None

        self.x2 = ''
        self.y2 = ''
        self.z2 = ''

        self.trace = False
        self.listOfTrace = []
        self.t = 0

        if (createSlider):
            from Slider import Slider
            self.slider = Slider('t', 't', 5, 100, -10, 10, self.parentWindow,
                                 self, 100, 50, '', 0)
        try:
            self.axesTransformation = parentWindow.axesTransformation
            self.width = parentWindow.width
            self.height = parentWindow.height
        except:
            pass

        self.prevCor = ''
        self.text = ''

    def visible(self): # Checks if point is visible onscreen
        if (0 <= self.screenPos[0] <= self.parentWindow.width
            and 0 <= self.screenPos[1] <= self.parentWindow.height):
            return True
        else:
            return False

    def drawTrace(self):
        # Iterates through all the previous position points
        for i in range(0,len(self.listOfTrace)):
            p = self.listOfTrace[i]
            ratio = (i+1)/len(self.listOfTrace) # Percentage of index

            if (self.parentWindow.gradientForTrace):
                colourRatio = ratio # Percentage of index
                #colourRatio = 1/(2*(1-e**(-(i+1))))
            else:
                colourRatio = 1

            if (self.parentWindow.trailEffect):
                radiusRatio = ratio / 1.0 # Percentage of index
            else:
                radiusRatio = 1

            p.colour = (int(colourRatio * self.colour[0]),
                        int(colourRatio * self.colour[1]),
                        int(colourRatio * self.colour[2])) # Sets colour
            p.calculateScreenPos()

            if (i != 0):
                # Dars line between adjacent points
                if (self.parentWindow.lineForTrace):
                    pygame.draw.aaline(self.parentWindow.screen, (0,0,0),
                                       self.listOfTrace[i - 1].screenPos,p.screenPos)
                if (p.visible()):
                    p.show(int(self.parentWindow.radius * radiusRatio), False)

    def screenCor(self, x, y):
        x = x + self.width/2
        y = self.height/2 - y
        return (int(x), int(y))

    def calculateScreenPos(self):
        if (self.posvec != None):
            self.axesTransformation = self.parentWindow.axesTransformation
            screenPos = matrixMultiply(self.axesTransformation, self.posvec)
            screenPos = self.parentWindow.screenCor(screenPos)
            self.screenPos = (screenPos[0] + self.parentWindow.xTranslation,
                              screenPos[1] + self.parentWindow.yTranslation)

    def show(self, radius = None, showLabel = True):
        if (radius == None):
            radius = self.parentWindow.radius

        #try:
        if (len(self.parentWindow.listOfSelectedPoints) == 1
            and self in self.parentWindow.listOfSelectedPoints):
            t = self.t
        else:
            t = self.parentWindow.t
        #except:
            #pass

        if (self.parentWindow.brownianMotion
            and self in self.parentWindow.listOfSelectedPoints):
            self.setCor(self.x+randint(-self.parentWindow.randomSpeed, self.parentWindow.randomSpeed),
                        self.y+randint(-self.parentWindow.randomSpeed, self.parentWindow.randomSpeed),
                        self.z+randint(-self.parentWindow.randomSpeed, self.parentWindow.randomSpeed))

        if ('t' in self.x2):
            #try:
            self.setCor(eval(syntaxCorrection(self.x2)),self.y,self.z)
            #except:
                #pass
        if ('t' in self.y2):
            try:
                self.setCor(self.x,eval(syntaxCorrection(self.y2)),self.z)
            except:
                pass
        if ('t' in self.z2):
            try:
                self.setCor(self.x,self.y,eval(syntaxCorrection((self.z2))))
            except:
                pass

        self.calculateScreenPos()

        if (self.equation != None):
            if (self.equation.type == 'cartesian'):
                if (self.equation in self.parentWindow.listOfSelectedEquations):
                    pygame.draw.circle(self.screen, (255,0,0),self.screenPos,radius+1,0)
                pygame.draw.circle(self.screen, self.equation.colour,self.screenPos,radius,0)

            if (self.mouseOverPoint()):
                showText2(self.screen,str(self.cor), self.screenPos[0] + int(self.parentWindow.radius*1.2),
                          self.screenPos[1]+radius+20, (255, 0, 0), (255, 255, 255), 20)
                pygame.draw.circle(self.screen, self.colour,self.screenPos,radius+1,0)

        elif (self.equation == None):
            text = '('+str(self.x)+', '+str(self.y)+', '+str(self.z)+')'
            if (self.parentWindow.showCoordinates):
                showText2(self.screen, text, self.screenPos[0] + radius +20,
                          self.screenPos[1]+radius+20, (255, 0, 0), (255, 255, 255), 20)

            if (self in self.parentWindow.listOfSelectedPoints):
                pygame.draw.circle(self.screen, (255,0,0),self.screenPos,radius+2,0)
            elif (self in self.parentWindow.listOfPoints):
                pygame.draw.circle(self.screen, (0,0,0),self.screenPos,radius+2,0)

            #pygame.draw.circle(self.screen, (255,255,255),self.screenPos,radius+1,0)
            pygame.draw.circle(self.screen, self.colour,self.screenPos,radius,0)
            if (showLabel and self.text != ''):
                showText(self.screen,self.text, self.screenPos[0],
                         self.screenPos[1]-radius-15, (255, 0, 0), (255, 255, 255), 25)

    def mouseOverPoint(self):
        if (self.screenPos != None):
            dx = self.screenPos[0] - pygame.mouse.get_pos()[0]
            dy = self.screenPos[1] - pygame.mouse.get_pos()[1]
            if (sqrt(dx**2 + dy**2) <= self.parentWindow.radius):
                return True
            return False

    def closeWindow(self):
        self.root.destroy()
        self.windowOpen = False

    # Window for Point settings which has Delete, Cancel and Apply buttons
    def window(self, x = None, y = None): # Pointwindow
        self.root = Tk()
        self.setCurrentWindow()
        self.parentWindow.listOfWindowPoints.append(self)
        self.root.bind('<Enter>', lambda event: self.setCurrentWindow())
        #self.root.bind('<Leave>', lambda event: self.resetCurrentWindow())
        self.windowOpen = True
        self.root.attributes('-topmost', True) #Makes sure that the window opens on top of the Pygame window.
        self.root.title('Point Properties')

        if (x == None):
            (x,y) = (pygame.mouse.get_pos()[0]+10,pygame.mouse.get_pos()[1]+10)
            
        #self.root.geometry('260x80+'+str(x)+'+'+str(y)) # 'width x height + xcor + ycor'
        # User input for the x coordinate of the point
        #self.coordinateslabel = Label(self.root, text='coordinates=')
        #self.coordinateslabel.grid(row = 0, column = 0, columnspan = 2)
        # User input for the x coordinate of the point
        self.coordinatesent = Entry(self.root, width = 20, font = 'Calibri 15')
        self.coordinatesent.grid(row = 0, column = 0, columnspan = 5)

        if (self.posvec != None):
            print(self.x2)
            if ('t' in self.x2 or (self.y2 or self.x2 or self.z2)):
                self.coordinatesent.insert(0, self.x2)
            else:
                self.coordinatesent.insert(0, str(self.posvec[0][0]))

            if ('t' in (self.y2 or self.x2 or self.z2)):
                self.coordinatesent.insert(len(self.coordinatesent.get()), '|'+self.y2)
            else:
                self.coordinatesent.insert(len(self.coordinatesent.get()), ','+str(self.posvec[1][0]))

            if ('t' in (self.y2 or self.x2 or self.z2)):
                self.coordinatesent.insert(len(self.coordinatesent.get()), '|'+self.z2)
            else:
                self.coordinatesent.insert(len(self.coordinatesent.get()), ','+str(self.posvec[2][0]))

        self.apply = Button(self.root,text='Apply',command = lambda: self.corValidation())
        # This button will effectively create the point (if the user inputs are valid)
        self.apply.grid(row = 2, column = 2)

        self.applyAndNew = Button(self.root, text = 'Apply and New', command = lambda: self.corValidation(True))
        # This button will effectively create the point (if the user inputs are valid)
        self.applyAndNew.grid(row = 2, column = 3, columnspan = 2)

        self.delete = Button(self.root, text = 'Delete', command = lambda: self.deletePoint())
        self.delete.grid(row = 2, column = 5)

        (Label(self.root, text = 'Label', width = 5)).grid(row = 2, column = 0)

        self.textent = Entry(self.root, width = 5, font = 'Calibri 15')
        self.textent.grid(row = 2, column = 1)
        self.textent.insert(0,self.text)

    def traceSetting(self):
        if (self.trace):
            self.trace = False
            self.traceButton.config(text = 'Show Trace')
        else:
            self.trace = True
            self.traceButton.config(text = 'No Trace')

    def deletePoint(self):
        if (self in self.parentWindow.listOfPoints):
            self.parentWindow.listOfPoints.remove(self)

        if (self in self.parentWindow.listOfSelectedPoints):
            self.parentWindow.listOfSelectedPoints.remove(self)
        #  Deletes all lines which have itself as a point
        for line in self.parentWindow.listOfLines:
            if (self in [line.point1, line.point2]):
                self.parentWindow.listOfLines.remove(line)
                if (line in self.parentWindow.listOfSelectedLines):
                    self.parentWindow.listOfSelectedLines.remove(line)
        try:
            self.root.destroy()
        except:
            pass


    # To check if the coordinates entered by the user are valid
    def corValidation(self, newPoint = False):
        validCor = True
        if (self in self.parentWindow.listOfSelectedPoints
            and len(self.parentWindow.listOfSelectedPoints) == 1):
            t = self.t
        else:
            t = self.parentWindow.t
        if ('t' in self.coordinatesent.get()):
            cor = self.coordinatesent.get().split('|')
        elif ('t' not in self.coordinatesent.get()):
            cor = self.coordinatesent.get().split(',')

        try:
            # The coordinates need to be integers because the pixels cannot
            # be decimals
            x = round(float(eval(syntaxCorrection(cor[0]))), 2)
            y = round(float(eval(syntaxCorrection(cor[1]))), 2)
            z = round(float(eval(syntaxCorrection(cor[2]))), 2)
        except :
            validCor = False
            
        if (validCor):
            #if (self.x2 != self.xent.get() or self.y2 != self.yent.get()
            # or self.z2 != self.zent.get()):
            #print(self.yent.get())

            (self.x2,self.y2,self.z2) = tuple(cor)
            print((self.x2,self.y2,self.z2))
            self.setCor(x,y,z)

            self.listOfTrace = []

            if (self not in self.parentWindow.listOfPoints):
                self.parentWindow.listOfPoints.append(self)

            if (newPoint):
                p = Point(self.parentWindow)
                p.window(self.root.winfo_x(),self.root.winfo_y())

            self.text = self.textent.get()
            self.closeWindow()

    def setCor(self,x,y,z):
        (self.x,self.y,self.z) = (round(x,3),round(y,3),round(z,3))
        self.posvec = [[x],[y],[z],[1]]
        self.cor = (round(x,3),round(y,3),round(z,3))
        #(self.x2,self.y2,self.z2) = (str(x),str(y),str(z))


    # Takes the relevant information, gets the required transformation matrix
    # and transforms the point
    def transformPoint(self):
        matrix = self.parentWindow.pointTransformation
        posvec = matrixMultiply(matrix,self.posvec)
        self.setCor(posvec[0][0],posvec[1][0],posvec[2][0])
    
    def setCurrentWindow(self):
        self.parentWindow.currentWindow = self.root
        
    def resetCurrentWindow(self):
        self.parentWindow.currentWindow = None
