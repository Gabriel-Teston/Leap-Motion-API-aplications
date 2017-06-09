import os, sys, inspect
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))


import Leap
from Leap import *


import pygame
from pygame.locals import *


resolution = (1297, 733)
pygame.init()
windowSurface = pygame.display.set_mode(resolution, HWSURFACE|DOUBLEBUF|RESIZABLE)
pygame.display.set_caption("Runnig!")


collors = [(50,50,50), (0, 0, 0), (0, 255, 0), (255, 255, 255)]


windowSurface.fill(collors[3])
def drawpolygon(x,y,pointer_size,collor):
    x1 = resolution[0] / 2 + x*2
    y1 = resolution[1] - y*2
    pygame.draw.polygon(windowSurface, collors[collor], (
        (x1 - pointer_size, y1 - pointer_size), (x1 + pointer_size, y1 - pointer_size),
        (x1 + pointer_size, y1 + pointer_size), (x1 - pointer_size, y1 + pointer_size)))
def drawline(x, y, x1, y1, pointer_size):
    x2 = resolution[0] / 2 + x*2
    y2 = resolution[1] - y*2
    x3 = resolution[0] / 2 + x1*2
    y3 = resolution[1] - y1*2
    pygame.draw.polygon(windowSurface, collors[1], (
        (x2 , y2 ), (x2 , y2 ),
        (x3 , y3 ), (x3 , y3 )),pointer_size)
def main():
    running = 1
    paused = 0
    controller = Leap.Controller()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == K_c:
                    windowSurface.fill(collors[3])
        if paused == False:
            if controller.is_connected:
                frame = controller.frame()
                windowSurface.fill(collors[3])
                for hand in frame.hands:
                    for finger in frame.fingers:
                        drawpolygon(finger.tip_position.x, finger.tip_position.y, 6, 0)
                        drawline(finger.tip_position.x, finger.tip_position.y, finger.joint_position(2).x,
                                 finger.joint_position(2).y, 6)
                        drawpolygon(finger.joint_position(2).x, finger.joint_position(2).y, 10, 0)
                        drawline(finger.joint_position(2).x, finger.joint_position(2).y, finger.joint_position(1).x,
                                 finger.joint_position(1).y, 6)
                        drawpolygon(finger.joint_position(1).x, finger.joint_position(1).y, 10, 0)
                        drawline(finger.joint_position(1).x, finger.joint_position(1).y, finger.joint_position(0).x,
                                 finger.joint_position(0).y, 6)
                        drawpolygon(finger.joint_position(0).x, finger.joint_position(0).y, 10, 0)
                        if finger.tip_position.z <= 0:
                            drawpolygon(finger.tip_position.x, finger.tip_position.y, 3, 2)
                    drawline(hand.fingers[0].joint_position(0).x, hand.fingers[0].joint_position(0).y,
                             hand.arm.wrist_position.x, hand.arm.wrist_position.y, 6)
                    drawline(hand.arm.wrist_position.x, hand.arm.wrist_position.y,
                             2 * hand.arm.wrist_position.x - hand.fingers[0].joint_position(0).x,
                             2 * hand.arm.wrist_position.y - hand.fingers[0].joint_position(0).y, 6)
                    drawpolygon(hand.palm_position.x, hand.palm_position.y, 10, 0)
                    drawpolygon(hand.arm.wrist_position.x, hand.arm.wrist_position.y, 10, 0)
                    drawpolygon(2 * hand.arm.wrist_position.x - hand.fingers[0].joint_position(0).x,
                                2 * hand.arm.wrist_position.y - hand.fingers[0].joint_position(0).y, 10, 0)
        pygame.display.update()
if __name__ == '__main__':
    main()