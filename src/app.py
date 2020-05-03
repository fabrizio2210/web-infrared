from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask import render_template
from resources.remote_control import RemoteControl
from models import remote_control
from resources.device import Device
from resources.key import Key
from resources import web_remote
from utils.networking import get_my_ip


app = Flask(__name__)
api = Api(app)
api.add_resource(RemoteControl, '/remote_control')
api.add_resource(Device, '/device/<string:name>')
api.add_resource(Key, '/device/<string:device_name>/key/<string:key_name>')

app.add_url_rule('/', view_func=web_remote.index)
app.add_url_rule('/device/<string:name>/web', view_func=web_remote.get_remote_control_device)

if __name__ == '__main__':
# Get own IP
  my_ip = get_my_ip()
  app.run(host=my_ip, port=5000, debug=True)
