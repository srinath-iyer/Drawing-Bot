# This file is now deprecated, and no longer being used for testing purposes. Please refer to bot.py in /esp-32-local.

"""
This file provides the test_bot class, is a simplified version of the bot class, and is used to test the bot class without needing to use the UI, since it is still in development.

"""

from machine import Pin
import utime

from servo import Servo


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

    ACCEPTABLE_ERROR = DISTANCE_PER_STEP

    ACCEPTABLE_ERROR_SQRD = 2*DISTANCE_PER_STEP**2 # One step allowed in each direction leads to total distance = step^2 + step^2 = 2*step^2

    # Conversion from inches to mm
    MAX_X_LOC = 8*25.4
    MAX_Y_LOC = 11.5*25.4

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
        
        #Limit switches
        self.limit_switch_x = Pin(self.LIMIT_SWITCH_X, Pin.IN)
        self.limit_switch_y = Pin(self.LIMIT_SWITCH_Y, Pin.IN)

        # Get robot ready for motion:
        self.enable()
        self.set_direction(self.direction_x, 1)
        self.set_direction(self.direction_y, 1)



    def zero_X(self):
        """This method sets loc_x to 0."""
        self.loc_x=0
    
    def zero_Y(self):
        """This method sets loc_y to 0."""
        self.loc_y=0

    def is_robot_zero(self):
        """
        Evaluates whether both loc_x and loc_y have been zeroed.

        This method is only called at startup (ie. when the robot is zeroed at first), and once is_zero is set to True, is treated as a final variable.
        This method checks if loc_x, loc_y, and pen_zero are zeroed, and sets is_zero to this value. This is valuable so that no automated instructions are carried out
        before the robot is zeroed.

        Returns:
            bool: is_zero

        """
        self.is_zero = (self.loc_x,self.loc_y) == (0,0)
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
            print("Incorrect arguments for set_direction(" + direction_pin)
        else:
            self.direction_pin.value(value)
      
    # TODO: Implement the logic for the method (if the Servo() object implementation works (see __init__ for more), then use the pertinent methods in here). 
    # This is entirely dependent on how you decide to control the servo and its protocols, so there's not much more I can say here.
    def pen_up(self):
        """
        This method moves or keeps the pen up.
        """
        if self.pen_state: # true = pen down
            self.pen_servo.write(45)
        self.pen_state = False





    # TODO: Implement the logic for the method (if the Servo() object implementation works (see __init__ for more), then use the pertinent methods in here). 
    # This is entirely dependent on how you decide to control the servo and its protocols, so there's not much more I can say here.
    def pen_down(self):
        """
        This method moves or keeps the pen down.
        """
        if not self.pen_state: # if pen is up
            self.pen_servo.off()
        self.pen_state = True
    
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
        
        dx = x - self.loc_x
        dy = y - self.loc_y
        total_distance = (dx**2 + dy**2)**0.5

        while dx**2 + dy**2 > self.ACCEPTABLE_ERROR_SQRD:
            # Calculate step increments proportional to the slope
            step_dx = self.DISTANCE_PER_STEP * (dx / total_distance)
            step_dy = self.DISTANCE_PER_STEP * (dy / total_distance)

            # Round steps to the nearest step_size for stepper motor precision
            step_dx = round(step_dx / self.DISTANCE_PER_STEP) * self.DISTANCE_PER_STEP
            step_dy = round(step_dy / self.DISTANCE_PER_STEP) * self.DISTANCE_PER_STEP

            # Update the current position
            for i in range(round(step_dx//self.DISTANCE_PER_STEP)):
                if(step_dx < -1):
                    self.set_direction(self.DIRECTION_X_PIN,(int)(not self.DIRECTION_X_PIN.value()))
                self.stepOne_X()
                self.update_loc_x()
            for i in range(round(step_dy//self.DISTANCE_PER_STEP)):
                if(step_dy < -1):
                    self.set_direction(self.DIRECTION_Y_PIN,(int)(not self.DIRECTION_Y_PIN.value()))
                self.stepOne_Y()
                self.update_loc_y()
            

            # Update remaining distance
            dx = x - self.loc_x
            dy = y - self.loc_x
            total_distance = (dx**2 + dy**2)**0.5



    def teleop(self, direction: int, steps: int):
        """
        This method allows users to manually control and move the robot a user-specified number of steps in a certain direction.
        
        Args:
            direction (int): The desired direction (x or y)
            steps (int): The desired number of steps

        Returns:
            None
        """
        pass

    # TODO: Implement this method. Not much more guidance here, you should develop the method and logic yourself. The hint is to use some sort of 
    # while looping.
    def auto_zero(self):
        """
        This method automatically zeros the robot X and Y axis. 
        
        Can be selected by the user in the Robot interface if manual zeroing is not preferred.

        Args:
            None

        Returns:
            None


        """

        # while limit switch X = low:
            # move towards direction of limit switch X

        # while limit switch Y = low:
            # move towards direction of limit switch Y


        #According to ChatGPT, limit switches send 0 when pressed (closed), and 1 when not pressed (open)
        #LIMIT_OPEN = 0
        while self.limit_switch_x == self.LIMIT_OPEN:
            self.stepOne_X(1) #move stepper X in direction of limit switch
        while self.limit_switch_y == self.LIMIT_OPEN:
            self.stepOne_Y(1) #move stepper Y in direction of limit switch

        self.zero_X()
        self.zero_Y()

    
    
    
    def stepOne_X(self):
        """
        This method moves the bot one step in the X direction.

        Args:
            None

        Returns:
            None
        """

        self.step_x.value(1) #Move step
        utime.sleep(self.STEPPER_DELAY)
        self.step_x.value(0)

    
    def stepOne_Y(self):
        """
        This method moves the bot one step in the Y direction.

        Args:
            None

        Returns:
            None
        """

        self.step_y.value(1) #Move step
        utime.sleep(self.STEPPER_DELAY)
        self.step_y.value(0)

        
    def update_loc_x(self): #update loc_x based on whether motor is moving clockwise/counter-clockwise
        """
        This method updates the X location of the robot based on the direction.

        Args:
            Direction(clockwise or counter-clockwise)

        Returns:
            None
        """
        #This stuff should be corrected later once we know whether direction_x == 1 means clockwise or counter
        if self.direction_x == 1:
            self.loc_x -= self.DISTANCE_PER_STEP 
        elif self.direction_x == 0:
            self.loc_x += self.DISTANCE_PER_STEP
            
    
    def update_loc_y(self): #update loc_y based on whether motor is moving clockwise/counter-clockwise
        """
        This method updates the Y location of the robot based on the direction.

        Args:
            Direction (clockwise or counter-clockwise)

        Returns:
            None
        """
        #This stuff should be corrected later once we know whether direction_y == 1 means clockwise or counter
        if self.direction_y == 1:
            self.loc_x -= self.DISTANCE_PER_STEP
        elif self.direction_y == 0:
            self.loc_x += self.DISTANCE_PER_STEP


    def get_status(self):
        return {"loc_x": self.loc_x, "loc_y": self.loc_y, "pen_status": self.pen_state, "enable": self.enabled}
    
    
    # TODO: Think about error raising and how that'll work for the user.
    def raise_error(message, error_type):
        pass






