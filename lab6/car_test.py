import requests

url = "http://localhost:8080/cars"

def print_car(car):
    print("Car ID:", car["id"])
    print("Make:", car["make"])
    print("Model:", car["model"])
    print("Year:", car["year"])
    print("VIN:", car["vin"])
    print("Color:", car["color"])
    print()

print("Requesting the list of all cars...")
response = requests.get(url) # sends a GET request
print("Status code:", response.status_code)
if response.status_code == 200:
    for car in response.json():
         print_car(car)

print("Adding a new car...")
new_car = { "make": "Fiat", "model":"Panda", "year":2020, "vin":"KL2SA3AR0SA716456", "color":"Black" }
response = requests.post(url, json = new_car) # sends a POST request with JSON data
print("Status code:", response.status_code)
if response.status_code == 201:
    print_car(response.json())


