#! /usr/bin/env python3

name = "e8247"

import time
import sys
import ogameasure
import rospy
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int32

class e8247(self):
    def __init__(self):
        host = rospy.get_param("~host")
        port = rospy.get_param("~port")
        com = ogameasure.ethernet(host,port)
        self.sg = ogameasure.Agilent.E8247C(com)

        self.query_freq　= rospy.Publisher("/dev/e8247/ip/f_cmd", Float64, queue_size=1)
        self.query_power = rospy.Publisher("/dev/e8247/ip/p_cmd", Float64, queue_size=1)
        self.query_onoff = rospy.Publisher("/dev/e8247/ip/onoff_cmd", String, queue_size=1)
        rospy.Subscriber("/dev/e8247/ip/freq", Float64, self.set_freq)
        rospy.Subscriber("/dev/e8247/ip/power", Float64, self.set_power)
        rospy.Subscriber("/dev/e8247/ip/onoff", String, self.set_onoff)

    def set_freq(self,q):
        self.sg.freq_set(q.data)
        return

    def set_power(self,q):
        self.sg.power_set(q.data)
        return

    def query_freq(self):
        freq = self.sg.freq_query()
        self.query_freq.publish(freq)
        return

    def query_power(self):
        freq = self.sg.freq_query()
        self.query_freq.publish(freq)
        return

    def set_onoff(self):
        self.sg.output_set(q.data)
        return

    def query_onoff(self):
        onoff = self.sg.output_query()
        self.query_onoff.publish(onoff)
        return

if __name__ == '__main__':
    rospy.init_node(name)
    sg = e8247()
    rospy.spin()
