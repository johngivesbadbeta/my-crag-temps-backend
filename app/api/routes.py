from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Crag, crag_schema, crags_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'vin diesel': 'family'}

# Creating a Crag
@api.route('/crags', methods = ['POST'])
@token_required
def create_crag(current_user_token):
    crag_name = request.json['crag_name']
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    city = request.json['city']
    state = request.json['state']
    rock_type = request.json['rock_type']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    crag = Crag(crag_name, latitude, longitude, city, state, rock_type, user_token = user_token)

    db.session.add(crag)
    db.session.commit()

    response = crag_schema.dump(crag)
    return jsonify(response)

# Retrieving Crags
@api.route('/crags', methods = ['GET'])
@token_required
def get_crag(current_user_token):
    a_user = current_user_token.token
    crags = Crag.query.filter_by(user_token = a_user).all()
    response = crags_schema.dump(crags)
    return jsonify(response)

# Retrieving a single crag
@api.route('/crags/<id>', methods = ['GET'])
@token_required
def get_single_crag(current_user_token, id):
    crag = Crag.query.get(id)
    response = crag_schema.dump(crag)
    return jsonify(response)

# Updating a crag
@api.route('/crags/<id>', methods = ['POST', 'PUT'])
@token_required
def update_crag(current_user_token, id):
    crag = Crag.query.get(id)
    crag.crag_name = request.json['crag_name']
    crag.latitude = request.json['latitude']
    crag.longitude = request.json['longitude']
    crag.city = request.json['city']
    crag.state = request.json['state']
    crag.rock_type = request.json['rock_type']
    crag.user_token = current_user_token.token

    db.session.commit()
    response = crag_schema.dump(crag)
    return jsonify(response)

# Deleting a crag
@api.route('/crags/<id>', methods = ['DELETE'])
@token_required
def delete_crag(current_user_token, id):
    crag = Crag.query.get(id)
    db.session.delete(crag)
    db.session.commit()
    response = crag_schema.dump(crag)
    return jsonify(response)