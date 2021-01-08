import paho.mqtt.client as mqtt
import json
import time


# mosquitto_pub -h dojot.atlantico.com.br -p 1883  -t /gesad/9e4ed4/attrs -m '{"breathing": true, "crying": true, "from": "bm", "sleeping": true, "time_no_breathing": 0, "to": "smp", "type": "notification" }'


class ClientBM:
    def __init__(self):
        self.client = mqtt.Client("bm")
        self.client.connect(host="dojot.atlantico.com.br", port=1883)
        self.client.on_message = self.callback
        self.client.on_publish = self.on_publish

    # pub to bm in dojot
    def publish_to_dojot(self, data):
        m = self.client.publish("/gesad/9e4ed4/attrs", payload=json.dumps(data))
        # while not m.is_published():
        #     self.client.publish("/gesad/9e4ed4/attrs", payload=json.dumps(data))
        #     print(m.is_published())
        #     time.sleep(1)

    def on_publish(self, client, userdata, result):
        if result == 0:
            print("data published")
        else:
            print("error on publishing")

    def subscribe(self):
        self.client.subscribe("/gesad/9e4ed4/attrs")

    def callback(self):
        self.internal_state = "normal"
        print("ok")

