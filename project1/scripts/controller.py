#!/usr/bin/env python2
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String


class Controller:
    def __init__(self):
        self.active_action = '6'
        rospy.init_node("vel_controller", anonymous=True)
        self.pub = rospy.Publisher("/cmd_vel_mux/input/navi", Twist, queue_size=1)

        self.sub = rospy.Subscriber("/bumper_halter", String, self.callback)
        self.sub = rospy.Subscriber("/manual_nav", String, self.callback)
        self.sub = rospy.Subscriber("/escape", String, self.callback)
        self.sub = rospy.Subscriber("/avoid", String, self.callback)
        self.sub = rospy.Subscriber("/periodic_turn", String, self.callback)
        self.sub = rospy.Subscriber("/auto_drive", String, self.callback)
        rospy.spin()

    def callback(self, data):
        priority, linear, angular = data.data.split("\n")
        print(data.data)
        if priority == '0':
            self.active_action = '6'
            return

        if priority > self.active_action:
            return

        # print('here')    
        self.active_action = priority
        vel_msg = Twist()
        vel_msg.linear.x = float(linear)
        vel_msg.angular.z = float(angular)
        print(vel_msg)
        self.pub.publish(vel_msg)
        # rospy.sleep(1)


if __name__ == "__main__":
    Controller = Controller()
