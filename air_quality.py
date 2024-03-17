# Air quality SDS011 sensor

from sds011 import SDS011
import time


def read_air_quality_sensor():
    sensor = SDS011("/dev/ttyUSB0", use_query_mode=True)
    sensor.sleep()
    sensor.sleep(sleep=False)
    time.sleep(20)
    query = sensor.query()
    sensor.sleep()
    return query[0], query[1]


# pm25_first_reading, pm10_first_reading = 0, 0
# pm25_second_reading, pm10_second_reading = 0, 0


# pm25_first_reading, pm10_first_reading = read_sensor()
# time.sleep(30)
# pm25_second_reading, pm10_second_reading = read_sensor()

# print(f'PM2.5 {pm25_first_reading} ug/m^3 | PM10 {pm10_first_reading} ug/m^3 \nPM2.5 {pm25_second_reading} ug/m^3 | PM10 {pm10_second_reading} ug/m^3')

