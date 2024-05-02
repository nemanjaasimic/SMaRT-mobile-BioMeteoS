from temp_humidity import get_temp_and_humidity_readings
from globe_temp import find_ds18b20, read_globe_temperature
from air_quality import read_air_quality_sensor
from gps import get_gps_data
from analog_sensors import get_wind_speed, get_uv_intensity


def main():
    
    print('Starting the measurements. Please wait...')

    gps_latitude, gps_longitude, gps_altitude, gps_altitude_units, gps_datetime = None, None, None, None, None
    while gps_latitude == None or gps_longitude == None or gps_altitude == None or gps_datetime == None:
        try:
            gps_latitude, gps_longitude, gps_altitude, gps_altitude_units, gps_datetime = get_gps_data()
        except Exception as error:
            print(f'Failed to retrieve GPS data. Message: {error.args[0]}. Trying again!')
            continue


    temp, humidity = None, None
    while temp == None or humidity == None:
        try:
            temp, humidity = get_temp_and_humidity_readings()
        except Exception as error:
            print(f'Failed to retrieve Temperature and Humidity data. Message: {error.args[0]}. Trying again!')
            continue


    wind_speed_m_s = None
    while wind_speed_m_s == None:
        try:
            wind_speed_m_s = get_wind_speed()
        except Exception as error:
            print(f'Failed to retrieve Wind Speed data. Message: {error.args[0]}. Trying again!')
            continue


    uv_intensity = None
    while uv_intensity == None:
        try:
            uv_intensity = get_uv_intensity()
        except Exception as error:
            print(f'Failed to retrieve UV Intensity data. Message: {error.args[0]}. Trying again!')
            continue


    globe_temp = None
    while globe_temp == None:
        try:
            globe_temp_sensor_name = find_ds18b20()
            globe_temp = read_globe_temperature(globe_temp_sensor_name)
        except Exception as error: 
            print(f'Failed to retrieve Globe temp data. Message: {error.args[0]}. Trying again!')
            continue


    pm25, pm10 = None, None
    while pm25 == None or pm10 == None:
        try:
            pm25, pm10 = read_air_quality_sensor()
            # time.sleep(60)
        except Exception as error:
            print(f'Failed to retrieve Air Quality PM data. Message: {error.args[0]}. Trying again!')
            continue

    print("Measurements completed.\nPlease take a look at the results below: \n")

    print (f'Reading started at: {gps_latitude}, {gps_longitude}, {gps_altitude}{gps_altitude_units}, {gps_datetime}')
    print (f'Temp is : {temp} C, Humidity is: {humidity} %RH')
    print (f'Wind speed is : {wind_speed_m_s} m/s')
    print (f'UV Intensity is : {uv_intensity} mW/cm^2')
    print (f'Globe temperature is : {globe_temp} C')
    print(f'PM2.5 {pm25} ug/m^3 | PM10 {pm10} ug/m^3')



if __name__ == "__main__":
    main()