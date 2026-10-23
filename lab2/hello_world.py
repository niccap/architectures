#hello_world.py
from flask import Flask
from waitress import serve

app = Flask(__name__)

@app.get("/")
def hello_world():
    return "<p>Hello, World!</p>"

serve(app, listen='*:8080')