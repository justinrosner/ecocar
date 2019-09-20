'''
This is the file that contains the main logic for the pygame instance and the
display methods to the screen
'''

# pylint: disable=E1101

import math
import pygame
import cruise_control
import input_box as ib
import utils
import button as bt
from car import Car

# Define some basic colours
WHITE = (255, 255, 255)
GREY = (159, 163, 168)
GREEN = pygame.Color("#6b9c58")
YELLOW = pygame.Color("#fcdb38")
RED = (255, 0, 0)
BLACK = (0, 0, 0)
TEXT_COLOR = (250, 105, 10)

# Load the fonts
FONT_40 = pygame.font.SysFont("Arial", 40, True, False)
FONT_30 = pygame.font.SysFont("Arial", 30, True, False)
FONT_19 = pygame.font.SysFont("Arial", 19, True, False)

LANESUPERPOSITIONS = [180, 280, 380]

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
        self.change = False
        self.update = False
        self.flag = True
        self.cars_on_screen = 0
        self.target_velocity = 30
        self.start_time = 0.0

    def run(self):
        '''
        Method that will invoke that main loop that contains all the game logic
        '''
        pygame.display.set_caption("EcoCAR DEV Challenge")

        # Creating a set of all cars currently on the screen
        cars_on_road = set()

        # Creating the main car
        player = Car(280, 800, 1, 100)
        player.load_image("images/chevy.png")
        cars_on_road.add(player)
        self.cars_on_screen += 1

        # Setup the velocity input box
        velocity_input = ib.InputBox(480, 30, 50, 30, '')

        text_title = FONT_40.render("EcoCAR DEV Challenge", True, TEXT_COLOR)
        text_ins = FONT_30.render("Click to Run!", True, TEXT_COLOR)
        text_velocity = FONT_19.render("Enter a velocity:", True, BLACK)

        # Setup the stripes.
        stripes = []
        stripe_count = 50
        stripe_y = -10
        stripe_width = 5
        stripe_height = 45
        space = 15

        for _ in range(stripe_count):
            stripes.append([255, stripe_y])
            stripes.append([345, stripe_y])
            stripe_y += stripe_height + space

        # Setup the buttons
        buttons = dict()
        buttons['spawn'] = bt.Button(60, 80, 30, 30, YELLOW, GREY)
        buttons['left'] = bt.Button(450, 150, 30, 30, YELLOW, GREY)
        buttons['right'] = bt.Button(550, 150, 30, 30, YELLOW, GREY)

        collision = True

        while not self.exit:
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

                # Handle the event for all of the various buttons
                for button in buttons.values():
                    button.handle_event(event)

                # Only take the input when its a valid int between 0-100
                if utils.is_int(new_velocity) and int(new_velocity) in range(0, 101):
                    self.target_velocity = int(new_velocity)
                    self.change = True
                    self.start_time = 0.0

            #  Screen-clearing code
            self.screen.fill(GREY)

            if not collision:
                # logic for smooth acceleration
                if self.change:
                    self.update = True
                    self.change = False
                    time_for_accel = utils.calculate_time(player.velocity, self.target_velocity)
                    start_vel = player.velocity
                    self.start_time = pygame.time.get_ticks()

                cur_time = pygame.time.get_ticks()

                if self.update and utils.ms_to_sec(cur_time - self.start_time) < time_for_accel:
                    player.velocity = round(utils.update_velocity(start_vel, self.target_velocity,
                                                                  utils.ms_to_sec(cur_time - self.start_time)), 2)
                # Spawn another car if needed
                possible_car = utils.car_spwan(buttons['spawn'], cars_on_road, self.cars_on_screen)
                if possible_car != None:
                    possible_car.load_image("images/chevy_black.png")
                    cars_on_road.add(possible_car)
                    self.cars_on_screen += 1


                # Change lanes if needed

                if utils.lane_change(player, buttons):
                    self.flag = True


                # Methods to draw info the the screen
                self.draw_stripes(stripe_count, stripes, stripe_width, stripe_height,
                                  player.velocity)
                self.draw_background(velocity_input, text_velocity, player.velocity)
                #self.draw_distance_line(car1, player)
                self.draw_buttons(buttons)

                # Creating a set of cars in the same lane as the main car
                cars_in_lane = set()
                closest_car = None
                min_distance = 10000 # Arbitrary value that is impossible for the cars to have

                # draw the cars to the screen and get the set of cars in the same lane as
                # the main car
                for car in cars_on_road:
                    if car.y_pos != player.y_pos and car.x_pos != player.x_pos:
                        car.move_spawned_cars(player.velocity)




                    # Check to get the closest car infront of the main car
                    if car.cur_lane == player.cur_lane and \
                       (car.x_pos != player.x_pos or car.y_pos != player.y_pos):
                        cars_in_lane.add(car)


                        if player.y_pos - car.y_pos < min_distance:
                            min_distance = player.y_pos - car.y_pos
                            closest_car = car


                    car.draw_image(self.screen)
                    self.screen.blit(FONT_19.render(str(car.velocity), True, RED),[car.x_pos, car.y_pos])
                    


                if closest_car != None:
                    distance = self.draw_distance_line(closest_car, player)
                    follow_dist = 800
                    self.acc_scenario1(distance, closest_car, follow_dist)
                    


                #Call cruise control

                
                pygame.display.flip()

            else:
                self.draw_start_menu(text_title, text_ins)

            self.clock.tick(60)

        pygame.quit()

    def draw_start_menu(self, text_title, text_ins):
        '''
        Function to draw the main menu for the app/demo
        Input:
            text_title (str) - The string we want to write to the title bar
            text_ins (str) - The string we want to add to the start menu
        Output:
            None
        '''
        self.screen.blit(text_title, [self.width / 2 - 190, self.height / 2 - 100])
        self.screen.blit(text_ins, [self.width / 2 - 85, self.height / 2 + 40])
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

    def draw_background(self, velocity_input, text_velocity, velocity):
        '''
        This is a method to draw the background to the current screen
        '''
        # Drawing the outer lines to the screen
        pygame.draw.lines(self.screen, YELLOW, False, [(165, 0), (165, 900)], 5)
        pygame.draw.lines(self.screen, YELLOW, False, [(435, 0), (435, 900)], 5)

        # Drawing the 'grass' to the screen
        pygame.draw.rect(self.screen, GREEN, (0, 0, 163, 900), 0)
        pygame.draw.rect(self.screen, GREEN, (437, 0, 163, 900), 0)

        # Handling the drawing the textbox to the screen
        velocity_input.update()
        self.screen.blit(text_velocity, [445, 0])
        velocity_input.draw(self.screen)

        # Writing the current velocity to the screen
        text_cur_velocity = FONT_19.render(f"Current Velocity:{velocity}", True, BLACK)
        self.screen.blit(text_cur_velocity, [0, 0])

    def draw_distance_line(self, front_car, player):
        '''
        This method draws a distance line from the main car to the car directly in
        front of it
        Input:
            front_car (Car obj) - The car directly in front of the main car
            player (Car obj) - The main car that the cruise control algorithm is following
        Output:
            None
        '''
        # Drawing the distance line between cars
        y_diff = front_car.y_pos - player.y_pos
        x_diff = abs(front_car.x_pos - player.x_pos)
        distance = round(math.sqrt(y_diff ** 2 + x_diff ** 2), 2)

        t_1 = (front_car.x_pos + 21, front_car.y_pos+ 60)
        t_2 = (player.x_pos + 21, player.y_pos)
        pygame.draw.line(self.screen, YELLOW, t_1, t_2)
        self.screen.blit(FONT_19.render(f"      Distance: {distance}", True, BLACK),
                         [(t_1[0] + t_2[0])/2, (t_1[1] + t_2[1])/2])

        return distance

    def draw_buttons(self, buttons):
        '''
        Method to draw the lane change and spawn buttons to the screen
        Input:
            buttons (dict of button objs) - Buttons to be drawn to the screen
        Output:
            None
        '''
        # Draw the text for the car spawn button and the lane change buttons
        self.screen.blit(FONT_19.render("Click to spawn car:", True, BLACK), [0, 50])
        self.screen.blit(FONT_19.render("Change lanes:", True, BLACK), [460, 115])

        for button in buttons.values():
            button.draw_button(self.screen)

    def acc_scenario1(self, distance, closest_car, follow_dist):
        if self.flag and distance <= follow_dist * 2:
            self.change = True
            self.target_velocity = closest_car.velocity
            self.start_time = 0.0
            self.flag = False




if __name__ == '__main__':
    GAME = Game()
    GAME.run()
