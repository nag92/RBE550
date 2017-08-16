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
        self._connected = connected

        # how to calculate heuristics
        if (heuristic is 'eucledian' or heuristic is 'manhattan'):
            self._heuristic = 'eucledian'
        else:
            self._heuristic = heuristic

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

        self.get_neighbours(start._loc)

    def get_neighbours(self, loc):
        locations = []
        print loc
        for x in [-self._step, 0, self._step]:
            for y in [-self._step, 0, self._step]:
                for z in [-self._angle_step, 0, self._angle_step]:
                    if not ( x == 0 and y == 0 and z ==0 ):
                        temp = loc + np.array([x,y,z])
                        print temp
                        locations.append( temp )

        return locations
