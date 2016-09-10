import numpy as np
from collections import Counter

class KD_TREE:
    
    # this queue keeps the k nearest points,value and distances
    class BOUNDED_PRIORITY_QUEUE:
        class _NODE_QUEUE:
            __slots__ = '_distance','_point','_value','_next'
            def __init__(self, distance, point, value):
                self._distance = distance
                self._point = point
                self._value = value
                self._next = None

            def __str__(self):
                return str(self._value)

        def __init__(self, max_length):
            self._len = 0
            self._max_length = max_length
            self._head = None
            self._tail = None
            self._type = None

        def __len__(self):
            return self._len

        def __str__(self):
            output = ""
            cursor = self._head
            while cursor != None:
                output += str(cursor._value) + ','
                cursor = cursor._next
            return output

        def is_empty(self):
            return self._len == 0
        
        def is_full(self):
            return (self._len == self._max_length)

        # insert a node in the queue if it is smaller than one element
        # then delete the highest element
        def insert(self, distance, point, value):     
            new_node = self._NODE_QUEUE(distance, point, value)

            if self.is_empty():
                self._head = new_node
                self._len = 1
                return 1
            
            cursor = self._head
            while cursor._next != None:
                if((cursor._point == point).all()):
                    return 1
                cursor = cursor._next
            if((cursor._point == point).all()):
                    return 1
                
            cursor = self._head

            if self._len < self._max_length:
                self._len += 1
                if cursor._distance < distance:
                    self._head, new_node._next = new_node, cursor
                    return 1

                while cursor._next != None and cursor._next._distance > distance:
                    cursor = cursor._next
                new_node._next, cursor._next = cursor._next, new_node
                return 1

            elif self._len == self._max_length:
                if cursor._distance < distance:
                    return 0

                while cursor._next != None and cursor._next._distance > distance:
                    cursor = cursor._next
                new_node._next, cursor._next = cursor._next, new_node

                self._head = self._head._next
                return 1

        def get_distances(self):
            output = list()
            cursor = self._head
            while cursor != None:
                output.append(cursor._distance)
                cursor = cursor._next
            return output

        def get_results(self):
            output = list()
            cursor = self._head
            while cursor != None:
                output.append(cursor._value)
                cursor = cursor._next
            return output
        
        def get_max(self):
            return self._head._distance

    class _NODE:
        def __init__(self, value, point, axis, location, parent=None):
            __slots__ = 'value','parent','point','axis','left','right','location'
            self.parent = parent
            self.point = point
            self.value = value
            self.axis = axis
            self.left = None
            self.right = None
            self.location = location
                    
        def __str__(self):
            return str(self.value)

    def __init__(self, max_depth, n_dim):
        self.max_depth = max_depth
        self.n_dim = n_dim
        self.root = None
        self.size = 0

    def __len__(self):
        return self.size   

    def median(self, n):
        if(n%2):
            return int(n/2)
        else:
            return n/2-1


    # arr is a list of points with the target at the last index
    def createTree(self, arr=None, current_node=None, axis=0):

        # split the points with the median on the nth axis
        temp = arr[arr[:,axis].argsort()]
        med = self.median(len(temp))
        
        if(self.size==0):
            current_node = self.add_root(temp[med,-1], temp[med,0:-1])
            current_node.axis = 0

        if(axis < self.max_depth):
            axis+=1
            
            if(self.size):
                current_node.point = temp[med,0:-1]
                current_node.value = temp[med,-1]
                current_node.axis = (axis%self.n_dim)

            left = self.add_left_node(temp[0:med,-1], current_node, temp[0:med,0:-1], axis)
            right = self.add_right_node(temp[(med+1):,-1], current_node, temp[(med+1):,0:-1], axis)

            self.createTree(temp[0:med,:], left, axis)
            self.createTree(temp[(med+1):,:], right, axis)
    
    def distance(self, point1, point2):
        tot = [(int(p1) - int(p2))**2 for p1, p2 in zip(point1, point2)]
        return sum(tot)
        
    def exploreTree(self, point, k, curr=None): 
        
        #initialization
        if(curr is None):
            curr = self.root
            self.best_dist = self.BOUNDED_PRIORITY_QUEUE(k)
        elif(curr.parent is None):
            return self.best_dist
        
        axis = curr.axis
        
        # Add the point to the queue. if it gets to a leaf, compare to each point in the leaf
        if curr.left is None:
            for i in range(len(curr.point)):
                self.best_dist.insert(self.distance(curr.point[i], point), curr.point[i], curr.value[i])
            return 
        else:    
            self.best_dist.insert(self.distance(curr.point, point), curr.point, curr.value)
        
        if(point[axis] < curr.point[axis]):
            curr = curr.left
        else:
            curr = curr.right
        self.exploreTree(point, k, curr)
        
        # when unwinding the recursion, test if a hyperspere would intersect a division
        if((not self.best_dist.is_full()) or (self.best_dist.get_max() > abs(point[axis] - curr.parent.point[axis]))):
            self.exploreTree(point, k, self.sibling(curr))

            
    def show(self):
        self.preorder(self.root)
        
    def preorder(self, curr):
        for child in self.children(curr):
            self.preorder(child)
            
    def root(self):
        return self.root
    
    def add_root(self, value, point):
        self.root = self._NODE(value, point, 0, None)
        self.size = 1
        return self.root

    def add_left_node(self, value, curr, point, axis):
        self.size += 1
        curr.left = self._NODE(value, point, axis, 'left', curr)
        return curr.left

    def add_right_node(self, value, curr, point, axis):
        self.size += 1
        curr.right = self._NODE(value, point, axis, 'right', curr)
        return curr.right
 
    def children(self, curr):
        if curr.left is not None:
            yield curr.left
        if curr.right is not None:
            yield curr.right

    def sibling(self, curr):
        if(curr.parent is None):
            return None
        
        p = curr.parent
        if(curr.location == 'left'):
            return p.right
        elif(curr.location == 'right'):
            return p.left
        
    def validate(self, test, k=1):
        accurate = 0
        point = test[:,0:-1]
        value = test[:,-1]

        for i in range(len(point)):
            tree.exploreTree(point[i], k)
            
            # vote for the most common target
            result = self.best_dist.get_results()
            
            most_common, occurence = Counter(result).most_common(1)[0]
            if occurence == 1:
                most_common = result[-1]

            if(most_common == value[i]):
                accurate += 1

        return accurate/len(point)