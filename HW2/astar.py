import Queue
import math
import numpy as np
import node


class AStar(object):
    """docstring for astar."""

    def __init__(self, env, robot, connected=8, heuristic="eucledian"):

        # Set the variables
        self._env = env
        self._robot = robot

        # which cells to check
        if not (connected == 8 or connected == 4):
            self._connected = 8
        else:
            self._connected = connected

        # how to calculate heuristics
        if not (heuristic is "eucledian" or heuristic is "manhattan"):
            self._heuristic = "eucledian"
        else:
            self._heuristic = heuristic

        # steps for pose
        self._step = 0.1
        self._angle_step = 0.25*math.pi

        # set up the Queue
        self._fringe = Queue.PriorityQueue()
        self._close_set = []


    def get_neighbours(self, loc):
        """
            Takes in a location as a numpy array
            returns the neighbours to that location
        """
        locations = []

        if self._connected == 4:
            dir = 1
            for i in xrange(6):

                if i % 2 == 0: dir = -1

                step = dir*self._step
                angle_inc = dir*self._angle_step

                if   i == 0 or i == 1 : locations.append(loc + np.array([step, 0, 0]))
                elif i == 2 or i == 3 : locations.append(loc + np.array([0, step, 0]))
                elif i == 4 or i == 5 : locations.append(loc + np.array([0 , 0, angle_inc]))

        else:

            for x in [-self._step, 0, self._step]:
                for y in [-self._step, 0, self._step]:
                    for z in [-self._angle_step, 0, self._angle_step]:
                        if not ( x == 0 and y == 0 and z == 0 ):
                            locations.append( loc + np.array([x,y,z]) )


        return filter(self.valid_location,locations)

    def valid_location(self, loc):
        """
            checks if a location is valid
        """
        self._robot.SetActiveDOFValues(loc)
        return self._env.CheckCollision(self._robot)

    def heuristic(self, loc1, loc2):
        """"
        calculates the heuristic cost fot two points
        """
        if self._heuristic is "manhattan":
            return np.sum(np.absolute( loc1 - loc2))
        elif self._heuristic is "eucledian":
            return  math.sqrt( np.sum( np.square(loc1-loc2) ))

    def run(self, start, goal):

        start = node.Node(start)
        goal = node.Node(goal)
        start._cost = 0
        self._fringe.put(start)



        found = False
