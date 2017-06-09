import os
import sys
import inspect

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2 ** 32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import serial

ser = serial.Serial('/dev/ttyUSB0', 9600)

import Leap
from Leap import *


def main():
    controller = Leap.Controller()
    while 1:
        if controller.is_connected:
            frame = controller.frame()
            if len(frame.hands) > 1:
                arm1 = frame.hands.leftmost
                arm2 = frame.hands.rightmost
                pitch_rads1 = int(arm1.direction.pitch // 0.018)
                pitch_rads2 = 90 + int(arm2.direction.pitch // 0.018)
                if pitch_rads1 > 0 and pitch_rads1 < 180:
                    pitch1 = str(pitch_rads1)
                    arm1serial = pitch1
                else:
                    arm1serial = "1"
                if pitch_rads2 > 0 and pitch_rads2 < 180:
                    pitch2 = str(pitch_rads2)
                    arm2serial = arm1serial + " " + pitch2 + "\n"
                else:
                    arm2serial = arm1serial + " 1\n"
            else:
                arm2serial = "1 1\n"
            ser.write(arm2serial)
            print arm2serial


if __name__ == '__main__':
    main()
