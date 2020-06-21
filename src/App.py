from Buttons import Buttons
from ElasticCollisionsInOneDimension import ElasticCollisionsInOneDimension
from ElasticCollisionsInTwoDimensions import ElasticCollisionsInTwoDimensions
from Graph import *

# Allows multiple Graph objects to exist simultaneously
class App:
    def __init__(self, screen, width, height):
        colours = {'white': (255, 255, 255), 'black' : (0, 0, 0), 'red' : (255, 0, 0),
                   'blue' : (0, 0, 255), 'green' : (0, 255, 0)}
        self.screen = screen
        (width, height) = self.screen.get_size()
        self.tabs = {}
        self.maxTabs = 2
        self.numberOfTabs = 2
        self.listOfTabs = []

        for i in range(self.maxTabs + 1):
             if (i == 0):
                 self.listOfTabs.append(Buttons('t'+str(i),'Elastic,Collisions',
                                                100*i , 0   ,100    ,30     ,None,  'rectangle', 20,
                                                colours['black'],colours['black'],colours['white'], self,''))
                 self.tabs['t'+str(i)] = ElasticCollisionsInOneDimension(width, height, self.screen, self)
             elif (i == 1):
                 self.listOfTabs.append(Buttons('t'+str(i),'2d,Collisions', 100*i,
                                                0   ,100    ,30     ,None,  'rectangle',
                                                20,     colours['black'],colours['black'],colours['white'], self,''))
                 self.tabs['t'+str(i)] = ElasticCollisionsInTwoDimensions(width, height, self.screen, self)

             else:
                 self.listOfTabs.append(Buttons('t'+str(i),'Graph ', 100*i , 0,
                                                100    ,30     ,None,  'rectangle',
                                                20,     colours['black'],
                                                colours['black'], colours['white'], self,''))
                 self.tabs['t'+str(i)] = Graph(width, height, self.screen, self)
        self.currentTab = 't2'

        self.newTabButton = Buttons('New Tab' ,'+', 320, 15 , 100 ,30 , 15,'circle',
                                    30,colours['black'],colours['black'],
                                    colours['white'], self,'')

    def updateTabs(self):
        while (1): # Program will continue to run unless interrupted
            self.events = pygame.event.get() # Gets all the keyboard and mouse inputs of the user
            obj = self.tabs[self.currentTab] # Current object that is being run
            obj.main() # Runs the main method

            for tab in self.listOfTabs: # Draws all the buttons representing the tabs
                if (tab.title == self.currentTab):
                    tab.fontColour = (255,0,0)
                else:
                    tab.fontColour = (0,0,0)
                tab.showButton()

            self.newTabButton.showButton()# Draws button to add new tab

            for event in self.events:
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    if (event.button == 1):
                        for tab in self.listOfTabs:
                            if (tab.mouseOverButton()):
                                self.currentTab = tab.title
                                buttonselected = True

                        if (self.newTabButton.mouseOverButton()):
                            buttonselected = True
                            self.newTabButton.x += 100 # Shifts the new tab button to the  right
                            self.numberOfTabs += 1 # Increments the number of tabs
                            # Creates new tab with the same object as the current tab
                            if (type(obj).__name__ == 'Graph'):
                                # type(object).__name__ returns the name of the
                                # class of the which the object is an instance of
                                buttob = Buttons('t'+str(self.numberOfTabs),
                                                 'Graph', 100*self.numberOfTabs,
                                                 0, 100, 30, None, 'rectangle',
                                                 20, colours['black'],
                                                 colours['black'],
                                                 colours['white'], self, '')
                                self.listOfTabs.append(button)
                                graph= Graph(width, height, self.screen, self)
                                self.tabs['t'+str(self.numberOfTabs)] = graph

                            elif (type(obj).__name__ == 'ElasticCollisionsInOneDimension'):
                                button = Buttons('t'+str(self.numberOfTabs),
                                                 '1d', 100*self.numberOfTabs, 0,
                                                 100, 30, None, 'rectangle', 20,
                                                 colours['black'],
                                                 colours['black'],
                                                 colours['white'], self, '')
                                self.listOfTabs.append(button)
                                app = ElasticCollisionsInOneDimension(width,
                                                                      height,
                                                                      self.screen,
                                                                      self)
                                self.tabs['t'+str(self.numberOfTabs)] = app

                            elif (type(obj).__name__ == 'ElasticCollisionsInTwoDimensions'):
                                button = Buttons('t'+str(self.numberOfTabs),
                                                 '2d', 100*self.numberOfTabs, 0,
                                                 100, 30, None, 'rectangle', 20,
                                                 colours['black'],
                                                 colours['black'],
                                                 colours['white'], self, '')
                                self.listOfTabs.append(button)
                                app = ElasticCollisionsInTwoDimensions(width,
                                                                       height,
                                                                       self.screen,
                                                                       self)
                                self.tabs['t'+str(self.numberOfTabs)] = app

            pygame.display.update()
