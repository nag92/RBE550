#!/usr/bin/env python
# -*- coding: utf-8 -*-
#HW1 for RBE 595/CS 525 Motion Planning
#code based on the simplemanipulation.py example
import time
import openravepy

if not __openravepy_build_doc__:
    from openravepy import *
    from numpy import *

def waitrobot(robot):
    """busy wait for robot completion"""
    while not robot.GetController().IsDone():
        time.sleep(0.01)

def tuckarms(env,robot):
    with env:
        jointnames = ['l_shoulder_lift_joint','l_elbow_flex_joint','l_wrist_flex_joint','r_shoulder_lift_joint','r_elbow_flex_joint','r_wrist_flex_joint']
        robot.SetActiveDOFs([robot.GetJoint(name).GetDOFIndex() for name in jointnames])
        robot.SetActiveDOFValues([1.29023451,-2.32099996,-0.69800004,1.27843491,-2.32100002,-0.69799996]);
        robot.GetController().SetDesired(robot.GetDOFValues());
    waitrobot(robot)




def touch_wall (env,robot):
    '''
    Move the arm of the PR2 to touch the puma
    '''
    with env:
        jointnames = ['l_shoulder_lift_joint','l_elbow_flex_joint','l_wrist_flex_joint']
        robot.SetActiveDOFs([robot.GetJoint(name).GetDOFIndex() for name in jointnames])
        robot.SetActiveDOFValues([-0.015,-1.0,0.7]);
        robot.GetController().SetDesired(robot.GetDOFValues());
    waitrobot(robot)



if __name__ == "__main__":

    env = Environment()
    env.SetViewer('qtcoin')
    env.Reset()
    # load a scene from ProjectRoom environment XML file
    env.Load('data/pr2test2.env.xml')
    time.sleep(0.1)

    # 1) get the 1st robot that is inside the loaded scene
    # 2) assign it to the variable named 'robot'
    robot = env.GetRobots()[0]

    # tuck in the PR2's arms for driving
    tuckarms(env,robot);


    #### YOUR CODE HERE ####

    # Move the Pr2 to the wall
    location =  robot.GetLinks()[0].GetTransform()
    location[0][3] = 0.16804
    location[1][3] = 0.1997
    robot.SetTransform(location)


    print "Collision status of PR2 robot : ", env.CheckCollision(robot)
    print "Self Collision status of PR2 robot: " ,robot.CheckSelfCollision()

    touch_wall(env,robot)

    print "Collision status of PR2 robot : ", env.CheckCollision(robot)
    print "Self Collision status of PR2 robot: " ,robot.CheckSelfCollision()



    #### END OF YOUR CODE ###


    raw_input("Press enter to exit...")
