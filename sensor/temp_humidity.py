# AM2301B DHT22 Temperature and Humidity Sensor

import adafruit_dht
from sensor.gpio_pinout import AM2301_DATA_PIN
import time


def get_temp_and_humidity_readings():
    try:
        dht_device = adafruit_dht.DHT22(AM2301_DATA_PIN, use_pulseio=False)
        temp, humidity = 0, 0
        get_measures(dht_device)
        temp = dht_device.temperature
        humidity = dht_device.humidity
        dht_device.exit()
        return temp, humidity
    except Exception as error:
        raise error


def get_measures(dht_device):
    while dht_device.temperature == None or dht_device.humidity == None:
        try:
            dht_device.measure()
        except Exception as error:
            print("DHT Device not ready yet")
            continue