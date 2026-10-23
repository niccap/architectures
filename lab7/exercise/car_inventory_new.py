# EXERCISE
# Develop and test with Postman a Service Oriented System for car inventory management
# where the communication between the Car Inventory Service and the VIN Decoder Service 
# is asynchronous and uses RabbitMQ
#
# Car Inventory Service
#
# HTTP method  API endpoint  Description
# GET          /cars         Get the list of all cars
# GET          /cars/<id>    Get the info of a single car
# POST         /cars         Add a new car
# DELETE       /cars/<id>    Delete a car

from flask import Flask, request, jsonify
from waitress import serve
import pika, threading, json
app = Flask(__name__)

cars = [
    { "id": 1, "make": "GMC", "model": "1500 Club Coupe", "year": 1998, "vin": "1D7RV1GTXAS806941", "color": "Red" },
    { "id": 2, "make": "Lamborghini", "model":"Gallardo", "year":2006, "vin":"JN1BY1PR0FM736887", "color":"Mauve" },
    { "id": 3, "make": "Chevrolet", "model":"Monte Carlo", "year":1996, "vin":"1G4HP54K714224234", "color":"Violet" }
]

server = 'localhost'
connection = pika.BlockingConnection(pika.ConnectionParameters(server))
channel = connection.channel()
channel.queue_declare(queue='car-info-request')
lock = threading.Lock()

## helper functions

def _find_next_id():
    with lock:
        id = max(car["id"] for car in cars) + 1
    return id

def _find_car_pos(id = None, vin = None):
    for pos, car in enumerate(cars):
        if id and car["id"] == id:
            return pos
        if vin and car["vin"] == vin:
            return pos
    return -1

def _has_all_fields(car):
    return set(car.keys()) == set(["id", "vin"])

## handlers

@app.get("/cars")
def get_cars():
    return jsonify(cars) # generates JSON from a Python list

@app.get("/cars/<int:id>")
def get_car(id):
    pos = _find_car_pos(id)
    if pos >= 0:
        return cars[pos]
    return {"error": "The requested id was not found"}, 404

@app.post("/cars")
def add_car():
    if not request.is_json:
        return {"error": "Request must be JSON"}, 415
    car = request.get_json()
    if _find_car_pos(vin = car["vin"]) != -1:
        return {"error": "The requested vin is already in use"}, 409
    car["id"] = _find_next_id()
    if _has_all_fields(car):
        with lock: cars.append(car) # add the temporary version
        channel.basic_publish(exchange = '', routing_key = 'car-info-request', body = car["vin"]) # ask the missing info
        print(" [O] Sent request for VIN: {}".format(car["vin"]))
        return car, 201
    return {"error": "Request has invalid or missing data"}, 422

@app.delete("/cars/<int:id>")
def delete_car(id):
    pos = _find_car_pos(id)
    if pos >= 0:
        with lock: cars.pop(pos)
        return "", 204
    return {"error": "The requested id was not found"}, 404

## main

def callback(ch, method, properties, body):
    info = body.decode()
    print(" [I] Received car info: {}".format(info))
    info = json.loads(info)
    if "error" not in info and "vin" in info:
        pos = _find_car_pos(vin = info["vin"])
        if pos >= 0:
            with lock: cars[pos].update(info)
    else:
        print("Error")

def consume_thread():
    # note: it is not safe to use the same connection in multiple threads
    connection = pika.BlockingConnection(pika.ConnectionParameters(server))
    channel = connection.channel()
    channel.queue_declare(queue='car-info-reply')
    channel.basic_consume(queue = 'car-info-reply', on_message_callback = callback, auto_ack = True)
    channel.start_consuming()
    
threading.Thread(target = consume_thread).start()
serve(app, listen='*:8080')
