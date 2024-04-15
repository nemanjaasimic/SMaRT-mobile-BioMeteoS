from temp_humidity import get_temp_and_humidity_readings
from globe_temp import find_ds18b20, read_globe_temperature
from air_quality import read_air_quality_sensor
from gps import get_gps_data
from analog_sensors import get_wind_speed


def main():
    
    gps_latitude, gps_longitude, gps_altitude, gps_altitude_units, gps_datetime = None, None, None, None, None
    while gps_latitude == None or gps_longitude == None or gps_altitude == None or gps_datetime == None:
        try:
            gps_latitude, gps_longitude, gps_altitude, gps_altitude_units, gps_datetime = get_gps_data()
        except Exception as error:
            print(error.args[0])
            continue
    
    print (f'Reading started at: {gps_latitude}, {gps_longitude}, {gps_altitude}{gps_altitude_units}, {gps_datetime}')

    temp, humidity = None, None
    while temp == None or humidity == None:
        try:
            temp, humidity = get_temp_and_humidity_readings()
        except Exception as error:
            print(error.args[0])
            continue
    
    print (f'Temp is : {temp} C, Humidity is: {humidity} ')

    wind_speed_m_s = None
    while wind_speed_m_s == None:
        try:
            wind_speed_m_s = get_wind_speed()
        except Exception as error:
            print(error.args[0])
            continue
    
    print (f'Wind speed is : {wind_speed_m_s} m/s')

    globe_temp = None
    while globe_temp == None:
        try:
            globe_temp_sensor_name = find_ds18b20()
            globe_temp = read_globe_temperature(globe_temp_sensor_name)
        except Exception as error: 
            print(error.args[0])
            continue
    
    print (f'Globe temperature is : {globe_temp} C')

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