"""
This file provides all necessary methods

"""

class Bot:
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
        self.pen_zero = None
        self.pen_loc = None

    def zero_X(self):
        self.loc_x=0
    
    def zero_Y(self):
        self.loc_y=0

    
    def zero_pen(self,abs_servo_val):
        pass


    def XY_zero(self):
        """
        This method checks if loc_x, loc_y, and pen_zero are zeroed, and sets is_zero to this value. This is valuable so that no automated instructions are carried out
        before the robot is zeroed.

        """
        self.is_zero=(self.loc_x,self.loc_y,self.pen_zero,self.pen_loc) == (0,0,True,0)




    def teleop():
        """
        This method takes in data from the HTML User interface, and moves the robot. It is primarily used for
        testing purposes and also for zeroing the robot at the beginning of the 
        """
        pass

    