import heapq

class PriorityQueue:
    def __init__(self):
        self._elements = []

    def empty(self):
        """ Check to see if the queue empty"""
        return len(self._elements) == 0

    def put(self, item, priority):
        """Add a element to the queue"""
        heapq.heappush(self._elements, (priority, item))

    def get(self):
        """Get the next element"""
        return heapq.heappop(self._elements)[1]

    def  get_list(self):
        """Returns the entire queue"""
        return [ item[1] for item in self._elements]

    def get_item(self,item):

        temp = [ i[1]._loc for i in self._elements ]
        if item in temp:
            loc = temp.index(item)
            return self._elements[loc]
        return None

    def remove(self, item):
        self._elements.remove(item)
        pass
