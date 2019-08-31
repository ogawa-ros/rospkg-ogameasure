#! /usr/bin/env python3

name = "fsw0020"

import time
import sys
import ogameasure
import rospy
import threading
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int32

class fsw0020(object):
    def __init__(self):
        host = rospy.get_param("~host")
        port = rospy.get_param("~port")
        com = ogameasure.ethernet(host, port)
        self.sg = ogameasure.Phasematrix.FSW0010(com)


        rospy.Subscriber("/dev/fsw0020/__IP__/f_cmd", Float64, self.set_freq)
        rospy.Subscriber("/dev/fsw0020/__IP__/power_cmd", Float64, self.set_power)
        rospy.Subscriber("/dev/fsw0020/__IP__/onoff_cmd", String, self.set_onoff)


        self.onoff_flag = 0
        self.freq_flag = 0
        self.power_flag = 0


    def set_freq(self,q):
        self.sg.freq_set(q.data)
        return

    def set_power(self,q):
        self.sg.power_set(q.data)
        return

    def set_onoff(self,q):
        self.sg.output_set(q.data)
        return



if __name__ == '__main__':
    rospy.init_node(name)
    sg = fsw0020()
    #sg.start_thread()
    rospy.spin()
