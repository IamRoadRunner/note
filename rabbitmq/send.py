import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
channel = connection.channel()

# 声明交换机
channel.exchange_declare(exchange='names',
                         type='fanout')

channel.queue_declare(queue='hello')
channel.queue_declare(queue='hello2', durable=True)

for i in range(1,6):
    print("sending:%s"%('.'*i))
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body='%s'%('.'*i),
                          #消息持久化
                          properties=pika.BasicProperties(
                              delivery_mode=2
                          ))

connection.close()