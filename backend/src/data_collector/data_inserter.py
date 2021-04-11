import datetime
import logging
import time

import requests
from serial import SerialException
from sqlalchemy.exc import IntegrityError, OperationalError
from sds011 import SDS011


from model.db import WeatherDataModel, db, RainDataModel, ParticulatesModel


class DataInserter:

    def __init__(self, netatmo_api_obj):
        self.netatmo_api_obj = netatmo_api_obj

    def start_inserting_data(self):
        while True:
            if connect_to_db():
                try:
                    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                    humidity = self.netatmo_api_obj.get_current_humidity()
                    temperature = self.netatmo_api_obj.get_current_temperature()
                    logging.info(f'{current_time}: inserting {temperature}°C {humidity}%')
                    db.session.add(WeatherDataModel(temperature, humidity, current_time))
                    db.session.commit()
                    try:
                        particulates_data = get_particulates()
                        if particulates_data is None:
                            logging.debug('skip inserting particulates data, because got invalid data from sensor')
                        else:
                            db.session.add(ParticulatesModel(particulates_data[0], particulates_data[1], current_time))
                            db.session.commit()
                            logging.info(f'{current_time}: inserting pm25: {particulates_data[0]} and pm10: '
                                         f'{particulates_data[1]}')
                    except (SerialException, TypeError):
                        logging.debug("skip inserting particulates data, because sensor is not connected")

                    rainfall = self.netatmo_api_obj.get_rain_last_hour()
                    rainfall_day = self.netatmo_api_obj.get_rain_last_day()

                    timestamp_rain = datetime.datetime.now().strftime('%Y-%m-%d %H') + ':00:00'
                    db.session.add(RainDataModel(rainfall, rainfall_day, timestamp_rain))
                    db.session.commit()
                    logging.info(
                        f'{timestamp_rain}: inserting {rainfall}mm for last hour and {rainfall_day}mm for last 24 '
                        f'hours')
                except (IntegrityError, ConnectionError) as e:
                    logging.debug(e)
                    db.session.rollback()

                except OperationalError:
                    logging.debug('connection to server closed')
                    time.sleep(30)
                except requests.exceptions.RequestException:
                    logging.debug('no internet connection')
                    time.sleep(30)
            close_connection()
            logging.debug("sleep for 10 minutes")
            time.sleep(600)  # insert data every 10 minutes


def connect_to_db():
    logging.debug('open db connection')
    try:
        db.create_all()
        return True
    except OperationalError:
        logging.debug("could not connect to database")
    return False


def close_connection():
    logging.debug('close db connection')
    db.session.close()


def get_particulates():
    sensor = SDS011("/dev/ttyUSB0", use_query_mode=True)
    try:
        sensor = SDS011("/dev/ttyUSB0", use_query_mode=True)
        sensor.sleep(sleep=False)
        time.sleep(20)
        values = sensor.query()
        sensor.sleep()
        return values
    except IndexError:
        sensor.sleep()
        return None


if __name__ == '__main__':
    particulates = get_particulates()
