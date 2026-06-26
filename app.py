from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'codec_project_secret'

users = {}

@app.route('/')
def home():
    return "Secure Authentication System Running"

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data['username']
    password = data['password']

    if username in users:
        return jsonify({"message": "User already exists"}), 400

    users[username] = generate_password_hash(password)

    return jsonify({"message": "Registration Successful"})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data['username']
    password = data['password']

    if username not in users:
        return jsonify({"message": "User not found"}), 404

    if not check_password_hash(users[username], password):
        return jsonify({"message": "Invalid Password"}), 401

    token = jwt.encode(
        {
            'user': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )

    return jsonify({"token": token})

@app.route('/protected')
def protected():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"message": "Token Missing"}), 401

    try:
        jwt.decode(
            token,
            app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        return jsonify({"message": "Access Granted"})
    except:
        return jsonify({"message": "Invalid Token"}), 401

if __name__ == '__main__':
    app.run(debug=True)