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




    # TODO: Test the Servo() implementation with a breadboard and the ESP-32. Use the https://pypi.org/project/micropython-servo/ docs to help
    def __init__(self):
        """
        The Bot class is instantiated in boot.py, and therefore init is called. It is assumed that the robot
        does not know its own position upon startup, and therefore will be required to zero in X, Y, and the Pen_Z directions before going anywhere.
        In order to zero the robot, a student will need to use the robot teleop interface, or select to use the auto_zero() method, also done in the interface.

            Args:
                None

            Returns:
                None

        """


        # State Variables
        self.is_zero = False # Note: This variable is treated as a final variable after it evaluates to True because it will never be changed again in main.py after being zeroed.
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

        


    # TODO: Find what input we would get from the limit_switch if it is triggered, and see how we can use that to say:
    # if(there's an indicator that the limit switch has been hit): then set self.loc_x = 0
    # There might be a limit switch library, though I have done zero research on this. My guess is that the input is simple a 1 or 0 (High, Low) where a High might mean it was triggered.
    def zero_X(self):
        """This method sets loc_x to 0."""
        self.loc_x=0
    
    # TODO: Find what input we would get from the limit_switch if it is triggered, and see how we can use that to say:
    # if(there's an indicator that the limit switch has been hit): then set self.loc_y = 0
    # There might be a limit switch library, though I have done zero research on this. My guess is that the input is simple a 1 or 0 (High, Low) where a High might mean it was triggered.
    def zero_Y(self):
        """This method sets loc_y to 0."""
        self.loc_y=0


    # TODO: Update the logic for self.is_zero based on the new parameters (only loc_x, loc_y, is there any way to make sure the pen is up before as well?)
    # self.is_zero = (self.loc_x,self.loc_y,self.pen_state)=(0,0,False) is a potential solution, but this involves in making sure we understand how servos work in terms of up/down upon startup
    def is_robot_zero(self):
        """
        Evaluates whether both loc_x and loc_y have been zeroed.

        This method is only called at startup (ie. when the robot is zeroed at first), and once is_zero is set to True, is treated as a final variable.
        This method checks if loc_x, loc_y, and pen_zero are zeroed, and sets is_zero to this value. This is valuable so that no automated instructions are carried out
        before the robot is zeroed.

        Returns:
            bool: is_zero

        """
        self.is_zero = (self.loc_x,self.loc_y,self.pen_zero,self.pen_loc) == (0,0,True,0)
        return self.is_zero
    
    def enable(self):
        """
        This method enables the robot by setting the enable pins. 
        
        There are two possible ways it can be called (yet to be decided): 
        1) Within main.py after is_robot_zero returns True. 
        2) After is_robot_zero returns True, we allow the user to click an enable button in the interface.

        Maybe the robot will be automatically enabled, 
        """
        self.enable_x.value(0)
        self.enable_y.value(0)

    # TODO: We will need to discuss abotu error raising or other things with this method. This isn't all that important at the moment.
    def disable(self):
        """
        Used at the termination of a program, or called by the user in the case of an E-Stop
        """
        self.enable_x.value(1)
        self.enable_y.value(1)
        self.pen_up()

    # TODO: Implement the set_direction method, which will take in the pin id (ex. `direction_x`) that suggests which motor we're reversing, and the value (a 1 or 0).
    # As a modifier method, it would look something like, where pin_object is for example, `direction_x` and value_given is a function parameter: pin_object.value(value_given)
    # Bonus ---> Write a good docstring using the Google Convention for this method
    def set_direction(self):
        pass


    # BIG TODO: As a start, familiarize yourself with the Bresenham's Line Algorithm (Google this), and think about what variables/states matter
    # Let's do this method together, because it involves a lot of method calling, logic, and math and also should be written really cleanly.
    def go_to(self, x: float, y: float):
        """
        This method takes in data from the HTML User interface, and moves the robot. It is primarily used for
        testing purposes and also for zeroing the robot at the beginning of the 

            Args:
                x (float): The desired x coordinate with reference to the zero point 
                y (float): The desired y coordinate with reference to the zero point

            Returns:
                None
        """
        pass
  
    
    # TODO: Implement the logic for the method (if the Servo() object implementation works (see __init__ for more), then use the pertinent methods in here). 
    # This is entirely dependent on how you decide to control the servo and its protocols, so there's not much more I can say here.
    def pen_up(self):
        """
        This method moves or keeps the pen up.
        """

    # TODO: Implement the logic for the method (if the Servo() object implementation works (see __init__ for more), then use the pertinent methods in here). 
    # This is entirely dependent on how you decide to control the servo and its protocols, so there's not much more I can say here.
    def pen_down(self):
        """
        This method moves or keeps the pen down.
        """
