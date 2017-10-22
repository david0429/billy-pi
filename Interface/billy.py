from flask import Flask
from flask import request
from playsound import playsound
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit

app = Flask(__name__)

mh = Adafruit_MotorHAT(addr=0x60)
myMotor1 = mh.getMotor(1)
myMotor1.setSpeed(150)
myMotor1.run(Adafruit_MotorHAT.FORWARD)
myMotor1.run(Adafruit_MotorHAT.RELEASE)
myMotor2 = mh.getMotor(2)
myMotor2.setSpeed(150)
myMotor2.run(Adafruit_MotorHAT.FORWARD)
myMotor2.run(Adafruit_MotorHAT.RELEASE)

def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

@app.route("/")
def web_interface():
  html = open("web_interface.html")
  response = html.read().replace('\n', '')
  html.close()
  myMotor1.setSpeed(0)
  myMotor2.setSpeed(40)
  return response

@app.route("/set_speed1")
def set_speed1():
  speed = request.args.get("speed")
  print "Received " + str(speed)

  direction = Adafruit_MotorHAT.FORWARD
  if int(speed) < 0:
    direction = Adafruit_MotorHAT.BACKWARD

  myMotor1.run(direction)
  myMotor1.setSpeed(abs(int(speed)))

  return "Received " + str(speed)

@app.route("/set_speed2")
def set_speed2():
  speed = request.args.get("speed")
  print "Received " + str(speed)

  direction = Adafruit_MotorHAT.BACKWARD

  myMotor2.run(direction)
  myMotor2.setSpeed(abs(int(speed)))

  return "Received " + str(speed)

@app.route("/set_audio")
def set_audio():
  sound = request.args.get("sound")
  print "Received " + str(sound)
  playSound(sound + ".mp3")
  return "Received " + str(sound)

def playSound(fileName):
  print "Playing " + fileName
  playsound("audio/" + fileName)
  print "DONE"

def main():
  app.run(host= '0.0.0.0')

main()
