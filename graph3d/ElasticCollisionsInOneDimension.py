from utils import *
from Buttons import Buttons
from Image import Image
from Slider import Slider
from utils_1d import *
import pygame

class ElasticCollisionsInOneDimension:
    def __init__(self, width, height, screen, parentApp):
        self.parentApp = parentApp
        self.width = width # self.width of the self.screen
        self.height = height# self.height of the self.screen
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.velocities = [10, -5,  1, 0] # self.velocities of the particles
        self.masses =     [2 ,  4, 20, 6] # Masses of the corresponding particles
        self.radius = 30 # Radius of the circles representing the particles

        self.noOfParticles = len(self.velocities)

        self.particleElasticity = 1.0 # Elasticity between the particles
        self.wallElasticity = 1.0 # Elasticity between the particles and the wall.

        self.listOfParticles = [] # The particle objects will be stored in this  list

        self.yCor = int(self.height*0.75)

        self.waitTime = 0.0
        self.speed = 1

        self.fontSize = 25
        self.fontColour = (255,0,0)
        self.fontBg = (255,255,255)

        self.bgColour = (255,255,255)
        self.colour = (0,0,0)
        self.particlePauseColour = (200,200,200)
        self.particlePlayColour = (0,0,255)
        self.particleCollisionColour = (0,255,0)

        self.run = False # To determine if the user wants to pause the simulation
        self.pausePlayButton = Buttons('Pause/Play' ,'Play'  ,0  ,40  ,100, 100,
                                       None,  'rectangle', 30,  colours['black'],
                                       colours['black'],colours['white'],self,
                                       '\Play')

        self.selectedParticle = None # Particle which is being controlles using sliders

        self.addParticleButton = Buttons('Add Particle', 'Add,Particle', 0, 140,
                                         50, 50, None, 'rectangle', 30,
                                         colours['black'],colours['black'],
                                         colours['white'],self, '')
        self.resetButton = Buttons('Reset', 'Reset',0,190, 50, 50, None,
                                   'rectangle', 30,  colours['black'],
                                   colours['black'],colours['white'],self, '')
        self.settingsButton = Buttons('Settings', 'Settings',0,240, 50, 50,
                                      None, 'rectangle', 30,  colours['black'],
                                      colours['black'],colours['white'],self, '')

        self.listOfSliders = [Slider('radius', 'radius', 150, 40,10, 60, self,
                                     self, 100, 50, 'integers',30),
                              Slider('particle elasticity', 'particleElasticity',
                                     150, 90,0, 2, self, self, 100, 50, '',1),
                              Slider('wall elasticity', 'wallElasticity', 300,
                                     90,0, 2, self, self, 100, 50, '',1),
                              Slider('speed', 'speed', 300, 40,0, 5, self, self,
                                     100, 50, '',1)]
        self.reset = True
        self.showMass = False
        self.showVelocity = False
        self.showKE = False

        self.buttonselected = False

    def settingsWindow(self):
        self.root = Tk()
        self.root.title('Settings')
        self.root.geometry('220x100+'+str(int(self.width/2))+'+'+str(int(0)))
        self.root.attributes('-topmost',True)

        label = Label(self.root, text = "Label Settings")
        label.grid(row = 0, column = 0)
        a = BooleanVar()
        velocityButton = Checkbutton(self.root,background = 'white',
                                     text = "Show velocity",
                                     variable = a, onvalue = True,
                                     offvalue = False, command = lambda a = a,
                                     self = self: exec("self.showVelocity = a.get()"))
        velocityButton.grid(row = 1, column = 0)
        if (self.showVelocity):
            velocityButton.select()


        b = BooleanVar()
        massButton = Checkbutton(self.root,background = 'white',
                                 text = "Show mass", variable = b,
                                 onvalue = True, offvalue = False,
                                 command = lambda b = b,
                                 self = self: exec("self.showMass = b.get()"))
        massButton.grid(row = 2, column = 0)
        if (self.showMass):
            self.massButton.select()

        c = BooleanVar()
        KEButton = Checkbutton(self.root,background = 'white',
                               text = "Show kinetic energy", variable = c,
                               onvalue = True, offvalue = False,
                               command = lambda c = c,
                               self = self: exec("self.showKE = c.get()"))
        KEButton.grid(row = 3, column = 0)
        if (self.showKE):
            KEbutton.select()


    def showText(self,text, centreX, centreY, fontColour, fontBg, fontSize):
            basicfont = pygame.font.SysFont('times.ttf', fontSize) # initialises font for displaying text
            text = basicfont.render(text, True, fontColour, fontBg) # Text for pause
            textrect = text.get_rect()
            textrect.center = (centreX,centreY) #
            self.screen.blit(text, textrect) # Shows text on self.screen

    def updateSliders(self):
        for slider in self.listOfSliders+self.selectedParticle.listOfSliders:
            if (slider.movePointer):
                if (slider.x < pygame.mouse.get_pos()[0] < slider.x + slider.width):
                    slider.pointer.setCor(pygame.mouse.get_pos()[0], slider.pointer.y, slider.pointer.z)
                    slider.pointer.screenPos = (pygame.mouse.get_pos()[0], slider.pointer.y)
                    slider.setVariable()
            if (slider in self.selectedParticle.listOfSliders):
                self.selectedParticle.listOfSliders[0].setValue(self.selectedParticle.mass)
                self.selectedParticle.listOfSliders[1].setValue(self.selectedParticle.velocity)
            slider.drawSlider()

    def pauseSimulation(self):
        self.run = False # Stops simulation

        # Changes image to play symbol
        try:
            filePath = fileLocation + '\Play' + '.jpg'
            self.pausePlayButton.image = pygame.image.load(filePath).convert()
        except:
            self.pausePlayButton.text = 'Play'

    def playSimulation(self):
        self.run = True # Restarts simulation
        # Changes image to pause symbol
        try:
            filePath = fileLocation + '\Pause' + '.jpg'
            self.pausePlayButton.image = pygame.image.load(filePath).convert()
        except:
            self.pausePlayButton.text = 'Pause'

    def checkEvents(self):
        if (pygame.key.get_pressed()[pygame.K_o] != 0):
            self.pauseSimulation()

        elif (pygame.key.get_pressed()[pygame.K_p] != 0):
            self.playSimulation()

        for event in self.parentApp.events:
            # Checks if the user wants to close the window
            if (event.type == pygame.QUIT):
                self.deleteAllWindows()
                pygame.quit()
                sys.exit()

            if (event.type == pygame.MOUSEBUTTONDOWN):
                if (event.button == 1):
                    # Checks if the user has clicked on the button
                    if (self.pausePlayButton.mouseOverButton()):
                        if (self.run):
                            self.pauseSimulation()

                        else:
                            self.playSimulation()

                    elif (self.addParticleButton.mouseOverButton()):
                        # Adds a new particle to the list
                        particle = Particle(10, 10, self, len(self.listOfParticles))
                        self.listOfParticles.append(particle)
                        n =  len(self.listOfParticles) + 2
                        for i in range(0, len(self.listOfParticles)):
                            particle = self.listOfParticles[i]
                            # Resets position of particles
                            particle.xCor = self.width*(i+1)/n

                    elif (self.resetButton.mouseOverButton()):
                        self.reset = True

                    elif (self.settingsButton.mouseOverButton()):
                        self.settingsWindow()

                    # Checks if the user has clicked inside any of the particles
                    # which then gives control to the user to change it's position
                    for particle in self.listOfParticles:
                        if (particle.mouseOverParticle()):
                            if (not self.run):
                                particle.moveParticle = True
                            self.selectedParticle = particle

                    for slider in self.listOfSliders+self.selectedParticle.listOfSliders:
                        if (slider.pointer.mouseOverPoint()): # Slider control of user
                            slider.movePointer = True

                if (event.button == 3):
                    if (not self.run):
                        # Checks if the user has clicked inside any of the
                        # particles which then gives control to the user to
                        # change it's position
                        for particle in self.listOfParticles:
                            if (particle.mouseOverParticle()):
                                particle.window()

            if (event.type == pygame.MOUSEBUTTONUP):
                if (event.button == 1):
                    if (not self.run):
                        for i in range(1,len(self.listOfParticles)):
                            particle = self.listOfParticles[i]
                            particle2 = self.listOfParticles[i-1]
                             # If particles overlap
                            if (particle.xCor - particle2.xCor < 2*self.radius):
                                if (particle.moveParticle):
                                    # Overlapping particle moved to right
                                    particle.xCor = particle2.xCor + 2*self.radius
                                elif (particle2.moveParticle):
                                    # Overlapping particle moved to left
                                    particle2.xCor = particle.xCor - 2*self.radius

                        for particle in self.listOfParticles:
                            particle.moveParticle = False

                    for slider in self.listOfSliders+self.selectedParticle.listOfSliders:
                        slider.movePointer = False


    def updateParticles(self):
        for i in range(0, len(self.listOfParticles)):
            particle = self.listOfParticles[i]
            particle2 = self.listOfParticles[i-1]
            if (self.run):
                particle.move() # Moves the particles

                for j in range(0, len(self.listOfParticles)):
                    self.listOfParticles[j].colour = self.particlePlayColour

            # If a particle's position is being controlled by the user then the position xCor of the particle will be the xCor of the mouse
            if (particle.moveParticle):
                if (particle.radius<pygame.mouse.get_pos()[0]<self.width - particle.radius):
                    particle.xCor = pygame.mouse.get_pos()[0]

            if (i != 0):
                if (particle.xCor - particle2.xCor <= 0):
                    if (particle.moveParticle):
                        particle2.xCor += 2*self.radius+2

                    elif (particle2.moveParticle):
                        particle.xCor -= 2*self.radius+2

                    self.listOfParticles[i] = particle2
                    self.listOfParticles[i-1] = particle

            if (not self.run):
                # If the simulation has been paused then the colour of all the
                # particles will turn grey to reflect this
                particle.colour = self.particlePauseColour
            # Shows the velocities and masses of the particles.
            particle.showInfo(self.showMass, self.showVelocity, self.showKE)
            particle.draw() # Draws the circles on the self.screen
            particle.listOfParticles = self.listOfParticles
            particle.run = self.run
            if (self.run):
                for j in range(0, len(self.listOfParticles)):
                    self.listOfParticles[j].colour = self.particlePlayColour

    def deleteAllWindows(self):
        for particle in self.listOfParticles:
            try:
                particle.listOfSliders[0].root.destroy()
            except:
                pass
            try:
                particle.listOfSliders[1].root.destroy()
            except:
                pass
            try:
                particle.root.destroy()
            except:
                continue

    def generateDefaultParticles(self):
        self.deleteAllWindows()
        self.listOfParticles = []
        start = 0
        # Creates Particle objects using the self.velocities and the
        # self.masses from the lists and adds them to the list
        while (start < len(self.velocities)):
            particle = Particle(self.velocities[start], self.masses[start], self,start)
            self.listOfParticles.append(particle)
            start += 1
        self.selectedParticle = self.listOfParticles[0]

    def updateWindow(self):
        for i in range(0,5):
            for particle in self.listOfParticles:
                try:
                    particle.root.update_idletasks()
                    particle.root.update()
                    if (i == 4):
                        coord = (particle.root.winfo_x(), particle.root.winfo_y())
                        pygame.draw.aaline(self.screen, (255,0,0),
                                           (particle.xCor, self.yCor-self.radius),
                                           coord, 2)
                except:
                    continue
        try:
            self.root.update_idletasks()
            self.root.update()
        except:
            pass
        self.pausePlayButton.showButton()
        self.addParticleButton.showButton()
        self.resetButton.showButton()
        self.settingsButton.showButton()

        # Draws the surface on which the particles are moving
        pygame.draw.line(self.screen, (0,0,0), (0,self.yCor),
                         (self.width,self.yCor))
        #pygame.display.update() # Updates the self.screen
        # Stops the loop for some time so the speed at which the particles are
        # moving can be controlled
        time.sleep(0.0)


    def collisionDetection(self):
        for i in range(0, len(self.listOfParticles)):
            particle = self.listOfParticles[i]
            if (i == 0):
                # Checks if the particle has touched the left wall and is still moving towards the left
                if (particle.xCor - particle.radius <= 0 and particle.velocity < 0):
                    # Reverses the direction to right and multiplies by the elasticity
                    particle.velocity = particle.velocity * self.wallElasticity * -1

            elif (i == len(self.listOfParticles)-1):
                # Checks if the particle has touched the right wall and is
                # still moving towards the right
                if (particle.xCor + particle.radius >= self.width
                    and particle.velocity > 0):
                    # Reverses the direction to left and multiplies by the elasticity
                    particle.velocity *= self.wallElasticity * -1
                    particle.colour = particle.particleCollisionColour
            if (i != 0):
                # This is the particle on the left side of the current particle
                particle2 = self.listOfParticles[i-1]
                # Checks if the the two particles are in contact with each other
                # as then the distance betweem them will the sum of their self.radius
                if (particle.xCor - particle2.xCor <= 2*self.radius):
                    # The current particle is on the right so its speed will be the 1st element
                    solution = collisionCalculator(particle.velocity, 
                                                   particle2.velocity,
                                                   particle.mass, particle2.mass,
                                                   self.particleElasticity)
                    (particle.velocity,particle2.velocity) = (solution[1],solution[0])
                    particle.colour = self.particleCollisionColour
                    particle2.colour = self.particleCollisionColour

    def main(self):
        # Fills the self.screen with white to erase the current object
        self.screen.fill(self.bgColour)
        if (self.reset):
            self.generateDefaultParticles()
            self.reset = False
        self.checkEvents()
        self.updateSliders()
        self.updateParticles()
        if (self.run):
            self.collisionDetection()
        self.updateWindow()
