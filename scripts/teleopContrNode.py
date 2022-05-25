#! /usr/bin/env python

"""
.. module:: teleopContrNode

:platform: Unix
:sypnosis: Python module for obstacne avoidance assistance for manual control with the teleop keyboard package


.. moduleauthor:: Carmine Recchiuto <carmine.recchiuto@dibris.unige.it>

ROS service node which takes the requested coordinates as a request for moving the robot to a specific position

Subscribers:
  /remap_cmd_cal
  /scan 

Publishers:
  /cmd_vel
"""

import rospy
import numpy as np
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan

walls = [False, False, False]
"""
List to determine if there is a wall present in three positions:
- Right
- Forward
- Left, respectvely.
"""

min_dist = 0.5
"""
Minimum distance variable to be compared to the output of the laser scan
"""

linear = Vector3(0, 0, 0)
"""
Variable to hold vector of 3 dimensions for linear velocity
"""

angular = Vector3(0, 0, 0)
"""
Varibale to hold vector of 3 dimensions for angular velocity
"""

repost = Twist(linear, angular)
"""
Variable for repositioning the robot, with the dtyoe being a twist message with the linear and angular velocities as arguments.
"""


def compute_min_dist(ranges):
	""" 
	This function uses the data gotten from the laser scanner attachment to compute the 
	minimum distance observed indicating the presence of a wall in a certain direction.
	Where the direction within the range of 0 to 720 degrees is given as:
	- right (0-240)
	- forward (241-480)
	- left (481-721)

	Args:
		ranges (list): List of 720 float values, of range values obtained from the LaserScan topic.

	Returns:
		distance (float): This is the shortest distance from the robot scanned by the laser scanner sensor.
	"""
	distance = [0,0,0]
	subarrays = [ ranges[0:240], ranges[241:480], ranges[481:721] ]
	distance = [ min(subarrays[0]), min(subarrays[1]), min(subarrays[2]) ]
	return distance
        
  
def callback_scan(data):
	"""
	This is a callback function called when the topic /scan is subscribed to.
	It creates a publisher object to publish to the /cmd_vel topic for controlling the robot movement, and determines
	whether the right, forward, or left directions are obstructed by a wall by using the compute_min_dist function
	to compare the distance of the sectors to a min_dist variable (0.5 in this case). 

	Args:
		data (obj): Instance of the Laser scan class.
	"""
	global repost
	global walls
	
	pub = rospy.Publisher('cmd_vel',Twist, queue_size=10)
	
	ranges = data.ranges
	distances = compute_min_dist(ranges)
	
	walls[0] = ( distances[0] < min_dist )
	walls[1] = ( distances[1] < min_dist )
	walls[2] = ( distances[2] < min_dist )
	
	if walls[0]:
		if repost.angular.z <0:
			print("cannot turn right")
			repost.angular.z = 0
					
	if walls[1]:
		if repost.linear.x > 0:
			repost.linear.x = 0
	
	if walls[2]:
		if repost.angular.z > 0:
			repost.angular.z = 0 
	
	pub.publish(repost)

def callback_remap(data):
	"""
	This is a callback function called when the topic /remap_cmd_vel is subscribed to.


	Args:
		data (obj): Object of twist class containing robot parameters of linear and angular speeds in their corresponding x, y and z directions
	"""
	global repost
	repost = data

def keyboard_remap():
	"""
	Function which creates subcribers to the /remap_cmd_vel and /scan topics
	"""
	rospy.Subscriber("/remap_cmd_vel", Twist, callback_remap)
	rospy.Subscriber("/scan", LaserScan, callback_scan)
	rospy.spin()
    
if __name__=="__main__":
	rospy.init_node('keyboard_remap_node')
	keyboard_remap()
