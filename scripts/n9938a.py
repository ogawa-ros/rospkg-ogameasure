#! /usr/bin/env python3

name = 'n9938a'

import time
import sys
import ogameasure
import rospy
import threading
from std_msgs.msg import Float64
from std_msgs.msg  import Float64MultiArray

class n9938a(object):

    def __init__(self):
        host = rospy.get_param("~host")
        port = rospy.get_param("~port")
        com = ogameasure.ethernet(host,port)
        self.sa = ogameasure.Keysight.N9938A(com)

        self.pub = rospy.Publisher("/dev/n9938a/__IP__/spec",Float64MultiArray,queue_size=1)
        rospy.Subscriber("/dev/n9938a/__IP__/freq_start_cmd", Float64, self.start_freq_set)
        rospy.Subscriber("/dev/n9938a/__IP__/freq_stop_cmd", Float64, self.stop_freq_set)
        rospy.Subscriber("/dev/n9938a/__IP__/freq_center_cmd", Float64, self.center_freq_set)
        self.flag = True


    def spec_publisher(self):
        while not rospy.is_shutdown():
            if self.flag == True:
                spec = Float64MultiArray(data=self.sa.trace_data_query())
                self.pub.publish(spec)
            else:
                pass
            time.sleep(0.001)
            continue
        return

    def start_freq_set(self,startf):
        self.flag = False
        time.sleep(0.01)
        self.sa.frequency_start_set(startf.data)
        time.sleep(0.1)
        self.flag = True
        return

    def stop_freq_set(self,stopf):
        self.flag = False
        time.sleep(0.01)
        self.sa.frequency_stop_set(stopf.data)
        time.sleep(0.1)
        self.flag = True
        return

    def center_freq_set(self,centerf):
        self.flag = False
        time.sleep(0.01)
        self.sa.frequency_center_set(centerf.data)
        time.sleep(0.1)
        self.flag = True
        return


    def start_thread(self):
        th = threading.Thread(target=self.spec_publisher)
        th.setDaemon(True)
        th.start()


if __name__ == '__main__':
    rospy.init_node(name)

    spec = n9938a()
    spec.start_thread()
    rospy.spin()
