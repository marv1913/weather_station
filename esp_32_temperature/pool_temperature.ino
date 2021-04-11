/*********
  Rui Santos
  Complete project details at https://RandomNerdTutorials.com  
*********/

#include <OneWire.h>
#include <DallasTemperature.h>
#include <WiFi.h>
#include <time.h>
#include <HTTPClient.h>

#define uS_TO_S_FACTOR 1000000  /* Conversion factor for micro seconds to seconds */
#define TIME_TO_SLEEP  900        /* Time ESP32 will go to sleep (in seconds) */

const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = 3600;
const int   daylightOffset_sec = 3600;

// GPIO where the DS18B20 is connected to
const int oneWireBus = 4;     

// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(oneWireBus);

// Pass our oneWire reference to Dallas Temperature sensor 
DallasTemperature sensors(&oneWire);

//String printLocalTime()
//{
//  struct tm timeinfo;
//  if(!getLocalTime(&timeinfo)){
//    Serial.println("Failed to obtain time");
//    return "Failed";
//  }
//  Serial.println(&timeinfo, "%d-%m-%Y %H:%M:%S");
//  return &timeinfo, "%d-%m-%Y %H:%M:%S";
//}

void setup() {
  // Start the Serial Monitor
  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin("", "");
  Serial.println("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  // Start the DS18B20 sensor
  sensors.begin();

  //init and get the time
//  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);


}

void sendTemperatureToREST(String temperature){
  HTTPClient http;

  http.begin("http://192.168.178.123:5000/pool_temperature");

  String httpRequestData = String("{\"temperature\":\"") + temperature + String("\"}"); 

       
      // Send HTTP POST request
  int httpResponseCode = http.POST(httpRequestData);

  
}

void loop() {

  
  sensors.requestTemperatures(); 
  float temperatureC = sensors.getTempCByIndex(0);
  float temperatureF = sensors.getTempFByIndex(0);
  Serial.print(temperatureC);
  Serial.println("ºC");
  Serial.print(temperatureF);
  Serial.println("ºF");
  sendTemperatureToREST(String(temperatureC));
  
  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
  esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_PERIPH, ESP_PD_OPTION_OFF);
  
  Serial.println("Setup ESP32 to sleep for every " + String(TIME_TO_SLEEP) + " Seconds");

  Serial.println("Going to sleep now");
  delay(1000);
  Serial.flush(); 
  esp_deep_sleep_start();
}
