from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from resources.remote_control import RemoteControl
from resources.device import Device
from resources.key import Key
import socket

# Get own IP
my_ip = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]

app = Flask(__name__)
api = Api(app)

api.add_resource(RemoteControl, '/remote_control')
api.add_resource(Device, '/device/<string:name>')
api.add_resource(Key, '/device/<string:device_name>/key/<string:key_name>')

if __name__ == '__main__':
  app.run(host=my_ip, port=5000, debug=True)

