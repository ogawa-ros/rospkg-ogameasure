#! /usr/bin/env python3

name = 'n9349c'

import time
import sys
import ogameasure
import rospy
import threading
from std_msgs.msg import Float64MultiArray

class n9343c(object):

    def __init__(self):
        host = rospy.get_param("~host")
        port = rospy.get_param("~port")
        com = ogameasure.ethernet(host, port)
        self.sa = ogameasure.Keysight.N9343C(com)
        self.pub = rospy.Publisher("/dev/n9343c/__IP__/spec", Float64MultiArray, queue_size=1)

    def spec_publisher(self):
        while not rospy.is_shutdown():
            spec = self.sa.trace_data_query()
            self.pub.publish(spec.tolist())
            continue
        return

    def start_thread(self):
        th = threading.Thread(target=self.spec_publisher)
        th.setDaemon(True)
        th.start()
        
if __name__ == '__main__':
    rospy.init_node(name)

    spec = n9343c()
    spec.start_thread()
    rospy.spin()
