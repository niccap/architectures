# RabbitMQ - Example 2 - Work Queues

import pika, sys # modified

server = 'localhost'

# Establish a connection to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(server))

# Create a channel for communication over the connection
channel = connection.channel()

# Declare a queue named 'hello' (if it doesn't exist, create it)
channel.queue_declare(queue = 'hello')

# Publish a message to the 'hello' queue
message = ' '.join(sys.argv[1:]) or "Hello World!" # new
channel.basic_publish(exchange = '', routing_key = 'hello', body = message) # modified

print(" [x] Sent '{}'".format(message)) # modified

# Close the connection to RabbitMQ
connection.close()


