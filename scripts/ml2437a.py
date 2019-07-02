#! /usr/bin/env python3

name = "ml2437a"

import time
import sys
import ogameasure
import rospy
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int32

class ml2437a(object):
    def __init__(self):
        host = rospy.get_param("~host")
        gpibport = rospy.get_param("~gpibport")
        com = ogameasure.gpib_prologix(host, gpibport)

        self.pm = ogameasure.Anritsu.ml2437a(com)

        ave_onoff = rospy.get_param("~ave_onoff")
        ave_num = rospy.get_param("~ave_num")
        self.pm.set_average_onoff(ave_onoff)
        self.pm.set_average_count(ave_num)

        self.publist = [rospy.Publisher("/dev/ml2437a/__IP__/ch{0}".format(ch), Float64, queue_size=1) for ch in ch_num]

    def power(self,ch):
        power = self.pm.measure(ch)
        return power


if __name__ == '__main__':
    node = rospy.get_param("~node")
    ch_num = rospy.get_param("~ch")
    rospy.init_node(node)
    pm = ml2437a()

    while not rospy.is_shutdown():
        for ch in ch_num:
            power = pm.power(ch)
            self.publist[ch].publish(power)
        continue
