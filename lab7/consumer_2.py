# RabbitMQ - Example 2 - Work Queues

import pika, time # modified

server = 'localhost'

# Establish a connection to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(server))

# Create a channel for communication over the connection
channel = connection.channel()

# Declare a queue named 'hello' (if it doesn't exist, create it)
channel.queue_declare(queue='hello')

# Define a callback function to handle received messages
def callback(ch, method, properties, body):
    print(" [x] Received {}".format(body.decode())) 
    time.sleep(body.decode().count('.')) # new
    print(" [x] Done") # new
    ch.basic_ack(delivery_tag = method.delivery_tag) # manual ack <--

# Set up a consumer that will invoke the callback function when a message is received
channel.basic_qos(prefetch_count = 1) # last update <-----
channel.basic_consume(queue = 'hello', on_message_callback = callback) # auto_ack removed <--

print(' [*] Waiting for messages. To exit, press CTRL+C')

# Start consuming messages from the queue
channel.start_consuming()


