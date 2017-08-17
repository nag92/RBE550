import Queue
import math
import numpy as np
import node


class AStar(object):
    """docstring for astar."""

    def __init__(self, env, robot, start, goal, connected=8, heuristic='eucledian'):

        # Set the variables
        self._env = env
        self._robot = robot

        # which cells to check
        self._connected = 4#connected

        # how to calculate heuristics
        if (heuristic is 'eucledian' or heuristic is 'manhattan'):
            self._heuristic = 'eucledian'
        else:
            self._heuristic = 'heuristic'

        # steps for pose
        self._step = 0.1
        self._angle_step = 0.25*math.pi

        # set up the Queue
        self._fringe = Queue.PriorityQueue()
        self._close_set = []
        start = node.Node(start)
        goal = node.Node(goal)
        start._cost = 0
        self._fringe.put(start)
        print self.eucledian(start._loc,goal._loc)
        #print self.get_neighbours(start._loc)

    def get_neighbours(self, loc):
        """
            Takes in a location as a numpy array
            returns the neighbours to that location
        """
        locations = []

        if self._connected == 4:
            dir = 1
            for i in xrange(6):

                if i%2 == 0: dir = -1

                step = dir*self._step
                angle_inc = dir*self._angle_step

                if i == 0 or i == 1 :
                    locations.append(loc + np.array([step, 0, 0]))
                elif i == 2 or i == 3 :
                    locations.append(loc + np.array([0, step, 0]))
                elif( i == 4 or i == 5):
                    locations.append(loc + np.array([0 , 0, angle_inc]))

        else:

            for x in [-self._step, 0, self._step]:
                for y in [-self._step, 0, self._step]:
                    for z in [-self._angle_step, 0, self._angle_step]:
                        if not ( x == 0 and y == 0 and z == 0 ):
                            locations.append( loc + np.array([x,y,z]) )


        return locations

    def valid_location(self, loc):
        """
            checks if a location is valid
        """
        self._robot.SetActiveDOFValues(loc)
        return self._env.CheckCollision(self._robot)

    def manhattan(self, loc1, loc2):
        """
            calculates the manhattan distance between two locations
        """
        return np.sum(np.absolute( loc1 - loc2))

    def eucledian(self,loc1, loc2):
        """
            calculates the eucledian distance between two locations
        """
        return  math.sqrt( np.sum( np.square(loc1-loc2) ))
