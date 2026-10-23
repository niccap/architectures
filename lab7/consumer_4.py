# RabbitMQ - Example 4 - Routing

import pika, sys # modified

# Establish a connection and creates a channel
server = 'localhost'
connection = pika.BlockingConnection(pika.ConnectionParameters(server))
channel = connection.channel()

# Declare an exchange of type direct and creates a temporary queue
channel.exchange_declare(exchange = 'direct_logs', exchange_type = 'direct') # modified
queue = channel.queue_declare(queue = '', exclusive = True).method.queue

# Binds the queue with the routing keys specified in the command line
severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

for severity in severities:
    channel.queue_bind(exchange='direct_logs', queue = queue, routing_key = severity)

# Define a callback function to handle log messages - modified
def callback(ch, method, properties, body):
    print(" [x] {}: {}".format(method.routing_key, body.decode())) 

# Set up a consumer that will invoke the callback function when a message is received
channel.basic_consume(queue = queue, on_message_callback = callback, auto_ack = True)

print(' [*] Waiting for logs. To exit, press CTRL+C')
channel.start_consuming()


