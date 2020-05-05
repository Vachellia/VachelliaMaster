import json
import pika
import base64
from core import RemoteClass, RequestManager

connection = pika.BlockingConnection(pika.ConnectionParameters(host="192.168.0.9"))
channel = connection.channel()
channel.queue_declare(queue="cell_1")


class Router(object):
    def __init__(self):
        self.class_instance_name = "Router"
        self.request_manager = RequestManager()
        self.new_request = self.request_manager.generate_request()

    def goto(self, parameters):
        print("[Router][test][parameters] -> ", parameters)
        self.router = RemoteClass("Temp", self.new_request)
        for procedure_call in parameters[1]:
            self.router.append_procedure_call(procedure_call)

        out_data = self.request_manager.compute_resolve(self.new_request, self.test2)
        base64_out_data = base64.b64encode(json.dumps(out_data).encode())
        print("[Router][test][remote_request] -> ", base64_out_data)
        channel.basic_publish(exchange="", routing_key="cell_1", body=base64_out_data)

        return {
            "status": "pending",
            "data": "request sent to ",
            "class_name": self.class_instance_name,
        }

    def test2(self, data):
        print(f"[test2] ->", data)
        return {
            "status": "pending",
            "data": "request sent to ",
            "class_name": self.class_instance_name,
        }
