from flask import request
from flask.json import jsonify
from sqlalchemy import desc

from model.db import WeatherDataModel, db, RainDataModel, PoolTemperatureModel
from model.db import app

QUERY_LIMIT = 144
QUERY_LIMIT_RAIN = 24

db.create_all()


@app.route('/weather', methods=['GET', 'POST'])
def handle_temperature():
    if request.method == 'GET':
        weather_data = WeatherDataModel.query.order_by(desc(WeatherDataModel.timestamp)).limit(QUERY_LIMIT).all()
        temperatures = [{"temperature": str(data.temperature), "timestamp": str(data.timestamp)} for data in
                        weather_data]
        humidity = [{"humidity": str(data.humidity), "timestamp": str(data.timestamp)} for data in weather_data]
        rain_data = RainDataModel.query.order_by(RainDataModel.timestamp).limit(QUERY_LIMIT_RAIN).all()
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
        weather_data = PoolTemperatureModel.query.order_by(desc(PoolTemperatureModel.timestamp)).limit(QUERY_LIMIT).all()
        results = [
            {"timestamp": str(data.timestamp),
             "temperature": str(data.temperature)
             }
            for data in weather_data]
        results = sort_list_of_dicts_by_timestamp(results)
        return jsonify({"temperatures": results})
    elif request.method == 'POST':
        data = request.get_json()
        new_temperature = PoolTemperatureModel(data['temperature'], data['timestamp'])

        db.session.add(new_temperature)
        db.session.commit()
        return jsonify({"message": "new temperature added"})


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


def sort_list_of_dicts_by_timestamp(list_of_dicts):
    return sorted(list_of_dicts, key=lambda k: k['timestamp'])


if __name__ == '__main__':
    app.run(host='0.0.0.0')
