# RabbitMQ - Example 3 - Publish/Subscribe

import pika, sys

server = 'localhost'

# Establish a connection to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(server))

# Create a channel for communication over the connection
channel = connection.channel()

# Declare an exchange named 'logs' of type fanout (instead of declaring a queue)
channel.exchange_declare(exchange = 'logs', exchange_type = 'fanout') # new

# Publish a message on the exchange
message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange = 'logs', routing_key = '', body = message) # modified

print(" [x] Sent '{}'".format(message))

# Close the connection to RabbitMQ
connection.close()

