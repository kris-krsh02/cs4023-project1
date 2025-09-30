#!/usr/bin/env python2

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String


class ManualNav:
    def __init__(self):
        rospy.init_node("nav_dispatcher", anonymous=True) # create nav_dispatcher node as intermediary for manual navigation
        self.pub = rospy.Publisher("/manual_nav", String, queue_size=1) # create corresponding topic for the layer
        # subscribe to custom topic, which turtlebot_teleop has been remapped to 
        self.sub = rospy.Subscriber("/custom_keyop", Twist, self.manual_nav) 
        rospy.spin() # keep node running

    def manual_nav(self, data):
        # User keyboard input
        linear_x = data.linear.x
        angular_z = data.angular.z

        # Do nothing if velocities are 0 (no user input)
        if linear_x == 0 and angular_z == 0:
            return

        # Publish user input velocity to layer topic
        vel_msg = "2\n" + str(linear_x) + "\n" + str(angular_z)
        self.pub.publish(vel_msg)
        rospy.sleep(0.1) 

        # Send signal to reset active action
        self.pub.publish('0\n0\n0')


if __name__ == "__main__":
    ManualNav = ManualNav()
