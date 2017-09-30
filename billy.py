from flask import Flask
from flask import request
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit

mh = Adafruit_MotorHAT(addr=0x60)

def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

myMotor = mh.getMotor(1)

app = Flask(__name__)

@app.route("/")
def web_interface():
  html = open("web_interface.html")
  response = html.read().replace('\n', '')
  html.close()
  return response

@app.route("/set_speed")
def set_speed():
  speed = request.args.get("speed")
  print "Received " + str(speed)

  direction = Adafruit_MotorHAT.FORWARD
  if speed < 0:
    direction = Adafruit_MotorHAT.BACKWARD

  myMotor.setSpeed(abs(int(speed)))

  return "Received " + str(speed)

def main():
  myMotor.setSpeed(150)
  myMotor.run(Adafruit_MotorHAT.FORWARD);
  myMotor.run(Adafruit_MotorHAT.RELEASE);

  app.run(host= '0.0.0.0')

main()
