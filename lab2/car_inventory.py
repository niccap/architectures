# LAB 2 - EXERCISE
# Develop and test with Postman a Web Service for car inventory management
#
# HTTP method  API endpoint  Description
# GET          /cars         Get the list of all cars
# GET          /cars/<id>    Get the info of a single car
# POST         /cars         Add a new car
# PUT          /cars/<id>    Modify car data
# PATCH        /cars/<id>    Modify part of the car data
# DELETE       /cars/<id>    Delete a car

from flask import Flask, request, jsonify
from waitress import serve

app = Flask(__name__)

cars = [
    { "id": 1, "make": "GMC", "model": "1500 Club Coupe", "year": 1998, "vin": "1D7RV1GTXAS806941", "color": "Red" },
    { "id": 2, "make": "Lamborghini", "model":"Gallardo", "year":2006, "vin":"JN1BY1PR0FM736887", "color":"Mauve" },
    { "id": 3, "make": "Chevrolet", "model":"Monte Carlo", "year":1996, "vin":"1G4HP54K714224234", "color":"Violet" }
]

fields = ["id", "make", "model", "year", "vin", "color"]

## helper functions

def _find_next_id():
    return max(car["id"] for car in cars) + 1

def _find_car_pos(id):
    for pos, car in enumerate(cars):
        if car["id"] == id:
            return pos
    return -1

def _has_all_fields(car):
    return set(car.keys()) == set(fields)

def _has_valid_fields(car):
    return set(car.keys()).issubset(set(fields))

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
    car["id"] = _find_next_id()
    if _has_all_fields(car):
        cars.append(car)
        return car, 201
    return {"error": "Request has invalid or missing data"}, 422

@app.put("/cars/<int:id>")
def modify_car(id):
    if not request.is_json:
        return {"error": "Request must be JSON"}, 415
    car = request.get_json()
    car["id"] = id
    if not _has_all_fields(car):
        return {"error": "Request has invalid or missing data"}, 422
    pos = _find_car_pos(id)
    if pos >= 0:
        cars[pos] = car
        return car
    return {"error": "The requested id was not found"}, 404

@app.patch("/cars/<int:id>")
def modify_car_part(id):
    if not request.is_json:
        return {"error": "Request must be JSON"}, 415
    car = request.get_json()
    car["id"] = id
    if not _has_valid_fields(car):
        return {"error": "Request has invalid data"}, 422
    pos = _find_car_pos(id)
    if pos >= 0:
        for key in car:
            cars[pos][key] = car[key]
        return cars[pos]
    return {"error": "The requested id was not found"}, 404

@app.delete("/cars/<int:id>")
def delete_car(id):
    pos = _find_car_pos(id)
    if pos >= 0:
        cars.pop(pos)
        return "", 204
    return {"error": "The requested id was not found"}, 404

serve(app, listen='*:8080')