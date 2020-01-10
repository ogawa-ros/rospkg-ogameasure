#! /usr/bin/env python3

node = 'tr_73u'

import time
import struct
import ogameasure
import threading

import rospy
from std_msgs.msg import Float64

class tr_73u(object):
    def __init__(self):
        port = rospy.get_param('~ondotori_usbport')
        self.ondotori = ogameasure.TandD.tr_73u(port)
        self.pub_temp = rospy.Publisher("/dev/TandD/__port__/temperature", Float64, queue_size=1)
        self.pub_humid = rospy.Publisher("/dev/TandD/__port__/humidity", Float64, queue_size=1)
        self.pub_press = rospy.Publisher("/dev/TandD/__port__/pressure", Float64, queue_size=1)
        time.sleep(0.01)


    def publish_data(self):
        while not rospy.is_shutdown():
            data = self.ondotori.output_current_data()
            self.pub_temp.publish(data[0])
            self.pub_humid.publish(data[1])
            self.pub_press.publish(data[2])
            time.sleep(5)
        return

    def start_thread(self):
        th = threading.Thread(target = self.publish_data)
        th.setDaemon(True)
        th.start()

if __name__ == '__main__':
    rospy.init_node(node)
    ondotori = tr_73u()
    ondotori.start_thread()
    rospy.spin()
