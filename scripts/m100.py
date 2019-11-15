#! /usr/bin/env python3

name = "m100"

import time, sys
import rospy
import ogameasure
from std_msgs.msg import Float64
from std_msgs.msg import String
import os

class m100(object):
    az = ""
    el = ""
    def __init__(self):
        self.m100 = ogameasure.Canon.M100_raspi.m100()
        rospy.Subscriber("/dev/m100/capture/savepath",String, self.capture_image)

    def capture_image(self,q):
        savefile = q.data
        file_path = os.path.dirname(savefile)
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        self.m100.capture(savefile)

if __name__ == "__main__" :
    rospy.init_node(name)
    m100()
    rospy.spin()
