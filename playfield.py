import pygame, os, random

LEFT_MARGIN = 8
TOP_MARGIN = 8
NUM_ROWS = 20
NUM_COLLUMNS = 10
BLOCK_SIZE = 34

COLORS = ["blue", "green", "red", "violet", "yellow"]


def grid_to_pixel(x, y):
    return (LEFT_MARGIN + x * BLOCK_SIZE, TOP_MARGIN + y * BLOCK_SIZE)

def pixel_to_grid(x, y):
    return ((x - LEFT_MARGIN) / BLOCK_SIZE, (y - TOP_MARGIN) / BLOCK_SIZE)

class Block(pygame.sprite.Sprite):
    def __init__(self, color, x = 0, y = 0):
        super().__init__()

        self.color = color
        self.surf = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.rect = self.surf.get_rect().move(x, y)
        
    
    def move(self, x, y):
        self.rect = self.rect.move(x, y)


class Grid(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        # This creates a grid of NUM_ROWS by NUM_COLLUMNS
        self.grid = [[None for i in range(NUM_ROWS)] for i in range(NUM_COLLUMNS)]
    
    def add_to_grid(self, block, pos_x, pos_y):
        x, y = grid_to_pixel(pos_x, pos_y)
        block.move(x, y)
        self.add(block)
        self.grid[pos_x][pos_y] = block
    
    def rem_from_grid(self, pos_x, pos_y):
        block = self.grid[pos_x][pos_y]
        self.remove(block)
        self.grid[pos_x][pos_y] = None


class Playfield():
    def __init__(self, screen, images_dict):
        self.screen = screen
        self.blocks = Grid()
        self.colors = COLORS
        self.block_images = images_dict
    
    def update(self):
        for s in self.blocks:
            # gravity
            #s.move(0, 1)
            pass
    
    def draw(self):
        self.screen.fill("black")
        for s in self.blocks:
            self.screen.blit(self.block_images[s.color], s.rect)

    def add_block(self, grid_x, grid_y, color=None):
        if color is None:
            color = random.choice(self.colors)
        
        self.blocks.add_to_grid(Block(color), grid_x, grid_y)

    def fill_with_blocks(self):
        for x in range(0, NUM_COLLUMNS):
            for y in range(0, NUM_ROWS):
                self.add_block(x, y)

class Cursor(pygame.sprite.Group):
    def __init__(self, color = None, shape = None):
        super().__init__()
        self.pos = 5
        if color is not None:
            self.color = color
        else:
            self.color = random.choice(COLORS)
        if shape is not None:
            self.shape = shape
        else:
            self.shape = [[None, True, None],
                          [None, True, True],
                          [None, True, None]]
        
        self.make_cursor_blocks()


    def move(self, delta):
        self.pos += delta
        if self.pos < 0:
            self.pos = 0
        if self.pos > NUM_COLLUMNS:
            self.pos = NUM_COLLUMNS
    
    def make_cursor_blocks(self):
        for x in range(len(self.shape)):
            for y in range(len(self.shape[x])):
                if self.shape[x][y] is True:
                    block = Block(self.color)
                    pos_x, pos_y = grid_to_pixel(self.pos + x, y)
                    block.move(pos_x,pos_y)
                    self.shape[x][y] = block
                    self.add(block)

