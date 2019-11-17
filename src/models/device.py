# Here there is the class of the single device
# it contains:
# - list of keys
# - name
# - method to execute the command

from models import remote_control


class DeviceModel():
  def __init__(self, name):
    self.name = name
    self.keys = {}

  def insert_key(self, key):
    self.keys.update({key.name : key})

  def json(self):
    return {'name' : self.name, 'keys' : [ key.json() for key in self.keys.values()] }

  def press(self, key_name):
    try:
      key = self.keys[key_name]
    except:
      return None
    return self.keys[key_name].press(self.name)

  @classmethod
  def find_by_name(cls, name):
    return remote_control.find_device_by_name(name)

  def find_key_by_name(self, key_name):
    try:
      key = self.keys[key_name]
    except:
      return None
    return self.keys[key_name]
