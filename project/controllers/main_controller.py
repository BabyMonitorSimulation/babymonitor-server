from project import app, client_bm
from flask import request, jsonify
from project.service.bm_service import last_record, insert_data
from project.util.validations import validate_request
from project.util.generate_data import generate_data
from project.util.clean import clean_data
from project import db
import json
import requests
from pprint import pprint

"""
request to send:
{
    "type": 'status'/'notification',
    'msg': {
        'breathing': ,
        'time_no_breathing':,
        'sleeping': ,
        'crying': ,
        },
    'route': {
        'from': ,
        'to': ,
    }
}

request to receive:
{
    "type": "confirmation",
    "msg": {
        "info": "Notificaiton confirmed!"
    }
    "route": {
        "from": ,
        "to": ,
    }
}
"""


@app.route("/check", methods=["GET"])
def check():
    return "I'm working BabyMonitor"


@app.route("/bm_status", methods=["GET"])
def bm_status():
    return client_bm.internal_state


@app.route("/bm_send", methods=["GET"])
def bm_send():
    global internal_state
    generate_data("new")
    body = last_record()
    msg_type = "notification" if body["crying"] or body["time_no_breathing"] > 5 else "status"
    body['type'] = msg_type
    body['from'] = 'bm'
    body['to'] = 'smp'

    if body['type'] == 'notification':
        client_bm.internal_state = 'critical'

    client_bm.publish_to_dojot(body)  

    return jsonify(body), 200
