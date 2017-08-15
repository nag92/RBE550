#!/usr/bin/env python
# -*- coding: utf-8 -*-
# HW1 for RBE 595/CS 525 Motion Planning
# code based on the simplemanipulation.py example
import time
import openravepy

if not __openravepy_build_doc__:
    from openravepy import *
    from numpy import *


def waitrobot(robot):
    """busy wait for robot completion"""
    while not robot.GetController().IsDone():
        time.sleep(0.01)


def tuckarms(env, robot):
    with env:
        jointnames = ['l_shoulder_lift_joint', 'l_elbow_flex_joint', 'l_wrist_flex_joint',
                      'r_shoulder_lift_joint', 'r_elbow_flex_joint', 'r_wrist_flex_joint']
        robot.SetActiveDOFs([robot.GetJoint(name).GetDOFIndex()
                             for name in jointnames])
        robot.SetActiveDOFValues(
            [1.29023451, -2.32099996, -0.69800004, 1.27843491, -2.32100002, -0.69799996])
        robot.GetController().SetDesired(robot.GetDOFValues())
    waitrobot(robot)


def quaterian_to_matrix(quat, trans):
    '''
        Takes in a quat and trans and outputs a homogenous matrix
    '''
    q = numpy.array(quat, dtype=numpy.float64, copy=True)
    n = numpy.dot(q, q)
    q *= math.sqrt(2.0 / n)
    q = numpy.outer(q, q)
    return numpy.array([
        [1.0 - q[2, 2] - q[3, 3], q[1, 2] - q[3, 0], q[1, 3] + q[2, 0], trans[0]],
        [q[1, 2] + q[3, 0], 1.0 - q[1, 1] - q[3, 3],     q[2, 3] - q[1, 0], trans[1]],
        [q[1, 3] - q[2, 0], q[2, 3] + q[1, 0], 1.0 - q[1, 1] - q[2, 2], trans[2]],
        [0.0, 0.0, 0.0, 1.0]])


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
    tuckarms(env, robot)

    #### YOUR CODE HERE ####

    '''
        Move the tables to new locations
        The values were manualy takening from the GUI
    '''
    with env:
        table_6 = env.GetBodies()[6]
        table_5 = env.GetBodies()[5]
        table_6.SetTransform(quaterian_to_matrix(
            [1, 0, 0, 0], [0.24528, -0.96942, 0.73999]))
        table_5.SetTransform(quaterian_to_matrix(
            [1, 0, 0, 0], [0.17350, 0.84887, 0.73999]))

    #### END OF YOUR CODE ###

    raw_input("Press enter to exit...")
