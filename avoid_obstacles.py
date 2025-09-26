import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class ObstacleAvoider:
    def __init__(self):
        rospy.init_node("obstacle_avoider", anonymous=True)
        self.pub = rospy.Publisher("/cmd_vel_mux/input/navi", Twist, queue_size=10)
        self.sub = rospy.Subscriber("/scan", LaserScan, self.avoid_dispatcher)
        rospy.spin()

    def avoid_dispatcher(self, data):
        symmetric = True  # logic needs to be implemented
        if symmetric:
            self.escape_symmetric()
        else:
            self.avoid_asymmetric()

    def escape_symmetric(self):
        pass

    def avoid_asymmetric(self):
        pass
