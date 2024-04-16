# amqps://wpedxutb:lbSlJWRQcV4IA2H_6xhJ55ycIms4VQdM@lionfish.rmq.cloudamqp.com/wpedxutb
import pika, json
from main import Product, db, app

# params = pika.URLParameters('amqps://ezkczogo:VVqntLhM0Q66X-yRLaX36WZ0R0Lh1YhZ@lionfish.rmq.cloudamqp.com/ezkczogo')

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.queue_declare(queue='main')

def callback(ch, method, properties, body):
    with app.app_context():   
        print('Recieved in main')
        data = json.loads(body)
        print(data)
        
        if properties.content_type == 'product_created':
            product = Product(id=data['id'], title=data['title'], image=data['image'])
            db.session.add(product)
            db.session.commit()
            print("New Product Created")
        
        elif properties.content_type == 'product_updated':
            product = Product.query.get(data['id'])
            # if product not at main level then create new
            if product is None:
                product = product = Product(id=data['id'], title=data['title'], image=data['image'])
                db.session.add(product)
            else:
                product.title = data['title']
                product.image = data['image']
            db.session.commit()
            print('Product Successfully Updated')

        elif properties.content_type == 'product_deleted':
            product = Product.query.get(data)
            if product is None:
                pass
            else:
                db.session.delete(product)
                db.session.commit()
            print('Product Deleted.')

channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()