# Here there is the module of remote_control
# It has to:
# - be able to read configuration
# - list the devices
from models.device import DeviceModel
from models.key import KeyModel
import subprocess
import os
import re

conf_dir = 'conf/'
devices = []

def get_devices():
  return devices

def read_configurations():
  for file in os.listdir(conf_dir):
    if file.endswith(".lircd.conf"):
      f = open(os.path.join(conf_dir, file), 'r')
      device = DeviceModel(name = file[:-11])
      stop = False
      start = False
      for row in f:
        if re.search("end codes", row):
          stop = True
        if start and not stop:
          key = KeyModel(re.findall("KEY_\w+", row)[0])
          device.insert_key(key)
        if re.search("begin codes", row):
          start = True
      f.close()
      devices.append(device)

def find_device_by_name(name):
  for device in devices:
    if device.name == name:
      return device
  return None

def press(device_name, key_id):
  # Call to lircd to execute the action
  #print("Call to lircd to execute on \"{}\" the \"{}\" key".format(device_name, key_id))
  try:
    # irsend SEND_ONCE televisore KEY_POWER
    result = subprocess.run(['irsend', 'SEND_ONCE', device_name, key_id], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
      return "OK"
    else:
      return result.stdout
  except Exception as e: print(e)
  finally:
    return "ERROR"


