"""
This file provides the Bot class, which provides all necessary methods for control and movement of the Pen Plotter robot. 
It involves methods to take in user input, change and maintain state variables, and send/recieve signals to/from electronic devices through 
Microcontroller Pin states. Users of this class will enjoy the fact that low abstraction controls have been implemented, therefore allowing users to
focus on algorithmic development and application.

"""

from machine import Pin
import utime

from servo import Servo

import math

class Bot:
    
    # Constants:


    DIRECTION_X_PIN = 33 # This needs to be fixed, since pins >= 34 are only Input
    STEP_X_PIN = 25
    ENABLE_X_PIN = 32

    DIRECTION_Y_PIN = 21 # Y Stepper driver is closest to ESP32
    STEP_Y_PIN = 19
    ENABLE_Y_PIN = 18

    SERVO_PIN = 27

    LIMIT_SWITCH_X = 12
    LIMIT_SWITCH_Y = 13 # Closest to ESP-32
    LIMIT_CLOSED = 0
    LIMIT_OPEN = 1

    STEPPER_DELAY = 0.001

    PULLEY_CIRCUM = 40 # 20 tooth pulley, 40 mm circumference

    STEPS_PER_REV = 200

    # Following constants are in mm
    DISTANCE_PER_STEP = PULLEY_CIRCUM/STEPS_PER_REV # 0.2 mm

    ACCEPTABLE_ERROR = 1 # This means that the acceptable error is 1mm, which doesn't make much of a difference visually.

    # Conversion from inches to mm
    MAX_X_LOC = 8*25.4
    MAX_Y_LOC = 11.5*25.4

    #Teleop button values for direction
    HTML_BUTTON_UP = 0
    HTML_BUTTON_DOWN = 1
    HTML_BUTTON_LEFT = 2
    HTML_BUTTON_RIGHT = 3


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
        self.loc_x = 4829.0 # Random values
        self.loc_y = 4829.0 # Random values
        self.pen_state = True # True -> Pen Down, False -> Pen Up
        self.enabled = False

        # Stepper_X
        self.direction_x = Pin(self.DIRECTION_X_PIN, Pin.OUT)
        self.step_x = Pin(self.STEP_X_PIN, Pin.OUT)
        self.enable_x = Pin(self.ENABLE_X_PIN, Pin.OUT)

        # Stepper_Y
        self.direction_y = Pin(self.DIRECTION_Y_PIN, Pin.OUT)
        self.step_y = Pin(self.STEP_Y_PIN, Pin.OUT)
        self.enable_y = Pin(self.ENABLE_Y_PIN, Pin.OUT)

        # Servo
        self.pen_servo = Servo(self.SERVO_PIN)
        self.pen_servo.off()
        self.pen_servo.write(45)
        self.pen_state = False
        
        # Limit switches
        self.limit_switch_x = Pin(self.LIMIT_SWITCH_X, Pin.IN)
        self.limit_switch_y = Pin(self.LIMIT_SWITCH_Y, Pin.IN)

        # Get robot ready for motion:
        self.enable()
        self.set_direction(self.direction_x, 0) # - X
        self.set_direction(self.direction_y, 1) # - Y



    def zero_X(self):
        """This method sets loc_x to 0. This method should not be called by the user in their scripts."""
        self.loc_x=0.0
    
    def zero_Y(self):
        """This method sets loc_y to 0. This method should not be called by the user in their scripts."""
        self.loc_y=0.0

    def is_robot_zero(self):
        """
        Evaluates whether both loc_x and loc_y have been zeroed. This method should not be called by the user in their scripts.

        This method is only called at startup (ie. when the robot is zeroed at first), and once is_zero is set to True, is treated as a final variable.
        This method checks if loc_x, loc_y, and pen_zero are zeroed, and sets is_zero to this value. This is valuable so that no automated instructions are carried out
        before the robot is zeroed.

        Returns:
            bool: is_zero

        """
        if not self.is_zero:
            self.is_zero = (self.loc_x,self.loc_y) == (0.0,0.0)
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
        self.enabled = True

    def disable(self):
        """
        Used at the termination of a program, or called by the user in the case of an E-Stop
        """
        self.enable_x.value(1)
        self.enable_y.value(1)
        self.pen_up()
        self.enabled = False

    def set_direction(self, direction_pin: Pin, value: int):
        """
        Sets a pin to a given value, either 0 or 1
        """
        if(value not in [0,1]):
            raise ValueError("Incorrect arguments for set_direction(" + direction_pin)
        else:
            direction_pin.value(value)
      
    def pen_up(self):
        """
        This method moves or keeps the pen up.
        """
        if self.pen_state: # true = pen down
            self.pen_servo.write(45)
        self.pen_state = False


    def pen_down(self):
        """
        This method moves or keeps the pen down.
        """
        if not self.pen_state: # if pen is up
            self.pen_servo.off()
        self.pen_state = True
    
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

        dx = x - self.loc_x
        dy = y - self.loc_y
        total_distance = (dx**2 + dy**2)**0.5

        error_x = 0
        error_y = 0


        while total_distance > self.ACCEPTABLE_ERROR:
            # Handle all direction switches

            if(x > self.loc_x):
                self.set_direction(self.direction_x, 1)
            if(x < self.loc_x):
                self.set_direction(self.direction_x, 0)
            if(y > self.loc_y):
                self.set_direction(self.direction_y, 0)
            if(y < self.loc_y):
                self.set_direction(self.direction_y, 1)

            # Calculate step increments proportional to the slope
            raw_step_dx = abs(self.DISTANCE_PER_STEP * (dx / total_distance))
            raw_step_dy = abs(self.DISTANCE_PER_STEP * (dy / total_distance))

            raw_step_dx += error_x
            raw_step_dy += error_y


            # Round steps to the nearest step_size for stepper motor precision
            step_dx = round(raw_step_dx / self.DISTANCE_PER_STEP) * self.DISTANCE_PER_STEP
            step_dy = round(raw_step_dy / self.DISTANCE_PER_STEP) * self.DISTANCE_PER_STEP

            error_x = raw_step_dx - step_dx
            error_y = raw_step_dy - step_dy

            # Update the current position
            for _ in range(round(step_dx/self.DISTANCE_PER_STEP)):
                self.step_one_X()
                self.update_loc_x()
                # for testing
                #print("X :" + str(self.loc_x) + ", " + "Y: " + str(self.loc_y))
            for _ in range(round(step_dy/self.DISTANCE_PER_STEP)):
                self.step_one_y()
                self.update_loc_y()
                # for testing
                #print("X :" + str(self.loc_x) + ", " + "Y: " + str(self.loc_y))
            

            # Update remaining distance
            dx = x - self.loc_x
            dy = y - self.loc_y
            total_distance = (dx**2 + dy**2)**0.5



    def teleop(self, button_id: int, steps: int):
        """
        This method allows users to manually control and move the robot a user-specified number of steps in a certain direction.
        
        Args:
            button_id (int): The button_id clicked in the UI
            steps (int): The desired number of steps

        Returns:
            None
        """

        if button_id == self.HTML_BUTTON_UP: # + Y
            self.set_direction(self.direction_y, 0)
            for _ in range(steps):
                self.step_one_y()
                self.update_loc_y()

        if button_id == self.HTML_BUTTON_DOWN: # - Y
            self.set_direction(self.direction_y, 1)
            for _ in range(steps):
                if(not self.check_y_lim_switch):
                    self.zero_Y()
                    break
                self.step_one_y()
                self.update_loc_y()

        if button_id == self.HTML_BUTTON_LEFT: # - X
            self.set_direction(self.direction_x, 0)
            for _ in range(steps):
                if(not self.check_x_lim_switch):
                    self.zero_X()
                    break
                self.step_one_X()
                self.update_loc_x()
                
        if button_id == self.HTML_BUTTON_RIGHT: # + X
            self.set_direction(self.direction_x, 1)
            for _ in range(steps):
                self.step_one_X()
                self.update_loc_x()

        self.is_robot_zero()


    def auto_zero(self):
        """
        This method automatically zeros the robot X and Y axis. 
        
        Can be selected by the user in the Robot interface if manual zeroing is not preferred.

        Args:
            None

        Returns:
            None


        """
        self.set_direction(self.direction_x,0)
        self.set_direction(self.direction_y,1)

        while self.check_x_lim_switch():
            self.step_one_X()
        while self.check_y_lim_switch():
            self.step_one_y()

        self.zero_X()
        self.zero_Y()
        self.is_robot_zero()

    
    
    
    def step_one_X(self):
        """
        This method moves the bot one step in the X direction.

        Args:
            None

        Returns:
            None
        """
        for i in range(8):
            self.step_x.value(1)
            utime.sleep(self.STEPPER_DELAY)
            self.step_x.value(0)
            utime.sleep(self.STEPPER_DELAY)
    
    def step_one_y(self):
        """
        This method moves the bot one step in the Y direction.

        Args:
            None

        Returns:
            None
        """
        for i in range(8):
            self.step_y.value(1)
            utime.sleep(self.STEPPER_DELAY)
            self.step_y.value(0)
            utime.sleep(self.STEPPER_DELAY)

        
    def update_loc_x(self):
        """
        This method updates the X location of the robot based on the direction.

        Args:
            Direction(clockwise or counter-clockwise)

        Returns:
            None
        """
        
        if self.direction_x.value() == 1:
            self.loc_x += self.DISTANCE_PER_STEP 
        elif self.direction_x.value() == 0:
            self.loc_x -= self.DISTANCE_PER_STEP
            
            
    
    def update_loc_y(self):
        """
        This method updates the Y location of the robot based on the direction.

        Args:
            Direction (clockwise or counter-clockwise)

        Returns:
            None
        """

        if self.direction_y.value() == 1:
            self.loc_y -= self.DISTANCE_PER_STEP
        elif self.direction_y.value() == 0:
            self.loc_y += self.DISTANCE_PER_STEP
            


    def get_status(self):
        return {"loc_x": self.loc_x, "loc_y": self.loc_y, "pen_status": self.pen_state, "enable": self.enabled}
    
    
    # TODO: Think about error raising and how that'll work for the user.
    def raise_error(message, error_type):
        pass

    def check_x_lim_switch(self):
        """
        Returns the status of the x limit switch.

        True = Open
        False = Closed
        """
        return self.limit_switch_x.value() == 1
    
    def check_y_lim_switch(self):
        """
        Returns the status of the y limit switch.

        True = Open
        False = Closed
        """
        return self.limit_switch_y.value() == 1







