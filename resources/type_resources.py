from flask_restful import Resource, reqparse
from models import type
from flask_jwt_extended import (jwt_required)

type_body = reqparse.RequestParser()
type_body.add_argument('name', help='This field cannot be blank', required=True)


class AddType(Resource):
    @jwt_required
    def post(self):
        data = type_body.parse_args()

        new_type = type.TypeModel(
            name=data['name'],
        )

        try:
            new_type.save_to_db()
            return {
                'message': 'Type Wallets {} was created'.format(data['name'])
            }
        except:
            return {'message': 'Something went wrong'}, 500

