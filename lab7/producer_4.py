# RabbitMQ - Example 4 - Routing

import pika, sys

# Establish a connection to the RabbitMQ server
server = 'localhost'
connection = pika.BlockingConnection(pika.ConnectionParameters(server))

# Create a channel for communication over the connection
channel = connection.channel()

# Declare an exchange of type direct
channel.exchange_declare(exchange = 'direct_logs', exchange_type = 'direct') # modified

# Generate a message from command line parameters
severity = sys.argv[1] if len(sys.argv) > 1 else 'info' # new
message = ' '.join(sys.argv[2:]) or "Hello World!" # modified

# Publish the message on the exchange
channel.basic_publish(exchange = 'direct_logs', routing_key = severity, body = message) # modified

print(" [x] Sent '{}'".format(message))

# Close the connection to RabbitMQ
connection.close()






