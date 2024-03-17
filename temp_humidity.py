# AM2301B DHT22 Temperature and Humidity Sensor

import adafruit_dht
from gpio_pinout import AM2301_DATA_PIN
import time


def get_temp_and_humidity_readings():
    dht_device = adafruit_dht.DHT22(AM2301_DATA_PIN, use_pulseio=False)
    try:
        temp, humidity = 0, 0
        temp = dht_device.temperature
        humidity = dht_device.humidity
        return temp, humidity
    except Exception as error:
        print(error.args[0])
        return None
    finally:
        dht_device.exit()
