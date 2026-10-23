# RabbitMQ - Example 1 - Hello World

import pika

server = 'localhost'

# Establish a connection to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(server))

# Create a channel for communication over the connection
channel = connection.channel()

# Declare a queue named 'hello' (if it doesn't exist, create it)
channel.queue_declare(queue = 'hello')

# Publish a message to the 'hello' queue
channel.basic_publish(exchange = '', routing_key = 'hello', body = 'Hello World!')

print(" [x] Sent 'Hello World!'")

# Close the connection to RabbitMQ
connection.close()



