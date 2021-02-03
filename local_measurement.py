from w1thermsensor import W1ThermSensor

sensor = W1ThermSensor()


def get_current_temperature():
    return sensor.get_temperature()
