from Buttons import Buttons
from Slider import Slider
from Image import Image
from Point import Point
from Line import Line
from Equation import Equation
from utils import *
from maths.Transformations import *
from maths.Matrices import *
from maths.Mathematical_Functions import regression
from String_Formatting import syntaxCorrection, entryFormatter, substituteValues
from tkinter import *

class Graph:
    def __init__(self, width, height, screen, parentApp):
        self.parentApp = parentApp
        self.type = None
        self.width = width
        self.height = height
        self.colour = (0, 0, 0)
        self.t = 0  # Point control variable
        self.screen = screen

        # These are lists required to keep track of and access all the different
        # objects created during the execution of the program
        self.listOfPoints = []
        self.listOfButtons = []
        self.listOfTransformationTypes = ['Rotation', 'Reflection', 'Scale']
        self.listOfLines = []
        self.listOfEquations = []
        self.listOfSelectedPoints = []
        self.listOfSelectedEquations = []
        self.listOfSelectedLines = []
        self.listOfImages = []

        self.XAxesSf = 40 # Zoom value
        self.YAxesSf = 40 # Zoom value
        self.ZAxesSf = 40 # Zoom value
        # Used to determine which transformation must be performed next on the selected points
        self.transformationParametersList = []

        self.buttonsCreated = False
        self.dropPoint = False

        self.rotationAngle = 20 # How many degrees to rotate points by at every instance
        self.radius = 10 # Radius of circles representing points

        self.axesTransformation = [[1,0,0,0],
                                   [0,1,0,0],
                                   [0,0,1,0],
                                   [0,0,0,1]]
        self.activeTransformations = []

        self.pointTransformation = [[1,0,0,0],
                                    [0,1,0,0],
                                    [0,0,1,0],
                                    [0,0,0,1]]# Identity matrix


        self.rotateAxes = False # Does the user want to see the points from a different perspective?
        self.axesRotationMousePos = None # Position of the mouse the instant the user activates the axes rotation function
        self.xRotation = 0.0 # Angle my which axes have been rotated about the x-axis
        self.yRotation = 0.0 # Angle my which axes have been rotated about the y-axis
        self.zRotation = 0.0 # Angle my which axes have been rotated about the y-axis
        self.prevXRotation = 0.0 # alias for 'self.xRotation'
        self.prevYRotation = 0.0 # alias for 'self.yRotation'

        self.translateAxes = False # Does the user want to scroll around the view?
        self.translateAxesMousePos = None # Position of the mouse the instant the user activates the translation function
        self.xTranslation = 0 # Amount to shift in horizontal direction
        self.yTranslation = 0 #  Amount to shift in vertical direction
        self.prevXTranslation = 0 # alias for 'self.xTranslation'
        self.prevYTranslation = 0 # alias for 'self.yTranslation'

        self.translationAmount = 1 # How many units to translate points by at every instance

        self.brownianMotion = False
        self.randomSpeed = 5

        self.lightBackground = True
        # These points will be used as a reference to draw the axes
        self.listOfGridLines = []
        self.listOfAxisPoints = []

        self.drawGrid = True
        # Calculating points at the end of gridlines and creating line
        calculateGridPoints(20, 20, 20, 1, 1 ,1, self, 0, 0, 0)


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

        self.origin = Point(self)
        self.origin.setCor(0,0,0)
        self.listOfAxisPoints.append(self.origin)

        # View control variables
        self.showCoordinates = False

        self.showAxes = True
        self.drawGrid = True

        # Selection tool
        self.select = False # Determines wether the user is usign the selection tool
        self.selectionPoint1 = () # The initial point where the user starts defining the area to be selected
        self.selectionPoint2 = () # The final point where the user chooses the area
        self.unselect = False
        self.tempSelectedPoints = []

        self.showTrace = True # Draw trace of points
        self.gradientForTrace = False # Draw with gradient colour
        self.lineForTrace = False # Draw lines between points
        self.trailEffect = False
        self.repeatTrace = False

        self.showTab = False
        self.mkey = False
        self.factList = ['Did you know..., that 1729 is the smallest number that can be represented as the sum of cubes of two pairs of integers:, 1729 = 9^3 + 10^3 = 12^3 + 1^3',
                         'Did you know..., that the sum of the reciprocals of the squares of the natural numbers is pi^2/6?',
                         'This fibonacci joke is as bad as the last two combined']
        self.jokeList = []

        self.listOfSliders = [Slider('radius', 'radius', 950, 0, 1, 20, self,
                                     self, 100, 50, 'integers',10),
                              Slider('rotation angle', 'rotationAngle', 950, 52,
                                     4, 90, self, self, 100, 50, 'integers',30),
                              Slider('t', 't', 950,104, -10, 10, self, self, 100,
                                     50, '',0),
                              Slider('random speed', 'randomSpeed', 950, 156, 0,
                                     10, self, self, 100, 50, 'integers',5)]

        self.notes = False # Determines which mode to switch to
        self.listOfStrokes = [[]] # List of points drawn by user
        self.collectPoints = False # Determines if the current position of a mouse is part of the latest stroke

        self.fact = True

        self.listOfWindowPoints = []
        self.listOfWindowParametricEquations = []
        self.listOfWindowCartesianEquations = []
        self.listOfWindowSliders = []
        self.listOfWindowImages = []

        self.lineOfBestFit = Equation(self,'parametric')
        (self.lineOfBestFit.xEquation,
         self.lineOfBestFit.yEquation,
         self.lineOfBestFit.zEquation) = ('t','at+b','0')
        self.showLineOfBestFit = False

        self.showNumberline = False

        self.buttonselected = False

    def settingsWindow(self):
        self.root = Tk()
        self.root.title('Settings')
        self.root.geometry('220x200+'+str(int(self.width/2))+'+'+str(int(0)))
        self.root.attributes('-topmost',True)

        traceLabel = Label(self.root, text = "Trace Settings")
        traceLabel.grid(row = 0, column = 0)

        a = BooleanVar()
        gradientButton = Checkbutton(self.root,background = 'white',
                                     text = "Gradient colouring", variable = a,
                                     onvalue = True, offvalue = False,
                                     command = lambda a = a,self = self: exec("self.gradientForTrace = a.get()"))
        gradientButton.grid(row = 1, column = 0, columnspan = 2)
        if (self.gradientForTrace):
            gradientButton.select()


        b = BooleanVar()
        trailButton = Checkbutton(self.root,background = 'white',
                                  text = "Trail effect", variable = b,
                                  onvalue = True, offvalue = False,
                                  command = lambda b = b,self = self: exec("self.trailEffect = b.get()"))
        trailButton.grid(row = 2, column = 0)
        if (self.trailEffect):
            trailButton.select()

        c = BooleanVar()
        lineButton = Checkbutton(self.root,background = 'white',
                                 text = "Draw lines", variable = c,
                                 onvalue = True, offvalue = False,
                                 command = lambda c = c,self = self: exec("self.lineForTrace = c.get()"))
        lineButton.grid(row = 3, column = 0)
        if (self.lineForTrace):
            lineButton.select()

        d = BooleanVar()
        repeatButton = Checkbutton(self.root,background = 'white',
                                   text = "Repeat trace", variable = d,
                                   onvalue = True, offvalue = False,
                                   command = lambda d = d,self = self: exec("self.repeatTrace = d.get()"))
        repeatButton.grid(row = 4, column = 0)
        if (self.repeatTrace):
            repeatButton.select()
        Label(self.root, text = "Other").grid(row = 6, column = 0)
        e = BooleanVar()
        numberButton = Checkbutton(self.root,background = 'white',
                                   text = "Numberline", variable = e,
                                   onvalue = True, offvalue = False,
                                   command = lambda e = e,self = self: exec("self.showNumberline = e.get()"))
        numberButton.grid(row = 7, column = 0)
        if (self.showNumberline):
            numberButton.select()

    def showFact(self):
        img = pygame.image.load(fileLocation + 'Loading'+'.jpg')
        #self.screen.blit(img, (int(self.width*0.4),int(self.height*0.2)))
        showText(self.screen, 'Please wait while we calculate the points on your graph. Thank You',
                 int(self.width/2), 10, (0,0,0), (200,200,200), 35)
        if (self.fact):
            #self.fact = False
            randNum = randint(0,len(self.factList)-1)
            y = int(self.height/2)
            showText(self.screen, 'Please wait while we calculate the points on your graph. Thank You',
                     int(self.width/2), y-50, (0,0,0), (200,200,200), 35)
            showText(self.screen, self.factList[randNum], int(self.width/2), y,
                     (0,0,0), (200,200,200), 35)
        else:
            listOfJokes = ['Joke1']
            #self.fact  = True
            i = randint(1,5)
            showImage(self.screen, 'Joke'+str(i), width/4,50)
        pygame.display.update()

    # Takes the relevant information, gets the required transformation matrix and transforms the point
    def getTransformationMatrix(self, transformation, prop1 = None,
                                prop2 = None, prop3 = None):
        if (transformation == 'Rotation'):
            matrix = rotation(prop2,prop1)

        elif (transformation == 'Reflection'):
            matrix = reflection(prop1)

        elif (transformation == 'Scale'):
            matrix = scale(prop1, prop2, prop3)

        elif (transformation == 'Translation'):
            matrix  = translation(prop1, prop2, prop3)

        elif (transformation == 'RotationAboutLine'):
            matrix = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]] # Identity matrix
            for line in self.listOfSelectedLines: # Iterates through all the selected lines
                # Combines transformations for individual lines by multiplying the matrices
                matrix = matrixMultiply(matrix, rotationAboutLine(prop2, line))
        return matrix


    def setCor(self,x,y,z):
        (self.x,self.y,self.z) = (round(x,3),round(y,3),round(z,3))
        self.posvec = [[x],[y],[z],[1]]
        self.cor = [x,y,z]

    #  List of all the buttons and their properties which are created at the start of the program
    def createButtons(self):

        listOfImages = ["\Close","\Point", "\Parametric Equation", "\Cartesian Equation", "\Line","\Rotation", "\Reflection", "\Scale", "\Coordinates", "\Coordinates", "\Reset View", "\Zoom In", "\Zoom Out"]
        #                 [title       ,text              ,x   ,y   ,width ,height ,radius ,shape,     fontSize, fontColour      ,borderColour,    bgColour,       parentWindow, imageFile]
        listOfButtons = [['Image'      ,'Image'     ,self.width-50 ,1   ,50    ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], ''],
                         ['Add Point'  ,'Add,Point'       ,50   ,40  ,50    ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], 'Point'],
                         ['Parametric Equation','Parametric,Equation',100   ,40  ,50    ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], 'Parametric Equation'],
                         ['Cartesian Equation','Cartesian,Equation',150  ,40  ,50    ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], 'Cartesian Equation'],
                         ['Add Line'  ,'Add,Line'        ,200 ,40  ,50    ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], 'Line'],
                         ['Rotation'   ,'Rotation'        ,250 ,40  ,50   ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], 'Rotation'],
                         ['Reflection' ,'Reflection'      ,300 ,40  ,50    ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], 'Reflection'],
                         ['Scale'      ,'Scale'           ,350 ,40  ,50    ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], 'Scale'],
                         ['Coordinates','Show,Coordinates',400 ,40  ,50    ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], 'Coordinates'],
                         ['Axes Display','Hide,Axes'      ,450 ,40  ,50    ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], 'Coordinates'],
                         ['Reset View','Reset,View'       ,self.width-60 , self.height-50,50    ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], 'Reset View'],
                         ['Zoom In'      ,'Zoom,In'  ,self.width-60   ,self.height-150  ,50    ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], 'Zoom In'],
                         ['Zoom Out'      ,'Zoom,Out'  ,self.width-60  ,self.height-100  ,50  ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], 'Zoom Out'],
                         ['NegativeXTranslation'  ,'-X'   ,self.width-90 ,90  ,120    ,30     ,30,     'circle',   30,      colours['black'],colours['red'], colours['white'], ''],
                         ['PositiveXTranslation'  ,'+X'   ,self.width-30 ,90  ,120    ,30     ,30,     'circle',   30,      colours['black'],colours['red'], colours['white'], ''],
                         ['NegativeYTranslation'  ,'-Y'   ,self.width-90 ,150  ,120    ,30     ,30,     'circle',   30,      colours['black'],colours['green'], colours['white'], ''],
                         ['PositiveYTranslation'  ,'+Y'   ,self.width-30 ,150  ,120    ,30     ,30,     'circle',   30,      colours['black'],colours['green'], colours['white'], ''],
                         ['NegativeZTranslation'  ,'-Z'   ,self.width-90 ,210  ,120    ,30     ,30,     'circle',   30,      colours['black'],colours['blue'], colours['white'], ''],
                         ['PositiveZTranslation'  ,'+Z'   ,self.width-30 ,210  ,120    ,30     ,30,     'circle',   30,      colours['black'],colours['blue'], colours['white'], ''],
                         ['Select'      ,'Select'  ,500   ,40  ,50    ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], 'Select'],
                         ['Drop Points'      ,'Drop,Points'  ,550   ,40  ,50    ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], 'Drop Points'],
                         ['Brownian Motion'      ,'Brownian,Motion'  ,600  ,40  ,50    ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], 'Brownian Motion'],
                         ['Grid Lines'      ,'Hide,Grid'  ,650  ,40  ,50    ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], 'Grid'],
                         ['Turn Right'      ,'Turn Right   '  ,self.width-60  ,self.height-250  ,50    ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], ''],
                         ['Turn Left'      ,'Turn Left    '  ,self.width-60  ,self.height-300  ,50    ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], ''],
                         ['Turn Up'      ,'Turn Up   '  ,self.width-60  ,self.height-350  ,50    ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], ''],
                         ['Turn Down'      ,'Turn Down    '  ,self.width-60  ,self.height-400  ,50    ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], ''],
                         ['Delete'      ,'Delete,Selection,'  ,700  ,40  ,50    ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], 'Delete'],
                         ['Background'      ,'Dark,Mode'  ,750  ,40  ,50    ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], 'Background'],
                         ['Left Click Toggle'      ,'Rotate,View'  ,800  ,40  ,50    ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], 'Left Click Toggle'],
                         ['Notes'      ,'Notes'  ,850  ,40  ,50    ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], 'Pen'],
                         ['Clear'      ,'Clear'  ,self.width-60  ,self.height-200  ,50    ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], ''],
                         ['Trace'      ,'Hide Trace'  ,self.width-60  ,self.height-450  ,50    ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], ''],
                         ['LOBF'      ,'Show,LOBF'  ,self.width-100  ,0  ,50    ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], ''],
                         ['Settings'      ,'Settings'  ,self.width-150  ,0  ,50    ,50     ,None,  'rectangle', 30,      colours['black'],colours['black'],colours['white'], '']]





        for button in listOfButtons:
            buttonObject = Buttons(button[0], button[1], button[2], button[3],
                                   button[4], button[5], button[6], button[7],
                                   button[8], button[9], button[10], button[11],
                                   self, button[12])
            self.listOfButtons.append(buttonObject)

    # This function responds to the inputs given by the user. This is like the OS of the entire program.
    def checkEvents(self):
        self.buttonselected = False
        if (self.notes): # Note mode
            for button in self.listOfButtons:
                if (button.title in ['Notes','Clear']):
                    button.showButton()

            for event in self.parentApp.events:
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()
                # Undo function
                if (pygame.key.get_pressed()[pygame.K_LCTRL] != 0
                    and pygame.key.get_pressed()[pygame.K_z] != 0):
                    if (len(self.listOfStrokes) == 1):
                        self.listOfStrokes = [[]]
                    else:
                        # Deletes latest stroke
                        del self.listOfStrokes[len(self.listOfStrokes)-1]
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    if (event.button == 1):
                        # Only these two buttons work in this mode
                        for button in self.listOfButtons:
                            if (button.title in ['Notes','Clear']
                                and button.mouseOverButton()):
                                button.leftClickCommand()
                                break
                        # Adds a new stroke with the current mouse position as starting point
                        self.listOfStrokes.append([pygame.mouse.get_pos()])
                        self.collectPoints = True # Marks beginning of stroke

                if (event.type == pygame.MOUSEMOTION):
                    if (self.collectPoints):
                        # Adds the current position of the mouse to the latest stroke
                        if(len(self.listOfStrokes) != 0):
                            self.listOfStrokes[len(self.listOfStrokes)-1].append(pygame.mouse.get_pos())

                if (event.type == pygame.MOUSEBUTTONUP):
                    if (event.button == 1):
                        self.collectPoints = False # Completes stroke

        else:
            if (pygame.key.get_pressed()[pygame.K_b] != 0):
                self.brownianMotion = True

            if (pygame.key.get_pressed()[pygame.K_n] != 0):
                self.brownianMotion = False

            if (pygame.key.get_pressed()[pygame.K_c] != 0):
                for point in self.listOfSelectedPoints:
                    point.listOfTrace = []

            if (pygame.key.get_pressed()[pygame.K_m] != 0):
                self.mkey == invert(self.mkey)

            if (pygame.key.get_pressed()[pygame.K_y] != 0):
                self.zRotation += 5

            if (pygame.key.get_pressed()[pygame.K_u] != 0):
                self.zRotation -= 5

            if (pygame.key.get_pressed()[pygame.K_h] != 0):
                self.XAxesSf = 40
                self.YAxesSf = 40
                self.ZAxesSf = 40


            for event in self.parentApp.events:
              #This is necessary for the window to close easily
                if (event.type == pygame.QUIT):
                    listOfObjects = self.listOfWindowPoints
                    listOfObjects += self.listOfWindowParametricEquations
                    listOfObjects += self.listOfWindowCartesianEquations
                    listOfObjects += self.listOfWindowSliders
                    listOfObjects += self.listOfWindowImages
                    for objects in listOfObjects:
                        try:
                            objects.root.destroy()
                        except:
                            continue
                    pygame.quit()
                    sys.exit()

                # If the user clicks the mouse
                if (event.type == pygame.MOUSEBUTTONDOWN):

                    if (event.button == 1): # If user left clicks

                        # If the user clicks on a button it's command is initated
                        for button in self.listOfButtons:
                            if (button.mouseOverButton()):
                                button.leftHold = True
                                button.leftClick = True
                                self.buttonselected = True
                        '''
                        for i in range(0,self.parentApp.numberOfTabs): # Iterates thorugh all the visible tabs
                            tab = self.parentApp.listOfTabs[i]
                            if (tab.mouseOverButton() ): # If the user clicks on the tab
                                self.buttonselected = True
                                self.parentApp.currentTab = tab.title # the currentTab becomes the title of the tab
                                tab.fontColour = (255,0,0) # highlights current tab
                                if (i == 1):
                                    pygame.display.set_caption('Elastic Collisions In One Dimension')
                                else:
                                    pygame.display.set_caption('Graphulator')
                                self.buttonselected = True

                        # To add an extra tab
                        if (self.parentApp.newTabButton.mouseOverButton()  and self.parentApp.numberOfTabs < self.parentApp.maxTabs):
                            self.buttonselected = True
                            self.parentApp.numberOfTabs += 1 # Increments number of tabs
                            self.parentApp.newTabButton.x += 100 # Shifts button to the right
                        '''

                        # Checks if the user wants to move any slider
                        equation = None
                        if (len(self.listOfSelectedEquations) > 0):
                            lastIndex = len(self.listOfSelectedEquations) - 1
                            equation = self.listOfSelectedEquations[lastIndex]

                        elif (len(self.listOfEquations) == 1):
                            equation = self.listOfEquations[0]

                        if (equation != None):
                            for slider in equation.listOfSliders:
                                if (slider.pointer.mouseOverPoint()):
                                    slider.movePointer = True
                                    self.buttonselected = True

                        point = None
                        if (len(self.listOfSelectedPoints) == 1):
                            point = self.listOfSelectedPoints[0]
                            slider = point.slider
                            if (slider.pointer.mouseOverPoint()):
                                slider.movePointer = True
                                self.buttonselected = True

                        for slider in self.listOfSliders:
                            if (slider.pointer.mouseOverPoint()):
                                slider.movePointer = True
                                self.buttonselected = True

                        if (not self.buttonselected):
                            # Checks if the user has clicks on any point
                            for point in self.listOfPoints:
                                # If the user has clicked on a point...
                                if (point.mouseOverPoint()):
                                    self.buttonselected = True
                                    # If the point was already selected ...
                                    if (point in self.listOfSelectedPoints):
                                        # It is unselected...
                                        self.listOfSelectedPoints.remove(point)
                                        # If the point is individual and wasn't selected
                                    elif (point.equation == None):
                                        # It is selected
                                        self.listOfSelectedPoints.append(point)
                                    break


                        if (not self.buttonselected):
                            for equation in self.listOfEquations:
                                # If equation was already selected then it is unselected
                                if (equation.mouseOverGraph()):
                                    self.buttonselected = True
                                    if (equation in self.listOfSelectedEquations):
                                        self.listOfSelectedEquations.remove(equation)
                                        equation.thickness = 1 # Normal thickness

                                    else: # Equation is selected
                                        self.listOfSelectedEquations.append(equation)
                                        equation.thickness = 2 # Bold
                                    break

                        if (not self.buttonselected):
                            for line in self.listOfLines:
                                if (line.mouseOverLine()):
                                    self.buttonselected = True
                                    if (line in self.listOfSelectedLines):
                                        self.listOfSelectedLines.remove(line)
                                        #print(self.listOfSelectedLines)

                                    else:
                                        self.listOfSelectedLines.append(line)
                                        #print(self.listOfSelectedLines)
                                    break

                        # If the user left-clicks but doesn't click on any
                        # button then that means the user has clicked on the screen
                        if (not self.buttonselected):
                            if (self.select):
                                # First vertex of rectangle
                                self.selectionPoint1 = pygame.mouse.get_pos()
                                self.buttonselected = True

                            elif (self.dropPoint):
                                createPoint(self)
                                self.buttonselected = True

                        # To determine if the user wants to move an image
                        if (not self.buttonselected):
                            for image in self.listOfImages:
                                if (image.mouseOverImage()):
                                    self.buttonselected = True
                                    image.move = True
                                    self.buttonselected = True
                                    break



                        if (not self.buttonselected):
                            if (self.mkey):
                                self.rotateAxes = True
                                self.axesRotationMousePos = pygame.mouse.get_pos()

                            else:
                                self.axesTranslationMousePos = pygame.mouse.get_pos()
                                self.translateAxes = True
                                self.select = False


                    # If the user presser the middle button i.e. the scroll bar
                    # buttton then that means the user wants to rotate the axes
                    elif (event.button == 2):
                        self.rotateAxes = True
                        # Records the position of the mouse when the user
                        # presses the middle button to calculate the angle by
                        # which the axes need to be rotated
                        self.axesRotationMousePos = pygame.mouse.get_pos()

                    # If the user right clicks on a point, if the point is a
                    # part of an equation, then the equation's window is
                    # displayed or else the point's individual window is displayed
                    elif (event.button == 3):
                        for point in self.listOfPoints:
                            if (point.mouseOverPoint()
                                and point.equation == None):
                                if (not point.windowOpen):
                                    point.window()
                            if (point.slider.mouseOverSlider()
                                and point in self.listOfSelectedPoints
                                and len(self.listOfSelectedPoints) == 1):
                                if (not point.slider.windowOpen):
                                    point.slider.window()
                        # Opens the window of an equation object if user
                        # right-clicks on graph
                        for equation in self.listOfEquations:
                            if (equation != self.lineOfBestFit):
                                if (equation.mouseOverGraph()
                                    and not equation.windowOpen):
                                    equation.window()
                                for slider in equation.listOfSliders:
                                    if (slider.mouseOverSlider()
                                        and (equation in self.listOfSelectedEquations
                                             or len(self.listOfEquations) == 1)):
                                        if (not slider.windowOpen):
                                            slider.window()

                        for slider in self.listOfSliders:
                            if (slider.mouseOverSlider()
                                and not slider.windowOpen):
                                slider.window()

                        if (self.select ):
                            self.selectionPoint1 = pygame.mouse.get_pos()
                            # Indicates that the user wants to unselect
                            self.unselect = True

                        for image in self.listOfImages:
                            if (image.mouseOverImage()):
                                if (not image.windowOpen):
                                    image.window()

                    #If the user scrolls up
                    if (event.button == 4):
                        self.XAxesSf = self.XAxesSf * 1.1
                        self.YAxesSf = self.YAxesSf * 1.1
                        self.ZAxesSf = self.ZAxesSf * 1.1

                    #If the user scrolls down
                    if (event.button == 5):
                        self.XAxesSf = self.XAxesSf * 0.9
                        self.YAxesSf = self.YAxesSf * 0.9
                        self.ZAxesSf = self.ZAxesSf * 0.9

                #If the user releases any of the mouse buttons
                if (event.type == pygame.MOUSEBUTTONUP):
                    if (event.button == 1):
                        self.collectPoints = False
                        if (self.mkey ):
                            self.rotateAxes = False
                            self.prevXRotation = self.xRotation
                            self.prevYRotation = self.yRotation

                        if (self.select ):
                            if (self.selectionPoint1 != ()):
                                #Resets attributes back to original state
                                self.selectionPoint1 = ()
                                self.tempSelectedPoints = []

                        for button in self.listOfButtons:
                            if (button.leftClick
                                and button.mouseOverButton()):
                                button.leftClickCommand()
                                button.leftClick = False
                            button.leftHold = False
                        # I
                        self.translateAxes = False
                        self.prevXTranslation = self.xTranslation
                        self.prevYTranslation = self.yTranslation

                        for equation in self.listOfEquations:
                            if (equation.showSliders):
                                for slider in equation.listOfSliders:
                                    slider.movePointer = False

                        for point in self.listOfPoints:
                            point.slider.movePointer = False

                        for slider in self.listOfSliders:
                            slider.movePointer = False


                        for image in self.listOfImages:
                            image.move = False

                    elif (event.button == 2):
                        self.rotateAxes = False
                        self.prevXRotation = self.xRotation
                        self.prevYRotation = self.yRotation

                    elif (event.button == 3):
                        # Resets attributes back to the original state
                        if (self.select ):
                            self.unselect = False
                            self.selectionPoint1 = ()
                            self.tempSelectedPoints = []

    def selectPoints(self):
        for point in self.listOfPoints: # Iterates through all the individual points
            if (point.equation == None):  # Checks if the onscreen x and y coordinates are in the region of the rectangle selected by the user
                if (min(self.selectionPoint1[0],self.selectionPoint2[0]) <= point.screenPos[0]
                    and point.screenPos[0] <= max(self.selectionPoint1[0],self.selectionPoint2[0])
                    and min(self.selectionPoint1[1],self.selectionPoint2[1]) <= point.screenPos[1]
                    and point.screenPos[1] <= max(self.selectionPoint1[1],self.selectionPoint2[1])):
                    if (point not in self.listOfSelectedPoints): # Selects point if not already in the list
                         self.listOfSelectedPoints.append(point)
                    else: # If the point is already in the list then it is removed
                         self.listOfSelectedPoints.remove(point)

    # Determines the transformation that the user wants to do on the points by looking at which button is clicked and which key is pressed
    def determineTransformation(self):
        info = ''
        if ('Rotation' in self.activeTransformations):
            info = 'Press the <- and -> keys to rotate about the y-axis,Press the up and down keys to rotate about the x-axis,Press the Z and X to rotate about the z-axis'
            showText(self.screen, info, int(self.width/2), 110, (0,0,0), (200,200,200), 30)
            transformation = None
            if (pygame.key.get_pressed()[pygame.K_RIGHT] != 0):
                transformation = ['Rotation','y',self.rotationAngle,None]
            if (pygame.key.get_pressed()[pygame.K_LEFT] != 0):
                transformation = ['Rotation','y',-self.rotationAngle,None]
            if (pygame.key.get_pressed()[pygame.K_UP] != 0):
                transformation = ['Rotation','x',self.rotationAngle,None]
            if (pygame.key.get_pressed()[pygame.K_DOWN] != 0):
                transformation = ['Rotation','x',-self.rotationAngle,None]
            if (pygame.key.get_pressed()[pygame.K_z] != 0):
                transformation = ['Rotation','z',-self.rotationAngle,None]
            if (pygame.key.get_pressed()[pygame.K_x] != 0):
                transformation = ['Rotation','z',self.rotationAngle,None]
            if (pygame.key.get_pressed()[pygame.K_r] != 0):
                transformation = ['RotationAboutLine', None,
                                  self.rotationAngle,None]
            if (pygame.key.get_pressed()[pygame.K_t] != 0):
                    transformation = ['RotationAboutLine', None,
                                      -self.rotationAngle,None]
            if (transformation != None):
                self.transformationParametersList.append(transformation)


        else:
            if (pygame.key.get_pressed()[pygame.K_RIGHT] != 0):
                self.yRotation += 10
            if (pygame.key.get_pressed()[pygame.K_LEFT] != 0):
                self.yRotation -= 10
            if (pygame.key.get_pressed()[pygame.K_UP] != 0):
                self.xRotation += 10
            if (pygame.key.get_pressed()[pygame.K_DOWN] != 0):
                self.xRotation -= 10


        if ('Reflection' in self.activeTransformations):
            if (pygame.key.get_pressed()[pygame.K_a] != 0
                or pygame.key.get_pressed()[pygame.K_d] != 0):
                self.transformationParametersList.append(['Reflection', 'x', None, None])
            if (pygame.key.get_pressed()[pygame.K_w]!=0
                or pygame.key.get_pressed()[pygame.K_s] != 0):
                self.transformationParametersList.append(['Reflection', 'y', None, None])
            if (pygame.key.get_pressed()[pygame.K_q]!=0
                or pygame.key.get_pressed()[pygame.K_e] != 0):
                self.transformationParametersList.append(['Reflection', 'z', None, None])
        else:
            if (pygame.key.get_pressed()[pygame.K_a]!=0):
                self.xTranslation -= 5
            if (pygame.key.get_pressed()[pygame.K_d]!=0):
                self.xTranslation += 5
            if (pygame.key.get_pressed()[pygame.K_w]!=0):
                self.yTranslation -= 5
            if (pygame.key.get_pressed()[pygame.K_s]!=0):
                self.yTranslation += 5

        if ('Scale' in self.activeTransformations):
            if (pygame.key.get_pressed()[pygame.K_PERIOD] != 0):
                self.transformationParametersList.append(['Scale', 1.05, 1, 1])
            if (pygame.key.get_pressed()[pygame.K_COMMA] != 0):
                self.transformationParametersList.append(['Scale', 0.95, 1, 1])

            if (pygame.key.get_pressed()[pygame.K_RIGHTBRACKET] != 0):
                self.transformationParametersList.append(['Scale', 1, 1.05, 1])
            if (pygame.key.get_pressed()[pygame.K_LEFTBRACKET] != 0):
                self.transformationParametersList.append(['Scale', 1, 0.95, 1])

            if (pygame.key.get_pressed()[pygame.K_RSHIFT] != 0):
                self.transformationParametersList.append(['Scale', 1, 1, 1.05])
            if (pygame.key.get_pressed()[pygame.K_LSHIFT] != 0):
                self.transformationParametersList.append(['Scale', 1, 1, 0.95])
        else:
            if (pygame.key.get_pressed()[pygame.K_PERIOD] != 0):
                self.XAxesSf *= 1.05
            if (pygame.key.get_pressed()[pygame.K_COMMA] != 0):
                self.XAxesSf *= 0.95

            if (pygame.key.get_pressed()[pygame.K_RIGHTBRACKET] != 0):
                self.YAxesSf *= 1.05
            if (pygame.key.get_pressed()[pygame.K_LEFTBRACKET] != 0):
                self.YAxesSf *= 0.95

            if (pygame.key.get_pressed()[pygame.K_RSHIFT] != 0):
                self.ZAxesSf *= 1.05
            if (pygame.key.get_pressed()[pygame.K_LSHIFT] != 0):
                self.ZAxesSf *= 0.95
        # Calculates the matrix that transforms the point at this instance
        self.calculatePointTransformation()


    def calculatePointTransformation(self):
        # Initialises as the identity martrix
        self.pointTransformation = [[1,0,0,0],
                                    [0,1,0,0,],
                                    [0,0,1,0],
                                    [0,0,0,1]]
        # Iterates through each list containing the transforamtion parameters
        for transformationParameters in self.transformationParametersList:
            matrix = self.getTransformationMatrix(transformationParameters[0],
                                                  transformationParameters[1],
                                                  transformationParameters[2],
                                                  transformationParameters[3]) # Gets matrix
            # Multiplies matrices to combines into single matrix
            self.pointTransformation = matrixMultiply(self.pointTransformation, matrix)

        self.transformationParametersList = [] # Resets list to empty for next cycle

    def updatePoints(self):
        for point in self.listOfPoints: # Iterates through all points
            point.calculateScreenPos()
            if (self.selectionPoint1 != () and point.visible() ): # Checks if point is within the selected region
                if (min(self.selectionPoint1[0],pygame.mouse.get_pos()[0]) <= point.screenPos[0]
                    and point.screenPos[0] <= max(self.selectionPoint1[0],pygame.mouse.get_pos()[0])
                    and min(self.selectionPoint1[1],pygame.mouse.get_pos()[1]) <= point.screenPos[1]
                    and point.screenPos[1] <= max(self.selectionPoint1[1],pygame.mouse.get_pos()[1])):

                    if (not self.unselect): # If the user is selecting
                        # If the point is not already selected
                        if (point not in self.listOfSelectedPoints):
                             self.listOfSelectedPoints.append(point) # it is added to the list
                             # To determine whether the poimt has been selected
                             # during current session
                             self.tempSelectedPoints.append(point)

                    elif (self.unselect): # If the user is unselecting
                        if (point in self.listOfSelectedPoints): # If the point was selected
                            self.listOfSelectedPoints.remove(point)# It is removed
                            # To determine that it was unselected during current session
                            self.tempSelectedPoints.append(point)

                else: # If point not in the region
                    if (not self.unselect):# If user is selecting
                        # If the point had been selected in this session
                        if (point in self.tempSelectedPoints):
                            self.listOfSelectedPoints.remove(point)# It is unselected
                            self.tempSelectedPoints.remove(point)

                    else: # If user is unselecting
                        # If the point has been unselected during this session
                        if (point in self.tempSelectedPoints):
                            self.listOfSelectedPoints.append(point) # If selected again
                            self.tempSelectedPoints.remove(point)


            if (self.showTrace):
                if (self.repeatTrace):
                    listOfCor = []
                else:
                     # Creates new list with only coordinates of points
                    listOfCor = list(map(lambda x: x.cor,point.listOfTrace))

                cor = (point.x,point.y,point.z) # Current coordinates of point

                if (cor not in listOfCor): # Avoids duplication
                    if (point.x != None):
                        p = Point(self)
                        p.setCor(point.x,point.y,point.z)
                        point.listOfTrace.append(p)

            if (point in self.listOfSelectedPoints):
                if ('t' not in syntaxCorrection(point.x2, False)+syntaxCorrection(point.y2,False)+syntaxCorrection(point.z2,False)):
                    point.transformPoint()

            if (point.visible()):
                point.show()
            point.drawTrace()

            if (point.windowOpen):
                pygame.draw.aaline(self.screen, point.colour, point.screenPos,
                                   (point.root.winfo_x(), point.root.winfo_y()))


    def updateLines(self):
        for line in self.listOfLines:
            if (line.visible()):
                line.drawLine()

    def screenCor(self,posvec):
        x = posvec[0][0]
        y = posvec[1][0]
        x = x + self.width/2
        y = self.height/2 - y
        return (int(x),int(y))

    def drawGradientBackground(self):
        # Draws background
        colour = 0
        rectHeight = 10
        height = self.height - rectHeight

        while (height + rectHeight > 0):
            if (colour> 255):
                break
            pygame.draw.rect(self.screen, (colour,colour,colour),
                             (0,height,self.width,rectHeight), 0)
            height -= rectHeight
            colour = 255 - int(255*(height/self.height))

    def drawAxes(self):
        for point in self.listOfAxisPoints:
            point.calculateScreenPos()
        self.drawGridLines()
        # Draws the lines representing the axes
        if (self.showAxes):
            pygame.draw.aaline(self.screen, (255,0,0), self.x1.screenPos,
                               self.x2.screenPos, 2)
            pygame.draw.aaline(self.screen, (0,255,0), self.y1.screenPos,
                               self.y2.screenPos, 2)
            pygame.draw.aaline(self.screen, (0,0,255), self.z1.screenPos,
                               self.z2.screenPos, 2)
            #Labels each end of the axes with the required letter
            showText(self.screen, '-X', self.x1.screenPos[0],
                     self.x1.screenPos[1], (0,0,0), (200,200,200), 30)
            showText(self.screen, '+X', self.x2.screenPos[0],
                     self.x2.screenPos[1], (0,0,0), (200,200,200), 30)

            showText(self.screen,'-Y', self.y1.screenPos[0],
                     self.y1.screenPos[1], (0,0,0), (200,200,200), 30)
            showText(self.screen,'+Y', self.y2.screenPos[0],
                     self.y2.screenPos[1], (0,0,0), (200,200,200), 30)

            if ((self.xRotation, self.yRotation) != (0.0, 0.0)):
                showText(self.screen,'+Z', self.z1.screenPos[0],
                         self.z1.screenPos[1], (0,0,0), (200,200,200), 30)
                showText(self.screen,'-Z', self.z2.screenPos[0],
                         self.z2.screenPos[1], (0,0,0), (200,200,200), 30)

    def drawGridLines(self):
        for line in self.listOfGridLines:
            if (line.visible()):
                if (self.lightBackground):
                    line.colour = (150,150,150)
                else:
                    line.colour = (255,255,255)
                if (self.drawGrid):
                    line.drawLine(self.showNumberline)

    def calculateAxesTransformation(self):
        # Rotates the axis by transforming the axis points by the angle and
        # scale factor required
        if (self.translateAxes):
            dx = pygame.mouse.get_pos()[0]-self.axesTranslationMousePos[0]
            self.xTranslation = self.prevXTranslation + dx
            dy = pygame.mouse.get_pos()[1]-self.axesTranslationMousePos[1]
            self.yTranslation = self.prevYTranslation + dy


        if (self.rotateAxes): # Checks if the axes need to be rotated
            self.yRotation = (self.prevYRotation + 360*(pygame.mouse.get_pos()[0]-self.axesRotationMousePos[0])/self.width)%360
            # This takes the previous angle by which the axes were rotated and then adds the additional angle which is determined by
            #the percentage of the distance between the point that the user pressed the middle button and the current position of the mouse
            self.xRotation =  (self.prevXRotation + 360*(pygame.mouse.get_pos()[1]-self.axesRotationMousePos[1])/self.width)%360
            self.twoDMode = False

        #self.axesTransformation =  matrixMultiply(scale(self.XAxesSf,self.YAxesSf,self.ZAxesSf),rotation(self.xRotation,'x'))
        self.axesTransformation =  rotation(self.xRotation,'x')
        self.axesTransformation =  matrixMultiply(self.axesTransformation,
                                                  rotation(self.yRotation,'y'))
        self.axesTransformation = matrixMultiply(self.axesTransformation,
                                                 rotation(self.zRotation,'z'))
        self.axesTransformation =  matrixMultiply(self.axesTransformation,
                                                  scale(self.XAxesSf,
                                                        self.YAxesSf,
                                                        self.ZAxesSf))


    def updateScreen(self):
        basicfont = pygame.font.SysFont('times.ttf', 40) # initialises font for displaying text

        if (self.notes):
            for stroke in self.listOfStrokes:
                # Draws a 1 pixel circle if stroke is comprised of only one point
                if (len(stroke) == 1):
                    pygame.draw.circle(self.screen, (0,0,0), stroke[0], 1, 0)
                elif(len(stroke) > 1):
                    # Draws lines between adjecent points
                    for i in range(0,len(stroke)-2):
                        pygame.draw.aaline(self.screen, (0, 0, 0),
                                           stroke[i], stroke[i+1],1)

        else:
            if (self.selectionPoint1 != ()):
                self.selectionPoint2 = pygame.mouse.get_pos()
                if (not self.unselect):
                    colour = (0,200,0)
                else:
                    colour = (200,0,0)
                self.drawSelectionBox(colour)

            self.calculateAxesTransformation()

            if (self.parentApp.numberOfTabs < self.parentApp.maxTabs):
                self.parentApp.newTabButton.showButton()

            self.drawAxes()
        # Changes the colour of the transformation buttons that are pressed

    def drawSelectionBox(self, colour):
            width = pygame.mouse.get_pos()[0]-self.selectionPoint1[0]
            height = pygame.mouse.get_pos()[1]-self.selectionPoint1[1]
            pygame.draw.rect(self.screen, colour, (self.selectionPoint1[0],
                                                   self.selectionPoint1[1],
                                                   width, height), 2)

    def updateButtons(self):
        for tab in self.parentApp.listOfTabs:
            if (int(tab.title[1:len(tab.title)]) <= self.parentApp.numberOfTabs):
                tab.showButton()
                if (tab.title == self.parentApp.currentTab):
                    tab.fontColour = (200,0,0)
                else:
                    tab.fontColour = (0,0,0)

        for button in self.listOfButtons:

            button.showButton() # Draws button onscreen

            if (button.mouseOverButton()):
                button.hover = True
            else:
                button.hover = False
            if (button.hover):
                if (button.shape == 'rectangle'):
                    #button.parentWindow.showText(button.text, int(button.x+button.width/2), int(button.y+button.height/2), button.fontColour, button.bgColour, button.fontSize+5)
                    y = button.y+button.height+7*len(button.text.split(','))
                    showText(self.screen, button.text, int(button.x+button.width/2),
                             y, (0,0,0), (255,255,255), button.fontSize+5)

                elif (button.shape == 'circle'):
                    showText(button.screen, button.text, button.x, button.y,
                             button.fontColour, button.bgColour, button.fontSize+5)
                #mouseImg = pygame.image.load('Mouse hand.png')
                #self.screen.blit(mouseImg, pygame.mouse.get_pos())



        for button in self.listOfButtons:
            # Keeps on translating the points as long as the button is held down
            if (button.leftHold
                and button.title in ['PositiveXTranslation', 'NegativeXTranslation',
                                     'PositiveYTranslation', 'NegativeYTranslation',
                                     'PositiveZTranslation','NegativeZTranslation',
                                     'Zoom In', 'Zoom Out']):
                button.leftClickCommand()

            if (button.mouseOverButton()):
                button.bgColour = (200,200,200)
            else:
                button.bgColour = (255,255,255)

    def updateEquations(self):
        if (self.showLineOfBestFit):
            listOfPoints = []
            xValues = []
            for point in self.listOfSelectedPoints:
                if (point.z == 0.0): # Extracts all selected points on the x-y plane
                    listOfPoints.append(point.cor)
                    xValues.append(point.cor[0])

            if (len(listOfPoints) > 1): # Line has to be for more than one point
                line = regression(listOfPoints)
                (self.lineOfBestFit.a, self.lineOfBestFit.b) = line
                # Line is drawn across the selected points only
                (self.lineOfBestFit.startValue,
                 self.lineOfBestFit.endValue) = (str(min(xValues)), str(max(xValues)))
                self.lineOfBestFit.calculatePoints()
                for point in self.lineOfBestFit.listOfPoints:
                    point.calculateScreenPos()
                self.lineOfBestFit.drawGraph()


        for equation in self.listOfEquations:
                for point in equation.listOfPoints:
                    point.transformPoint()
                    point.calculateScreenPos()

                    if (self.showTrace
                        and equation in self.listOfSelectedEquations):
                        captureTrace = True
                        if (len(point.listOfTrace) > 0):
                            if (point.cor == point.listOfTrace[len(point.listOfTrace)-1].cor):
                                captureTrace = False
                        if (captureTrace):
                            p = Point(self)
                            p.setCor(point.x,point.y,point.z)
                            point.listOfTrace.append(p)
                        point.drawTrace()

                equation.drawGraph()

        equation = None

        if (len(self.listOfSelectedEquations) > 0):
            i = len(self.listOfSelectedEquations)-1
            equation = self.listOfSelectedEquations[i]
            if (equation == self.lineOfBestFit
                and len(self.listOfSelectedEquations) > 1):
                equation = self.listOfSelectedEquations[i-1]

        elif (len(self.listOfEquations) == 2):
            equation = self.listOfEquations[1]


        if (equation == self.lineOfBestFit and not self.showLineOfBestFit):
            equation = None

        if (equation != None):
            if (equation.type  == 'parametric'):
                showText2(self.screen,
                          'x = '+substituteValues(equation,equation.xEquation)+' | y = '+substituteValues(equation,equation.yEquation)+' | z = '+substituteValues(equation,equation.zEquation),
                          self.width/2, self.height-180, equation.colour, (255,255,255), 20)
            else:
                showText2(self.screen, equation.cartesianEquation, self.width/2, self.height-180, equation.colour, (255,255,255), 20)
        if (self.lineOfBestFit.mouseOverGraph()):
            equation = self.lineOfBestFit
            showText2(self.screen, 'x = '+substituteValues(equation,equation.xEquation)+' | y = '+substituteValues(equation,equation.yEquation)+' | z = '+substituteValues(equation,equation.zEquation),
                      pygame.mouse.get_pos()[0],  pygame.mouse.get_pos()[1],
                      equation.colour, (255,255,255), 20)


    def updateSliders(self):
        equation = None
        if (len(self.listOfSelectedEquations) > 0):
            equation = self.listOfSelectedEquations[len(self.listOfSelectedEquations)-1]
        elif (len(self.listOfEquations) == 2):
            equation = self.listOfEquations[1]
        if (equation == self.lineOfBestFit):
            equation = None
        if (equation != None):
            for slider in equation.listOfSliders:
                if (equation != None):
                    if (equation.type == 'parametric'):
                        if (slider.text in ['limit1','limit2']
                        and equation.xEquation == 't' and equation.zEquation == '0'):
                            slider.startValue = eval(syntaxCorrection(equation.startValue))
                            slider.endValue = eval(syntaxCorrection(equation.endValue))
                            slider.drawSlider()
                            equation.limit1Point1.calculateScreenPos()
                            equation.limit1Point2.calculateScreenPos()
                            equation.limit2Point1.calculateScreenPos()
                            equation.limit2Point2.calculateScreenPos()
                            try:
                                pygame.draw.aaline(self.screen, self.colour,
                                                   equation.limit1Point1.screenPos,
                                                   equation.limit1Point2.screenPos)
                                pygame.draw.aaline(self.screen, self.colour,
                                                   equation.limit2Point1.screenPos,
                                                   equation.limit2Point2.screenPos)
                            except:
                                pass
                            showText(self.screen, 'Area:,Trp: '+str(round(integral(equation.yEquation,equation.limit1,equation.limit2,rule = 'trapezium',equation = equation),5))+',Smp: '+str(round(integral(equation.yEquation,equation.limit1,equation.limit2,rule = 'simpsons',equation = equation),5)), 50, int(self.height/2), (0,0,0), (255,255,255), 20)

                        if (slider.text in syntaxCorrection(equation.xEquation, False) or slider.text in syntaxCorrection(equation.yEquation, False) or slider.text in syntaxCorrection(equation.zEquation, False)):
                            slider.drawSlider()

                    elif (equation.type == 'cartesian'):
                        if (slider.text in equation.cartesianEquation):
                            slider.drawSlider()

                if (slider.movePointer):
                    if (slider.x <= pygame.mouse.get_pos()[0] <= slider.x + slider.width):
                        slider.pointer.setCor(pygame.mouse.get_pos()[0], slider.pointer.y, slider.pointer.z)
                        slider.pointer.screenPos = (pygame.mouse.get_pos()[0], slider.pointer.y)
                        slider.setVariable()
                        if ('limit' not in slider.text):
                            equation.calculatePoints()

        slider = []
        if (len(self.listOfSelectedPoints)==1):
            slider = [self.listOfSelectedPoints[0].slider]
        for slider in self.listOfSliders+slider:
            slider.drawSlider()
            if (slider.movePointer):
                if (slider.x < pygame.mouse.get_pos()[0] < slider.x + slider.width):
                    slider.pointer.setCor(pygame.mouse.get_pos()[0], slider.pointer.y, slider.pointer.z)
                    slider.pointer.screenPos = (pygame.mouse.get_pos()[0], slider.pointer.y)
                    slider.setVariable()

    # Updates the windows for different objects and formats the user entries where required
    def updateWindows(self):
        for point in self.listOfWindowPoints:
            try:
                entryFormatter(point.coordinatesent)
                point.root.update_idletasks()
                point.root.update()
            except:
                self.listOfWindowPoints.remove(point)
                point.windowOpen = False

        for equation in self.listOfWindowParametricEquations:
            try:
                entryFormatter(equation.xEquationent)
                entryFormatter(equation.yEquationent)
                entryFormatter(equation.zEquationent)
                entryFormatter(equation.startValueent)
                entryFormatter(equation.endValueent)
                equation.root.update_idletasks()
                equation.root.update()
            except:
                self.listOfWindowParametricEquations.remove(equation)
                equation.windowOpen = False

        for equation in self.listOfWindowCartesianEquations:
            try:
                entryFormatter(equation.cartesianEquationent)
                entryFormatter(equation.startXent)
                entryFormatter(equation.endXent)
                entryFormatter(equation.startYent)
                entryFormatter(equation.endYent)
                entryFormatter(equation.startZent)
                entryFormatter(equation.endZent)
                equation.root.update_idletasks()
                equation.root.update()
            except:
                self.listOfWindowCartesianEquations.remove(equation)
                equation.windowOpen = False

        for slider in self.listOfWindowSliders:
            try:
                slider.root.update_idletasks()
                slider.root.update()
            except:
                self.listOfWindowSliders.remove(slider)
                slider.windowOpen = False

        for image in self.listOfWindowImages:
            try:
                image.root.update_idletasks()
                image.root.update()
            except:
                self.listOfWindowImages.remove(image)
                image.windowOpen = False
        try:
            self.root.update_idletasks()
            self.root.update()
        except:
            self.windowOpen = False


    def updateImages(self):
        for image in self.listOfImages:
            if (self.xRotation == image.xAngle
                and self.yRotation == image.yAngle
                and self.zRotation == image.zAngle):
                if (image.move):
                    # Sets position of image to position of mouse
                    (image.x,image.y) = pygame.mouse.get_pos()
                # Image is only displayed if the angles are the same as when
                image.show()


    # Calls all the methods necessary for the program to function properly
    def main(self):
        if (not self.buttonsCreated):
            self.createButtons() # Creates the button objects required for the module
            self.buttonsCreated = True

        if (not self.notes):
            for i in range(0,500): # Updates the windows
                self.updateWindows()

        # Draws appropriate background
        if (not self.lightBackground):
            self.drawGradientBackground()
        else:
            self.screen.fill((255,255,255))


        self.updateImages() # Performs tasks associated with images
        self.updateScreen()

        self.checkEvents() # Responds to all valid user inputs

        if (not self.notes):
            self.determineTransformation() # Checks user inputs to identify transformations
            self.updatePoints() # Performs tasks associated with points
            self.updateLines() # Performs tasks associated with lines
            self.updateEquations() # Performs tasks associated with equations
            self.updateSliders() # Performs tasks associated with sliders
            self.updateButtons() # Performs tasks associated with buttons

def calculateGridPoints(x, y, z,stepX, stepY, stepZ, self, x2 = 0, y2 = 0, 
                        z2 = 0, step = 1):
        # Calculating points at the end of the grid lines and creates a line 
        # joining them
        
        i = -x
        while (i <= x):
            # XY plane parallels
            k = -z2
            while (k <= z2):
                if (k == 0):
                    text = str(i)
                else:
                    text = ''
               # print('|'+text)
                p1 = Point(self)
                p1.setCor(i,y,k)
                self.listOfAxisPoints.append(p1)
                p2 = Point(self)
                p2.setCor(i,-y,k)
                self.listOfAxisPoints.append(p2)
                l = Line(p1,p2,self, text)
                self.listOfGridLines.append(l)
                k += stepZ

            #XZ plane parallels
            j = -y2
            while (j <= y2):
                p1 = Point(self)
                p1.setCor(i,j,z)
                self.listOfAxisPoints.append(p1)
                p2 = Point(self)
                p2.setCor(i,j,-z)
                self.listOfAxisPoints.append(p2)
                l = Line(p1,p2,self,text)
                self.listOfGridLines.append(l)
                j += stepY
            i += stepX

        j = -y
        while (j <= y):
            
            # XY plane parallels
            k = -z2
            while (k <= z2):
                if (k == 0):
                    text = str(j)
                else:
                    text = ''
                p1 = Point(self)
                p1.setCor(x,j,k)
                self.listOfAxisPoints.append(p1)
                p2 = Point(self)
                p2.setCor(-x,j,k)
                self.listOfAxisPoints.append(p2)
                l = Line(p1,p2,self,text)
                self.listOfGridLines.append(l)
                k += stepZ
            
            #YZ plane parallels
            i = -x2
            while (i <= x2):
                p1 = Point(self)
                p1.setCor(i,j,z)
                self.listOfAxisPoints.append(p1)
                p2 = Point(self)
                p2.setCor(i,j,-z)
                self.listOfAxisPoints.append(p2)
                l = Line(p1,p2,self)
                self.listOfGridLines.append(l)
                i += stepX
            
            j += stepY

        k = -z
        while (k <= z):
            # XZ plane parallels
            i = -x2
            while (i <= x2):
                if (i == 0):
                    text = str(k)
                else:
                    text = ''
                p1 = Point(self)
                p1.setCor(i,y,k)
                self.listOfAxisPoints.append(p1)
                p2 = Point(self)
                p2.setCor(i,-y,k)
                self.listOfAxisPoints.append(p2)
                l = Line(p1,p2,self,text)
                self.listOfGridLines.append(l)
                i += stepX

            #YZ plane parallels
            j = -y2
            while (j <= y2):
                p1 = Point(self)
                p1.setCor(x,j,k)
                self.listOfAxisPoints.append(p1)
                p2 = Point(self)
                p2.setCor(-x,j,k)
                self.listOfAxisPoints.append(p2)
                l = Line(p1,p2,self)
                self.listOfGridLines.append(l)
                j += stepY
            k += stepZ


def createPoint(graph):
    valid = False
    # This calculates the coordinates of the point
    a = (pygame.mouse.get_pos()[0] - graph.origin.screenPos[0])/graph.XAxesSf 
    b = -(pygame.mouse.get_pos()[1] - graph.origin.screenPos[1])/graph.YAxesSf
    point = Point(graph) # Creates new point object
     # Determines which dimension the two coordinates correspond to and sets coordinates accordingly
    if (graph.yRotation == 0.0 and graph.xRotation == 0.0):
        point.setCor(a,b,0)
        valid = True
    elif (graph.yRotation in (90.0, -270.0) and graph.xRotation == 0.0):
        point.setCor(0,b,a)
        valid = True
    elif (graph.yRotation in (180.0, -180.0) and graph.xRotation == 0.0):
        point.setCor(-a,b,0)
        valid = True
    elif (graph.yRotation in (270.0, -90.0) and graph.xRotation == 0.0):
        point.setCor(-a,b,0)
        valid = True
    elif (graph.xRotation in (90.0, -270.0) and graph.yRotation == 0.0):
        point.setCor(a,0,-b)
        valid = True
    elif (graph.xRotation in (180.0, -180.0) and graph.yRotation == 0.0):
        point.setCor(a,-b,0)
        valid = True
    elif (graph.xRotation in (270.0, -90.0) and graph.yRotation == 0.0):
        point.setCor(a,0,b)
        valid = True
    point.calculateScreenPos()
    if (valid):
        graph.listOfPoints.append(point)
