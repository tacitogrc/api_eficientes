from flask import Flask, request, jsonify
from app.infrastructure.database.sqlite import db
from app.api.routes import register_routes


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    register_routes(app)
    db.init_app(app)
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)



