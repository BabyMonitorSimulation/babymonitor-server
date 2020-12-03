from project import app
from flask import request, jsonify
from project.service.bm_service import last_record, insert_data
from project.util.validations import validate_request
from project.util.generate_data import generate_data
from project.util.clean import clean_data
from project import db
import json
import requests
from pprint import pprint

internal_state = "normal"

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
    global internal_state
    return internal_state


@app.route("/bm_send", methods=["GET"])
def bm_send():
    global internal_state
    generate_data("new")
    data = last_record()
    msg_type = "notification" if data["crying"] or data["time_no_breathing"] > 5 else "status"
    body = {
        "type": msg_type,
        "msg": data,
        "route": {"from": "bm", "to": "smp"},
    }

    if body['type'] == 'notification':
        internal_state = 'critical'


    # Send request to smp
    requests.post("http://localhost:5003/bm_receive", json=body)

    return jsonify(body), 200


@app.route("/bm_receive", methods=["POST"])
def bm_receive():
    global internal_state
    validate, msg = validate_request(request)

    if not validate:
        return jsonify({"msg": msg}), 400

    internal_state = "normal"
    pprint(request.json)
    return "OK", 200
