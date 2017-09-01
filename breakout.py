# breakout.py
# Nathaniel Diamond (ncd27) and Meredith Anderer (mra85)
# 12/4/16
"""Primary module for Breakout application

This module contains the main controller class for the Breakout application. There is no
need for any any need for additional classes in this module.  If you need more classes, 
99% of the time they belong in either the play module or the models module. If you 
are unsure about where a new class should go, 
post a question on Piazza."""
from constants import *
from game2d import *
from play import *


# PRIMARY RULE: Breakout can only access attributes in play.py via getters/setters
# Breakout is NOT allowed to access anything in models.py

class Breakout(GameApp):
    """Instance is the primary controller for the Breakout App
    
    This class extends GameApp and implements the various methods necessary for processing 
    the player inputs and starting/running a game.
    
        Method start begins the application.
        
        Method update either changes the state or updates the Play object
        
        Method draw displays the Play object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Play.
    Play should have a minimum of two methods: updatePaddle(input) which moves
    the paddle, and updateBall() which moves the ball and processes all of the
    game physics. This class should simply call that method in update().
    
    The primary purpose of this class is managing the game state: when is the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
        view    [Immutable instance of GView; it is inherited from GameApp]:
                the game view, used in drawing (see examples from class)
        input   [Immutable instance of GInput; it is inherited from GameApp]:
                the user input, used to control the paddle and change state
        _state  [one of STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE]:
                the current state of the game represented a value from constants.py
        _game   [Play, or None if there is no game currently active]: 
                the controller for a single game, which manages the paddle, ball, and bricks
        _mssg   [GLabel, or None if there is no message to display]
                the currently active message
    
    STATE SPECIFIC INVARIANTS: 
        Attribute _game is only None if _state is STATE_INACTIVE.
        Attribute _mssg is only None if  _state is STATE_ACTIVE or STATE_COUNTDOWN.
    
    For a complete description of how the states work, see the specification for the
    method update().
    
    You may have more attributes if you wish (you might need an attribute to store
    any text messages you display on the screen). If you add new attributes, they
    need to be documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        Attribute _keyPressed:      [boolean] True if a key was held down
                                    during the last call to update and False
                                    otherwise.
        Attribute _gameClock:       [float] that keeps track of the time
                                    elapsed throughout the game starting at
                                    STATE_COUNTDOWN (doesn't add when game
                                    is paused).
        Attribute _lastReset:       [float] that keeps track of the last
                                    time a countdown was started.
        Attribute _mssg2:           [GLabel, or None if there is no secondary
                                    message to display] The currently active
                                    secondary message.
        Attribute _soundIcon:       [Immutable instance of GImage] Sound icon
                                    in the bottom left corner of the screen
                                    that when pressed turns the sound on or
                                    off.
        Attribute _noIcon           [Immutable instance of GImage] Icon that
                                    goes over the sound icon when the user
                                    turns off the sound.
        Attribute _mousePressed:    [boolean] indicating whether or not the
                                    mouse was pressed in the last call
                                    to update.
        Attribute _lifeCounter:     [GLabel] that says how many lives are
                                    left in the game.
        Attribute _soundOnLastGame: [boolean] that indicates whether
                                    the sound was on last game for
                                    the sake of continuity.
        Attribute _alphaIncreasing  [boolean] that keeps track of whether
                                    the alpha value is currently increasing
                                    or decreasing in the starting animation."""
                
    # DO NOT MAKE A NEW INITIALIZER!
    
    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """Initializes the application.
        
        This method is distinct from the built-in initializer __init__ (which you 
        should not override or change). This method is called once the game is running. 
        You should use it to initialize any game specific attributes.
        
        This method should make sure that all of the attributes satisfy the given 
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message 
        (in attribute _mssg) saying that the user should press to play a game."""
        self._state = STATE_INACTIVE
        self._game = None
        self._keyPressed = False
        self._mousePressed = False
        self._mssg = GLabel(text = "Press any key to start",
                            x = GAME_WIDTH/2, y = GAME_HEIGHT/2,
                            font_size = 30, font_name = "ComicSansBold.ttf",
                            linecolor = colormodel.BLACK)
        self._mssg2 = None
        
    def update(self,dt):
        """Animates a single frame in the game.
        
        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Play.  The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Play object _game to play the game.
        
        As part of the assignment, you are allowed to add your own states.  However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWGAME,
        STATE_COUNTDOWN, STATE_PAUSED, and STATE_ACTIVE.  Each one of these does its own
        thing, and so should have its own helper.  We describe these below.
        
        STATE_INACTIVE: This is the state when the application first opens.  It is a 
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen.
        
        STATE_NEWGAME: This is the state creates a new game and shows it on the screen.  
        This state only lasts one animation frame before switching to STATE_COUNTDOWN.
        
        STATE_COUNTDOWN: This is a 3 second countdown that lasts until the ball is 
        served.  The player can move the paddle during the countdown, but there is no
        ball on the screen.  Paddle movement is handled by the Play object.  Hence the
        Play class should have a method called updatePaddle()
        
        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        paddle and the ball moves on its own about the board.  Both of these
        should be handled by methods inside of class Play (NOT in this class).  Hence
        the Play class should have methods named updatePaddle() and updateBall().
        
        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.
        
        The rules for determining the current state are as follows.
        
        STATE_INACTIVE: This is the state at the beginning, and is the state so long
        as the player never presses a key.  In addition, the application switches to 
        this state if the previous state was STATE_ACTIVE and the game is over 
        (e.g. all balls are lost or no more bricks are on the screen).
        
        STATE_NEWGAME: The application switches to this state if the state was 
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        
        STATE_COUNTDOWN: The application switches to this state if the state was
        STATE_NEWGAME in the previous frame (so that state only lasts one frame).
        
        STATE_ACTIVE: The application switches to this state after it has spent 3
        seconds in the state STATE_COUNTDOWN.
        
        STATE_PAUSED: The application switches to this state if the state was 
        STATE_ACTIVE in the previous frame, the ball was lost, and there are still
        some tries remaining.
        
        You are allowed to add more states if you wish. Should you do so, you should 
        describe them here.
        
        STATE_COMPLETE: This state occurs when the user has either won
        or lost the game of breakout.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._determineState()
        
        if self._state != STATE_INACTIVE:   
            self._updateSound()
        
        if self._state == STATE_INACTIVE:
            self._inactive()
        
        if self._state == STATE_NEWGAME:
            self._newgame()
            
        #If the game is not inactive the game clock will always be updated.
        if self._state != STATE_INACTIVE:
            self._updateGameClock(dt)
        
        if self._state == STATE_COUNTDOWN:
            self._countdown()
                
        if self._state == STATE_ACTIVE:
            self._active()
        
        if self._state == STATE_COMPLETE:
            self._active() #keeps the paddle and the ball (if still there)
            #moving around the screen for fun
        
        #See if any keys are pressed each call of update.    
        self._keyPressed = self.input.key_count > 0
        #See if the mouse is pressed after each call of update.
        self._mousePressed = self.input.touch is not None
        
    def draw(self):
        """Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject.  To draw a GObject 
        g, simply use the method g.draw(self.view).  It is that easy!
        
        Many of the GObjects (such as the paddle, ball, and bricks) are attributes in Play. 
        In order to draw them, you either need to add getters for these attributes or you 
        need to add a draw method to class Play.  We suggest the latter.  See the example 
        subcontroller.py from class."""
        if self._mssg is not None:    
            self._mssg.draw(self.view)
            
        if self._mssg2 is not None:
            self._mssg2.draw(self.view)
        
        if not self._state == STATE_INACTIVE:
            #Sound on bottom left
            self._soundIcon.draw(self.view)
            if not self._game.getSoundOn():
                self._noIcon.draw(self.view)
            #draw the life counter
            self._lifeCounter.draw(self.view)
            #call the game's draw method
            self._game.draw(self._view)
               
    # HELPER METHODS FOR THE STATES GO HERE
    
    def _determineState(self):
        """Switches the state when this should be done.
        Called after every update."""
        if self._state == STATE_INACTIVE:
            if self.input.key_count > 0 and not self._keyPressed:
                self._switchToNewgame()
        elif self._state == STATE_NEWGAME:
            self._switchToCountdown()
        elif self._state == STATE_COUNTDOWN:
            if (self._countdownTimer() > 3
                and not self._game.getBallReleased()):
                self._switchToActive()
        elif self._state == STATE_ACTIVE:
            if not self._game.hasBall() and self._game.getTries() > 0:
                self._switchToPaused()
            elif not self._game.hasBall() or self._game.noBricks():
                self._gameOver()
        elif self._state == STATE_PAUSED:
            if self.input.key_count > 0 and not self._keyPressed:
                self._switchToCountdown()
        else: #if it's in STATE_COMPLETE
            if self.input.is_key_down('n') and not self._keyPressed:
                self._soundOnLastGame = self._game.getSoundOn()
                self._switchToNewgame()
    
    def _inactive(self):
        """Called when the breakout is in state inactive."""
        currentAlpha = self._mssg.linecolor[3]
        if currentAlpha <= A_INC: 
            self._alphaIncreasing = True
        elif currentAlpha >= 1-A_INC:
            self._alphaIncreasing = False
            
        if self._alphaIncreasing:
            self._mssg.linecolor = [0,0,0,currentAlpha + A_INC]
        else:
             self._mssg.linecolor = [0,0,0,currentAlpha - A_INC]
    
    def _switchToNewgame(self):
        """Switches the game into a new game. This method just changes
        the state.  Others like this might do other operations."""
        self._state = STATE_NEWGAME
        
    def _newgame(self):
        """Starts a new game by assigning a new Play object to
        self._game and switches the game state to countdown."""
        self._mssg = None
        self._game = Play()
        self._gameClock = 0
        self._lastReset = 0
        
        #If there was a game with the sound off last game it will
        #keep it off.
        try:
            if not self._soundOnLastGame:
                self._game.switchSound()
        except:
            pass
            #Catches the potential error
        
        #Both images taken from the public domain on pixabay.com
        self._soundIcon = GImage(source = 'Sound Icon.jpg', x = SOUND_DIM/2.0,
                                 y = SOUND_DIM/2.0, width = SOUND_DIM,
                                 height = SOUND_DIM)
        self._noIcon = GImage(source = 'No Icon.png', x = SOUND_DIM/2.0,
                                 y = SOUND_DIM/2.0, width = SOUND_DIM,
                                 height = SOUND_DIM)
        
        self._lifeCounter = GLabel(text = "Lives Remaining: 3",
                        x = GAME_WIDTH - 60, y = 12,
                        font_size = 13, font_name = "ComicSans.ttf",
                        linecolor = colormodel.BLACK)
        
    def _switchToCountdown(self):
        """Method that switches the game to STATE_COUNTDOWN"""
        self._clearMessage()
        self._lastReset = self._gameClock
        
        self._mssg2 = GLabel(text = str(int(4-self._countdownTimer())),
                        x = GAME_WIDTH/2, y = GAME_HEIGHT/2,
                        font_size = 24, font_name = "ComicSans.ttf",
                        linecolor = colormodel.BLUE)
        self._state = STATE_COUNTDOWN
    
    def _countdown(self):
        """Method that executes during the update method if the game is
        in the countdown state.  Moreover, it updates the paddle so the
        player can start moving it before the ball is released and it
        updates the countdown message if a second has passed since the
        last number was changed."""
        self._game.updatePaddle(self.input)
        if self._countdownTimer() <= 3:
            self._mssg2.text = str(int(4 - self._countdownTimer()))
            
    def _switchToActive(self):
        """Method that switches this breakout to STATE_ACTIVE.
        In doing so the secondary message is erased and the
        game has its ball served."""
        self._game.serveBall()
        self._mssg2 = None
        self._state = STATE_ACTIVE
        
    def _active(self):
        """Method that executes during the update method if the game
        is active.  It updates the ball and paddle."""
        self._game.updatePaddle(self.input)
        if self._game.hasBall():
            #updates the ball by the amount of time that has passed in the
            #game for one call to update
            self._game.updateBall(GAME_TIME)
                
    def _switchToPaused(self):
        """Method that executes at first when the state is paused.
        The game has the appropriate message created and the state is
        changed to STATE_PAUSED."""
        if self._game.getTries() == 2:
            self._mssg = GLabel(text = "Press any key to serve second ball",
                            x = GAME_WIDTH/2, y = GAME_HEIGHT/2,
                            font_size = 24, font_name = "ComicSans.ttf",
                            linecolor = colormodel.BLACK)
            self._lifeCounter.text = "Lives Remaining: 2"
        else:
            self._mssg = GLabel(text = "Press any key to serve last ball",
                            x = GAME_WIDTH/2, y = GAME_HEIGHT/2,
                            font_size = 24, font_name = "ComicSans.ttf",
                            linecolor = colormodel.BLACK)
            self._lifeCounter.text = "Lives Remaining: 1"
        self._state = STATE_PAUSED
    
    def _clearMessage(self):
        """Clears the current game message.
        Used as a helper to some methods that switch between states."""
        self._mssg = None
        
    def _countdownTimer(self):
        """Returns: a float that shows how much time has passed in
        the countdown progression (this is only called when the game
        is counting down)"""
        return self._gameClock - self._lastReset
        
    def _updateGameClock(self,dt):
        """Updates the game clock by the amount dt.
        
        Parameter dt: Amount to be added to the clock.
        Precondition: dt is an int or a float >=0."""
        self._gameClock += dt
        
    def _gameOver(self):
        """Called when the game is over.  It switches the state into
        STATE_COMPLETE and creates the proper message depending on
        whether the user won or lost."""
        self._state = STATE_COMPLETE
        if self._game.noBricks():
            self._mssg = GLabel(text = "Congratulations, you won!",
                            x = GAME_WIDTH/2, y = GAME_HEIGHT/2,
                            font_size = 30, font_name = "Arial.ttf",
                            linecolor = colormodel.BLACK)
        else:
            self._mssg = GLabel(text = "Game over",
                            x = GAME_WIDTH/2, y = GAME_HEIGHT/2,
                            font_size = 30, font_name = "Arial.ttf",
                            linecolor = colormodel.BLACK)
            self._lifeCounter.text = "Lives Remaining: 0"
        
        self._mssg2 = GLabel(text = "Press n to start a new game",
                            x = GAME_WIDTH/2, y = GAME_HEIGHT/2 - 30,
                            font_size = 16, font_name = "ComicSans.ttf",
                            linecolor = colormodel.DARK_GRAY)
        
    def _updateSound(self):
        """Checks to see if sound should be updated and does so."""
        mousePress = self.input.touch
        if mousePress is not None and not self._mousePressed:
            if self._soundIcon.contains(mousePress.x,mousePress.y):
                self._game.switchSound()