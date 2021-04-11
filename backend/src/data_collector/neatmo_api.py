import json
import urllib
from json.decoder import JSONDecodeError

import requests

import variables


class NetatmoApi:

    def __init__(self, mac_address, outside_temperature_module_mac, rain_module_mac, username, password, client_id,
                 client_secret):
        self.mac_address = mac_address
        self.outside_temperature_module_mac_address = outside_temperature_module_mac
        self.rain_module_mac = rain_module_mac
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret

    def get_weather_station_data(self):
        try:
            r = requests.get(
                f'https://api.netatmo.com/api/getstationsdata?{urllib.parse.urlencode({"device_id": self.mac_address})}'
                f'&get_favorites=false', headers={'Authorization': f'Bearer {self.get_authorization()}'})
            return json.loads(r.text)
        except JSONDecodeError:
            return {}

    def get_authorization(self):
        r = requests.post(f'https://api.netatmo.com/oauth2/token',
                          data={'grant_type': 'password', 'username': self.username, 'password': self.password,
                                'client_id': self.client_id, 'client_secret': self.client_secret})
        return json.loads(r.text)['access_token']

    def get_current_humidity(self):
        data_as_dict = self.get_weather_station_data()
        try:
            for module in data_as_dict['body']['devices'][0]['modules']:
                if module['_id'] == self.outside_temperature_module_mac_address:
                    return module['dashboard_data']['Humidity']
        except KeyError:
            return 0

    def get_current_temperature(self):
        data_as_dict = self.get_weather_station_data()
        try:
            for module in data_as_dict['body']['devices'][0]['modules']:
                if module['_id'] == self.outside_temperature_module_mac_address:
                    return module['dashboard_data']['Temperature']
        except KeyError:
            return 0

    def get_rain_last_day(self):
        data_as_dict = self.get_weather_station_data()
        for module in data_as_dict['body']['devices'][0]['modules']:
            if module['_id'] == self.rain_module_mac:
                try:
                    return module['dashboard_data']['sum_rain_24']
                except KeyError:
                    return 0

    def get_rain_last_hour(self):
        try:
            data_as_dict = self.get_weather_station_data()
            for module in data_as_dict['body']['devices'][0]['modules']:
                if module['_id'] == self.rain_module_mac:
                    return module['dashboard_data']['sum_rain_1']
        except KeyError:
            return 0


if __name__ == '__main__':
    netatmo_api = NetatmoApi(variables.WEATHER_STATION_MAC, variables.OUTSIDE_MODULE_MAC, variables.RAIN_MODULE_MAC,
                             variables.NETATMO_USERNAME, variables.NETATMO_PASSWORD, variables.NETATMO_CLIENT_ID,
                             variables.NETATMO_CLIENT_SECRET)
    print(netatmo_api.get_current_temperature())

