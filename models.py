# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask
# from sqlalchemy_serializer import SerializerMixin
# import os

# basedir = os.path.abspath(os.path.dirname(__file__))

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] =\
#         'sqlite:///' + os.path.join(basedir, 'database.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# class User(db.Model, SerializerMixin):
#     __tablename__ = 'user'
    
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(128), nullable=False)
#     is_artist = db.Column(db.Boolean, default=False)
#     artworks = db.relationship('Artwork', backref='artist', lazy=True)
#     reviews = db.relationship('Review', backref='user', lazy=True)

#     def __repr__(self) -> str:
#         return f"{self.name}"

# class Artwork(db.Model, SerializerMixin):
#     __tablename__ = 'artwork'

#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     artist_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     reviews = db.relationship('Review', backref='artwork', lazy=True)
    
#     def __repr__(self) -> str:
#         return f"{self.title}"

# class Review(db.Model, SerializerMixin):
#     __tablename__ = 'review'

#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.Text, nullable=False)
#     rating = db.Column(db.Integer, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'), nullable=False)
    
#     def __repr__(self) -> str:
#         return f"{self.content}"



# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import MetaData
# from sqlalchemy_serializer import SerializerMixin

# metadata = MetaData()

# db = SQLAlchemy(metadata=metadata)

# # Add models here
# class Earthquake(db.Model, SerializerMixin):
#     __tablename__ = 'earthquakes'  # Table name

#     id = db.Column(db.Integer, primary_key=True)  # Primary key
#     magnitude = db.Column(db.Float)  # Magnitude of the earthquake
#     location = db.Column(db.String)  # Location of the earthquake
#     year = db.Column(db.Integer)  # Year of the earthquake

#     def __repr__(self):
#         return f"<Earthquake {self.id}, {self.magnitude}, {self.location}, {self.year}>"
