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
        host = "192.168.100.44"
        #host = rospy.get_param("~host")
        gpibport_list = eval("[4,5]")
        #gpibport_list = eval(rospy.get_param("~gpibport_list"))
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

        topic1 = "/dev/gpdvc15_100rs/ip_192_168_100_44/port_4/i_cmd"
        rospy.Subscriber(topic1, Float64, self.set_output, callback_args=0)
        time.sleep(1)
        print(topic1)
        topic2 = "/dev/gpdvc15_100rs/ip_192_168_100_44/port_5/i_cmd"
        rospy.Subscriber(topic2, Float64, self.set_output, callback_args=1)
        time.sleep(1)
        print(topic2)


        #for i ,port in enumerate(gpibport_list):
            #topic = "/dev/gpdvc15_100rs/ip_192_168_100_44/port_%d/i_cmd"%(port)
            #topic = "/dev/gpdvc15_100rs/__IP__/port_%d/i_cmd"%(port)
            #print(topic)
            #print("args")
            #print(i)
            #print(port)
            #rospy.Subscriber(topic, Float64, self.set_output, callback_args=1)
            #time.sleep(1)

    def set_output(self,q,args):
        lo = self.loatt[args]
        time.sleep(1)
        msg = Float64()
        msg = q.data
        print(lo)
        print(q.data)
        lo.output_set(msg)
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
