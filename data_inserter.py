import datetime
import logging
import time

from flask import Flask
from sqlalchemy.exc import IntegrityError

import local_measurement
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import variables

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{user}:{password}@{host}:{port}/weather_station". \
    format(user=variables.DB_USERNAME, password=variables.DB_PASSWORD, host=variables.DB_HOST, port=variables.DB_PORT)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class WeatherDataModel(db.Model):
    __tablename__ = 'weather_data'

    timestamp = db.Column(db.TIMESTAMP, primary_key=True)
    temperature = db.Column(db.DECIMAL)
    humidity = db.Column(db.DECIMAL)

    def __init__(self, temperature, humidity, timestamp):
        self.temperature = temperature
        self.timestamp = timestamp
        self.humidity = humidity

    # def __repr__(self):
    #     return f"<Car {self.name}>"


class RainDataModel(db.Model):
    __tablename__ = 'rain_data'

    timestamp = db.Column(db.TIMESTAMP, primary_key=True)
    rainfall = db.Column(db.DECIMAL)

    def __init__(self, rainfall, timestamp):
        self.rainfall = rainfall
        self.timestamp = timestamp


class DataInserter:

    def __init__(self, netatmo_api_obj):
        self.netatmo_api_obj = netatmo_api_obj
        connect_to_db()

    def start_inserting_data(self):
        while True:
            current_time = datetime.datetime.now()
            temperature = local_measurement.get_current_temperature()
            humidity = self.netatmo_api_obj.get_current_humidity()
            logging.info(f'{current_time}: inserting {temperature}°C {humidity}%')
            db.session.add(WeatherDataModel(temperature, humidity, current_time))
            db.session.commit()

            try:
                rainfall = self.netatmo_api_obj.get_rain()
                timestamp_rain = datetime.datetime.now().strftime('%Y-%m-%d %H') + ':00:00'
                db.session.add(RainDataModel(rainfall, timestamp_rain))
                db.session.commit()
                logging.info(f'{timestamp_rain}: inserting {rainfall}mm')
            except IntegrityError:
                pass

            time.sleep(600)  # insert data every 5 minutes


def connect_to_db():
    db.create_all()
