import pygame
from utils import show_multiline_text


# This class is used to represents individual lines created by the user
class Line:
    def __init__(self, point1, point2, parent_window, text=''):
        self.point1 = point1  # Point object
        self.point2 = point2  # Point object
        self.parent_window = parent_window
        self.colour = (0, 0, 0)  # The colour of the line
        self.text = text

    def delete_line(self):
        self.parent_window.lines.remove(self)
        self.parent_window.selected_lines.remove(self)

    # Draws the line on-screen by using the coordinates of the points
    def draw_line(self, showLabel=True):
        if self in self.parent_window.selected_lines:
            self.colour = (255, 0, 0)
        elif self not in self.parent_window.grid_lines:
            self.colour = (0, 0, 0)

        pygame.draw.aaline(self.parent_window.get_screen(), self.colour, self.point1.screen_pos,
                           self.point2.screen_pos)

        if showLabel and self.text != '':
            show_multiline_text(self.parent_window.get_screen(), self.text,
                                int((self.point1.screen_pos[0] + self.point2.screen_pos[0]) / 2),
                                int((self.point1.screen_pos[1] + self.point2.screen_pos[1]) / 2),
                                (255, 0, 0), (255, 255, 255), 20)

    def mouse_over_line(self):
        # If the line is vertical
        if (self.point2.screen_pos[0] - pygame.mouse.get_pos()[0] == 0
                or self.point2.screen_pos[0] - self.point1.screen_pos[0] == 0):
            if (abs(self.point2.screen_pos[0] - pygame.mouse.get_pos()[0]) == 0
                    and abs(self.point2.screen_pos[0] - self.point1.screen_pos[0]) == 0
                    and min(self.point1.cor[1], self.point2.cor[1]) < pygame.mouse.get_pos()[1] < max(
                        self.point1.cor[1], self.point2.cor[1])):
                return True
            else:
                return False

        if (min(self.point1.screen_pos[0], self.point2.screen_pos[0]) < pygame.mouse.get_pos()[0] < max(self.point1.screen_pos[0],
                                                                                                        self.point2.screen_pos[0])
                and min(self.point1.screen_pos[1], self.point2.screen_pos[1]) < pygame.mouse.get_pos()[1] < max(
                    self.point1.screen_pos[1], self.point2.screen_pos[1])):
            dy = (self.point2.screen_pos[1] - self.point1.screen_pos[1])
            dx = (self.point2.screen_pos[0] - self.point1.screen_pos[0])
            # Gradient of line joining two adjacent points on the curve
            gradient1 = dy / dx
            dy = (self.point2.screen_pos[1] - pygame.mouse.get_pos()[1])
            dx = (self.point2.screen_pos[0] - pygame.mouse.get_pos()[0])
            # Gradient of line joining the point on the curve and the point
            # where the mouse has been clicked
            gradient2 = dy / dx
            if abs(round(gradient1, 1)) < 0.1:
                if abs(round(gradient2, 1)) < 0.1 and gradient1 * gradient2 >= 0:
                    return True
            elif (abs(round(gradient1, 1)) * 0.82 < abs(round(gradient2, 1)) < abs(round(gradient1, 1) * 1.18)
                  and gradient1 * gradient2 >= 0):
                return True
            else:
                return False

    def visible(self):  # Determines if the line will be visible to the user
        if self.point1.screen_pos[0] < 0 and self.point2.screen_pos[0] < 0:
            return False
        # If the x-coordinates of both points are outside the width range of the screen
        elif (self.point1.screen_pos[0] > self.parent_window.width
              and self.point2.screen_pos[0] > self.parent_window.width):
            return False
        # If the y-coordinates of both points are outside the hight range of the screen
        elif ((self.point1.screen_pos[1] < 0 and self.point2.screen_pos[1] < 0)
              or (self.point1.screen_pos[1] > self.parent_window.height
                  and self.point2.screen_pos[1] > self.parent_window.height)):
            return False
        else:
            return True  # In any other case
