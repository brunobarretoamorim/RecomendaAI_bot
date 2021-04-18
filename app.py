from flask import Flask, request, render_template, jsonify
import subprocess

#app = Flask("Modelo")
app = Flask(__name__)

@app.route("/")
def index():
  return render_template('index.html')

   
@app.route("/hello", methods=["GET"])
def hello():
    return "Hello check!!!"

