# Main file where the magic happens - Runs the game client
# Date: 4-14-20

import numpy as np
import plebs as pbs
import sys
from configs import *
import obstacles as obs


# Game class to manage game settings
class Game:
    def __init__(self, screen_w, screen_h, num_players):
        pygame.display.set_caption('Battle of Plebs')                   # Caption
        self.screen_w = screen_w                                        # Screen width
        self.screen_h = screen_h                                        # Screen height
        self.window = pygame.display.set_mode((screen_w, screen_h))     # Game window
        self.crash = False                                              # When to shut down the game
        self.font = pygame.font.SysFont(None, 40)                       # Initialize a font
        self.clock = pygame.time.Clock()                                # Set Game clock
        self.title_sprite = pygame.image.load(TITLE).convert_alpha()    # Load the title image
        self.total_players = num_players                                # Total number of players for resets
        self.remaining_plebs = num_players                              # Remaining players

        # Initialize a list of walls for the borders
        self.walls = [obs.Obstacles(0, [0, 0+(self.screen_h-WALL_WIDTH)*i, self.screen_w, WALL_WIDTH], i)
                      for i in range(2)] + \
                     [obs.Obstacles(0, [0+(self.screen_w-WALL_WIDTH)*i, 0, WALL_WIDTH, self.screen_h], i)
                      for i in range(2)]

        # Initialize a list of randomly placed items
        self.items = [obs.Obstacles(1, [np.random.randint(100, self.screen_w - 100),
                                        np.random.randint(100, self.screen_h - 100),
                                        ITEM_DIM, ITEM_DIM], i) for i in range(self.total_players)]

        # Initialize player/AI down here. args = (id, [x, y, w, h], [sprite_paths])
        self.plebs = [pbs.Plebs(i, [100+100*i, 425, 93, 105],
                                ALL_SPRITES[i]) for i in range(self.total_players)]

        # These plebs are just for display on the main menu
        self.display_plebs = [pbs.Plebs(i, [self.screen_w/2.5 + 100 * i, self.screen_h/4, int(93*.7), int(105*.7)],
                                        ALL_SPRITES[i]) for i in range(self.total_players)]

    def options(self):
        # Options page - functions to be updated later on
        running = True                  # Display the contents of the page
        while running:                  # Loop until no longer running
            self.clock.tick(FPS)        # Screen FPS

            for event in pygame.event.get():            # Get Game events
                if event.type == pygame.QUIT:           # If the window is closed, stop program
                    self.exit()

                if event.type == pygame.KEYDOWN:        # If escape key is pressed down
                    if event.key == pygame.K_ESCAPE:
                        running = False                 # Escape takes me back to main menu, quit the loop

            # Draw Function here.
            self.window.fill((0, 0, 0))                 # Fill screen with black
            self.display_text('Options', 20, 20)        # Display Options in the top left corner
            pygame.display.update()

    def selected(self, id):
        '''
        The specific pleb has been selected based on button click to be active/deactive player.
        Player will light up with a green outline if the player controls them.
        :param id: Id tag / index of a pleb that has been selected for player control
        :return: N/A
        '''
        if not self.plebs[id].player:               # Player has not been selected before, but is now activated
            self.plebs[id].player = True            # This pleb is now an active player
            self.display_plebs[id].player = True    # Main Screen pleb updated too
        else:
            self.plebs[id].player = False           # This pleb is no longer an active player
            self.display_plebs[id].player = False   # Main Screen pleb updated too
        print("id: [{}]\tPlayer: {}".format(id, self.plebs[id].player))


    def exit(self):
        '''
        Stops the game and the program.
        :return: N/A
        '''
        pygame.quit()       # Quit the game
        sys.exit()          # Complete shutdown

    def main_menu(self):
        '''
        Makes the main menu page to greet the user. Displays various texts, buttons, and sprite choices.
        Buttons can be selected with mouse presses.
        :return: N/A
        '''

        # Make the main menu screen
        running = True
        frames = 0              # Used for animation variation
        counter = 0             # Limit the amount of frames before specific animations

        while running:

            self.clock.tick(FPS)    # Screen FPS
            click = False           # Reset clicks to false

            for event in pygame.event.get():            # Get game close event - if user closes game window
                if event.type == pygame.QUIT:
                    running = False
                    self.exit()                         # Full quit if x is pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False                 # Resumes game if escape is pressed - crash if game not running
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True                    # Indicates user pressed a button

            mx, my = pygame.mouse.get_pos()     # Get the position of the user's mouse

            # Doing some drawing for the main menu specifically
            self.window.fill((0, 0, 0))

            # Display the Title image
            self.window.blit(pygame.transform.scale(self.title_sprite, (800, 100)), (self.screen_w/4, 20))
            self.display_text('Main Menu', 50, 50)                                          # Display Main menu text
            self.display_text("Character Options:", self.screen_w*.4, self.screen_h*.18)    # Display Character text

            # Set up and display a series of buttons
            self.make_button("Play Game", mx, my, 50, 100, 200, 50, click, self.run)        # Play - x, y, w, h
            self.make_button("Options", mx, my, 50, 200, 200, 50, click, self.options)      # Options - x, y, w, h
            self.make_button("Exit", mx, my, 50, 300, 200, 50, click, self.exit)            # Exit

            # Used to display specific plebs as buttons
            for pleb in self.display_plebs:
                self.make_button(" ", mx, my, pleb.x, pleb.y, pleb.w, pleb.h, click, self.selected, pleb.id)
                pleb.draw(self.window, frames)      # Display the pleb in each button

            # Limits the maximum option for frames and counter
            counter += 1
            if counter == 5:
                counter = 0
                frames += 1
                if frames == 10:
                    frames = 0

            # Display everything to the screen
            pygame.display.update()

    def display_text(self, text, x, y):
        '''
        Displays the given text at a specified coordinate. Font object is currently set in the init.
        :param text: String of text to display to the screen
        :param x: Integer x coordinate
        :param y: Integer y coordinate
        :return: N/A
        '''

        text_obj = self.font.render(text, 1, (0,255,0))         # Define a text object with the color green
        text_rect = text_obj.get_rect()                         # Get the rectangle from it
        text_rect.topleft = (x, y)                              # Where to place the text
        self.window.blit(text_obj, text_rect)                   # Blits the text to the screen

    def make_button(self, button_text, mx, my, x, y, w, h, click, func, *argv):
        '''
        Generalized function to make buttons display on screen with specific functionality when pressed.
        :param button_text: String, text to display on screen
        :param mx: Integer Mouse x coordinates
        :param my: Integer Mouse y coordinates
        :param x: Integer x coordinate of top left corner of button
        :param y: Integer y coordinate of top left corner of button
        :param w: Integer width from the top left x coordinate
        :param h: Integer height from the top left y coordinate
        :param click: Boolean value if a click has happened
        :param func: Function for the specific button
        :param argv: Various additional arguments required for the given function if any
        :return: N/A
        '''

        button = pygame.Rect(x, y, w, h)        # Create Button object with dimensions

        if button.collidepoint((mx, my)):       # Check if the mouse collides with the button
            if click:                           # If Clicked
                if len(argv) == 0:              # No additional arguments
                    func()                      # Run the passed in function
                else:                           # Arg to say more args coming
                    func(*argv)                 # Pass all the remaining next argument in

        pygame.draw.rect(self.window, (255, 0, 0), button)      # Draw the button
        self.display_text(button_text, x, y)                    # Display text on button

    def make_new_item(self):
        '''
        Checks the contents of the items list and if any of the items are dead, it remakes them in a random location
        at the specified list index.
        :return: N/A
        '''

        for item in self.items:         # Look through all the items
            if item.dead:               # Item has exploded
                my_id = item.id         # Set the id to replace the item

                # Set the new item to the dead item index
                self.items[my_id] = obs.Obstacles(1, [np.random.randint(100, self.screen_w - 100),
                                                      np.random.randint(100, self.screen_h - 100),
                                                      ITEM_DIM, ITEM_DIM], my_id)
                print("Initializing new item: {}".format(self.items[my_id].id))     # DEBUG

    def reset_game(self):
        self.crash = False                              # Reset crash variable
        self.remaining_plebs = self.total_players       # Reset remaining plebs

        for i, pleb in enumerate(self.plebs):           # Reset all plebs
            pleb.reset_pleb()

            if self.display_plebs[i].player:            # Keep player active
                pleb.player = True                      # Only if they were a player before

        for item in self.items:                         # Reset the items
            item.reset_obst()

        print('Reset Game')

    def run(self):
        '''
        Run the game to show characters, items, everything in action.
        Checks collisions and allows players to make moves.
        :return: N/A
        '''

        #self.reset_game()                           # Reset the game after a winner
        frames = 0
        counter = 0

        while not self.crash:                       # Keep going while the game hasn't ended.
            self.clock.tick(FPS)                    # Frames per second
            click = False                           # User clicked button
            for event in pygame.event.get():        # Get game close event - if user closes game window
                if event.type == pygame.QUIT:
                    self.crash = True               # Crash will get us out of the game loop
                    self.exit()                     # Crash everything
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:        # Escape takes me to the main menu
                        self.main_menu()                    # Go to main menu
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True                    # Indicates user pressed a button

            # Do Moves here
            for pleb in self.plebs:
                if pleb.alive:                              # Pleb is alive
                    if pleb.player:                         # Pleb is a human player
                        move = pleb.active_player()         # Keyboard to control pleb
                    else:
                        move = np.random.randint(0, 6)      # Have them move randomly - replace with AI later

                    pleb.do_move(move)                                          # Pleb makes a move
                    collision, wall_ind = pleb.check_collision(self.walls)      # Check this move to see if it collided

                    if collision:               # Collided with a wall
                        pleb.undo_move(move)    # Undo what you did, knock back

                    '''
                    # Pleb collision
                    collision = pleb.check_collision(self.plebs)  # Check if it collided with other plebs
                    if collision:               # Collided with a wall
                        pleb.undo_move(move)    # Undo what you did, knock back
                    '''

                    # Item collision
                    collision, item_ind = pleb.check_collision(self.items)  # Check if collided with an item
                    if collision and move == 5:                             # Collided with item and move is space
                        pleb.pick_up(self.items[item_ind])                  # Pick Up Item
                        print("contact with item")          # DEBUG

                    elif move == 5:
                        pleb.set_down()     # Set down item if pleb has one

                    if not pleb.alive:              # Check if pleb died
                        self.remaining_plebs -= 1   # If they're dead, then subtract from remaining plebs

            self.make_new_item()    # Look through for any dead items and reset them

            # Draw everything on screen once per frame
            self.draw_window(frames, click)

            # Update frame and counter, keeps it from become too large of a number
            counter += 1
            if counter == 5:
                counter = 0
                frames += 1
                if frames == 10:
                    frames = 0

    def draw_window(self, frames, click):
        '''
        Displays everything in the run function.
        :param frames: Integer value used to select a specific sprite image
        :return: N/A
        '''

        self.window.fill((100, 100, 100))  # Screen Color fill

        # Draw stuff here
        for block in self.walls:
            block.draw(self.window)             # Draw all the walls

        for pleb in self.plebs:
                pleb.draw(self.window, frames)  # Draws the plebs and their items

        for item in self.items:                 # Draw the items last so that the players can pick them up
            if not item.picked_up:              # Draw at the front if not picked up
                item.draw(self.window)          # Draw Item

        if self.remaining_plebs <= 1:
            mx, my = pygame.mouse.get_pos()         # Get the position of the user's mouse
            self.display_text("GAME OVER!!", self.screen_w / 2 - 40, self.screen_h / 2 - 40)  # Display Game over
            self.make_button("RESET", mx, my, self.screen_w / 2, self.screen_h / 2, 100, 30, click, self.reset_game)

        # Update the game screen
        pygame.display.update()


# Main - where the magic happens
if __name__ == '__main__':
    print("Battle of Plebs")
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, len(ALL_SPRITES))      # Initialize Game object
    game.main_menu()                                                # Go to the game menu
    #game.run()                  # Run the game

