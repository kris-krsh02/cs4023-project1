#!/usr/bin/env python2

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from kobuki_msgs.msg import BumperEvent


class BumperHalter:
    def __init__(self):
        rospy.init_node("bumper_halter", anonymous=True) # create bumper_halter node
        self.pub = rospy.Publisher("/bumper_halter", String, queue_size=1) # create corresponding topic for the layer

        self.sub = rospy.Subscriber(
            "/mobile_base/events/bumper", BumperEvent, self.halter
        ) # topic that contains bumper data
        rospy.spin() # keep node alive

    def halter(self, data):
        collision = data.state # whether there is collision (1) or not (0)
        if collision:
            # Reset velocity to 0
            msg = "1\n0\n0"
            self.pub.publish(msg)

            # Backout of obstacle
            msg = "1\n-0.2\n-2"
            self.pub.publish(msg)
            rospy.sleep(1) # give robot time to backout

            # Send signal that layer has concluded
            msg = "0\n0\n0"
            self.pub.publish(msg)


if __name__ == "__main__":
    BumperHalter = BumperHalter()
