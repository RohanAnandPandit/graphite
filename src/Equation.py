from imports import *
from Slider import *
from Buttons import *
from utils import randomColour
from String_Formatting import syntaxCorrection
from maths.Mathematical_Functions import *
# This class is used to represent a graph inputted by the user
class Equation: #Used for plotting graphs
    def __init__(self, parentWindow, equationType):
        self.type = equationType # Parametric or Cartesian
        self.parentWindow = parentWindow
        self.windowOpen = True

        #These are local constants which may be used in the equation and can be controlled using sliders
        self.a = 1
        self.b = 1
        self.c = 1
        self.d = 1

        self.sliderWidth = 180

        #These three expressions represent the x,y and z coordinates in terms of a fourth variable 't'
        #These attributes will only be used if the equation is parametric type
        self.xEquation = str()
        self.yEquation = str()
        self.zEquation = str()

        # This attribute is a string which represents the equation using the
        # variables x, y and z (in the given domain)
        self.cartesianEquation = None

        #These start and end values are used for Cartesian equations to reduce
        # the amount of time the program takes to search for all the points.
        #This is useful for spheres for example where the points are only
        #located in the domain -radius <= x,y,z <= radius
        self.startX = '-1'
        self.endX = '1'
        self.startY = '-1'
        self.endY = '1'
        self.startZ = '-1'
        self.endZ = '1'

        #This is the domain of the parametric variable
        self.startValue = '-1'
        self.endValue = '1'

        # A listof Point objects with cordinates that satisfy the equation
        self.listOfPoints = []


        self.limit1 = 0
        self.limit1Point1 = Point(self.parentWindow)
        self.limit1Point2 = Point(self.parentWindow)
        self.limit2 = 0
        self.limit2Point1 = Point(self.parentWindow)
        self.limit2Point2= Point(self.parentWindow)

        # A list of Slider objects that will be displayed and active when the graph of the equation is selected
        self.listOfSliders = [Slider('a','a', 0, self.parentWindow.height-60,
                                     -10, 10, self.parentWindow, self, 180,60, '',1),
                              Slider('b','b', 180,self.parentWindow.height-60,
                                     -10, 10, self.parentWindow, self, 180,60, '',1),
                              Slider('c','c', 360,self.parentWindow.height-60,
                                     -10, 10, self.parentWindow, self, 180,60, '',1),
                              Slider('d','d', 540,self.parentWindow.height-60,
                                     -10, 10, self.parentWindow, self, 180,60, '',1),
                              Slider('e','e', 720,self.parentWindow.height-60,
                                     -10, 10, self.parentWindow, self, 180, 60, '',1),
                              Slider('limit1','limit1', 0,self.parentWindow.height-110 ,
                                     -10, 10, self.parentWindow, self, 180,50,'',0),
                              Slider('limit2','limit2', 200,self.parentWindow.height-110,
                                     -10, 10, self.parentWindow, self, 180, 50, '',0)]

        self.parentWindow = parentWindow
        self.showSliders = False
        self.isSelected = True
        # Colour of the lines used to draw the curve or the points satisfying
        # the equation
        self.colour = randomColour()
        self.thickness = 1

        #Tkinter window
        self.root = None

        # The amount by which the parametric variable or x,y and z will be
        # incremented to calculate or check valid points
        # Lower the increment, greater the detail but longer the time it takes
        # to calculate the points and vice versa
        self.accuracy = '0.1'

        #Temporary variable to get the general shape of the graph in a short time
        self.error = 5
        self.listOfSides = []

    def drawGraph(self):
        if (self.type == 'parametric'):
            add = 1 # To skip points
            i = add
            # Remember that the screenPos of a point is a tuple containing the
            # display coordinates of the point
            while (i < len(self.listOfPoints2)-add):
                if (self.listOfPoints2[i] != '' and self.listOfPoints2[i-add] != ''):
                    if (self.listOfPoints2[i].visible() or self.listOfPoints2[i-add].visible()):
                        plot = True
                    elif (self.listOfPoints2[i].screenPos[0] < 0
                          and self.listOfPoints2[i-add].screenPos[0] < 0
                          or self.listOfPoints2[i].screenPos[0] > self.parentWindow.width
                          and self.listOfPoints2[i-add].screenPos[0] > self.parentWindow.width):
                        plot = False
                    elif (self.listOfPoints2[i].screenPos[1] < 0
                          and self.listOfPoints2[i-add].screenPos[1] < 0
                          or self.listOfPoints2[i].screenPos[1] > self.parentWindow.height
                          and self.listOfPoints2[i-add].screenPos[1] > self.parentWindow.height):
                        plot = False
                    else:
                        plot = True
                    if (plot):
                        self.listOfPoints2[i].show()
                        # Drawing a line between adjacent points
                        if (self.thickness == 1):
                            # A smoother line drawing function which only allows one thickness
                            pygame.draw.aaline(self.parentWindow.screen,
                                               self.colour,
                                               self.listOfPoints2[i-add].screenPos,
                                               self.listOfPoints2[i].screenPos)
                        elif (self.thickness == 2):
                            # Not as smooth but allows different thicknesses
                            pygame.draw.line(self.parentWindow.screen,
                                             self.colour,
                                             self.listOfPoints2[i-add].screenPos,
                                             self.listOfPoints2[i].screenPos,
                                             self.thickness)

                i = i + add

      # Cartesian equation will be represented only as individual points because
      # it is very difficult to represent curved surfaces
        elif (self.type == 'cartesian'):
              for point in self.listOfPoints2:
                  point.calculateScreenPos()
                  point.show() # Draws point

    # This is used to check if the user is hovering the mouse over any point on
    # the graph of the equation
    def mouseOverGraph(self):
        # Checks if the user has clicked on any of the points in the graph for the equation
        for point in self.listOfPoints:
            if (point == '' or point.screenPos == None):
                continue
            if (point.mouseOverPoint()):
                return True
        if (self.type == 'cartesian'): # If the user hasn't clicked on any of the
            return False
         # Similar to the Line class, checks if the user has clicked on any
         # line between adjacent points
        elif (self.type == 'parametric'):
            i = 1
            while (i < len(self.listOfPoints)-1):# Iterates through all the points
                if (self.listOfPoints[i] != ''
                    and self.listOfPoints[i-1] != ''): # To ensure it is not an undefined point
                    point1 = self.listOfPoints[i]
                    point2 = self.listOfPoints[i-1]
                    try:
                        if (point2.screenPos[0] - pygame.mouse.get_pos()[0] == 0
                            # When one of the lines is vertical (to avoid zero divison error)
                            or point2.screenPos[0] - point1.screenPos[0] == 0):
                            if (point2.screenPos[0] - pygame.mouse.get_pos()[0] == 0
                                and point2.screenPos[0] - point1.screenPos[0] == 0
                                and min(point1.cor[1],self.point2.cor[1]) < pygame.mouse.get_pos()[1]
                                and pygame.mouse.get_pos()[1] < max(point1.cor[1],point2.cor[1])):
                                return True
                            else:
                                return False
                        # First checls if the mouse is in the rectangle whcih has the line as a diagonal
                        if (min(point1.screenPos[0],point2.screenPos[0]) < pygame.mouse.get_pos()[0]
                            and pygame.mouse.get_pos()[0] < max(point1.screenPos[0],point2.screenPos[0])
                            and min(point1.screenPos[1],point2.screenPos[1]) < pygame.mouse.get_pos()[1] < max(point1.screenPos[1],point2.screenPos[1])):
                            # Gradient of line joining two adjacent points on the curve
                            dy = (point1.screenPos[1] - point2.screenPos[1])
                            dx = (point1.screenPos[0] - point2.screenPos[0])
                            gradient1 = dy / dx
                            # Gradient of line joining the point on the curve and the point where the mouse has been clicked
                            dy = point1.screenPos[1] - pygame.mouse.get_pos()[1]
                            dx = point1.screenPos[0] - pygame.mouse.get_pos()[0]
                            gradient2 = dy / dx
                            if (gradient1 == 0):
                                if (abs(round(gradient2,2)) <= 0.1): # For small gradients
                                    return True
                            elif (abs(round(gradient1,2))*0.9 <= abs(round(gradient2,2)) <= abs(round(gradient1,2))*1.1
                                  and gradient1*gradient2 >= 0): # Compares gradients
                                return True
                            else:
                                return False
                    except:
                        pass
                i += 1





    # These are the windows that will be created when the user wants to add a
    # new parametric or Cartesian equation or edit them.
    # When these windows are open the rest of the program will stop functioning
    # (unless the required methods are specifically called).
    def window(self, x = None, y = None): # Equationwindow
        self.root = Tk()
        self.windowOpen = True
        self.root.title('Equation Properties')
        self.root.after(1, lambda: self.root.focus_force())
        # Makes sure that the window opens on top of the Pygame window.
        self.root.attributes('-topmost', True)
        if (x == None):
            (x,y) = (pygame.mouse.get_pos()[0] + 10, pygame.mouse.get_pos()[1] + 10)
            
        #self.root.geometry('300x200+'+str(x)+'+'+str(y))

        Label(self.root, text = 'step =', font = 'Caibri 10').grid(column = 1, row = 4)

        self.accuracyent = Entry(self.root, width = 5, font = 'Calibri 10')
        self.accuracyent.grid(column = 0, row = 4)


        if (self.type == 'parametric'):
            self.parentWindow.listOfWindowParametricEquations.append(self)
            Label(self.root, text = 'x =', font = 'Calibri 15').grid(column = 0, row = 0)
            Label(self.root, text = 'y =', font = 'Calibri 15').grid(column = 0, row = 1)
            Label(self.root, text = 'z =', font = 'Calibri 15').grid(column = 0, row = 2)


            self.xEquationent = Entry(self.root, font = 'Calibri 15')
            self.xEquationent.grid(column = 1, row = 0)

            self.yEquationent = Entry(self.root, font = 'Calibri 15')
            self.yEquationent.grid(column = 1, row = 1)

            self.zEquationent = Entry(self.root, font = 'Calibri 15')
            self.zEquationent.grid(column = 1, row = 2)

            apply = Button(self.root, text='Apply',
                               command = lambda: self.setInfoParametric(self.xEquationent.get(),
                                                                        self.yEquationent.get(),
                                                                        self.zEquationent.get(),
                                                                        self.startValueent.get(),
                                                                        self.endValueent.get(),
                                                                        self.accuracyent.get()))
            apply.grid(column = 5, row = 5)

            delete = Button(self.root, text='Delete', command = lambda: self.deleteEquation())
            delete.grid(column = 1, row = 5)


            close = Button(self.root, text='Close', command = lambda: self.closeWindow())
            close.grid(column = 2, row = 5)

            self.startValueent = Entry(self.root, width = 7, font = 'Calibri 10')
            self.startValueent.grid(column = 2, row = 3)

            self.endValueent = Entry(self.root, width = 7, font = 'Calibri 10')
            self.endValueent.place(relx = 0.7, rely = 0.65)

            self.trangelabel = Label(self.root, text='≤ t ≤', font = 'Calibri 10')
            self.trangelabel.place(relx = 0.6, rely = 0.65)

            # Inserts the current values of the variables if they exist
            if (self.xEquation != None):
                self.xEquationent.insert(0,self.xEquation)
                self.yEquationent.insert(0,self.yEquation)
                self.zEquationent.insert(0,self.zEquation)
            self.startValueent.insert(0,self.startValue)
            self.endValueent.insert(0,self.endValue)
            self.accuracyent.insert(0,self.accuracy)


        elif (self.type == 'cartesian'):
            self.parentWindow.listOfWindowCartesianEquations.append(self)
            Label(self.root, text='Equation:').grid(column = 0, row = 0)

            self.cartesianEquationent = Entry(self.root, font = 'Calibri 15')
            self.cartesianEquationent.grid(column = 0, row = 1)

            self.startXent = Entry(self.root, width = 7, font = 'Calibri 12')
            self.startXent.place(relx = 0.2, rely = 0.25)

            self.xrangelabel = Label(self.root, text='≤ x ≤', font = 'Calibri 12')
            self.xrangelabel.place(relx = 0.4, rely = 0.25)

            self.endXent = Entry(self.root, width = 7, font = 'Calibri 12')
            self.endXent.place(relx = 0.6, rely = 0.25)

            self.startYent = Entry(self.root, width = 7, font = 'Calibri 12')
            self.startYent.place(relx = 0.2, rely = 0.35)

            Label(self.root, text='≤ y ≤', font = 'Calibri 12').grid(column = 1, row = 3)

            self.endYent = Entry(self.root, width = 7, font = 'Calibri 12')
            self.endYent.place(relx = 0.6, rely = 0.35)

            self.startZent = Entry(self.root, width = 7, font = 'Calibri 12')
            self.startZent.place(relx = 0.2, rely = 0.45)

            Label(self.root, text='≤ z ≤', font = 'Calibri 12').grid(column = 1, row = 4)

            self.endZent = Entry(self.root, width = 7, font = 'Calibri 12')
            self.endZent.place(relx = 0.6, rely = 0.45)

            self.apply = Button(self.root, text='Apply',
                               command = lambda: self.setInfoCartesian(self.cartesianEquationent.get(),
                                                                       self.startXent.get(),
                                                                       self.endXent.get(),
                                                                       self.startYent.get(),
                                                                       self.endYent.get(),
                                                                       self.startZent.get(),
                                                                       self.endZent.get(),
                                                                       self.accuracyent.get(),
                                                                       self.errorent.get()))
            self.apply.place(relx = 0.8, rely = 0.8)

            self.delete = Button(self.root, text='Delete',
                                 command = lambda: self.deleteEquation())
            self.delete.place(relx = 0.1, rely = 0.8)


            self.close = Button(self.root, text='Close',
                                command = lambda: self.closeWindow())
            self.close.place(relx = 0.5, rely = 0.8)

            self.convertButton = Button(self.root, text = 'Convert',
                                        command = lambda: self.convert())
            self.convertButton.place(relx = 0.8, rely = 0.7)

            self.errorlabel = Label(self.root, text='error=')
            self.errorlabel.place(relx = 0.1, rely = 0.55)

            self.errorent = Entry(self.root, width =5)
            self.errorent.place(relx = 0.3, rely = 0.55)

            if (self.cartesianEquation != None):
                self.cartesianEquationent.insert(0,self.cartesianEquation)
            # Inserts the current values of the variables (which will be default
            # if the Equation object has been created for the first time)
            self.startXent.insert(0,self.startX)
            self.endXent.insert(0,self.endX)
            self.startYent.insert(0,self.startY)
            self.endYent.insert(0,self.endY)
            self.startZent.insert(0,self.startZ)
            self.endZent.insert(0,self.endZ)
            self.accuracyent.insert(0,self.accuracy)
            self.errorent.insert(0,self.error)


    def convert(self):
        self.parentWindow.listOfEquations.remove(self)# Removes any record of the equation
        for point in self.listOfPoints: # Iterates throiugh list of points
            point.equation = None # Sets equation to None
            self.parentWindow.listOfPoints.append(point) # Adds point to listOfPoints
            if (self in self.parentWindow.listOfSelectedEquations): # If the equation was selected,
                self.parentWindow.listOfSelectedPoints.append(point)# so will the points
        if (self in self.parentWindow.listOfSelectedEquations):
            self.parentWindow.listOfSelectedEquations.remove(self)# Removes any record of the equation
        self.root.destroy() # Closes window

    # Closes the tkinter window after which the rest of the program will continue to run
    def closeWindow(self):
        self.root.destroy()
        self.windowOpen = False


    def sliderSettings(self):
        if (not self.showSliders):
            for equation in self.parentWindow.listOfEquations:
                equation.showSliders = False
            self.showSliders = True

    # Removes the Equation object from the Graph object's listOfEquations and
    # all the Point objects from the listOfPoints
    def deleteEquation(self):
        if (self in self.parentWindow.listOfEquations):
            self.parentWindow.listOfEquations.remove(self)
        if (self in self.parentWindow.listOfSelectedEquations):
            self.parentWindow.listOfSelectedEquations.remove(self)
        self.closeWindow()


    def calculatePoints(self):
        # Attributes aliased as local variables so that the eval() function
        # will use these values
        a = self.a
        b = self.b
        c = self.c
        d = self.d
        # Ensures that all the required variables have been converted to the
        # right data type
        startValue = eval(syntaxCorrection(self.startValue))
        endValue = eval(syntaxCorrection(self.endValue))
        xEquation = syntaxCorrection(self.xEquation)
        yEquation = syntaxCorrection(self.yEquation)
        zEquation = syntaxCorrection(self.zEquation)
        accuracy = eval(self.accuracy)

        #Removes all the older points before the new points are calculated
        for point in self.listOfPoints:
            if (point in self.parentWindow.listOfPoints):
                self.parentWindow.listOfPoints.remove(point)

        self.listOfPoints = [] # Initialises new list
        self.listOfPoints2 = [] # Initialises new list
        try:
            t = self.listOfSliders[len(self.listOfSliders)-2].variable
            self.limit1Point2.setCor(t,eval(syntaxCorrection(self.yEquation)),0)
            t = self.listOfSliders[len(self.listOfSliders)-1].variable
            self.limit2Point2.setCor(t,eval(syntaxCorrection(self.yEquation)),0)
        except:
            pass

        # Loops through all the values of 't' in the given range and increment
        if (self.type == 'parametric'):
            t = startValue
            tracker = 0
            while (t <= endValue):
                try:
                   #Each coordinate is evaluated based on the value of t and
                   # the alphabetical constants
                    x = eval(xEquation)
                    y = eval(yEquation)
                    z = eval(zEquation)
                    #Creates Point object, sets the coordinates and adds it to
                    # the listOfPoints so that they are transformed with the
                    # rest of the points
                    # Python automaticallty calculates coimplex solutions of an
                    # equation which cannot be plotted
                    if ((type(x),type(y),type(z)) != (complex,complex,complex)):
                        p = Point(self.parentWindow)
                        p.equation = self
                        p.setCor(x, y, z)
                        self.listOfPoints2.append(p)
                    else:
                        if (self.listOfPoints == []):
                            # Represents an undefined point so that there is a
                            # gap in the graph at this point
                            self.listOfPoints2.append('')
                        elif (self.listOfPoints[len(self.listOfPoints)-1] != '' ):
                            # Represents an undefined point so that there is a
                            # gap in the graph at this point
                            self.listOfPoints2.append('')
                except:
                  # If there is an error while evaluating the expression, such
                  # as ZeroDivision or TypeError
                  if (self.listOfPoints == []):
                      # Represents an undefined point so that there is a gap in
                      # the graph at this point
                      self.listOfPoints2.append('')
                  elif (self.listOfPoints2[len(self.listOfPoints)-1] != ''):
                    self.listOfPoints.append('')
                t = round(t + accuracy,3) # Increments the variable by the
                # To ensure that the last point given in the range is also included
                if (t > endValue and tracker == 0):
                  t = endValue
                  tracker = 1 # To prevent the code being stuck in an infinite loop

        elif (self.type == 'cartesian'):
            if (True):
              # All the attributes are evaluated and changed to local variables
              # of the same name
                startX = eval(syntaxCorrection(self.startX))
                endX = eval(syntaxCorrection(self.endX))
                startY = eval(syntaxCorrection(self.startY))
                endY = eval(syntaxCorrection(self.endY))
                startZ = eval(syntaxCorrection(self.startZ))
                endZ = eval(syntaxCorrection(self.endZ))
                accuracy = eval(self.accuracy)
                trackerX = 0
                trackerY = 0
                trackerZ = 0

                # This loop is equivalent iterating through a three-dimensional array
                x = startX
                while (x <= endX):
                    y = startY # Resets y
                    while (y <= endY):
                        z = startZ # Resets z
                        while (z <= endZ):
                            try:
                                equation = list(syntaxCorrection(self.cartesianEquation))
                                l = len(equation)
                                i = 0
                                while (i < l):
                                    if (equation[i] == '='):
                                        equation.insert(i, '=')
                                        l = l + 1
                                        i = i + 2
                                    else:
                                        i = i + 1

                                if (eval(''.join(equation))):
                                    p = Point(self.parentWindow)
                                    p.equation = self
                                    p.setCor(x, y, z)
                                    self.listOfPoints2.append(p)
                                else:
                                    lhs = eval(self.listOfSides[0])
                                    i = 1
                                    # Iterates through all the indivudual
                                    # expressions that must be equal ot each other
                                    while (i < len(self.listOfSides)):
                                        rhs = eval(self.listOfSides[i])
                                        # This condition is there because the
                                        # second condition doesn't work if one
                                        # of the values is zero
                                        if (round(lhs,3) == round(rhs,3)):
                                            if (i == len(self.listOfSides)-1):
                                                # Creates Point object with satisfying coordinates
                                                p = Point(self.parentWindow)
                                                p.equation = self
                                                p.setCor(x, y, z)
                                                self.listOfPoints2.append(p)
                                        # Allows a margin of error as
                                        # expressions may not be exactly equal
                                        elif (lhs*rhs >= 0
                                              and  1-(self.error/100) <= abs(lhs/rhs) <= 1+(self.error/100)):
                                            # If loop has reached the last
                                            # expressions then the Point object is created
                                            if (i == len(self.listOfSides)-1):
                                                p = Point(self.parentWindow)
                                                p.equation = self
                                                p.setCor(x, y, z)
                                                self.listOfPoints2.append(p)
                                        else:
                                            break
                                        i = i + 1
                            except:
                                pass

                            z = z + accuracy # Increments z coordinate
                            if (z > endZ and trackerZ == 0): # To ensure that the last
                              z = endZ
                              trackerZ = 1
                        y = y + accuracy
                        if (y > endY and trackerY == 0):
                          y = endY
                          trackerY = 1
                    x = x + accuracy
                    if (x > endX and trackerX == 0):
                      x = endX
                      trackerX = 1
                self.parentWindow.screen.fill((255,255,255))
        for point in self.listOfPoints2:
            if (point != ''):
                self.listOfPoints.append(point)

    # ZeroDivisionError or TypeError or NameError

    def setInfoParametric(self, xEquation, yEquation, zEquation, startValue,
                          endValue, accuracy = '0.05'):
        a = self.a
        b = self.b
        c = self.c
        d = self.d
        e = self.e
        # Assigns values to the correct variable
        self.xEquation = xEquation
        self.yEquation = yEquation
        self.zEquation = zEquation
        self.startValue = startValue
        self.endValue = endValue
        self.accuracy = accuracy

        self.calculatePoints() # Calculates the points using the above information

        self.sliderSettings()
        # Adds Equation object to list of equation of Graph class
        if (self not in self.parentWindow.listOfEquations):
            self.parentWindow.listOfEquations.append(self)
        try:
            t = self.limit1
            self.limit1Point1.setCor(self.limit1,0,0)
            self.limit1Point2.setCor(self.limit1,
                                     eval(syntaxCorrection(self.yEquation)),0)
            t = self.limit2
            self.limit2Point1.setCor(self.limit2, 0, 0)
            self.limit2Point2.setCor(self.limit2,
                                     eval(syntaxCorrection(self.yEquation)),0)
        except:
            pass

        self.parentWindow.main() # Runs the main method to quickly plot graph

    def setInfoCartesian(self, cartesianEquation, startX, endX, startY, endY,
                         startZ, endZ, accuracy, error):
        # Attributes to local variables with same name
        a = self.a
        b = self.b
        c = self.c
        d = self.d
        self.cartesianEquation = cartesianEquation # Expression to calculate points
        cartesianEquation = syntaxCorrection(cartesianEquation) # Equation in Python syntax

        # Assigns attributes to the values given by user
        self.startX = startX
        self.endX = endX
        self.startY = startY
        self.endY = endY
        self.startZ = startZ
        self.endZ = endZ
        self.accuracy = accuracy
        self.error = eval(error)

        self.listOfSides = cartesianEquation.split("=") # Lists of individual expressions

        self.parentWindow.showFact() # Shows an interesting fact while calculating points
        self.calculatePoints() # Calculates points
        self.sliderSettings()
        if (self not in self.parentWindow.listOfEquations): # Adds Equation object to list of equations
            self.parentWindow.listOfEquations.append(self)

        self.parentWindow.main() # Runs the main method to quickly plot graph
