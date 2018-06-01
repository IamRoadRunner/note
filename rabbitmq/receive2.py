import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='names',
                         type='fanout')

#队列持久化
channel.queue_declare(queue='hello2', durable=True, exclusive=True)

#binding
channel.queue_bind(exchange='names',
                   queue='hello2')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count('.'))
    #防止丢失，没有回复会重新发送
    ch.basic_ack(delivery_tag=method.delivery_tag)

#公平调度
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='hello')

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()