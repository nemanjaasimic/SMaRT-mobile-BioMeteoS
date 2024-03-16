# AM2301B DHT22 Temperature and Humidity Sensor

import adafruit_dht
from gpio_pinout import AM2301_DATA_PIN
import time


dht_device = adafruit_dht.DHT22(AM2301_DATA_PIN, use_pulseio=False)


while True:
    try:
        temp, humidity = 0, 0
        temp = dht_device.temperature
        humidity = dht_device.humidity

        print (f'Temp is : {temp} C, Humidity is: {humidity} ')
        time.sleep(3)
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2)
        continue
    except Exception as error:
        dht_device.exit()
        raise error
    
    time.sleep(5)