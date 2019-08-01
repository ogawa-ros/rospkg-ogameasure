#! /usr/bin/env python3

name = "11713B"

import time
import sys
import ogameasure
import rospy
from std_msgs.msg import Int32

class agilent_11713B(object):

    def __init__(self):
        host = rospy.get_param("~host")
        port = rospy.get_param("~port")
        com = ogameasure.gpib_prologix(host, port)
        self.sw = ogameasure.Agilent.agilent_11713B(com)

        rospy.Subscriber("/dev/87104b/__IP__/open_ch_cmd", Int32, self.switch_open)
        rospy.Subscriber("/dev/87104b/__IP__/close_ch_cmd", Int32, self.switch_close)

    def switch_open(self, q):
        self.sw.switch_open(q.data)
        return

    def switch_close(self, q):
        self.sw.switch_close(q.data)
        return


if __name__ == "__main__":
    rospy.init_node(name)
    sw = agilent_11713B()
    rospy.spin()
