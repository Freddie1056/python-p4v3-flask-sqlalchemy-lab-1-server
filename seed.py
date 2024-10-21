# server/seed.py
# artworks="", reviews=""

from app import app
from models import db, User

with app.app_context():

    # Delete all rows in the "users" table
    db.create_all()
    User.query.delete()

    # Add several User instances to the "users" table
    db.session.add(User(name="John", email="", password="", is_artist="true"))

    # Commit the transaction
    db.session.commit()
