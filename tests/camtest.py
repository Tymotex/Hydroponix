from picamera import PiCamera
from time import sleep
import pycurl

import datetime

camera = PiCamera()
camera.vflip = True
camera.resolution = (1024, 768)
camera.start_preview(alpha=192)
sleep(1)
camera.capture("pic.jpg")
camera.stop_preview()

