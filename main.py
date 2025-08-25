import pygame, os
from playfield import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    clock = pygame.time.Clock()

    blue_block = pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "blue.png")))
    green_block = pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "green.png")))
    red_block = pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "red.png")))
    violet_block = pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "violet.png")))
    yellow_block = pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "yellow.png")))
    block_images = {"blue": blue_block, "green": green_block, "red": red_block, "violet": violet_block, "yellow": yellow_block}

    field = Playfield(screen, block_images)
    cursor = Cursor()
    #field.fill_with_blocks()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        field.update()
        field.draw()
        cursor.update()
        
        for s in cursor:
            screen.blit(block_images[cursor.color], s.rect)


        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()