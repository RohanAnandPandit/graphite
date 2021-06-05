from App import App
import os
import pygame
import ctypes
from utils import window_size, set_screen, APP_PATH
import pickle
pygame.init()


ctypes.windll.shcore.SetProcessDpiAwareness(1)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (2, 50)

width, height = window_size()

# Only one pygame root can be used by all the different tabs
set_screen((3000, 1600))
pygame.display.set_caption('Graphite')
try:
    file = open(APP_PATH, 'rb')
    app = pickle.load(file)
    app.reset_graph()
except (FileNotFoundError, EOFError):
    app = App(width, height)  # Application object

app.update_tabs()  # Starts the main program
