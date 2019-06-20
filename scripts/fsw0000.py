#! /usr/bin/env python3

name = "fsw0000"

import time
import sys
from ogamesure import QuickSyn_FSW0000
import rospy
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int32

class fsw0000(self):
    def __init__(self):
        host = rospy.get_param("~host")
        port = rospy.get_param("~port")
        sg = QuickSyn_FSW0000.FSW0000(host,port)

        self.query_freq　= rospy.Publisher("/dev/fsw0000/ip/f_cmd",Float64,queue_size=1)
        self.query_power = rospy.Publisher("/dev/fsw0000/ip/p_cmd",Float64,queue_size=1)
        self.query_onoff = rospy.Publisher("/dev/fsw0000/ip/onoff_cmd",Float64,queue_size=1)
        rospy.Subscriber("/dev/fsw0000/ip/freq",Float64,self.set_freq)
        rospy.Subscriber("/dev/fsw0000/ip/power",Float64,self.set_power)
        rospy.Subscriber("/dev/fsw0000/ip/onoff",String,self.set_onoff)

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
    rospy.init_node("fsw0000")

    sg = fsw0000()
    rospy.spin()
