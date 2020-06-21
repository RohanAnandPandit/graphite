from tkinter import *
from App import App
import os
import pygame
pygame.init()
import ctypes
from utils import windowSize

ctypes.windll.shcore.SetProcessDpiAwareness(1)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (2, 50)
 
(width, height) = windowSize()

# Only one pygame window can be used by all the different tabs
screen = pygame.display.set_mode((width, height))
app = App(screen, width, height) # Application object
app.updateTabs() # Starts the main program