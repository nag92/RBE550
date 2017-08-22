import priorityqueue
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
        self._fringe = priorityqueue.PriorityQueue()
        self._close_set = []


    def get_neighbours(self, node):
        """
            Takes in a location as a numpy array
            returns the neighbours to that location
        """
        locations = []
        loc = node._loc
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
            return self.manhattan(loc1,loc2)
        elif self._heuristic is "eucledian":
            return  self.eucledian(loc1,loc2)

    def travelCost(self,loc1,loc2):
        """
            find the travel cost between points
        """
        return self.eucledian(loc1,loc2)
        pass


    def manhattan(self, loc1, loc2):
        """
            returns the manhattan cost between points
        """
        return np.sum(np.absolute( loc1 - loc2))

    def eucledian(self, loc1, loc2):
        """
            return the eucledian cost between points
        """
        return math.sqrt(np.sum(np.square(loc1 - loc2)))

    def makePath(self, start, goal):
        """
            takes in a list and returns a path from start to finish
        """
        current = goal
        path = [goal._loc]
        while current is not start:
            current = current._parent
            path.append(current._loc)
        return list(reversed(path))


    def run(self, start, goal):
        """
        run astar
        """
        start_node = node.Node(start)
        goal_node  = node.Node(goal)
        start_node._g_cost = 0

        self._fringe.put(start_node,start_node.getCost())

        while not self._fringe.empty():

            current = self._fringe.get()

            self._close_set.append(current)

            if current == goal_node:
                print "FOUND" 
                break

            for next in self.get_neighbours(current):
                new_cost = current._g_cost +  self.travelCost(current,next)
                old = self._fringe.get_item(current)
                if old is not None:
                    if old[1]._g_cost > new_cost:
                        self._fringe.remove(old)
                        self._close_set.remove(old[1])
                        old[1]._g_cost = new_cost
                        old[1]._parent = current
                        self._fringe.put(old[1], old[1].getCost()) 
                else:
                    temp_node = node.Node(next)
                    temp_node._parent = current
                    temp_node._g_cost = new_cost
                    temp_node._h_cost = self.heuristic(next,goal_node._loc)
                    self._fringe.put(temp_node,temp_node.getCost())

        path = self.makePath(start, self._close_set[-1])
        print path

            
