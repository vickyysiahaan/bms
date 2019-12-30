from flask_restful import Resource, reqparse
from models import users, revoked_tokens, contact
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt, get_jwt_claims)

parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)
parser.add_argument('role', help='This field cannot be blank', required=True)

login = reqparse.RequestParser()
login.add_argument('username', help='This field cannot be blank', required=True)
login.add_argument('password', help='This field cannot be blank', required=True)


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()

        if users.UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}

        new_user = users.UserModel(
            username=data['username'],
            password=users.UserModel.generate_hash(data['password']),
            role=data['role']
        )

        new_contact = contact.ContactModel(
            first_name="",
            last_name="",
            email="",
            phone="",
            job="",
            salary="",
            photo=None,
            users=new_user
        )

        try:
            new_user.save_to_db()
            new_contact.save_to_db()
            return {
                'message': 'User {} was created'.format(data['username'])
            }
        except:
            return {'message': 'Something went wrong'}, 500

class UserLogin(Resource):
    def post(self):
        data = login.parse_args()
        current_user = users.UserModel.find_by_username(data['username'])
        _current_user = {
            "id" : current_user.id,
            "username": current_user.username,
            "role": current_user.role
        }

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}


        if users.UserModel.verify_hash(data['password'], current_user.password):
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


class AllUsers(Resource):
    @jwt_required
    def get(self):
        try:
            return users.UserModel.return_all()
        except:
            raise
            return {'message': 'Something went wrong'}, 500

    @jwt_required
    def delete(self):
        return users.UserModel.delete_all()


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }
