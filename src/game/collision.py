import math
from dataclasses import dataclass

from game.generate import Ball, Box

@dataclass
class Point:
    x:float
    y:float


def distance_squared(p1:Point, p2:Point):
    d_x = abs(p1.x - p2.x)
    d_y = abs(p1.y - p2.y)

    return (d_x*d_x) + (d_y*d_y)


def clamp(ub:float, lb:float, val):
    result = val

    if ub < lb: #swap if lb and ub are incorrectly arranged
        temp = ub
        ub = lb
        lb = temp

    if val > ub:
        return ub
    elif val < lb:
        return lb
    else:
        return val
    

def ball_box_collides(ball:Ball, box:Box):
    #clamp ball location to box
     
    clamped_x = clamp(
        ub=box.x + box.w,
        lb=box.x,
        val=ball.x
    )

    clamped_y = clamp(
        ub=box.y+box.h,
        lb=box.y,
        val=ball.y
    )

    dist_squared = distance_squared(Point(ball.x, ball.y), Point(clamped_x, clamped_y))

    return dist_squared < (ball.r**2)