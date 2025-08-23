import pygame, random
from block import *

LEFT_MARGIN = 8
TOP_MARGIN = 8
NUM_ROWS = 20
NUM_COLLUMNS = 10
BLOCK_SIZE = 34

class Playfield():
    def __init__(self, screen):
        self.screen = screen
        self.blocks = pygame.sprite.Group()

        blue_block = pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "blue.png")))
        green_block = pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "green.png")))
        red_block = pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "red.png")))
        violet_block = pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "violet.png")))
        yellow_block = pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "yellow.png")))
        self.colors = ["blue", "green", "red", "violet", "yellow"]
        self.block_images = {"blue": blue_block, "green": green_block, "red": red_block, "violet": violet_block, "yellow": yellow_block}
        
    
    def update(self):
        for s in self.blocks:
            # gravity
            #s.move(0, 1)
            pass
    
    def draw(self):
        self.screen.fill("black")
        for s in self.blocks:
            self.screen.blit(s.surf, s.rect)

    def add_block(self, grid_x, grid_y,color=None):
        if color is None:
            color = random.choice(self.colors)
        
        x = LEFT_MARGIN + grid_x * BLOCK_SIZE
        y = TOP_MARGIN + grid_y * BLOCK_SIZE
        self.blocks.add(Block(color, self.block_images[color], x, y))

    def fill_with_blocks(self):
        for x in range(0, NUM_COLLUMNS):
            for y in range(0, NUM_ROWS):
                self.add_block(x, y)
