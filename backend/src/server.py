from flask import request
from flask.json import jsonify

from model.db import WeatherDataModel, db, RainDataModel, PoolTemperatureModel
from model.db import app

QUERY_LIMIT = 144
db.create_all()

@app.route('/weather', methods=['GET', 'POST'])
def handle_temperature():
    if request.method == 'GET':
        weather_data = WeatherDataModel.query.order_by(WeatherDataModel.timestamp).limit(QUERY_LIMIT).all()
        results = {'temperatures': [
            {str(data.timestamp):
                 {"temperature": str(data.temperature),
                  "humidity": str(data.humidity)
                  }
             } for data in weather_data]}
        rain_data = RainDataModel.query.order_by(RainDataModel.timestamp).limit(QUERY_LIMIT).all()
        rainfall = [{str(data.timestamp): {'sum_1': str(data.rainfall), 'sum_24': str(data.rainfall_day)}} for data in
                    rain_data]
        results['rain'] = rainfall
        return results
    elif request.method == 'POST':
        data = request.get_json()
        new_temperature = WeatherDataModel(data['temperature'], data['timestamp'])

        db.session.add(new_temperature)
        db.session.commit()
        return {"message": "new temperature added"}


@app.route('/pool_temperature', methods=['GET', 'POST'])
def handle_pool_temperature():
    if request.method == 'GET':
        weather_data = PoolTemperatureModel.query.order_by(PoolTemperatureModel.timestamp).limit(QUERY_LIMIT).all()
        results = [
            {"timestamp": str(data.timestamp),
             "temperature": str(data.temperature)
             }
            for data in weather_data]
        return jsonify(results)
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



if __name__ == '__main__':
    app.run(host='0.0.0.0')
