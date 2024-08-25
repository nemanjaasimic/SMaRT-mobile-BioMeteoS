from db_context import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Measurement(db.Model):
    __tablename__ = 'measurement'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = db.Column(db.Date, nullable=False)    
    time = db.Column(db.Time, nullable=False)    
    altitude = db.Column(db.Float(precision=2), default=100.0, nullable=False)
    longitute = db.Column(db.String(), default="00° 00' 00.00\"", nullable=False)
    latitude = db.Column(db.String(), default="00° 00' 00.00\"", nullable=False)
    temperature = db.Column(db.Float(precision=2), default=0.0, nullable=False)
    relative_humidity = db.Column(db.Float(precision=2), default=0.0, nullable=False)
    globe_temperature = db.Column(db.Float(precision=2), default=0.0, nullable=False)
    wind_speed = db.Column(db.Float(precision=2), default=0.0, nullable=False)
    limited_wind_speed = db.Column(db.Float(precision=2), default=0.0, nullable=False)
    pm_2_5 = db.Column(db.Float(precision=2), default=0.0, nullable=False)
    pm_10 = db.Column(db.Float(precision=2), default=0.0, nullable=False)
    uv_b = db.Column(db.Float(precision=2), default=0.0, nullable=False)

    location_id = db.Column(UUID(as_uuid=True), db.ForeignKey('location.id'), unique=False, nullable=False)
    location = db.relationship("Location", back_populates="measurements")

    def __init__(self, date, time, altitude, longitude, latitude, temperature, relative_humidity, globe_temperature, wind_speed, limited_wind_speed, pm_2_5, pm_10, uv_b, location_id):
        self.date = date        
        self.time = time        
        self.altitude = altitude
        self.longidute = longitude
        self.latitude = latitude
        self.temperature = temperature
        self.relative_humidity = relative_humidity
        self.globe_temperature = globe_temperature
        self.wind_speed = wind_speed
        self.limited_wind_speed = limited_wind_speed
        self.pm_2_5 = pm_2_5
        self.pm_10 = pm_10
        self.uv_b = uv_b
        self.location_id = location_id
    