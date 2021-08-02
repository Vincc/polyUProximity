import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.function_base import angle
import pylab as pl
from matplotlib import collections  as mc
import math
import pygame
import time
import serial
import io
import ast
#[(2,3),(3,2)], [(0,3),(2,3)], 
lines = [[(2,2),(3,1)]]
        # [(3,2),(5,2)]
linesB = [[(p[0]*100, p[1]*100) for p in line] for line in lines]
global c    
ser = serial.Serial("COM4", 9600, timeout = 0.1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
c = 0
while True:

    sio.flush() # it is buffering. required to get the data out *now*
    proxData = sio.readline()
    proxData = [i.split(":") for i in proxData.rstrip().split(";")][:-1]
    if proxData != []:
        print(proxData)

c = 0

def intersect(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return 0

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    if int(x) not in range(line2[0][0], line2[1][0]) and int(y) not in range(line2[0][1], line2[1][1]):
        return 0
    return x, y

def getDistance(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

class proxSensor:
    def __init__(self, pos, angleRange):
        self.pos = pos
        self.angleRange = angleRange
        self.currentAngle = self.angleRange[0]
        self.range = 5
        self.stepVal = 1
        
    # def read(self):
    #     ins = list(filter(lambda x: x!= 0, [intersect((self.pos,(self.pos[0]+(self.range*math.cos(math.radians(self.currentAngle))),self.pos[1]+(self.range*math.sin(math.radians(self.currentAngle))))),i) for i in lines]))
    #     print([intersect((self.pos,(self.pos[0]+(self.range*math.cos(math.radians(self.currentAngle))),self.pos[1]+(self.range*math.sin(math.radians(self.currentAngle))))),i) for i in lines])
    #     dis = map(getDistance, [self.pos for i in range(len(ins))] ,ins)
    #     try:
    #         return min(dis)
    #     except ValueError:
    #         return 0

    

    def step(self):
        global c
        self.currentAngle += self.stepVal
        if self.currentAngle == self.angleRange[1] or self.currentAngle == self.angleRange[0]:
            self.stepVal = self.stepVal * -1
            c+=1
    def draw(self, lineLen):
        x=self.pos[0]+(lineLen* math.cos(math.radians(self.currentAngle)))
        y=self.pos[1]+(lineLen* math.sin(math.radians(self.currentAngle)))
        return (x*100,y*100)

prox1 = proxSensor((0,0), (0,90))
prox2 = proxSensor((0,5), (-90,0))
prox3 = proxSensor((5,0),(90,180))
prox4 = proxSensor((5,5),(180,240))

proxes =[prox1, prox2, prox3, prox4]

pygame.init()
screen = pygame.display.set_mode([500, 500]) #drawing window
while True:
    for i in linesB:
        
        pygame.draw.line(screen, (0,255,0), i[0], i[1], 1)
    for proxn in proxes:

        pygame.draw.line(screen, (0,0,255), (proxn.pos[0]*100,proxn.pos[1]*100), proxn.draw(proxn.read()), 1)
        proxn.step()
    print(c)
    if c >= 4:
        screen.fill((0,0,0))
        c = 0
    time.sleep(0.01)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit(0)

# while True:
#     plt.pause(0.05)


print("test")