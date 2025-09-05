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
    return ((x - LEFT_MARGIN) // BLOCK_SIZE, (y - TOP_MARGIN) // BLOCK_SIZE)

def shape_type_to_shape(type):
    if type not in SHAPES:
        raise Exception("Wrong shape!")
    
    match type:
        case "t":
            shape = [[True, True, True],
                     [None, True, None]]
        case "i":
            shape = [[True, True, True, True]]
        case "l":
            shape = [[True, True, True],
                     [None, None, True]]
        case "invl":
            shape = [[True, True, True],
                     [True, None, None]]
        case "s":
            shape = [[None, True, True],
                     [True, True, None]]
        case "z":
            shape = [[True, True, None],
                     [None, True, True]]
    
    return shape

class Block(pygame.sprite.Sprite):
    def __init__(self, color, x = 0, y = 0):
        super().__init__()

        self.color = color
        self.surf = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.rect = self.surf.get_rect().move(x, y)
        
    
    def move(self, x, y):
        self.rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)

    def get_coords(self):
        return (self.rect.x, self.rect.y)


class Grid(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        # This creates a grid of NUM_ROWS by NUM_COLLUMNS
        self.grid = [[None for i in range(NUM_ROWS)] for i in range(NUM_COLLUMNS)]
    
    def print_grid(self):
        for y in range(len(self.grid[0])):
            string = ""
            for x in range(len(self.grid)):
                if self.grid[x][y] is None:
                    string += "-"
                else:
                    string += "o"
            print(string)
        print("\n")
            
    
    def add_to_grid(self, block, pos_x, pos_y):
        x, y = grid_to_pixel(pos_x, pos_y)
        block.move(x, y)
        self.add(block)
        self.grid[pos_x][pos_y] = block
    
    def rem_from_grid(self, pos_x, pos_y):
        block = self.grid[pos_x][pos_y]
        self.remove(block)
        self.grid[pos_x][pos_y] = None
    
    def move_within_grid(self, old_x, old_y, new_x, new_y):
        if not self.get_block(new_x, new_y) is None:
            raise Exception("Moving a block to a non-empty space!")
        if self.get_block(old_x, old_y) is None:
            raise Exception("Attempting to move an empty space!")
        self.grid[new_x][new_y] = self.grid[old_x][old_y]
        self.grid[old_x][old_y] = None
        pix_x, pix_y = grid_to_pixel(new_x, new_y)
        self.grid[new_x][new_y].move(pix_x, pix_y)
    
    def get_block(self, x, y):
        return self.grid[x][y]
    
    def is_empty(self):
        return len(self.sprites()) == 0
    
    def is_row_filled(self, y):
        for x in range(NUM_COLLUMNS):
            if self.grid[x][y] is None:
                return False
        return True
    
    def offset_by_one_row(self, upto):
        for y in reversed(range(upto)):
            for x in range(NUM_COLLUMNS):
                block = self.get_block(x, y)
                if block != None:
                    self.move_within_grid(x, y, x, y+1)

    def offset_empty_rows(self, rows):
        for y in sorted(rows):
            self.offset_by_one_row(y)

class Playfield():
    def __init__(self, screen, images_dict):
        self.screen = screen
        self.blocks = Grid()
        self.colors = COLORS
        self.block_images = images_dict
    
    def update(self):
        for s in self.blocks:
            pass
    
    def draw(self):
        # Drawing the border around the plaifield
        pygame.draw.rect(self.screen, "white", pygame.Rect((LEFT_MARGIN // 2) - 2,
                                                           (TOP_MARGIN // 2) - 2,
                                                           (NUM_COLLUMNS * BLOCK_SIZE + LEFT_MARGIN // 2) + 6,
                                                           (NUM_ROWS * BLOCK_SIZE + TOP_MARGIN // 2) + 6))
        pygame.draw.rect(self.screen, "black", pygame.Rect((LEFT_MARGIN // 2) + 1,
                                                           (TOP_MARGIN // 2) + 1,
                                                           (NUM_COLLUMNS * BLOCK_SIZE + LEFT_MARGIN // 2),
                                                           (NUM_ROWS * BLOCK_SIZE + TOP_MARGIN // 2)))
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
    
    def check_filled_rows(self):
        filled_rows = []
        if self.blocks.is_empty():
            return filled_rows

        for y in reversed(range(NUM_ROWS)):
            if self.blocks.is_row_filled(y):
                filled_rows.append(y)
        return filled_rows
    
    def clear_filled_rows(self, rows):
        for y in rows:
            for x in range(NUM_COLLUMNS):
                self.blocks.rem_from_grid(x, y)
        self.blocks.offset_empty_rows(rows)

class Cursor(pygame.sprite.Group):
    def __init__(self, screen, block_images, playfield, shape_keeper, color = None, shape = None):
        super().__init__()
        self.block_images = block_images
        self.screen = screen
        self.field = playfield
        self.BASE_POS = 5
        self.collision_detected_last_time = False
        self.shape_keeper = shape_keeper
        
        self.pos = self.BASE_POS
        self.y_pos = 0
        if color is not None:
            self.color = color
        else:
            self.color = random.choice(COLORS)

        if shape not in SHAPES:
            self.shape_type = "s"
        else:
            self.shape_type = shape

        # key rebound timers
        self.reb_left = 0
        self.reb_right = 0
        self.reb_rot_cw = 0
        self.reb_down = 0

        self.new_shape()
        
        self.update_block_positions()

    def draw(self):
        for s in self:
            self.screen.blit(self.block_images[self.color], s.rect)
    

    def new_shape(self, shape=None, color=None):
        self.pos = self.BASE_POS
        self.y_pos = 0

        if shape is None:
            shape = random.choice(SHAPES)
        
        self.shape_type = shape

        if color is None:
            self.color = random.choice(COLORS)
        else:
            self.color = color

        self.shape = shape_type_to_shape(shape)
        self.pos -= len(self.shape)//2
    
    def update(self, gravity):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if self.reb_left == 0 or self.reb_left > 20:
                if not self.check_collisions(-1):
                    self.move(-1)
            self.reb_left += 1
        else:
            self.reb_left = 0
        if keys[pygame.K_RIGHT]:
            if self.reb_right == 0 or self.reb_right > 20:
                if not self.check_collisions(1):
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
        if keys[pygame.K_DOWN]:
            if self.reb_down == 0 or self.reb_down > 20:
                if not self.check_collisions() and not gravity:
                    self.y_pos += 1
            self.reb_down += 1
        else:
            self.reb_down = 0
        if keys[pygame.K_ESCAPE]:
            pygame.quit()

        
        if gravity:
            if self.collision_detected_last_time and self.check_collisions():
                if self.y_pos == 0:
                    print("Game over!")
                    print(f"Final score: {self.shape_keeper.score}.")
                    print(f"You reached level {self.shape_keeper.level}.")
                    pygame.quit()
                self.transfer_to_field()
                shape, color = self.shape_keeper.take_next_shape()
                self.new_shape(shape, color)
                self.update_block_positions()
            else:
                self.y_pos += 1
                if self.y_pos > 20:
                    self.y_pos = 20

        self.update_block_positions()

        if self.check_collisions():
            self.collision_detected_last_time = True
        else:
            self.collision_detected_last_time = False

    def update_block_positions(self):
        for y in range(len(self.shape)):
            for x in range(len(self.shape[y])):
                if self.shape[y][x] is True:
                    block =  Block(self.color)
                    self.shape[y][x] = block
                    self.add(block)
                if self.shape[y][x] is not None:
                    pos_x, pos_y = grid_to_pixel(self.pos + x, self.y_pos + y)
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
    
    def check_collisions(self, x_offset = 0):
        for s in self:
            pix_x, pix_y = s.get_coords()
            pos_x, pos_y = pixel_to_grid(pix_x, pix_y)

            pos_x += x_offset
            if pos_x < 0:
                pos_x = 0
            if pos_x >= NUM_COLLUMNS:
                pos_x = NUM_COLLUMNS - 1

            # Special check for x_offset
            if x_offset != 0:
                if not self.field.blocks.get_block(pos_x, pos_y) is None:
                    return True
            else:
                # Checking for a collision with the bottom of the field:
                if pos_y + 1 >= NUM_ROWS:
                    return True
                # Checking if there's something in the further down position in the field:
                elif not self.field.blocks.get_block(pos_x, pos_y + 1) is None:
                    return True
        return False
            
    def transfer_to_field(self):
        for s in self:
            pix_x, pix_y = s.get_coords()
            pos_x, pos_y = pixel_to_grid(pix_x, pix_y)
            self.remove(s)

            self.field.add_block(pos_x, pos_y, self.color)

class ScoreDisplay():
    def __init__(self, font, screen, block_images, score = 0, level = 1):
        self.score = score
        self.num_rows_cleared = 0
        self.level = level
        self.font = font
        self.screen = screen
        self.block_images = block_images
        self.next_color = random.choice(COLORS)
        self.next_shape = random.choice(SHAPES)
        self.next_shape_blocks = shape_type_to_shape(self.next_shape)

        self.score_rect = pygame.Rect(LEFT_MARGIN * 3 + BLOCK_SIZE * NUM_COLLUMNS,
                                TOP_MARGIN//2,
                                BLOCK_SIZE * NUM_COLLUMNS,
                                BLOCK_SIZE)
        self.level_rect = pygame.Rect(LEFT_MARGIN * 3 + BLOCK_SIZE * NUM_COLLUMNS,
                                TOP_MARGIN + BLOCK_SIZE + 6,
                                BLOCK_SIZE * NUM_COLLUMNS,
                                BLOCK_SIZE)
        self.next_shape_rect = pygame.Rect(LEFT_MARGIN * 3 + BLOCK_SIZE * NUM_COLLUMNS,
                                TOP_MARGIN + 10 + (BLOCK_SIZE + 6) * 2,
                                BLOCK_SIZE * 4,
                                BLOCK_SIZE * 4)
        self.surf = None

    def draw(self):
        score_display_surf = self.font.render(f"Score: {self.score}00", False, "white")
        level_display_surf = self.font.render(f"Level: {self.level}", False, "white")
        next_shape_surf = pygame.Surface((BLOCK_SIZE*4, BLOCK_SIZE*4))
    
        self.screen.blit(score_display_surf, self.score_rect)
        self.screen.blit(level_display_surf, self.level_rect)

        width = len(self.next_shape_blocks)
        for y in range(len(self.next_shape_blocks[0])):
            for x in range(width):
                if self.next_shape_blocks[width-x-1][y]:
                    next_shape_surf.blit(self.block_images[self.next_color], (x*BLOCK_SIZE, y * BLOCK_SIZE))
        
        self.screen.blit(next_shape_surf, self.next_shape_rect)

    def add_score(self, num_rows):
        if num_rows == 1:
            self.score += 1
        elif num_rows == 2:
            self.score += 2
        elif num_rows == 3:
            self.score += 4
        elif num_rows >= 4:
            self.score += 10
        else:
            return
        
        self.num_rows_cleared += num_rows

        if self.num_rows_cleared >= 10:
            self.advance_level()
            self.num_rows_cleared -= 10
    
    def advance_level(self):
        self.level += 1
        if self.level > 10:
            self.level = 10

    def take_next_shape(self):
        s = self.next_shape
        c = self.next_color
        self.next_shape = random.choice(SHAPES)
        self.create_shape_pattern()
        self.next_color = random.choice(COLORS)
        return (s, c)
    
    def create_shape_pattern(self):
        self.next_shape_blocks = shape_type_to_shape(self.next_shape)
