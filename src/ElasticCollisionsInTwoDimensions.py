from utils import *
from Buttons import *
from Slider import *
from Particle2D import *
from utils_2d import *
import pygame

class ElasticCollisionsInTwoDimensions:
    def __init__(self, width, height, screen, parentApp):
        self.parentApp = parentApp
        self.width = width # self.width of the self.screen
        self.height = height# self.height of the self.screen
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.velocities = [[1,1], [-1, -1]] # Velocities in vector form
        self.masses = [5,5,5]
        self.radius = 30 # Radius of the circles representing the particles

        self.noOfParticles = len(self.velocities)

        self.particleElasticity = 1.0 # Elasticity between the particles
        self.wallElasticity = 1.0 # Elasticity between the particles and the wall.

        self.listOfParticles = [] # The particle objects will be stored in this  list


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
        self.pausePlayButton = Buttons('Pause/Play', 'Play', 0, 40, 100, 100,
                                       None,  'rectangle', 30,  colours['black'],
                                       colours['black'], colours['white'], self, '\Play')

        self.selectedParticle = None # Particle which is being controlles using sliders

        self.addParticleButton = Buttons('Add Particle', 'Add,Particle', 0, 140,
                                         50, 50, None, 'rectangle', 30,
                                         colours['black'],colours['black'],
                                         colours['white'],self, '')
        self.resetButton = Buttons('Reset', 'Reset',0,190, 50, 50, None, 'rectangle',
                                   30,  colours['black'], colours['black'],
                                   colours['white'],self, '')
        self.settingsButton = Buttons('Settings', 'Settings',0,240, 50, 50,
                                      None, 'rectangle', 30,  colours['black'],
                                      colours['black'],colours['white'],self, '')

        self.listOfSliders = [Slider('radius', 'radius', 150, 40,10, 60, self,
                                     self, 100, 50, 'integers',30),
                              Slider('particle elasticity', 'particleElasticity',
                                     150, 90,0, 2, self, self, 100, 50, '',1),
                              Slider('wall elasticity', 'wallElasticity', 300,
                                     90,0, 2, self, self, 100, 50, '',1),
                              Slider('speed', 'speed', 300, 40, 0, 5, self,
                                     self, 100, 50, '',1)]
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
        a = BooleanVar() # Tkinter construct to hold Boolean values
        velocityButton = Checkbutton(self.root,background = 'white',
                                     text = "Show velocity", variable = a,
                                     onvalue = True, offvalue = False,
                                     command = lambda a = a,self = self: exec("self.showVelocity = a.get()"))

        velocityButton.grid(row = 1, column = 0)
        # Ensures that the checkbuttons are in consistent states
        if (self.showVelocity):
            velocityButton.select()


        b = BooleanVar()# Tkinter construct to hold Boolean values
        massButton = Checkbutton(self.root,background = 'white',
                                 text = "Show mass", variable = b,
                                 onvalue = True, offvalue = False,
                                 command = lambda b = b,self = self: exec("self.showMass = b.get()"))

        massButton.grid(row = 2, column = 0)
        # Ensures that the checkbuttons are in consistent states
        if (self.showMass):
            self.massButton.select()

        c = BooleanVar()# Tkinter construct to hold Boolean values
        KEButton = Checkbutton(self.root,background = 'white',
                               text = "Show kinetic energy", variable = c,
                               onvalue = True, offvalue = False,
                               command = lambda c = c,self = self: exec("self.showKE = c.get()"))
        KEButton.grid(row = 3, column = 0)
        if (self.showKE):# Ensures that the checkbuttons are in consistent states
            KEbutton.select()


    def showText(self,text, centreX, centreY, fontColour, fontBg, fontSize):
            # initialises font for displaying text
            basicfont = pygame.font.SysFont('times.ttf', fontSize)
            text = basicfont.render(text, True, fontColour, fontBg) # Text for pause
            textrect = text.get_rect()
            textrect.center = (centreX,centreY) #
            self.screen.blit(text, textrect) # Shows text on self.screen

    def updateSliders(self):
        for slider in self.listOfSliders+self.selectedParticle.listOfSliders:
            if (slider.movePointer):
                if (slider.x < pygame.mouse.get_pos()[0] < slider.x + slider.width):
                    slider.pointer.setCor(pygame.mouse.get_pos()[0],
                                          slider.pointer.y, slider.pointer.z)
                    slider.pointer.screenPos = (pygame.mouse.get_pos()[0],
                                                slider.pointer.y)
                    slider.setVariable()
            if (slider in self.selectedParticle.listOfSliders):
                self.selectedParticle.listOfSliders[0].setValue(self.selectedParticle.mass)
                #self.selectedParticle.listOfSliders[1].setValue(self.selectedParticle.velocity)
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
            if event.type == pygame.QUIT: # Checks if the user wants to close the window
                self.deleteAllWindows()
                pygame.quit()
                sys.exit()

            if (event.type == pygame.MOUSEBUTTONDOWN):
                if (event.button == 1):
                    # Checks if the user has clicked on the button
                    if (self.pausePlayButton.mouseOverButton()):
                        if (self.run):
                            self.run = False # Stops simulation
                            # Changes image to play symbol
                            try:
                                filePath = fileLocation + '\Play' + '.jpg'
                                image = pygame.image.load(filePath).convert()
                                self.pausePlayButton.image = image
                            except:
                                self.pausePlayButton.text = 'Play'
                        else:
                            self.run = True # Restarts simulation
                            # Changes image to pause symbol
                            try:
                                filePath = fileLocation + '\Pause' + '.jpg'
                                image = pygame.image.load(filePath).convert()
                                self.pausePlayButton.image = image
                            except:
                                self.pausePlayButton.text = 'Pause'

                    elif (self.addParticleButton.mouseOverButton()):
                        # Creates a new partcile with
                        p = Particle2D(randint(self.radius, self.width-self.radius),
                                       randint(self.radius, self.height-self.radius),
                                       randint(1,5), [randint(-2,2),randint(-2,2)], self)
                        self.listOfParticles.append(p)

                    elif (self.resetButton.mouseOverButton()):
                        self.listOfParticles = []

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
                        # Slider control of user
                        if (slider.pointer.mouseOverPoint()):
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
                    self.listOfParticles[j].colour = particle.particlePlayColour

            # If a particle's position is being controlled by the user then the
            # position xCorof the particle will be the xCor of the mouse
            if (particle.moveParticle):
                if (particle.radius < pygame.mouse.get_pos()[0] < self.width - particle.radius):
                    particle.x = pygame.mouse.get_pos()[0]
                if (particle.radius < pygame.mouse.get_pos()[1] < self.height - particle.radius):
                    particle.y = pygame.mouse.get_pos()[1]


            if (not self.run):
                # If the simulation has been paused then the colour of all the
                # particles will turn grey to reflect this
                particle.colour = particle.particlePauseColour
            # Shows the self.velocities and self.masses of the particles.
            particle.showInfo(self.showMass, self.showVelocity, self.showKE)
            particle.draw() # Draws the circles on the self.screen
            particle.listOfParticles = self.listOfParticles
            particle.run = self.run
            if (self.run):
                for j in range(0, len(self.listOfParticles)):
                    self.listOfParticles[j].colour = particle.particlePlayColour


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


    def updateWindow(self):
        for i in range(0,5):
            for particle in self.listOfParticles:
                try:
                    particle.root.update_idletasks()
                    particle.root.update()
                    if (i == 4):
                        pygame.draw.aaline(self.screen, (255,0,0),
                                           (particle.x, particle.y),
                                           (particle.root.winfo_x(),
                                            particle.root.winfo_y()), 2)
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

        #pygame.display.update() # Updates the self.screen
        # Stops the loop for some time so the speed at which the particles are
        # moving can be controlled
        time.sleep(0.0)


    def getComponentVelocities(self, p1, p2):
        (dx,dy) = (p2.x-p1.x,-(p2.y-p1.y))

        angle = atan2(dy,dx)

        matrix = rotation(-angle,'z')

        v1 = matrixMultiply(matrix, [[p1.velocity[0]],[p1.velocity[1]],[0],[1]])
        v2 = matrixMultiply(matrix, [[p2.velocity[0]],[p2.velocity[1]],[0],[1]])

        if (v1[1][0] == 0):
            angle1 = pi/2
        else:
            angle1 = atan(v1[1][0]/v1[1][0])


        if (v2[1][0] == 0):
            angle2 = pi/2
        else:
            angle2 = atan(v2[1][0]/v2[1][0])


        return [p1.getSpeed()*cos(angle1),p2.getSpeed()*cos(angle2),
                p1.getSpeed()*sin(angle1),p2.getSpeed()*sin(angle2)]

    def collisionDetection(self):
        # Iterates through all the particles
        for i in range(0, len(self.listOfParticles)):
            p1 = self.listOfParticles[i]
            if (self.width - (p1.x+p1.radius) <= 0 and p1.velocity[0] > 0
                or p1.x-p1.radius <= 0 and p1.velocity[0] < 0):
                p1.velocity[0] = p1.velocity[0]*(-self.wallElasticity)

            if (self.height - (p1.y+p1.radius) <= 0 and -p1.velocity[1] > 0
                or p1.y-p1.radius <= 0 and -p1.velocity[1] < 0):
                p1.velocity[1] = p1.velocity[1]*(-self.wallElasticity)

            # Iterates through all the particles before the current one
            for j in range(0,i):
                p2 = self.listOfParticles[j]
                distance = hypot(p2.y-p1.y,p2.x-p1.x)
                if (distance < 2*self.radius): # Checks if there is an overlap
                    self.collisionCalculator2D(p1,p2)
                    pygame.display.update()
                    time.sleep(1)

    def collisionCalculator2D(self, particle1, particle2):
        p1 = particle1
        p2 = particle2

        (dx,dy) = (particle2.x-particle1.x,-(particle2.y-particle1.y))
        # Angle that the line of centres makes with the horizontal
        angle = atan2(dy,dx)

        # For testing purporposes
        pygame.draw.aaline(self.screen, (255,0,0), (p1.x +3*dx,p1.y-3*dy),
                           (p2.x-3*dx,p2.y+3*dy))
        pygame.draw.circle(self.screen, (0,255,0), (int(p1.x),int(p1.y)),
                           p1.radius+5, 2)
        pygame.draw.circle(self.screen, (0,0,255), (int(p2.x),int(p2.y)),
                           p2.radius+5, 2)

        # Gets components parallel and perpendicular to the line of centres
        components = self.getComponentVelocities(particle1, particle2)


        # Final velocities parallel to the line of centres
        solution = collisionCalculator(components[0], components[1],
                                       particle1.mass, particle2.mass,
                                       self.particleElasticity)

        # Assigns velocities based on the gradient
        if (dy < 0 and dx < 0):
            print((dy,dx))
            particle1.velocity = [-sin(angle)*components[0]+solution[0]*cos(angle),
                                  (cos(angle)*components[2]+solution[0]*sin(angle))]

            particle2.velocity = [(sin(angle)*components[1]+solution[1]*cos(angle)),
                                  -(cos(angle)*components[3]+solution[1]*sin(angle))]
        if (dy > 0 and dx < 0):
            print((dy,dx))
            particle1.velocity = [sin(angle)*components[0]+solution[0]*cos(angle),
                                  (cos(angle)*components[2]+solution[0]*sin(angle))]

            particle2.velocity = [-(sin(angle)*components[1]+solution[1]*cos(angle)),
                                  -(cos(angle)*components[3]+solution[1]*sin(angle))]
        if (dy < 0 and dx > 0):
            print((dy,dx))
            particle1.velocity = [-(sin(angle)*components[0]+solution[0]*cos(angle)),
                                  (cos(angle)*components[2]+solution[0]*sin(angle))]

            particle2.velocity = [(sin(angle)*components[1]+solution[1]*cos(angle)),
                                  -(cos(angle)*components[3]+solution[1]*sin(angle))]
        if (dy > 0 and dx > 0):
            print((dy,dx))
            particle1.velocity = [(sin(angle)*components[0]+solution[0]*cos(angle)),
                                  -(cos(angle)*components[2]+solution[0]*sin(angle))]

            particle2.velocity = [-(sin(angle)*components[1]+solution[1]*cos(angle)),
                                  -(cos(angle)*components[3]+solution[1]*sin(angle))]

        particle1.velocity = list(map(lambda x: round(x,2), particle1.velocity))
        particle2.velocity = list(map(lambda x: round(x,2), particle2.velocity))
        # Moves the particles in the direction of the line of centres to avoid continuous overlap
        dist = hypot((particle2.y+particle2.velocity[1])-(particle1.y+particle1.velocity[1]),
                     (particle2.x+particle2.velocity[0])-(particle1.x+particle1.velocity[0]))
        while (dist - 2*self.radius < 0):
            v = (particle2.velocity[0]-particle1.velocity[0],
                 particle2.velocity[1]-particle1.velocity[1])
            (particle1.x,particle1.y) = (particle1.x+dx*0.01,particle1.y-dy*0.01)
            (particle2.x,particle2.y) = (particle2.x-dx*0.01,particle2.y+dy*0.01)

    def generateDefaultParticles(self):
        for i in range(0,len(self.velocities)):
            # Creates a new partcile with
            p = Particle2D(randint(self.radius,self.width-self.radius),
                           randint(self.radius,self.height-self.radius), randint(1,5),
                           [randint(-2,2),randint(-2,2)], self)
            self.listOfParticles.append(p)
        self.selectedParticle = self.listOfParticles[0]

    def main(self):
        # Fills the screen with white to erase the current objects
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
