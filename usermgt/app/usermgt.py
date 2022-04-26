from flask import request, jsonify, make_response
from config import Config
import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
import jwt
from functools import wraps


from database import app, db
from database.models import User, BlacklistToken


app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.TRACK_MODIFICATIONS

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message' : 'Token is missing'}), 401
        try:
            res = BlacklistToken.check_blacklist(token)
            if res:
                return jsonify({'message' : 'Token is invalid'}), 401
            data = jwt.decode(token,Config.SECRET_KEY)
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid'}), 401
        return f(current_user, *args,**kwargs)
    return decorated        




@app.route('/validateAccess',methods=['GET'])
@token_required
def validate_access(current_user):
    
    return jsonify({'id' : current_user.public_id}), 200



@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authentication' :  'Basic realm= "Login required"'})

    user =User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authentication' :  'Basic realm= "Login required"'})
    if check_password_hash(user.password,auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},Config.SECRET_KEY  )
        return jsonify({'token': token.decode('UTF-8')})
    return make_response('Could not verify', 401, {'WWW-Authentication' :  'Basic realm= "Login required"'})


@app.route('/logout',methods=['DELETE'])
@token_required
def logout(current_user):
    auth_token = request.headers['x-access-token']
    blacklist_token = BlacklistToken(token=auth_token)
    db.session.add(blacklist_token)
    db.session.commit()    
    return jsonify({'message' : 'User has been Deleted'})

@app.route('/user',methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'],method='sha256')
    new_user = User(public_id=str(uuid.uuid4()),username=data['username'],email=data['email'],password=hashed_password,admin=False,custid = data['custid'],deleted =False,created_on=datetime.datetime.utcnow())
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New User Created!'})

@app.route('/user',methods=['GET'])
@token_required
def get_all_users(current_user):
    if not current_user.admin:
        return jsonify({'message':'Can not perform action'})
    users = User.query.all()
    output = []  # finall output
    for user in users:
        user_data = {} # create a new dictionary for each user
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['admin']= user.admin
        user_data['custid'] = user.custid
        user_data['email'] = user.email
        output.append(user_data)
    return jsonify({'users':output})

@app.route('/user/<custid>',methods=['GET'])
@token_required
def get_all_users_custid(current_user,custid):
    if not current_user.admin:
        return jsonify({'message':'Can not perform action'})
    users = User.query.filter_by(custid=custid).all()
    output = []  # finall output
    for user in users:
        user_data = {} # create a new dictionary for each user
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['admin']= user.admin
        user_data['custid'] = user.custid
        user_data['email'] = user.email
        output.append(user_data)
    return jsonify({'users':output})


@app.route('/user/<username>',methods=['GET'])
@token_required
def get_user(current_user,username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify ({'message' : 'No User Found'})
    user_data = {} # create a new dictionary for each user
    user_data['public_id'] = user.public_id
    user_data['username'] = user.username
    user_data['admin']= user.admin
    user_data['custid'] = user.custid
    user_data['email']= user.email

    return jsonify({'users':user_data})


# @app.route('/user/<public_id>',methods=['GET'])
# @token_required
# def get_user(current_user,public_id):
#     user = User.query.filter_by(public_id=public_id).first()
#     if not user:
#         return jsonify ({'message' : 'No User Found'})
#     user_data = {} # create a new dictionary for each user
#     user_data['public_id'] = user.public_id
#     user_data['username'] = user.username
#     user_data['admin']= user.admin
#     user_data['custid'] = user.password
#     user_data['email']= user.email

#     return jsonify({'users':user_data})


@app.route('/user/<public_id>',methods=['PUT'])
@token_required
def update_user(current_user,public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify ({'message' : 'No User Found'})
    data = request.get_json()
    user.email = data['email']
    user.admin = data['admin']
    db.session.commit()    
    return jsonify({'message' : 'User is Promoted'})

# @app.route('/user/changepass/<public_id>',methods=['PUT'])
# @token_required
# def promote_user(current_user,public_id):
#     user = User.query.filter_by(public_id=public_id).first()
#     if not user:
#         return jsonify ({'message' : 'No User Found'})
#     data = request.get_json()
#     hashed_password = generate_password_hash(data['password'],method='sha256')
#     user.password = hashed_password
#     db.session.commit()    
#     return jsonify({'message' : 'User is Promoted'})


@app.route('/user/changepass/<username>',methods=['PUT'])
@token_required
def promote_user(current_user,username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify ({'message' : 'No User Found'})
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'],method='sha256')
    user.password = hashed_password
    db.session.commit()    
    return jsonify({'message' : 'User is Promoted'})


@app.route('/user/<public_id>',methods=['DELETE'])
@token_required
def delete_user(current_user,public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify ({'message' : 'No User Found'})
    #db.session.delete(user)
    user.deleted = True
    db.session.commit()    
    return jsonify({'message' : 'User has been Deleted'})



if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=6200)    

