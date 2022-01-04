# Space Invaders

This is a game for Raspberry Pi with a Sense Hat extension, implemented in Python.
Invaders (red dots) enter your space, drop bombs (yellow dots) and move their way towards your base (green dot). You can move your base left and right and shoot at invaders using the joystick. Bombs cannot be eliminated, so you have to avoid them by moving.
Make sure you don't get hit by a bomb and no invader reaches the surface of your planet!

Execution:<br>
<code>
python space-invaders.py
</code>
  
You can change the difficulty of the game by adjusting the following parameters in the Python script:
<pre><code>
SPEED=10.0              # Frames per second (=speed of bullets)
BULLET_LIMIT=3          # Maximum number of concurrent bullets
INVADER_IDLENESS=2      # Bullet steps per invader step
INVADER_DENSITY=0.15    # Probability of new invaders per step
BOMB_DENSITY=0.05       # Probability of dropped bombs per invader per step
</code></pre>
