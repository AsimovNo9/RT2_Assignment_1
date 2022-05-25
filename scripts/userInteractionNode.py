#!/usr/bin/env python

"""
.. module:: userInteractionNode

:platform: Unix
:sypnosis: Python module for user interation with assignment 3 package based off the terminal


..  moduleauthor:: Carmine Recchiuto <carmine.recchiuto@dibris.unige.it>

ROS node which gives the user a series of choices for interaction with the assignment 3 package between
  - Option 1 (1): giving desried coordinates
  - Option 2 (2): Manual Control without assistance
  - Option 3 (3): Manual Control with assistance
  - Option 0 (0): exit

Service:
  /reachCoordinateSerivce
  /keyboardService
"""

import rospy
from assignment_3.srv import *

def calluser():
	"""
	Function to prompt the user by giving options that can be selected for
	running the code. The selectable inputs vary from the numbers 0-3

	Input:
		user_input (int): Choices between options 0 through 3, with numbers 0-3 respectively.

	Returns:
		int: returns the input given by the user. For properfucntioning, should be between 0-3.
	"""
	print("What do you want to do?")
	print("1. Reach a (x,y) coordinate")
	print("2. Drive the robot with the keybord")
	print("3. Drive the robot with some assistance")
	print("0. Exit")
	ans = input('Insert the number corresponding to the action you would do:')
	return ans
	
def opt1():
	"""
	Function that gets called when the user inputs 1, for option 1.
	This requests the user to input floats of a coordinante position in 2D space.
	A client object for the reachCoordinateService is created, and the coordinates
	are passed as a request, with the service responding with the final status of the
	robot - reached the point or not.

	Input:
		x (): Input coordinate for the x-axis.
		y (): Input coordinate for the y-axis.

	Returns:
		Print: The final status of the robot and goal is printed onto the screen. If the position has been reached or not.
	"""
	print("Option 1")
	x = float(input("Insert coordinate x: "))
	y = float(input("Insert coordinate y: "))
				
	print("You have insert the coordinate: (",x,",",y,")")
				
	rospy.wait_for_service("/reachCoordinateService")
	client = rospy.ServiceProxy("/reachCoordinateService", reachCoordinateService)
	
	rt = client(x,y)
	if rt.ret == 0:
		print("Target not reached, goal cancelled")
	elif rt.ret == 1:
		print("Target reached!")
		
def opt2():
	"""
	Function that gets called when the user inputs 2, for option 2.
	This creates a client object for the keyboardService and passes 0 as a request,
	which links to the teleop keyyboard without assistance.
	"""
	print("Option 2")
	rospy.wait_for_service("/keyboardService")
	client = rospy.ServiceProxy("/keyboardService", keyboardService)
	client(0)
	
def opt3():
	"""
	Function that gets called when the user inputs 3, for option 3.
	This creates a client object for the keyboardService and passes 1 as a request,
	which links to the teleop keyboard with assistance.
	"""
	print("Option 3")
	rospy.wait_for_service("/keyboardService")
	client = rospy.ServiceProxy("/keyboardService", keyboardService)
	client(1)
	

if __name__ == "__main__":
	rospy.init_node('userInteractionNode')
	
	while(1):
		ans = calluser();
		if ans.isnumeric():
			ans = int(ans)
			
			if ans==1:
				opt1()
					
			elif ans==2:
				opt2()
					
			elif ans==3:
				opt3()
				
			elif ans == 0:
				sys.exit()
	
			else:
				print("error")
		else:
			print("Invalid input")
		

