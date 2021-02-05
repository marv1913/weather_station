from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from src import variables

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
    rainfall_day = db.Column(db.DECIMAL)

    def __init__(self, rainfall, rainfall_day, timestamp):
        self.rainfall = rainfall
        self.rainfall_day = rainfall_day
        self.timestamp = timestamp
