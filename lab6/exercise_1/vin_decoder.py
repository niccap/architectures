# EXERCISE 1
# Develop and test with Postman a Service Oriented System for car inventory management
# Vin Decoder Service
#
# HTTP method  API endpoint   Description
# GET          /decode/<vin>  Get the information of a car with a given vin

from flask import Flask
from waitress import serve
import random
app = Flask(__name__)

models = {
    'Toyota': ['Corolla', 'Camry', 'Rav4', 'Prius', 'Highlander'],
    'Ford': ['Fusion', 'Focus', 'Escape', 'Explorer', 'Mustang'],
    'Honda': ['Civic', 'Accord', 'CR-V', 'Pilot', 'Odyssey'],
    'Chevrolet': ['Malibu', 'Cruze', 'Equinox', 'Tahoe', 'Silverado'],
    'Volkswagen': ['Golf', 'Jetta', 'Passat', 'Tiguan', 'Atlas'],
    'BMW': ['3 Series', '5 Series', 'X3', 'X5', '7 Series'],
    'Mercedes-Benz': ['C-Class', 'E-Class', 'GLC', 'GLE', 'S-Class'],
    'Audi': ['A3', 'A4', 'Q5', 'Q7', 'A8'],
    'Hyundai': ['Elantra', 'Sonata', 'Tucson', 'Santa Fe', 'Kona'],
    'Nissan': ['Altima', 'Maxima', 'Rogue', 'Pathfinder', 'Titan']
}

colors = [
    'Red', 'Blue', 'Green', 'Black', 'White', 'Silver', 'Gray', 'Yellow', 'Orange', 'Brown',
    'Gold', 'Purple', 'Pink', 'Turquoise', 'Magenta', 'Lime', 'Teal', 'Beige', 'Cyan', 'Indigo',
    'Maroon', 'Olive', 'Violet', 'Charcoal', 'Ruby', 'Sapphire', 'Emerald', 'Ivory', 'Pearl', 'Crimson'
]

## handlers

@app.get("/decode/<string:vin>")
def decode_vin(vin):
    if len(vin) == 17:
        make = random.choice(list(models.keys()))
        return {
            'make': make,
            'model': random.choice(models[make]),
            'year': random.randint(1950, 2020),
            'color': random.choice (colors)
        }
    return {"error": "The requested vin is invalid"}, 422

serve(app, listen='*:8081')