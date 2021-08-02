import math
import pygame
import time
import serial
import io

#define serial port
ser = serial.Serial("COM4", 9600, timeout = 0.1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

class proxSensor:
    
    def __init__(self, pos, offsetAngle, multiple):
        self.pos = pos
        self.offset = offsetAngle
        self.multiple = multiple

    def draw(self, iter):
        dis = int(iter[0])
        
        angle = int(iter[1])* self.multiple +self.offset
        #print((angle+self.offset)*self.multiple)
        x=self.pos[0]*(500/effectiveRange)+(dis*(500/effectiveRange)* math.cos(math.radians(angle)))
        y=self.pos[1]*(500/effectiveRange)+(dis*(500/effectiveRange)* math.sin(math.radians(angle)))

        print(x,y)
        return (x,y)

#set range of sensor
effectiveRange = 100

#Define sensors
prox1 = proxSensor((0,0), 70, -1) 
prox2 = proxSensor((100,0), 200,-1)
prox3 = proxSensor((0,100), 0,-1)
prox4 = proxSensor((100,100), -90, -1)
proxes =[prox1, prox2, prox3, prox4]

pygame.init()
screen = pygame.display.set_mode([500, 500]) #drawing window
c = 0
while True:
    
    sio.flush() # it is buffering. required to get the data out *now*
    proxData = sio.readline()
    
    if proxData == "ResetFlag\n":
        time.sleep(2)
        screen.fill((0,0,0))
        continue
    if proxData == "next\n":
        c+=1
        c = c%len(proxes)
        continue

    proxData = proxData.rstrip().split(":")# split data from arduino into a 2D list
    if proxData != "" and proxData != [""]:
        print(proxData)
        if int(proxData[0]) > effectiveRange:
            proxData[0] = str(effectiveRange)
        pygame.draw.line(screen, (0,0,255), (proxes[c].pos[0]*(500/effectiveRange),proxes[c].pos[1]*(500/effectiveRange)), proxes[c].draw(proxData))   
        pygame.display.flip()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit(0)
    