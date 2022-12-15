# the `ball` module contains the `Ball` class for this tui pong game
# representation character is `o`
# the ball moves in a random direction at the start of the game
# direction is represented by a vector (x, y)
# the ball bounces off the walls and the paddles
# bouning off the wall negates the y value of the vector,
#   y_dir = (- y_dir)
# bouncing off the paddle negates the x value of the vector, and normalizes the y value in a way that the further the ball is from the center of the paddle, the more the y value is normalized
#   x_dir = (- x_dir)
#   y_dir = (y_dir * (y_pos - paddle_center) / (paddle_height / 2))*2
# if the ball's x position is less than 0, the left player scores
# if the ball's x position is greater than the width of the screen, the right player scores

import random
import math
from paddle import Paddle

class Ball:
    def __init__(self: 'Ball', pos: tuple(int, int), dir: tuple(int, int), char: str) -> None:
        self.pos = pos
        self.dir = dir
        self.char = char

    def move(self: 'Ball', width: int, height: int, left_paddle: 'Paddle', right_paddle: 'Paddle') -> None:
        # move the ball in the direction it is currently moving
        self.pos = (self.pos[0] + self.dir[0], self.pos[1] + self.dir[1])

        # bounce the ball off the walls
        if self.pos[1] <= 0 or self.pos[1] >= height:
            # negate the y value of the direction vector
            self.dir = (self.dir[0], -self.dir[1])
        
        # bounce the ball off the paddles/players on the left
        if self.pos[0] <= 0:
            # if catched by the left paddle
            if self.pos[1] >= left_paddle.pos[1] and self.pos[1] <= left_paddle.pos[1] + left_paddle.height:
                # negate the x value of the direction vector
                # normalize the y value of the direction vector
                self.dir = (-self.dir[0], \
                    self.dir[1] \
                        * (self.pos[1] - left_paddle.pos[1] - left_paddle.height / 2) \
                        / (left_paddle.height / 2) \
                        * 2)
            # if missed by the left paddle
            else:
                # reset
                self.reset(width, height)
                # send signal that the right player scored
                right_paddle.score += 1
                # wait for the player press 'c' to continue
                print('Press c to continue')


        # bounce the ball off the paddles/players on the right
        if self.pos[0] >= width:
            if self.pos[1] >= right_paddle.pos[1] and self.pos[1] <= right_paddle.pos[1] + right_paddle.height:
                self.dir = (-self.dir[0], self.dir[1] * (self.pos[1] - right_paddle.pos[1] - right_paddle.height / 2) / (right_paddle.height / 2) * 2)
            else:
                self.reset(width, height)
                left_paddle.score += 1
                print('Press c to continue')
            
    def start(self: 'Ball') -> None:
        # set the ball to be moving
        self.dir = (random.randint(-1, 1), random.randint(-1, 1))
        # set the ball to be moving in a random direction
        if self.dir[0] == 0:
            self.dir = (1, self.dir[1])
        if self.dir[1] == 0:
            self.dir = (self.dir[0], 1)
    
    def reset(self: 'Ball', width: int, height: int) -> None:
        # reset the ball to the center of the screen
        self.pos = (width // 2, height // 2)
        # set the ball to be at rest
        self.dir = (0, 0)

        