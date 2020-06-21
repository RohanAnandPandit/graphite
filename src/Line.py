import pygame
from tkinter import *
# This class is used to represents individual lines created by the user
class Line:
    def __init__(self, point1, point2, parentWindow, text = ''):
        self.point1 = point1 # Point object
        self.point2 = point2 # Point object
        self.parentWindow = parentWindow
        self.colour = (0,0,0) # The colour of the line
        self.screen = self.parentWindow.screen
        self.text = text

    def deleteLine(self):
        self.parentWindow.listOfLines.remove(self)
        self.parentWindow.listOfSelectedLines.remove(self)

    # Draws the line on-screen by using the coordinates of the points
    def drawLine(self, showLabel = True):
        if (self in self.parentWindow.listOfSelectedLines):
            self.colour = (255,0,0)
        elif (self not in self.parentWindow.listOfGridLines):
            self.colour = (0,0,0)

        pygame.draw.aaline(self.screen, self.colour, self.point1.screenPos,
                           self.point2.screenPos)
        if (showLabel and self.text != ''):
            showText(self.screen, self.text,
                     int((self.point1.screenPos[0]+self.point2.screenPos[0])/2),
                     int((self.point1.screenPos[1]+self.point2.screenPos[1])/2),
                     (255, 0, 0), (255, 255, 255), 20)


    def mouseOverLine(self):
        # If the line is vertical
        if (self.point2.screenPos[0] - pygame.mouse.get_pos()[0] == 0
            or self.point2.screenPos[0] - self.point1.screenPos[0] == 0):
            if (abs(self.point2.screenPos[0] - pygame.mouse.get_pos()[0]) == 0
                and abs(self.point2.screenPos[0] - self.point1.screenPos[0]) == 0
                and min(self.point1.cor[1],self.point2.cor[1]) < pygame.mouse.get_pos()[1]
                and pygame.mouse.get_pos()[1] < max(self.point1.cor[1],self.point2.cor[1])):
                return True
            else:
                return False

        if (min(self.point1.screenPos[0],self.point2.screenPos[0]) < pygame.mouse.get_pos()[0]
            and pygame.mouse.get_pos()[0] < max(self.point1.screenPos[0],self.point2.screenPos[0])
            and min(self.point1.screenPos[1],self.point2.screenPos[1]) < pygame.mouse.get_pos()[1]
            and pygame.mouse.get_pos()[1] < max(self.point1.screenPos[1],self.point2.screenPos[1])):
            dy = (self.point2.screenPos[1] - self.point1.screenPos[1])
            dx = (self.point2.screenPos[0] - self.point1.screenPos[0])
            # Gradient of line joining two adjacent points on the curve
            gradient1 =  dy / dx
            dy = (self.point2.screenPos[1] - pygame.mouse.get_pos()[1])
            dx = (self.point2.screenPos[0] - pygame.mouse.get_pos()[0])
            # Gradient of line joining the point on the curve and the point
            # where the mouse has been clicked
            gradient2 = dy / dx
            if (abs(round(gradient1,1)) < 0.1):
                if (abs(round(gradient2,1)) < 0.1 and gradient1*gradient2 >= 0):
                    return True
            elif (abs(round(gradient1,1))*0.82 < abs(round(gradient2,1)) < abs(round(gradient1,1)*1.18)
                and gradient1*gradient2 >= 0):
                return True
            else:
                return False

    def visible(self): # Determines if the line will be visible to the user
        if (self.point1.screenPos[0] < 0 and self.point2.screenPos[0] < 0):
            return False
        # If the x-coordinates of both points are outside the width range of the screen
        elif (self.point1.screenPos[0] > self.parentWindow.width
              and self.point2.screenPos[0] > self.parentWindow.width):
            return False
        # If the y-coordinates of both points are outside the hight range of the screen
        elif ((self.point1.screenPos[1] < 0 and self.point2.screenPos[1] < 0)
              or (self.point1.screenPos[1] > self.parentWindow.height
                  and self.point2.screenPos[1] > self.parentWindow.height)):
            return False
        else:
            return True # In any other case
