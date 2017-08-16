import Queue
import math
import numpy as np
import node

class AStar(object):
    """docstring for astar."""

    def __init__(self, env, robot, start, goal, connected, heuristic):
        super(astar, self).__init__()
        self._env = env
        self._robot = robot
        self._start = start
        self._goal - goal
        self._connected = connected
        self._heuristic = heuristic
