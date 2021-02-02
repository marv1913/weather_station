from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import desc

import variables

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{user}:{password}@{host}:{port}/weather_station".\
    format(user=variables.DB_USERNAME, password=variables.DB_PASSWORD, host=variables.DB_HOST, port=variables.DB_PORT)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class TemperatureModel(db.Model):
    __tablename__ = 'temperatures'

    timestamp = db.Column(db.TIMESTAMP, primary_key=True)
    temperature = db.Column(db.DECIMAL)

    def __init__(self, temperature, timestamp):
        self.temperature = temperature
        self.timestamp = timestamp

    # def __repr__(self):
    #     return f"<Car {self.name}>"


@app.route('/temperatures', methods=['GET', 'POST'])
def handle_temperature():
    if request.method == 'GET':
        temperatures = TemperatureModel.query.order_by(desc(TemperatureModel.timestamp)).limit(2).all()
        results = [
            {
                "temperature": str(temperature.temperature),
                "timestamp": temperature.timestamp,
            } for temperature in temperatures]
        return {'temperatures': results}
    elif request.method == 'POST':
        data = request.get_json()
        new_temperature = TemperatureModel(data['temperature'], data['timestamp'])

        db.session.add(new_temperature)
        db.session.commit()
        return {"message": "new temperature added"}



if __name__ == '__main__':
    app.run()