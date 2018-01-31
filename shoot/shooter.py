import pygame
import math
from Bullet import Bullet
import random

class Shooter:

    #constractor
    def __init__(self, surface, x, y):
        self.x = x
        self.y = y
        self.surface = surface
        self.stack = []
        self.color = (random.randint(40, 250), random.randint(40, 250), random.randint(40, 250))
        self.angle = 0
        self.life = 100
        self.score = 0
        self.RADIUS = 20
        self.BULL_SPEED = 5


    def set_random_position(self, x_bound, y_bound):
        """
        sets shooter at a random position in given boundries
        """
        self.x = random.randint(0 + self.RADIUS, x_bound - self.RADIUS)
        self.y = random.randint(0 + self.RADIUS, y_bound - self.RADIUS)



    def set_new_color(self):
        """
        set a new random color
        """
        self.color = (random.randint(40, 250), random.randint(40, 250), random.randint(40, 250))



    def _rot_center(self, image):
        """
        rotate an image by its center
        """
        loc = image.get_rect().center
        rot_sprite = pygame.transform.rotate(image, self.angle)
        rot_sprite.get_rect().center = loc
        return rot_sprite


    def distance(self, x, y):
        """
        gets x and y's point on the screen and
        return the distance from shooter to this point
        """
        return math.sqrt(((self.x - x)**2) + ((self.y - y)**2))



    def _show_life(self, x_screen, y_screen):
        """
        shows a rectangle representing shooters life and place it under the shooter
        using screen deltas
        """
        pygame.draw.rect(self.surface, (255,0,0), pygame.Rect(int(self.x) - 15 - x_screen, int(self.y) + 25 - y_screen, self.life * 0.3, 3))


    #--------------------------------------------
    #INPUT: screen deltas for movement
    #OUTPUT: show shooter and its life
    #--------------------------------------------
    def show(self, x_screen, y_screen):
        """
        place shooter on the screen and show it using screen deltas
        """
        pic = pygame.image.load("shoot\\cannon.png").convert_alpha()
        pic = self._rot_center(pic)
        center = (int(self.x) - pic.get_rect().center[0] - x_screen, int(self.y) - pic.get_rect().center[1] - y_screen)
        self.surface.blit(pic, center)
        (r, g, b) = self.color
        pygame.draw.circle(self.surface, (r-40, g-40, b - 40), (int(self.x) - x_screen, int(self.y) - y_screen), self.RADIUS)
        pygame.draw.circle(self.surface, self.color, (int(self.x) - x_screen, int(self.y) - y_screen), self.RADIUS-3)
        self._show_life(x_screen, y_screen)


    def check_hit(self, stack):
        """
        get a stack of a another shooter
        and check if current shooter was hit by one of its bullet.
        if it was, decrease shooter's life.
        """
        hit_list = []
        if stack != self.stack:
            for bull in stack:
                if self.distance(bull.x, bull.y) <= self.RADIUS:
                    self.life -= 10
                    hit_list.append(bull)
        return hit_list



    def get_angle(self, x_screen, y_screen):
        """
        return angle between mouse an shooter using screen deltas.
        """
        (Mx, My) = pygame.mouse.get_pos()
        dx = self.x - Mx - x_screen
        dy = self.y - My - y_screen
        rads = math.atan2(-dy, dx)
        degs = math.degrees(rads) + 90
        return degs


    def shoot(self, shot_angle):
        """
        shoots a bullet
        """
        self.stack.append(Bullet(self.surface, self.x, self.y, shot_angle + 180, 37, self.color))


    def show_shot(self, x_screen, y_screen):
        """
        show all shooter's bullets on the screen using screen deltas
        """
        if len(self.stack) != 0:
            for bullet in self.stack:
                bullet.show(x_screen, y_screen)

    def move_shot(self):
        """
        increases all bullets' progress.
        if a bullet's progress passed 600, delete it.
        """
        for bullet in self.stack:
            if bullet.progress > 600:
                    self.stack.remove(self.stack[self.stack.index(bullet)])
            bullet.progress += self.BULL_SPEED
            bullet.update()



    def stack_to_list(self):
        """
        return a list of bullet stack information
        """
        s = []
        for bullet in self.stack:
            s.append(bullet.to_list())
        return s


    def to_list(self):
        """
        return a list of shooter information
        """
        return [self.x, self.y, self.stack_to_list(), self.color, self.angle, self.life, self.score]
