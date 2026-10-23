# EXERCISE
# Develop and test with Postman a Service Oriented System for car inventory management
# where the communication between the Car Inventory Service and the VIN Decoder Service 
# is asynchronous and uses RabbitMQ
# Vin Decoder Service
#
# Input Queue: car-info-request
# Output Queue: car-info-reply

import random, pika, time, json

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

server = 'localhost'
connection = pika.BlockingConnection(pika.ConnectionParameters(server))
channel = connection.channel()
channel.queue_declare(queue='car-info-request')
channel.queue_declare(queue='car-info-reply')

def callback(ch, method, properties, body):
    vin = body.decode()
    print(" [I] Received request for VIN: {}".format(vin))
    if len(vin) == 17:
        make = random.choice(list(models.keys()))
        info = {
            'vin': vin,
            'make': make,
            'model': random.choice(models[make]),
            'year': random.randint(1950, 2020),
            'color': random.choice (colors)
        }
    else: 
        info = {"error": "The requested vin is invalid"}
    time.sleep(random.randint(1, 5)) # simulate processing time
    channel.basic_publish(exchange = '', routing_key = 'car-info-reply', body = json.dumps(info))
    print(" [O] Sent car info: {}".format(str(info)))

channel.basic_consume(queue = 'car-info-request', on_message_callback = callback, auto_ack = True)
print(' [*] Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()

