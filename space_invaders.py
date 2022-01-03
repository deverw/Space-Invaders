from sense_hat import SenseHat, ACTION_RELEASED
from time import sleep
from random import random

# Color definitions
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
WHITE=(255,255,255)

# Game parameters
SPEED=10.0              # Frames per second (=speed of bullets)
BULLET_LIMIT=2          # Maximum number of concurrent bullets
INVADER_IDLENESS=2      # Bullet steps per invader step
INVADER_DENSITY=0.15    # Probability of new invaders

def clamp(value, min_value=0, max_value=7):
    return min(max_value, max(min_value, value))

class Game:
    def __init__(self):
        self.score=0
        self.alive=True
        self.tick=0
        self.base=self.Base(3)
        self.invaders=[]

    def action(self):
        # handle invaders
        if (self.tick%INVADER_IDLENESS)==0:
            # create invaders
            if random()>0.8:
                self.invaders.append(self.Invader(0,0))
            for i in self.invaders:
                i.move()
                # Game over if invader reaches bottom line
                if i.y>6:
                    self.alive=False    

        # handle bullets
        for b in self.base.bullets:
            b.move()
            # check for hit invaders
            for i in self.invaders:
                if (b.x==i.x) and (b.y==i.y):
                    b.explode()
                    self.invaders.remove(i)
                    self.base.bullets.remove(b)
                    self.score+=1
            # remove missed bullets
            if b.y<0:
                self.base.bullets.remove(b)
        self.refresh_display()
    
    def refresh_display(self):
        hat.clear()
        self.base.display()
        for i in self.invaders:
            i.display()
        for b in self.base.bullets:
            b.display()
    
    def over(self):
        hat.stick.direction_any = self.base.fire        # don't disturb message display after game over
        hat.show_message("Game Over!", text_colour=RED)
        hat.show_message("Score: %s" % self.score, text_colour=GREEN)

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
                self.y=6
    
            def move(self):
                self.y-=1

            def display(self):
                hat.set_pixel(self.x, self.y, BLUE)
            
            def explode(self):
                hat.set_pixel(self.x, self.y, WHITE)
                sleep(1/SPEED)

    class Invader:
        def __init__(self,x,y):
            self.x=x
            self.y=y
            self.direction=1
            self.alive=True

        def move(self):
            # move back and forth, get lower after each line
            self.x+=self.direction
            if (self.x>7) or (self.x<0):
                self.y+=1
                self.x-=self.direction
                self.direction*=-1

        def display(self):
            hat.set_pixel(self.x, self.y, RED)


# create objects
hat = SenseHat()
game=Game()

# configure joystick
hat.stick.direction_left = game.base.move_left
hat.stick.direction_right = game.base.move_right
hat.stick.direction_middle = game.base.fire
hat.stick.direction_any = game.refresh_display

# game loop
while (game.alive):
    game.action()
    sleep(1/SPEED)
    game.tick+=1
game.over()