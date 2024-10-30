"""
This file provides the Bot class, which provides all necessary methods for control and movement of the Pen Plotter robot. 
It involves methods to take in user input, change and maintain state variables, and send/recieve signals to/from electronic devices through 
Microcontroller Pin states. Users of this class will enjoy the fact that low abstraction controls have been implemented, therefore allowing users to
focus on algorithmic development and application.

"""

from machine import Pin
import utime

from servo import Servo

class Bot:
    
    # Constants:
    DIRECTION_X_PIN = None
    STEP_X_PIN = None
    ENABLE_X_PIN = None
    DIRECTION_Y_PIN = None
    STEP_Y_PIN = None
    ENABLE_Y_PIN = None
    SERVO_PIN = None
    LIMIT_SWITCH_X = None
    LIMIT_SWITCH_Y = None

    


    def __init__(self):
        """
        The Bot class is instantiated in boot.py, and therefore init is called. It is assumed that the robot
        does not know its own position upon startup, and therefore will be required to zero in X, Y, and the Pen_Z directions before going anywhere.
        In order to zero the robot, a student will need to use the robot teleop interface, or select to use the auto_zero() method, also done in the interface.

            Parameters:
            None

            Returns:
            None

        """


        # State Variables
        self.is_zero = False
        self.loc_x = None
        self.loc_y = None
        self.pen_state = None # True -> Pen Down, False -> Pen Up

        # Create Pin Objects:
        self.direction_x = Pin(self.DIRECTION_X_PIN, Pin.OUT)
        self.step_x = Pin(self.STEP_X_PIN, Pin.OUT)
        self.enable_x = Pin(self.ENABLE_X_PIN, Pin.OUT)
        self.direction_y = Pin(self.DIRECTION_Y_PIN, Pin.OUT)
        self.step_y = Pin(self.STEP_Y_PIN, Pin.OUT)
        self.enable_y = Pin(self.ENABLE_Y_PIN, Pin.OUT)
        self.pen_servo = Servo(self.SERVO_PIN)
        self.limit_switch_x = Pin(self.LIMIT_SWITCH_X, Pin.IN)
        self.limit_switch_y = Pin(self.LIMIT_SWITCH_Y, Pin.IN)

        



    def zero_X(self):
        """This method sets loc_x to 0."""
        self.loc_x=0
    
    def zero_Y(self):
        """This method sets loc_y to 0."""
        self.loc_y=0



    def set_XY_zero(self):
        """
        Note: This method is only called at startup (ie. when the robot is zeroed at first), and once is_zero is set to True, is treated as a final variable.
        This method checks if loc_x, loc_y, and pen_zero are zeroed, and sets is_zero to this value. This is valuable so that no automated instructions are carried out
        before the robot is zeroed.

        """
        self.is_zero = (self.loc_x,self.loc_y,self.pen_zero,self.pen_loc) == (0,0,True,0)


    def get_XY_zeroed(self):
        """
        This method returns whether the robot has been zeroed. Since 
        """
        return self.is_zero
    
    def enable(self):
        """
        This method enables the robot by setting the enable pins
        """
        self.enable_x.value(0)
        self.enable_y.value(0)

    def go_to(self, x: float, y: float):
        """
        This method takes in data from the HTML User interface, and moves the robot. It is primarily used for
        testing purposes and also for zeroing the robot at the beginning of the 

            Parameters:
            x -> float : The desired x coordinate with reference to the zero point 
            y -> float : The desired y coordinate with reference to the zero point

            Returns:
            None
        """
        pass
    
    
    def pen_up(self):
        """
        This method moves or keeps the pen up.
        """

    
    def pen_down(self):
        """
        This method moves or keeps the pen down.
        """
