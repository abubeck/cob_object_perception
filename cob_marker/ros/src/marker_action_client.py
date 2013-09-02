#! /usr/bin/env python

import roslib; roslib.load_manifest('cob_marker')
import rospy

import actionlib
import cob_object_detection_msgs.msg
from tf.transformations import *
import tf


def marker_client():
    client = actionlib.SimpleActionClient('/cob_marker/object_detection', cob_object_detection_msgs.msg.DetectObjectsAction)
    client.wait_for_server()

    goal = cob_object_detection_msgs.msg.DetectObjectsGoal()
    goal.object_name.data = "AUB"

    client.send_goal(goal)

    client.wait_for_result()

    return client.get_result()

if __name__ == '__main__':
    try:
        rospy.init_node('cob_marker_client')
	listener = tf.TransformListener()
	rospy.sleep(1.0)
        result = marker_client()
        print "Result:"
        print result
        #rospy.sleep(0.5)
	bpose = listener.transformPose('/base_link',result.object_list.detections[0].pose)
	print bpose
	ori = bpose.pose.orientation
	print euler_from_quaternion((ori.x, ori.y, ori.z, ori.w))
    except rospy.ROSInterruptException:
        print "program interrupted before completion"
