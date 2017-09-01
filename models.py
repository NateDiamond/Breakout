# models.py
# Nathaniel Diamond (ncd27) and Meredith Anderer (mra85)
# 12/4/16
"""Models module for Breakout

This module contains the model classes for the Breakout game. That is anything that you
interact with on the screen is model: the paddle, the ball, and any of the bricks.

Technically, just because something is a model does not mean there has to be a special 
class for it.  Unless you need something special, both paddle and individual bricks could
just be instances of GRectangle.  However, we do need something special: collision 
detection.  That is why we have custom classes.

You are free to add new models to this module.  You may wish to do this when you add
new features to your game.  If you are unsure about whether to make a new class or 
not, please ask on Piazza."""
import random # To randomly generate the ball velocity
from constants import *
from game2d import *


# PRIMARY RULE: Models are not allowed to access anything except the module constants.py.
# If you need extra information from Play, then it should be a parameter in your method, 
# and Play should pass it as a argument when it calls the method.


class Paddle(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball, as well as move it
    left and right.  You may wish to add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO CREATE A NEW PADDLE
    def __init__(self,x,y):
        """Initializer for Paddle class
        
        Parameter x: Starting x for the paddle
        Precondition: x must be a float or an int
        
        Parameter y: Starting y for the paddle
        Precondition: y must be a float or an int"""
        
        GRectangle.__init__(self, x=x, y=y, width = PADDLE_WIDTH,
                            height = PADDLE_HEIGHT,
                            fillcolor = colormodel.BLACK)
        
    # METHODS TO MOVE THE PADDLE AND CHECK FOR COLLISIONS
    def collides(self,ball):
        """Returns: True if the ball collides with the paddle
        Note that top of the ball is not checked because ball cannot bounce
        from underneath the paddle.
        
        Parameter ball: The ball to check
        Precondition: ball is of class Ball"""
        r = BALL_DIAMETER/2.0
        a = self.contains(ball.x-r, ball.y-r)
        b = self.contains(ball.x+r, ball.y-r)
        c = self.contains(ball.x-r, ball.y+r)
        d = self.contains(ball.x+r, ball.y+r)
        
        return (a or b or c or d) and ball.isMovingDown() 
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Brick(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball.  You may wish to 
    add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO CREATE A BRICK
    def __init__(self, x, y, color):
        """Initializer for class Brick.
        
        Parameter x: x coordinate of brick's center.
        Precondition: x must be an int or a float.
        
        Parameter y: y coordinate of brick's center.
        Precondition: y must be an int or a float.
        
        Parameter color: color of the brick
        Precondition: Must be an RGB or HSV color from colormodel
                      or a four element list of floats between 0 and 1."""              
        GRectangle.__init__(self,x=x,y=y,width = BRICK_WIDTH,
                          height = BRICK_HEIGHT,fillcolor = color)

    # METHOD TO CHECK FOR COLLISION
    def collides(self,ball):
        """Returns: True if the ball collides with this brick
        Parameter ball: The ball to check
        Precondition: ball is of class Ball"""
        r = BALL_DIAMETER/2.0
        a = self.contains(ball.x-r, ball.y-r)
        b = self.contains(ball.x+r, ball.y-r)
        c = self.contains(ball.x-r, ball.y+r)
        d = self.contains(ball.x+r, ball.y+r)
        
        return a or b or c or d
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse because a ball must have additional attributes for velocity.
    This class adds this attributes and manages them.
    
    INSTANCE ATTRIBUTES:
        _vx [int or float]: Velocity in x direction 
        _vy [int or float]: Velocity in y direction 
    
    The class Play will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.
    
    How? The only time the ball can change velocities is if it hits an obstacle
    (paddle or brick) or if it hits a wall.  Why not just write methods for these
    instead of using setters?  This cuts down on the amount of code in Gameplay.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO SET RANDOM VELOCITY
    def __init__(self):
        """Initializer for the Ball class."""
        
        GEllipse.__init__(self, x = GAME_WIDTH/2.0, y = GAME_HEIGHT/2.0,
                 width = BALL_DIAMETER, height = BALL_DIAMETER,
                 fillcolor = colormodel.BLACK)
        
        #The following three lines are suggestions taken from the
        #assignment outline.
        self._vy = -5.0
        self._vx = random.uniform(1.0,5.0)
        self._vx = self._vx *random.choice([-1,1])
        
    # METHODS TO MOVE AND/OR BOUNCE THE BALL
    def moveBall(self, time):
        """Moves the ball in the direction it is heading based on its
        speed and the time it has moved for.
        
        Parameter time: The amount of time for which the ball has moved.
        Precondition: time is a float or an int and time >= 0."""
        self.x += time * self._vx
        self.y += time * self._vy
        
    def vertBounce(self):
        """Flips the sign of the ball's y-velocity in order to bounce
        it vertically."""
        self._vy = -self._vy
        
    def horBounce(self):
        """Flips the sign of the ball's x-velocity so as to bounce it
        horizontally."""
        self._vx = -self._vx
        
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def isMovingDown(self):
        """Returns: True if the ball is moving downward (i.e., self._vy < 0)"""
        return self._vy<0
   
    def isMovingRight(self):
        """Returns: True if the ball is moving downward (i.e, self._vx > 0)"""
        return self._vx > 0
    
    def kick(self, kickFactor):
        """Speeds the ball up by a factor of kickFactor.
        
        Parameter kickFactor: factor by which the ball is sped up at the kick
        Precondition: kickFactor is an int or float > 1"""
        self._vx *= kickFactor
    
# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE