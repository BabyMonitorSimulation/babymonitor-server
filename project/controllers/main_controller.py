from flask import request, jsonify
from project import app
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

# def send_baby_data_to_smartphone():
#     while True:
#         generate_data("new")
#         body = last_record()
#         body["type"] = (
#             "notification"
#             if body["crying"] or body["time_no_breathing"] > 5
#             else "status"
#         )
#         body["from"] = "bm"
#         body["to"] = "smp"

#         if body["type"] == "notification":
#             client_bm.internal_state = "critical"

#         requests.post("http://localhost:5001", json=body)
#         sleep(1)


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
    data['from'] = 'bm'
    data['to'] = 'smp'
    client_bm.publish_to_dojot(data)

    return jsonify(data), 200


@app.route("/get-confirmation", methods=["POST"])
def get_confirmation():
    print(request.json)
    last_data = BabyMonitorService(BabyMonitorSend).last_data()
    confirmation = {"id_notification": last_data["id"]}
    BabyMonitorService(BabyMonitorReceive).insert_data(confirmation)


# babymonitor:
# GET /start -> generate data from baby
# GET /confirmation -> generate good status

# smartphone:
# POST /receive-data -> receive the data from baby
# GET /confirmation -> send a confirmation to babymonitor

# tv:
# /change-status -> change the status of tv (lock or unlock)
# /receive-notification -> receive a notification from smartphone
