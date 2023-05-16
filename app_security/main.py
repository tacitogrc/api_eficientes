from flask import Flask, request, jsonify
from app_security.infrastructure.database.sqlite import db
from app_security.api.routes import register_routes as routes_base
from app_security.api.routes_v1 import register_routes as routes_v1
from app_security.api.routes_v2 import register_routes as routes_v2

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    routes_base(app)
    routes_v1(app)
    routes_v2(app)
    db.init_app(app)
    # db.create_all()
    
    with app.app_context():
        db.create_all()
        
    return app


app = create_app()

# @app.before_first_request
# def create_tables():
#     db.create_all()

if __name__ == '__main__':
    app.run(debug=True)



