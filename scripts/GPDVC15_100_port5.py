#! /usr/bin/env python3

name = "GPDVC15_port5"

import time
import sys
import ogameasure
import rospy
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int32

class GPDVC15_100(object):

    def __init__(self):

        com = ogameasure.gpib_prologix(host, gpibport)
        loatt = ogameasure.ELVA1.GPDVC15.GPDVC15_100(com)


        topic = "/dev/gpdvc15_100rs/__IP__/port_5/i_cmd"
        rospy.Subscriber(topic, Float64, self.set_output)

    def set_output(self,q):
        loatt.output_set(q.data)
        return


if __name__ == "__main__" :
    rospy.init_node(name)
    host = rospy.get_param("~host")
    gpibport = eval(rospy.get_param("~gpibport"))
    loatt = GPDVC15_100()
    rospy.spin()
