from flask import Flask, request, jsonify, session, make_response
from flask_session import Session
from flask_bcrypt import Bcrypt
from functools import wraps
from config import ApplicationConfig
from models.databaseconfig import db
from models import Admin, Asset, Request, Employee
import os

app = Flask(__name__)
app.config.from_object(ApplicationConfig)

# Initialize Flask-Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Initialize Flask-Session for session management
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Initialize SQLAlchemy database
db.init_app(app)

# Hardcoded user credentials for demonstration purposes
user_credentials = {'email': 'Klif@example.com', 'password': '5100'}

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            return jsonify({'message': 'This is a protected page'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Route for home page (protected by login)
@app.route('/')
@login_required
def home():
    return jsonify({'username': 'admin', 'password': 'password'})

# Route for user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if email != user_credentials['email'] or password != user_credentials['password']:
        return jsonify({'message': 'Invalid credentials'}), 401
    resp = make_response(jsonify({'message': 'Login successful'}), 200)
    session['email'] = email  # Store email in session
    print(session)
    return resp

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if email != user_credentials['email'] or password != user_credentials['password']:
        return jsonify({'message': 'Invalid credentials'}), 401
    # Set a cookie to mark the user as authenticated
    resp = make_response(jsonify({'message': 'Login successful'}), 200)
    session['email'] = email  # Store email in session
    print(session)
    return resp

# Route for user logout
@app.route('/logout')
def logout():
    resp = make_response(jsonify({'message': 'Logout successful'}), 200)
    session.pop('email', None)  # Remove email from session
    return resp

# Route for adding a new asset by admin
@app.route('/assets/add', methods=['POST'])
@login_required
def add_asset():
    data = request.get_json()
    if 'admin' in session:
        new_asset = Asset(name=data['name'], category=data['category'])
        db.session.add(new_asset)
        db.session.commit()
        return jsonify({'message': 'Asset added successfully'})
    else:
        return jsonify({'message': 'Unauthorized access'}), 403

# Route for updating an existing asset by admin
@app.route('/assets/update/<int:asset_id>', methods=['PUT'])
@login_required
def update_asset(asset_id):
    data = request.get_json()
    asset = Asset.query.get(asset_id)
    if asset:
        if 'admin' in session:
            asset.name = data.get('name', asset.name)
            asset.category = data.get('category', asset.category)
            db.session.commit()
            return jsonify({'message': 'Asset updated successfully'})
        else:
            return jsonify({'message': 'Unauthorized access'}), 403
    else:
        return jsonify({'message': 'Asset not found'}), 404

# Route for removing an asset by admin
@app.route('/assets/remove/<int:asset_id>', methods=['DELETE'])
@login_required
def remove_asset(asset_id):
    asset = Asset.query.get(asset_id)
    if asset:
        if 'admin' in session:
            db.session.delete(asset)
            db.session.commit()
            return jsonify({'message': 'Asset removed successfully'})
        else:
            return jsonify({'message': 'Unauthorized access'}), 403
    else:
        return jsonify({'message': 'Asset not found'}), 404

# Route for approving a request by admin
@app.route('/requests/approve/<int:request_id>', methods=['PUT'])
@login_required
def approve_request(request_id):
    request_item = Request.query.get(request_id)
    if request_item:
        if 'admin' in session:
            request_item.status = 'approved'
            db.session.commit()
            return jsonify({'message': 'Request approved successfully'})
        else:
            return jsonify({'message': 'Unauthorized access'}), 403
    else:
        return jsonify({'message': 'Request not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
