#! /usr/bin/env python3

name = 'pmx18_2A'

import time
import sys
import ogameasure
import rospy
import threading
from std_msgs.msg import Float64
from std_msgs.msg import Int32
from std_msgs.msg import Float64
from std_msgs.msg import Bool

class pmx18_2A(object):

    def __init__(self):
        host = rospy.get_param("~host")
        port = rospy.get_param("~port")
        com = ogameasure.ethernet(host,port)
        self.ps = ogameasure.KIKUSUI.PMX18_2A(com)

        self.pub_onoff = rospy.Publisher("/dev/pmx18/__IP__/onoff",Int32,queue_size=1)
        self.pub_curr = rospy.Publisher("/dev/pmx18/__IP__/curr",Float64,queue_size=1)
        self.pub_volt = rospy.Publisher("/dev/pmx18/__IP__/volt",Float64,queue_size=1)


        rospy.Subscriber("/dev/pmx18/__IP__/curr_cmd",Float64, self.current_set)
        rospy.Subscriber("/dev/pmx18/__IP__/volt_cmd",Float64, self.volt_set)
        rospy.Subscriber("/dev/pmx18/__IP__/output_on_cmd",Float64, self.output_on_set)
        rospy.Subscriber("/dev/pmx18/__IP__/output_off_cmd",Float64, self.output_off_set)

        self.flag = True

    def parameter_publisher(self):
        while not rospy.is_shutdown():
            if self.flag == True:
                onoff = int(self.ps.query_output_onoff())
                current = float(self.ps.query_A())
                voltage = float(self.ps.query_V())
                self.pub_onoff.publish(onoff)
                self.pub_curr.publish(current)
                self.pub_volt.publish(voltage)
            else:
                pass
            time.sleep(0.01)
            continue
        return


    def output_on_set(self,q):
        self.flag = False
        self.ps.set_ON()
        time.sleep(0.01)
        self.flag = True
        return

    def output_off_set(self,q):
        self.flag = False
        self.ps.set_OFF()
        time.sleep(0.01)
        self.flag = True
        return

    def current_set(self,curr):
        self.flag = False
        self.ps.set_A(curr.data)
        time.sleep(0.01)
        self.flag = True
        return

    def volt_set(self,volt):
        self.flag = False
        self.ps.set_V(volt.data)
        time.sleep(0.01)
        self.flag = True
        return

    def start_thread(self):
        th = threading.Thread(target=self.parameter_publisher)
        th.setDaemon(True)
        th.start()



if __name__ =='__main__':
    rospy.init_node(name)

    param = pmx18_2A()
    param.start_thread()
    rospy.spin()
