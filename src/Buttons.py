import pygame
from tkinter import *
from utils import showText, invert, showImage, fileLocation
from Equation import Equation
from Line import Line

# The class is called 'Buttons' instead of 'Button' because 'Button' is a tkinter function
class Buttons:
    def __init__(self, title, text, x, y, width, height, radius, shape, fontSize,
                 fontColour, borderColour, bgColour, parentWindow, imageFile):
        from Point import Point
        self.parentWindow = parentWindow
        self.screen = self.parentWindow.screen
        self.leftClick = False
        self.rightClick = False
        self.leftHold = False
        self.hover = False
        # Button proprties
        self.x = x
        self.y = y
        self.title = title # A buttons function is determined by it's title
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
        self.fontSize = 20
        self.image = None
        if (imageFile != ''):
            try:
                filePath = fileLocation + imageFile + '.jpg'
                self.image = pygame.image.load(filePath).convert()
            except:
                pass

    # Determines if the mouse pointer is in the area of the button based on the shape
    def mouseOverButton(self):
        if (self.shape == 'circle'):
            dx = self.x - pygame.mouse.get_pos()[0]
            dy = self.y - pygame.mouse.get_pos()[1]
            if ((dx**2 + dy**2)**0.5 <= self.radius+5 ):
                return True
            return False
        elif (self.shape == 'rectangle'):
            if (self.x < pygame.mouse.get_pos()[0] < self.x + self.width
                and self.y < pygame.mouse.get_pos()[1] < self.y + self.height):
                return True
            return False

    def hoverCommand(self):
        pass

    #  The procedure that need to be performed when the mouse is left clicked on the button
    def leftClickCommand(self):
        self.active = invert(self.active)
        if (self.title == 'Add Point'):
            from Point import Point
            point = Point(self.parentWindow)
            point.window()

        # Makes a particular type of transformation active and the rest inactive
        if (self.title in self.parentWindow.listOfTransformationTypes):
            if (self.active):
                self.borderColour = (0,0,255)
                self.parentWindow.activeTransformations.append(self.text)
            elif (not self.active):
                self.borderColour = (0,0,0)
                self.parentWindow.activeTransformations.remove(self.text)

        # This button determines if the coordinates of a point should be
        # displayed on the screen
        if (self.title == 'Coordinates'):
            if (self.parentWindow.showCoordinates):
                self.parentWindow.showCoordinates = False
                self.text = 'Show,Coordinates'
            else:
                self.parentWindow.showCoordinates = True
                self.text = 'Hide,Coordinates'

        # Initial amount to translate by
        (x,y,z) = (0,0,0)
        # Depending on hte title of the button the amount is added/subtracted
        # from the local variables
        if (self.title == 'PositiveXTranslation'):
            x += self.parentWindow.translationAmount

        if (self.title == 'NegativeXTranslation'):
            x -= self.parentWindow.translationAmount

        if (self.title == 'PositiveYTranslation'):
            y += self.parentWindow.translationAmount

        if (self.title == 'NegativeYTranslation'):
            y -= self.parentWindow.translationAmount

        if (self.title == 'PositiveZTranslation'):
            z += self.parentWindow.translationAmount

        if (self.title == 'NegativeZTranslation'):
            z -= self.parentWindow.translationAmount

        if ((x,y,z) != (0,0,0)):
            # The coordinates of all selected points are translated
            for point in self.parentWindow.listOfSelectedPoints:
                point.setCor(point.x+x,point.y+y,point.z+z)
            for equation in self.parentWindow.listOfSelectedEquations:
                for point in equation.listOfPoints:
                    if (point != ''):
                        point.setCor(point.x+x,point.y+y,point.z+z)


        # Resets all the variables that affect the view to their original value
        if (self.title == 'Reset View'):

            self.parentWindow.xRotation = 0.0
            self.parentWindow.yRotation = 0.0
            self.parentWindow.zRotation = 0.0

            self.parentWindow.prevXRotation = 0.0
            self.parentWindow.prevYRotation = 0.0

            self.parentWindow.xTranslation = 0
            self.parentWindow.yTranslation = 0

            self.parentWindow.twoDMode = True

        # An 'Equation' object is created even before any of it's equation and
        # ranges are assigned.
        # Calling the 'window' method allows the user to do so.
        if (self.title == 'Parametric Equation'):
            e = Equation(self.parentWindow, 'parametric')
            e.window()

        if (self.title == 'Cartesian Equation'):
            e = Equation(self.parentWindow, 'cartesian')
            e.window()
        # Controls whether the x,y and z axes are displayed
        if (self.title == 'Axes Display'):
            if (self.parentWindow.showAxes):
                self.parentWindow.showAxes = False
                self.text = 'Show,Axes'
            else:
                self.parentWindow.showAxes = True
                self.text = 'Hide,Axes'

        # When a user clicks on a mouse the point changes colour and gets added
        # to a list. Clicking on the 'Add Line' button will create a new 'Line' object
        # only if two points are selected
        if (self.title == 'Add Line'):
            # There must be at least two selected points to create line
            if (len(self.parentWindow.listOfSelectedPoints) >= 2):
                i = 1
                # Iterates through all the points and creates line object betewen adjacent point
                while (i < len(self.parentWindow.listOfSelectedPoints)):
                    # Creates a new line object for the two points selected by the user
                    l = Line(self.parentWindow.listOfSelectedPoints[i-1],
                             self.parentWindow.listOfSelectedPoints[i],self.parentWindow)
                    self.parentWindow.listOfLines.append(l)
                    i = i + 1
                    # If there are more than two points then creates a line between the first and last point
                if (len(self.parentWindow.listOfSelectedPoints) > 2):
                    l = Line(self.parentWindow.listOfSelectedPoints[0],
                             self.parentWindow.listOfSelectedPoints[len(self.parentWindow.listOfSelectedPoints)-1],
                             self.parentWindow)
                    self.parentWindow.listOfLines.append(l)

        if (self.title == 'Zoom Out'):
            self.parentWindow.XAxesSf = self.parentWindow.XAxesSf * 0.95
            self.parentWindow.YAxesSf = self.parentWindow.YAxesSf * 0.95
            self.parentWindow.ZAxesSf = self.parentWindow.ZAxesSf * 0.95

        if (self.title == 'Zoom In'):
            self.parentWindow.XAxesSf = self.parentWindow.XAxesSf * 1.05
            self.parentWindow.YAxesSf = self.parentWindow.YAxesSf * 1.05
            self.parentWindow.ZAxesSf = self.parentWindow.ZAxesSf * 1.05

        if (self.title == 'Drop Points'):
            self.parentWindow.dropPoint = invert(self.parentWindow.dropPoint)
            if (self.parentWindow.dropPoint):
                self.borderColour = (0,0,255)
            else:
                self.borderColour = (0,0,0)


        if (self.title == 'Brownian Motion'):
            self.parentWindow.brownianMotion = invert(self.parentWindow.brownianMotion)
            if (self.parentWindow.brownianMotion):
                self.borderColour = (0,0,255)
            else:
                self.borderColour = (0,0,0)


        if (self.title == 'Grid Lines'):
            if (self.text == 'Hide,Grid'):
                self.text = 'Show,Grid'
            else:
                self.text = 'Hide,Grid'
            self.parentWindow.drawGrid = invert(self.parentWindow.drawGrid)

        if (self.title == 'Turn Left'):
            self.parentWindow.yRotation += 90.0
            self.parentWindow.prevYRotation += 90.0

        if (self.title == 'Turn Right'):
            self.parentWindow.yRotation -= 90.0
            self.parentWindow.prevYRotation -= 90.0

        if (self.title == 'Turn Up'):
            self.parentWindow.xRotation += 90.0
            self.parentWindow.prevXRotation += 90.0

        if (self.title == 'Turn Down'):
            self.parentWindow.xRotation -= 90.0
            self.parentWindow.prevXRotation -= 90.0

        if (self.title == 'Select'):
            self.parentWindow.select = invert(self.parentWindow.select)
            self.parentWindow.translateAxes = False
            self.parentWindow.rotateAxes = False
            if (self.parentWindow.select):
                self.borderColour = (0,0,255)
            else:
                self.borderColour = (0,0,0)

        if (self.title == 'Delete'):
            while (len(self.parentWindow.listOfSelectedPoints) > 0):
                self.parentWindow.listOfSelectedPoints[0].deletePoint()
            while (len(self.parentWindow.listOfSelectedLines) > 0):
                self.parentWindow.listOfSelectedLines[0].deleteLine()

        if (self.title == 'Background'):
            self.parentWindow.lightBackground = invert(self.parentWindow.lightBackground)
            if (not self.parentWindow.lightBackground):
                self.text = 'Light,Mode'
            else:
                self.parentWindow.text = 'Dark,Mode'

        if (self.title == 'Left Click Toggle'):
            if (self.text == 'Rotate,View'):
                self.parentWindow.mkey = True
                self.text = 'Scroll,view'
            else:
                self.parentWindow.mkey = False
                self.text = 'Rotate,View'
            self.parentWindow.select = False

        if (self.title == 'Notes'):
            self.parentWindow.notes = invert(self.parentWindow.notes)
            listOfObjects = self.parentWindow.listOfWindowPoints
            listOfObjects += self.parentWindow.listOfWindowParametricEquations
            listOfObjects += self.parentWindow.listOfWindowCartesianEquations
            listOfObjects +=self.parentWindow.listOfWindowSliders
            listOfObjects += self.parentWindow.listOfWindowImages
            for objects in listOfObjects:
                try:
                    objects.root.destroy()
                except:
                    continue


        if (self.title == 'Clear'):
            if (self.parentWindow.notes):
                if (self.parentWindow.collectPoints):
                    # Allows current stroke to continue
                    self.parentWindow.listOfStrokes = [[]]
                else:
                    self.parentWindow.listOfStrokes = [] # Resets to original state
            else:
                for point in self.parentWindow.listOfPoints:
                    point.listOfTrace = []
                for equation in self.parentWindow.listOfEquations:
                    for point in equation.listOfPoints:
                        point.listOfTrace = []

        if (self.title == 'Trace'):
            if (self.text == 'Hide Trace'):
                self.text = 'Show Trace'
                self.parentWindow.showTrace = False
            else:
                self.text = 'Hide Trace'
                self.parentWindow.showTrace = True

        # Closes the program
        if (self.title == 'Close'):
            pygame.quit()
            sys.exit()

        if (self.title == 'Image'):
            i = Image(0,0,self.parentWindow.xRotation, self.parentWindow.yRotation,
                      self.parentWindow.zRotation, self.parentWindow)
            i.window() # Creates image object and opens it's window

        if (self.title == 'LOBF'):
            self.parentWindow.showLineOfBestFit = invert(self.parentWindow.showLineOfBestFit)
            if (self.parentWindow.showLineOfBestFit):
                self.text = 'Hide,LOBF'
            else:
                self.text = 'Show,LOBF'
        if (self.title == 'Settings'):
            self.parentWindow.settingsWindow()


    # Draws the button
    def showButton(self):
        if (self.shape == 'rectangle'):
            # Border
            pygame.draw.rect(self.screen, self.borderColour,
                             (self.x-2,self.y-2, self.width+3,self.height+3), 2)

            if (self.image != None):
                self.screen.blit(self.image, (self.x,self.y)) # Image
            else:
                pygame.draw.rect(self.screen, self.bgColour,
                                 (self.x, self.y, self.width,self.height), 0) # Fill
                showText(self.screen, self.text, int(self.x+self.width/2),
                         int(self.y+self.height / 2), self.fontColour,
                         self.bgColour, self.fontSize, 20)

        elif (self.shape == 'circle'):
            pygame.draw.circle(self.screen, self.bgColour, (self.x, self.y),
                               self.radius, 0) # Fill
            pygame.draw.circle(self.screen, self.borderColour, (self.x, self.y),
                               self.radius, 1) # Border
            if (self.image != None):
                self.screen.blit(self.image,
                                 (self.x - self.radius, self.y - self.radius))
            else:
                showText(self.screen, self.text, self.x, self.y, (0, 0, 0),
                         (255, 255, 255), self.fontSize, 20)
