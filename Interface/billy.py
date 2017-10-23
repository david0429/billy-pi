from flask import Flask
from flask import request
import pygame
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit

app = Flask(__name__)

mh = Adafruit_MotorHAT(addr=0x60, freq=100)
myMotor1 = mh.getMotor(1)
myMotor1.setSpeed(150)
myMotor1.run(Adafruit_MotorHAT.FORWARD)
myMotor1.run(Adafruit_MotorHAT.RELEASE)
myMotor2 = mh.getMotor(2)
myMotor2.setSpeed(150)
myMotor2.run(Adafruit_MotorHAT.FORWARD)
myMotor2.run(Adafruit_MotorHAT.RELEASE)
myMotor3 = mh.getMotor(3)
myMotor3.setSpeed(150)
myMotor3.run(Adafruit_MotorHAT.FORWARD)
myMotor3.run(Adafruit_MotorHAT.RELEASE)

def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

@app.route("/")
def web_interface():
  html = open("web_interface.html")
  response = html.read().replace('\n', '')
  html.close()
  myMotor1.setSpeed(0)
  myMotor2.setSpeed(40)
  myMotor3.setSpeed(40)
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

@app.route("/open_mouth")
def openMouth():
  print "Opening"
  myMotor3.run(Adafruit_MotorHAT.BACKWARD)
  myMotor3.setSpeed(36)
  return "Opened"

@app.route("/close_mouth")
def closeMouth():
  print "Closing"
  myMotor3.run(Adafruit_MotorHAT.BACKWARD)
  myMotor3.setSpeed(48)
  return "Closed"

@app.route("/set_audio")
def set_audio():
  sound = request.args.get("sound")
  print "Received " + str(sound)
  playSound(sound + ".mp3")
  return "Received " + str(sound)

def playSound(fileName):
  print "Playing " + fileName
  pygame.mixer.music.load("audio/" + fileName)
  pygame.mixer.music.play()
  openMouth()
  print "DONE"

def main():
  pygame.mixer.init()
  app.run(host= '0.0.0.0')

main()
