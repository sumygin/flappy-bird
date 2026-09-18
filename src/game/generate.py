import random, pygame
from dataclasses import dataclass

from config.constants import *

@dataclass  
class Box:
    #top-left corner
    x:float
    y:float
    w:float
    h:float
    passed:bool = False


@dataclass
class Circle:
    #centre
    x:float
    y:float
    r:float


def box_to_rect(box:Box):
    return pygame.Rect(box.x, box.y, box.w, box.h)


class Screen():
    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height

        self.timesteps_since_obstacle = 0

        self.active_obstacles = []
        #active_obstacles is a queue of the obstacles on the screen. every timestep they are moved


    def get_obstacles(self):
        return self.active_obstacles


    def update(self):
        #if needed, add new obstacle at right edge

        if self.timesteps_since_obstacle > OBSTACLE_FREQ or not self.active_obstacles:
            self.create_obstacle()
            self.timesteps_since_obstacle = 0
        else:
            self.timesteps_since_obstacle += 1

        #delete obstacle off-screen, NOTE: only does one at a time
        first_obst = self.active_obstacles[0]

        if first_obst.x + first_obst.w <= 0:
            self.active_obstacles.pop(0)
            self.active_obstacles.pop(0)

        #move active obstacles
        for obstacle in self.active_obstacles:
            obstacle.x -= SCROLL_SPEED


    def create_obstacle(self):
        #determine obstacle height, then create two boxes to match
        gap_height = random.randint(OBSTACLE_MIN_GAP_HEIGHT, OBSTACLE_MAX_GAP_HEIGHT)
        obs_width = random.randint(OBSTACLE_MIN_WIDTH, OBSTACLE_MAX_WIDTH)
        
        gap_y = random.randint(OBSTACLE_GAP_PADDING, self.height - OBSTACLE_GAP_PADDING - gap_height)

        #add top box
        self.active_obstacles.extend([
            Box(
                x=self.width, y=0, w=obs_width, h=gap_y
            ),
            Box(
                x=self.width, y=gap_y+gap_height, w=obs_width, h=self.height-(gap_y + gap_height)
            )]
        )


    def get_obstacles_between_bounds(self):
        #instead of checking collision against all obstacles, we check only those within range of bird
        pass


    def render_bg(self, screen):
        screen.fill(BG_COL)


    def render(self, screen):
        #draw all boxes

        for obst in self.active_obstacles:
            pygame.draw.rect(surface=screen, color=OBST_COL, rect=box_to_rect(obst))