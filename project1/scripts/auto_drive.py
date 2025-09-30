#!/usr/bin/env python2

import rospy
from std_msgs.msg import String

class AutoDrive:
    def __init__(self):
        rospy.init_node("auto_drive", anonymous=True) # create auto_drive node
        pub = rospy.Publisher("/auto_drive", String, queue_size=10) # create corresponding topic for the layer
        rate = rospy.Rate(3) # publish at rate 3Hz

        # Publish while rospy is running
        while not rospy.is_shutdown():
            msg = '6\n0.2\n0'
            pub.publish(msg)
            rate.sleep()

            
if __name__ == "__main__":
    AutoDrive = AutoDrive()