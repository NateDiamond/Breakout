# play.py
# Nathaniel Diamond (ncd27) and Meredith Anderer (mra85)
# 12/4/16
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout App. 
Instances of Play represent a single game.  If you want to restart a new game, you are 
expected to make a new instance of Play.

The subcontroller Play manages the paddle, ball, and bricks.  These are model objects.  
Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer."""
from constants import *
from game2d import *
from models import *


# PRIMARY RULE: Play can only access attributes in models.py via getters/setters
# Play is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)

class Play(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It animates the 
    ball, removing any bricks as necessary.  When the game is won, it stops animating.  
    You should create a NEW instance of Play (in Breakout) if you want to make a new game.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 25 for an example.
    
    INSTANCE ATTRIBUTES:
        _paddle [Paddle]: the paddle to play with 
        _bricks [list of Brick]: the list of bricks still remaining 
        _ball   [Ball, or None if waiting for a serve]:  the ball to animate
        _tries  [int >= 0]: the number of tries left 
    
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Breakout. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Breakout.  Only add the getters and setters that you need for 
    Breakout.
    
    You may change any of the attributes above as you see fit. For example, you may want
    to add new objects on the screen (e.g power-ups).  If you make changes, please list
    the changes with the invariants.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    Attribute _ballReleased:    [boolean] indicating whether
                                or not serveBall() has been called yet.
    Attribute _paddleDirection: [int] representing the
                                direction the paddle is heading
                                (see constants).
    Attribute _leftPressed:     [boolean] that indicates whether or not
                                the left arrow key was previously held down.
    Attribute _rightPressed:    [boolean] indicating whether or not the
                                right arrow key was previously held down.
    Attribute _paddleSound:     [Immutable instance of Sound] object that plays
                                when the ball hits the paddle.
    Attribute _soundOn:         [boolean] indicating whether the sound is on
                                or not.
    Attribute _breakSound1:     [Immutable instance of Sound] First breaking
                                sound to play when a ball hits a brick.
    Attribute _breakSound2:     [Immutable instance of Sound] Second breaking
                                sound to play when a ball hits a brick.
    Attribute _serveBallSound:  [Immutable instance of Sound] Whenever the ball
                                is served this plays.
    Attrbute _kickCounter:      [int] Counts the number of times the paddle
                                collides with the ball either since the
                                beginning of the game or since the last kick
                                to figure out when the ball should be
                                kicked."""
    
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getBallReleased(self):
        """Getter for attribute _ballReleased"""
        return self._ballReleased
    
    def noBricks(self):
        """Returns: True if there are no bricks left in this Play instance"""
        return len(self._bricks) == 0
    
    def getTries(self):
        """Returns the number of tries the Play instance has left."""
        return self._tries
    
    def hasBall(self):
        """Returns: True if the Play instance has a ball currently in play."""
        return self._ball is not None
    
    def getSoundOn(self):
        """Returns: True if the Play instance has the sound on."""
        return self._soundOn
    
    # INITIALIZER (standard form) TO CREATE PADDLES AND BRICKS
    def __init__(self):
        """Initializer for the class Play"""
        self._bricks = []
        #xStart and yStart are the center coordinates of the top left brick
        xStart = BRICK_SEP_H/2.0 + BRICK_WIDTH/2 #FIX THIS (LOOK AT CONSTANTS)
        yStart = GAME_HEIGHT - BRICK_Y_OFFSET - BRICK_HEIGHT/2.0
        
        #vertical and horizontal increments defined below
        dx = BRICK_WIDTH + BRICK_SEP_H
        dy = BRICK_HEIGHT + BRICK_SEP_V
        for r in range(BRICK_ROWS):
            for c in range(BRICKS_IN_ROW):
                self._bricks.append(Brick(xStart + c*dx,yStart - r*dy,
                                          BRICK_COLORS[(r/2)%5]))
        
        self._paddle = Paddle(GAME_WIDTH/2.0,PADDLE_OFFSET + PADDLE_HEIGHT/2.0)
        self._ballReleased = False
        self._paddleDirection = PADDLE_STILL
        #booleans that keep track of whether the left or right key was pressed
        #for the sake of ameliorating paddle movement
        self._leftPressed = False
        self._rightPressed = False
        self._tries = 3
        
        #Initialization of sound
        self._soundOn = True
        self._paddleSound = Sound('Blip_Select16.wav')
        #This sound is free to used and was offered up by Damaged Panda on
        #opengameart.org
        self._breakSound1 = Sound('saucer1.wav')
        self._breakSound2 = Sound('saucer2.wav')
        self._serveBallSound = Sound('bounce.wav')      
                
    # UPDATE METHODS TO MOVE PADDLE, SERVE AND MOVE THE BALL
    def updatePaddle(self, input):
        """Updates the paddle's location.
        
        Parameter input: last keyboard input given
        Precondition: input is None or a valid GInput"""
        buffer = PADDLE_SPEED + PADDLE_WIDTH/2.0
        
        if input != None:
            if (input.is_key_down('right') and input.is_key_down('left')):
                if not self._rightPressed:
                    self._paddleDirection = PADDLE_RIGHT
                    self._rightPressed = True
                elif not self._leftPressed:
                    self._paddleDirection = PADDLE_LEFT
                    self._leftPressed = True
            else:
                if input.is_key_down('right'):
                    self._paddleDirection = PADDLE_RIGHT
                    self._rightPressed = True
                    self._leftPressed = False
                elif input.is_key_down('left'):
                    self._paddleDirection = PADDLE_LEFT
                    self._leftPressed = True
                    self._rightPressed = False
                else:
                    self._paddleDirection = PADDLE_STILL
                    self._leftPressed = False
                    self._rightPressed = False
        
        if (self._paddleDirection == PADDLE_RIGHT
            and self._paddle.x <= GAME_WIDTH - buffer):
            self._paddle.x += PADDLE_SPEED
        elif (self._paddleDirection == PADDLE_LEFT
              and self._paddle.x >= buffer):
            self._paddle.x -= PADDLE_SPEED
                
                
    def serveBall(self):
        """Creates the ball and changes attribute _ballReleased to True.
        Also, if the sound is on it will play the serveBallSound.
        Attribute kickCounter is initialized or reset."""
        self._ball = Ball()
        self._ballReleased = True
        if self.getSoundOn():
            self._serveBallSound.play()
        self._kickCounter = 0
        
    def updateBall(self, time):
        """Updates the ball's location by moving it based on the time
        ellapsed during the move.  It also checks for collisions so as
        to change the ball's direction for future calls to updateBall.
        
        Parameter time: Amount of time for which the ball has moved.
        Precondition: time is a float or an int and time >= 0."""
        #move the ball
        self._ball.moveBall(time)
        
        #check for collisions
        self._collisionHelper()
        self._wallCollision()
        
    # DRAW METHOD TO DRAW THE PADDLES, BALL, AND BRICKS
    def draw(self, view):
        """Draws the paddles, ball, and bricks onto the given view.
        
        Parameter view: view to be drawn onto
        Precondition: view is a valid view of a GameApp instance."""
        for b in self._bricks:
            b.draw(view)
        self._paddle.draw(view)
        
        if self.getBallReleased():
            if self._ball is not None:
                self._ball.draw(view)
    
    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    def _collisionHelper(self):
        """Helper method to update ball that checks for collisions
        and bounces the ball as necessary."""
        for b in self._bricks:
            if b.collides(self._ball):
                self._ball.vertBounce()
                self._bricks.remove(b)
                if self.getSoundOn():
                    option = random.choice([0,1])
                    if option == 0:
                        self._breakSound1.play()
                    else:
                        self._breakSound2.play()
                break
        if self._paddle.collides(self._ball):
            if (self._ball.x <= self._paddle.left + PADDLE_WIDTH/4.0
                and self._ball.isMovingRight()):
                    self._ball.horBounce()
            elif (self._ball.x >= self._paddle.right - PADDLE_WIDTH/4.0
                  and not self._ball.isMovingRight()):
                    self._ball.horBounce()
            if self.getSoundOn():
                self._paddleSound.play()
            self._ball.vertBounce()
            self._updateKicker()
                  
    def _wallCollision(self):
        """Helper method that changes the direction of the ball if it hits
        the left, right or top wall, and makes the appropriate changes if the
        ball reaches the bottom wall and disappears from view, going out of play
        (a life is then lost)."""
        #checks if ball hits top wall and bounces it down
        if self._ball.top >= GAME_HEIGHT:
            self._ball.vertBounce()
        #checks if ball has reached bottom and 
        if self._ball.top <= 0:
            self._ball = None
            self._tries -= 1
            self._ballReleased = False
            return
        #checks if ball has reached left and bounces it right
        if self._ball.left <= 0:
            self._ball.horBounce()
        #checks if ball has reached right and bounces it left
        if self._ball.right >= GAME_WIDTH:
            self._ball.horBounce()
        
    
    # ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED) HERE
    def switchSound(self):
        """Makes self._soundOn the opposite boolean of what it is."""
        self._soundOn = not self._soundOn
        
    def _updateKicker(self):
        """Updates the kicker counter by one and checks
        if the ball should be sped up"""
        self._kickCounter += 1
        if self._kickCounter >= KICK_INTERVAL:
            self._ball.kick(KICK_FACTOR)
            self._kickCounter = 0
        