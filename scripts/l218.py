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
        print(host)
        print(gpibport)
        self.l218 = ogameasure.Lakeshore.model218(com)

        self.publist = [rospy.Publisher("/dev/218/__IP__/temp/ch{0}".format(ch), Float64, queue_size=1) for ch in range(1,ch_num+1)]

    def temp_publisher(self,ch=0):
        while not rospy.is_shutdown():
            for i in range(ch_num):
                temp = list(self.l218.kelvin_reading_query(ch=0))
                self.pub_list[i].publish(temp[i])
            continue

    def start_thread(self):
        th = threading.Thread(target=self.temp_publisher)
        th.setDaemon(True)
        th.start()

if __name__ == '__main__':
    rospy.init_node(name)
    ch_num = rospy.get_param("~ch")


    temp = l218()
    temp.start_thread()
    rospy.spin()
