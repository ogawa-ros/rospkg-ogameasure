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
        self.loatt = []
        print(gpibport_list)
        for i in gpibport_list:
            gpibport = i
            print(gpibport)
            com = ogameasure.gpib_prologix(host, gpibport)
            lo = ogameasure.ELVA1.GPDVC15.GPDVC15_100(com)
            self.loatt.append(lo)
            time.sleep(1)
            print(self.loatt)

        """
        topic1 = "/dev/gpdvc15_100rs/ip_192_168_100_44/port_4/i_cmd"
        rospy.Subscriber(topic1, Float64, self.set_output,callback_args=0)
        time.sleep(1)
        print(topic1)
        topic2 = "/dev/gpdvc15_100rs/ip_192_168_100_44/port_5/i_cmd"
        rospy.Subscriber(topic2, Float64, self.set_output2,callback_args=1)
        time.sleep(1)
        print(topic2)

        """
        s = []
        d = [self.set_output, self.set_output2]
        for i ,port in enumerate(gpibport_list):
            topic = "/dev/gpdvc15_100rs/__IP__/port_%d/i_cmd"%(port)
            print(topic)
            print("args")
            print(i)
            print(port)
            #sub = rospy.Subscriber(topic, Float64, self.set_output, callback_args=i)
            sub = rospy.Subscriber(topic, Float64, d[i], callback_args=i)
            s.append(sub)
            print(s)
            time.sleep(1)


    def set_output(self,q,args):
        lo = self.loatt[0]
        time.sleep(1)
        print(lo)
        print(q.data)
        lo.output_set(q.data)

        return

    def set_output2(self,q,args):
        lo = self.loatt[1]
        time.sleep(1)
        print(q.data)
        print(lo)

        lo.output_set(q.data)

        return

if __name__ == "__main__" :
    rospy.init_node(name)
    host = rospy.get_param("~host")
    gpibport_list = eval(rospy.get_param("~gpibport_list"))
    att = GPDVC15_100()
    rospy.spin()
