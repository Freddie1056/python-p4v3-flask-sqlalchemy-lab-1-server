from flask import Flask, make_response, jsonify, request, url_for, redirect, session
# from models import User, Artwork, Review, app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
import bcrypt
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model, SerializerMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_artist = db.Column(db.Boolean, default=False)
    artworks = db.relationship('Artwork', backref='artist', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    def __repr__(self) -> str:
        return f"{self.name}"

class Artwork(db.Model, SerializerMixin):
    __tablename__ = 'artwork'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reviews = db.relationship('Review', backref='artwork', lazy=True)
    
    def __repr__(self) -> str:
        return f"{self.title}"

class Review(db.Model, SerializerMixin):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'), nullable=False)
    
    def __repr__(self) -> str:
        return f"{self.content}"

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'

@app.route('/register', methods=['POST'])
def register():
    # Ensure the request is JSON
    if not request.is_json:
        return jsonify({'message': 'Content-Type must be application/json'}), 415  # Unsupported Media Type

    data = request.get_json()

    # Check for required fields
    required_fields = ['name', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400  # Bad request status

    # Check if user already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'User already exists'}), 409  # Conflict status

    # Hash the password for security
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    # Create new user
    new_user = User(
        name=data['name'],
        email=data['email'],
        password=hashed_password,
        is_artist=data.get('is_artist', False)
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/register', methods=['GET'])
def get_registration_info():
    return jsonify({
        'message': 'Send a POST request to register a user.',
        'example_request': {
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'securepassword',
            'is_artist': False
        }
    }), 200

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

# View to get users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    
    if users:
        response_body = f"{users}"
        return make_response(jsonify(response_body), 200)
    else:
        error_message = {
            "message": f"User {id} not found."
        }
        return make_response(jsonify(error_message), 404)

# View to get a user by id
@app.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = User.query.get(id)
    
    if user:
        response_body = {
            "id": user.id,
            "name": user.name,
            "magnitude": user.email,
            "year": user.is_artist,
        }
        return make_response(jsonify(response_body), 200)
    else:
        error_message = {
            "message": f"User {id} not found."
        }
        return make_response(jsonify(error_message), 404)

# View to get earthquakes by minimum magnitude
# @app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
# def get_earthquakes_by_magnitude(magnitude):
#     earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
#     response_body = {
#         "count": len(earthquakes),
#         "quakes": [
#             {
#                 "id": quake.id,
#                 "location": quake.location,
#                 "magnitude": quake.magnitude,
#                 "year": quake.year
#             } for quake in earthquakes
#         ]
#     }

#     return make_response(jsonify(response_body), 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
