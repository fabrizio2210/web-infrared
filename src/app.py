from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import socket

my_ip = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]

app = Flask(__name__)
api = Api(app)


items = []

class Item(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('price',
    type=float,
    required=True,
    help="This field can not be blank."
  )
  def get(self, name):
    item = next(filter(lambda x: x['name'] == name, items), None)
    return {'item': item}, 200 if item else 404

  def post(self, name):
    if next(filter(lambda x: x['name'] == name, items), None):
      return {'message': "An item with name '{}' already exists.".format(name)}, 400
    data = Item.parser.parse_args()
    item = {'name': name, 'price': data['price']}
    items.append(item)
    return item, 201

  def delete(self, name):
    global items
    items = list(filter(lambda x: x['name'] != name, items))
    return{'message': "item deleted"}

  def put(self, name):
    data = Item.parser.parse_args()
    item =  next(filter(lambda x: x['name'] == name, items), None)
    if item is None:
      item ={ 'name': name, 'price': data['price']}
      items.append(item)
    else:
      item.update(data)
    return item

class ItemList(Resource):
  def get(self):
    return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(host=my_ip, port=5000, debug=True)
