from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/set_speed")
def set_speed():
  speed = request.args.get("speed")
  print "Received " + str(speed)
  return "Received " + str(speed)

app.run(host= '0.0.0.0')
