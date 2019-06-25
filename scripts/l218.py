#! /usr/bin/env python3

name = "l218"

import time
import sys
import ogameasure
import rospy
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int32

class l218(self):
    def __init__(self):
        host = rospy.get_param("~host")
        gpibport = rospy.get_param("~gpibport")
        com = ogameasure.gpib_prologix(host, gpibport)
        self.l218 = ogameasure.Lakeshore.model218(com)

        publist = [rospy.Publisher("/dev/218/ip/temp/ch{0}".format(ch), Float64, queue_size=1) for ch in ch_num]

    def temp(self,ch):
        temp = self.l218.kelvin_reading_query(ch)
        return temp


if __name__ == '__main__':
    node = rospy.get_param("~node")
    ch_num = rospy.get_param("~ch")
    rospy.init_node(name)
    l218 = l218()
    rospy.spin()

    while not rospy.is_shutdown():
        for i in ch_num:
            temp = l218.temp(ch)
            publist[ch].publish(temp)
        continue
