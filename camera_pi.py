import io
import time
import picamera
import numpy as np
import cv2

from base_camera import BaseCamera

CAMERA_RESOLUTION = 1080, 720
CAMERA_FRAMERATE = 30


class Camera(BaseCamera):

  @staticmethod
  def frames():
    with picamera.PiCamera() as camera:
      camera.resolution = CAMERA_RESOLUTION
      camera.framerate = CAMERA_FRAMERATE
      # let camera warm up
      time.sleep(2)

      stream = np.empty(CAMERA_RESOLUTION + (3,), np.uint8)
      stream = io.BytesIO()
      for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
	# return current frame
	stream.seek(0)
	frame_stream = stream.read()
	frame_array = cv2.imdecode(np.fromstring( frame_stream, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
	yield frame_array 
	stream.seek(0) 
	stream.truncate()
