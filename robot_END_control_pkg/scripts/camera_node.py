#!/usr/bin/env python
import rospy
from moveit_commander import PlanningSceneInterface
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose

rospy.init_node('camera_node', anonymous=True)
scene = PlanningSceneInterface()
rospy.sleep(2)


def add_object_1():
    object1_pose = PoseStamped()
    object1_pose.header.frame_id = "root"
    object1_pose.pose.position.x = 1
    object1_pose.pose.position.z = .1
    size = [.2, .2, .2]
    scene.add_box("object1", object1_pose, size)


def add_object_2():
    object2_pose = PoseStamped()
    object2_pose.header.frame_id = "root"
    object2_pose.pose.position.x = -1
    object2_pose.pose.position.z = .05
    size = [.1, .1, .1]
    scene.add_box("object2", object2_pose, size)


def send_goal():
    pub = rospy.Publisher('chatter', Pose, queue_size=10)
    rate = rospy.Rate(50)
    while not rospy.is_shutdown():
        goal = Pose()
        print "Enter X position"
        goal.position.x = input()
        print "Enter Y position"
        goal.position.y = input()
        print "Enter Z position"
        goal.position.z = input()
        pub.publish(goal)
        rate.sleep()


if __name__ == '__main__':
    try:
        add_object_1()
        add_object_2()
        send_goal()
    except rospy.ROSInterruptException:
        pass


