"""
This file provides all necessary methods

"""

from machine import pin
import utime

class Bot:
    # create constant pins (all capitalized)
    # step, enable, direction for each 1 of the 2 stepper drivers and 1 for servo (output) 7
    # limited switches, one for x, one for y (input) 2

    


    def __init__(self):
        """
        The Bot class is instantiated in boot.py, and therefore init is called. It is assumed that the robot
        does not know its own position upon startup, and therefore will be required to zero in X, Y, and the Pen_Z directions before going anywhere.
        In order to zero the robot, a student will need to use the robot teleop interface.

        Parameters:
        None

        
        """
        self.is_zero = False
        self.loc_x = None
        self.loc_y = None


        self.pen_up = False

        



    def zero_X(self):
        """This method sets loc_x to 0."""
        self.loc_x=0
    
    def zero_Y(self):
        """This method sets loc_y to 0."""
        self.loc_y=0

    

    def zero_pen(self,abs_servo_val):
        pass


    def XY_zero(self):
        """
        This method checks if loc_x, loc_y, and pen_zero are zeroed, and sets is_zero to this value. This is valuable so that no automated instructions are carried out
        before the robot is zeroed.

        """
        self.is_zero = (self.loc_x,self.loc_y,self.pen_zero,self.pen_loc) == (0,0,True,0)




    def go_to():
        """
        This method takes in data from the HTML User interface, and moves the robot. It is primarily used for
        testing purposes and also for zeroing the robot at the beginning of the 
        """
        pass
    
    
    def pen_up():
        """
        This method moves or keeps the pen up.
        """

    
    def pen_up():
        """
        This method moves or keeps the pen down.
        """
