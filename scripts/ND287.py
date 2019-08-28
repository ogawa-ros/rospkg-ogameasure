#! /usr/bin/env python3

node = "ND287"

import time
import sys
import ogameasure
import rospy
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int32

class ND287(object):
    def __init__(self):
        az_port = rospy.get_param("~az_usbport")
        el_port = rospy.get_param("~el_usbport")
        self.encorder_az = ogameasure.HEIDENHAIN.ND287(az_port)
        #self.encorder_el = ogameasure.HEIDENHAIN.ND287(el_port)

    def set_display(self):
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

    def get_az(self):
        _az = self.encorder_az.output_position_display_value()
        az = float(_az.strip(b"\x02\x00\r\n").decode())
        return az

    def get_el(self):
        _el = self.encorder_el.output_position_display_value()
        el = float(_el.strip(b"\x02\x00\r\n").decode())
        return el


if __name__ == '__main__':
    rospy.init_node(node)
    pub_az = rospy.Publisher("/dev/ND287/__port__/az", Float64, queue_size=1)
    pub_el = rospy.Publisher("/dev/ND287/__port__/el", Float64, queue_size=1)

    encorder = ND287()
    encorder.set_display()
    while not rospy.is_shutdown():
        ret = encorder.get_az()
        pub_az.publish(float(az))
        continue
