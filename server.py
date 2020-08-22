import eventlet
import sys

eventlet.monkey_patch()

import pika
from flask import Flask
from termcolor import colored
from core.vachellia import Vachellia, get_json
from flask_socketio import SocketIO, send, emit


app = Flask(__name__)
vachellia_json = get_json(r"vachellia.json")
vachellia = Vachellia(vachellia_json)
socketio = SocketIO(app, cors_allowed_origins="*", sameSite=None)

print(
    colored(
        """
██    ██  █████   ██████ ██   ██ ███████ ██      ██      ██  █████  
██    ██ ██   ██ ██      ██   ██ ██      ██      ██      ██ ██   ██ 
██    ██ ███████ ██      ███████ █████   ██      ██      ██ ███████ 
 ██  ██  ██   ██ ██      ██   ██ ██      ██      ██      ██ ██   ██ 
  ████   ██   ██  ██████ ██   ██ ███████ ███████ ███████ ██ ██   ██ 
                                                                    
    """
    )
)
print(f"[ {colored('C TYPE', 'green')}  ] -> [ {vachellia_json['name']} ]")
print(f"[ {colored('VERSION', 'green')} ] -> [ {vachellia_json['version']} ]")


@socketio.on("request")
def request(data):
    out_data = vachellia.operate_request(data)
    emit("response", out_data, namespace="/")


def callback(ch, method, properties, in_data):
    out_data = vachellia.operate_request(in_data)
    socketio.emit("response", out_data, broadcast=True)


def run_channel_listener():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=vachellia_json["pika_host"])
        )
        channel = connection.channel()
        channel.queue_declare(queue=vachellia_json["name"])
        channel.basic_consume(
            queue=vachellia_json["name"], on_message_callback=callback, auto_ack=True
        )
        print(
            f"[ {colored('PIKA STARTING', 'green')} ] -> [ {vachellia_json['pika_host']} ]"
        )
        print(f"[ {colored('SERVER STARTED', 'green')} ] -> [ To exit press CTRL+C ]\n")
        channel.start_consuming()
    except Exception as error:
        print(error)
        print(f"[ {colored('PIKA FAILED', 'red')} ] -> [ {vachellia_json['pika_host']} ]")
        # sys.exit(1)

eventlet.spawn(run_channel_listener)

if __name__ == "__main__":
    print(
        f"[ {colored('SOCKET STARTING', 'green')} ] -> [ {vachellia_json['socket_host']}:{vachellia_json['socket_port']} ]"
    )
    socketio.run(
        app, host=vachellia_json["socket_host"], port=vachellia_json["socket_port"]
    )
