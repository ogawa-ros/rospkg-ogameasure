#! /usr/bin/env python3

name = "adios"

import sys
import time
import queue
import threading

import rospy
from std_msgs.msg import Int32
from std_msgs.msg import String
from std_msgs.msg import Int32

import ogameasure

class adios(object):
    def __init__(self):
        self.func_queue = queue.Queue()

        host = rospy.get_param("~host")
        port = rospy.get_param("~port")
        com = ogameasure.ethernet(host, port)
        self.att = ogameasure.SENA.adios(com)

        rospy.Subscriber("/dev/adios/__IP__/att1_cmd", Int32, self.regist_set_att, callback_args=1)
        rospy.Subscriber("/dev/adios/__IP__/att2_cmd", Int32, self.regist_set_att, callback_args=2)
        self.pub1 = rospy.Publisher("/dev/adios/__IP__/att1", Int32 , queue_size=1)
        self.pub2 = rospy.Publisher("/dev/adios/__IP__/att2", Int32 , queue_size=1)
        time.sleep(0.5)

        self.th = threading.Thread(target=self.loop)
        self.th.setDaemon(True)
        self.th.start()
        return


    def loop(self):
        while not rospy.is_shutdown():
            power1 = self.att.get_att1()
            time.sleep(0.01)
            power2 = self.att.get_att2()
            time.sleep(0.01)

            self.pub1.publish(power1)
            self.pub2.publish(power2)

            if not self.func_queue.empty():
                f = self.func_queue.get()
                f['func'](f['data'], f['num'])
            else:
                pass

            time.sleep(1)
            continue

    def regist_set_att(self, req, args):
        self.func_queue.put({'func': self.set_att, 'data': req.data, 'num': args})
        pass

    def set_att(self, data, num):
        self.att._set_att(num, data)
        return

if __name__ == '__main__':
    rospy.init_node(name)
    att = adios()
    rospy.spin()
