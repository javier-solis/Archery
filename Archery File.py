#All imports------------------------------------------
import time

import pygame
from pygame.locals import *
import math
import spidev
import RPi.GPIO as GPIO


#Misc. Variables--------------------------------------
RED = (255,0,0)
BLACK= (0,0,0)
WHITE=(255,255,255)
forceperstretch=3000

running=True


#Variables for Main Simulator------------------------------
screenheight=750
screenwidth=750

arrowlength=5
arrowheight=2

posX=0
posY=screenheight-arrowheight

arrow = pygame.Rect(0, posY, arrowlength, arrowheight)
surface = pygame.display.set_mode([screenwidth,screenheight])
blackscreen=pygame.Rect(0, 0, screenwidth, screenheight)




#Initialize Pygame--------------------------------------
pygame.init()
pygame.display.set_caption("Archery Simulator")
pygame.draw.rect(surface, RED, arrow)
pygame.display.update()


#Setting up readChannel--------------------------------
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 2000000

def readChannel(channel):
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return 3.3*data/1024


#Using Accelerometer to Find Angle--------------------
horizontal=1.07421875
down=0.88032226562
up=1.29504743304

def angle():
    if readChannel(2)<=horizontal:
        return (((math.pi)/2)/(horizontal-down))*(horizontal-readChannel(2))
    elif readChannel(2)>horizontal:
        print("Pointed down")
        return 0
    else:
        return 0


#LED---------------------------------------------------

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led = 23

GPIO.setup(led,GPIO.OUT)
GPIO.output(led,0)


#Finding Velocity using Potentiometers------------------

default1=readChannel(3)
default2=readChannel(4)


def velocity():
    return forceperstretch*(abs(readChannel(3) - default1))

def velocityX():
    return abs(math.cos(angle())*velocity())

def velocityY():
    return abs(math.sin(angle())*velocity())


#Button to initialize everything----------------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
input_pin = 5
GPIO.setup(input_pin,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

pushed = False

def input_check2(input):
    global pushed 
    if input==1:
        if pushed==False: 
            pushed = True 
    else:
        if pushed==True: 
            pushed = False 



#Creating a State Machine------------------------------
state=0
velx=0
vely=0


#Moving target-----------------------------------------
move_commandx = 0 
move_commandy = 0
target=pygame.Rect(0, 0, 10, 10)
pygame.draw.rect(surface, WHITE, target)
pygame.display.update()
#While Loop--------------------------------------------

while running == True:

    if state==0:
        input_check2(GPIO.input(input_pin))
        GPIO.output(led,0)
        surface.fill(BLACK)

        for event in pygame.event.get(): #check for inputs here!
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    shoot_command = True
                if event.key == K_ESCAPE:
                    terminate()

        #defining movement of targets
        pressed = pygame.key.get_pressed() 


        if pressed[pygame.K_LEFT]:
            move_commandx-=1
        if pressed[pygame.K_RIGHT]:
            move_commandx+=1
        if pressed[pygame.K_UP]:
            move_commandy-=1
        if pressed[pygame.K_DOWN]:
            move_commandy+=1
        
        #drawing target
        target = pygame.Rect(move_commandx, move_commandy, 10, 10)
        pygame.draw.rect(surface, WHITE, target)
        pygame.display.update()
        
        if pushed==True:
            velx=velocityX()
            vely=velocityY()
            timeInitial=time.time()
 
            state=1

    if state==1:
        for event in pygame.event.get():        
            if event.type == pygame.QUIT:
                running = False
                
        GPIO.output(led,1)
        
        #Defining Positon of Arrow
        posX= (velx*(time.time()-timeInitial))
        posY= (screenheight-((vely)*(time.time()-timeInitial) - ((1/2)*(9.81)*((time.time()-timeInitial)**2))))

        
        #Changing Position of Arrow 
        arrow = pygame.Rect(posX, posY, arrowlength, arrowheight)
        pygame.draw.rect(surface, RED, arrow)
        pygame.display.update()

        if posY>=screenheight:
            print("Arrow is off screen. Wait 2 seconds to restart.")
            time.sleep(2)
            pygame.draw.rect(surface, BLACK, blackscreen)
            state=0
        

                

#Ending-------------------------------------------------
GPIO.cleanup()
pygame.quit()                           
