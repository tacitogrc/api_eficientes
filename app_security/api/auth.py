import jwt
import datetime
from functools import wraps
from flask import request, jsonify

SECRET_KEY = 'your_secret_key_here'
ALGORITHM = 'HS256'
TOKEN_EXPIRATION_MINUTES = 30

def encode_auth_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRATION_MINUTES),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Token expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace('Bearer ', '')

        if not token:
            return jsonify({'error': 'Token is missing'}), 403

        decoded_token = decode_auth_token(token)
        if isinstance(decoded_token, str):
            return jsonify({'error': decoded_token}), 403

        return f(decoded_token, *args, **kwargs)

    return decorated
