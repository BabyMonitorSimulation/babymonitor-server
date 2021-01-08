from project import db
from datetime import datetime


class BabyMonitorSend(db.Model):
    __tablename__ = "baby_monitor_send"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    crying = db.Column(db.Boolean, nullable=False)
    sleeping = db.Column(db.Boolean, nullable=False)
    breathing = db.Column(db.Boolean, nullable=False)
    time_no_breathing = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String, nullable=False)


class BabyMonitorReceive(db.Model):
    """ type: confirmation / ??? """

    __tablename__ = "baby_monitor_receive"
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    type = db.Column(db.String(80), nullable=True, default='confirmation')
    id_notification = db.Column(db.Integer, db.ForeignKey("baby_monitor_send.id"))
