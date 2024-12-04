"""
This (script.py) must be the name of the file that contains/calls commands to move the robot.

Any functions that you want to be run must be in the main method, and must be called as robot.method() (ex. robot.auto_home())

Do NOT Delete the main() method, or your script will not run. You can feel free to write any other helper methods/classes outside of main.

"""
from bot import Bot # This line is not strictly necessay as variables and imports are shared across files in the ESP32, however, if you are using VSC, this will be helpful for viewing doctrings.
import math

async def main(robot:Bot):
    """
    Add main functions in this method.
    """
    # The following is a circle algorithm just for testing purposes:
    # Circle function:
    # radius = 1cm, so circumference = 2
    center_x = 100
    center_y = 100

    x=50
    theta=0
    radius = 50
    x_init = 100+radius
    y_init = 100
    await robot.go_to(x_init, y_init)
    for i in range(x):
        theta+=(2*math.pi)/x
        x_curr = center_x + radius * math.cos(theta)
        y_curr = center_y + radius * math.sin(theta)
        await robot.go_to(x_init,y_init,x_curr,y_curr,1,0.2)
        x_init,y_init = robot.loc_x, robot.loc_y

        