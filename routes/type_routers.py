from app import app
from resources import type_resources
from flask_restful import Api

api = Api(app)
api.add_resource(type_resources.AddType, '/type-wallets')
