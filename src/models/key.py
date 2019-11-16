from models import remote_control

class KeyModel():
  def __init__(self, _id):
    # Remove "KEY_" part
    self.name = _id[4:]
    self.id = _id

  def json(self):
    return {'name': self.name, 'id': self.id}

  def press(self, device_name):
    return remote_control.press(device_name, self.id)

