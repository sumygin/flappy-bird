from config.constants import g, JUMP_STRENGTH, SCROLL_SPEED

class Bird():
    def __init__(self, x:float, y:float):
        self.vx = SCROLL_SPEED
        self.vy = 0
        self.x = x
        self.y = y

    def update(self):
        #apply gravity
        self.vy += g

        #apply velocities
        self.x += self.vx
        self.y += self.vy

    def jump(self):
        self.vy -= JUMP_STRENGTH