from db_context import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Location(db.Model):
    __tablename__ = 'location'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), unique=True, nullable=False)
    measurements = db.relationship('Measurement', back_populates='location', lazy='dynamic')


    def __init__(self, name):
        self.name = name 
