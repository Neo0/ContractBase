# coding: utf-8
from flask import Flask
from flask import request
import jwt, Crypto.PublicKey.RSA as RSA, datetime

app = Flask(__name__)

database_user = {'root': 'toor'}
is_login = False


def token(username):
    global database_user
    key = RSA.generate(2048)
    priv_pem = key.exportKey()
    payload = {'url': 'neo0.xyz', 'name': username, 'level': 'low'}
    priv_key = RSA.importKey(priv_pem)
    access_token = jwt.generate_jwt(payload, priv_key, 'RS256', datetime.timedelta(minutes=5))
    return access_token


@app.route('/login', methods=('GET', 'POST'))
def login():
    global database_user
    global is_login
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in database_user:
            if database_user[username] == password:
                is_login = True
                return token(username)  # login success
            else:
                is_login = False
                return 2  # password error
        else:
            is_login = False
            return 3  # username error or need register


@app.route('/register', methods=('GET', 'POST'))
def register():
    global database_user
    username = request.form.get('username')
    password = request.form.get('password')
    if username in database_user:
        return False
    else:
        database_user[username] = password
        return True


if __name__ == '__main__':
    app.run(port=8000)
