import pygame, os
from playfield import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((800,720))
    clock = pygame.time.Clock()

    blue_block = pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "blue.png")))
    green_block = pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "green.png")))
    red_block = pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "red.png")))
    violet_block = pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "violet.png")))
    yellow_block = pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "yellow.png")))
    block_images = {"blue": blue_block, "green": green_block, "red": red_block, "violet": violet_block, "yellow": yellow_block}

    font = pygame.font.Font(os.path.join("graphics", "VT323-Regular.ttf"), 40)
    score_disp = ScoreDisplay(font, screen, block_images)
    field = Playfield(screen, block_images)
    cursor = Cursor(screen, block_images, field, score_disp)
    #field.fill_with_blocks()
    base_gravity_offset = 1000
    gravity_offset = base_gravity_offset
    gravity_dt = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        is_grav_frame = gravity_dt > gravity_offset

        field.update()
        filled_rows = field.check_filled_rows()
        if len(filled_rows) > 0:
            field.clear_filled_rows(filled_rows)
            score_disp.add_score(len(filled_rows))
            gravity_offset = base_gravity_offset - 70 * score_disp.level - 1

        cursor.update(is_grav_frame)

        if is_grav_frame:
            is_grav_frame = False
            gravity_dt = 0
        
        screen.fill("black")
        field.draw()
        cursor.draw()
        score_disp.draw()
        
        for s in cursor:
            screen.blit(block_images[cursor.color], s.rect)


        pygame.display.flip()

        dt = clock.tick(30)
        gravity_dt += dt

    pygame.quit()


if __name__ == "__main__":
    main()