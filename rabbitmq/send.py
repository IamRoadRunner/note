# -*- coding: utf-8 -*-
import pika
import sys
from pika import spec

connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
channel = connection.channel()

# def confirm_handler(frame):
#     if type(frame.method) == spec.Confirm.SelectOk:
#         print 'channel in confirm mode'
#     elif type(frame.method) == spec.Basic.Nack:
#         if frame.method.delivery_tag in msg_ids:
#             print 'message lost!'
#     elif type(frame.method) == spec.Basic.Ack:
#         if frame.method.delivery_tag in msg_ids:
#             print 'confirm received!'
#             msg_ids.remove(frame.method.delivery_tag)
#
# channel.confirm_delivery(callback=confirm_handler)

# 声明交换机
channel.exchange_declare(exchange='hello_exchange',
                         exchange_type='direct',
                         passive=False,
                         durable=True,
                         auto_delete=False
                         )

msg = sys.argv[1]
msg_props = pika.BasicProperties(content_type = 'text/plain')
msg_ids = []


channel.basic_publish(
    body=msg,
    exchange='hello_exchange',
    routing_key='hello',
    properties=msg_props
)

msg_ids.append(len(msg_ids) + 1)
channel.close()
