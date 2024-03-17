from temp_humidity import get_temp_and_humidity_readings
from radiation_temp import find_ds18b20, read_radiation_temperature
from air_quality import read_air_quality_sensor
import time


def main():
    
    temp, humidity = None, None
    while temp == None or humidity == None:
        try:
            temp, humidity = get_temp_and_humidity_readings()
        except Exception as error:
            print(error.args[0])
            continue
    
    print (f'Temp is : {temp} C, Humidity is: {humidity} ')

    radiation_temp = None
    while radiation_temp == None:
        try:
            radiation_temp_sensor_name = find_ds18b20()
            radiation_temp = read_radiation_temperature(radiation_temp_sensor_name)
        except Exception as error: 
            print(error.args[0])
            continue
    
    print (f'Radiation temperature is : {radiation_temp} C')

    pm25, pm10 = None, None

    while pm25 == None or pm10 == None:
        try:
            pm25, pm10 = read_air_quality_sensor()
            # time.sleep(60)
        except Exception as error:
            print(error.args[0])
            continue

    print(f'PM2.5 {pm25} ug/m^3 | PM10 {pm10} ug/m^3')



if __name__ == "__main__":
    main()