#!/usr/bin/env python

"""
.. module:: reachCoordinateNode

:platform: Unix
:sypnosis: Python module for moving robot to required coordinates given by the user


.. moduleauthor:: Carmine Recchiuto <carmine.recchiuto@dibris.unige.it>

ROS service node which takes the requested coordinates as a request for moving the robot to a specific position

Service:
  /reachCoordinateService
"""

import rospy
import os
import actionlib
from assignment_3.srv import reachCoordinateService 
from move_base_msgs.msg import *
from actionlib_msgs.msg import *

def reachCoordinate_handler(req):
	"""
	This function is the callback function to the reachCoordinateService.
	It takes in a request in the form of cartesian coordinates and proceses
	the robot movement, returning either 0 or 1 for an incomplete or complete
	process respectively

	Args:
		req ((float64, float64)): This is the requested coordinates with the respective axis x and y.

	Returns:
		Bool: 0 if task not complete, 1 if task complete.
	"""
	x = req.x
	y = req.y
	
	client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
	client.wait_for_server()
	
	goal = MoveBaseGoal()
	
	goal.target_pose.header.frame_id = 'map'
	goal.target_pose.pose.orientation.w = 1
	goal.target_pose.pose.position.x = x
	goal.target_pose.pose.position.y= y
	client.send_goal(goal)
	
	state_goal = client.wait_for_result(timeout=rospy.Duration(50.0))
	
	if not state_goal:
		client.cancel_goal()
		return 0

	return 1

def reachCoordinate_server():
	"""
	Creates the reachCoordinateService service object
	"""
	srv = rospy.Service('reachCoordinateService', reachCoordinateService, reachCoordinate_handler)
	print("Service ready")
	rospy.spin()


if __name__ == "__main__":
	rospy.init_node('reachCoordinateNode')
	reachCoordinate_server()
