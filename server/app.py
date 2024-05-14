from models.admin import Admin
from models.employee import Employee
from models.manager import Manager
from models.approved_asset import ApprovedAsset
from models.asset import Asset
from models.request import Request
from flask import Flask, make_response, request, redirect, url_for
from flask_migrate import Migrate



import jwt
from jwt import InvalidTokenError, ExpiredSignatureError
import os 
import base64

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
import random
import string
from models.init import db
from flask_cors import CORS
import bcrypt


app = Flask(__name__)
app.config['SWAGGAR'] = {
    'title':'Authentication and Authorisation for user',
    'uiversion': 3
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
secret_key = base64.b64encode(os.urandom(24)).decode('utf-8')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)

migrate = Migrate(app,db)

db.init_app(app)











@app.before_request
def check_if_logged_in():
    endpoint = request.endpoint
    

    if endpoint != 'login' and endpoint != 'logout' and endpoint != 'register':
        

       
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return redirect(url_for('logout'))
        auth_token = auth_header.split()[1]

        

        if not auth_token:
            return redirect(url_for('logout'))
        
        # clean token
        
        print('clean token is:', auth_token)


        payload = decode_token(auth_token)
        if isinstance(payload,str):
            return redirect(url_for('logout'))
    
   
def decode_token(token):
    
    try:
        print(token)
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return "The token is expired please login again"
    except jwt.InvalidTokenError:
        return "The token is invalid please login again"















@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    status = data.get('status')
   
    hashed_pass = generate_password_hash(password,method='pbkdf2:sha512')
   
    try:
        if status == 'manager':
            new_user = Manager(username=username,password=hashed_pass, email=email)
            db.session.add(new_user)
            db.session.commit()
        elif status == 'employee':
            
            new_user = Employee(username=username,password=hashed_pass, email=email)
            db.session.add(new_user)
            db.session.commit()
        elif status == 'admin':
            auth_code = data.get('authcode')
            if not auth_code:
                return make_response({'error':'No auth-code was given to register admin'}, 400)
            hashed_auth_code = bcrypt.hashpw(auth_code.encode('utf-8'), bcrypt.gensalt())
            

            new_user = Admin(username=username,password=hashed_pass, email=email, auth_code=hashed_auth_code)
            db.session.add(new_user)
            db.session.commit()
       
    except ValueError:
        return make_response({"error":'email, username or password is not valid, valueError'},400)
    except IntegrityError:
        return make_response({"error":'password, username or email not valid not valid, IntegrityError'},400)
    except:
        return make_response({"error":'password, username or email not valid not valid, ask engineer'},400)
    
    if not new_user:
        return make_response({'error':f'bad request form frontend, make validations'}, 400)

    print('new user',new_user)
    return make_response({'message':f'{status} has been registered'},200)
    

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    status = data.get('status')
    user = None
    

    

    
    if status == 'manager':

        user = Manager.query.filter_by(username=username).first()

        if not user:
            return make_response({'error':'username is not valid'}, 401)
        
        if not user.approved:
            return make_response({'error':f'{user.username} of status {status} is not approved'}, 401)

    if status == 'employee':
        user = Employee.query.filter_by(username=username).first()

        if not user:
            return make_response({'error':'username is not valid'}, 401)


        if not user.approved:
            return make_response({'error':f'{user.username} of status {status} is not approved'}, 401)
        
        


    if status == 'admin':
        auth_code = data.get('authcode')
        
        if not auth_code:
            print('up here')
            return make_response({'message':'auth-code to sign in as a admin was not given'}, 401)
        user = Admin.query.filter_by(username = username).first()

        if not user:
            
            return make_response({'error':'admin username is not valid'}, 401)
    
        if not bcrypt.checkpw(auth_code.encode('utf-8'), user.auth_code):
            
            return make_response({'error':'Invalid admin auth-code'}, 401)
        
    if not user:
        return make_response({'error':'bad request'}, 400)
    

    
    
    
    
    user.password = generate_password_hash(password,method='pbkdf2:sha512')

    if check_password_hash(user.password, password):
        expiration_time = datetime.utcnow() + timedelta(hours=3)
        token = jwt.encode({'user_id':user.id,'exp':expiration_time}, secret_key, algorithm='HS256')
        
        print('I run')
        return make_response({'message':f'{status} has logged in', 'token':token}, 200)
    
    else:
        print('wrong pass')
        return make_response({'error':'wrong password'},400)
    
@app.route('/approve', methods=['PATCH'])
def approve_emp():
    data = request.json
    username_to_approve = data.get('username')
    status_to_approve = data.get('status')
    
    if status_to_approve == 'employee':
        user = Employee.query.filter_by(username = username_to_approve).first()
    if status_to_approve == 'manager':
        user = Manager.query.filter_by(username = username_to_approve).first()
    
    if user is None:
        return make_response({'error':f"{status_to_approve} not found"}, 404)
    
    try:
        user.approved = True
        db.session.commit()
        return make_response({'message':f'{username_to_approve} of status {status_to_approve} has been approved'}, 200)
        
    except:
        return make_response({'error':"something went wrong ask engineeer"}, 500)

    

    
@app.route('/peopletoapprove', methods=['GET'])
def get_pople_to_approve():
    
    managers = Manager.query.filter(Manager.approved == False).all()
    employees = Employee.query.filter(Employee.approved == False).all()

    if not managers and not employees:
        print(managers, employees)
        return make_response({}, 200)
    
    managers_to_return = []
    for manager in managers:
        manager_dict = manager.to_dict()
        managers_to_return.append(manager_dict)

    employees_to_return = []
    for employee in employees:
        employee_dict = employee.to_dict()
        employees_to_return.append(employee_dict)

   

    people_to_return = {
        'maagers': managers_to_return,
        'employees':employees_to_return
    }
    return make_response(people_to_return, 200)

@app.route('/logout', methods=['GET'])
def logout(): 
    
    return make_response({'message':'send user back to login page'})



@app.route('/protected_route', methods=['GET'])
def protected_routes(): 
    
    return make_response({'message':'this is protected'}, 303)


@app.route('/assets', methods=['GET', 'POST'])
def assets():
    if request.method == 'GET':
        assets = Asset.query.all()
        if not assets:
            return make_response({'message':'There are no assets'})
        assets_to_return = [asset.to_dict() for asset in assets]
        return make_response(assets_to_return, 200)
    if request.method == 'POST':
        data = request.json
        name = data.get('name')
        stock = data.get('stock')
        if not stock:
            stock = 1
    
        asset = Asset.query.filter_by(name = name).first()

        if not asset:
            
            category = data.get('category')
            condition = data.get('condition')
            image_url = data.get('image-url')
            if not image_url or not condition or not category:
                if not asset:
                    
                    return make_response('asset not posted beacuse invalid request data', 400)
            asset = Asset(name=name, category=category, condition=condition, image_url=image_url, stock=stock)
            db.session.add(asset)
            db.session.commit()
            return make_response('asset(s) has been posted', 201)
        
    
        asset.stock = asset.stock + stock
        db.session.commit()
        
        return make_response('asset(s) has been posted', 201)

@app.route('/assets/<int:id>', methods=['GET','PATCH'])
def asset_by_id(id):
    asset = Asset.query.filter_by(id=id).first()
    if not asset:
            return make_response('asset not found', 404)
    if request.method == 'GET':
        asset_dict = asset.to_dict()

        return make_response(asset_dict, 200)
    if request.method == 'PATCH':
        data = request.json
        new_stock = data.get('stock')
        if not new_stock:
            return make_response('no  new stock value was given', 400)
        try:
            stock_int = int(new_stock)
        except:
            return make_response('Not a vaild new value for stock of an asset')
        asset.stock = stock_int 
        db.session.commit()
        asset_dict = asset.to_dict()
        return make_response(asset_dict, 200)
    


@app.route('/managers/<int:id>', methods=['GET'])
def get_manager_by_id(id):
    manager = Manager.query.filter_by(id = id).first()

    if not manager:
        return make_response('manager not found', 404)
    
    manager_dict = manager.to_dict()
    return make_response(manager_dict, 200)

@app.route('/employees/<int:id>', methods=['GET'])
def get_employee_by_id(id):
    employee = Employee.query.filter_by(id = id).first()

    if not employee:
        return make_response('employee not found', 404)
    
    employee_dict = employee.to_dict()
    return make_response(employee_dict, 200)

@app.route('/admins/<int:id>', methods=['GET'])
def get_admin_by_id(id):
    admin = Admin.query.filter_by(id = id).first()

    if not admin:
        return make_response('admin not found', 404)
    
    admin_dict = admin.to_dict()
    return make_response(admin_dict, 200)




@app.route('/requests', methods=['GET','POST'])
def requests():
    if request.method == 'GET':
        reqs = Request.query.all()
        reqs_to_return = [req.to_dict() for req in reqs]
        
        return make_response(reqs_to_return, 200)
    
    if request.method == 'POST':
        data = request.json
        asset_id = data.get('asset-id')
        employee_id = data.get('employee-id')
        reason = data.get('reason')
        quantity = data.get('quantity')
        urgency = data.get('urgency')

        things = [asset_id, employee_id, reason, quantity, urgency]
        for thing in things:
            if not thing:
                return make_response('missing fields required to post a request, validate on frontend', 400)
        try:

            req = Request(asset_id=asset_id, employee_id=employee_id, reason=reason, quantity=quantity, urgency=urgency)
        except IntegrityError:
            return make_response('Employee or asset does not exist', 400)
        

        return make_response(req.to_dict(), 201)
    



            

        


    


        
    
    
        



    
    
       
            


    






























































# # app.py
# from flask import Flask, jsonify, make_response, redirect, request, session, url_for
# from functools import wraps
# from flask_cors import CORS
# from flask_migrate import Migrate
# from flask_session import Session
# from config import ApplicationConfig
# from models.databaseconfig import db
# from flask_bcrypt import Bcrypt
# import os

# app = Flask(__name__)
# app.config.from_object(ApplicationConfig)

# CORS(app, supports_credentials=True)
# bcrypt = Bcrypt(app)
# migrate = Migrate(app, db)
# server_session = Session(app)
# db.init_app(app)

# from models import admin, assets, requests, employee
# user_name = 'Klif'
# pass_word = '5100'

# app.secret_key = os.urandom(24)
# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         # username = session['username']
#         # print(username)
#         if 'username' not in session:
#             return jsonify({'message': 'This is a protected page'})
#             # return redirect(url_for('login'))
#         return f(*args, **kwargs)
#     return decorated_function

# @app.route('/')
# @login_required
# def home():
#     return jsonify({'username': 'admin', 'password': 'password'})

# @app.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     if email != user_name or password != pass_word:
#         return jsonify({'message': 'Invalid credentials'}), 401

#     resp = make_response(jsonify({'message': 'Login successful'}), 200)
#     session['email'] = email  # Store email in session
#     print(session)
#     return resp

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     if email != user_name or password != pass_word:
#         return jsonify({'message': 'Invalid credentials'}), 401

#     # Set a cookie to mark the user as authenticated
#     resp = make_response(jsonify({'message': 'Login successful'}), 200)
#     session['email'] = email  # Store email in session
#     print(session)
#     return resp

# @app.route('/logout')
# def logout():
#     resp = make_response(jsonify({'message': 'Logout successful'}), 200)
#     session.pop('email', None)  # Remove username from session
#     return resp

# if __name__ == '__main__':
#     app.run(debug=True)
