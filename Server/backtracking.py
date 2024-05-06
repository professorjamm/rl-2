ALIGN_ERROR = 5 # Degrees
DIST_ERROR = 20 # pixels

# WASD as a one-hot encoded binary
MOVE_FORWARD = 0b1000
MOVE_BACKWARD = 0b0010
TURN_RIGHT = 0b0001
TURN_LEFT = 0b0100

QUAD_ONE = 1
QUAD_TWO = 2
QUAD_THREE = 3
QUAD_FOUR = 4

AXIS_XP = 5
AXIS_YP = 6
AXIS_XN = 7
AXIS_YN = 8

import math as math

def determine_quadrant(xdiff, ydiff):
    if(xdiff == 0):
        if(ydiff > 0):
            return AXIS_YP
        elif(ydiff < 0):
            return AXIS_YN
    elif(ydiff == 0):
        if(xdiff > 0):
            return AXIS_XP
        elif(xdiff < 0):
            return AXIS_XN

    if(xdiff > 0 and ydiff > 0):
        return QUAD_ONE
    elif(xdiff < 0 and ydiff > 0):
        return QUAD_TWO
    elif(xdiff < 0 and ydiff < 0):
        return QUAD_THREE
    elif(xdiff > 0 and ydiff < 0):
        return QUAD_FOUR

def get_xtheta(xdiff, ydiff):
    if (xdiff == 0):
        return 90
    return math.degrees(math.atan(abs(ydiff)/abs(xdiff)))


def get_dist(xdiff, ydiff):
    return math.sqrt(xdiff ** 2 + ydiff ** 2)


def get_direction(xpos, ypos, rot, xdest, ydest):
    xdiff = xpos - xdest
    ydiff = ydest - ypos

    region = determine_quadrant(xdiff, ydiff)

    thetax = get_xtheta(xdiff, ydiff)
    thetacar = 0
    thetadiff = 0
    dist = get_dist(xdiff, ydiff)



    match region:
        case 1: # QUAD_ONE
            thetacar = 270 - thetax
        case 2: # QUAD_TWO
            thetacar = 90 + thetax
        case 3: # QUAD_THREE
            thetacar = 90 - thetax
        case 4: # QUAD_FOUR
            thetacar = 270 + thetax
        case 5: # AXIS_XP
            thetacar = 270
        case 6: # AXIS_YP
            thetacar = 180
        case 7: # AXIS_XN
            thetacar = 90
        case 8: # AXIS_YN
            thetacar = 0
        case _:
            print("huh")

    thetadiff = rot - thetacar

    # print(f"x: {thetax}, car: {thetacar}, diff: {thetadiff}")

    if(dist < DIST_ERROR):
        # print("We made it outta da hood")
        return -1

    if(abs(thetadiff) > ALIGN_ERROR):
        if(thetadiff > 0):
            return TURN_LEFT
        elif(thetadiff <= 0):
            return TURN_RIGHT
    else:
       if(dist > 0):   
        return MOVE_FORWARD

 


    
    




