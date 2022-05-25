#!/usr/bin/env python

"""
.. module:: teleopNode

:platform: Unix
:sypnosis: Python module for running teleop keyboard without or with assistance


.. moduleauthor:: Carmine Recchiuto <carmine.recchiuto@dibris.unige.it>

ROS service node which takes the teleop request and either returns the teleop keyboard node withot or with assistance

Service:
  /keyboardService
"""

import rospy
import os
from assignment_3.srv import keyboardService

def teleop_handler(req):
	"""
	This function is the callback function to the keyboardService.
	It takes in a request as an integer of either 1 or 0. Where 0 launches the teleop
	keyboard package, and 1 launches the same package with obstacle avoidance assistance

	Args:
		req (int): Either 0 or 1, which selects the teleop keyboard without assistance or with assistance respectively

	Returns:
		int: 0

	Raises:
		error: An error which occurs when neither 0 or 1 is passed as the request
	"""
	
	if req.action == 0:
		print("Driving the robot without help")
		os.system("rosrun teleop_twist_keyboard teleop_twist_keyboard.py")
	elif req.action == 1:
		print("Driving the robot with help")
		os.system("roslaunch assignment_3 option3.launch")
	else:
		print("error")
	
	return 0

def teleop_server():
	"""
	This function creates the Keyboard service server object

	"""
	srv = rospy.Service('keyboardService', keyboardService, teleop_handler)
	print("Service ready")
	rospy.spin()


if __name__ == "__main__":
	rospy.init_node('teleopNode')
	teleop_server()
