import pygame
from utils import randomColour
from tkinter import *

class Particle2D:
    def __init__(self, x,y, mass, velocity, parentWindow):
        self.parentWindow = parentWindow
        self.width = parentWindow.width
        # Radius of the circles representing the particles
        self.radius = self.parentWindow.radius
        self.velocity  = velocity # Its velocity
        self.mass = mass # Its mass
        self.moveParticle = False
        self.particlePauseColour = self.parentWindow.particlePauseColour
        self.particlePlayColour = randomColour()
        self.particleCollisionColour = self.parentWindow.particleCollisionColour
        self.noOfParticles = self.parentWindow.noOfParticles
        self.listOfParticles = self.parentWindow.listOfParticles
        self.particleElasticity = self.parentWindow.particleElasticity
        self.wallElasticity = self.parentWindow.wallElasticity
        self.colour = self.particlePlayColour
        self.waitTime = self.parentWindow.waitTime
        self.fontColour = self.parentWindow.fontColour
        self.fontSize = self.parentWindow.fontSize
        self.fontBg = self.parentWindow.fontBg
        self.screen = parentWindow.screen
        self.x = x
        self.y = y
        self.screen = self.parentWindow.screen
        self.listOfSliders = [Slider('mass', 'mass', 500, 40,0, 50,
                                     self.parentWindow, self, 100, 50, '',10)]
        self.windowOpen = False


    def showInfo(self, showMass, showVelocity, showKE):
        if (showVelocity):
            # Text for velocity
            showText2(self.screen, str(self.velocity)+' m/s', self.x,
                      self.y - self.radius-20, self.fontColour, self.fontBg,
                      self.fontSize)
        if (showMass):
            # Text for mass
            showText2(self.screen,str(self.mass)+' kg', self.x,
                      self.y+self.parentWindow.radius+10, self.fontColour,
                      self.fontBg, self.fontSize)
        if (showKE):
            KE = round(0.5 *self.mass*(self.getSpeed()**2),2) # Calculates KE
            # Text for kinetic energy
            showText(self.screen,str(KE)+' J', self.x,
                     self.y + self.parentWindow.radius+30, self.fontColour,
                     self.fontBg, self.fontSize)

    def deleteParticle(self):
      self.parentWindow.listOfParticles.remove(self)
      self.root.destroy()

    def closeWindow(self):
      self.root.destroy()

    def valueValidation(self):
        #try:
        velocity = [round(float(self.velocityEnt.get().split(',')[0]),2),
                    round(float(self.velocityEnt.get().split(',')[1]),2)]
        mass = round(float(self.massEnt.get()),2)
        self.setValues(velocity, mass)
        #except:
            #pass

    def setValues(self,velocity,mass):
        self.velocity = velocity
        self.mass = mass

    def mouseOverParticle(self):
        dx = (pygame.mouse.get_pos()[0]-self.x)
        dy = (pygame.mouse.get_pos()[1]-self.y)
        if (sqrt(dx**2+dy**2) <= self.parentWindow.radius):
            return True
        return False

    def window(self): # Particlewindow
        self.root = Tk() # Creates window
        self.windowOpen = True
        # Opens window on top of all other windows
        self.root.attributes('-topmost', True)

        self.root.title('Properties') # Title of window
        # Position of window
        self.root.geometry("240x100+"+str(int(self.x))+'+'+str(int(self.y)+10))

        self.massLabel = Label(self.root, text = "mass =") # Textbox
        self.massLabel.place(relx = 0.1, rely = 0.4)

        self.velLabel = Label(self.root, text = "velocity =") # Textbox
        self.velLabel.place(relx = 0.1, rely = 0.1)

        self.velocityEnt = Entry(self.root) # Input for velocity
        self.velocityEnt.place(relx=0.4,rely=0.1)

        self.massEnt = Entry(self.root) # Input for mass
        self.massEnt.place(relx=0.4,rely=0.4)

        self.delete = Button(self.root, text='Delete',
                             command = lambda: self.deleteParticle()) # Button to delete particle object
        self.delete.place(relx = 0.1, rely = 0.75)

        self.applyButton = Button(self.root,text='Apply',
                                  command=lambda:self.valueValidation()) # Changes value of variables
        self.applyButton.place(relx=0.5,rely=0.75)


    def move(self):
        self.x += self.velocity[0]*self.parentWindow.speed
        self.y -= self.velocity[1]*self.parentWindow.speed

    def draw(self):
        pygame.draw.circle(self.screen, self.colour,
                           (int(self.x), int(self.y)),self.parentWindow.radius, 0)
        pygame.draw.circle(self.screen, (0,0,0),
                           (int(self.x),int(self.y)),self.parentWindow.radius, 1)
        # Drawss lines to represent the components of the particle's velocity
        pygame.draw.aaline(self.screen, (255-self.colour[0], 255-self.colour[1], 255-self.colour[2]),
                           (int(self.x),int(self.y)), (int(self.x+10*self.velocity[0]),self.y ), 1)

        pygame.draw.aaline(self.screen, (255-self.colour[0],255-self.colour[1],255-self.colour[2]),
                           (int(self.x),int(self.y)), (int(self.x),int(self.y-10*self.velocity[1])), 1)

        self.showInfo(self.parentWindow.showMass, self.parentWindow.showVelocity,
                      self.parentWindow.showKE)

    def getSpeed(self):
        return mag(self.velocity)
