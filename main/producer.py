# amqps://wpedxutb:lbSlJWRQcV4IA2H_6xhJ55ycIms4VQdM@lionfish.rmq.cloudamqp.com/wpedxutb
import pika, json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)