import logging

import variables
import  data_collector.data_inserter
from data_collector.neatmo_api import NetatmoApi

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    netatmo_api = NetatmoApi(variables.WEATHER_STATION_MAC, variables.OUTSIDE_MODULE_MAC, variables.RAIN_MODULE_MAC,
                             variables.NETATMO_USERNAME, variables.NETATMO_PASSWORD, variables.NETATMO_CLIENT_ID,
                             variables.NETATMO_CLIENT_SECRET)
    data_inserter = data_collector.data_inserter.DataInserter(netatmo_api)

    data_inserter.start_inserting_data()




