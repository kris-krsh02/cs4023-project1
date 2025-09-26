import rospy
from geometry_msgs.msg import Twist
from kobuki_msmgs.msg import BumperEvent


class BumperHalter:
    def __init__(self):
        rospy.init_node("bumper_halter", anonymous=True)
        self.pub = rospy.Publisher("/cmd_vel_mux/input/navi", Twist, queue_size=10)
        self.sub = rospy.Subscriber(
            "/mobile_base/events/bumper", BumperEvent, self.halter
        )
        rospy.spinn()

    def halter(self, data):
        collision = data.state
        if collision:
            vel = Twist()
            vel.linear.x = 0
            vel.angular.z = 0

            self.pub.publish(vel)
            rospy.sleep()
