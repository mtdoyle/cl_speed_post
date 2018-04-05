# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import pika
import sys
import json

rabbitmq_settings = json.load(open('servers.json'))['servers']['rabbitmq']
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = 'edina_addresses_resolved'

f = open(filename,'r')

credentials = pika.PlainCredentials('guest', 'guest')

connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_settings['host'], port=rabbitmq_settings['port'], credentials=credentials))

channel = connection.channel()

channel.queue_delete(queue='clspeed')

channel.queue_declare(queue='clspeed', durable=True)

channel.queue_purge(queue='clspeed')

for item in f.readlines():
    channel.basic_publish(exchange='',
                        routing_key='clspeed',
                        body=item.strip(),)


connection.close()
