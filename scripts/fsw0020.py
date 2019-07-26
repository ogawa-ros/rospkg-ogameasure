#! /usr/bin/env python3

name = "fsw0020"

import time
import sys
import ogameasure
import rospy
import threading
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int32

class fsw0020(object):
    def __init__(self):
        host = rospy.get_param("~host")
        port = rospy.get_param("~port")
        com = ogameasure.ethernet(host, port)
        self.sg = ogameasure.Phasematrix.FSW0010(com)

        self.query_freq = rospy.Publisher("/dev/fsw0020/__IP__/freq", Float64, queue_size=1)
        self.query_power = rospy.Publisher("/dev/fsw0020/__IP__/power", Float64, queue_size=1)
        self.query_onoff = rospy.Publisher("/dev/fsw0020/__IP__/onoff", String, queue_size=1)
        rospy.Subscriber("/dev/fsw0020/__IP__/freq_cmd", Float64, self.set_freq)
        rospy.Subscriber("/dev/fsw0020/__IP__/power_cmd", Float64, self.set_power)
        rospy.Subscriber("/dev/fsw0020/__IP__/onoff_cmd", String, self.set_onoff)


        self.onoff_flag = 0
        self.freq_flag = 0
        self.power_flag = 0


    def set_freq(self,q):
        self.sg.freq_set(q.data)
        return

    def set_power(self,q):
        self.sg.power_set(q.data)
        return

    def set_onoff(self):
        self.sg.output_set(q.data)
        return

    def query_freq(self):
        while not rospy.is_shutdown():
            time.sleep(10)
            freq = self.sg.freq_query()
            self.query_freq.publish(freq)
            continue

    def query_power(self):
        while not rospy.is_shutdown():
            time.sleep(10)
            power = self.sg.power_query()
            self.query_power.publish(power)
            continue

    def query_onoff(self):
        while not rospy.is_shutdown():
            time.sleep(10)
            freq = self.sg.output_query()
            self.query_onoff.publish(onoff)
            continue


    """
    def query_onoff(self):
        while not rospy.is_shutdown():
            if self.onoff_flag == 0:
                time.sleep(10)
                continue
            else:
                onoff = self.sg.output_query()
                self.query_onoff.publish(onoff)
                self.onoff_flag == 0
            continue

    def query_freq(self):
        while not rospy.is_shutdown():
            if self.freq_flag == 0:
                continue
            else:
                onoff = self.sg.freq_query()
                self.query_freq.publish(onoff)
                self.freq_flag == 0
            continue

    def query_freq(self):
        while not rospy.is_shutdown():
            if self.power_flag == 0:
                continue
            else:
                onoff = self.sg.power_query()
                self.query_power.publish(onoff)
                self.power_flag == 0
            continue
    """
    def start_thread(self):
        th = threading.Thread(target=self.query_onoff)
        th.setDaemon(True)
        th.start()
        th = threading.Thread(target=self.query_power)
        th.setDaemon(True)
        th.start()
        th = threading.Thread(target=self.query_freq)
        th.setDaemon(True)
        th.start()

if __name__ == '__main__':
    rospy.init_node(name)
    sg = fsw0020()
    sg.start_thread()
    rospy.spin()
