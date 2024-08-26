from model.measurement import db, Measurement
from scheduler import scheduler
from sensor.data_fetcher import fetch_values

from datetime import datetime
import random
import uuid

def generate_measurement(location_id):
    with scheduler.app.app_context():
        gps_datetime, gps_altitude, gps_altitude_units, gps_longitude, gps_latitude, temp, humidity, globe_temp, wind_speed_m_s, limited_wind_speed_m_s, pm25, pm10, uv_intensity = fetch_values()
        print("measuring obtained ")
        measurement = Measurement(
            date=gps_datetime.date(),
            time=gps_datetime.time().strftime('%H:%M:%S'),
            altitude=gps_altitude,
            longitude=gps_longitude,
            latitude=gps_latitude,
            temperature=temp,
            relative_humidity=humidity,
            globe_temperature=globe_temp,
            wind_speed=wind_speed_m_s,
            limited_wind_speed=limited_wind_speed_m_s,
            pm_2_5=pm25,
            pm_10=pm10,
            uv_b=uv_intensity,
            location_id=location_id
        )

        print(measurement)

        db.session.add(measurement)
        db.session.commit()
        return measurement