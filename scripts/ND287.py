#! /usr/bin/env python3

node = "ND287"

import time
import sys
import ogameasure
import rospy
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int32

class ma24126a(object):
    def __init__(self):
        az_port = eval(rospy.get_param("~az_usbport"))
        el_port = eval(rospy.get_param("~el_usbport"))
        self.encorder_az = ogameasure.HAIDENHAIN.ND278(az_port)
        #self.encorder_el = ogameasure.HAIDENHAIN.ND278(el_port)

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
        return az

    def get_el(self):
        _el = self.encorder_el.output_position_display_value()
        return el


if __name__ == '__main__':
    rospy.init_node(node)
    ch_num = rospy.get_param("~ch_num")
    publist = [rospy.Publisher("/dev/ma24126a/__port__/ch{0}".format(ch), Float64, queue_size=1) for ch in range(1,ch_num+1)]
    usbpm = ma24126a()


    while not rospy.is_shutdown():
        for ch in range(0,ch_num):
            time.sleep(0.1)
            ret = usbpm.power(ch)
            power = float(ret.decode().split('\n')[0])
            publist[ch].publish(power)
        continue
