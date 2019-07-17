print("Program Opened")

#imports
import pygame
from pygame.locals import *

import time
import spidev
import math

#Accelerometer stuff
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 2000000

#drawing variables
SCREENHEIGHT = 1000
SCREENWIDTH= 1000
arrow_posx = 0
arrow_posy = SCREENHEIGHT


#defines angle
def readChannel(channel):
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return 3.3*data/1024

#arrow flying 
def drawArrow(coordinates):
    ArrowRect = pygame.Rect(arrow_posx,arrow_posy,30,10)





#simulator turning on
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

screen.blit(player, (x, y))
pygame.display.update() 
 

background_colour = (255,255,255)

pygame.display.set_caption('Archery')
screen.fill(background_colour)
pygame.display.flip()




running = True
while running:
    #calculating angle 
    def angle():
        return math.atan(readChannel(1)/readChannel(0))
    print(angle()*(180/math.pi))
    
    #letting simulator run
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    coordinates[0]+=1
    coordinates[0]+=1
    drawArrow()
    
    arrow_posx+= 1

    
from sys import exit
while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
