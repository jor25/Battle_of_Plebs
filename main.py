# Main file where the magic happens - Runs the game client
# Date: 4-14-20

import numpy as np
import pygame


# Game class to manage game settings
class Game:
    def __init__(self, screen_w, screen_h, num_players):
        pygame.display.set_caption('Battle of Plebs')                   # Caption
        self.screen_w = screen_w                                        # Screen width
        self.screen_h = screen_h                                        # Screen height
        self.window = pygame.display.set_mode((screen_w, screen_h))     # Game window
        self.crash = False                                              # When to shut down the game
        # Initialize player/AI down here.

    def run(self):
        '''
        Run the game to show network.
        :return:
        '''
        clock = pygame.time.Clock()
        frames = 0

        while not self.crash:                   # Keep going while the game hasn't ended.
            clock.tick(30)                      # Frames per second
            for event in pygame.event.get():    # Get game close event - if user closes game window
                if event.type == pygame.QUIT:
                    self.crash = True           # Crash will get us out of the game loop

            # Do Moves here

            # Draw everything on screen once per frame
            self.draw_window(frames)

            frames += 1

    def draw_window(self, frames):
        self.window.fill((0, 0, 0))  # Screen Color fill
        # Draw stuff here

        pygame.display.update()


if __name__ == '__main__':
    print("Battle of Plebs")
    pygame.init()               # Initialize the pygame instance
    game = Game(800, 600, 1)    # Initialize Game object
    game.run()                  # Run the game

