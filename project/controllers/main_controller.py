from flask import request, jsonify
from project import app, socketio
from project.util.clean import clean_data
from project.util.generate_data import generate_data
from project.model.db_model import BabyMonitorSend, BabyMonitorReceive
from project.service.bm_service import BabyMonitorService
from project.communication.client_bm import ClientBM
from threading import Thread
from time import sleep
import requests
import json


client_bm = ClientBM()

@app.route("/", methods=["GET"])
def check():
    return "I'm working BabyMonitor"


@app.route("/bm_send", methods=["GET"])
def bm_send():
    global client_bm
    data_send = BabyMonitorService(BabyMonitorSend).last_record()
    data_receive = BabyMonitorService(BabyMonitorReceive).last_record()

    if not data_send:
        data = generate_data("new")

    elif data_send["type"] == "notification" and not data_receive:
        data = generate_data("repeat")

    elif (
        data_send["type"] == "notification"
        and data_receive["id_notification"] != data_send["id"]
    ):
        data = generate_data("repeat")
    elif (
        data_send["type"] == "notification"
        and data_receive["id_notification"] == data_send["id"]
    ):
        data = generate_data("fine")

    else:
        data = generate_data("new")
    data["type"] = (
        "notification" if data["crying"] or data["time_no_breathing"] > 5 else "status"
    )

    BabyMonitorService(BabyMonitorSend).insert_data(data)
    data["from"] = "bm"
    data["to"] = "smp"
    client_bm.publish_to_dojot(data)
    print(f"send {data}")
    socketio.emit("BabyMonitorSent", data)

    return jsonify(data), 200


@app.route("/get-confirmation", methods=["POST"])
def get_confirmation():
    print(request.json)
    print(f"receive {request.json}")
    socketio.emit("BabyMonitorReceive", request.json)
    last_data = BabyMonitorService(BabyMonitorSend).last_record()
    confirmation = {"id_notification": last_data["id"]}
    BabyMonitorService(BabyMonitorReceive).insert_data(confirmation)

    return "OK"

