# 2-player game in this tui pong game, this contains the logic `Game` class

import random
import math
from ball import Ball
from paddle import Paddle
import curses

class Game:
    def __init__(self: 'Game', width: int, height: int, left_paddle: 'Paddle', right_paddle: 'Paddle', ball: 'Ball') -> None:
        self.width = width
        self.height = height
        self.left_paddle = left_paddle
        self.right_paddle = right_paddle
        self.ball = ball

    def reset(self: 'Game') -> None:
        self.left_paddle.reset(self.height)
        self.right_paddle.reset(self.height)
        self.ball.reset(self.width, self.height)


    def update(self: 'Game') -> None:
        self.ball.move(self.width, self.height, self.left_paddle, self.right_paddle)
        self.left_paddle.move(self.height, self.right_paddle.pos[1] - self.left_paddle.pos[1])
        self.right_paddle.move(self.height, self.left_paddle.pos[1] - self.right_paddle.pos[1])

    def draw(self: 'Game', screen: 'curses.window') -> None:
        screen.clear()
        for y_off in range(-self.left_paddle.height // 2, self.left_paddle.height // 2):
            screen.addch(self.left_paddle.pos[1] + y_off, self.left_paddle.pos[0], self.left_paddle.char)
        for y_off in range(-self.right_paddle.height // 2, self.right_paddle.height // 2):
            screen.addch(self.right_paddle.pos[1] + y_off, self.right_paddle.pos[0], self.right_paddle.char)
        screen.addstr(int(self.ball.pos[1]), int(self.ball.pos[0]), self.ball.char)
        screen.addstr(0, 0, 'Score: ' + str(self.left_paddle.score) + ' | ' + str(self.right_paddle.score))
        screen.refresh()

def main(screen: 'curses.window') -> None:
    curses.curs_set(0)
    screen.nodelay(True)
    screen.timeout(100)

    width = 80
    height = 24

    left_paddle = Paddle((1, height // 2), 5, '|')
    right_paddle = Paddle((width - 2, height // 2), 5, '|')
    ball = Ball((width // 2, height // 2), (0, 0), 'o')
    ball.start()
    game = Game(width, height, left_paddle, right_paddle, ball)

    while True:
        key = screen.getch()
        if key == ord('q'):
            break
        elif key == ord('r'):
            game.reset()
        elif key == ord('p'):
            ball.start()
        elif key == curses.KEY_UP:
            game.right_paddle.move(height, -1)
        elif key == curses.KEY_DOWN:
            game.right_paddle.move(height, 1)
        elif key == ord('w'):
            game.left_paddle.move(height, -1)
        elif key == ord('s'):
            game.left_paddle.move(height, 1)

        game.update()
        game.draw(screen)

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

try:
    # curses.wrapper(main)
    main(screen)
finally:
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()

if __name__ == '__main__':
    main()