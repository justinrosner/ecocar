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


'''Starts'''
def laneChange(direction, player_x, player_y):#direction from the press of button, player x
    #the leftLane and stuff is just the set coordinates for the lanes
    if (((player_x == leftLane) and (direction == left)) or ((player_x == rightLane) and (direction == right))):#trying to turn into barrier
        return errorVariable #replace with whatever we want error to say
    else:
        if((player_x == leftLane) or (player_x == rightLane)):#both cases looking at middle lane
            carY = carM1.y
            carVel = carM1.velocity
        else:#players in the middle 
            if (direction == left):
                carY = carL1.y
                carVel = carL1.velocity
            else:#player in middle, direction is right
                carY = carR1.y
                carVel = carR1.velocity

        if (abs(carY - player_y) <= (2*player.height)):#the safe range is gonna be 2 car lengths in front or behind
            return errorVariable #replace with whatever we want error to say   
        vrel=(((player.velocity-carVel)*1000)/3600)#relative velocity in m/s negative if we're slower
        deltaY = (player_y - carY)#negative if we're in front of car 
        if (((deltaY > 0) and ((vrel*2*(12))<deltaY)) or ((deltaY < 0) and ((vrel*2*(12))>deltaY))):#the 12 is pixels per meter and 2 is 2 seconds
            return succVariable #replace with whatever you want success to be 
  
    return errorVariable
    
    '''Ends'''
