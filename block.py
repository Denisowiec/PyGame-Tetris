import pygame, os
colors = ["blue", "green", "red", "violet", "yellow"]

class Block(pygame.sprite.Sprite):
    def __init__(self, color, image, x = 0, y = 0):
        super().__init__()
        if color not in colors:
            print("Wrong sprite color!")
            self.color = "blue"
        else:
            self.color = color

        self.surf = image
        self.rect = self.surf.get_rect().move(x, y)
        
    
    def move(self, x, y):
        self.rect = self.rect.move(x, y)