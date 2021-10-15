from buttons import Buttons
from graph import Graph
import utils
import pygame
from utils import colours
import sys
import pickle


# Allows multiple Graph objects to exist simultaneously
class App:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.tabs = {}
        self.max_tabs = 1
        self.number_of_tabs = 1
        self.tabs = {}
        self.events = []
        self.graphs = {}
        self.tab_width = 100
        self.tab_height = 30
        self.tabs['t0'] = Buttons('t0', 'Graph ', 0, 0,
                                  self.tab_width, self.tab_height, None, 'rectangle',
                                  20, colours['black'],
                                  colours['black'], colours['white'],
                                  self, '')

        self.graphs['t0'] = Graph(width, height, self)

        self.current_tab = 't0'

        self.new_tab_button = Buttons('New Tab', '+', self.tab_width + 20,
                                      15, self.tab_width, self.tab_height, 15, 'circle',
                                      30, colours['black'], colours['black'],
                                      colours['white'], self, '')
    def get_screen(self):
        from utils import screen
        return screen

    def get_events(self):
        return self.events

    def update_tabs(self):
        while True:  # Program will continue to run unless interrupted
            self.events = pygame.event.get()  # Gets all the keyboard and mouse inputs of the user

            obj = self.graphs[self.current_tab]  # Current object that is being run
            obj.main()  # Runs the main method

            self.show_tabs()

            self.check_events(obj)

            pygame.display.update()

    def show_tabs(self):
        for tab in self.tabs.values():  # Draws all the buttons representing the tabs
            if tab.title == self.current_tab:
                tab.font_colour = (255, 0, 0)
            else:
                tab.font_colour = (0, 0, 0)
            tab.show_button()
        self.new_tab_button.show_button()  # Draws button to add new tab

    def check_events(self, obj):
        for event in self.events:
            if event.type == pygame.QUIT:
                self.save_app()
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for tab in self.tabs.values():
                        if tab.mouse_over_button():
                            self.current_tab = tab.title
                            button_selected = True

                    if self.new_tab_button.mouse_over_button():
                        button_selected = True
                        self.new_tab_button.x += self.tab_width  # Shifts the new tab button to the  right
                        self.number_of_tabs += 1  # Increments the number of tabs
                        # Creates new tab with the same object as the current tab
                        if type(obj).__name__ == 'Graph':
                            # type(object).__name__ returns the name of the
                            # class of the which the object is an instance of
                            button = Buttons('t' + str(self.number_of_tabs),
                                             'Graph', self.tab_width * (self.number_of_tabs - 1),
                                             0, self.tab_width, self.tab_height, None, 'rectangle',
                                             20, colours['black'],
                                             colours['black'],
                                             colours['white'], self, '')
                            self.tabs['t' + str(self.number_of_tabs)] = button
                            graph = Graph(self.width, self.height, self)
                            self.graphs['t' + str(self.number_of_tabs)] = graph

    def save_app(self):
        self.events = []
        file = open(utils.APP_PATH, 'wb')
        self.remove_unnecessary_objects()
        pickle.dump(self, file)

    def remove_unnecessary_objects(self):
        for graph in self.graphs.values():
            for button in graph.buttons:
                button.image = None

    def reset_graph(self):
        for graph in self.graphs.values():
            for button in graph.buttons:
                button.set_image()
