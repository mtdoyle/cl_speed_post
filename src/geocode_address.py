import pika
import json
from pygeocoder import Geocoder
import time
import sys

from pygeolib import GeocoderError

rabbitmq_server = json.load(open('servers.json'))['servers']['rabbitmq']

connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_server['host']))
channel = connection.channel()

channel.queue_declare(queue='clspeed', durable=True)
channel.basic_qos(prefetch_count=1)

this = sys.modules[__name__]


def get_coords(address):
    geo_addr = None
    geocoder = Geocoder()
    try:
        geo_addr = geocoder.geocode(address).coordinates
    except GeocoderError as e:
        return get_coords(address)
    return geo_addr



def check_one_address(address):
    f = open('edina_addresses_coords','a')
    address = bytes.decode(address)
    coords = get_coords(address)
    try:
        f.write("{0},{1},{2},{3}\n".format(address, coords[0], coords[1], 'ROOFTOP'))
    except TypeError as e:
        print("debug")
    f.close()


def callback(ch, method, properties, body):
    check_one_address(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(callback,
                      queue='clspeed')

print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()