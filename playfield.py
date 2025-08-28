import pygame, os, random

LEFT_MARGIN = 16
TOP_MARGIN = 20
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
    
    def get_corrds(self):
        return (self.rect.x, self.rect.y)


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
        # Drawing the border around the plaifield
        pygame.draw.rect(self.screen, "white", pygame.Rect((LEFT_MARGIN // 2) - 2,
                                                           (TOP_MARGIN // 2) - 2,
                                                           (NUM_COLLUMNS * BLOCK_SIZE + LEFT_MARGIN // 2) + 4,
                                                           (NUM_ROWS * BLOCK_SIZE + TOP_MARGIN // 2) + 4))
        pygame.draw.rect(self.screen, "black", pygame.Rect((LEFT_MARGIN // 2) + 1,
                                                           (TOP_MARGIN // 2) + 1,
                                                           (NUM_COLLUMNS * BLOCK_SIZE + LEFT_MARGIN // 2) - 2,
                                                           (NUM_ROWS * BLOCK_SIZE + TOP_MARGIN // 2) - 2))
        # Drawing the blocks in the playfield
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
    def __init__(self, screen, block_images, playfield, color = None, shape = None):
        super().__init__()
        self.block_images = block_images
        self.screen = screen
        self.field = playfield
        
        self.pos = 5
        if color is not None:
            self.color = color
        else:
            self.color = random.choice(COLORS)

        if shape not in SHAPES:
            self.shape_type = "s"
        else:
            self.shape_type = shape

        self.reb_left = 0
        self.reb_right = 0
        self.reb_rot_cw = 0

        self.new_shape()
        
        self.update_block_positions()

    def draw(self):
        for s in self:
            self.screen.blit(self.block_images[self.color], s.rect)
    

    def new_shape(self, shape=None):
        if shape is None:
            shape = self.shape_type
        else:
            self.shape_type = shape
        
        match shape:
            case "t":
                self.shape = [[None, None, None],
                              [True, True, True],
                              [None, True, None]]
            case "i":
                self.shape = [[True, True, True, True]]
            case "l":
                self.shape = [[None, None, None],
                              [True, True, True],
                              [None, None, True]]
            case "invl":
                self.shape = [[None, None, None],
                              [True, True, True],
                              [True, None, None]]
            case "s":
                self.shape = [[None, True, True],
                              [True, True, None]]
            case "z":
                self.shape = [[True, True, None],
                              [None, True, True]]
    
    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if self.reb_left == 0 or self.reb_left > 20:
                self.move(-1)
            self.reb_left += 1
        else:
            self.reb_left = 0
        if keys[pygame.K_RIGHT]:
            if self.reb_right == 0 or self.reb_right > 20:
                self.move(1)
            self.reb_right += 1
        else:
            self.reb_right = 0
        if keys[pygame.K_UP]:
            if self.reb_rot_cw == 0 or self.reb_rot_cw > 20:
                self.rotate(True)
            self.reb_rot_cw += 1
        else:
            self.reb_rot_cw = 0

        if self.check_collisions():
            self.transfer_to_field()
            self.new_shape()
        

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
        height = len(self.shape)
        temp_shape = [[None for x in range(height)] for x in range(width)]

        if width == height:
            if clockwise:
                for y in range(height):
                    for x in range(width):
                        temp_shape[x][height-y-1] = self.shape[y][x]
        else:
            for y in range(height):
                for x in range(width):
                    temp_shape[x][height-y-1] = self.shape[y][x]
        
        self.shape = temp_shape
        new_width = len(self.shape[0])
        new_height = len(self.shape)
        self.move(width-new_width)
    
    def check_collisions(self):
        for s in self:
            pix_x, pix_y = s.get_coords()
            pos_x, pos_y = pixel_to_grid(pix_x, pix_y)

            # Checking for a collision with the bottom of the field:
            if pos_y > NUM_ROWS:
                return True
            # Checking if there's something in the further down position in the field:
            elif not self.field.blocks[pos_x][pos_y + 1] is None:
                return True
            
    def transfer_to_field(self):
        for s in self:
            pix_x, pix_y = s.get_coords()
            pos_x, pos_y = pixel_to_grid(pix_x, pix_y)

            self.field.add_block(pos_x, pos_y, self.color)


            