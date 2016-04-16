# coding:utf-8
from flask import Flask
from flask import request
import jwt, Crypto.PublicKey.RSA as RSA, datetime

app = Flask(__name__)


@app.route('/', methods=('GET', 'POST'))
def m():
    if request.method == 'POST':
        access_token = request.form.get('access_token')
        key = RSA.generate(2048)
        pub_pem = key.publickey().exportKey()
        pub_key = RSA.importKey(pub_pem)
        header, claims = jwt.verify_jwt(access_token, pub_key, ['RS256'])


if __name__ == '__main__':
    app.run(debug=True, port=5000)
