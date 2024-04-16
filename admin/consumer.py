# amqps://wpedxutb:lbSlJWRQcV4IA2H_6xhJ55ycIms4VQdM@lionfish.rmq.cloudamqp.com/wpedxutb
import pika, json, os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()
from product.models import Product

# params = pika.URLParameters('amqps://ezkczogo:VVqntLhM0Q66X-yRLaX36WZ0R0Lh1YhZ@lionfish.rmq.cloudamqp.com/ezkczogo')

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
    print('Recieved in admin')
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    product.likes = product.likes + 1
    product.save()
    print('Product likes increased!')

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()