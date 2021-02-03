from flask import request, Flask
from sqlalchemy import desc

from data_inserter import WeatherDataModel, db




@app.route('/weather', methods=['GET', 'POST'])
def handle_temperature():
    if request.method == 'GET':
        weather_data = WeatherDataModel.query.order_by(desc(WeatherDataModel.timestamp)).limit(2).all()
        results = [
            {data.timestamp:
                 {"temperature": str(data.temperature),
                  "humidity": str(data.humidity)
                  }
             } for data in weather_data]
        return {'temperatures': results}
    elif request.method == 'POST':
        data = request.get_json()
        new_temperature = WeatherDataModel(data['temperature'], data['timestamp'])

        db.session.add(new_temperature)
        db.session.commit()
        return {"message": "new temperature added"}


if __name__ == '__main__':
    app.run()