

# Weather Station

## REST endpoint
The REST server was devoloped by using the python library flask. The server provides two endpoints:

### weather data

 - supports http method GET
 - URI: ``/weather``
 - weather data containing rain, humidity and temperature data as JSON list

### water temperature data

 - supports http methods POST and GET
 - URI: ``/pool_temperature``
 - endpoint can be used to add new temperature values sending a POST request: e.g. ``{"temperature": "20.5"}
 - send a GET request to this endpoint to get all temperature data from the last 24 hours  


## Webpage
The website was developed using react. There are subpages for different types of diagrams. The library react-chart-js is used for visualizing the data from the REST server.

![screenshot of diagram for humidity data](https://github.com/marv1913/weather_station/blob/master/screenshots/humidity_data.png)

![screenshot of diagram for rain data](https://github.com/marv1913/weather_station/blob/master/screenshots/rain_data.png)

![screenshot of diagram for temperature data](https://github.com/marv1913/weather_station/blob/master/screenshots/temperature_data.png)
	
### Temperature measurement application for ESP-32
The program reads temperature data from a ds18b20 temperature sensor every 15 minutes and sends it to the water temperature endpoint of the REST server. After the temperature data were sent to the server the microcontroller goes into deep sleep mode to save energy.
