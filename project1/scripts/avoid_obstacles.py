#!/usr/bin/env python2

import rospy, math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from datetime import datetime


class ObstacleAvoider:
    def __init__(self):
        self.mid = None
        laser_offset = 0.257
        self.obstacle_thr = 0.3 + laser_offset
        self.sym_thr = 0.01

        rospy.init_node("obstacle_avoider", anonymous=True)
        self.pub_avoid = rospy.Publisher("/avoid", String, queue_size=1)
        self.pub_escape = rospy.Publisher("/escape", String, queue_size=1)
        self.sub = rospy.Subscriber(
            "/scan", LaserScan, self.avoid_dispatcher, queue_size=1
        )
        rospy.spin()

    def avoid_dispatcher(self, data):
        if self.mid is None:
            self.mid = len(data.ranges) // 2
        ranges = data.ranges
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

        print(l_min, r_min, datetime.now())

        if l_min < self.obstacle_thr or r_min < self.obstacle_thr:
            if abs(l_min - r_min) < self.sym_thr:
                self.escape_symmetric()
            else:
                self.avoid_asymmetric(l_min - r_min)

    def escape_symmetric(self):
        print("escape")
        t0 = rospy.Time.now().to_sec()
        current_angle = 0

        while current_angle < 3.14159:
            self.pub_escape.publish("3\n0\n0.2")
            t1 = rospy.Time.now().to_sec()
            current_angle = 0.2 * (t1 - t0)

        self.pub_escape.publish("0\n0\n0")

    def avoid_asymmetric(self, dir):
        print("avoid")
        speed = 0.25 * dir / abs(dir)
        msg = "4\n0\n" + str(speed)
        self.pub_avoid.publish(msg)
        rospy.sleep(1)
        msg = "0\n0\n0"
        self.pub_avoid.publish(msg)


if __name__ == "__main__":
    ObstacleAvoider = ObstacleAvoider()
