#! /usr/bin/env python3

node = "ma24126a"

import time
import sys
import ogameasure
import threading
import rospy
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int32

class ma24126a(object):
    def __init__(self):
        port_list = eval(rospy.get_param("~port_list"))
        self.pm = [ogameasure.Anritsu.ma24126a(port) for port in port_list]
        [rospy.Subscriber("/dev/ma24126a/__port__/zero_set/{0}".format(ch), Int32, self.zero_set, callback_args=ch) for ch in range(1,ch_num+1)]

        for ch in range(ch_num):
            self.pm[ch].start()

        self.switch = 1

    def switch(self,q):
        self.switch = q.data

    def power(self):
        while not rospy.is_shutdown():
            if self.switch == 0:
                time.sleep(0.001)
                continue
            elif self.switch == 1:
                for ch in range(0,ch_num):
                    time.sleep(0.1)
                    ret = self.pm[ch].power()
                    power = float(ret.decode().split('\n')[0])
                    publist[ch].publish(power)
            continue

    def zero_set(self, q, args):
        if q.data == 1:
            self.switch = 0
            time.sleep(0.1)
            print("##### usb power meter is doing zero setting now ####")
            self.pm[args-1].zero_set()
            print("##### usb power meter finished zero setting  ####")
            self.switch = 0
        else:
            pass
        return

    def start_thread(self):
        th = threading.Thread(target=self.power)
        th.setDaemon(True)
        th.start()



if __name__ == '__main__':
    rospy.init_node(node)
    ch_num = rospy.get_param("~ch_num")
    publist = [rospy.Publisher("/dev/ma24126a/__port__/{0}".format(ch), Float64, queue_size=1) for ch in range(1,ch_num+1)]

    usbpm = ma24126a()
    usbpm.start_thread()
    rospy.spin()
