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

        self.loatt = []
        for i in gpibport_list:
            gpibport = i
            com = ogameasure.gpib_prologix(host, gpibport)
            lo = ogameasure.ELVA1.GPDVC15.GPDVC15_100(com)
            self.loatt.append(lo)

        for i, port in enumerate(gpibport_list):
            topic = "/dev/gpdvc15_100rs/__IP__/port_%d/i_cmd"%(port)
            sub = rospy.Subscriber(topic, Float64, self.set_output, callback_args=i)

    def set_output(self,q,args):
        lo = self.loatt[args]
        lo.com.open()
        loatt.output_set(q.data)
        lo.com.close()
        return


if __name__ == "__main__" :
    rospy.init_node(name)
    host = rospy.get_param("~host")
    gpibport_list = eval(rospy.get_param("~gpibport_list"))
    att = GPDVC15_100()
    rospy.spin()
