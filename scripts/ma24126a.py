#! /usr/bin/env python3

node = "ma24126a"

import time
import sys
import ogameasure
import rospy
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int32

class ma24126a(object):
    def __init__(self):
        port_list = eval(rospy.get_param("~port_list"))
        self.pm = [ogameasure.Anritsu.ma24126a(port) for port in port_list]
        [rospy.Subscriber("/dev/ma24126a/__port__/zero_set/ch{0}".format(ch), Int32, self.zero_set, callback_args=ch) for ch in range(1,ch_num+1)]

        for ch in range(ch_num):
            self.pm[ch].start()

    def power(self,ch):
        power = self.pm[ch].power()
        return power

    def zero_set(self, q, args):
        if q.data == 1:
            print("##### usb power meter is doing zero setting now ####")
            self.pm[args-1].zero_set()
            print("##### usb power meter finished zero setting  ####")
        else:
            pass
        return




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
