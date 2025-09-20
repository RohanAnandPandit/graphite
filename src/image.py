import pygame
from tkinter import Tk, Label, Entry, Button
from .utils import IMAGES_PATH


class Image:
    def __init__(self, x, y, xAngle, yAngle, zAngle, parentWindow):
        self.root = None
        self.parentWindow = parentWindow
        self.x = x  # Coordinates
        self.y = y
        self.xAngle = xAngle  # Angle at which photograph should appear
        self.yAngle = yAngle
        self.zAngle = zAngle
        self.image = None
        self.move = False
        self.windowOpen = False

    def mouseOverImage(self):
        if (self.x <= pygame.mouse.get_pos()[0] <= self.x + self.width
                and self.y <= pygame.mouse.get_pos()[
                    1] <= self.y + self.height):
            return True
        return False

    def show(self):  # Displays image on screen
        if self.image is not None:
            self.parentWindow.get_screen().blit(self.image, (self.x, self.y))

    def setImage(self, file):
        if self not in self.parentWindow.images:
            self.parentWindow.images.append(self)
        try:
            self.image = pygame.image.load(IMAGES_PATH + file + '.jpg')
            (self.width, self.height) = self.image.get_rect().size
            self.image = self.image.convert()
        except:
            pass

    def deleteImage(self):
        try:
            self.parentWindow.images.remove(self)
        except:
            pass
        self.root.destroy()

    def window(self):  # Image window
        self.root = Tk()
        self.windowOpen = True
        self.parentWindow.image_windows.append(self)

        cord = str(pygame.mouse.get_pos()[0] - 100) + '+' + str(
            pygame.mouse.get_pos()[1] + 10)
        self.root.geometry('260x60+' + cord)
        # Makes sure that the root opens on top of the Pygame root.
        self.root.attributes('-topmost', True)
        self.root.title('Image Properties')

        self.filelabel = Label(self.root, text='file name=')
        self.filelabel.place(relx=0.1, rely=0.1)

        self.fileent = Entry(self.root,
                             width=20)  # User input for file name of image
        self.fileent.place(relx=0.05, rely=0.4)

        self.apply = Button(self.root, text='Apply',
                            command=lambda: self.setImage(self.fileent.get()))
        self.apply.place(relx=0.6, rely=0.1)  # This button sets the image

        self.delete = Button(self.root, text='Delete',
                             command=lambda: self.deleteImage())
        self.delete.place(relx=0.8, rely=0.1)
