'''
This is the GUI/Representation of an adaptive cruise control algorithm
'''

import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (159, 163, 168)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
TEXT_COLOR = (250, 105, 10)


class Car:
    '''
    This is the general class for cars that we will use to describe both our car
    and the surrounding cars on the road
    '''

    def __init__(self, x_pos=0, y_pos=0, d_x=4, d_y=0, width=30, height=30):
        self.image = ""
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.d_x = d_x
        self.d_y = d_y
        self.width = width
        self.height = height

    def load_image(self, img):
        '''
        Function to load the image we are going to use for the car
        '''

        self.image = pygame.image.load(img).convert()
        self.image = pygame.transform.scale(self.image, (110, 191))
        self.image.set_colorkey(BLACK)

    def draw_image(self):
        '''
        Draw the image of the car to the screen
        '''

        screen.blit(self.image, [self.x_pos, self.y_pos])

    def move_x(self):
        '''
        Function to move the car along the x-axis
        '''

        self.x_pos += self.d_x

    def move_y(self):
        '''
        Function to move the car along the y-axis
        '''

        self.y_pos += self.d_y

    def check_out_of_screen(self):
        '''
        Function to see if the car has moved off of the visible screen
        '''

        if self.x_pos + self.width > 600 or self.x_pos < 0:
            self.x_pos -= self.d_x


def check_collision(player_x, player_y, player_width, player_height, car_x,
                    car_y, car_width, car_height):
    '''
    Function to check if two cars have crashed (coordinates overlap)
    '''

    return bool((player_x+player_width > car_x) and (player_x < car_x+car_width) and \
                (player_y < car_y+car_height) and (player_y+player_height > car_y))


def draw_main_menu(screen, size, text_title, text_ins):
    '''
    Function to draw the main menu for the app/demo
    '''

    screen.blit(text_title, [size[0] / 2 - 106, size[1] / 2 - 100])
    screen.blit(text_ins, [size[0] / 2 - 85, size[1] / 2 + 40])
    pygame.display.flip()

def main():
    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Create a player car object
    player = Car(175, 475, 0, 0, 110, 191)
    player.load_image("chevy.png")

    collision = True

    # Load the fonts
    font_40 = pygame.font.SysFont("Arial", 40, True, False)
    font_30 = pygame.font.SysFont("Arial", 30, True, False)
    text_title = font_40.render("EcoCAR DEV Challenge", True, TEXT_COLOR)
    text_ins = font_30.render("Click to Run!", True, TEXT_COLOR)

    # Setup signal buttons
    # left_signal = pygame.Rect(screen, (0,0,240),(150,90,100,50))
    right_signal = pygame.Rect(0, 0, 0, 0)

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

    # Main program loop
    while not done:
        # Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # Reset everything when the user starts the game.
            if collision and event.type == pygame.MOUSEBUTTONDOWN:
                collision = False
                player.x_pos = 175
                player.d_x = 0
                score = 0
                pygame.mouse.set_visible(True)

            if not collision:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        player.d_x = 4
                    elif event.key == pygame.K_LEFT:
                        player.d_x = -4

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        player.d_x = 0
                    elif event.key == pygame.K_RIGHT:
                        player.d_x = 0

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos  # Gets the mouse position
                    if right_signal.collidepoint(mouse_pos):
                        print("Nice the button works")

        # --- Game logic should go here

        # --- Screen-clearing code goes here
        screen.fill(GREY)

        # --- Drawing code should go here
        if not collision:
            # Draw the stripes
            for i in range(stripe_count):
                pygame.draw.rect(screen, WHITE, [stripes[i][0], stripes[i][1],
                                                stripe_width, stripe_height])

            # Move the stripes
            for i in range(stripe_count):
                stripes[i][1] += 3
                if stripes[i][1] > size[1]:
                    stripes[i][1] = -40 - stripe_height

            player.draw_image()
            player.move_x()
            player.check_out_of_screen()

            '''
            We will have to come back to this stuff later

            # Check if the other cars move out of the screen.
            for i in range(car_count):
                cars[i].draw_rect()
                cars[i].y_pos += cars[i].d_y
                if cars[i].y_pos > size[1]:
                    score += 10
                    cars[i].y_pos = random.randrange(-150, -50)
                    cars[i].x_pos = random.randrange(0, 340)
                    cars[i].d_y = random.randint(4, 9)


            # Check the collision of the player with the car
            for i in range(car_count):
                if check_collision(player.x_pos, player.y_pos, player.width, player.height,
                                cars[i].x_pos, cars[i].y_pos, cars[i].width,
                                cars[i].height):
                    collision = True
                    pygame.mouse.set_visible(True)
                    break

            '''
            pygame.display.flip()

            # Draw the rect (THIS IS JUST A TEST)
            pygame.draw.rect(screen, [0, 0, 0], right_signal)

        else:
            draw_main_menu(screen, size, text_title, text_ins)

        # Limiting to 60 frames per second
        clock.tick(60)

if __name__ == '__main__':
    pygame.init()

    size = (600, 700)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("EcoCAR DEV Challenge")

    main()
    pygame.quit()

