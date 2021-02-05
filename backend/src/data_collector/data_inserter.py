import datetime
import logging
import time


from sqlalchemy.exc import IntegrityError, OperationalError

from model.db import WeatherDataModel, db, RainDataModel


class DataInserter:

    def __init__(self, netatmo_api_obj):
        self.netatmo_api_obj = netatmo_api_obj
        connect_to_db()

    def start_inserting_data(self):
        from data_collector import local_measurement
        while True:
            try:
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                temperature = local_measurement.get_current_temperature()
                humidity = self.netatmo_api_obj.get_current_humidity()
                logging.info(f'{current_time}: inserting {temperature}°C {humidity}%')
                db.session.add(WeatherDataModel(temperature, humidity, current_time))
                db.session.commit()

                try:
                    rainfall = self.netatmo_api_obj.get_rain_last_hour()
                    rainfall_day = self.netatmo_api_obj.get_rain_last_day()

                    timestamp_rain = datetime.datetime.now().strftime('%Y-%m-%d %H') + ':00:00'
                    db.session.add(RainDataModel(rainfall, rainfall_day, timestamp_rain))
                    db.session.commit()
                    logging.info(
                        f'{timestamp_rain}: inserting {rainfall}mm for last hour and {rainfall_day}mm for last 24 hours')
                except IntegrityError:
                    db.session.rollback()

                time.sleep(600)  # insert data every 5 minutes
            except OperationalError:
                logging.debug('connection to server closed')
                time.sleep(30)


def connect_to_db():
    db.create_all()
