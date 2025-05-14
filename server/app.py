#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, abort
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Route to fetch earthquake by ID
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)  # Assuming Earthquake model is properly set up
    if earthquake is None:
        abort(404)  # If no earthquake with that ID exists
    return jsonify(earthquake.to_dict())  # Assuming you have a `to_dict()` method in your model

# Route to fetch earthquakes by magnitude
@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter_by(magnitude=magnitude).all()
    if not earthquakes:
        abort(404)  # If no earthquakes match the magnitude
    return jsonify([earthquake.to_dict() for earthquake in earthquakes])

# Handle 404 errors
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found'}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
