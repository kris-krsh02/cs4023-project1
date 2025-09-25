import rospy
from geometry_msgs.msg import Twist


def auto_drive():
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    rospy.init_node("auto_drive", anonymous=True)
    vel = Twist()
    vel.linear.x = 0.2
    vel.angular.z = 0
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        pub.publish(vel)
        rate.sleep()


if __name__ == "__main__":
    try:
        auto_drive()
    except rospy.ROSInterruptException:
        pass
