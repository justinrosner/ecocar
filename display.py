'''
This is the file that contains the main logic for the pygame instance and the
display methods to the screen
'''

# pylint: disable=E1101

import os
import pygame
import cruise_control
from car import Car

# Define some basic coloursW
WHITE = (255, 255, 255)
GREY = (159, 163, 168)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
TEXT_COLOR = (250, 105, 10)

class Game:
    '''
    Game class so that we can have more than one instance of pygame running if
    ever necessary
    '''

    def __init__(self):
        '''
        Method to initialize the game class and the pygame instance
        '''

        pygame.init()
        pygame.display.set_caption("EcoCAR DEV Challenge")
        self.width = 600
        self.height = 700
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.exit = False

    def run(self):
        '''
        Method that will invoke that main loop that contains all the game logic
        '''
        pygame.display.set_caption("EcoCAR DEV Challenge")

        # Creating the main car
        player = Car(175, 475, 0, 0)
        player.load_image("images/chevy.png")

        # Load the fonts
        font_40 = pygame.font.SysFont("Arial", 40, True, False)
        font_30 = pygame.font.SysFont("Arial", 30, True, False)
        text_title = font_40.render("EcoCAR DEV Challenge", True, TEXT_COLOR)
        text_ins = font_30.render("Click to Run!", True, TEXT_COLOR)

        # Setup the stripes.
        stripes = []
        stripe_count = 20
        stripe_x = 185
        stripe_y = -10
        stripe_width = 20
        stripe_height = 80
        space = 20

        for i in range(stripe_count):
            stripes.append([185, stripe_y])
            stripes.append([400, stripe_y])
            stripe_y += stripe_height + space

        collision = True

        while not self.exit:
            # pygame event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

                # Reset everything when the user starts the game.
                if collision and event.type == pygame.MOUSEBUTTONDOWN:
                    collision = False
                    player.x_pos = 250
                    player.d_x = 0
                    player.d_y = 0
                    pygame.mouse.set_visible(True)

                if not collision:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            player.d_x = 4
                        elif event.key == pygame.K_LEFT:
                            player.d_x = -4
                        elif event.key == pygame.K_UP:
                            player.d_y = - 4
                        elif event.key == pygame.K_DOWN:
                            player.d_y = 4

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                            player.d_x = 0
                        elif event.key == pygame.K_RIGHT:
                            player.d_x = 0
                        elif event.key == pygame.K_UP:
                            player.d_y = 0
                        elif event.key == pygame.K_DOWN:
                            player.d_y = 0

            # --- Game logic should go here ie. function calls to cruise_control ---

            #  Screen-clearing code
            self.screen.fill(GREY)

            # Drawing and moving the stripes
            if not collision:
                # Draw the stripes
                for i in range(stripe_count):
                    pygame.draw.rect(self.screen, WHITE, [stripes[i][0], stripes[i][1],
                                                          stripe_width, stripe_height])

                # Move the stripes
                for i in range(stripe_count):
                    stripes[i][1] += 3
                    if stripes[i][1] > self.size[1]:
                        stripes[i][1] = -40 - stripe_height

                player.draw_image(self.screen)
                player.move_x()
                player.move_y()
                player.check_out_of_screen()

                pygame.display.flip()

            else:
                self.draw_start_menu(self.screen, self.size, text_title, text_ins)

            self.clock.tick(60)

        pygame.quit()

    def draw_start_menu(self, window, display_size, text_title, text_ins):
        '''
        Function to draw the main menu for the app/demo
        Input:
            window (screen obj) - The screen we are drawing the output of the game to
            display_size (width(int), height(int)) - The width and height of the screen
            text_title (str) - The string we want to write to the title bar
            text_ins (str) - The string we want to add to the start menu
        Output:
            None
        '''
        window.blit(text_title, [display_size[0] / 2 - 190, display_size[1] / 2 - 100])
        window.blit(text_ins, [display_size[0] / 2 - 85, display_size[1] / 2 + 40])
        pygame.display.flip()


if __name__ == '__main__':
    GAME = Game()
    GAME.run()