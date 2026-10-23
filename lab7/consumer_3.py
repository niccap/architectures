# RabbitMQ - Example 3 - Publish/Subscribe

import pika # modified

server = 'localhost'

# Establish a connection and creates a channel
connection = pika.BlockingConnection(pika.ConnectionParameters(server))
channel = connection.channel()

# Declare an exchange named 'logs' of type fanout (instead of declaring a queue)
channel.exchange_declare(exchange = 'logs', exchange_type = 'fanout') # new

# Creates a temporary queue and binds it to the exchange
queue = channel.queue_declare(queue = '', exclusive = True).method.queue # new
channel.queue_bind(exchange = 'logs', queue = queue) # new

# Define a callback function to handle log messages - modified
def callback(ch, method, properties, body):
    print(" [x] {}".format(body.decode())) 

# Set up a consumer that will invoke the callback function when a message is received
channel.basic_consume(queue = queue, on_message_callback = callback, auto_ack = True)

print(' [*] Waiting for logs. To exit, press CTRL+C')

# Start consuming messages from the queue
channel.start_consuming()





