from random import randint
import pygame
from tkinter import *

fileLocation = "C:/GitHub_Projects/graph3d/images/"
colours = {'white' : (255, 255, 255), 'black' : (0, 0, 0), 'red' : (255, 0, 0),
           'blue' : (0, 0, 255), 'green' : (0, 255, 0)}

def invert(var):
    if (var):
        return False
    return True

def randomColour():
    return (randint(1, 254), randint(1, 254), randint(1, 254))

def windowSize():
    # The width and height of the screen can be found by using Tkinter
    test = Tk()
    width = test.winfo_screenwidth()
    height = test.winfo_screenheight() - 150 # Takes the toolbar into account
    test.destroy()
    return (width, height)

def showText(screen, text2, centreX, centreY, fontColour, fontBg, fontSize, gap=30):
    y = centreY
    for line in text2.split(','):
        # initialises font for displaying text
        basicfont = pygame.font.SysFont('unifont.ttf', fontSize) 
        text = basicfont.render(line, True, fontColour, fontBg)
        textrect = text.get_rect()
        textrect.center = (centreX,y) # 
        screen.blit(text, textrect) # Shows text on self.screen
        y = y +gap

def showText2(screen, text, centreX, centreY, fontColour, fontBg, fontSize):
    # initialises font for displaying text
    basicfont = pygame.font.SysFont('unifont.ttf', fontSize) 
    text = basicfont.render(text, True, fontColour, fontBg)
    textrect = text.get_rect()
    textrect.center = (centreX,centreY) # 
    screen.blit(text, textrect) # Shows text on self.screen
        
def showImage(screen, image, x, y):
    image = pygame.image.load(fileLocation + image + '.jpg').convert()
    screen.blit(image,(x,y))
    


