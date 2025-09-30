#!/usr/bin/env python2

import rospy, math, random
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import String


class PeriodicTurn:
    def __init__(self):
        # Hold previous position for distance comparison to measure 1ft
        self.prev_x = None  
        self.prev_y = None

        rospy.init_node("periodic_turn", anonymous=True) # create periodic_turn node
        self.pub = rospy.Publisher("/periodic_turn", String, queue_size=10) # create corresponding topic for the layer
        self.sub = rospy.Subscriber("/odom", Odometry, self.periodic_turn) # subscribe to odometry topic to determine positioning
        rospy.spin()

    def periodic_turn(self, data):
        # Initialize prevous position when starting
        if self.prev_x is None:
            self.prev_x = data.pose.pose.position.x
            self.prev_y = data.pose.pose.position.y

        # Get current position
        curr_x = data.pose.pose.position.x
        curr_y = data.pose.pose.position.y

        # Calculate distance between current and previous position
        dist = math.sqrt((curr_x - self.prev_x) ** 2 + (curr_y - self.prev_y) ** 2)

        # If 1ft distance reached
        if dist > 0.3:  # approx 1 ft
            angle = random.randint(-15, 15) # get random angle within +/-15 deg
            angle_rad = math.radians(angle) # convert to radians for angular velocity

            # Publish turning velocity
            ang_vel = "5\n0\n" + str(angle_rad)
            self.pub.publish(ang_vel)

            # Set new previous position
            self.prev_x = curr_x
            self.prev_y = curr_y

            rospy.sleep(1) # give enough time to turn
            self.pub.publish("0\n0\n0") # Send signal that layer has concluded


if __name__ == "__main__":
    PeriodicTurn = PeriodicTurn()
