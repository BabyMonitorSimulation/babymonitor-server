import paho.mqtt.client as mqtt
import json


class ClientBM:
    def __init__(self):
        self.client = mqtt.Client("bm")
        self.client.connect(host="dojot.atlantico.com.br", port=1883)
        self.client.on_message = self.callback
        self.internal_state = 'normal'

    def publish_to_dojot(self, data):
        self.client.publish("/gesad/9e4ed4/attrs", payload=json.dumps(data))

    def subscribe(self):
        self.client.subscribe("/gesad/9e4ed4/attrs")
        

    def callback(self):
        self.internal_state = 'normal'
        print('ok')