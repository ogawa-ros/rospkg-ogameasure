#! /usr/bin/env python3

name = "m100"

import time, sys
import rospy
import ogameasure
from std_msgs.msg import Float64
from std_msgs.msg import String

class m100(object):
    az = ""
    el = ""
    path = "/home/m100raspi/data/optical-pointing/"
    def __init__(self):
        self.m100 = ogameasure.Canon.M100_raspi.m100()
        rospy.Subscriber("/dev/m100/capture/mode_cmd",String, self.capture_image)
        rospy.Subscriber("/necst_telescope/coordinate/apparent_az_cmd",Float64, self.recieve_az)
        rospy.Subscriber("/necst_telescope/coordinate/apparent_el_cmd",Float64, self.recieve_el)

    def recieve_az(self,q):
        self.az = q.data

    def recieve_el(self,q):
        self.el = q.data

    def capture_image(self,q):
        mode = q
        timestr = time.strftime('%Y%m%d_%H.%M.%S', time.strptime(time.ctime()))
        savename = "/" + timestr + "_az_" + str(self.az) +"_el_" + str(self.el) + ".JPG"
        savepath = self.path + savename
        self.m100.capture(savepath)

if __name__ == "__main__" :
    rospy.init_node(name)
    m100()
    rospy.spin()
