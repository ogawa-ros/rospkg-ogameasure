#! /usr/bin/env python3

name = "GPDVC15"

import time
import sys
import ogameasure
import rospy
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int32

class GPDVC15(self):
    def __init__(self):
        host = rospy.get_param("~host")
        gpibport = rospy.get_param("~gpibport")
        com = ogameasure.gpib_prologix(host, gpibport)
        self.loatt = ogameasure.ELVA1.GPDVC15(com)
        rospy.Subscriber("/dev/GPDVC15/ip/onoff", String, self.set_output)

    def set_output(self):
        self.loatt.output_set(q.data)
        return

if __name__ == '__main__':
    node = rospy.get_param("~node")
    rospy.init_node(name)
    loatt = GPDVC15()
    rospy.spin()
