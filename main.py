import datetime
from datetime import time

from flask import jsonify
from sqlalchemy import desc

from app import db, TemperatureModel

if __name__ == '__main__':
    db.create_all()
    temp_model = TemperatureModel('20', datetime.datetime.now())

    db.session.add(temp_model)
    db.session.commit()

    temperatures = TemperatureModel.query.order_by(desc(TemperatureModel.timestamp)).limit(2).all()

