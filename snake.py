from enum import Enum
import random
import pygame
from geese.app import App, Processor

class Ent:
    def entity(self):
        return (self,)

class Timer:
    def __init__(self, stop=100.0):
        self.current = 0.0
        self.stop = stop

class UpdateTimer(Processor):
    def process(self, *args, **kwargs):
        for ent, (timer,) in self.world.get_components(Timer):
            if timer.current >= timer.stop:
                timer.current = 0.0
            timer.current += self.world._last_delta

class Position:
    def __init__(self, x, y):
        self.x: float = x
        self.y: float = y

class Direction(Enum):
    Left = "left"
    Right = "right"
    Up = "up"
    Down = "down"

class Square(Ent):
    def __init__(self, pos: Position, x, y):
        self.pos = pos
        self.width = x
        self.height = y
        self.direction = Direction.Right

    def rect_pair(self):
        return (self.sprite, self.sprite.get_rect().move(self.pos.x, self.pos.y))
    
class HandleInput(Processor):
    def process(self, *args, **kwargs):
        for ent, (square,) in self.world.get_components(Square):
            square.direction = self.set_snake_direction(square)

    def set_snake_direction(self, sq: Square):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    return Direction.Left
                    break
                elif event.key == pygame.K_RIGHT:
                    return Direction.Right
                    break
                elif event.key == pygame.K_DOWN:
                    return Direction.Down
                    break
                elif event.key == pygame.K_UP:
                    return Direction.Up
                    break
                else: 
                    return sq.direction
                    break
            else:
                return sq.direction
                break
        return sq.direction

class MoveSquares(Processor):
    def process(self, *args, **kwargs):
        for ent, (square,) in self.world.get_components(Square):
            if self.check_timer():
                print(square.direction)

                if square.direction == Direction.Left:
                    square.pos.x -= 22
                if square.direction == Direction.Right:
                    square.pos.x += 22
                if square.direction == Direction.Up:
                    square.pos.y -= 22
                if square.direction == Direction.Down:
                    square.pos.y += 22

    def check_timer(self):
        finished = False
        for ent, (timer,) in self.world.get_components(Timer):
            finished = (timer.stop == 500.0 
                and timer.current >= timer.stop)
        return finished


class DrawSquare(Processor):
    def process(self, *args, **kwargs):
        for ent, (screen,) in self.world.get_components(pygame.Surface):
            screen.fill((255, 0, 0))
            for ent, (square,) in self.world.get_components(Square):
                pygame.draw.rect(
                    screen,
                    (0,255,0),
                    (square.pos.x, square.pos.y, square.width, square.width)
                )

            pygame.display.flip()

app = App()
app._components[1] = Square(
    Position(0, 0),
    20,
    20
).entity()
app._components[2] = Square(
    Position(0, 40),
    0,
    0
).entity()
app._components[3] = (pygame.display.set_mode((400, 400)),)
app._components[4] = (Timer(stop=500.0),)
app.add_processor(MoveSquares())
app.add_processor(DrawSquare())
app.add_processor(UpdateTimer())
app.add_processor(HandleInput())
pygame.draw.rect(
    app._components[3][0],
    (0, 255, 0),
    (0, 0, 20, 20)
)
app.loop_process()
