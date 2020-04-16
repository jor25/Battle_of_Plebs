# Main file where the magic happens - Runs the game client
# Date: 4-14-20

import numpy as np
import pygame
import plebs as pbs
import sys


# Game class to manage game settings
class Game:
    def __init__(self, screen_w, screen_h, num_players):
        pygame.display.set_caption('Battle of Plebs')                   # Caption
        self.screen_w = screen_w                                        # Screen width
        self.screen_h = screen_h                                        # Screen height
        self.window = pygame.display.set_mode((screen_w, screen_h))     # Game window
        self.crash = False                                              # When to shut down the game
        self.font = pygame.font.SysFont(None, 40)                       # Initialize a font
        self.clock = pygame.time.Clock()

        # Initialize player/AI down here.
        self.plebs = pbs.Plebs(0, [200, 425, 90, 100])                   # [x,y,w,h]

    def options(self):
        running = True
        while running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False                 # Escape takes me back to main menu

            self.window.fill((0, 0, 0))
            self.display_text('options', 20, 20)
            pygame.display.update()



    def exit(self):
        pygame.quit()       # Quit the game
        sys.exit()          # Complete shutdown

    def main_menu(self):
        # Make the main menu screen
        running = True
        while running:

            self.clock.tick(60)
            click = False       # Reset clicks to false

            for event in pygame.event.get():            # Get game close event - if user closes game window
                if event.type == pygame.QUIT:
                    running = False
                    self.exit()                         # Full quit if x is pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False                 # Will resume game if escape is pressed - crash if game not running
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            mx, my = pygame.mouse.get_pos()

            self.window.fill((0, 0, 0))
            self.display_text('main menu', 20, 20)                                          # Display main menu
            self.make_button("Play Game", mx, my, 50, 100, 200, 50, click, self.run)        # Play - x, y, w, h
            self.make_button("Options", mx, my, 50, 200, 200, 50, click, self.options)      # Options - x, y, w, h
            self.make_button("Exit", mx, my, 50, 300, 200, 50, click, self.exit)            # Exit
            pygame.display.update()


    def display_text(self, text, x, y):
        text_obj = self.font.render(text, 1, (0,255,0))
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x, y)          # Where to place the text
        self.window.blit(text_obj, text_rect)

    def make_button(self, button_text, mx, my, x, y, w, h, click, func):
        button = pygame.Rect(x, y, w, h)

        if button.collidepoint((mx, my)):
            if click:
                func()  # Run the passed in function

        pygame.draw.rect(self.window, (255, 0, 0), button)  # Draw the button
        self.display_text(button_text, x, y)


    def run(self):
        '''
        Run the game to show network.
        :return:
        '''
        frames = 0

        while not self.crash:                   # Keep going while the game hasn't ended.
            self.clock.tick(60)                 # Frames per second
            for event in pygame.event.get():    # Get game close event - if user closes game window
                if event.type == pygame.QUIT:
                    self.crash = True           # Crash will get us out of the game loop
                    self.exit()                 # Crash everything
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:        # Escape takes me to the main menu
                        self.main_menu()                    # Go to main menu

            # Do Moves here
            move = self.plebs.active_player()
            self.plebs.do_move(move)
            # Draw everything on screen once per frame
            self.draw_window(frames)

            frames += 1

    def draw_window(self, frames):
        self.window.fill((0, 0, 0))  # Screen Color fill
        # Draw stuff here
        self.plebs.draw(self.window, frames)
        pygame.display.update()


if __name__ == '__main__':
    print("Battle of Plebs")
    pygame.init()               # Initialize the pygame instance
    game = Game(800, 600, 1)    # Initialize Game object
    game.main_menu()
    #game.run()                  # Run the game

