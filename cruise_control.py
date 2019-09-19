'''
This file contains the logic for the cruise control algorithms
'''

import math


def check_collision(player_x, player_y, car_x, car_y):
    '''
    Function to check if two cars have crashed (coordinates overlap)
    Input:
        player_x (int) - The x coordinate of the main car on the screen
        player_y (int) - The y coordinate of the main car on the screen
        car_x (int) - The x coordinate of the secondary car on the screen
        car_y (int) - The y coordinate of the secondary car on the screen
    Output:
        A boolean value denoting if there has been a collosion between the two
        given cars(inputs)
    '''

    return bool((player_x + 42 + 10 > car_x) and (player_x < car_x + 42 + 10) and \
                (player_y < car_y + 60 + 10) and (player_y + 60 + 10 > car_y))

def acc_scenario1(player_x, player_y, player_speed, car_x,
                    car_y, car_speed, follow_dist):

    if player_x == car_x and math.abs(player_y - car_y) <= (follow_dist * 2):
        if (player_speed > car_speed):
            return (car_speed**2 - player_speed**2)/ (2 * ((player_y - car_y) - follow_dist)) #This returns the deceleration value (will be negative)
    return 0