import pygame
import math

class Bullet:

    #constractor
    def __init__(self, surface, start_x, start_y, angle, progress, color):
        self.surface = surface
        self.angle = angle
        self.start_x = start_x
        self.start_y = start_y
        self.progress = progress
        self.color = color
        self.x = self.start_x + (self.progress * math.sin(math.radians(self.angle)))
        self.y = self.start_y + (self.progress * math.cos(math.radians(self.angle)))


    def show(self, x_screen, y_screen):
        """
        show bullet
        """
        pygame.draw.circle(self.surface, self.color, (int(self.x) - x_screen , int(self.y) - y_screen), 5)

    def update(self):
        """
        matches the progress and start position to the current postion
        """
        self.x = self.start_x + (self.progress * math.sin(math.radians(self.angle)))
        self.y = self.start_y + (self.progress * math.cos(math.radians(self.angle)))


    def to_list(self):
        """
        return a list of bullet information
        """
        return [self.start_x, self.start_y, self.angle, self.progress, self.color]




