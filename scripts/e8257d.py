#! /usr/bin/env python3

name = "e8257d"

import time
import sys
import threading
import ogameasure
import rospy
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int32

class e8257(object):
    def __init__(self):
        host = rospy.get_param("~host")
        port = rospy.get_param("~port")
        com = ogameasure.ethernet(host, port)
        self.sg = ogameasure.Agilent.E8257D(com)

        self.pub_freq = rospy.Publisher("/dev/e8257d/__IP__/freq", Float64, queue_size=1)
        self.pub_power = rospy.Publisher("/dev/e8257d/__IP__/power", Float64, queue_size=1)
        self.pub_onoff = rospy.Publisher("/dev/e8257d/__IP__/onoff", String, queue_size=1)
        rospy.Subscriber("/dev/e8257d/__IP__/freq_cmd", Float64, self.set_freq)
        rospy.Subscriber("/dev/e8257d/__IP__/power_cmd", Float64, self.set_power)
        rospy.Subscriber("/dev/e8257d/__IP__/onoff_cmd", String, self.set_onoff)

    def set_freq(self,q):
        self.sg.freq_set(q.data)
        return

    def set_power(self,q):
        self.sg.power_set(q.data)
        return

    def query_freq(self):
        freq = self.sg.freq_query()
        self.pub_freq.publish(freq)
        return

    def query_power(self):
        power = self.sg.power_query()
        self.pub_power.publish(power)
        return

    def set_onoff(self):
        self.sg.output_set(q.data)
        return

    def query_onoff(self):
        onoff = self.sg.output_query()
        self.pub_onoff.publish(onoff)
        return

    def publish_data(self):
        while not rospy.is_shutdown():
            self.query_freq()
            self.query_power()
            #self.query_onoff()
            time.sleep(0.01)
            continue

    def start_thread(self):
        th = threading.Thread(target=self.publish_data)
        th.setDaemon(True)
        th.start()


if __name__ == '__main__':
    rospy.init_node(name)
    sg = e8257()
    sg.start_thread()
    rospy.spin()
