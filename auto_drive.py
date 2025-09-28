#!/usr/bin/env python2

import rospy
from std_msgs.msg import String

class AutoDrive:
    def __init__(self):
        rospy.init_node("auto_drive", anonymous=True)
        pub = rospy.Publisher("/auto_drive", String, queue_size=10)
        rate = rospy.Rate(3)
        while not rospy.is_shutdown():
            msg = '6\n0.1\n0'
            pub.publish(msg)
            rate.sleep()

            
if __name__ == "__main__":
    AutoDrive = AutoDrive()