from sense_hat import SenseHat, ACTION_RELEASED
from time import sleep
from random import random

# Color definitions
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW=(127,127,0)
WHITE=(255,255,255)
BLACK=(0,0,0)

# Game parameters
SPEED=10.0              # Frames per second (=speed of bullets)
BULLET_LIMIT=3          # Maximum number of concurrent bullets
INVADER_IDLENESS=2      # Bullet steps per invader step
INVADER_DENSITY=0.15    # Probability of new invaders per step
BOMB_DENSITY=0.05       # Probability of dropped bombs per invader per step

def clamp(value, min_value=0, max_value=7):
    return min(max_value, max(min_value, value))

def do_nothing(self):
    pass

class Game:
    def __init__(self):
        self.score=0
        self.alive=True
        self.tick=0
        self.base=self.Base(3)
        self.invaders=[]
        self.bombs=[]
        # configure joystick
        hat.stick.direction_left = self.base.move_left
        hat.stick.direction_right = self.base.move_right
        hat.stick.direction_middle = self.base.fire
        hat.stick.direction_any = self.refresh_display
    def action(self):
        # handle bullets
        for b in self.base.bullets:
            b.move()
            # remove used bullets
            if b.y<0 or b.hit:
                self.base.bullets.remove(b)
            # check for hit invaders
            for i in self.invaders:
                if (b.x==i.x) and (b.y==i.y):
                    b.hit=True
                    self.invaders.remove(i)
                    self.score+=1
        # handle invaders and bombs
        if not(self.tick%INVADER_IDLENESS):
            # create invaders
            if random()>1-INVADER_DENSITY:
                self.invaders.append(self.Invader(0,0))
            for i in self.invaders:
                # create bombs
                if random()>1-BOMB_DENSITY:
                    self.bombs.append(self.Bomb(i.x,i.y))
                i.move()
                # Game over if invader reaches bottom line
                if i.y>6:
                    self.deactivate_control()
                    self.alive=False   
                    i.invade()
            # drop bombs
            for o in self.bombs:
                o.move()
                # remove misguided bombs
                if o.y>7:
                    self.bombs.remove(o)
                # Game over if base is hit
                if (o.y==7) and (o.x==self.base.x):
                    self.deactivate_control()
                    self.alive=False
                    o.explode()
        self.refresh_display()
    def refresh_display(self):
        hat.clear()
        for b in self.base.bullets:
            b.display()
        for o in self.bombs:
            o.display()
        for i in self.invaders:
            i.display()
        self.base.display()
    def deactivate_control(self):
        # remove joystick calls
        hat.stick.direction_left = do_nothing
        hat.stick.direction_right = do_nothing
        hat.stick.direction_middle = do_nothing
        hat.stick.direction_any = do_nothing
    def over(self):
        hat.show_message("Game Over!", text_colour=RED)
        hat.show_message("Score: %s" % self.score, text_colour=GREEN)
        print("Score: %s" % self.score)

    class Base:
        def __init__(self,x):
            self.x=x
            self.bullets=[]
        def move_left(self, event):
            if event.action != ACTION_RELEASED:
                self.x=clamp(self.x-1)
        def move_right(self, event):
            if event.action != ACTION_RELEASED:
                self.x=clamp(self.x+1)
        def fire(self, event):
            if event.action != ACTION_RELEASED:
                if len(self.bullets)<BULLET_LIMIT:
                    self.bullets.append(self.Bullet(self.x))
        def display(self):
            hat.set_pixel(self.x, 7, GREEN)

        class Bullet:
            def __init__(self,x):
                self.x=x
                self.y=7
                self.hit=False   
            def move(self):
                self.y-=1
            def display(self):
                if self.hit:
                    hat.set_pixel(self.x, self.y, WHITE)
                else:
                    hat.set_pixel(self.x, self.y, BLUE)            

    class Invader:
        def __init__(self,x,y):
            self.x=x
            self.y=y
            self.direction=1
        def move(self):
            # move back and forth, get lower after each line
            self.x+=self.direction
            if (self.x>7) or (self.x<0):
                self.y+=1
                self.x-=self.direction
                self.direction*=-1
        def display(self):
            hat.set_pixel(self.x, self.y, RED)
        def invade(self):
            # fill bottom line
            for n in range(8):
                hat.set_pixel(7-n, 7, RED)
                sleep (INVADER_IDLENESS/SPEED)

    class Bomb:
        def __init__(self,x,y):
            self.x=x
            self.y=y
        def move(self):
            self.y+=1            
        def display(self):
            hat.set_pixel(self.x, self.y, YELLOW)
        def explode(self):
            # flash 3 times
            for n in range(3):
                hat.set_pixel(self.x, self.y, WHITE)
                sleep (INVADER_IDLENESS/SPEED)
                hat.set_pixel(self.x, self.y, BLACK)
                sleep (INVADER_IDLENESS/SPEED)

# create objects
hat=SenseHat()
game=Game()

# game loop
while (game.alive):
    game.action()
    sleep(1/SPEED)
    game.tick+=1
game.over()