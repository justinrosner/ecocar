'''
This is the file that contains the main logic for the pygame instance and the
display methods to the screen
'''

# pylint: disable=E1101

import os
import pygame
import math
import cruise_control
import input_box as ib
import utils
from car import Car

# Define some basic coloursW
WHITE = (255, 255, 255)
GREY = (159, 163, 168)
GREEN = pygame.Color("#6b9c58")
YELLOW = pygame.Color("#fcdb38")
BLACK = (0, 0, 0)
TEXT_COLOR = (250, 105, 10)

CurrentLane = 1
LaneSuperpositions = [ 180, 280, 380 ]
change = False
update = False
flag = True 

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
        self.height = 900
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.exit = False

    def run(self):
        '''
        Method that will invoke that main loop that contains all the game logic
        '''
        pygame.display.set_caption("EcoCAR DEV Challenge")

        # Creating the main car
        player = Car(0, 750, 100)
        player.load_image("images/chevy.png")

        # Test for the second car
        car1 = Car(0, 50, 0)
        car1.load_image("images/chevy_black.png")


        velocity_input = ib.InputBox(480, 30, 50, 30, '')
        car_spawn = ib.InputBox(480, 120, 50, 30, '')

        # Load the fonts
        font_40 = pygame.font.SysFont("Arial", 40, True, False)
        font_30 = pygame.font.SysFont("Arial", 30, True, False)
        font_20 = pygame.font.SysFont("Arial", 20, True, False)
        text_title = font_40.render("EcoCAR DEV Challenge", True, TEXT_COLOR)
        text_ins = font_30.render("Click to Run!", True, TEXT_COLOR)
        text_velocity = font_20.render("Enter a velocity:", True, BLACK)
        text_cur_velocity = font_20.render(f"Current Velocity: {player.velocity}", True, BLACK)

        # Setup the stripes.
        stripes = []
        stripe_count = 50
        stripe_y = -10
        stripe_width = 5
        stripe_height = 45
        space = 15

        for i in range(stripe_count):
            stripes.append([255, stripe_y])
            stripes.append([345, stripe_y])
            stripe_y += stripe_height + space

        collision = True
        CurrentLane = 1
        LaneSuperpositions = [ 180, 280, 380 ]
        while not self.exit:
            global change
            global update
            global flag
            # pygame event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

                # Reset everything when the user starts the game.
                if collision and event.type == pygame.MOUSEBUTTONDOWN:
                    collision = False
                    player.x_pos = 280
                    pygame.mouse.set_visible(True)

                # handle the event for the velocity input box
                new_velocity = velocity_input.handle_event(event)
                new_car = car_spawn.handle_event(event)

                # Only change the car velocity when its a valid int between 0-100
                if utils.is_int(new_velocity) and int(new_velocity) in range(0, 101):
                    target_velocity = int(new_velocity)
                    change = True
                    start_time = 0.0

                # EVERYTHING BELOW IS FOR THE SPAWNING BOX

                car1.x_pos = LaneSuperpositions[ CurrentLane ]
                if utils.is_int(new_car) and int(new_car) in range(-101, 201):
                    car1.velocity = int( (player.velocity - int(new_car))  / 10 )
                    car1.realVel = int(new_car)



              

            # --- Game logic should go here ie. function calls to cruise_control ---'



            

            #  Screen-clearing code
            self.screen.fill(GREY)

            if not collision:

                # Drawing the distance line between cars
                T1 = (car1.x_pos + 21, car1.y_pos+ 60)
                T2 = (player.x_pos + 21, player.y_pos)
                dist_between = abs(player.y_pos - (car1.y_pos+60)) / 12
                #follow_dist = player.velocity
                           

                if dist_between < 40 and flag:
                    change = True
                    target_velocity = car1.realVel
                    start_time = 0.0
                    flag = False


                if dist_between < 20:
                    car1.velocity = 0                   


                
                if change:
                    update = True
                    change = False
                    time_for_accel = utils.calculate_time(player.velocity, target_velocity)
                    start_vel = player.velocity
                    start_time = pygame.time.get_ticks()

                cur_time = pygame.time.get_ticks()

                if update and utils.ms_to_sec(cur_time - start_time) < time_for_accel:
                    player.velocity = round(utils.update_velocity(start_vel, target_velocity,
                                                            utils.ms_to_sec(cur_time - start_time)), 2)
                self.draw_stripes(stripe_count, stripes, stripe_width, stripe_height,
                             player.velocity)

                # Drawing the outer lines to the screen
                pygame.draw.lines(self.screen, YELLOW, False, [(165,0), (165,900)], 5)
                pygame.draw.lines(self.screen, YELLOW, False, [(435,0), (435,900)], 5)

                # Drawing the 'grass' to the screen
                pygame.draw.rect(self.screen, GREEN, (0, 0, 163, 900), 0)
                pygame.draw.rect(self.screen, GREEN, (437, 0, 163, 900), 0)

                # Handling the drawing the textbox to the screen
                velocity_input.update()
                self.screen.blit(text_velocity, [445, 0])
                velocity_input.draw(self.screen)

           


                pygame.draw.line(self.screen, YELLOW, T1, T2)
                self.screen.blit(font_20.render("      Distance: " + str(round(dist_between)) + "m", True, BLACK),[(T1[0] + T2[0])/2, (T1[1] + T2[1])/2])
                

                #Handling the drawing of car spawn to screen
                car_spawn.update()
                car_spawn.draw(self.screen)

                # Writing the current velocity to the screen
                text_cur_velocity = font_20.render("Current Velocity: " + str(round(player.velocity)), True, BLACK)
                self.screen.blit(text_cur_velocity, [0, 0])

                player.draw_image(self.screen)
                player.check_out_of_screen()

                car1.draw_image(self.screen)
                car1.move_y()

                pygame.display.flip()

            else:
                self.draw_start_menu(self.screen, (self.width, self.height),
                                     text_title, text_ins)

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

    def draw_stripes(self, stripe_count, stripes, stripe_width, stripe_height, velocity):
        '''
        Method to draw the stripes to the road
        Input:
            stripe_count (int) - The number of stripes to draw to the screen
            stripes ([int, int]) - An array of the positions of the stripes on the screen
            stripe_width (int) - The pixel width of the stripes
            stripe_height (int) - The pixrl height of the stripes
            velocity (double) - The velocity of the car
        Output:
            None
        '''
        # Drawing the stripes
        for i in range(stripe_count):
            pygame.draw.rect(self.screen, WHITE, [stripes[i][0], stripes[i][1],
                                                    stripe_width, stripe_height])
        # Move the stripes
        for i in range(stripe_count):
            # This accounts for speed at which the line moves
            stripes[i][1] += velocity / 10
            if stripes[i][1] > self.height:
                stripes[i][1] = -30 - stripe_height

    def draw_background(self, screen):
        '''
        This is am method to draw the background to the current screen
        '''


if __name__ == '__main__':
    GAME = Game()
    GAME.run()
