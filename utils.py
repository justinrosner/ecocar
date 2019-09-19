'''
This file contains a bunch of helper functions
'''

# Defining some constants
BRAKE = -10.04
ACCEL = 3.3
GREY = (159, 163, 168)
LANESUPERPOSITIONS = [180, 280, 380]

def update_velocity(initial_velocity, target_velocity, elapsed_time):
    '''
    This is a function that will be called to show the acceleration and deceleration of the
    car smoothly
    Input:
        initial_velocity (double) - The initial velocity for the car
        target_velocity (double) - The target velocity for the car
        elapsed_time (double) - The time that has passed since the car started accelerating
    Output:
        A double representing the updated speed of the car
    '''
    initial = kmh_to_ms(initial_velocity)
    target = kmh_to_ms(target_velocity)
    if target > initial:
        return ms_to_kmh(ACCEL * elapsed_time + initial)
    return ms_to_kmh(BRAKE * elapsed_time + initial)


def calculate_time(initial_velocity, target_velocity):
    '''
    This is a function that will be called to get the time it will take to update
    the velocity of the car to the desired speed
    Input:
        initial_velocity (double) - The current velocity of the car
        target_velocity (double) - The desired velocity of the car
    '''
    cur = kmh_to_ms(initial_velocity)
    target = kmh_to_ms(target_velocity)
    if cur > target:
        return (target - cur) / BRAKE
    return (target - cur) / ACCEL

def kmh_to_ms(velocity):
    '''
    Function to convert from km/h to m/s
    Input:
        velocity (double) - The velocity of the car in km/h
    Output:
        A double representing the velocity of the car in m/s
    '''
    return velocity * (5 / 18)


def ms_to_kmh(velocity):
    '''
    Function to convert from m/s to km/h
    Input:
        velocity (double) - The velocity of the car in m/s
    Output:
        A double representing the velocity of the car in km/h
    '''
    return velocity * (18 / 5)

def is_int(string):
    '''
    Method to check if a given string is an integer
    '''
    try:
        int(string)
        return True
    except ValueError:
        return False
    except TypeError:
        return False

def ms_to_sec(milli):
    '''
    Function to convert from milliseconds to seconds
    Input:
        milli (double)
    Output:
        The time inputted in seconds
    '''
    return milli / 1000

def lane_change(player, buttons):
    '''
    This function checks if a button has been pressed for a lane change, if yes it will
    then complete the lane change
    Input:
        player (Car obj) - The main car that we are moving
        buttons (dict of buttons) - The left and right lane change buttons
    Output:
        None
    '''
    if buttons['left'].pressed and player.cur_lane != 0:
        if player.x_pos > LANESUPERPOSITIONS[player.cur_lane - 1]:
            player.x_pos -= 2
        else:
            buttons['left'].pressed = False
            player.cur_lane -= 1
            player.x_pos = LANESUPERPOSITIONS[player.cur_lane]
            buttons['left'].colour = GREY
    else:
        buttons['left'].colour = GREY

    if buttons['right'].pressed and player.cur_lane != 2:
        if player.x_pos < LANESUPERPOSITIONS[player.cur_lane + 1]:
            player.x_pos += 2
        else:
            buttons['right'].pressed = False
            player.cur_lane += 1
            player.x_pos = LANESUPERPOSITIONS[player.cur_lane]
            buttons['right'].colour = GREY
    else:
        buttons['right'].colour = GREY
