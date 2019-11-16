# Here there is the module of remote_control
# It has to:
# - be able to read configuration
# - list the devices
from models.device import DeviceModel
from models.key import KeyModel

devices = []

def get_devices():
  return devices

def read_configurations():
  key_power = KeyModel('KEY_POWER')
  key_1 = KeyModel('KEY_1')
  device = DeviceModel(name = 'televisore',
    keys = {key_power.name : key_power, key_1.name: key_1 }
    )
  devices.append(device)

def find_device_by_name(name):
  for device in devices:
    if device.name == name:
      return device
  return None

def press(device_name, key_id):
  # Call to lircd to execute the action
  print("Call to lircd to execute on \"{}\" the \"{}\" key".format(device_name, key_id))
  return "OK"
