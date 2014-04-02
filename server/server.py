from flask import Flask
from flask import request
from foursquare import Foursquare
from map import Map
import json

app = Flask(__name__)
app.secret_key = "ZjBjNTUzNWIyMmZmNDRkZGVmYzU5NDY2"

client = Foursquare(client_id='IGJS4FY0IXWLVJVG0IE0IFGIGBVT2HDBK1QAQYMP4WU2VKOE', client_secret='W3SBDEHHTCX2YUSD30Z1RUDIEBJRN3PHTVC0OVBZ0OBGHICK')
map = Map("edmonton-roads-2.0.1.txt")

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
  # Process the coordinates in a way that the map class can understand
  def process(val):
    return int(float(val)*100000)

  start = eval(request.args.get('start', '(0, 0)')) #53.65488,-113.33914
  end = eval(request.args.get('end', '(0, 0)')) #53.64727,-113.35890

  start = (process(start[0]), process(start[1]))
  end = (process(end[0]), process(end[1]))

  path = map.find_path(start, end)

  return str(map.get_path_names(path))

if __name__ == "__main__":
  app.run(debug=True)
