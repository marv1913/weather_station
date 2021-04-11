import json
from datetime import datetime

from flask import request
from flask.json import jsonify
from sqlalchemy import desc

from model.db import WeatherDataModel, db, RainDataModel, PoolTemperatureModel, ParticulatesModel
from model.db import app

QUERY_LIMIT = 144
QUERY_LIMIT_RAIN = 24

db.create_all()


# TODO remove more than 2 decimal places of temperature values

@app.route('/weather', methods=['GET', 'POST'])
def handle_weather():
    if request.method == 'GET':
        weather_data = WeatherDataModel.query.order_by(desc(WeatherDataModel.timestamp)).limit(QUERY_LIMIT).all()
        temperatures = [{"temperature": str(data.temperature), "timestamp": str(data.timestamp)} for data in
                        weather_data]
        humidity = [{"humidity": str(data.humidity), "timestamp": str(data.timestamp)} for data in weather_data]
        rain_data = RainDataModel.query.order_by(desc(RainDataModel.timestamp)).limit(QUERY_LIMIT_RAIN).all()
        rainfall = [{'timestamp': str(data.timestamp), 'sum_1': str(data.rainfall), 'sum_24': str(data.rainfall_day)}
                    for data in rain_data]
        humidity = sort_list_of_dicts_by_timestamp(humidity)
        rainfall = sort_list_of_dicts_by_timestamp(rainfall)
        temperatures = sort_list_of_dicts_by_timestamp(temperatures)

        weather_data = {"temperatures": temperatures, "humidity": humidity, "rain": rainfall}
        return jsonify(weather_data)


@app.route('/pool_temperature', methods=['GET', 'POST'])
def handle_pool_temperature():
    if request.method == 'GET':
        weather_data = PoolTemperatureModel.query.order_by(desc(PoolTemperatureModel.timestamp)).limit(
            QUERY_LIMIT).all()
        results = [
            {"timestamp": str(data.timestamp),
             "temperature": str(data.temperature)
             }
            for data in weather_data]
        results = sort_list_of_dicts_by_timestamp(results)
        return jsonify({"temperatures": results})
    elif request.method == 'POST':
        data = json.loads(request.data)
        new_temperature = PoolTemperatureModel(data['temperature'], datetime.now().strftime("%Y-%m-%d %H:%M"))

        db.session.add(new_temperature)
        db.session.commit()
        return jsonify({"message": "new temperature added"})


@app.route('/particulates', methods=['GET'])
def handle_particulates_data():
    if request.method == 'GET':
        particulates_data = ParticulatesModel.query.order_by(desc(ParticulatesModel.timestamp)).limit(QUERY_LIMIT).all()
        results = [
            {"timestamp": str(data.timestamp),
             "pm_10": str(data.pm_10),
             "pm_25": str(data.pm_25)
             }
            for data in particulates_data]
        results = sort_list_of_dicts_by_timestamp(results)
        return jsonify(results)


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


def sort_list_of_dicts_by_timestamp(list_of_dicts):
    return sorted(list_of_dicts, key=lambda k: k['timestamp'])


if __name__ == '__main__':
    app.run(host='0.0.0.0')
