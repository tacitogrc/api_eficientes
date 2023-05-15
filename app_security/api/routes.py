import json

from flask import Flask, jsonify, request, Response
from app_security.domain.user.User import create_user, get_user, get_all_users, update_user, delete_user
from app_security.domain.user.model.UserModel import User
from app_security.infrastructure.database.sqlite import db
from app_security.api.auth import encode_auth_token, token_required

def register_routes(app):
    
    @app.route('/api/v1/index', methods=['POST'])
    def index():
        return jsonify({'data': 'Hello API World!'}), 200
