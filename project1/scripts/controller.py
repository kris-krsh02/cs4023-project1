#!/usr/bin/env python2
import rospy, rosnode
from geometry_msgs.msg import Twist
from std_msgs.msg import String


class Controller:
    def __init__(self):
        self.active_action = "6" # priority of currently executed action

        rospy.init_node("vel_controller", anonymous=True) # velocity controller node
        self.pub = rospy.Publisher("/cmd_vel_mux/input/navi", Twist, queue_size=1) # publisher for velocity topic

        # Subscribe to all custom topics for prioritization (name corresponds to layer)
        self.sub = rospy.Subscriber("/bumper_halter", String, self.callback)
        self.sub = rospy.Subscriber("/manual_nav", String, self.callback)
        self.sub = rospy.Subscriber("/escape", String, self.callback)
        self.sub = rospy.Subscriber("/avoid", String, self.callback)
        self.sub = rospy.Subscriber("/periodic_turn", String, self.callback)
        self.sub = rospy.Subscriber("/auto_drive", String, self.callback)
        rospy.spin() # keep node running

    def callback(self, data):
        priority, linear, angular = data.data.split("\n") # decouple data from subscribers

        # Priority 0 is a signal that a higher layer has concluded
        # Resets active action to lowest priority to unblock
        if priority == "0":
            self.active_action = "6"
            return

        # Block lower priority actions
        if priority > self.active_action:
            return

        self.active_action = priority

        # Create and publish velocity message
        vel_msg = Twist()
        vel_msg.linear.x = float(linear)
        vel_msg.angular.z = float(angular)
        self.pub.publish(vel_msg)


if __name__ == "__main__":
    Controller = Controller()