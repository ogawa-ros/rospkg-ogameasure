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
        print("nandeya")
        host = rospy.get_param("~host")
        gpibport_list = eval(rospy.get_param("~gpibport_list"))
        self.loatt = []
        print(gpibport_list)
        for i in gpibport_list:
            gpibport = i
            print(gpibport)
            com = ogameasure.gpib_prologix(host, gpibport)
            loatt = ogameasure.ELVA1.GPDVC15.GPDVC15_100(com)
            self.loatt.append(loatt)
            time.sleep(1)
        print(self.loatt)

        for i ,port in enumerate(gpibport_list):
            topic = "/dev/gpdvc15_100rs/__IP__/port_%d/i_cmd"%(port)
            print(topic)
            rospy.Subscriber(topic, Float64, self.set_output, callback_args=i)

    def set_output(self,q,args):
        lo = self.loatt[args]
        time.sleep(1)
        lo.output_set(q.data)
        print(args)
        print(lo)
        print(q)
        return

if __name__ == "__main__" :
    print("1")
    rospy.init_node(name)
    print("2")
    loatt = GPDVC15_100()
    print("3")
    rospy.spin()
