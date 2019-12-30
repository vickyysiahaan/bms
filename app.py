from flask import Flask, jsonify
from config import Run
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config.from_object(Run)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return revoked_tokens.RevokedTokenModel.is_jti_blacklisted(jti)


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {
        'id': user["id"],
        'role': user["role"]
    }


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user["username"]


@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'The {} token has expired'.format(token_type)
    }), 401


from models import revoked_tokens
from routes import *

if __name__ == '__main__':
    app.run();
