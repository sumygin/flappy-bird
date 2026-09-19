from config.constants import g, JUMP_STRENGTH, BIRD_COL, TRAINING, SCROLL_SPEED, WHITE
from game.collision import clamp, Point
from game.generate import Circle

import math, pygame

class Bird():
    def __init__(self, x:float, y:float, r:float, height:float):
        self.vy = 0

        self.x = x
        self.y = y
        self.r = r

        self.height = height

        self.trail = []


    def update(self):

        self.y += self.vy

        if self.y > self.height - self.r or self.y < self.r:
            return True #if dies

        #apply velocities
        self.y = clamp(ub=self.r, val=self.y, lb=self.height-self.r) #make sure doesnt go off-screen

        self.vy = JUMP_STRENGTH


        if not TRAINING:
            last_point_index = 0

            for i in range(len(self.trail)):
                point = self.trail[i]
                

                if point.x < 0:
                    last_point_index = i
                else:
                    point.x -= SCROLL_SPEED

            self.trail = self.trail[last_point_index:]

            self.trail.append(Point(self.x, self.y))

        return False


    def jump(self):
        self.vy = -JUMP_STRENGTH


    def render(self, screen):
        if not TRAINING:
            for point in self.trail:
                pygame.draw.circle(surface=screen, color=WHITE, center=(point.x, point.y), radius=self.r/2)
        
        pygame.draw.circle(surface=screen, color=BIRD_COL, center=(self.x, self.y), radius=self.r)



    def getBall(self):
        return Circle(x=self.x, y=self.y, r=self.r)


    def getVy(self):
        return self.vy