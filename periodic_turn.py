#!/usr/bin/env python2

import rospy, math, random
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


class PeriodicTurn:
    def __init__(self):
        self.prev_x = 0  # proof this, hardcoded value
        self.prev_y = 0

        rospy.init_node("periodic_turn", anonymous=True)
        self.pub = rospy.Publisher("/cmd_vel_mux/input/navi", Twist, queue_size=10)
        self.sub = rospy.Subscriber("/odom", Odometry, self.periodic_turn)
        rospy.spin()

    def periodic_turn(self, data):
        curr_x = data.pose.pose.position.x
        curr_y = data.pose.pose.position.y
        dist = math.sqrt((curr_x - self.prev_x) ** 2 + (curr_y - self.prev_y) ** 2)

        if dist > 0.3:  # approx 1 ft
            angle = random.randint(-15, 15)
            angle_rad = math.radians(angle)
            ang_vel = Twist()
            ang_vel.angular.z = angle_rad

            self.pub.publish(ang_vel)
            rospy.sleep(3)

            self.prev_x = curr_x
            self.prev_y = curr_y
