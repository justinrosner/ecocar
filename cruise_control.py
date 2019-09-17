'''
'''

import math


def check_collision(player_x, player_y, player_width, player_height, car_x,
                    car_y, car_width, car_height):
    '''
    Function to check if two cars have crashed (coordinates overlap)
    Input:
        player_x () -
        player_y () -
        player_width () -
        player_height () -
        car_x () -
        car_y () -
        car_width () -
        car_height () -
    Output:
        A boolean value denoting if there has been a collosion between the two
        given cars(inputs)
    '''

    return bool((player_x+player_width > car_x) and (player_x < car_x+car_width) and \
                (player_y < car_y+car_height) and (player_y+player_height > car_y))

def acc_scenario1(player_x, player_y, player_speed, car_x,
                    car_y, car_speed, follow_dist):

    if player_x == car_x and math.abs(player_y - car_y) <= (follow_dist * 2):
        if (player_speed > car_speed):
            return (car_speed**2 - player_speed**2)/ (2 * ((player_y - car_y) - follow_dist)) #This returns the deceleration value (will be negative)
    return 0