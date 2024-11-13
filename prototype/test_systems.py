"""
This file is used to test all the subsystems of the robot without needing to use the UI, since it is still in development.

Will be stored in ESP32 local and run from main.py, along with test_bot.py which is a simplified version of the bot class.
"""

import test_bot
from test_bot import Bot

def test_systems():
    robot = Bot()
    robot.zero_X()
    while(not robot.is_robot_zero()):
        robot.stepOne_Y()
        if(robot.limit_switch_y.value() == 0):
            robot.zero_Y()

    print(str(robot.get_status()))
    robot.pen_down()
    print("Pen should be down: " + str(robot.get_status()))
    robot.pen_up()
    print("Pen should be up: " + str(robot.get_status()))

    robot.pen_down()

    robot.go_to(0,50)
    print(str(robot.get_status))
    robot.go_to(50,robot.loc_y)
    print(str(robot.get_status))
    robot.go_to(100,152)
    robot.pen_up()
    robot.go_to(50,50)

