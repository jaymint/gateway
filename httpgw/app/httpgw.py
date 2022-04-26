from flask import Flask,request, jsonify, make_response
#from config import Config
import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from functools import wraps
from flask_cors import CORS
from publisher.publish import MQ
from publisher.config import Config
import json



app = Flask(__name__)
CORS(app)


pub = MQ()
pub.connect()

@app.route('/v1/publishdata/event',methods=['POST'])
def publisheventdata():
    data = request.get_json()
    pub.sendMQ(Config.EVENTRKEY,json.dumps(data))
    return jsonify({'message': 'Data Published on RQ!'})



@app.route('/v1/publishdata/snapshot',methods=['POST'])
def publishsnapshotdata():
    data = request.get_json()
    pub.sendMQ(Config.SNAPSHOTRKEY,json.dumps(data))
    return jsonify({'message': 'Data Published on RQ!'})

def main():
    app.run(debug=True,host='0.0.0.0',port=6199)
if __name__=='__main__':
    main()    

