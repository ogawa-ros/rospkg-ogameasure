#! /usr/bin/env python3

name = "GPDVC15"

import time
import sys
import ogameasure
import rospy
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int32

class GPDVC15_100(object):
    def __init__(self):
        host = rospy.get_param("~host")
        gpibport_list = eval(rospy.get_param("~gpibport_list"))
        com_list = []
        self.loatt = []
        for i in gpibport_list:
            gpibport = i
            com = ogameasure.gpib_prologix(host, gpibport)
            com_list.append(com)
            loatt = ogameasure.ELVA1.GPDVC15.GPDVC15_100(com)
            self.loatt.append(loatt)

        for i ,port in enumerate(gpibport_list):
            topic = "/dev/gpdvc15_100rs/__IP__/port_%d/i_cmd"%(i)
            rospy.Subscriber(topic, String, self.set_output, callback_args=i)

    def set_output(self,q,args):
        self.loatt[args].output_set(q.data)
        return

if __name__ == '__main__':
    rospy.init_node(name)
    node = rospy.get_param("~node")
    loatt = GPDVC15_100()
    rospy.spin()
