import pygame
from geese.app import App, Processor

class Ent:
    def entity(self):
        return (self,)

class Position:
    def __init__(self, x, y):
        self.x: float = x
        self.y: float = y

class Square(Ent):
    def __init__(self, pos: Position, file):
        self.pos = pos
        self.sprite = pygame.image.load(file)

    def rect_pair(self):
        return (self.sprite, self.sprite.get_rect().move(self.pos.x, self.pos.y))
    

class MoveSquares(Processor):
    def process(self, *args, **kwargs):
        for ent, (square,) in self.world.get_components(Square):
            square.pos.x += 0.01

class DrawSquare(Processor):
    def process(self, *args, **kwargs):
        for ent, (screen,) in self.world.get_components(pygame.Surface):
            screen.fill((255, 0, 0))
            for ent, (square,) in self.world.get_components(Square):
                screen.blit(*square.rect_pair())
            pygame.display.flip()

app = App()
app._components[1] = Square(
    Position(0, 0),
    "New Piskel.png"
).entity()
app._components[2] = Square(
    Position(0, 40),
    "New Piskel.png"
).entity()
app._components[3] = (pygame.display.set_mode((400, 400)),)
app.add_processor(MoveSquares())
app.add_processor(DrawSquare())
app.loop_process()
pygame.draw.rect(
    app._components[3],
    (0, 255, 0),
    (20, 20, 20, 20)
)
