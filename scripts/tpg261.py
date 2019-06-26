import rospy, os, sys, time, serial, threading, std_msgs.msg
from ogamesure import tpg261_device


class tpg261_driver(object):
    def __init__(self):

        self.pub_p = rospy.Publisher("/tpg_pressure", Float64, queue_size=1)
        self.pub_s = rospy.Publisher("/tpg_state", String, queue_size=1)
        self.pub_u = rospy.Publisher("/tpg_unit", String, queue_size=1)


    def query_pressure(self):
        p = pressure()        
        self.pub_p(p)

    def query_state(self):
        s = pressure_error()
        self.pub_s(s)

    def check_state(self):
        c = check()
        self.pub_s(c)

    def change_unit_torr(self):
        t = pres_unit_torr()
        self.pub_u(t)

    def check_unit_pa(self):
        a = pres_unit_pa()
        self.pub_u(a)

if __name__ == "__main__" :
    rospy.init_node("tpg261")
    tpg = tpg261_driver()
    thread_tpg = threading.Thread(target=tpg.query_pressure)
    thread_tpg.start()
    tpg.query_pressure()
