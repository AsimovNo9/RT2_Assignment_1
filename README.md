# Research Track 2 Using Solution for assignment_3 for Research Track 1 by Dr. Carmine Recchuito
This project implements documentation for the assignment_3 task of the research track one course which gives robot movement instructions in a number of ways

1. Giving cartesian coordinates to robot
2. Controlling manually with teleop keyboard package
3. Controlling manually with teleop keyboard package and obstacle avoidance assistance 

## Dependencies

Before downloading the package, install the following dependencies:

```
- xterm (sudo apt-get xterm)
- ROS navigation package (sudo apt-get install ros-noetic-navigation)
- ROS teleop twist keyboard (sudo apt-get install ros-noetic-teleop-twist-keyboard)
```

Additionally, please download in your ROS workspace the following packages: 

```
- final_assignment (https://github.com/CarmineD8/final_assignment), switch to the Noetic branch
- slam_gmapping (https://github.com/CarmineD8/slam_gmapping), switch to the Noetic branch
```

## How to run the simulation

Follow those steps to launch the simulation:

```
roslaunch final_assignment simulation_gmapping.launch
roslaunch final_assignment move_base.launch
roslaunch assignment_3 main.launch
```

## Documentation Link
<a href= "https://asimovno9.github.io/RT2_Assignment_1/">Documentation Link!</a>


