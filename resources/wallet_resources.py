from flask_restful import Resource, reqparse
from models import wallets
from flask_jwt_extended import (jwt_required, get_jwt_claims)

wallet_body = reqparse.RequestParser()
wallet_body.add_argument('name', help='This field cannot be blank', required=True)
wallet_body.add_argument('amount', help='This field cannot be blank', required=True)
wallet_body.add_argument('type_id', help='This field cannot be blank', required=True)


class AddWallet(Resource):
    @jwt_required
    def post(self):
        data = wallet_body.parse_args()
        current_user = get_jwt_claims()
        new_wallet = wallets.WalletModel(
            name=data['name'],
            amount=data['amount'],
            user_id= current_user['id'],
            type_id=data['type_id'],
        )

        try:
            new_wallet.save_to_db()
            return {
                'message': 'Wallets {} was created'.format(data['name'])
            }
        except:
            raise
            return {'message': 'Something went wrong'}, 500

class Allwallets(Resource):
    @jwt_required
    def get(self):
        try:
            return wallets.WalletModel.return_all()
        except:
            return {'message': 'Something went wrong'}, 500

