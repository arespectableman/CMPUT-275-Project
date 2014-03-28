from flask import Flask
from flask import request
from foursquare import Foursquare
from graph import Graph
import json

app = Flask(__name__)
client = Foursquare(client_id='IGJS4FY0IXWLVJVG0IE0IFGIGBVT2HDBK1QAQYMP4WU2VKOE', client_secret='W3SBDEHHTCX2YUSD30Z1RUDIEBJRN3PHTVC0OVBZ0OBGHICK')

# Some little helper functions to help ease readability

def reconstruct_path(start, dest, parents):
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

def  straight_line_dist(lat1, lon1, lat2, lon2):
    """
    Computes the straightline distance between
    two points (lat1, lon1) and (lat2, lon2)
    """
    return ((lat2-lat1)**2 + (lon2-lon1)**2)**0.5

def process_coord(coord):
    """
    given a string with a standardlatitude or
    longitude coordinate convert it be in
    100, 1000ths of a degree. Truncate to be an
    int.
    """
    return int(float(coord)*100000)

def least_cost_path(graph, start, dest, cost):
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
            return reconstruct_path(start, dest, parents)

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

def load_edmonton_road_map(filename):
    """
    Read in the Edmonton Road Map Data from the
    given filename and create our Graph, a dictionary
    for looking up the latitude and longitude information
    for vertices and a dictionary for mapping streetnames
    to their associated edges.
    """
    graph = Graph()
    location = {}
    streetnames = {}

    with open(filename, 'r') as f:
        for line in f:
            elements = line.split(",")
            if(elements[0] == "V"):
                graph.add_vertex(int(elements[1]))
                location[int(elements[1])] = (process_coord(elements[2]),
                                              process_coord(elements[3]))
            elif (elements[0] == "E"):
                graph.add_edge((int(elements[1]), int(elements[2])))
                streetnames[(int(elements[1]), int(elements[2]))] = elements[3]

    return graph, location, streetnames


@app.route("/venues")
def venues():
  """
  Defaults location to Edmonton
  """
  latitude = request.args.get('lat', '53.523325')
  longitude = request.args.get('lng', '-113.524104')

  ll = u'' + latitude + ',' + longitude

  response = client.venues.search(params={'ll': ll})
  parsed_response = json.dumps(response)
  return str(parsed_response)

@app.route("/route")
def route():
  """
  Generate a route from one location to another.
  """

  # Process the coordinates
  def process(val):
    return int(float(val)*100000)

  start_lat = process(request.args.get('start_lat', '53.65488'))
  start_lng = process(request.args.get('start_lng', '-113.33914'))
  end_lat = process(request.args.get('end_lat', '53.64727'))
  end_lng = process(request.args.get('end_lng', '-113.35890'))

  # Find closest vertices to the provided lat and lon positions
  def find_closest_vertex(lat, lon):
    return min(location, key=lambda v:straight_line_dist(lat, lon, location[v][0], location[v][1]))

  start = find_closest_vertex(start_lat, start_lng)
  dest = find_closest_vertex(end_lat, end_lng)

  # Find path
  path = least_cost_path(graph, start, dest, cost_distance)

  # Print path out to stdout
  pretty_path = str(len(path))
  for v in path:
    pretty_path = pretty_path + " " + str(location[v][0]) + " " + str(location[v][1])

  return str(pretty_path)

graph, location, streetnames = load_edmonton_road_map("edmonton-roads-2.0.1.txt")

# Define our cost_distance function that takes in an edge e = (vertexid, vertexid)
cost_distance = lambda e: straight_line_dist(location[e[0]][0], location[e[0]][1],
                                             location[e[1]][0], location[e[1]][1])

if __name__ == "__main__":
  app.run(debug=True)

