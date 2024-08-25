from flask import current_app
from model.measurement import db, Measurement

from datetime import datetime
import random
import uuid

def generate_measurement(location_id):
    with current_app.app_context():
        # gps_datetime, gps_altitude, gps_altitude_units, gps_longitude, gps_latitude, temp, humidity, globe_temp, wind_speed_m_s, limited_wind_speed_m_s, pm25, pm10, uv_intensity = data_fetcher.fetch_values()
        
        # measurement = Measurement(
        #     id=uuid.uuid4(),
        #     date=gps_datetime.date(),
        #     time=gps_datetime.time().strftime('%H:%M:%S'),
        #     altitude=gps_altitude,
        #     longitude=gps_longitude,
        #     latitude=gps_latitude,
        #     temperature=temp,
        #     relative_humidity=humidity,
        #     globe_temperature=globe_temp,
        #     wind_speed=wind_speed_m_s,
        #     limited_wind_speed=limited_wind_speed_m_s,
        #     pm_2_5=pm25,
        #     pm_10=pm10,
        #     uv_b=uv_intensity,
        #     location_id=location_id
        # )
        measurement = Measurement(
            date=datetime.now().date(),
            time=datetime.now().time(),
            altitude=random.uniform(100.0, 2000.0),
            longitude="00° 00' 00.00\"",
            latitude="00° 00' 00.00\"",
            temperature=random.uniform(-10.0, 35.0),
            relative_humidity=random.uniform(0.0, 100.0),
            globe_temperature=random.uniform(-10.0, 35.0),
            wind_speed=random.uniform(0.0, 30.0),
            limited_wind_speed=random.uniform(0.0, 30.0),
            pm_2_5=random.uniform(0.0, 500.0),
            pm_10=random.uniform(0.0, 500.0),
            uv_b=random.uniform(0.0, 10.0),
            location_id=location_id
        )
        db.session.add(measurement)
        db.session.commit()
        return measurement