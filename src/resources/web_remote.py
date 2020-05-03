from flask import render_template, send_file
from models.device import DeviceModel
from models import remote_control

def index():
  return render_template('index.j2', title='Home', devices=remote_control.get_devices())

def get_remote_control_device(name):
  device = DeviceModel.find_by_name(name)
  return render_template('remote_control.j2', title='Home', device=device.json())

def get_stylesheet():
  return send_file('files/stylesheet.css')
