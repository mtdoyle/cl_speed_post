import pika
import db
import json
import check_address
import re

rabbitmq_server = json.load(open('servers.json'))['servers']['rabbitmq']

connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_server['host']))
channel = connection.channel()

channel.queue_declare(queue='clspeed', durable=True)
channel.basic_qos(prefetch_count=1)


def check_one_address(address):
    address = bytes.decode(address)
    address = re.sub(r'County Rd 31', 'Xerxes Ave S', address)
    speed = check_address.get_speed(address)
    if speed == -1:
        return
    address_as_dict = {}
    address_split = address.split(',')
    address_as_dict['street'] = address_split[0]
    address_as_dict['city'] = address_split[1]
    address_as_dict['zip'] = address_split[2]
    address_as_dict['emm_lat'] = address_split[3]
    address_as_dict['emm_lng'] = address_split[4]
    address_as_dict['emm_acc'] = address_split[5]
    address_as_dict['state'] = 'mn'
    db.write_entry(speed, address_as_dict)

def callback(ch, method, properties, body):
    check_one_address(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(callback,
                      queue='clspeed')

print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()