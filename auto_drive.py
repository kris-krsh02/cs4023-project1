#!/usr/bin/env python2

import rospy
from geometry_msgs.msg import Twist

class AutoDrive:
    def __init__():
        rospy.init_node("auto_drive", anonymous=True)
        pub = rospy.Publisher("/cmd_vel_mux/input/navi", Twist, queue_size=10)
        vel = Twist()
        vel.linear.x = 0.2
        vel.angular.z = 0
        rate = rospy.Rate(3)
        while not rospy.is_shutdown():
            pub.publish(vel)
            print("Velocity " + str(vel))
            rate.sleep()
