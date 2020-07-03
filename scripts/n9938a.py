#! /usr/bin/env python3

name = 'n9938a'

import time
import sys
import ogameasure
import rospy
import threading
from std_msgs.msg import Bool
from std_msgs.msg import Float64
from std_msgs.msg import Int32
from std_msgs.msg  import Float64MultiArray

class n9938a(object):

    def __init__(self):
        host = rospy.get_param("~host")
        port = rospy.get_param("~port")
        com = ogameasure.ethernet(host,port)
        self.sa = ogameasure.Keysight.N9938A(com)

        self.pub1 = rospy.Publisher("/dev/n9938a/__IP__/spec",Float64MultiArray,queue_size=1)

        rospy.Subscriber("/dev/n9938a/__IP__/freq_start_cmd", Float64, self.start_freq_set)
        rospy.Subscriber("/dev/n9938a/__IP__/freq_stop_cmd", Float64, self.stop_freq_set)
        rospy.Subscriber("/dev/n9938a/__IP__/freq_center_cmd", Float64, self.center_freq_set)

        rospy.Subscriber("/dev/n9938a/__IP__/rbw_set_cmd", Float64, self.resol_bw_set)
        self.pub2 = rospy.Publisher("/dev/n9938a/__IP__/rbw_query_cmd",Float64MultiArray,queue_size=1)
        #rospy.Subscriber("/dev/n9938a/__IP__/rbw_query_cmd", Float64, self.resol_bw_query)

        rospy.Subscriber("/dev/n9938a/__IP__/vbw_set_cmd", Float64, self.vid_bw_set)
        self.pub3 = rospy.Publisher("/dev/n9938a/__IP__/vbw_query_cmd",Float64MultiArray,queue_size=1)
        #rospy.Subscriber("/dev/n9938a/__IP__/vbw_query_cmd", Float64, self.vid_bw_query)

        rospy.Subscriber("/dev/n9938a/__IP__/rbw_auto_cmd", Int32, self.resol_bw_auto_set)

        self.flag = True




    def spec_publisher(self):
        while not rospy.is_shutdown():
            if self.flag == True:
                spec = Float64MultiArray(data=self.sa.trace_data_query())
                self.pub1.publish(spec)
            else:
                pass
            time.sleep(0.1)
            continue
        return

    def start_freq_set(self,startf):
        self.flag = False
        time.sleep(0.3)
        self.sa.frequency_start_set(startf.data)
        time.sleep(0.1)
        self.flag = True
        return

    def stop_freq_set(self,stopf):
        self.flag = False
        time.sleep(0.3)
        self.sa.frequency_stop_set(stopf.data)
        time.sleep(0.1)
        self.flag = True
        return

    def center_freq_set(self,centerf):
        self.flag = False
        time.sleep(0.3)
        self.sa.frequency_center_set(centerf.data)
        time.sleep(0.1)
        self.flag = True
        return


    def resol_bw_set(self,rbw):
        self.flag = False
        time.sleep(0.3)
        self.sa.resolution_bw_set(rbw.data)
        time.sleep(0.1)
        self.flag = True
        return

        """
    def resol_bw_query(self):
        self.flag = False
        time.sleep(0.3)
        ret = self.sa.resolution_bw_query()
        time.sleep(0.1)
        self.flag = True
        return ret
        """
    def resol_bw_query(self):

        self.flag = False
        time.sleep(0.3)
        ret = self.sa.resolution_bw_query()
        self.pub2.publish(ret)
        time.sleep(0.1)
        self.flag = True
        return ret


    def vid_bw_set(self,vbw):
        self.flag = False
        time.sleep(0.3)
        self.sa.video_bw_set(vbw.data)
        time.sleep(0.1)
        self.flag = True
        return

        """
    def vid_bw_query(self):
        self.flag = False
        time.sleep(0.3)
        ret = self.sa.video_bw_query()
        time.sleep(0.1)
        self.flag = True
        return ret
        """

    def vid_bw_query(self):

        self.flag = False
        time.sleep(0.3)
        ret = self.sa.video_bw_query()
        self.pub3.publish(ret)
        time.sleep(0.1)
        self.flag = True
        return ret



    def resol_bw_auto_set(self,auto):
        self.flag = False
        time.sleep(0.3)
        self.sa.resolution_bw_auto_set(auto)
        time.sleep(0.1)
        self.flag = True
        return



    def start_thread(self):
        th = threading.Thread(target=self.spec_publisher)
        th.setDaemon(True)
        th.start()


if __name__ == '__main__':
    rospy.init_node(name)

    spec = n9938a()
    spec.start_thread()
    rospy.spin()
