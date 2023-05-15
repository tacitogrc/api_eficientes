from app_security.domain.user.model.UserModel import User
from app_security.infrastructure.database.sqlite import db

def create_user(name, email):
    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def get_user(user_id):
    return User.query.get(user_id)

def get_all_users():
    return User.query.all()

def update_user(user_id, name=None, email=None):
    user = User.query.get(user_id)
    if user:
        if name:
            user.name = name
        if email:
            user.email = email
        db.session.commit()
    return user

def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return user
