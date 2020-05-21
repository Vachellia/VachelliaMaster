import eventlet
eventlet.monkey_patch()

import pika
from flask import Flask
from termcolor import colored
from core.vachellia import Vachellia, get_json
from flask_socketio import SocketIO, send, emit

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
print(f"[ {colored('C TYPE', 'green')}  ] -> [ MASTER ]")
print(f"[ {colored('VERSION', 'green')} ] -> [ 0.01 ]")

vachellia = Vachellia(get_json(r"vachellia.json"))


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", sameSite=None)

@socketio.on('request')
def request(data):
    out_data = vachellia.operate_request(data)
    emit('response', out_data, namespace='/')


def callback(ch, method, properties, in_data):
    out_data = vachellia.operate_request(in_data)
    socketio.emit('response', out_data, broadcast=True)

def run_channel_listener():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="master")
    channel.basic_consume(queue="master", on_message_callback=callback, auto_ack=True)
    print(f"[ {colored('STARTED', 'green')} ] -> [ To exit press CTRL+C ]\n")
    channel.start_consuming()

eventlet.spawn(run_channel_listener)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0")
