#!/usr/bin/env python
import sys
import moveit_commander
import rospy
from geometry_msgs.msg import Pose
from moveit_commander import MoveGroupCommander


moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('planning_node', anonymous=True)
group_name = "arm"
move_group = moveit_commander.MoveGroupCommander(group_name)
robot = moveit_commander.RobotCommander()
move_group.set_planning_time(10)
rospy.sleep(2)


def print_state():
    arm = MoveGroupCommander("arm")
    print ("============ Current_Position ============")
    print(arm.get_current_pose(arm.get_end_effector_link()))
    planning_frame = move_group.get_planning_frame()
    print "============ Planning_Frame: %s ============" % planning_frame


def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.position)
    print ("============   Before_Moving  ============")
    print_state()
    pose_goal = Pose()
    pose_goal.orientation.w = 1.0
    pose_goal.position.x = data.position.x
    pose_goal.position.y = data.position.y
    pose_goal.position.z = data.position.z
    move_group.set_pose_target(pose_goal)
    plan = move_group.go(wait=True)
    # Calling `stop()` ensures that there is no residual movement
    move_group.stop()
    # It is always good to clear your targets after planning with poses.
    # Note: there is no equivalent function for clear_joint_value_targets()
    move_group.clear_pose_targets()
    print ("============     After_Moving     ============")
    print_state()


def read_goal():
    rospy.Subscriber("chatter", Pose, callback)
    rospy.spin()


if __name__ == '__main__':
    read_goal()




