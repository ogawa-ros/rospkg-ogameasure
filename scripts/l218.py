#! /usr/bin/env python3

name = "l218"

import time
import sys
import ogameasure
import rospy
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int32

class l218(object):
    def __init__(self):
        host = rospy.get_param("~host")
        gpibport = rospy.get_param("~gpibport")
        com = ogameasure.gpib_prologix(host, gpibport)
        self.l218 = ogameasure.Lakeshore.model218(com)

        self.publist = [rospy.Publisher("/dev/218/__IP__/temp/ch{0}".format(ch), Float64, queue_size=1) for ch in range(1,ch_num+1)]

    def temp(self,ch=0):
        temp = self.l218.kelvin_reading_query(ch)
        return temp


if __name__ == '__main__':
    rospy.init_node(name)
    ch_num = rospy.get_param("~ch")

    l218 = l218()

    while not rospy.is_shutdown():
        for i in range(ch_num):
            temp = list(l218.temp())
            publist[ch].publish(temp[i])
        continue
