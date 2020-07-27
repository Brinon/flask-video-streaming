#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np

# import camera driver
if os.environ.get('CAMERA', 'pi'):
  Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
  from camera import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)


@app.route('/')
def index():
  """Video streaming home page."""
  return render_template('index.html')


def last_frame():
  return render_template('last_frame.html')


def gen(camera):
  """Video streaming generator function."""
  while True:
    frame_arr = camera.get_frame()
    _, arr = frame = cv2.imencode('.jpeg', frame_arr)

    yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + arr.tostring() + b'\r\n')


@app.route('/video_feed')
def video_feed():
  """Video streaming route. Put this in the src attribute of an img tag."""
  return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/frame')
def frame():
  """ returns the latest frame as a str """
  frame_arr = Camera().get_frame()
  _, arr = frame = cv2.imencode('.jpeg', frame_arr)
  return Response(arr.tostring(), mimetype='image/jpeg')

if __name__ == '__main__':
  app.run(host='0.0.0.0', threaded=True)
