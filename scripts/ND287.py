#! /usr/bin/env python3

node = "ND287"

import time
import sys
import ogameasure
import rospy
import threading
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int32

class ND287(object):
    def __init__(self):
        self.az_count = 0
        az_port = rospy.get_param("~az_usbport")
        el_port = rospy.get_param("~el_usbport")
        self.encorder_az = ogameasure.HEIDENHAIN.ND287(az_port)
        self.encorder_el = ogameasure.HEIDENHAIN.ND287(el_port)
        self.pub_az = rospy.Publisher("/dev/ND287/__port__/az", Float64, queue_size=1)
        self.pub_el = rospy.Publisher("/dev/ND287/__port__/el", Float64, queue_size=1)
        self.az = self.get_az()

    def setting(self):
        self.encorder_az.press_key("soft1")
        self.encorder_az.press_key("soft1")
        self.encorder_az.press_key("9")
        self.encorder_az.press_key("5")
        self.encorder_az.press_key("1")
        self.encorder_az.press_key("4")
        self.encorder_az.press_key("8")
        self.encorder_az.press_key("ENT")
        self.encorder_az.press_key("down")
        self.encorder_az.press_key("down")
        self.encorder_az.press_key("ENT")
        self.encorder_az.press_key("NAVI")
        self.encorder_az.press_key("down")
        self.encorder_az.press_key("soft1")
        self.encorder_az.press_key("ENT")
        self.encorder_az.press_key("CLR")

    def pub_az(self):
        while not rospy.is_shutdown():
            az = self.az
            az2  = self.get_az()
            hensa = az2-az
            if hensa > 100:
                count = count - 1
            if hensa < -100:
                count = count + 1
            azaz = az2 + self.count*360
            self.pub_az.publish(float(azaz))
            self.az = az
            time.sleep(0.01)
            continue

    def get_az(self):
        _az = self.encorder_az.output_position_display_value()
        az = float(_az.strip(b"\x02\x00\r\n").decode())
        return az

    def get_el(self):
        while not rospy.is_shutdown():
            _el = self.encorder_el.output_position_display_value()
            el = float(_el.strip(b"\x02\x00\r\n").decode())
            self.pub_el.publish(float(el))
            time.sleep(0.01)
            continue

    def start_thread(self):
        th = threading.Thread(target = self.pub_az)
        th.setDaemon(True)
        th.start()
        check = threading.Thread(target = self.get_el)
        check.setDaemon(True)
        check.start()


if __name__ == '__main__':
    rospy.init_node(node)
    encorder = ND287()
    encorder.start_thread()
