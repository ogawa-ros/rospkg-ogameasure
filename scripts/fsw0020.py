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
        self.sg = ogameasure.Phasematrix.FSW0020(com)


        rospy.Subscriber("/dev/fsw0020/__IP__/f_cmd", Float64, self.set_freq)
        rospy.Subscriber("/dev/fsw0020/__IP__/power_cmd", Float64, self.set_power)
        rospy.Subscriber("/dev/fsw0020/__IP__/onoff_cmd", String, self.set_onoff)

        self.freq_pub = rospy.Publisher("/dev/fsw0020/__IP__/freq",Float64,queue_size=1)

        self.flag = True

    def set_freq(self,q):
        self.flag = False
        self.sg.freq_set(q.data)
        time.sleep(1)
        self.flag = True
        return

    def set_power(self,q):
        self.flag = False
        self.sg.power_set(q.data)
        time.sleep(1)
        self.flag = True
        return

    def set_onoff(self,q):
        self.flag = False
        self.sg.output_set(q.data)
        time.sleep(1)
        self.flag = True
        return

    def query_freq(self):
        while not rospy.is_shutdown():
            if self.flag == False:
                time.sleep(0.1)
                continue
            elif self.flag == True:
                try:
                    f = self.sg.freq_query()
                    self.freq_pub.publish(float(f))
                    time.sleep(3)
                except:
                    pass
                continue
            else:
                pass
            continue

    def start_thread(self):
        th = threading.Thread(target = self.query_freq)
        th.setDaemon(True)
        th.start()


if __name__ == '__main__':
    rospy.init_node(name)
    sg = fsw0020()
    sg.start_thread()
    rospy.spin()
