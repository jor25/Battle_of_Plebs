# Class for in game obstacles and potentially objects.
# Date: 4-17-20

import pygame

class Obstacles:
    def __init__(self, category, coords):
        self.category = category        # 0 is wall, 1 will be something else
        self.x, self.y, self.w, self.h = coords         # Initalize coords
        self.hitbox = (self.x, self.y, self.w, self.h)  # Set up location

    def draw(self, window):
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)


