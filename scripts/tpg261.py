#! /usr/bin/env python3

name = "tpg261"

import time, sys, rospy, threading, ogameasure
from std_msgs.msg import Float64
from std_msgs.msg import String

class tpg261(object):
    def __init__(self):

        serial = rospy.get_param("~serial")
        com = ogameasure.usb(serial)
        self.tpg = ogameasure.Pfeiffer.tpg261(com)

        self.pub_p = rospy.Publisher("/dev/tpg/FTHB88LO/pressure", Float64, queue_size=1)
        self.pub_s = rospy.Publisher("/dev/tpg/FTHB88LO/state", String, queue_size=1)
        self.pub_t = rospy.Publisher("/dev/tpg/FTHB88LO/turn", String, queue_size=1)

    def query_pressure(self):
        while not rospy.is_shutdown():
            p = self.tpg.pressure()
            self.pub_p.publish(p)

    def tpg_state(self):
        s = self.tpg.tpg_status()
        self.pub_s.publish(s)

    def turn_state(self):
        c = self.tpg.turn_status_g1()
        self.pub_t.publish(c)

    def tpg_on(self):
        self.tpg.gauge_on_g1()

    def tpg_off(self):
        self.tpg.gauge_off_g1()

    def change_unit_torr(self):
        selfpres_unit_bar()

    def change_unit_torr(self):
        self.pres_unit_torr()

    def check_unit_pa(self):
        self.pres_unit_pa()

if __name__ == "__main__" :
    rospy.init_node(name)
    tpg = tpg261()
    thread_tpg = threading.Thread(target=tpg.query_pressure)
    thread_tpg.start()
    tpg.query_pressure()
    rospy.spin()
