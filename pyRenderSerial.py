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

    def draw(self):
        dis = int(proxData[proxes.index(self)][0])
        print("prox" + str(proxes.index(self)+1))
        
        angle = int(proxData[proxes.index(self)][1])* self.multiple +self.offset
        #print((angle+self.offset)*self.multiple)
        x=self.pos[0]*(500/effectiveRange)+(dis*(500/effectiveRange)* math.cos(math.radians(angle)))
        y=self.pos[1]*(500/effectiveRange)+(dis*(500/effectiveRange)* math.sin(math.radians(angle)))
        print("angle: "  + str(angle))
        print("distance: "  + str(dis))
        print("line end vertex position:")
        print(self.pos[0]*(500/effectiveRange), self.pos[1]*(500/effectiveRange))
        print(x,y)
        return (x,y)

#set range of sensor
effectiveRange = 100

#Define sensors
prox1 = proxSensor((0,0), 70, -1)
prox2 = proxSensor((100,0), 200,-1)
prox3 = proxSensor((0,100), 0,-1)
prox4 = proxSensor((100,100), -90, -1)
proxes =[prox1, prox2]

pygame.init()
screen = pygame.display.set_mode([500, 500]) #drawing window
while True:
    sio.flush() # it is buffering. required to get the data out *now*
    proxData = sio.readline()
    if proxData == "ResetFlag\n":
            screen.fill((0,0,0))
            continue
    proxData = [i.split(":") for i in proxData.rstrip().split(";")][:-1]# split data from arduino into a 2D list
    for i in proxData:
        if int(i[0]) > effectiveRange:
            i[0] = str(effectiveRange)

    if proxData != [] and len(proxData) == len(proxes):
            print(proxData)
            for proxn in proxes:
                pygame.draw.line(screen, (0,0,255), (proxn.pos[0]*(500/effectiveRange),proxn.pos[1]*(500/effectiveRange)), proxn.draw())
                time.sleep(0.01)
                pygame.display.flip()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit(0)