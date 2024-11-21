"""
This file is used to test drawing a circle
"""

import test_bot
import math
import bot
from test_bot import Bot

def test_systems():
    robot = Bot()
    robot.zero_X()

    robot.go_to(100, 100)

    segments=50
    theta=0
    radius = 50
    
    robot.pen_down()

    for i in range(segments):
        theta+=(2*math.pi)/segments
        x_curr = robot.loc_x + radius * math.cos(theta)
        y_curr = robot.loc_y + radius * math.sin(theta)

        robot.go_to(x_curr, y_curr)
        