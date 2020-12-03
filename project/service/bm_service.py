from project import db
from project.model.db_model import BabyMonitor
from project.util.clean import clean_data
from datetime import datetime


def delete_all_rows():
    database.query.delete()


def insert_data(data):
    babymonitor = BabyMonitor(**data)
    db.session.add(babymonitor)
    db.session.commit()
    return babymonitor


def update_data(data):
    last_record = db.query.order_by(db.database.id.desc()).first()
    if data["crying"]:
        crying = {"crying": data["crying"]}
        BabyMonitor.query.filter_by(id=last_record.id).update(crying)
    if not data["breathing"]:
        time_no_breathing = {"time_no_breathing": data["time_no_breathing"]}
        BabyMonitor.query.filter_by(id=last_record.id).update(time_no_breathing)
    db.session.commit()


def last_record():
    return clean_data(BabyMonitor.query.all()[-1].__dict__)


def get_by_id(id):
    return BabyMonitor.query.filter_by(id=id).first()


"""class BabyMonitorService:
    def __init__(, database):
        .database = database

    def delete_all_rows():
        .database.query.delete()

    def insert_data(self, data):
        data_babymonitor = self.database(**data, time=datetime.utcnow())
        db.session.add(data_babymonitor)
        db.session.commit()

    def update_data(self, data):
        last_record = self.database().query.order_by(self.database.id.desc()).first()
        if data["crying"]:
            crying = {"crying": data["crying"]}
            BabyMonitor.query.filter_by(id=last_record.id).update(crying)
        if not data["breathing"]:
            time_no_breathing = {"time_no_breathing": data["time_no_breathing"]}
            BabyMonitor.query.filter_by(id=last_record.id).update(time_no_breathing)
        db.session.commit()

    def last_record(self):
        import ipdb; ipdb.set_trace()
        data = self.database().query.order_by(self.database.id.desc()).first()
        if not data:
            return data

        return data.__dict__

    def get_by_id(self, id):
        return BabyMonitor.query.filter_by(id=id).first()
"""
