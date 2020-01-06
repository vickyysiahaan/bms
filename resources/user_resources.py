from app import db
from flask import request
from flask_restful import Resource
from models.users import User, UserSchema
from models import revoked_tokens
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt, get_jwt_claims)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class UserListResource(Resource):
    # User Registration
    def post(self):
        try:
            if User.find_by_username(request.json["username"]):
                return {'message': 'User {} already exists'.format(request.json["username"])}

            new_user = User(
                username=request.json['username'],
                password=User.generate_hash(request.json['password']),
                full_name=request.json['full_name'],
                email=request.json['email'],
                department=request.json['department'],
                position=request.json['position']
            )

            db.session.add(new_user)
            db.session.commit()

            return {
                'message': 'User {} was created'.format(new_user.username)
            }

        except:
            return {'message': 'Something went wrong'}, 500

    # Get All Users
    def get(self):
        users = User.query.all()
        return users_schema.dump(users)

class UserResource(Resource):
    # Get User Data by ID
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user_schema.dump(user)

    # Edit User Data by ID
    def patch(self, user_id):
        try:
            user = User.query.get_or_404(user_id)

            if 'full_name' in request.json:
                user.full_name = request.json['full_name']
            if 'email' in request.json:
                user.full_name = request.json['email']
            if 'department' in request.json:
                user.department = request.json['department']
            if 'position' in request.json:
                user.position = request.json['position']

            db.session.commit()
            return user_schema.dump(user)
        except:
            return {'message': 'Something went wrong'}, 500

    # Delete User Data by ID
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return 'SUCCESSFULL', 204

class UserLogin(Resource):
    # User Login Authentication
    def post(self):
        current_user = User.find_by_username(request.json['username'])
        _current_user = {
            "id" : current_user.id,
            "username": current_user.username
        }

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(request.json['username'])}

        if User.verify_hash(request.json['password'], current_user.password):
            access_token = create_access_token(identity=_current_user)
            refresh_token = create_refresh_token(identity=_current_user)
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'Wrong credentials'}


class UserLogoutAccess(Resource):
    # User Logout Authentication
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = revoked_tokens.RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = revoked_tokens.RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        user_claims = get_jwt_claims()
        print(user_claims)
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }
