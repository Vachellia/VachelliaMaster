import json
import base64
from core import RemoteClass, RequestManager
from termcolor import colored


class Router(object):
    def __init__(self):
        self.class_instance_name = "Router"
        self.request_manager = RequestManager()

    def goto(self, parameters):
        print(
            f"[{colored('OK', 'green')}][{colored(parameters[2], 'green')}] -> [Routing request data to /{parameters[0]}]", 
        )
        self.new_request = self.request_manager.generate_request(parameters[2])
        self.router = RemoteClass("Temp", self.new_request)
        for procedure_call in parameters[1]:
            self.router.append_procedure_call(procedure_call)

        return {
            "status": "pending",
            "data": "routing request data",
            "class_name": self.class_instance_name,
            "message_channel": parameters[0],
            "message_host": "192.168.0.9",
            "request": self.new_request,
            "continue_method": self.goto_response,
        }

    def goto_response(self, data):
        print(
            f"[{colored('OK', 'green')}][{colored(self.new_request.get_id(), 'green')}] -> [Routed request data responded]"
        )
        return {
            "status": "success",
            "data": data,
            "class_name": self.class_instance_name,
        }
