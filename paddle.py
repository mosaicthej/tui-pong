# paddle module contains the `Paddle` class for this tui pong game
# representation character is `|`
# the paddle moves up and down
# the paddle can't move off the screen

import math

class Paddle:
    def __init__(self: 'Paddle', pos: tuple[int, int], height: int, char: str) -> None:
        self.pos = pos  # center of the paddle
        self.height = height
        self.char = char
        self.score = 0

    def move(self: 'Paddle', height: int, dir: int) -> None:
        self.pos = (self.pos[0], self.pos[1] + dir)
        if self.pos[1] < 0:
            self.pos = (self.pos[0], 0)
        if self.pos[1] + self.height > height:
            self.pos = (self.pos[0], height - self.height)

    def reset(self: 'Paddle', height: int) -> None:
        self.pos = (self.pos[0], height // 2)