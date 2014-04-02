"""
Map module for working with map data.

It reads in map data from a file.
Each line in the file contains either a vertex or an edge
in the following format.

V(ertex),{id},{latitude},{longitude}
e.g. V,30198538,53.618369,-113.602987

E(dge),{vertex},{vertex},{name}
e.g. E,314080060,314080061,23 Avenue NW
"""

from graph import Graph

def straight_line_dist(lat1, lon1, lat2, lon2):
    """
    Computes the straightline distance between
    two points (lat1, lon1) and (lat2, lon2)
    """
    return ((lat2-lat1)**2 + (lon2-lon1)**2)**0.5

class Map:
    def __init__(self, filename):
        """
        Construct a new map. Delegates to load_map.
        """
        self.load_map(filename)

    def load_map(self, filename):
        """
        Read in the Road Map Data from the
        given filename and create our Graph, a dictionary
        for looking up the latitude and longitude information
        for vertices and a dictionary for mapping streetnames
        to their associated edges.

        Each line in the file contains either a vertex or an edge
        in the following format.

        V(ertex),{id},{latitude},{longitude}
        e.g. V,30198538,53.618369,-113.602987

        E(dge),{vertex},{vertex},{name}
        e.g. E,314080060,314080061,23 Avenue NW
        """
        self._graph = Graph()
        self._location = {}
        self._streetnames = {}

        with open(filename, 'r') as f:
            for line in f:
                elements = line.split(",")
                if(elements[0] == "V"):
                    self._graph.add_vertex(int(elements[1]))
                    self._location[int(elements[1])] = (self.process_coord(elements[2]),
                                                  self.process_coord(elements[3]))
                elif (elements[0] == "E"):
                    self._graph.add_edge((int(elements[1]), int(elements[2])))
                    self._streetnames[(int(elements[1]), int(elements[2]))] = elements[3]

    def reconstruct_path(self, start, dest, parents):
        """
        reconstruct_path reconstructs the shortest path from vertex
        start to vertex dest.

        "parents" is a dictionary which maps each vertex to their
        respective parent in the lowest cost path from start to that
        vertex.

        >>> parents = {'l': ' ', 'e': 'l', 'a': 'e', 'h':'a'}
        >>> reconstruct_path('l', 'h', parents)
        ['l', 'e', 'a', 'h']

        """
        current = dest
        path = [dest]

        while current != start:
            path.append(parents[current])
            current = parents[current]

        path.reverse()
        return path

    def process_coord(self, coord):
        """
        given a string with a standardlatitude or
        longitude coordinate convert it be in
        100, 1000ths of a degree. Truncate to be an
        int.
        """
        return int(float(coord)*100000)

    def least_cost_path(self, graph, start, dest, cost):
        """
        Using Dijkstra's algorithm to solve for the least
        cost path in graph from start vertex to dest vertex.
        Input variable cost is a function with method signature
        c = cost(e) where e is an edge from graph.

        >>> graph = Graph({1,2,3,4,5,6}, [(1,2), (1,3), (1,6), (2,1), (2,3), (2,4), (3,1), (3,2), \
                (3,4), (3,6), (4,2), (4,3), (4,5), (5,4), (5,6), (6,1), (6,3), (6,5)])
        >>> weights = {(1,2): 7, (1,3):9, (1,6):14, (2,1):7, (2,3):10, (2,4):15, (3,1):9, \
                (3,2):10, (3,4):11, (3,6):2, (4,2):15, (4,3):11, (4,5):6, (5,4):6, (5,6):9, (6,1):14,\
                (6,3):2, (6,5):9}
        >>> cost = lambda e: weights.get(e, float("inf"))
        >>> least_cost_path(graph, 1,5, cost)
        [1, 3, 6, 5]
        """
        # est_min_cost[v] is our estimate of the lowest cost
        # from vertex start to vertex v
        est_min_cost = {}

        # parents[v] is the parent of v in our current
        # shorest path from start to v
        parents = {}

        # todo is the set of vertices in our graph which
        # we have seen but haven't processed yet. This is
        # the list of vertices we have left "to do"
        todo = {start}

        est_min_cost[start] = 0

        while todo:
            current = min(todo, key=lambda x: est_min_cost[x])

            if current == dest:
                return self.reconstruct_path(start, dest, parents)

            todo.remove(current)

            for neighbour in graph.neighbours(current):
                #if neighbour isn't in est_min_cost, that means I haven't seen it before,
                #which means I should add it to my todo list and initialize my lowest
                #estimated cost and set it's parent
                if not neighbour in est_min_cost:
                    todo.add(neighbour)
                    est_min_cost[neighbour] = (est_min_cost[current] + cost((current, neighbour)))
                    parents[neighbour] = current
                elif est_min_cost[neighbour] > (est_min_cost[current] + cost((current, neighbour))):
                    #If my neighbour isn't new, then I should check if my previous lowest cost path
                    #is worse than a path going through vertex current. If it is, I will update
                    #my cost and record current as my new parent.
                    est_min_cost[neighbour] = (est_min_cost[current] + cost((current, neighbour)))
                    parents[neighbour] = current

        return []

    # Find closest vertices to the provided lat and lon positions
    def find_closest_vertex(self, lat, lon):
        return min(self._location, key=lambda v:straight_line_dist(lat, lon, self._location[v][0], self._location[v][1]))

    # Define our cost_distance function that takes in an edge e = (vertexid, vertexid)
    def cost_distance(self, e):
        return straight_line_dist(self._location[e[0]][0], self._location[e[0]][1],
                                                   self._location[e[1]][0], self._location[e[1]][1])

    def find_path(self, start, end):
        """
        Find a path from the start coordinates to the end coordinates.
        This simply returns the ids of the vertices.
        Call get_path_names with this path to get a more useful path.
        """
        start = self.find_closest_vertex(start[0], start[1])
        dest = self.find_closest_vertex(end[0], end[1])

        # Find path
        path = self.least_cost_path(self._graph, start, dest, self.cost_distance)
        return path

    def get_path_names(self, path):
        """
        Returns a list of a set of coordinates, two consequent pair of coordinates
        represent a path.
        """
        pretty_path = str(len(path))
        for v in path:
          pretty_path = pretty_path + " " + str(self._location[v][0]) + " " + str(self._location[v][1])
        return pretty_path
        
    def greedy_route(l):
    """
    Generate a route between multiple places using a greedy algorithm
    where l is a list of vertices and l[0] is the starting node.
    """
    #start at the beginning, remove is from remaining possibilities
    current = l[0]
    l.pop(0)
    greedy_path = [current]

    #while there are still places to go
    While l != 0:
        nearest_dist = float("inf")
        nearest_vert = None

        #find the nearest vertex in l
        for i in l:
            path = find_path(current, i)
            if path[4] < nearest_dist:
                nearest_dist = path[4]
                nearest_vert = i

        #remove it and add it to the greedy_path
        current = nearest_vert
        l.remove(current)
        greedy_path.append(current)
            
   return greedy_path
