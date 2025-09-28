import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from kobuki_msgs.msg import BumperEvent


class BumperHalter:
    def __init__(self):
        rospy.init_node("bumper_halter", anonymous=True)
        self.pub = rospy.Publisher("/bumper_halter", String, queue_size=1)

        self.sub = rospy.Subscriber(
            "/mobile_base/events/bumper", BumperEvent, self.halter
        )
        rospy.spin()

    def halter(self, data):
        collision = data.state
        if collision:
            msg = "1\n0\n0"
            self.pub.publish(msg)

            # kinda need to manually drag out in the simulation
            # rethink this, maybe ask expected behavior
            msg = "1\n-0.2\n-1.7"
            self.pub.publish(msg)
            rospy.sleep(1)
            msg = "0\n0\n0"
            self.pub.publish(msg)


if __name__ == "__main__":
    BumperHalter = BumperHalter()
