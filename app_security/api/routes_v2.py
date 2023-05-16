import json

from flask import Flask, jsonify, request, Response
from wtforms import Form, StringField, IntegerField, validators
from werkzeug.datastructures import ImmutableMultiDict
from email_validator import validate_email, EmailNotValidError

from app_security.domain.user.User import create_user, get_user, get_all_users, update_user, delete_user
from app_security.domain.user.model.UserModel import User
from app_security.infrastructure.database.sqlite import db
from app_security.api.auth import encode_auth_token, token_required


class ClienteForm(Form):
    id = IntegerField('ID')
    name = StringField('Name', validators=[validators.InputRequired()])
    email = StringField('Email', validators=[validators.InputRequired(), validators.Email()])



def register_routes(app):
    
    @app.route('/api/v2/login', methods=['POST'])
    def login2(current_user_id):
        data = request.get_json()
        email = data['email']
        user = User.query.filter_by(email=email).first()

        if user:
            token = encode_auth_token(user.id)
            return jsonify({'token': token})
        return jsonify({'error': 'User not found'}), 404
    
    @app.route('/api/v2/users', methods=['POST'])
    @token_required
    def create2(current_user_id):
        data = request.get_json()
        
        form_data = ImmutableMultiDict(data)
        form = ClienteForm(form_data)
        
        if form.validate():
            name, email = data['name'], data['email']
            user = create_user(name, email)
            return jsonify({'user': user.to_dict()}), 201
        else:
            errors = {}
            for field, field_errors in form.errors.items():
                errors[field] = field_errors[0]  # Apenas exibe a primeira mensagem de erro por campo
            return jsonify({'error': "Form validation failed",
                            "errors": errors}), 404

    @app.route('/api/v2/users', methods=['GET'])
    @token_required
    def get_all2(current_user_id):
        users = get_all_users()
        #return jsonify({'users': [user.to_dict() for user in users]})
        users_dict = {'users': [user.to_dict() for user in users]}
        response = Response(json.dumps(users_dict, sort_keys=False), mimetype='application/json')
        return response

    @app.route('/api/v2/users/<int:user_id>', methods=['GET'])
    @token_required
    def get_one2(user_id):
        user = get_user(user_id)
        if user:
            return jsonify({'user': user.to_dict()})
        return jsonify({'error': 'User not found'}), 404

    @app.route('/api/v2/users/<int:user_id>', methods=['PUT'])
    @token_required
    def update2(user_id):
        data = request.get_json()
        name, email = data.get('name'), data.get('email')
        user = update_user(user_id, name, email)
        if user:
            return jsonify({'user': user.to_dict()})
        return jsonify({'error': 'User not found'}), 404

    @app.route('/api/v2/users/<int:user_id>', methods=['DELETE'])
    @token_required
    def delete2(user_id):
        user = delete_user(user_id)
        if user:
            return jsonify({'result': 'User deleted'})
        return jsonify({'error': 'User not found'}), 404