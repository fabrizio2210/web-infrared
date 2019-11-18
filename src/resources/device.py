from flask_restful import Resource
from models.device import DeviceModel

class Device(Resource):
  def get(self, name):
    device = DeviceModel.find_by_name(name)
    if device:
      return { 'device' : device.json()}
    return {'message': 'Device not found'}, 404

