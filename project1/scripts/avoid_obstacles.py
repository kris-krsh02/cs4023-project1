#!/usr/bin/env python2

import rospy, math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from datetime import datetime


class ObstacleAvoider:
    def __init__(self):
        self.mid = None # laser ranges midpoint
        laser_offset = 0.257 # distance from front of robot to laser
        self.obstacle_thr = 0.3 + laser_offset # distance within which obtacles are to be avoided
        self.sym_thr = 0.01 # allowed difference between sensors for symmetric obstacles

        rospy.init_node("obstacle_avoider", anonymous=True) # initialize collective node for obstacle avoidance
        self.pub_avoid = rospy.Publisher("/avoid", String, queue_size=1) # create corresponding topic for the avoid layer
        self.pub_escape = rospy.Publisher("/escape", String, queue_size=1) # create corresponding topic for the escape layer
        self.sub = rospy.Subscriber(
            "/scan", LaserScan, self.avoid_dispatcher, queue_size=1
        ) # subscribe to scan topic to get input from laser 
        rospy.spin() # keep node running

    # Function to determine if an obstacle is symmetric or asymmetric
    def avoid_dispatcher(self, data):
        if self.mid is None:
            self.mid = len(data.ranges) // 2

        ranges = data.ranges # all laser readings

        # Get minimum laser reading on each side; set above maximum laser reading if nan (nothing to read within range)
        try:
            l_range = [x for x in ranges[self.mid :] if not math.isnan(x)]
            l_min = min(l_range)
        except:
            l_min = self.obstacle_thr + 10

        try:
            r_range = [x for x in ranges[: self.mid] if not math.isnan(x)]
            r_min = min(r_range)
        except:
            r_min = self.obstacle_thr + 10


        # Dispatch if at least one sensor is within obstacle threshold
        if l_min < self.obstacle_thr or r_min < self.obstacle_thr:
            if abs(l_min - r_min) < self.sym_thr: # check for symmetric obstacles
                self.escape_symmetric()
            else:
                self.avoid_asymmetric(l_min - r_min)

    def escape_symmetric(self):
        t0 = rospy.Time.now().to_sec()
        current_angle = 0

        # Send angular velocity until angle turned reaches approx 180 deg
        while current_angle < 3.14159:
            self.pub_escape.publish("3\n0\n0.2")
            t1 = rospy.Time.now().to_sec()
            current_angle = 0.2 * (t1 - t0)
 
        self.pub_escape.publish("0\n0\n0") # Send signal that turning is over

    def avoid_asymmetric(self, dir):
        # Set turning velocity in the direction away from the closer laser reading
        # 0.25 is arbitrary chosen velocity
        vel = 0.25 * dir / abs(dir)
        msg = "4\n0\n" + str(vel)
        self.pub_avoid.publish(msg)

        rospy.sleep(1) # Pause to complete turn
        msg = "0\n0\n0" # Send signal that turning is over
        self.pub_avoid.publish(msg)


if __name__ == "__main__":
    ObstacleAvoider = ObstacleAvoider()
