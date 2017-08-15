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
    handles = []
    #Grab all the tables
    tables = [ env.GetBodies()[i] for i in xrange(1,7)]

    # loop through all the tables
    for body in tables:

        # Get the name
        name_id = int(body.GetName()[-1])
        print type(int(name_id))
        center = body.GetTransform()[:3,3]
        color = array(((1,0,0),(1,0,0),(1,0,0),(1,0,0),(1,0,0)))

        # draw all the lines
        if name_id < 5:
            lines = array(((center[0] - 0.6, center[1] - 0.3,0.74),
                           (center[0] - 0.6, center[1] + 0.3,0.74),
                           (center[0] + 0.6, center[1] + 0.3,0.74),
                           (center[0] + 0.6, center[1] - 0.3,0.74),
                           (center[0] - 0.6, center[1] - 0.3,0.74)))
        else:
            lines = array(((center[0] - 0.3, center[1] - 0.6,0.74),
                           (center[0] + 0.3, center[1] - 0.6,0.74),
                           (center[0] + 0.3, center[1] + 0.6,0.74),
                           (center[0] - 0.3, center[1] + 0.6,0.74),
                           (center[0] - 0.3, center[1] - 0.6,0.74)))



        handles.append(env.drawlinestrip(points=lines,
                                         linewidth=5.0,
                                         colors=color))




    #### END OF YOUR CODE ###


    raw_input("Press enter to exit...")
