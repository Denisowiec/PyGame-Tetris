import pygame, os, random

LEFT_MARGIN = 8
TOP_MARGIN = 8
NUM_ROWS = 20
NUM_COLLUMNS = 10
BLOCK_SIZE = 34

COLORS = ["blue", "green", "red", "violet", "yellow"]
SHAPES = ["t", "i", "l", "invl", "s", "z"]


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
        self.rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)


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

        if shape not in SHAPES:
            shape = "t"

        match shape:
            case "t":
                self.shape = [[True, True, True],
                              [None, True, None]]
            case "i":
                self.shape = [[True, True, True, True]]
            case "l":
                self.shape = [[True, True, True],
                              [None, None, True]]
            case "invl":
                self.shape = [[True, True, True],
                              [True, None, None]]
            case "s":
                self.shape = [[None, True, True],
                              [True, True, None]]
            case "z":
                self.shape = [[True, True, None],
                              [None, True, True]]
                
        
        self.update_block_positions()
    
    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.move(-1)
        if keys[pygame.K_RIGHT]:
            self.move(1)
        if keys[pygame.K_UP]:
            self.rotate(True)

        self.update_block_positions()

    def update_block_positions(self):
        for y in range(len(self.shape)):
            for x in range(len(self.shape[y])):
                if self.shape[y][x] is True:
                    block =  Block(self.color)
                    self.shape[y][x] = block
                    self.add(block)
                if self.shape[y][x] is not None:
                    pos_x, pos_y = grid_to_pixel(self.pos + x, y)
                    self.shape[y][x].move(pos_x,pos_y)
        

    def move(self, delta):
        self.pos += delta
        if self.pos < 0:
            self.pos = 0
        
        # Right side movement is limited by the width if the currently held shape
        if self.pos + len(self.shape[0]) > NUM_COLLUMNS:
            self.pos = NUM_COLLUMNS - len(self.shape[0])
    
    def rotate(self, clockwise):
        width = len(self.shape[0])
        if clockwise:
            temp_shape = [[None for x in range(len(self.shape))] for x in range(len(self.shape[0]))]
            for y in range(len(self.shape)):
                for x in range(len(self.shape[y])):
                    temp_shape[x][y] = self.shape[y][x]
        
        self.shape = temp_shape
            


    

