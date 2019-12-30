from app import app
from resources import wallet_resources
from flask_restful import Api

api = Api(app)

api.add_resource(wallet_resources.AddWallet, '/wallets')
api.add_resource(wallet_resources.Allwallets, '/wallets')