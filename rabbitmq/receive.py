# -*- coding: utf-8 -*-
import pika
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='hello_exchange',
                         exchange_type='direct',
                         passive=False,
                         durable=True,
                         auto_delete=False
                         )

channel.queue_declare(queue='hello_queue')
channel.queue_bind(queue='hello_queue',
                   exchange='hello_exchange',
                   routing_key='hello')


def callback(channel, method, properties, body):
    channel.basic_ack(delivery_tag=method.delivery_tag)
    if body == 'quit':
        channel.basic_cancel(consumer_tag='hello_consumer')
        channel.stop_consuming()
    else:
        print body
    return


channel.basic_consume(callback,
                      queue='hello_queue',
                      consumer_tag='hello_consumer')

channel.start_consuming()
