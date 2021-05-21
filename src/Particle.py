from imports import *
from utils import *
from utils_1d import *
from Slider import Slider 
from math import *
# Creates a class for the particles that will be on the horizontal surface
class Particle:
    def __init__(self, velocity, mass, parentWindow, pos = 0): # Initialises the object
        self.parentWindow = parentWindow
        self.width = parentWindow.width
        self.radius = self.parentWindow.radius # Radius of the circles representing the particles
        self.velocity  = velocity # Its velocity
        self.mass = mass # Its mass
        self.pos = pos # Its index value
        # Its position along the line
        self.xCor = self.parentWindow.width*(pos+1)/(len(self.parentWindow.velocities)+2)
        self.prevXCor = self.xCor
        self.moveParticle = False
        self.particlePauseColour = self.parentWindow.particlePauseColour
        self.particlePlayColour = self.parentWindow.particlePlayColour
        self.particleCollisionColour = self.parentWindow.particleCollisionColour
        self.noOfParticles = self.parentWindow.noOfParticles
        self.listOfParticles = self.parentWindow.listOfParticles
        self.particleElasticity = self.parentWindow.particleElasticity
        self.wallElasticity = self.parentWindow.wallElasticity
        self.colour = self.particlePlayColour
        self.yCor = self.parentWindow.yCor
        self.waitTime = self.parentWindow.waitTime
        self.fontColour = self.parentWindow.font_colour
        self.fontSize = self.parentWindow.font_size
        self.fontBg = self.parentWindow.font_bg
        self.listOfSliders = [Slider('mass', 'mass', 500, 40,0, 50,
                                     self.parentWindow, self, 100, 50, '',10),
                              Slider('velocity', 'velocity', 500, 90,-25, 25,
                                     self.parentWindow, self, 100, 50, '',10)]
        self.windowOpen = False


    def mouseOverParticle(self):
        dx = (pygame.mouse.get_pos()[0]-self.xCor)
        dy = pygame.mouse.get_pos()[1]-(self.yCor-self.parentWindow.radius)
        distance = sqrt(dx**2 + dy**2)
        if (distance <= self.parentWindow.radius):
            return True
        return False

    def window(self): # Particlewindow
        self.root = Tk() # Creates window
        self.windowOpen = True

        # Opens window on top of all other windows
        self.root.attributes('-topmost', True)

        self.root.title('Properties') # Title of window
        # Position of window
        self.root.geometry("240x100+"+str(int(self.xCor))+'+'+str(int(self.yCor)+10))

        self.massLabel = Label(self.root, text = "mass =") # Textbox
        self.massLabel.place(relx = 0.1, rely = 0.4)

        self.velLabel = Label(self.root, text = "velocity =") # Textbox
        self.velLabel.place(relx = 0.1, rely = 0.1)

        self.velocityEnt = Entry(self.root) # Input for velocity
        self.velocityEnt.place(relx=0.4,rely=0.1)

        self.massEnt = Entry(self.root) # Input for mass
        self.massEnt.place(relx=0.4,rely=0.4)
        # Button to delete particle object
        self.delete = Button(self.root, text='Delete',
                             command = lambda: self.deleteParticle())
        self.delete.place(relx = 0.1, rely = 0.75)
        # Changes value of variables
        self.applyButton = Button(self.root, text='Apply',
                                  command=lambda:self.valueValidation())
        self.applyButton.place(relx=0.5,rely=0.75)

    def deleteParticle(self):
      self.parentWindow.listOfParticles.remove(self)
      self.root.destroy()

    def closeWindow(self):
      self.root.destroy()

    def valueValidation(self):
        try:
            velocity = round(float(self.velocityEnt.get()),2)
            mass = round(float(self.massEnt.get()),2)
            self.setValues(velocity, mass)
        except:
            pass

    def setValues(self,velocity,mass):
        self.velocity = velocity
        self.mass = mass

    def showText(self,text, centreX, centreY, fontColour, fontBg, fontSize):
        # initialises font for displaying text
        basicfont = pygame.font.SysFont('times.ttf', fontSize)
        text = basicfont.render(text, True, fontColour, fontBg) # Text for pause
        textrect = text.get_rect()
        textrect.center = (centreX,centreY) #
        self.screen.blit(text, textrect) # Shows text on self.screen

    def move(self):
        # Each particle moves to the right by 'speed' number of pixels for every loop
        self.xCor = self.xCor + self.velocity*self.parentWindow.speed

    def showInfo(self, showMass, showVelocity, showKE):
        if (showVelocity):
            self.showText(str(round(self.velocity, 2)) + ' m/s', self.xCor,
                          self.yCor - 2*self.parentWindow.radius - 10,
                          self.fontColour, self.fontBg, self.fontSize) # Text for velocity
        if (showMass):
            self.showText(str(self.mass)+' kg', self.xCor, self.yCor + 20,
                          self.fontColour, self.fontBg, self.fontSize) # Text for mass
        if (showKE):
            # Calculates kinetic energy
            KE = round(0.5 * self.mass * (self.velocity ** 2), 2)

            # Text for kinetic energy
            self.showText(str(KE)+' J', self.xCor, self.yCor + 40,
                          self.fontColour, self.fontBg, self.fontSize)

    def draw(self):
        # Draws the circle in the position of the particle.
        pygame.draw.circle(self.parentWindow.get_screen(), self.colour,
                           (int(self.xCor), self.yCor - self.parentWindow.radius),
                           self.parentWindow.radius, 0)

        if self == self.parentWindow.selectedParticle:
            pygame.draw.circle(self.parentWindow.get_screen(), (255, 0, 0),
                               (int(self.xCor),
                                self.yCor - self.parentWindow.radius),
                               self.parentWindow.radius, 2)
        else:
            pygame.draw.circle(self.parentWindow.get_screen(), (0, 0, 0),
                               (int(self.xCor),
                                self.yCor - self.parentWindow.radius),
                               self.parentWindow.radius, 2)
