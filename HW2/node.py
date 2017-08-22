class Node(object):
    """Node
        This is a class for a Node.
        A node is a point on the map along with all information on how that
        point was added to the graph
    """
    def __init__(self, loc=None):
        self._loc = loc

        self._h_cost = 0.0

        self._g_cost = 0.0

        self._parent = None

        self._generation = 0.0

        self._distance = 0.0

    def getCost(self):
        return self._g_cost + self._h_cost

    def __cmp__(self, other):
        return cmp(self._cost, other.priority)


    def __eq__(self, other):
        """
        check if equal
        """
        return set(other._loc) == set(self._loc)
