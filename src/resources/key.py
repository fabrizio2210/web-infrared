from flask_restful import Resource
from models.device import DeviceModel
from models.key import KeyModel

class Key(Resource):
  def post(self, device_name, key_name):
    device = DeviceModel.find_by_name(device_name)
    if device:
      key = device.find_key_by_name(key_name)
      if key:
        result = key.press(device_name)
        if result == "OK":
          return {'message' : 'Action executed' }, 200
        else:
          return {'error' : 'Something went wrong during the execution of action: {}'.format(result)}, 500
      return {'error': 'Key not found'}, 404
    return {'error': 'Device not found'}, 404
