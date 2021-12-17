import math

#import python Module
import Config

#return the velocity and acceleration of the gazes in degrees of visual angle per second
def VelocityInDeg(gazes,headGazes):
    velocity=0
    acceleration=0
    duration=0
    outGazes=[]
    #get height of the screen in millimeters
    h=Config.PHYSICAL_SCREEN_HEIGHT
    #get distance from the screen in millimeters
    
    if len(headGazes)==0:
        return False
    d=float(headGazes[0][2])

    for i in range(1,len(gazes)):
        #calculate the distance between this gazes and the previous one in pixel
        s=math.sqrt((float(gazes[i][0])-float(gazes[i-1][0]))**2+(float(gazes[i][1])-float(gazes[i-1][1]))**2)
        #find the current distance from the screen
        for j in range(i,len(headGazes)):
            #compare timestamps
            if float(headGazes[j][4])>=float(gazes[i][3]):
                d=float(headGazes[j][2])/10
                break
        #convert size in pixel to degrees of visual angle
        s=sizeInDeg(h,d,s)
        #calculate velocity in degrees of visual angle per second
        temp=velocity
        duration=(float(gazes[i][3])-float(gazes[i-1][3]))/10**6
        velocity=s/duration
        acceleration=(velocity-temp)/duration
        outGazes.append([gazes[i][0],gazes[i][1],gazes[i][3],velocity,acceleration,gazes[i][4]])
    return outGazes

#return the size in degrees of visual angle of the distance "s" in pixel
def sizeInDeg(h,d,s):
    #"h"(height of the screen) and "d"(distance from the screen) in millimeters
    r=Config.SCREEN_HEIGHT
    # Calculate the number of degrees that correspond to a single pixel
    deg_per_px = math.degrees(math.atan2(0.5*h, d)) / (0.5*r)
    # Calculate the size of the stimulus in degrees
    size_in_deg = s * deg_per_px
    return(size_in_deg)
