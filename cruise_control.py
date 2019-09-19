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

def acc_scenario1(player_x, player_y, player_speed, car_x, car_y, car_speed, follow_dist): #####This assumes input in km/h, and following distance is either 2,3,4 depending on how far you want to follow
    player_ms = player_speed/3.6 #convert to m/s
    car_ms = car_speed/3.6 #convert to m/s
    accel = -10.04 
    timeA = ((car_ms - player_ms)/accel) #time it takes to slow down using our acc
    deltaD = ((player_ms - car_ms)/2)*timeA*(12) #distance shrunk between cars in pixels 
    if player_x == car_x and abs(player_y - car_y) <= (follow_dist * deltaD):
        if (player_speed > car_speed):
            return timeA #This returns the time for deceleration
    return 0


'''Starts'''
'''Starts'''
def laneChange(direction, player_x, player_y):#direction from the press of button, player x
    #the leftLane and stuff is just the set coordinates for the lanes\
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

        car_ms = carVel/3.6 #convert to m/s

        if (abs(carY - player_y) <= (2*player.height)):#the safe range is gonna be 2 car lengths in front or behind
            return errorVariable #replace with whatever we want error to say
        vrel=(((player.velocity-carVel)*1000)/3600)#relative velocity in m/s negative if we're slower
        deltaY = (player_y - carY)#negative if we're in front of car
        if ((((deltaY > 0) and ((vrel*2*(12))<deltaY)) or ((deltaY < 0) and ((vrel*2*(12))>deltaY))) and abs(vrel) < 20):#the 12 is pixels per meter and 2 is 2 seconds, the vrel<20 is important because anything above that will mean that they're not gonna have enough time to adjust speed
            return succVariable #replace with whatever you want success to be

    return errorVariable

    '''Ends'''


def adjust_speed(distance, follow_dist):

    if distance >= follow_dist*2:
        return True

    return False
