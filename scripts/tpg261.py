#! /usr/bin/env python3

name = "tpg261"

import time
import sys
import ogameasure
import rospy
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int32

class tpg261(object):
    def __init__(self):

        com = ogameasure.usb('FTHB88LO')
        self.tpg = ogameasure.Pfeiffer.tpg261(com)

        self.pub_p = rospy.Publisher("/tpg/pressure", String, queue_size=1)
        self.pub_s = rospy.Publisher("/tpg/state", String, queue_size=1)
        self.pub_t = rospy.Publisher("/tpg/turn", String, queue_size=1)
        self.pub_u = rospy.Publisher("/tpg/unit", String, queue_size=1)

    def query_pressure(self):
        p = self.tpg.pressure()        
        self.pub_p.publish(p)
        return

    def tpg_state(self):
        s = self.tpg.tpg_status()
        self.pub_s.publish(s)
        return

    def turn_state(self):
        c = self.tpg.turn_status_g1()
        self.pub_t.publish(c)
        return

    def tpg_on(self):
        self.tpg.gauge_on_g1()
        return

    def tpg_off(self):
        self.tpg.gauge_off_g1()
        return

    def change_unit_torr(self):
        selfpres_unit_bar()
        return

    def change_unit_torr(self):
        self.pres_unit_torr()
        return

    def check_unit_pa(self):
        self.pres_unit_pa()
        return

if __name__ == "__main__" :
    rospy.init_node("tpg261")
    tpg = tpg261_driver()
    thread_tpg = threading.Thread(target=tpg.query_pressure)
    thread_tpg.start()
    tpg.query_pressure()
