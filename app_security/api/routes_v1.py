import json

from flask import Flask, jsonify, request, Response
from app_security.domain.user.User import create_user, get_user, get_all_users, update_user, delete_user
from app_security.domain.user.model.UserModel import User
from app_security.infrastructure.database.sqlite import db
from app_security.api.auth import encode_auth_token, token_required

def register_routes(app):
    
    @app.route('api/v1/login', methods=['POST'])
    def login():
        data = request.get_json()
        email = data['email']
        user = User.query.filter_by(email=email).first()

        if user:
            token = encode_auth_token(user.id)
            return jsonify({'token': token})
        return jsonify({'error': 'User not found'}), 404
    
    @app.route('api/v1/users', methods=['POST'])
    @token_required
    def create():
        data = request.get_json()
        name, email = data['name'], data['email']
        user = create_user(name, email)
        return jsonify({'user': user.to_dict()}), 201

    @app.route('api/v1/users', methods=['GET'])
    @token_required
    def get_all(current_user_id):
        users = get_all_users()
        #return jsonify({'users': [user.to_dict() for user in users]})
        users_dict = {'users': [user.to_dict() for user in users]}
        response = Response(json.dumps(users_dict, sort_keys=False), mimetype='application/json')
        return response

    @app.route('api/v1/users/<int:user_id>', methods=['GET'])
    @token_required
    def get_one(user_id):
        user = get_user(user_id)
        if user:
            return jsonify({'user': user.to_dict()})
        return jsonify({'error': 'User not found'}), 404

    @app.route('api/v1/users/<int:user_id>', methods=['PUT'])
    @token_required
    def update(user_id):
        data = request.get_json()
        name, email = data.get('name'), data.get('email')
        user = update_user(user_id, name, email)
        if user:
            return jsonify({'user': user.to_dict()})
        return jsonify({'error': 'User not found'}), 404

    @app.route('api/v1/users/<int:user_id>', methods=['DELETE'])
    @token_required
    def delete(user_id):
        user = delete_user(user_id)
        if user:
            return jsonify({'result': 'User deleted'})
        return jsonify({'error': 'User not found'}), 404