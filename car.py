'''
This file contains the logic for anything related to the movement of a car
'''

# pylint: disable= E0611

import pygame

BLACK = (0, 0, 0)

class Car:
    '''
    This is the general class for cars that we will use to describe both our car
    and the surrounding cars on the road
    '''
    def __init__(self, x_pos=0, y_pos=0, velocity=0):
        self.image = ""
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.velocity = velocity # in kmh
        self.realVel = 10;

        # Arbitrary height and width of cars
        # Initial values are w=110, h=191
        self.width = 42
        self.height = 60

    def move_y(self):
        self.y_pos += self.velocity

    def load_image(self, img):
        '''
        Function to load the image we are going to use for the car
        Input:
            img (str) - The name of the file/image to load
        Output:
            None
        '''
        self.image = pygame.image.load(img).convert()
        self.image = pygame.transform.scale(self.image, (42, 60))
        self.image.set_colorkey(BLACK)

    def draw_image(self, screen):
        '''
        Draw the image of the car to the screen
        Input:
            screen (screen object) - The screen the game will output to
        Output:
            None
        '''
        screen.blit(self.image, [self.x_pos, self.y_pos])

    def change_velocity(self, velocity):
        '''
        Method to change the velocity of the car
        Input:
            velocity (double) - The new velocity of the car in km/h
        Output:
            None
        '''
        self.velocity = round(velocity)

    def check_out_of_screen(self):
        '''
        Function to see if the car has moved off of the visible screen
        '''
        if self.x_pos + self.width > 600 or self.x_pos < 0:
            self.x_pos -= self.d_x
