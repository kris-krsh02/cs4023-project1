#!/usr/bin/env python2

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String


class ManualNav:
    def __init__(self):
        rospy.init_node("nav_dispatcher", anonymous=True)
        self.pub = rospy.Publisher("/manual_nav", String, queue_size=1)
        self.sub = rospy.Subscriber("/custom_keyop", Twist, self.manual_nav)
        rospy.spin()

    def manual_nav(self, data):
        linear_x = data.linear.x
        angular_z = data.angular.z

        if linear_x == 0 and angular_z == 0:
            return

        vel_msg = "2\n" + str(linear_x) + "\n" + str(angular_z)
        self.pub.publish(vel_msg)
        rospy.sleep(0.1)


if __name__ == "__main__":
    ManualNav = ManualNav()
