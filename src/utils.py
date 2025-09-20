from random import randint
import pygame
from tkinter import Tk

NAME = 'Graphite'
DIR_PATH = './'
IMAGES = 'images'
IMAGES_PATH = DIR_PATH + IMAGES + '/'
APP_NAME = 'graph_app'
APP_PATH = DIR_PATH + APP_NAME
FONT_NAME = 'Vogue.ttf'
FONT_PATH = f'{DIR_PATH}/fonts/{FONT_NAME}'

colours = {'white': (255, 255, 255), 'black': (0, 0, 0), 'red': (255, 0, 0),
           'blue': (0, 0, 255), 'green': (0, 255, 0)}

screen = None


def set_screen(dimensions):
    global screen
    screen = pygame.display.set_mode(dimensions, pygame.RESIZABLE)


def invert(var):
    return not var


def random_colour():
    return randint(1, 254), randint(1, 254), randint(1, 254)


def window_size():
    # The width and height of the screen can be found by using Tkinter
    test = Tk()
    width = test.winfo_screenwidth()
    height = test.winfo_screenheight() - 150  # Takes the toolbar into account
    test.destroy()
    return width, height


def show_multiline_text(screen, text2, centreX, centreY, fontColour, fontBg,
                        fontSize, gap=30):
    y = centreY
    for line in text2.split(','):
        # initialises font for displaying text
        try:
            basicfont = pygame.font.Font(FONT_PATH, fontSize)
            text = basicfont.render(line, True, fontColour, fontBg)
            textrect = text.get_rect()
            textrect.center = (centreX, y)  #
            screen.blit(text, textrect)  # Shows text on self.screen
            y = y + gap
        except:
            pass


def show_text(screen, text, centreX, centreY, fontColour, fontBg, fontSize):
    # initialises font for displaying text
    try:
        basicfont = pygame.font.Font('Vogue.ttf', fontSize)
        text = basicfont.render(text, True, fontColour, fontBg)
        textrect = text.get_rect()
        textrect.center = (centreX, centreY)  #
        screen.blit(text, textrect)  # Shows text on self.screen
    except:
        pass


def show_image(screen, image, x, y):
    image = pygame.image.load(IMAGES_PATH + image + '.jpg').convert()
    screen.blit(image, (x, y))
