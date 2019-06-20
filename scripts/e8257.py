#! /usr/bin/env python3

name = "e8257"

import time
import sys
from ogamesure import e8257
import rospy
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int32

class e8257(self):
    def __init__(self):
        host = rospy.get_param("~host")
        port = rospy.get_param("~port")
        sg = e8257.e8257(host,port)

        self.query_freq　= rospy.Publisher("/dev/e8257/ip/f_cmd", Float64, queue_size=1)
        self.query_power = rospy.Publisher("/dev/e8257/ip/p_cmd", Float64, queue_size=1)
        self.query_onoff = rospy.Publisher("/dev/e8257/ip/onoff_cmd", String, queue_size=1)
        rospy.Subscriber("/dev/e8257/ip/freq", Float64, self.set_freq)
        rospy.Subscriber("/dev/e8257/ip/power", Float64, self.set_power)
        rospy.Subscriber("/dev/e8257/ip/onoff", String, self.set_onoff)

    def set_freq(self,q):
        sg.freq_set(q.data)
        return

    def set_power(self,q):
        sg.power_set(q.data)
        return

    def query_freq(self):
        freq = sg.freq_query()
        self.query_freq.publish(freq)
        return

    def query_power(self):
        freq = sg.freq_query()
        self.query_freq.publish(freq)
        return

    def set_onoff(self):
        sg.output_set(q.data)
        return

    def query_onoff(self):
        onoff = sg.output_query()
        self.query_onoff.publish(onoff)
        return

if __name__ == '__main__':
    rospy.init_node(name)
    sg = e8257()
    rospy.spin()
