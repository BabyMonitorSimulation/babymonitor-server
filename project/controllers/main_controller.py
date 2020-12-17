from pprint import pprint
from flask import request, jsonify
from project import app
from project.util.clean import clean_data
from project.util.generate_data import generate_data
from project.service.bm_service import last_record, insert_data
from project.communication.client_bm import ClientBM
import json
import requests

client_bm = ClientBM()
client_bm.subscribe()


@app.route("/check", methods=["GET"])
def check():
    return "I'm working BabyMonitor"


@app.route("/bm_status", methods=["GET"])
def bm_status():
    return client_bm.internal_state


@app.route("/bm_send", methods=["GET"])
def bm_send():
    generate_data("new")
    body = last_record()
    msg_type = (
        "notification" if body["crying"] or body["time_no_breathing"] > 5 else "status"
    )
    body["type"] = msg_type
    body["from"] = "bm"
    body["to"] = "smp"

    if body["type"] == "notification":
        client_bm.internal_state = "critical"

    client_bm.publish_to_dojot(body)

    return jsonify(body), 200
