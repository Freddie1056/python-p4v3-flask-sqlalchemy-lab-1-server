from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

# Add models here
class Earthquake(db.Model, SerializerMixin):
    __tablename__ = 'earthquakes'  # Table name

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    magnitude = db.Column(db.Float)  # Magnitude of the earthquake
    location = db.Column(db.String)  # Location of the earthquake
    year = db.Column(db.Integer)  # Year of the earthquake

    def __repr__(self):
        return f"<Earthquake {self.id}, {self.magnitude}, {self.location}, {self.year}>"
