# Class for in game obstacles and potentially objects.
# Date: 4-17-20

import pygame
import random

class Obstacles:
    def __init__(self, category, coords):
        self.category = category        # 0 is wall, 1 will be something else
        self.x, self.y, self.w, self.h = coords         # Initalize coords
        self.hitbox = (self.x, self.y, self.w, self.h)  # Set up location
        self.hold_time = 10
        self.held_for = self.hold_time           # Needs to be held for 5 frames before being able to drop
        self.activated = False      # Activated when picked up
        self.picked_up = False      # Only let it be picked up if this is false

    def blow_up(self):  # If category is 1, it can explode
        if self.category == 1:  # It can do this
            print("BOOM")

    def item_picked_up(self):       # The item was picked up
        if self.category == 1:      # Item
            self.picked_up = True   # Item is picked up
            self.activated = True   # Activate the item
            print("Item Activated".format())

    def item_put_down(self):    # Place the item down
        if self.category == 1:          # Item
            self.picked_up = False      # Item is placed down
            self.held_for += 1          # Increment held_time
            print("PLACED ITEM")

    def draw(self, window):
        if self.category == 0:      # Walls
            pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

        elif self.category == 1:    # Items
            if self.activated:      # Activated - starts out not activated until it's picked up
                color_num = random.randint(0, 255)      # Activate
            else:
                color_num = 0       # Not active
            pygame.draw.rect(window, (0, 0, color_num), self.hitbox, 10)

        if self.held_for < self.hold_time and not self.picked_up:    # Increment only if not being held and less than 5
            self.held_for += 1  # Increment held_for every frame