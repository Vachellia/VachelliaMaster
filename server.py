import pika
from core.vachellia import Vachellia, get_json


vachellia = Vachellia(get_json(r"vachellia.json"))
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()
channel.queue_declare(queue="hello")
channel.queue_declare(queue="world")


def callback(ch, method, properties, in_data):
    # print(f"[🌿][callback][in_data] -> [ {in_data} ]")
    out_data = vachellia.operate_request(in_data)
    channel.basic_publish(exchange="", routing_key="world", body=out_data)


channel.basic_consume(queue="hello", on_message_callback=callback, auto_ack=True)
print("[🌿][Vachellia Up] ->  [ To exit press CTRL+C ]")
channel.start_consuming()
