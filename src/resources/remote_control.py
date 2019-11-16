from flask_restful import Resource
from models import remote_control

remote_control.read_configurations()

class RemoteControl(Resource):
  def get(self):
    return {'devices':[device.json() for device in remote_control.get_devices()]}

