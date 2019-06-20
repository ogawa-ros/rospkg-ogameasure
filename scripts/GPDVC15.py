#! /usr/bin/env python3

name = "GPDVC15"

import time
import sys
from ogamesure import GPDVC15
import rospy
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int32

class GPDVC15(self):
    def __init__(self):
        host = rospy.get_param("~host")
        port = rospy.get_param("~port")
        loatt = GPDVC15.GPDVC15(host,port)
        rospy.Subscriber("/dev/GPDVC15/ip/onoff", String, self.set_output)

    def set_output(self):
        loatt.output_set(q.data)
        return

if __name__ == '__main__':
    node = rospy.get_param("~node")
    rospy.init_node(name)
    loatt = GPDVC15()
    rospy.spin()
