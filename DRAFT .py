#imports
import pygame
import time
import spidev
import math

#Calculating Incline Angle
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 2000000
 

def readChannel(channel):
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return 3.3*data/1024

#Notes: readChannel(0) is for x-axis, readChannel(1) is for y-axis, and readChannel(2) is for z-axis
while True:
  def angle():
    return atan(readChannel(1)/readChannel(0))

#Simulating arrow 
arrow_posx = 0
arrow_posy = SCREENHEIGHT


background_colour = (255,255,255)
(width, height) = (1000, 1000)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Archery')
screen.fill(background_colour)
pygame.display.flip()



running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      
def terminate():
    pygame.quit()


terminate()

