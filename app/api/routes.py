from flask import Flask, jsonify, request
from app.domain.user.User import create_user, get_user, get_all_users, update_user, delete_user
from app.infrastructure.database.sqlite import db


def register_routes(app):
    
    @app.route('/users', methods=['POST'])
    def create():
        data = request.get_json()
        name, email = data['name'], data['email']
        user = create_user(name, email)
        return jsonify({'user': str(user)}), 201

    @app.route('/users', methods=['GET'])
    def get_all():
        users = get_all_users()
        return jsonify({'users': [str(user) for user in users]})

    @app.route('/users/<int:user_id>', methods=['GET'])
    def get_one(user_id):
        user = get_user(user_id)
        if user:
            return jsonify({'user': str(user)})
        return jsonify({'error': 'User not found'}), 404

    @app.route('/users/<int:user_id>', methods=['PUT'])
    def update(user_id):
        data = request.get_json()
        name, email = data.get('name'), data.get('email')
        user = update_user(user_id, name, email)
        if user:
            return jsonify({'user': str(user)})
        return jsonify({'error': 'User not found'}), 404

    @app.route('/users/<int:user_id>', methods=['DELETE'])
    def delete(user_id):
        user = delete_user(user_id)
        if user:
            return jsonify({'result': 'User deleted'})
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)




'''
    @app.route('/')
    def index():
        pass

    @app.route('/users')
    def index():
        users = query.order_by(id).all()
        if len(users) == 0:
            abort(404)    
            return jsonify({
                'success': True,
                'users': users
            })
            
    @app.route('/users')
    def index():
        users = query.order_by(id).all()
        if len(users) == 0:
            abort(404)    
            return jsonify({
                'success': True,
                'users': users
            })
            
    # store        
    @app.route('/users', methods=['POST'])
    def store():
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)    
        try:
            user = User(name=name, age=age)
            create()        
            return jsonify({
                'success': True,
                'created': format()
            })
        except:
            abort(422)

    #show  
    @app.route('/users/<int:user_id>')
    def show(user_id):
        user = query.filter(id == user_id).one_or_none()
        if user is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'user': format()
            })

    #update
    @app.route('/users/<int:user_id>', methods=['PATCH'])
    def update(user_id):
        body = request.get_json()    
        try:
            user = query.filter(id == user_id).one_or_none()
            if user is None:
                abort(404)        
                if 'name' in body:
                    name = body.get('name')        
                    update()        
                    return jsonify({
                        'success': True,
                        'updated': format()
                    })
        except:
            abort(422)
            
    #destroy
    @app.route('/users/<int:user_id>', methods=['DELETE'])
    def destroy(user_id):
        try:
            user = query.filter(id == user_id).one_or_none()
            if user is None:
                abort(404)        
                delete()        
                return jsonify({
                    'success': True,
                    'deleted': format()
            })
        except:
            abort(422)
'''