from config.constants import g, JUMP_STRENGTH, BIRD_COL
from game.collision import clamp
from game.generate import Circle

import math, pygame

class Bird():
    def __init__(self, x:float, y:float, r:float, height:float):
        self.vy = 0

        self.x = x
        self.y = y
        self.r = r

        self.height = height


    def update(self):
        #apply gravity
        self.vy += g

        self.y += self.vy
        if self.y < 0:
            self.vy = 0

        if self.y > self.height - self.r:
            return True #if dies

        #apply velocities
        self.y = clamp(ub=self.r, val=self.y, lb=self.height-self.r) #make sure doesnt go off-screen

        return False


    def jump(self):
        self.vy = -JUMP_STRENGTH


    def render(self, screen):
        pygame.draw.circle(surface=screen, color=BIRD_COL, center=(self.x, self.y), radius=self.r)


    def getBall(self):
        return Circle(x=self.x, y=self.y, r=self.r)